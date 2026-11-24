---
name: principle-finish-one-phase-before-switching
description: "Apply when a second job is about to open while the first is still unfinished, or when a day has several threads open and none closed. Keep exactly one active phase and give it a hard end time."
disable-model-invocation: true
---

# Finish One Phase Before Switching

An unfinished job keeps part of your attention after you leave it. That leftover attention makes the next job worse ([Leroy 2009](https://doi.org/10.1016/j.obhdp.2009.04.002)). In those studies, finishing helped most when it happened under time pressure, so give each phase a hard end time. Interrupted work is often picked up again only after other jobs in between ([Mark, Gonzalez and Harris 2005](https://ics.uci.edu/~gmark/CHI2005.pdf)).

**Pattern:**
- Keep exactly one phase active. Every other job is queued or parked, with a written next step.
- Open a new phase only when the current one meets its exit criteria, or is parked on purpose.
- Give the active phase an end time, not only a goal.

**Check:** `one_active` and `gate-open` in **focus-routines**.
