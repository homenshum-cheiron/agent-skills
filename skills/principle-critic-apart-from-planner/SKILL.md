---
name: principle-critic-apart-from-planner
description: "Apply when one agent both plans the day and judges what matters most. A fresh-context critic ranks the work without reading the plan, and a person sees both when they disagree."
disable-model-invocation: true
---

# Critic Apart From Planner

A planner that grades its own plan tends to agree with it. A separate critic that has not seen the plan gives a second opinion that is not anchored by it.

**Pattern:**
- The critic ranks from messages, open reviews, the calendar and recent state. It must not read the plan files.
- When the critic and the planner disagree, show both, one line each. Neither overwrites the other.
- Prefer a critic that cannot open the plan files to one that promises it did not. A self-reported source list is advice, not proof.
- Even a blocked critic can pick up hints of the plan from shared messages or history. Say so.

**Check:** `critic_blind` in **focus-routines**. It trusts the critic's own source list.
