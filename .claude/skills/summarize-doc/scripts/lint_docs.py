#!/usr/bin/env python3
"""Lint Docs-MCNuX docs against the mechanical rules of CLAUDE.md.

Usage, from the repo root:
  python3 .claude/skills/summarize-doc/scripts/lint_docs.py            # every doc in the repo
  python3 .claude/skills/summarize-doc/scripts/lint_docs.py a/b.md     # selected docs
  python3 .../lint_docs.py --draft <dir>/<area>/<slug>.md ...          # drafts outside the repo

Errors are rule violations and give exit status 1. Warnings need a human look.
The required frontmatter keys and sections come from assets/doc-template.md,
so the template is the single place that defines the doc shape.

Not checked, because a script cannot judge them: active voice, noun clusters,
units on every number, one term per concept, and narrative of the discussion.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
TEMPLATE = SKILL / "assets" / "doc-template.md"
SKIP_DIRS = {".git", ".obsidian", ".claude"}
MAX_WORDS = 25
MAX_SENTENCES = 6
SUMMARY_SENTENCES = (2, 4)


def split_frontmatter(text):
    """Return (ordered key -> raw value, body, number of lines before the body)."""
    if not text.startswith("---\n"):
        return None, text, 0
    end = text.find("\n---", 4)
    if end < 0:
        return None, text, 0
    keys = {}
    for line in text[4:end].splitlines():
        m = re.match(r"([A-Za-z][A-Za-z-]*):\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip()
    rest = text[end + 4:]
    body = rest[1:] if rest.startswith("\n") else rest
    return keys, body, text[: len(text) - len(body)].count("\n")


def load_template():
    keys, body, _ = split_frontmatter(TEMPLATE.read_text())
    required = [k for k, v in keys.items() if not v.startswith("<optional")]
    optional = [k for k, v in keys.items() if v.startswith("<optional")]
    sections = []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            nxt = next((l for l in lines[i + 1:] if l.strip()), "")
            sections.append((line[3:].strip(), nxt.startswith("Optional")))
    return required, optional, sections


def blank(match):
    return "\n" * match.group(0).count("\n")


def units(body):
    """Yield (line, kind, text) for each paragraph, list item and callout."""
    out, cur, kind, start = [], [], None, 0

    def flush():
        nonlocal cur, kind
        if cur:
            out.append((start, kind, " ".join(cur)))
        cur, kind = [], None

    for n, raw in enumerate(body.split("\n"), 1):
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith("|"):
            flush()
            continue
        if s.startswith(">"):
            content = s.lstrip(">").strip()
            m = re.match(r"\[!(\w+)\][+-]?", content)
            if m:
                flush()
                kind, start = "callout:" + m.group(1).lower(), n
                content = content[m.end():].strip()
            elif kind is None or not kind.startswith(("callout", "quote")):
                flush()
                kind, start = "quote", n
            if content:
                cur.append(content)
            continue
        m = re.match(r"(?:[-*]|\d+\.)\s+(.*)", s)
        if m:
            flush()
            kind, start = "item", n
            cur.append(m.group(1))
            continue
        if kind == "item" and raw[:1] in (" ", "\t"):
            cur.append(s)
            continue
        if kind != "para":
            flush()
            kind, start = "para", n
        cur.append(s)
    flush()
    return out


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[(])", text)
    return [p for p in parts if re.search(r"\w", p)]


def words(sentence):
    return [t for t in sentence.split() if re.search(r"\w", t)]


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def mcnux_default_branch(repo):
    r = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if r.returncode == 0:
        return r.stdout.strip()
    for ref in ("origin/main", "origin/master", "main", "master"):
        if git(repo, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return ref
    return None


def repo_docs():
    docs = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if not SKIP_DIRS.intersection(rel.parts):
            docs.append(p)
    return docs


def lint(path, ctx, report):
    text = path.read_text()
    stem = path.stem

    def err(line, msg):
        report.append((path, line, "error", msg))

    def warn(line, msg):
        report.append((path, line, "warning", msg))

    # File name and place.
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.md", path.name) or re.match(r"\d+-", path.name):
        err(0, "file name is not a kebab-case concept slug without a number prefix")
    clashes = [p for p in ctx["all_md"] if p.stem == stem and p.resolve() != path.resolve()]
    if clashes:
        where = ", ".join(str(p.relative_to(ROOT)) for p in clashes)
        if ctx["draft"]:
            warn(0, f"a doc named {stem} already exists ({where}); fine only if this draft replaces it")
        else:
            err(0, f"file name is not unique across the repo (also {where})")

    # Frontmatter.
    keys, body, offset = split_frontmatter(text)
    if keys is None:
        err(1, "missing frontmatter")
        keys = {}
    for k in ctx["required_keys"]:
        if not keys.get(k):
            err(1, f"frontmatter lacks '{k}'")
    for k in keys:
        if k not in ctx["required_keys"] and k not in ctx["optional_keys"]:
            warn(1, f"frontmatter key '{k}' is not in the template")
    if keys.get("area") and keys["area"] != path.parent.name:
        err(1, f"area '{keys['area']}' does not match the folder '{path.parent.name}'")
    if keys.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", keys["date"]):
        err(1, "date is not YYYY-MM-DD")
    commit = keys.get("verified-against", "")
    if commit and not re.fullmatch(r"[0-9a-f]{7,40}", commit):
        err(1, "verified-against is not a short commit id")
    elif commit and ctx["mcnux"]:
        repo, default = ctx["mcnux"], ctx["mcnux_default"]
        if git(repo, "cat-file", "-e", commit + "^{commit}").returncode != 0:
            warn(1, f"commit {commit} is not in the MCNuX repo at {repo}")
        elif default:
            merged = git(repo, "merge-base", "--is-ancestor", commit, default).returncode == 0
            if not merged and not keys.get("verified-branch"):
                warn(1, f"commit {commit} is not on MCNuX {default}; add verified-branch, or re-verify after the merge")
            if merged and keys.get("verified-branch"):
                warn(1, f"commit {commit} is on MCNuX {default}; drop verified-branch")

    # Structure.
    plain = re.sub(r"```.*?```", blank, body, flags=re.S)
    plain = re.sub(r"\$\$.*?\$\$", blank, plain, flags=re.S)
    lines = plain.split("\n")
    if sum(1 for l in lines if l.startswith("# ")) != 1:
        err(offset + 1, "a doc has exactly one level-1 heading")
    found = [(l[3:].strip(), n) for n, l in enumerate(lines, 1) if l.startswith("## ")]
    names = [name for name, _ in found]
    known = [name for name, _ in ctx["sections"]]
    for name, optional in ctx["sections"]:
        if name not in names and not optional:
            err(offset + 1, f"missing section '{name}'")
    for name, n in found:
        if name not in known:
            warn(offset + n, f"section '{name}' is not in the template")
    order = [known.index(name) for name in names if name in known]
    if order != sorted(order):
        err(offset + 1, "sections are not in template order")

    # Code-side names.
    for n, line in enumerate(lines, 1):
        for span in re.findall(r"`([^`]+)`", line):
            if re.fullmatch(r"\[?MCNX-[A-Z]+-\d+\]?", span):
                continue
            if re.search(r"/|::|\(|_|\.\w{1,4}$", span):
                warn(offset + n, f"`{span}` looks like a code-side name; docs cite spec ids only")

    # Sentences and paragraphs.
    prose = re.sub(r"\$[^$\n]+\$", "X", plain)
    prose = re.sub(r"`[^`\n]+`", "C", prose)
    callouts = {}
    for n, kind, chunk in units(prose):
        sents = sentences(chunk)
        for s in sents:
            count = len(words(s))
            if count > MAX_WORDS:
                err(offset + n, f"sentence has {count} words (limit {MAX_WORDS}): {s[:60]}...")
        if len(sents) > MAX_SENTENCES:
            err(offset + n, f"paragraph has {len(sents)} sentences (limit {MAX_SENTENCES})")
        if kind.startswith("callout:"):
            callouts[kind[8:]] = (n, len(sents))
    for name in ("question", "summary"):
        if name not in callouts:
            err(offset + 1, f"missing [!{name}] callout")
    if "question" in callouts and callouts["question"][1] != 1:
        err(offset + callouts["question"][0], "the question callout is one sentence")
    if "summary" in callouts:
        n, count = callouts["summary"]
        lo, hi = SUMMARY_SENTENCES
        if not lo <= count <= hi:
            err(offset + n, f"the summary callout has {count} sentences (needs {lo} to {hi})")

    # Links, papers, spec ids.
    for n, line in enumerate(lines, 1):
        for target in re.findall(r"\[\[([^\]|#]+)", line):
            if target.strip() not in ctx["stems"]:
                err(offset + n, f"wikilink [[{target}]] has no target doc")
        for arxiv in re.findall(r"arXiv:(\d{4}\.\d{4,5})", line):
            if arxiv not in ctx["references"]:
                msg = f"arXiv:{arxiv} is not registered in references.md"
                (warn if ctx["draft"] else err)(offset + n, msg)
    section_ids = set()
    in_mcnux = False
    for n, line in enumerate(lines, 1):
        if line.startswith("## "):
            in_mcnux = line[3:].strip() == "In MCNuX"
            continue
        if in_mcnux and line.strip():
            m = re.match(r"- \[(MCNX-[A-Z]+-\d+)\]", line)
            if not m:
                err(offset + n, "an 'In MCNuX' line starts with '- [MCNX-...]'")
            else:
                section_ids.add(m.group(1))
    front_ids = set(re.findall(r"MCNX-[A-Z]+-\d+", keys.get("specs", "")))
    if "In MCNuX" in names and section_ids != front_ids:
        diff = ", ".join(sorted(section_ids ^ front_ids))
        warn(1, f"frontmatter specs and the 'In MCNuX' section differ: {diff}")
    for spec in sorted(section_ids | front_ids):
        if ctx["spec_text"] is not None and f"[{spec}]" not in ctx["spec_text"]:
            warn(1, f"[{spec}] does not appear in the MCNuX specs")

    # Index line.
    if not ctx["draft"] and f"[[{stem}]]" not in ctx["readme"]:
        err(0, "README.md has no line for this doc")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path, help="docs to lint (default: every doc in an area folder)")
    ap.add_argument("--draft", action="store_true", help="paths are drafts outside the repo: skip the README check")
    ap.add_argument("--mcnux", type=Path, default=ROOT / ".." / ".." / "repos" / "MCNuX", help="MCNuX checkout")
    args = ap.parse_args()

    all_md = repo_docs()
    if args.paths:
        targets = [p.resolve() for p in args.paths]
    else:
        targets = [p for p in all_md if len(p.relative_to(ROOT).parts) == 2]
    if not targets:
        print("no docs to lint")
        return 0

    required, optional, sections = load_template()
    refs = (ROOT / "references.md").read_text() if (ROOT / "references.md").exists() else ""
    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    mcnux = args.mcnux.resolve()
    spec_text = None
    if (mcnux / ".git").exists():
        spec_text = "".join(p.read_text() for p in sorted((mcnux / "specs").glob("*.md")))
    else:
        print(f"note: no MCNuX checkout at {mcnux}; commit and spec-id checks skipped")
        mcnux = None
    ctx = {
        "draft": args.draft,
        "all_md": all_md,
        "stems": {p.stem for p in all_md} | {p.stem for p in targets},
        "required_keys": required,
        "optional_keys": optional,
        "sections": sections,
        "references": set(re.findall(r"arXiv:(\d{4}\.\d{4,5})", refs)),
        "readme": readme,
        "mcnux": mcnux,
        "mcnux_default": mcnux_default_branch(mcnux) if mcnux else None,
        "spec_text": spec_text,
    }

    report = []
    for path in sorted(targets):
        if not path.exists():
            report.append((path, 0, "error", "file not found"))
            continue
        lint(path, ctx, report)

    report.sort(key=lambda r: (str(r[0]), r[1]))
    for path, line, level, msg in report:
        try:
            shown = path.relative_to(ROOT)
        except ValueError:
            shown = Path(path.parent.name) / path.name  # a draft: show <area>/<slug>.md
        print(f"{shown}:{line}: {level}: {msg}")
    errors = sum(1 for r in report if r[2] == "error")
    warnings = len(report) - errors
    print(f"{len(targets)} doc(s): {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
