---
name: bluf-notes
description: "Use when condensing meeting notes, conference takeaways, research or status into a page someone can read in 30 seconds: bottom line first, an owner on every card, plain English with the situation and background a newcomer needs, raw notes kept in an appendix."
---

# BLUF notes

Goal: the first screen reads in about 30 seconds, and a reader who missed the meeting still understands what happened, why it matters, and what is theirs. Short is good. Cryptic is not.

## Page layout

1. **Context box**, 2-4 sentences: what this page is, where the notes came from (event, meeting, thread, date), and the one question the page answers.
2. **Top takeaways**, 3-5 full sentences ranked by dollar, hour or risk impact, immediately useful first. Each starts with its owner's name, says what to do and why, and links to its card.
3. **Cards**, one per insight, in the same order. Use the [page template](references/template.md).
4. **Glossary**, one line for each acronym, product or internal term the cards use.
5. **Appendix**: raw notes, transcripts and long tables, collapsed. Never delete raw notes; move them here.

## Card rules

- **Owner** is the person most tied to the topic: who owns that code, customer, decision or relationship. Never blank; write "owner unclear, suggest X" when unsure.
- **Situation** gives the background a newcomer needs. Name a thing in plain words before its short name.
- **Scenario** is one concrete example, real when one exists. A made-up one is labeled "example".
- **Why it matters** gives dollars, hours or risk, with the math. Write "impact unknown" rather than invent a number.
- **Evidence**: at most 3 bullets, each naming its source.
- **Next step**: who does what by when, marked "now" if it can start today.
- **Confidence**: verified, inference or unverified, and why.

## Plain-English rules

- Complete sentences. No arrows, slash-joined lists or "label: value" shorthand inside sentences.
- Concrete nouns and verbs: "we pay twice for the same tokens" beats "cache-accounting regression".
- Keep what a speaker or source said apart from your own reading, labeled "our read".
- Merge duplicate insights. An insight with no next step and no impact moves to the appendix.
- Invent no numbers, names or quotes.
- Newcomer test: could someone who missed the meeting explain each card back? If not, add situation, not length elsewhere.

When rewriting an existing page, keep all original content in the appendix and re-read the whole page after writing. See the [worked example](examples/worked.md).
