---
name: unattended-run-setup
description: "Use before launching a long coding-agent job that nobody will watch: set the effort ceiling, write done as a pass/fail check, pre-authorize places and reversible steps, ask every decision up front, state what a subagent costs, switch models only at task boundaries, and require a final report for a reader who never watched."
---

# Unattended run setup

A long job that nobody watches fails in two quiet ways: it stops early with a list of what is left, or it finishes with a report that hides small choices. Both are setup problems. Fix them before the start, because nobody can answer a question mid-run.

Source: a public video walkthrough of frontier-model setup advice (AI Labs, YouTube `EFGvVCpW9zc`, captions read 2026-11-14) and the vendor guidance it cites. Rules marked *video* are one source's report; check your host's docs.

## 1. Pick the mode and the effort ceiling

| Mode | Effort | Why |
|---|---|---|
| Unattended long job, lead or router | high | fewer mistakes, fewer early stops (*video*, vendor guidance) |
| Watched or cost-sensitive work | medium plus a finishing instruction | a person catches early stops |
| Above high (extra-high, max) | avoid unless measured for this task | small score gains for many more tokens (*video*) |

A finishing instruction ("check the definition of done before ending a turn; if an item is open and no hard limit stops you, do it now") reduces unfinished sessions at medium. It does not fix runs that end with a list of what is left. Those need high.

If you keep a measured exception above high (one reviewer step where a higher setting caught defects the default missed), name it with its evidence. Do not leave a silent conflict with the ceiling.

## 2. Write done as a check

Write what done means as commands, tests, or files that must exist, and set the bar high. Add: "Do not stop at a list of remaining work; do the next item, or name the exact limit that stopped you."

## 3. Pre-authorize places, not prompts

List every folder, repo, branch pattern, and test environment the run may change without asking. Then state the reversibility test: steps that can be undone (edit after a backup, new branch, draft pull request, scratch file) go ahead; steps that cannot (send a message, merge, delete without an archive copy, force-push a shared branch, paid spend, production write) wait for a person.

## 4. Ask decisions up front, approve exactly

Before the start, ask every decision the run needs in one message. When a person approves, they name exactly what is approved, not just "go". Record that scope so the run does not ask the same kind of question again.

## 5. State what a subagent costs

Each subagent reads its own context, and the lead re-reads its result. One field report measured a lead plus workers at about 1.7 times a single session on a small feature (*video*); telling the lead what a subagent costs roughly halved how many it started (vendor guidance). Put this in the lead's brief: "Start a subagent only for work that can run at the same time. A plan with fewer than two independent items stays in one session." Pin a model in every subagent definition; an unpinned subagent can inherit the lead's most expensive model.

Write a short task-to-model table in the host instruction file (lead, hard build, simple build, search and log reading, fresh-context review). Keep it a dated, per-host choice, re-read against live capacity (see `budget-aware-routing`).

## 6. Switch models only at task boundaries

A switched model re-reads the whole conversation without the cache discount, and the previous model's hidden reasoning does not carry over. Finish the task, compact or start fresh, then switch. Check your host's cache lifetime instead of assuming one.

## 7. Plain launchers do not read escalation lines

If the instruction files tell a worker to stop with an "escalate" marker that only a wrapper script handles, a worker started by a plain launcher stops with no output. State in the brief which launcher runs the job. Under a plain launcher, the worker finishes at the model and effort it was given, or reports the exact blocker.

## 8. Final report for a reader who never watched

Show actual results (test output, screenshots, diff paths), list every change including small ones, list what was not done and why, and list decisions needed. Summaries tend to drop small changes.

## Rewriting old rules

A model may treat every "never" line as unbreakable. Where a person wants the final say, write "ask before X" and list routine steps that need no approval. Keep "never" for true hard lines. Retire old rules into an archive; do not delete them (see `instruction-hygiene-review`).

Related: `host-loop-guards` (stall stops, hooks), `budget-aware-routing` (model and effort from a fresh read), `one-writer-handoff`.

See the [synthetic worked example](examples/worked.md).
