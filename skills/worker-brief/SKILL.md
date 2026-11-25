---
name: worker-brief
description: "Use when writing a brief for a worker or subagent: state the job, the why, guardrails with a reason each, and done-criteria as checks, then lint the brief before dispatch."
---

# Worker brief

A brief that only lists steps produces a worker that follows the steps and misses the outcome. Write the outcome, the reason, the few limits that matter, and the checks that would prove it, then let the worker choose the how.

## The four parts

1. **Job.** The outcome, in plain words, covering the whole task, not one step. Do not fill this part with a numbered how-to.
2. **Why.** Why the job exists and why it matters now. Every instruction works better with a reason behind it. An empty Why fails the checker.
3. **Guardrails.** Only the limits that really matter: what not to touch, what not to send, what must stay local. Write each one as you would to a colleague, with a `because`. Soften words like "critical" and "you must"; they tend to make a model overdo the rule.
4. **Done means.** A few checks or examples the worker can run. Each check should be pass or fail, and should point at a source or command. Tell the worker not to stop until every check passes, and to report each one.

When you cannot fill the four parts yet, interview the requester until you can, then write the brief and lint it. Do not dispatch a half-filled brief.

If a previous run was bad, treat that as feedback on the brief: say what was off, why, and what good looks like, then re-dispatch the fixed brief rather than chaining "also fix X" follow-ups.

## Checker

```sh
python3 skills/worker-brief/scripts/lint_brief.py path/to/brief.md
```

The checker exits 1 when a heading is missing, Why is empty, a guardrail has no `because`, Done means has no testable check, or the Job section is more than half numbered how-to steps.

See the [worked example](examples/worked.md) and a [template](references/template.md).
