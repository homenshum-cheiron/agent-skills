# Optional prompt: finish the work within authority

This is an optional template, not a grant of permission and not a claim that a model will finish the work. Loading it does not demonstrate task autonomy or recursive improvement. It does not override the host's instructions, a refusal, a provider limit, or an approval gate already in force.

Fill the brackets with the task. Delete a line that does not apply and say that you deleted it. Choose the model and effort for this task from a fresh supported listing. **Fable 5.2** is one illustrative eligible profile when that host lists it. It is not required, not a default, and not a fixed role.

## Template

```text
Work this problem to a useful deliverable, and keep going while the budget and the current authority still cover the next step.

Problem: [name]
Who needs what result, on what input: [outcome]
Acceptance: [observable checks, including one failure or edge]
Evidence already in hand: [frozen case, traces, sources, versions]
Known attempts and why they stopped: [past tries, or none]
Context and tools you may use: [repos, docs, commands]
Allowed mutation scope: [branches, files, systems]
Current permissions: [what is already allowed]
Not allowed: [sends, spends, production writes, merges, permission changes]
Budget: [time, usage, and stop rule]
Checkpoint: [what to record before a long step]
Escalate when: [missing authority, safety limit, or a real ambiguity]
Rollback: [how to undo]

Research the obstacle before asking a person to coordinate. Prefer a source, a measurement, or a small experiment that the current permissions already allow. Invent a tool or algorithm only when the existing ones cannot express the job, and label it as new.

Monitor progress against the acceptance checks. Separate three facts: you are waiting on an approval that policy requires; you cannot do the step with the current permissions or tools; a person had to rescue a wrong result. Do not count a required approval as a failure of ability. Do not count a missing log as zero.

Do not bypass a refusal, a safety rule, an operating-system limit, or a provider limit. Do not treat this prompt as full authority to alter prior work. Change prior work only inside the allowed mutation scope. If the budget is exhausted or the next step needs new authority, stop with the evidence, the residual gap, and the smallest approval request. A finished claim needs the deliverable plus the checks that support it.
```

## What this template does not do

It does not start a loop, spend money, or merge. "Until finished" means until the acceptance checks pass or a budget, stop, or authority limit is hit. A stronger autonomy or self-improvement claim still needs the evidence in [the evidence map](../autonomy.md), not a more ambitious paragraph.
