<!-- Portable, single-file version of the owner-routed-brief skill. Paste into AGENTS.md, a rules file or a system prompt on hosts without skill folders. -->

# Owner-routed brief

Goal: every person opens one file and finds only what is theirs, ranked by what it is worth, readable by someone who missed every meeting. Fill the names, channels, sources and times from a deployment config (see config.example.yaml); keep them out of this recipe.

## 1. Gather, then verify

Read raw sources before digests. Sweep in this order and note the time window: workspace-wide mentions of each owner (not only familiar channels), the configured channels with their thread replies, calendar for today through the next return date, open and recently closed pull requests with CI state, tickets, eval exports, meeting transcripts, notes, and research. For a long document, read by place: outline, find the exact string, read the smallest section, keep offsets for citation. An offline reader such as [context-walk](https://github.com/homenshum-cheiron/context-walk) does this without network calls. A surface whose tool failed is "unswept", never "clear". Check every carried-over claim against the live system before repeating it.

## 2. Dedupe and rank

Merge items that describe the same decision into one topic. Score each topic by dollars, hours saved, or risk, and write the math: "3 people times 2 hours a week" or "8 of 11 unfinished cases". A number you did not measure is labeled "estimate: <assumption>". Unknown impact stays "impact unknown"; never rank it with an invented figure. Break ties by deadline, then by how many people it unblocks. Put immediately actionable items first.

## 3. Assign one owner per topic

The owner is the person most tied to it: who owns the code (a CODEOWNERS file helps), the customer, the decision or the relationship. Name the source of the assignment. If it is a guess, write "(owner guess, confirm)". Helpers are listed after the owner. Each owner file holds only that owner's cards plus one line pointing to cards where they help.

## 4. Write each card

Use the card template below. Owner first, then Situation with background, Scenario with one concrete case, Before and After, Economic leverage with stated assumptions, Action items each with "done when", and Confidence. Keep what a source said apart from "our read". Results use four verdicts, passed, failed, unverified and inconclusive, counted separately and never pooled into one score.

Any card about an eval, speed or cost fills the metrics block in the template: per-case verdict counts, latency p50 and p95 (p90 if that is the team's target), throughput as tasks finished per hour with its time window, dollars per task and per passed task, cache-write share of cost, and what the cost covers. Separate speed-first work (a chat reply) from volume-first work (a batch run), because they are judged on different targets. Missing is "missing", never zero. The `eval-scorecard` skill computes the block from a per-case CSV.

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

## Card template

Copy one block per topic. Delete a line only if it truly does not apply, and say why in Confidence.

```markdown
### <Rank>. <Topic in plain words>

- **Owner:** <name> (<why this person: owns the code, customer, decision or relationship>). Helpers: <names>. Write "(owner guess, confirm)" when it is a guess.
- **Situation:** 1-3 sentences a newcomer needs: what exists today, who is involved, what happened or was said that raised this. Name each thing in plain words before its short name.
- **Scenario:** one concrete case, real when one exists ("Case X saved 11 of 18 markets and stopped"). A made-up illustration is labeled "example".
- **Before:** what happens today, observably.
- **After:** what will be observably different once the action is done.
- **Economic leverage:** dollars, hours or risk, with the math and its assumptions ("estimate: 3 reruns a week at $6 each"). Say "impact unknown" rather than invent.
- **Action items:**
  - [ ] <who> does <what> by <when>. Done when: <check anyone can run>.
- **Said vs our read:** "<source> said ..." kept apart from "Our read: ...".
- **Confidence:** verified, inference or unverified, and why.
```

## Metrics block (required on any eval, speed or cost card)

| Metric | Value | Label |
|---|---|---|
| Cases, and the build or revision they ran on | | measured |
| Passed / failed / unverified / inconclusive (separate counts) | | judged, name the judge |
| Finished every required output | | measured |
| Latency p50, p95 per task (and p90 if that is the target) | | measured, n timed |
| Time to first output (speed-first work only) | | measured or missing |
| Tasks finished per hour, and the window it was measured over | | measured, or estimate with assumption |
| Dollars per task, per passed task | | derived; say what cost covers |
| Cache-write share of cost | | measured or missing |
| Spend on unfinished tasks | | measured |

Rules: a blank is "missing", not zero. A sum of task durations is not wall-clock time when tasks ran in parallel. A cost that covers only model calls says so. A speed or cost gain that changes an answer is a regression, so record accuracy on the same run.

## Glossary line format

- **Term:** one plain sentence saying what it is and why it shows up here.
