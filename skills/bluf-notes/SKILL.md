---
name: bluf-notes
description: "Use when condensing notes, conference takeaways, research or status into something readable at a glance, and when writing pull request bodies, team-channel posts, findings reports with gaps and fix plans, a visual artifact with system design diagrams, or a coding agent's report back to its owner: bottom line first, owner named, every sentence proof-checked with a verdict and a shareable source link."
---

# BLUF notes

Goal: the first screen reads in about 30 seconds, and a reader who missed the meeting still understands what happened, why it matters, and what is theirs. Short is good. Cryptic is not.

## Page layout

1. **Context box**, 2-4 sentences: what this page is, where the notes came from, and the one question it answers. Write it for a colleague who was not there.
2. **Top takeaways**, 3-5 sentences ranked by dollar, hour or risk impact, useful first. Each starts with the owner, says what to do and why, and links to its card.
3. **Cards**, one per insight, in the same order. Use the [page template](references/template.md).
4. **Glossary**, only if needed: one line for each acronym, product or internal term the cards use.
5. **Appendix**: raw notes, transcripts and long tables, collapsed. Never delete raw notes; move them here.

## Card format

- **Owner** is the person most tied to the topic: who owns that code, customer, decision or relationship. Never blank; write "owner unclear, suggest X" when unsure.
- **Situation** is 1-3 sentences of background a newcomer needs. Name the thing in plain words before its short name.
- **Scenario** is one concrete example, real when one exists. A made-up one is labeled "example".
- **Bottom line** is one sentence saying what we should do or believe.
- **Why it matters** gives dollars, hours, risk or customer impact. Write "impact unknown" rather than invent a number. If the data already exists, compute it instead of listing a to-do.
- **Evidence**: at most 3 bullets, each naming its source.
- **Next step**: who does what by when, marked "now" if it can start today.
- **Confidence**: verified, inference or unverified, and why.

## Findings, gaps and fix plans: Before, GAP, FIX PLAN, After

For findings that expose a problem, use one line per finding, then nest **GAP** (what is missing or broken, and the root cause if known) and **FIX PLAN** (owner, steps, proof test). Show **Before** (today's state at a named commit, with links), then GAP, then FIX PLAN, then **After** (proposed until a rerun proves it). Delegate fixes once approved. See the [reference](references/findings-artifacts-evidence.md).

## Visual artifact with system design diagrams

When findings span several owners or components, or the user asks for an artifact like the team's, build one self-contained page and link it from a short chat post. Search the team's existing artifacts as style references. Put sequential steps on separate levels, label every arrow with what is handed off, and use Mermaid or inline SVG so diagrams render offline. See the [reference](references/findings-artifacts-evidence.md).

## Engineering write-ups: pull request bodies, channel posts, agent reports

Use this shape for pull request descriptions, team-channel posts, and reports back to the person who dispatched the work. See the [worked example](examples/worked.md).

1. **One-line headline**: what this is and what you want.
2. **Background**: 2-4 bullets for a reader who has never seen the code.
3. **Items**: one bold line each, then **Cause**, **Status** (with links), and **Docs** (official docs; check every link).
4. **Asks or to-dos**: who does what, and what "done" looks like, yes or no.
5. **Out of scope / unverified**: what was left out, and why.

Pull request bodies include how it was tested and the risk if wrong. Agent reports lead with the verdict and mark unverified work. Long logs go in a collapsed block or a link.

## Evidence standard: proof-check every sentence before it ships

A note is not ready until every factual sentence has been checked against its source. Split the draft into claims, search every system the user actually works in, and give each claim a verdict: verified, wrong, unverified, or inference (label "our read"). Each verified claim carries a shareable link. Never upgrade a guess to a fact. See the [reference](references/findings-artifacts-evidence.md).

## Plain-English rules

- Complete sentences only. No fragments, arrows, or "label: value" shorthand (Cause / Status / Docs / GAP / FIX PLAN labels are the exception).
- Define every acronym, tool, pull request number and internal term the first time it appears, or put it in the glossary.
- Label every named company and person the first time they appear, e.g. "Acme Robotics (company) lunch with Jordan Lee (Staff Engineer)". Take roles from a real source, or write "(role unverified)".
- Prefer concrete nouns and verbs: "we pay twice for the same tokens" beats "cache-accounting regression".
- Newcomer test: could someone who missed the meeting explain the card back? If not, add situation.
- Keep what a source said apart from your own reading, labeled "our read".
- Merge duplicates. An insight with no next step and no impact moves to the appendix.
- Invent no numbers, names or quotes. Label placeholders.
- Re-read: the first screen must carry the bottom line, and every item must pass the newcomer test.

When rewriting a page, move original content to the appendix, rebuild from the original plus its sources, and re-read. See the [worked example](examples/worked.md).
