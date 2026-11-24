---
name: principle-design-before-code
description: "Apply when a branch, a pull request or an agent run is about to start code. A short design file lands in a commit before the first code commit."
disable-model-invocation: true
---

# Design Before Code

The long jobs are often the ones whose plan changed after the code started. Writing the design first is cheap, and a check on commit order makes the rule something that can fail instead of a wish. Turning a repeated correction into a check, rather than another line of instructions, follows [pstack](https://github.com/cursor/plugins/tree/main/pstack) and the talk [All Code Is Slop (Except Mine)](https://www.youtube.com/watch?v=O_zcc6Xl12g).

**Pattern:**
- A few lines are enough: the problem, the outcome, what is in and out, how it will be tested.
- Order is by commit position, so a rebase cannot reorder it.
- The only exemption is a small change with a written reason.

**Check:** `design_gate.py` and the example `pre-push` hook in **focus-routines**.
