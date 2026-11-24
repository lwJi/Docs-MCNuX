---
name: summarize-doc
description: Turn a finished MCNuX discussion into Docs-MCNuX docs. Decides the doc split, drafts each doc in the template for review, and after approval writes the docs, the README lines, the references and the Known list, then runs the lint script. Use whenever the user says they are ready to summarize, record, write up or capture a discussion in this repo, approves drafts for writing, or invokes /summarize-doc, even if they do not name the skill.
---

# Summarize a discussion into docs

This skill is the procedure. The rules that define a good doc live in the repo `CLAUDE.md`: content rules, style, layout and assumed background. Follow them, and do not restate or override them here. If a rule and this skill disagree, `CLAUDE.md` wins.

The work has two phases with an approval gate between them. Phase 1 writes nothing to the repo.

## Phase 1: Draft

1. **Load the fixed context.** Read `conventions.md`, `references.md` and `README.md`, and list the existing docs. This prevents three common faults: redefining a symbol that conventions already owns, citing a paper that is not registered, and writing a doc that duplicates or fails to link an existing one.

2. **Pin the MCNuX state.** In the MCNuX checkout (`../../repos/MCNuX`), record the short commit and the branch, and test whether the commit is on the default branch:

   ```bash
   git -C ../../repos/MCNuX rev-parse --short HEAD
   git -C ../../repos/MCNuX merge-base --is-ancestor HEAD origin/main && echo merged || echo unmerged
   ```

   A commit from an open PR can vanish in a rebase or squash, and then `verified-against` points at nothing. For an unmerged commit, fill `verified-branch` with the branch and PR number, and say so when presenting the drafts.

3. **Harvest the discussion.** Collect, from the conversation itself:
   - each headline result,
   - every step the user asked about, since those steps get the full derivation and the rest get key steps only,
   - what the user misread at first, which belongs in Pitfalls,
   - spec ids, and any place where code and spec disagree,
   - every numeric value with its unit.

4. **Decide the split.** One doc holds one headline result. The test: the summary callout answers the question with one statement or one formula. If it needs two, split. Order the docs by dependency, and express the dependency in `builds-on`. Pick the area folder from the table in `README.md` and a kebab-case slug that is unique in the repo. Draft directly; do not stop to ask about the split. State the split in one line above the drafts, so the user can redirect at review.

5. **Fix the terms.** Wording drifts during a discussion, for example "error bar", "sigma" and "standard error" for one quantity. Choose one term per concept before drafting, and prefer the term that conventions or the specs already use.

6. **Draft and lint.** Copy `assets/doc-template.md` for each doc and write the draft into the session scratchpad as `<area>/<slug>.md`. Lint the drafts and fix them until no errors remain:

   ```bash
   python3 .claude/skills/summarize-doc/scripts/lint_docs.py --draft <scratchpad>/<area>/<slug>.md
   ```

   Then read each draft once for what the script cannot judge: active voice, noun clusters of three words or fewer, a unit on every dimensional number, no code-side names, and no narrative of the discussion.

7. **Present for review, then stop.** Show in chat:
   - the split, in one line,
   - each draft in full, with its frontmatter in a `yaml` block so the body renders,
   - what else the write phase will change: the README lines, new rows in `references.md`, and changes to the Known and Gaps lists,
   - choices worth a second look, such as a renamed term or an unmerged commit.

   Wait for the user's approval. A doc is meant to be re-read cold months later, so the user checks it while the discussion is still fresh.

## Phase 2: Write

Start this phase only after the user approves the drafts. If this skill's text is no longer in context, load it again first.

1. Apply any revisions the user asked for, and lint the drafts again.
2. Write each doc to `<area>/<slug>.md`. Create the area folder if this is its first doc.
3. Update `README.md`: add the area heading if it is new, and one line per doc with its link and its one-sentence takeaway.
4. Register each new paper in `references.md`.
5. Update the Known and Gaps lists in `CLAUDE.md`. Move a topic to Known only when the discussion showed the user now holds it; a broad gap stays listed.
6. Lint the repo, without `--draft`, and fix every error:

   ```bash
   python3 .claude/skills/summarize-doc/scripts/lint_docs.py
   ```

7. Report the files written, the lint result including warnings, and what is unchecked, such as the rendering in Obsidian. Do not commit unless the user asks.

## The lint script

`scripts/lint_docs.py` reads the required frontmatter keys and sections from `assets/doc-template.md`, so a change to the template changes the check with it.

| Level | What it checks |
|---|---|
| error | frontmatter keys, `area` matching the folder, date format, commit id format |
| error | one level-1 heading, required sections in template order, question and summary callouts |
| error | sentences of 25 words or fewer, paragraphs of six sentences or fewer, a summary of two to four sentences |
| error | wikilink targets, kebab-case unique file names, the README line, papers registered in `references.md` |
| error | "In MCNuX" lines that start with a spec id |
| warning | a commit that is not on the MCNuX default branch without `verified-branch` |
| warning | spec ids missing from the MCNuX specs, or differing between frontmatter and the "In MCNuX" section |
| warning | backtick spans that look like file paths, functions or APIs |

Inline math counts as one word, and display math is ignored. Run the script after any later edit to a doc as well, not only inside this skill.

## The template

`assets/doc-template.md` is the only copy of the template. Notes on filling it:

- `specs` lists the same spec ids as the "In MCNuX" section.
- `verified-branch` appears only while the commit is unmerged. Remove the line once the commit reaches the default branch.
- Pitfalls and "In MCNuX" are optional. Omit an optional section that would be empty.
- References holds arXiv ids with equation numbers. For a standard result with no paper, say so in one line.
