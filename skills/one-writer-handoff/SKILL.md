---
name: one-writer-handoff
description: "Coordinate parallel engineering work and transfer ownership without concurrent writes, stale context, or duplicate stacks."
---

# One-writer handoff

Parallelize by independent artifacts. Do not multiply writers on one branch to make work appear faster.

- Inspect existing branches, worktrees, sessions, and assignments within authorized access before creating another lane. Distinguish the coordinator, artifact writer, reviewer, and release owner.
- Give each writer an exact artifact boundary and dependency contract. Readers can investigate in parallel; shared schema changes need a single writer or a reviewed contract first.
- Before transfer, ask the current writer to stop at a known revision. Verify the worktree state and any running commands. Preserve uncommitted work without resetting or killing another session.
- Handoff the goal, latest decisions and rejected approaches, branch/revision, changed files, test receipts, unresolved decisions, and permitted next action. Link source details rather than pasting an entire session.
- The receiving writer verifies the revision and acknowledges ownership before editing. A declared `owner` field is not a mutex or a lease. If the previous writer cannot be verified idle, continue read-only work elsewhere.
- Integrate in dependency order. Never restack a teammate's branch just because it depends on yours; coordinate that boundary.

Use [the handoff contract](references/handoff.md) and [the worked example](examples/worked.md).
