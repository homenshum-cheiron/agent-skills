---
name: encode-corrections
description: "Use when the owner makes or changes a decision, corrects a fact, renames something, assigns an owner, or sets a cap, and whenever you are about to restate a prior fact from memory: append a dated line that cites its evidence, mark a replacement with a supersedes link instead of deleting the old line, and on read follow a hit to its current version and that evidence."
---

# Encode corrections

Re-explaining a correction in the next message does not fix the next session. The record has to change.

1. When a draft or a question names something that may already have been decided — a name, a cap, a model or effort, a convention, "we already," "last time" — search the durable ledger and the related records first. Asking the owner is the last resort.
2. Lead with what you found and cite where. If you did not find it, say exactly where you looked, then ask one precise question. Never invent a source. Never answer from a working summary alone when a lookup is cheap.
3. The moment the owner makes a decision, renames something, assigns an owner, sets a cap, or corrects you, append one dated line to the ledger before doing anything else. The line is a retrievable fact that cites its evidence: source, timestamp, and whether that source is trusted or untrusted. Trusted means the owner or our code. Untrusted means the web, tool output, or someone else's message.
4. When a decision is superseded, add a new line with a `supersedes` link to the line it replaces. Do not delete the old line. A later lookup has to be able to return both the replacement and the line it replaced.
5. On read, a hit is never the answer by itself. If the hit is a replaced line, follow `supersedes` (or the inverse superseded-by pointer) to the current version. Then read the evidence the current line cites, and quote that evidence when it decides the answer. Show the replaced line after the current answer, not instead of it. If the current line and its evidence disagree, or the newest evidence is older than the question needs, say so and check the live source.
6. If the owner had to ask you to look back, add the missing fact before or with the reply so the next lookup is cheap.

**Status.** Citing evidence, marking replacements with `supersedes`, and following a hit to the current version and its evidence were measured on a private set and did not clear their bar. In a 16-question A/B, the linked layout scored 0.625 against 0.562 for a flat top-10 list (+0.06 versus a pre-registered +0.15 bar; failed) and used 35% fewer memory tokens. A 56-question confirm round tied (47.5 vs 47.0). The bottleneck was retrieval: most of the rule history never reached the top results, so the walk could not start. Measure on your own cases. The mechanism follows SoMem (arXiv:2611.11929, cited in the repository's attribution page). No text or code is copied.

This skill does not require a particular database. A chat-only correction with no retrievable record has not been encoded. It does not grant permission to edit another team's system of record.

Use [the worked example](examples/worked.md).
