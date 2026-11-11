---
name: one-writer-handoff
description: "Use when more than one person or agent could edit the same branch, when handing off a session, or when deciding which free work can start."
---

# One-writer handoff

One writer owns a mutable branch at a time. Readers may run in parallel. Independent work runs in parallel only on independent branches or files.

- Inspect existing branches, worktrees, sessions, and assignments within authorized access before creating another lane. Verify that a branch or file is free instead of assuming it is. Do not write on a branch another person or agent already owns.
- Distinguish the coordinator, the artifact writer, the reviewer, and the release owner when those roles differ. There is one outcome owner. A temporary planner or worker seat does not inherit auto-delegation or a permanent hierarchy.
- Give each writer an exact artifact boundary and dependency contract. Shared schema changes need a single writer or a reviewed contract first.
- Rank waiting work by the nearest sourced deadline it unblocks, then by how much downstream work it unblocks. Two items can run together when neither needs the other's output and they do not share one scarce resource, such as one session or one spend cap.
- Start without an extra ask when the step is free and reversible: offline tests, read-only investigation, a new draft branch, or notes. Paid runs, pushes to branches other people review, merges, force-pushes, and any message to another person still need an explicit go. Do not assign other people's work or raise a spend cap.
- Before transfer, the current writer stops at a known revision. Verify the worktree and any running commands. Preserve uncommitted work. Do not reset or kill another session. Never take over because a timer expired.
- Hand off the outcome and acceptance criteria, the decisions and rejected approaches, the repository identity, the branch, the revision, a dirty-work checkpoint if needed, the evidence and its confidence, the single next action, and the current write owner. Repeat the constraints and approvals still in force. Do not widen them. Link artifacts rather than pasting a transcript. Record the model and effort last used as observed facts, not as a default for the next session.
- The receiving writer re-reads the head and acknowledges ownership before editing. A JSON field, an owner flag, or a handoff file is not a mutex, a lease, a fence, or a grant of send, review, merge, account, or spend authority.
- Auto-transfer write ownership only when a real authority can compare-and-swap the expected head, epoch, fencing token, and owner, and you have observed a verified stop of the old writer. If those mechanisms are absent or untested, do not auto-transfer, and do not describe the runtime as ready. Read-only preparation can continue.
- Bind every test log and review to the repository, the base SHA, and the candidate head SHA. Uncommitted work gets a diff digest, not a claim that a committed revision was reviewed. Right before landing, re-read the head and the required check revisions under the project's declared gates.
- Keep candidate, reviewed, landed, deployed, and live-verified separate. Integrate in dependency order. Do not restack someone else's branch because it depends on yours.

Use [the handoff contract](references/handoff.md), [revision binding](references/revision.md), and [the worked example](examples/worked.md). This is a coordination recipe. Unless a deployment ships and tests fencing, locks, and verified stop, this folder does not enforce them.
