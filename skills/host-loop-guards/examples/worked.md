# Worked example (synthetic): auditing a host before adopting a loop card

A teammate pastes a short card: "add a stop hook that runs `./check.sh`, cap retries at three, stop after the same error twice, and auto-append repeats into the project instruction file."

## What you do

1. Inventory the host, read-only. Note hooks, permission or approval modes, worktree support, and any existing handoff file. Do not print tokens or environment values.
2. Check whether the repo already has a deterministic check, and whether the agent is allowed to edit it.
3. Mine recent session logs, if they are local and free: how often a second identical command recovers; how often a third does; how often recovery happens only after the command changes.
4. Compare each card element to native support and to that inventory.

## What you write down

- The host already has hooks and permissions. You do not add a new framework.
- You draft (and do not install) a deny rule for the check script and workflows, a stall stop that fires only on a same-command same-error repeat, and a reminder that a stop hook must use its working directory in a worktree.
- You skip auto-append into the standing file, and you skip a script-only done-signal for a design review that no script grades.
- You park a hard "three tries" cap until the log mine is in hand.

The output is a short verdict table plus the config draft. Live settings stay unchanged until the owner reviews the draft.
