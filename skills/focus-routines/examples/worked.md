# Example: one day with two tempting side jobs (synthetic)

Everything here is made up: the person, the phases, the times and the outputs shown. No routine was run on a real desk for this page.

Setup: a developer directs three coding agents. Deep blocks are 09:30 to 11:30 and 14:00 to 16:00. Yesterday ended with five open threads and nothing merged.

## Morning

The critic ranks from messages, open reviews, the calendar and recent state, without reading any plan. Its top item is "finish the import parser: two teams wait on it". The planner had proposed "start the new export format". The phase pick shows both lines. The developer picks the parser.

`today.json` after the pick:

```json
{"date": "2031-03-04", "phase_id": "P1", "done_picture": "parser passes the 40 fixture files and the review is requested",
 "first_step": {"when": "09:30", "where": "desk", "action": "open the failing fixture test"}}
```

The estimate comes from the last three parser jobs, which took 5, 7 and 9 hours from start to merge. The plan says 7 hours plus 2 for rework, not the 3 hours it feels like.

## 10:05, in the first deep block

A colleague asks for a review of an unrelated change. The say-no gate logs it as `batch` and drafts: "I am on the parser until 11:30; I can review after 3 PM." The developer sends it.

An agent on a side job (renaming a config key, phase P3) asks for the top model tier:

```text
$ python3 scripts/tier_route.py --want top --phase P3
{"ts": "2031-03-04T10:06:00+00:00", "phase_id": "P3", "tier": "mid", "in_block": true, "wanted": "top", "capped": true,
 "reason": "deep block: top is only for the active phase (P1); this run is tagged P3"}
```

The parser agent, tagged P1, gets the top tier.

## 10:40, the tempting shortcut

The developer wants to open a branch for the export format "just to sketch it".

```text
$ python3 scripts/focus_check.py gate-open P2
{"check": "phase_gate", "verdict": "failed", "pass": false, "detail": "phase P1 is still open: finish it or park it first"}
```

The export idea goes into `phases.json` as queued, with a next step for tomorrow.

## 13:50, a push without a design

An agent worktree pushes a 200-line retry helper with no design file. The example hook answers:

```text
design-gate: BLOCKED refs/heads/agent/retry-helper: no design file in the branch or the ledger. write docs/design/<name>.md (or DESIGN*.md / PLAN*.md / *.mmd) in a commit before the first code commit
```

The agent writes a 15-line design, puts that commit before the code commit, and pushes again. A one-line typo fix from another worktree passes with `design-exempt: typo in a log message` in its commit message.

## 17:30, before stopping

The residual snapshot writes three lines for P1: done (38 of 40 fixtures pass), stuck on (two files with mixed line endings), next step (09:30 tomorrow, open the line-ending fixture first).

```text
$ python3 scripts/focus_check.py all
```

Expected for this made-up day: `one_active`, `done_picture`, `no_interrupt`, `switch_cap`, `snapshot_fresh`, `model_tier` and `critic_blind` all report `passed`. If the snapshot had been skipped, `snapshot_fresh` would report `failed` the next evening, and with no ask log at all `no_interrupt` would report `unverified`, not `passed`.

## What this example does not show

It does not show that the day went faster. The weekly review compares the 9-hour plan with the real hours. A passing check means the state files have the right shape at the right time. It does not mean the done-picture was a good one.
