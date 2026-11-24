# Routine designs

Seven routines. Each one names a suggested trigger, what it reads, what it writes, and the check that can fail it. The times are examples. Your host owns the schedule; nothing in this folder creates one. Each routine reports to its owner only and sends nothing to anyone else.

Give every routine a review-by date about two weeks out. On that date keep, change or drop it from its pass and fail log.

## 1. Priority critic (the judge)

- **Why:** the planner should not grade its own plan.
- **Trigger:** each workday morning, before the phase pick.
- **Reads:** messages and threads that involve the owner, open reviews, the calendar for the rest of the week, recently changed state. **It must not read** `today.json`, `phases.json` or any plan file. It ranks from scratch.
- **Writes:** `critic.json`: a ranked list. Each item has the bigger goal it serves, the best time block, and evidence links. It also lists every source it read.
- **Check:** `critic_blind` fails when a required source kind is missing, when a plan file is in the source list, or when an item has no bigger picture, block or evidence.
- **Limit:** the source list is self-reported. A stronger setup runs the critic where the plan files cannot be opened.

## 2. Phase pick (the planner)

- **Why:** one phase a day, chosen before the day starts.
- **Trigger:** each workday morning, after the critic.
- **Reads:** `phases.json`, the critic's ranking, the calendar, and how long similar past jobs really took.
- **Writes:** `today.json`: the one phase, the done-picture, the if-then first step (when, where, first action), and an estimate taken from past actuals plus a buffer.
- **When planner and critic disagree:** show both, one line each, and let the owner choose. Neither overwrites the other.
- **Checks:** `one_active` (exactly one active phase) and `done_picture` (dated today, a done-picture, a first step with a time and an action, and the phase is the active one).

## 3. Say-no gate and switch counter

- **Why:** an ask that arrives in a deep block is the usual way a phase dies.
- **Trigger:** inside an existing hourly desk run. No new routine.
- **Reads:** new asks aimed at the owner, the active phase, and which threads had activity in the last hour.
- **Writes:** one row per ask in `parking.jsonl` with a verdict: `in_phase`, `batch` (the fixed message time), `park` or `no`. During a deep block only `in_phase` or urgent asks reach the owner. Decide ahead of time what urgent means, for example an outage or a deadline under four hours. For a deferred ask, draft a reply such as "I am on X; I can look after 3 PM". The owner sends it or not.
- **Also writes:** one row per run in `switches.jsonl` with the active threads.
- **Checks:** `no_interrupt` (nothing off-phase and non-urgent surfaced in a block) and `switch_cap` (at most 3 active threads, 1 in a block).

## 4. Residual snapshot

- **Why:** an open job with no written next step stays in your head.
- **Trigger:** at the end of each deep block and at the end of the day.
- **Reads:** `phases.json`, the day's commits and reviews.
- **Writes:** for each open phase, three lines: done, stuck on, next concrete step (a time plus a first action). It updates `next_step` and `updated` in `phases.json`.
- **Check:** `snapshot_fresh` fails when an open phase has no next step with a time and an action, or was not updated in 26 hours.

## 5. Tier routing at peak

- **Why:** the best-energy hours and the strongest model both belong to the hardest part.
- **Trigger:** every time a model run is started. This is a rule inside your own router or launcher, not a scheduled routine.
- **Rule:** in a deep block, only the active phase may use the top tier; other work is capped at mid. Outside a block, the top tier needs a phase tag.
- **Writes:** one row per run in `models.jsonl`.
- **Check:** `model_tier` fails on a top run off the active phase in a block, a cheap run on the active phase in a block, or a top run with no phase tag outside one.
- **Example:** `tier_route.py` in this folder decides the allowed tier and writes the row. Map your own models to top, mid and cheap. How to choose a model and effort for a job is a separate question.

## 6. Design-first gate

- **Why:** the long jobs are often the ones whose plan changed after the code started.
- **Trigger:** when a branch is pushed or a pull request is opened or updated.
- **Reads:** the branch's commits and the pull request text or commit messages.
- **Check:** `design_gate.py` fails when no design file was added before the first code commit. The only exemption is 30 changed lines or fewer with a `design-exempt: <reason>` line.
- **Phase gate:** `focus_check.py gate-open <phase>` fails when another active phase has not met its exit criteria. A new branch waits until the current phase closes or is parked.
- **Output:** one line to the owner. It does not comment on the pull request and changes no review state.
- **Local form:** the example `pre-push` hook. Scope it to the folders where agent worktrees live, and grandfather branches older than the day you turn it on.

## 7. Weekly reality review

- **Why:** estimates only improve when they meet actuals.
- **Trigger:** once a week, at a fixed time.
- **Reads:** the week's finished work with real timestamps (opened, first review, approved, merged), the ask log, estimate against actual per phase, and the pass and fail log of every check above.
- **Writes:** an updated duration table by job type, then a short note: the biggest bottleneck and its fix, estimate against actual by type, any rule that failed more than half its runs, and any rule that reached its review-by date.
- **Check:** the run fails when the table did not gain the week's finished jobs (compare the row count with the source), or when the segments of a job do not add up to its total.
- **What to measure:** split each job into waiting-to-start, working, waiting for review, rework, and waiting to merge. The largest segment is often not the coding.

## Slim before you add

Routines cost attention and usage. Fund a new one by cutting first.

1. **List what runs.** For each routine: the trigger, runs per week, and its share of usage. Read the share from your host's own usage report. If you cannot, say it is unknown.
2. **Stop runs that should never start.** Move a filter into the trigger (for example, only the owner's own pull requests) so other events do not wake the routine at all.
3. **Cut hours nobody reads.** An hourly run around the clock is 168 runs a week. Working hours on workdays is about 55.
4. **Merge duplicates.** Two routines that produce a status list become one snapshot. A cron that polls for a failure becomes a trigger on the failure.
5. **Delete one-offs.** A paused routine made for one day goes.
6. **Then add.** Estimate each new routine as runs per week times cost per run, taken from a similar existing routine. Label the figure an estimate. Add only what the freed room covers.

Count the saving and the new cost in the same unit, and keep estimates apart from measured figures.
