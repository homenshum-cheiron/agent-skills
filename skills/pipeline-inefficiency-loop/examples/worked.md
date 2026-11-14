# Worked example (synthetic): three laps on a ticket-routing pipeline

Everything here is invented for illustration: the pipeline, the hosts, the counts, the costs, and the owners. No number below is a measurement. Labels such as OBS (observed), DER (derived), and EST (estimated) show how each input would be treated in a real run.

## Setting

A pipeline, `triage`, reads a support ticket, fetches the relevant policy page, and routes the ticket to a team. A shared fetch tool, `shared.tool.web_fetch`, is also used by a second pipeline, `faq`.

## Step 0: bounds

- Budget: $20 for the whole loop, $8 per lap. Four hours of agent time per lap.
- Human gates: the platform owner approves each paid run and each merge.
- Premise threshold: 100 harmful outcomes avoided a year, or $500 a year saved.
- Stop rules: budget spent; two laps in a row with nothing above the threshold; a fix that cannot be shown on a same-version baseline; the owner says stop.
- Frozen: grader v3, the 40-case eval, these bounds.

## Lap 1

**Scan.** Stamp: commit `aaaa111`, prompt v5, skills v2, tool set v4, model `model-a`, grader v3. The latest eval has 9 failed rows of 40. Walking each row upstream to the first broken contract:

| FM ID | Rows | Status before this lap |
|---|---|---|
| `FM-shared.tool.web_fetch-01`: status 200 with an empty body, treated as "no policy" | 5 | untracked (new ID added this lap) |
| `FM-triage.prompt.route-01`: right policy, wrong team chosen | 3 | tracked and posted |
| unattributed (trace missing) | 1 | n/a |

A scoring rule ("failed only because the source is unreachable") had removed 4 of the 5 fetch rows from the accuracy score. They still count under the FM ID.

**Premise.** 50,000 tickets a year (OBS, ticket system count). 1.2% of fetch spans over 7 days are status 200 with an empty body (OBS, trace query). That is about 600 tickets a year routed without the policy (DER). About half of those are misrouted (EST, from the 5 eval rows and a 20-row trace sample). So about 300 misroutes a year (DER from EST). The fix adds a check and costs about $0 a year, so the risk direction is safe. 300 is above the threshold of 100. `FM-triage.prompt.route-01` comes to about 90 a year (EST) and ranks second.

**Validate.** Options: (a) treat an empty 200 as a typed `empty` error, retry once, then state the gap in the answer; (b) switch the fetch library; (c) do nothing. The fetch library's docs say some sites return an empty shell that a script fills in later. Option (b) would not change that. Verdict: build (a).

**Lean test.** Rung 3 replays the 5 stored rows with the typed-error check, at $0: 4 of 5 now route correctly. Rung 4 to 6: those 5 cases plus 2 controls from `faq`, which shares the tool, at 3 runs each, with the reference on the same cases. That is 7 cases × 3 runs × 2 arms = 42 runs. At an illustrative $0.10 a run, that is about $4.20 of the $8 lap cap. The owner read the plan first and approved the paid rungs.

**Fix.** On the same stamp apart from the change, `FM-shared.tool.web_fetch-01` goes from 5 rows to 1. No measure gets worse on `triage` or `faq`, and confident-wrong answers stay at 0. The owner approves the merge. Older results are marked stale.

**Lesson.**

- Why not sooner: the signal existed (`status=200 len=0` in fetch logs), but no scan read it. A scoring rule hid 4 of 5 rows.
- Detector: a daily count of empty-200 fetches per host, added to the scan.
- Register: the FM status becomes "tracked and posted".
- Scan checklist: "count rows that scoring rules drop, per FM ID".
- Replay on stored traces from the two earlier evals: it flags all 5 rows from this lap and 0 of 310 earlier rows that passed.

## Lap 2

**Scan.** The new detector flags a second host with empty-200 fetches. The lap-1 fix already covers it: 0 failed rows. That confirms the change generalizes, but it is not a new finding. The top new finding is cost: `triage.tool.policy_lookup` fetches the same page about 3 times per run. At $0.003 a run (OBS) × 50,000 runs (OBS), that is $150 a year (DER). It is below the $500 threshold, so it is downgraded and logged, not built.

**Lesson.** Why not sooner: there was no per-run duplicate-fetch metric. Detector: duplicate fetches per run, added to the scan. Verdict: parked. Revisit if volume grows by about 4 times.

## Lap 3 and stop

`FM-triage.prompt.route-01` was re-estimated with the new counts at about 90 a year (EST), still below the threshold. Nothing is above the threshold for the second lap in a row, so the stop rule fires. Spend: about $4.20 of $20.

## Lap summaries the owner sees

```
Lap 1: empty-200 fetch read as "no policy" (shared.tool.web_fetch, FM-shared.tool.web_fetch-01)
  Premise: 50,000/yr · ~$0 · risk safe · ~300 misroutes/yr avoided (EST)
  Test: replay, then 42 runs, $4.20 of $8
  Verdict: adopted; FM count 5 -> 1 on aaaa111+fix
  Lesson: signal unread, rows hidden by a scoring rule -> daily empty-200 count per host
Lap 2: duplicate policy fetches (triage.tool.policy_lookup), $150/yr, below threshold, parked
  Lesson: no duplicate-fetch metric -> per-run duplicate count added
Lap 3: nothing above threshold. Stop (two laps in a row).
```

What this example does not show: that the loop works on a real pipeline. That needs real laps, recorded with their failures, and a held-out check.
