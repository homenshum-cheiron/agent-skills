# Worked example (synthetic)

A team compares two builds of a document-classification agent on 20 synthetic cases.

Weak report: "Build B scores 75%, up from 60%, and is faster."

Scorecard for build B (all numbers invented):

| Metric | Value | Label |
|---|---|---|
| Cases | 20, all on build B, judge v2 | measured |
| Passed / failed / unverified / inconclusive | 9 / 5 / 0 / 6 | judged |
| Finished every required output | 14 of 20 | measured |
| Latency p50 / p95 per case (nearest rank) | 6.1 / 19.4 min | measured, 20 of 20 timed |
| Tasks finished per hour | 4.2 over a 200-minute window | measured |
| Dollars per case, mean / median | $6.00 / $4.80 | derived, model calls only |
| Cost per passed case | $13.33 | derived |
| Spend on unfinished cases | $41.00 | measured |
| Cache-write share of cost | missing | not exported |

What the weak report hid: "75%" counted the 6 inconclusive cases as passes (9 plus 6, of 20), the faster claim came from a sum of durations while cases ran three at a time, and a third of the spend bought no finished case. The useful next step is to finish the 6 cases, not to tune the model.
