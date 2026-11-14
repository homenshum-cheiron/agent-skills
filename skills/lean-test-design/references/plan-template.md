# Lean test plan (template)

Copy this file. Fill it before any paid run. The owner reads it before the first paid rung.

## Header

- Question, in one sentence: arms, measure, decision that the result changes.
- Decision value: the smallest gap that changes the decision, and what that is worth per year.
- Pipeline version stamp: commit, prompts, skills, tool set, model ID per arm, grader version.
- Baseline: run ID on the same version. If none exists, say so; earlier results are references only.
- Owner who reads the plan, and the date they read it.

## Research result

One line per arm: settled by research (yes or no), with the card link. Arms settled by research leave the plan here.

## Coverage matrix

| Case | Behavior A | Behavior B | Behavior C | Behavior D | Cost per run (measured, per arm) | Minutes per run |
|---|---|---|---|---|---|---|
| c01 | ✓ | | ✓ | | | |
| c02 | | ✓ | | | | |

Fill cells from case metadata and past runs. Never from the answer key. Write "unknown" when a cell cannot be filled; do not guess.

## Minimal set

- Chosen cases, in greedy order, with the behaviors each one added.
- Named gaps: behaviors with no case.
- Tier 2 and tier 3 cases, for expansion only.

## Cases per arm

| Arm | Cases | Why these | Anchor case |
|---|---|---|---|
| reference | full minimal set | | |
| arm 1 | only cases whose behaviors it can change | | |

## Ladder and caps

| Rung | What runs | Expected cost | Cap | Status |
|---|---|---|---|---|
| 1 Static audit | | $0 | | |
| 2 Dry run | | $0 | | |
| 3 Replay or stub | | $0 | | |
| 4 One paid case | | | | |
| 5 Minimal set, one run | | | | |
| 6 Repeats and next tier | | | | |

- Total cap:
- Naive cost (all arms × all cases × all repeats):
- Plan cost:

## Stop rule

Stop and report when a cap is hit, tracing or grading looks wrong, the feature did not fire, the one-case rung shows no arm differs, or the budget cannot reach the needed repeats.

## Results log

| Rung | Arm | Version stamp | Result | Compared with (same-version baseline) | Stale? |
|---|---|---|---|---|---|
