---
name: host-loop-guards
description: "Use when configuring how a coding agent starts, retries, and stops a task: stall stops, handoff files, protecting the check from edits, and worktree-aware hooks or permissions. Apply per host. Do not install a viral checklist."
---
# Host-loop guards

A short card can make a coding-agent loop look like a missing framework: a script as `done`, a retry cap, a stop hook, and auto-appended standing instructions. Most hosts already ship the primitives. Adopt only the narrow gaps below, as drafts, and only for tasks that already have a deterministic check.

Related skills, by name only: `one-writer-handoff`, `proof-before-review`, and `encode-corrections`. This skill is host loop configuration, not how to write a handoff or score a review.

## Already native (do not rebuild)

- **Claude Code:** hooks, including a Stop hook whose exit 2 can continue the turn; `allow` / `ask` / `deny`; worktrees (`isolation: worktree`); subagents; `CLAUDE.md`. A Stop hook may fire at end of turn. Consecutive blocks can cap. A missing Stop script is often non-blocking. After entering a worktree, `${CLAUDE_PROJECT_DIR}` may still point at the main checkout while the hook working directory follows the worktree.
- **Codex CLI:** sandbox modes (commonly `codex exec -s workspace-write`), approval modes, `AGENTS.md`, `codex exec -o` for a turn artifact, and command hooks. Confirm today's hook contract before treating a hook as a hard gate.
- **Cursor:** rules, `hooks.json` (shell, MCP, stop, session start), local and cloud or background agents. Local hooks may not run on a cloud agent.
- **Other hosts:** skills, subagents, permission or auto-review layers, and routines can stand in for hooks. A missing Stop-hook API is not a reason to invent a second runtime.

Reuse the existing handoff format (`STATE.md`, `EPOCH-N.md`, or `LAST.md`). Do not add a second file format for the same job.

## Adopt (drafts only; do not write live settings from this skill)

### 1. Same-command stall stop, then handoff

If the *same command* or plan fails twice with the *same error*, and nothing about the attempt changed, write what was tried into the existing handoff file and stop. If the agent changed the command or plan, let it continue. Do not hard-code a universal retry cap. Confirm on your own logs first: a later success is often a changed plan, not a third identical try.

### 2. Protect the check from edits

Deny or ask on edits to the check script, CI workflows, and gold fixtures. A green check is worthless if the agent can weaken it. Prefer a hook or permission rule over a standing-file line the model can ignore. This skill describes the draft; it does not grant permissions.

### 3. Worktree-aware hook and permissions audit

Any stop or check hook must run from the hook working directory, not from a project-root variable that may still point at the main checkout. Honor any official "stop hook already active" flag and any block cap. Review `allow` / `ask` / `deny` by undo cost. Use a script as `done` only where it actually measures the claim.

## Skip

- Pasting a whole "harness loop" card into a standing file or into a named model "tonight."
- Auto-appending repeated failures into `CLAUDE.md`, `AGENTS.md`, or editor rules. Promote a repeat into a hook, lint rule, or test, and keep standing files short. Owner-approved corrections belong in a ledger, not an automatic append.
- Treating script green as done for work a script cannot grade.
- A new DAG or worktree framework when the host already isolates worktrees or subagents.

## Park

- A hard-coded retry number until a local log mine exists.
- A Stop-hook check on a repo that has no deterministic check, or on a host whose hook contract you have not verified this week.
- Assuming cloud or background agents inherit local hooks.

## Config drafts (illustrative; adapt names to the repo)

Claude Code, project or user `settings.json` (review before any install):

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Edit(check.sh)",
      "Write(check.sh)",
      "Edit(.github/workflows/**)",
      "Write(.github/workflows/**)"
    ]
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "if [ -x ./check.sh ]; then ./check.sh; rc=$?; [ \"$rc\" -eq 0 ] && exit 0; exit 2; else exit 0; fi",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Run the check from the hook working directory. Map a failed check to **exit 2**; exit 1 is usually non-blocking. A Stop hook is a nudge, not proof of success, and must not loop on a fuzzy condition. See [references/verification-deny-and-standing-files.md](references/verification-deny-and-standing-files.md) for exit codes, deny-before-classifier, sandbox, and shrinking standing files.

Codex: add the same deny or guard as a PreToolUse hook, keep `codex exec -s workspace-write -C <repo> -o <dir>/LAST.md`, and write the stall into `LAST.md` or the existing epoch file. Do not turn a CI-repair hook that *continues* on a failed check into a stall stop; they solve different problems.

Cursor: put the stall rule in a project rule, and add a shell or file-edit guard if the hook API can deny. Do not assume a cloud agent will run that hook.

Other hosts: enforce the stall and "do not edit the check" in a skill; use the host's permission or auto-review layer as the gate.

## Safety

Drafts only. Installing hooks or permission changes needs an explicit owner review. Never paste secrets, private paths, or live settings into a public note. Re-read the host's hook docs on the day you install.
