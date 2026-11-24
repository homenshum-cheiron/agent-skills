---
name: principle-busy-is-not-progress
description: "Apply when judging a day, a standup, or an agent's report by how many threads were touched. Judge by whether the one important thing moved."
disable-model-invocation: true
---

# Busy Is Not Progress

Twenty touched threads and an unmoved main job is a bad day. One finished phase and nineteen untouched threads is a good one.

**Pattern:**
- Write the done-picture for the active phase before the day starts: what is true when it is done.
- At the end of the day, report the done-picture first: met, partly met (with what is left), or not met.
- Count activity only after that, and only if it explains the outcome.

**Check:** `done_picture` in **focus-routines**.
