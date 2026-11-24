---
name: focus-routines
description: "Use when a person or an agent desk has many threads open and little finished, when planning a day or week of agent work, or when designing recurring routines that protect one phase of work at a time. Each rule comes with a check that can fail."
---

# Focus routines

Goal: one phase of work moves to done before the next one opens, and every rule that protects it has a check that can fail. A rule with no failing check is a wish.

This folder is a method plus local checks. It schedules nothing, sends nothing, and selects no model. The reader's host owns schedules and permissions.

## Principles

Eleven short skills, one principle each. Read the leaf skill in full for any principle you apply. Each entry names when it applies, then the rule.

**Attention**

- **Finish One Phase Before Switching** (**principle-finish-one-phase-before-switching**). A second job is about to open while the first is unfinished. Keep one active phase with a hard end time.
- **Busy Is Not Progress** (**principle-busy-is-not-progress**). A day is judged by threads touched. Judge it by whether the one important thing moved.
- **Fixed Times for Messages** (**principle-fixed-times-for-messages**). Pings keep arriving during focused work. Decide once when messages get read.
- **Say No, or Say When** (**principle-say-no-or-say-when**). An ask arrives that is not the active phase. Ask for the deadline and importance, then answer with no or a time.

**Planning**

- **Plan From Past Durations** (**principle-plan-from-past-durations**). Estimating or promising a date. Use what similar jobs really took, plus rework.
- **Deep Work in the Best Hours** (**principle-deep-work-in-best-hours**). Laying out a day. Give the important job whole blocks in your best hours.
- **Start With an If-Then Step** (**principle-start-with-an-if-then-step**). Writing a first step. Name when, where and the first action.
- **Write the Next Step Before Stopping** (**principle-write-the-next-step-before-stopping**). End of a block, a day or a handoff. Done, stuck on, next step.

**Delegation**

- **Best Model on the Hardest Part** (**principle-best-model-on-the-hardest-part**). A run starts in a deep block. Only the active phase gets the top tier.
- **Critic Apart From Planner** (**principle-critic-apart-from-planner**). One agent plans and judges. A fresh-context critic ranks without reading the plan.

**Verification**

- **Design Before Code** (**principle-design-before-code**). Code is about to start. A short design file lands first.

The idea that each rule needs a check that can fail follows [pstack](https://github.com/cursor/plugins/tree/main/pstack) and the talk [All Code Is Slop (Except Mine)](https://www.youtube.com/watch?v=O_zcc6Xl12g).

## The routines

Seven designs, each with a trigger, inputs, an output and one check: [routine designs](references/routines.md).

| Routine | Protects | Check |
|---|---|---|
| Priority critic | critic apart from planner, busy is not progress | `critic_blind` |
| Phase pick | finish one phase, past durations, if-then step | `one_active`, `done_picture` |
| Say-no gate and switch counter | fixed message times, say no or say when | `no_interrupt`, `switch_cap` |
| Residual snapshot | next step before stopping | `snapshot_fresh` |
| Tier routing at peak | best hours, best model on the hardest part | `model_tier` |
| Design-first gate | design before code | `design_gate.py` |
| Weekly reality review | past durations | the review's own row count |

Adopt one routine at a time. Start with the phase pick and the residual snapshot: they need no hook and no other routine.

## Slim before you add

A new routine spends attention and usage. List what already runs and what each run costs, cut or merge first, and add only with the room that frees. Give every routine a review-by date. Details are in the routine designs.

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
