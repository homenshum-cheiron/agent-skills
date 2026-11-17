# Card template

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
