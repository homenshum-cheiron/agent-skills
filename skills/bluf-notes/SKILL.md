---
name: bluf-notes
description: "Use when condensing notes, takeaways, research, or status into a glanceable write-up, pull request body, or owner report: bottom line first, owner on every card, and the background a newcomer needs."
---

# BLUF notes

Goal: the first screen reads in about 30 seconds, and a reader who missed the meeting still understands what happened, why it matters, and what is theirs. Short is good. Cryptic is not. A card that only makes sense to the person who wrote it has failed.

## Page layout

1. **Context box**, 2-4 sentences: what this page is, where the notes came from (event, meeting, thread, date), and the one question the page answers. Write it for a colleague who was not there.
2. **Top takeaways**, 3-5 full sentences ranked by dollar, hour or risk impact, immediately useful first. Each starts with its owner's name, says what to do and why, and links to its card.
3. **Cards**, one per insight, in the same order. Use the [page template](references/template.md).
4. **Glossary**, only if needed: one line for each acronym, product or internal term the cards use.
5. **Appendix**: raw notes, transcripts and long tables, collapsed. Never delete raw notes; move them here.

## Card format

- **Owner** is the person most tied to the topic: who owns that code, customer, decision or relationship. Never blank; write "owner unclear, suggest X" when unsure.
- **Situation** is 1-3 sentences of background a newcomer needs. Name the thing in plain words before its short name ("the request router, the open-source library we use to talk to many model providers through one interface").
- **Scenario** is one concrete example, real when one exists. A made-up one is labeled "example".
- **Bottom line** is one sentence saying what we should do or believe.
- **Why it matters** gives dollars, hours, risk or customer impact. Write "impact unknown" rather than invent a number.
- **Evidence**: at most 3 bullets, each naming its source.
- **Next step**: who does what by when, marked "now" if it can start today.
- **Confidence**: verified, inference or unverified, and why.

## Engineering write-ups: pull request bodies, channel posts, agent reports

Use this shape for pull request descriptions, engineering posts in team chat (review asks, incident or fix posts, vendor issue lists), and any report a coding agent sends back to the person who dispatched it.

1. **One-line headline**: what this is and what you want, in one plain sentence ("Fix the date parser in the literature-search client so one research query stops retrying every five minutes; needs one review").
2. **Background**: 2-4 bullets on why things are set up this way and why this matters now (a customer or compliance constraint, the existing system, what it costs today). Write for a reader who has never seen the code.
3. **Items**: a numbered list. Each item is ONE bold line stating the problem or change, then nested bullets:
   - **Cause:** why it happens, in plain words, with a file or function name where useful.
   - **Status:** fixed, open, in progress or unverified, with links to the pull request, issue, commit or CI run.
   - **Docs:** links to the official docs for the feature or API involved, and what the upstream tool can already do. Check every link opens before using it.
   Drop a sub-bullet only when it genuinely has nothing to say; never pad.
4. **Asks or to-dos**: a checklist. Each line names who does what, and what "done" looks like. Make each ask specific enough to answer yes or no (exact behaviors, versions, endpoints), never "better support for X".
5. **Out of scope / unverified**: one line on anything deliberately left out and why.

Rules for this shape:
- Pull request bodies also include how it was tested (commands and results) and the risk if it is wrong.
- Agent reports lead with the verdict (done, blocked, partly done) before the items, and state anything not verified as unverified.
- Chat posts use the platform's markdown; long logs and diffs go in a collapsed block or a link, not inline.

## Chat replies that report on work

Start every work reply with **Needs you**, **Done?**, **How**, and **Problems**, in that order. Details and the checker: [chat replies](references/chat-replies.md).

## Plain-English rules

- Complete sentences only. No headline fragments, arrows, slash-joined lists or "label: value" shorthand inside sentences (the Cause / Status / Docs sub-bullet labels above are the one exception).
- Define every acronym, tool, pull request number and internal term the first time it appears, or put it in the glossary.
- Prefer concrete nouns and verbs: "we pay twice for the same tokens" beats "cache-accounting regression".
- Newcomer test: could someone who missed the meeting explain each card or item back? If not, add situation, not length elsewhere.
- Keep what a speaker or source said apart from your own reading, labeled "our read".
- Merge duplicates. An insight with no next step and no impact moves to the appendix.
- Invent no numbers, names or quotes. Placeholders are labeled as placeholders.
- Re-read after writing: confirm the first screen carries the bottom line and every item passes the newcomer test.

When rewriting an existing page, keep all original content in the appendix, rebuild the context box, takeaways and cards from the original plus its sources, and re-read the whole page after writing. See the [worked example](examples/worked.md).
