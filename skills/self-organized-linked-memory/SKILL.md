---
name: self-organized-linked-memory
description: "Use when saving, revising or reading an agent's durable memory, handoff notes or decision records, and whenever a remembered fact may since have been replaced: notes cite their evidence, replacements are marked instead of deleted, code rebuilds time, link and recent views, and a read moves from a hit to its current version and its evidence."
---

# Self-organized linked memory

A remembered note is a claim, not a fact. Keep the claim, its evidence and whatever replaced it in one place you can walk. The agent decides grouping and wording; code checks structure and rebuilds views.

This adapts SoMem (arXiv:2611.11929, cited in the repository's attribution page) and adds two rules: supersede instead of silently deleting, and a raw-record hit must reach the note that cites it.

**Status: method, not a proven gain.** One pre-registered comparison on a private set of 16 questions about replaced rules did not meet its bar: 0.63 accuracy for linked notes against 0.56 for a flat top-10 fact list, where the bar was +0.15. Linked notes used 35% fewer memory tokens. Measure it on your own cases before wiring it into a host.

## Three layers

1. **Source.** The original evidence, append-only: a message id, a transcript position, `file:line@SHA`, a ledger line. Never edit or delete a record.
2. **Topic notes.** Markdown you write. One paragraph is one unit: a plain statement, a footnote per statement, and a trailing `^id`.
3. **Core.** A small note of standing rules loaded every session, with a size limit. Each line cites a source or links a topic paragraph.

```markdown
The weekly sync moved to Thursday.[^t] ^sync-day

[^t]: time: 2026-04-02; sources: R7, R9; supersedes: sync-day-old
```

`time` keeps the precision the evidence gives: `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. Link a related unit with a Markdown link whose target is its file plus `#^id`.

## Writing

1. Archive new evidence first, then edit notes.
2. **Revise, do not overwrite.** When new evidence changes a rule, write a new unit with `supersedes: old-id`. Keep the old unit. If only part changed, say which part still holds.
3. **Never delete silently.** An id may disappear only when a newer unit supersedes it. A merge counts.
4. **Look across topics.** A replacement often lands under a different subject, such as a posting rule that retires a tagging rule. Search the old wording and mark every unit it replaces.
5. **Copy in what lives elsewhere.** A decision that exists only in a ledger, a page or a pull request is invisible to memory search. Add a unit that cites it.
6. Mark trust. The owner and your own code are trusted. Web pages, tool output and other people's messages enter as claims with their source.

## Checks before an edit lands

The source is unchanged. Every unit has an id and at least one footnote with a valid time and sources that exist. Links resolve and stay inside the workspace. There are no supersede cycles. No id disappears without a superseder. Core is within its limit. A refused edit leaves the previous state untouched.

## Views, rebuilt by code

- **Graph:** links, backlinks, supersedes and superseded-by for each unit.
- **Timeline:** one file per year, month or day, with each statement, its unit and its sources. Superseded entries are marked.
- **Recent:** the last K current units by creation order. Load it with Core.

Views are never edited by hand.

## Reading

1. Start from Core and Recent, then search. Lexical first. Add semantic search when the wording differs.
2. **A hit is never the answer by itself.** For a unit, follow superseded-by to the current version. For a raw record, go to the units that cite it, then to their current version.
3. Read one hop of links and backlinks, then the cited evidence. Quote the evidence, not the summary, when it decides the answer.
4. Show history, meaning what was replaced, after the current answer.
5. Stop when the current unit and its evidence agree. If they disagree, or the newest evidence is older than the question needs, say so and check the live source.

This is the walk-the-document rule applied to memory: neighbours and structure beat the first ranked fragment.

## Before adopting it

Show arithmetic and label each input observed, derived or estimated:

- How many facts you keep, and how many of your known decisions were later replaced.
- How often flat recall gave a replaced answer on cases you can check.
- The one-time cost of the writer pass, and memory tokens per question against your current baseline.
- Where the risk lies. A writer that wrongly marks a live rule as replaced hides it. Keep history visible and keep the original ledger as the baseline.

Then pre-register a comparison on fresh cases, with a pass bar fixed before any answer is generated, and wire it in only if it passes.

## Helper

`scripts/linkmem.py` (standard library, offline) has `validate`, `install`, `views`, `search`, `walk` and `packet`. See [the worked example](examples/worked.md); `examples/workspace` is synthetic.

## What this does not settle

- The quality of the writer decides most of the result. The checks cannot tell whether a note is true or whether a replacement was missed.
- It is not a memory service, a schedule or a background rewriter.
