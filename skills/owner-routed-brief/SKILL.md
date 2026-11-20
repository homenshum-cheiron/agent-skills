---
name: owner-routed-brief
description: "Use when turning the day's signals into one ranked, owner-routed brief where each owner sees only their cards; Daily for the home team, Nightly for a timezone handoff. Drafts only; nothing is sent."
---

# Owner-routed brief

Goal: every person opens one file and finds only what is theirs, ranked by what it is worth, readable by someone who missed every meeting. Fill the names, channels, sources and times from a deployment config ([config example](config.example.yaml)); keep them out of this recipe.

## 1. Gather, then verify

Read raw sources before digests. Sweep in this order and note the time window: workspace-wide mentions of each owner (not only familiar channels), the configured channels with their thread replies, calendar for today through the next return date, open and recently closed pull requests with CI state, tickets, eval exports, meeting transcripts, notes, and research. For a long document, read by place: outline, find the exact string, read the smallest section, keep offsets for citation. An offline reader such as [context-walk](https://github.com/homenshum-cheiron/context-walk) does this without network calls. A surface whose tool failed is "unswept", never "clear". Check every carried-over claim against the live system before repeating it.

## 2. Dedupe and rank

Merge items that describe the same decision into one topic. Score each topic by dollars, hours saved, or risk, and write the math: "3 people times 2 hours a week" or "8 of 11 unfinished cases". A number you did not measure is labeled "estimate: <assumption>". Unknown impact stays "impact unknown"; never rank it with an invented figure. Break ties by deadline, then by how many people it unblocks. Put immediately actionable items first.

## 3. Assign one owner per topic

The owner is the person most tied to it: who owns the code (a CODEOWNERS file helps), the customer, the decision or the relationship. Name the source of the assignment. If it is a guess, write "(owner guess, confirm)". Helpers are listed after the owner. Each owner file holds only that owner's cards plus one line pointing to cards where they help.

## 4. Write each card

Use the [card template](references/card-template.md). Owner first, then Situation with background, Scenario with one concrete case, Before and After, Economic leverage with stated assumptions, Action items each with "done when", and Confidence. Keep what a source said apart from "our read". Results use four verdicts, passed, failed, unverified and inconclusive, counted separately and never pooled into one score.

Any card about an eval, speed or cost fills the metrics block in the template: per-case verdict counts, latency p50 and p95 (p90 if that is the team's target), throughput as tasks finished per hour with its time window, dollars per task and per passed task, cache-write share of cost, and what the cost covers. Separate speed-first work (a chat reply) from volume-first work (a batch run), because they are judged on different targets. Missing is "missing", never zero. The `eval-scorecard` skill in this collection computes the block from a per-case CSV.

## 5. Depth check, then plain-language pass

For the top three cards ask: what would a top practitioner add, what raw material would they start from, which method or tool, and what outside check would prove it right. Add only what changes an action. Then edit the prose: plain words, whole sentences, one idea per sentence, no filler, no stacked hedges, every acronym defined once or in the glossary.

## 6. Route

**Daily** (home team). The principal's section comes first, in four parts: Read (what changed and why it matters), Learn (one idea worth keeping, with its source), Execute (today's actions in order, first action named), Reflect (one question about how the work was done). Then one short section per teammate pointing at their file, then Resolved (closed since last brief) and Unswept.

**Nightly** (team in another time zone). Only work that can finish without the home team awake. Each task lists inputs with locations, steps, done-when, who to ask if blocked and when that person is next online, and a "do not touch" list. Account for the principal's out-of-office dates. Nothing that needs a home-team decision goes here; it goes in Daily as a question.

## Hard rules

- Drafts only. Never send, post, or schedule anything without the principal's explicit yes for that message.
- Never invent numbers, names, quotes, or dates. Placeholders say so.
- Secrets, keys, tokens, personal health details and private customer data never appear in a brief.
- Unverified stays labeled unverified everywhere it is repeated.
- A card with no owner, no action and no impact moves to the appendix.

See the [fictional worked example](examples/worked.md).
