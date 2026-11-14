# Worked example (synthetic): three laps on a ticket-routing pipeline

Everything here is invented for illustration: the pipeline, the hosts, the counts, the costs, and the owners. No number below is a measurement. Labels such as OBS (observed), DER (derived), and EST (estimated) show how each input would be treated in a real run.

## Setting

A pipeline, `triage`, reads a support ticket, fetches the relevant policy page, and routes the ticket to a team. A shared fetch tool, `shared.tool.web_fetch`, is also used by a second pipeline, `faq`.

## Step 0: bounds (the owner read them)

- Budget: $20 for the whole loop, $8 per lap. Lap cap: 5.
- Premise threshold: 100 harmful outcomes avoided a year, or $500 a year saved.
- False-flag ceiling: a new detector may flag at most 2 earlier clean rows.
- Human gates: the platform owner approves each paid run and each merge.
- Stop rules: budget or lap cap reached; two laps in a row with nothing above the threshold; no same-version baseline for the top finding; the owner says stop.
- Frozen: grader v3, the 40-case eval used for adopt decisions, these bounds.

"Confident-wrong" here means a ticket routed to the wrong team with no "needs review" flag.

## Lap 1

**Scan.** Stamp: commit `aaaa111`, prompt v5, skills v2, tool set v4, model `model-a`, grader v3. The latest eval has 9 failed rows of 40. Walking each row upstream to the first broken contract:

| FM ID | Rows | Status before this lap |
|---|---|---|
| `FM-shared.tool.web_fetch-01`: status 200 with an empty body, treated as "no policy" | 5 (all 5 confident-wrong) | untracked (ID added to the register while pinning, before the finding was written) |
| `FM-triage.prompt.route-01`: right policy, wrong team chosen | 3 (2 of them confident-wrong) | tracked and posted |
| unattributed (trace missing) | 1 | n/a |

A scoring rule ("failed only because the source is unreachable") had removed 4 of the 5 fetch rows from the accuracy score. They still count under the FM ID.

**Premise.**

- `FM-shared.tool.web_fetch-01`: 50,000 tickets a year (OBS, ticket system count). 1.2% of tickets had at least one fetch with status 200 and an empty body (OBS, 7-day trace query grouped by ticket). That is about 600 tickets a year routed without the policy (DER). About half of those are misrouted (EST, from a 20-ticket sample), so about 300 misroutes a year (DER from EST). The estimate decides the threshold: the finding crosses 100 if more than 1 in 6 are misrouted. The owner checked the sample and agreed. The fix adds a check and costs about $0 a year, so the risk direction is safe.
- `FM-triage.prompt.route-01`: the eval cases are chosen to be hard, so 3 of 40 does not scale to production. Instead: 0.18% of tickets were reassigned by a person when the policy had been present (OBS, 90-day reassignment log). 50,000 × 0.0018 = 90 a year (DER). Below the threshold.

Rank: the fetch finding first.

**Validate (desk steps).** Options: (a) treat an empty 200 as a typed `empty` error, retry once, then state the gap in the answer; (b) switch the fetch library; (c) do nothing. The fetch library's docs say some sites return an empty shell that a script fills in later. Option (b) would not change that. Option (a) is worth testing.

**Lean test.** Rung 3 replays the 5 stored rows with the typed-error check, at $0: 4 of 5 now route correctly. Rungs 4 to 6: those 5 cases plus 2 controls from `faq`, which shares the tool, at 3 runs each, with the reference on the same cases. That is 7 cases × 3 runs × 2 arms = 42 runs. To check for regressions, the candidate also runs the other 35 adopt cases once, against the baseline eval on the same stamp: 35 runs. Total 77 runs. At an illustrative $0.10 a run, that is about $7.70 of the $8 lap cap. The owner read the plan first and approved the paid rungs.

**Fix.** On the same stamp apart from the change, and under the register definitions the lap started with, `FM-shared.tool.web_fetch-01` goes from 5 rows to 1. No measure gets worse on `triage` (all 40 adopt cases) or on the `faq` controls. Confident-wrong rows fall from 7 to 3: 1 remaining fetch row and the 2 route rows. The owner approves the merge. Older results are marked stale.

**Lesson.**

- Why not sooner: the signal existed (`status=200 len=0` in fetch logs), but no scan read it. A scoring rule hid 4 of 5 rows.
- Detector: a daily count of empty-200 fetches per host, added to the scan.
- Register: the FM status becomes "tracked and posted".
- Scan checklist: "count rows that scoring rules drop, per FM ID".
- Replay on the two earlier 40-case evals (80 rows, 69 passed): it flags 0 of the 69, under the ceiling of 2. It flags all 5 of this lap's rows, which is a sanity check only.
- Applies from lap 2.

## Lap 2

**Scan.** The new detector flags 3 fresh empty-200 fetches from a second host since the merge. All 3 were real empties, and the lap-1 check handled all 3 (typed error, retry, gap stated). That is consistent with the change working beyond the first host. It is not proof. It is not a new finding either.

The top new finding is cost. `triage.tool.policy_lookup` fetches the same page about 3 times per run. The two duplicate fetches cost $0.003 per run (OBS, span cost × 2). $0.003 × 50,000 runs = $150 a year (DER). That is below the $500 threshold, so the finding is parked, not built.

**Lesson.** Why not sooner: there was no per-run duplicate-fetch metric. Detector: duplicate fetches per run, added to the scan from lap 3. Replay: false-flag ceiling not applicable, because this is a per-run cost metric, not a row flag. The replay only checks that the metric reads about 3 fetches per run on earlier traces. Revisit if volume grows about 4 times.

## Lap 3 and stop

**Scan.** Under the lap-2 detectors, no new FM appears. The top finding is still `FM-triage.prompt.route-01` at about 90 a year (DER), below the threshold.

**Lesson.** No new gap, so nothing is encoded. The entry says "not encoded: nothing new found" instead of claiming a lesson.

Laps 2 and 3 both found nothing above the threshold, so the stop rule fires. Spend: about $7.70 of $20. Laps used: 3 of 5.

## Lap summaries the owner sees

```
Lap 1: empty-200 fetch read as "no policy" (shared.tool.web_fetch, FM-shared.tool.web_fetch-01)
  Premise: 50,000/yr · ~$0 · risk safe · ~300 misroutes/yr avoided (DER from EST, owner checked)
  Test: replay, then 42 runs plus 35 regression runs, $7.70 of $8
  Verdict: adopted; FM count 5 -> 1 on aaaa111 + fix
  Lesson: signal unread, rows hidden by a scoring rule -> daily empty-200 count per host (from lap 2)
  Next: duplicate policy fetches
Lap 2: duplicate policy fetches (triage.tool.policy_lookup), $150/yr, below threshold, parked
  Confirmation: lap-1 detector flagged 3 fresh rows, 3 real, all handled
  Lesson: no duplicate-fetch metric -> per-run duplicate count (from lap 3)
  Next: re-scan; no candidate above threshold yet
Lap 3: nothing above threshold; not encoded. Stop (two laps in a row).
```

What this example does not show: that the loop works on a real pipeline. That needs real laps, recorded with their failures, and a held-out check.
