---
name: focus-routines
description: "Use when a person or an agent desk has many threads open and little finished, when planning a day or week of agent work, or when designing recurring routines that protect one phase of work at a time. Each rule comes with a check that can fail."
---

# Focus routines

Goal: one phase of work moves to done before the next one opens, and every rule that protects it has a check that can fail. A rule with no failing check is a wish.

This folder is a method plus local checks. It schedules nothing, sends nothing, and selects no model. The reader's host owns schedules and permissions.

## The ten principles

1. **Finish one phase before you switch.** An unfinished job keeps part of your attention after you leave it (attention residue, Sophie Leroy, 2009). Interruptions cost depth, not only minutes (Gloria Mark and colleagues). Keep exactly one active phase.
2. **Busy is not progress.** Judge the day by whether the one important thing moved, not by how many threads were touched.
3. **Plan from real past durations.** People underestimate their own jobs even when they know earlier ones ran long (the planning fallacy: Kahneman and Tversky; Buehler, Griffin and Ross). Look up how long the last similar job took, end to end, and add time for rework.
4. **Deep work goes in the best-energy hours.** Give the important job whole blocks. Put messages and chores in low-energy time.
5. **The best model goes on the hardest part.** In a deep block the top model tier belongs to the active phase. Side jobs take a smaller tier. This one is ours, not from the research above.
6. **Write done, stuck, next step before you stop.** An open job with no written next step keeps running in your head. Three lines close it.
7. **Start with an if-then first step.** "At 9:30, at the desk, open the failing parser test" beats "work on the parser" (implementation intentions, Peter Gollwitzer).
8. **Fixed times for messages.** Decide once when messages get read. Do not decide again on every ping.
9. **Say no, or say when.** Ask for the deadline and the importance first. "I am on X; I can look after 3 PM" is a complete answer.
10. **Design before code; critic apart from planner.** A short design file lands before the first code commit. A fresh-context critic ranks the day without reading the plan, and a person sees both when they disagree.

## The routines

Seven designs, each with a trigger, inputs, an output and one check: [routine designs](references/routines.md).

| Routine | Protects | Check |
|---|---|---|
| Priority critic | 2, 10 | `critic_blind` |
| Phase pick | 1, 3, 7 | `one_active`, `done_picture` |
| Say-no gate and switch counter | 8, 9 | `no_interrupt`, `switch_cap` |
| Residual snapshot | 6 | `snapshot_fresh` |
| Tier routing at peak | 4, 5 | `model_tier` |
| Design-first gate | 10 | `design_gate.py` |
| Weekly reality review | 3 | the review's own row count |

Adopt one routine at a time. Start with the phase pick and the residual snapshot: they need no hook and no other routine.

## Slim before you add

A new routine spends attention and usage. Before adding one, list what already runs, how often, and what each run costs. Cut or merge first: move a filter into the trigger so a run never starts, drop overnight and weekend runs nobody reads, replace a status list with the snapshot. Add the new routine only with the room that frees. Give every routine a review-by date, and keep, change or drop it from its pass and fail log. Details are in the routine designs.

## The checks

State lives in small files in one folder: [state files and settings](references/state-files.md).

- [focus_check.py](scripts/focus_check.py) runs the seven state checks. Verdicts are passed, failed, unverified (no data) and inconclusive (unreadable file). Missing data never passes.
- [design_gate.py](scripts/design_gate.py) fails a branch when no design file landed before the first code commit. It orders by commit position, so a rebase cannot reorder it. The only exemption is 30 changed lines or fewer plus a `design-exempt: <reason>` line.
- [tier_route.py](scripts/tier_route.py) answers one question: which tier may this run use now. It logs the answer. It knows no model names.
- [pre-push](examples/pre-push) is an example hook for the design gate with chaining, a folder scope and grandfathering, with [its settings](examples/design-gate.conf.example). Read it, then install it by hand in one repository, with the owner's review.

```sh
python3 scripts/focus_check.py all
python3 scripts/focus_check.py gate-open P2
python3 scripts/design_gate.py . origin/main HEAD --body pr-body.txt
python3 scripts/tier_route.py --want top --phase P1
```

## Limits

- The checks prove shape and timing. A person can still write a done-picture that is vague, or mark an ask urgent that is not. `critic_blind` trusts the critic's own source list.
- The design gate proves a design file came first. It does not prove the design is good or that the code follows it.
- The default deep blocks are examples. Set `FOCUS_BLOCKS` and `FOCUS_TZ` to your own best hours.
- No result is claimed. Whether these routines shorten real work is for the weekly review to measure on your own jobs.

See [the worked example](examples/worked.md).
