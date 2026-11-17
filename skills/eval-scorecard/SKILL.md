---
name: eval-scorecard
description: "Use when reporting an eval batch, a benchmark run, or a before-and-after comparison of agent builds: count passed, failed, unverified and inconclusive cases separately, give latency p50 and p95, throughput as tasks finished per hour with its window, dollars per task and per passed task, and cache-write share, each labeled measured, derived, estimate or missing."
---

# Eval scorecard

One number hides the trade-offs that decide a build. A batch report gives quality, speed and cost on the same run, and says where each number came from.

## Steps

1. **Pin the run.** Name the revision or build of every case, the model, the judge or grader and its version, the case list, and what the cost figure covers (model calls only, or search and tools too). A run that mixes builds says so.
2. **Count four verdicts apart.** Passed, failed, unverified (no evidence either way yet) and inconclusive (evidence, but it does not settle the case). Never print one pooled score or a pass rate that hides the other three. When your reading disagrees with the judge, show both counts.
3. **Separate finished from correct.** "Finished every required output" is its own row. An unfinished case is not a failure of correctness, and it is not a pass.
4. **Latency per task.** p50 and p95 per case with the nearest-rank method named, plus the slowest case. For speed-first work (a chat reply) also give time to first output. For volume-first work (a batch run) the target is usually the p90 or p95 finish time.
5. **Throughput is not latency.** Tasks finished per hour needs the real batch window: first start to last end. A sum of case durations counts overlap twice when cases run in parallel. Without the window, print the serial-equivalent rate and label it an estimate with that assumption.
6. **Cost per task.** Mean and median per case, cost per passed case (all spend divided by passed cases), spend on unfinished cases, and cache-write share of cost. Unknown cost is "missing", never zero. A cost per passed case is only computed when every case has a cost.
7. **Compare like with like.** A before-and-after claim reruns the same cases on the same judge. A speed or cost gain that changes an answer is a regression.

Run the [scorecard script](scripts/scorecard.py) on a per-case CSV (`case_id, verdict, duration_s, cost_usd, finished, cache_write_usd`):

```bash
python3 scripts/scorecard.py cases.csv --cost-scope "model only" --wall-seconds 12000
```

It exits 2 on an unknown verdict, a missing column, a duplicate case id or a non-number. It computes from the file; it does not run an eval or check that the verdicts are right.

Try it on the [synthetic CSV](examples/cases.csv): one case has no numbers, so cost per passed case prints "missing". See the [worked example](examples/worked.md).
