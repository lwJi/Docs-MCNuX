# Docs-MCNuX

Companion notes for MCNuX (`../../repos/MCNuX`). The goal is recall: months later, a doc should bring back what was learned and why it mattered, without re-reading the code.

## Workflow

1. The user asks a question about MCNuX and we discuss it until the topic is understood. Read the MCNuX code and specs before making claims about behavior, and say so when the two disagree.
2. When the user says they are ready, summarize the discussion in the doc template for review.
3. Write to this repo only after the user approves the summary.

## Content rules

- Record durable content only: equations, derivations, models, assumptions, approximations, units and conventions.
- Leave out function names, file paths and APIs. The only code-side references are spec ids such as `[MCNX-GEO-03]`, in the "In MCNuX" section.
- Use the notation in [[conventions]]. A doc defines only symbols that are not listed there.
- Cite papers as arXiv id plus equation number, and register each new paper in [[references]].
- Derivations give the key steps. Write out in full only the steps the user asked about in discussion.

## Assumed background

Skip background on what is known; spend the words on the gaps. Update both lists as discussions reveal more.

- Known: 3+1 general relativity, basic radiative transfer.
- Gaps: Monte Carlo transport methods, weak-interaction microphysics.

## Style

- Obsidian only: `[[wikilinks]]`, callouts, `$...$` and `$$...$$` math.
- Plain declarative sentences in the present tense. No narrative of the discussion itself.
- State units for every dimensional quantity and every numeric value.
- Number an equation only if the text refers back to it.
- Use one term for one quantity or concept. Never use a synonym for a term that is already defined.
- Keep each sentence to 25 words or fewer, with one idea per sentence.
- Use the active voice. Make the actor or the quantity the subject.
- Keep noun clusters to three words or fewer.
- Keep each paragraph to one topic and six sentences or fewer.

## Layout

- One doc per concept with one headline result. If the summary needs two short answers, write two docs.
- Docs live in area folders, created when their first doc lands. The areas are listed in [[README]].
- File names are kebab-case concept slugs, unique across the repo, with no number prefixes.
- Every new doc gets one line in [[README]]: its link and its one-sentence takeaway.

## Doc template

```markdown
---
area: <area folder>
date: <YYYY-MM-DD>
verified-against: <MCNuX short commit>
specs: [<spec codes>]
builds-on: ["[[conventions]]"]
---
# <Concept>

> [!question]
> The question that prompted this doc, in one sentence.

> [!summary]
> Two to four sentences: what to recall in 30 seconds.

## Setup
Symbols and assumptions beyond [[conventions]].

## Derivation
Key steps to the headline result.

## Assumptions and limits
What is approximated, and where it breaks.

## Why it matters
What this enables in MCNuX, or what goes wrong without it.

## Pitfalls
Optional. Convention traps, and what was misunderstood at first.

## In MCNuX
Optional. Spec ids only, one line each.

## References
arXiv id and equation number.
```
