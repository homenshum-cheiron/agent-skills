---
name: principle-plan-from-past-durations
description: "Apply when estimating a job, picking how much fits in a day, or promising a date. Look up how long the last similar jobs took end to end, then add time for rework."
disable-model-invocation: true
---

# Plan From Past Durations

People underestimate their own jobs even when they know earlier ones ran long. This is the planning fallacy ([Buehler, Griffin and Ross 1994](https://doi.org/10.1037/0022-3514.67.3.366)). The fix is to use outside numbers: what similar jobs actually took.

**Pattern:**
- Find the last three similar jobs and their real start-to-merge times.
- Split each one into waiting to start, working, waiting for review, rework and waiting to merge. The largest part is often not the coding.
- Estimate from those numbers plus a rework buffer. Label it an estimate.
- Once a week, put the actuals next to the estimates and update the table.

**Check:** the weekly reality review in **focus-routines**.
