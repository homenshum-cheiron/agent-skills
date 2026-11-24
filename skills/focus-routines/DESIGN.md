# Design: focus-routines

Written before the skill, so the order of this branch matches the rule the skill teaches: design first, then code.

## Problem

A person who directs several coding agents can open ten threads in a morning and close none. The usual answers are advice ("focus more") or a bigger dashboard. Neither one can fail, so neither one changes a day.

## Outcome

One portable folder that gives a person or an agent:

1. Ten short principles, each tied to a named, published idea.
2. Seven routine designs. Each one has a trigger, what it reads, what it writes, and one check that can fail.
3. Local scripts for those checks. They read small state files and git history. They call no provider and start nothing.

## What goes in

| File | Purpose |
|---|---|
| `SKILL.md` | The principles and when to use each routine. |
| `references/routines.md` | The seven routine designs and the "slim before you add" rule. |
| `references/state-files.md` | State file shapes and settings. |
| `scripts/focus_check.py` | Seven checks over the state files. Three verdicts: passed, failed, unverified. |
| `scripts/design_gate.py` | Fails a branch when no design file landed before the first code commit. |
| `scripts/tier_route.py` | Decides the highest model tier a run may use now, and logs the decision. |
| `examples/pre-push` | A pre-push hook example: chains an older hook, limits scope to chosen folders, grandfathers old branches. |
| `examples/design-gate.conf.example` | Settings for that hook. |
| `examples/worked.md` | One synthetic day. |
| `tests/test_focus_routines.py` (repository level) | Negative, unverified and passing cases for every script, and real pushes to a throwaway repository for the hook. |

## Decisions

- **State is plain files in one folder.** Default `~/.focus`, changed with `FOCUS_DIR`. No service, no database. A routine on any host can write them.
- **Missing data is never a pass.** A check with no data returns `unverified` and a nonzero exit code. An unreadable file returns `inconclusive`.
- **The clock decides whether a log row is in a deep block.** A logged flag is used only when the row has no time. A flag is easy to write wrong.
- **Deep blocks are settings.** `FOCUS_BLOCKS` and `FOCUS_TZ`. The defaults are examples. A person sets their own best hours.
- **The design gate orders by commit position, not commit time.** A rebase rewrites times. Position survives it.
- **The only exemption is small and written down.** At most 30 changed lines and a `design-exempt:` line with a reason in a commit message.
- **The hook is an example, not an installer.** The reader copies it by hand into one repository after reading it. Nothing here edits git settings.
- **Tiers, not model names.** `top`, `mid`, `cheap`. The reader maps their own models to tiers. Named models would go stale.
- **Planner and critic are separate routines.** The critic may not read the plan. The check on this is weak (it trusts the critic's own source list) and the text says so.

## What stays out

- Schedules, triggers and chat posts. The routine designs name a suggested time; the reader's host owns the schedule.
- Any measured saving. The designs say how to count cost before adding a routine. They carry no figures.
- A model router. `tier_route.py` answers one question (which tier is allowed now) and logs it.
- A second routing skill. `budget-aware-routing` already covers how to choose a model and effort. This skill adds only the time-of-day and phase rule.

## Failure modes

- A check that can be satisfied by editing its own state file. Mitigation: the reference names which routine may write each file, and says the checks prove shape and timing, not truth.
- A design file with no content. Mitigation: a design file needs at least three non-blank lines and must still exist at the branch tip.
- A hook that blocks work with no way forward. Mitigation: every block message names the fix; old branches are grandfathered by date; out-of-scope folders pass silently.
- A principle list that reads as doctrine. Mitigation: each routine has a review-by date and is kept, changed or dropped from its pass and fail log.

## Test plan

- `python3 scripts/validate_repo.py` and `python3 -m unittest discover -s tests -v`.
- Each script's `--selftest`.
- Hook: real `git push` to a bare repository in a temporary folder. Cases: design after code rejected, no design rejected, design before code accepted, small change with and without the exempt line, over the line limit with the exempt line, grandfathered branch, deleted ref, out-of-scope folder, chained hook failing, chained hook passing.

## Rollback

Delete `skills/focus-routines/`, `tests/test_focus_routines.py`, and the catalog, decision, verification and attribution lines that name the skill.
