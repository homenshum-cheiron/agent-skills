# Worked example (fictional)

All names, numbers and systems below are invented to show the shape.

**Inputs swept 07:30-08:15 PT:** chat mentions for 3 owners, 2 channels with threads, calendar through next Tuesday, 4 open pull requests, one eval export of 20 cases. Ticket tool timed out: tickets are **unswept**.

**Ranked topics**

| Rank | Topic | Owner | Basis |
|---|---|---|---|
| 1 | Batch runs stop before saving every region | Sam Okafor | 6 of 20 cases unfinished; $41 of $120 model spend went to them (measured) |
| 2 | Provider server errors are not retried | Sam Okafor (owner guess, confirm) | Risk: each error fails a whole run; frequency unknown |
| 3 | Write a speed target for chat replies | Alex Rivera | Impact unknown until first-output time is recorded |

**One card**

### 1. Batch runs stop before saving every region

- **Owner:** Sam Okafor (wrote the worker pool, per CODEOWNERS). Helpers: Min Park.
- **Situation:** The batch agent answers one question per region. A run passes only if every region is saved.
- **Scenario:** Case C-07 saved 9 of 12 regions, then hit the 3-worker cap and timed out.
- **Before:** 6 of 20 cases end unfinished and are never scored.
- **After:** every case saves every region or marks it "review required".
- **Economic leverage:** $41 of model spend bought no scored answer (measured). Estimate: if half the unfinished cases become scorable, about 3 more verdicts per run at no extra spend.
- **Action items:**
  - [ ] Sam raises the worker cap behind a flag by Thursday. Done when: C-07 replays with 12 of 12 saved.
- **Said vs our read:** Min said the cap was set during a load test. Our read: the cap, not the model, ends these runs.
- **Confidence:** verified for the counts; inference for the cause.

**Metrics block (computed with the eval-scorecard skill)**

| Metric | Value | Label |
|---|---|---|
| Cases | 20 | measured |
| Passed / failed / unverified / inconclusive | 9 / 5 / 0 / 6 | judged by grader v2 |
| Finished every required output | 14 of 20 | measured |
| Latency p50 / p95 | 6.1 min / 19.4 min | measured, 20 timed |
| Tasks finished per hour | 4.2 over a 200-minute window | measured |
| Dollars per task / per passed task | $6.00 / $13.33 | derived, model only |
| Cache-write share | missing | not exported |

**Daily, principal section:** Read: topic 1 decides whether this week's eval can be scored. Learn: a sum of case durations is not wall-clock time when cases overlap. Execute: first, confirm the owner on topic 2. Reflect: which number on this page did we measure, and which did we assume?

**Nightly handoff task for Min:** Replay case C-07 on the flagged build. Inputs: `evals/latest/cases.csv`, branch `worker-cap-flag`. Done when: 12 of 12 regions saved, log attached. Ask: Sam, online 08:00 PT. Do not touch: the scorer, the answer keys, production deploys.
