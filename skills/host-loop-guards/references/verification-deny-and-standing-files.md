# Verification, deny rules, and standing files

A short addition to [the parent skill](../SKILL.md). Official hook and permission contracts change; re-read the host docs on the day you install. Drafts only.

## Hook exit codes (Claude Code)

On Claude Code, a hook that should stop a tool call, or send the model back at Stop / task-complete, must **exit 2**. Exit 0 is success. Exit 1, or any other nonzero code, is usually a *non-blocking* error: the turn or task can still be marked complete.

Wrap the project's verification script so any failure becomes exit 2: if the script is executable, run it, exit 0 on success, and exit 2 on any other code; if it is missing, exit 0. This skill does not ship that script. Run it from the hook working directory. Honor any official "stop hook already active" flag and any consecutive-block cap. Do not copy this exit-code mapping onto another host; read that host's contract first.

An illustrative Claude Code settings draft would deny reads of environment and secrets files, and deny edits to the verification script and CI workflow files, plus a Stop hook that runs the wrapper above. Review and adapt before any install. Do not paste secrets or live settings into a public note.

## Deny rules are the hard layer

An approval classifier (Claude Code auto mode, or a similar reviewer on another host) is a judgment call. Official guidance is that deny and ask rules, and pre-tool hooks, run *before* that classifier. If the model gets a change wrong, ask whether you can take it back. Wrong code that you can revert can stay with the model. A secret in the transcript, a discarded uncommitted change, or a force-push generally belongs in `deny` or `ask`.

A read-deny on environment files also covers a direct print of those files in current Claude Code docs. It does not cover a test or helper script that opens the file later. Permissions decide whether a tool call starts, not what a running process can reach. A host sandbox, when available, is what enforces the same file and network limits on child processes. Hooks, MCP servers, and the host process itself may still run outside that sandbox.

## Standing files stay short

A project instruction file (the host's usual project instruction filename, or editor rules) should hold what the model cannot see from the code, plus owner-approved locks. It should not shout older-model steering ("IMPORTANT", a row of exclamation marks) and it should not auto-append every failure. If the host has an official audit or doctor command, run it and *review* the cuts. Do not delete owner policy just to hit a line cap.
