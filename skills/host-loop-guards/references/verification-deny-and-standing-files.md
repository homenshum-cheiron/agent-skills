# Verification, deny rules, and standing files

A short addition to [the parent skill](../SKILL.md). Official hook and permission contracts change; re-read the host docs on the day you install. Drafts only.

## Hook exit codes (Claude Code)

On Claude Code, a hook that should stop a tool call, or send the model back at Stop / task-complete, must **exit 2**. Exit 0 is success. Exit 1, or any other nonzero code, is usually a *non-blocking* error: the turn or task can still be marked complete. A verify script such as `./check.sh` should be wrapped so any failure becomes exit 2:

```bash
if [ -x ./check.sh ]; then
  ./check.sh
  rc=$?
  if [ "$rc" -eq 0 ]; then exit 0; fi
  exit 2
else
  exit 0
fi
```

Run it from the hook working directory. Honor any official "stop hook already active" flag and any consecutive-block cap. Do not copy this exit-code mapping onto another host; read that host's contract first.

## Deny rules are the hard layer

An approval classifier (Claude Code auto mode, or a similar reviewer on another host) is a judgment call. Official guidance is that deny and ask rules, and pre-tool hooks, run *before* that classifier. If the model gets a change wrong, ask whether you can take it back. Wrong code that you can revert can stay with the model. A secret in the transcript, a discarded uncommitted change, or a force-push generally belongs in `deny` or `ask`.

A `Read` deny on `.env` also covers a direct `cat` of that file in current Claude Code docs. It does not cover a test or helper script that opens the file later. Permissions decide whether a tool call starts, not what a running process can reach. A host sandbox, when available, is what enforces the same file and network limits on child processes. Hooks, MCP servers, and the host process itself may still run outside that sandbox.

## Standing files stay short

A project instruction file (`CLAUDE.md`, `AGENTS.md`, or editor rules) should hold what the model cannot see from the code, plus owner-approved locks. It should not shout older-model steering ("IMPORTANT", a row of exclamation marks) and it should not auto-append every failure. If the host has an official audit or doctor command, run it and *review* the cuts. Do not delete owner policy just to hit a line cap.
