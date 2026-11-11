# Handoff contract

Use only fields that matter to the actual task. Do not create a bureaucracy for a small edit.

- Outcome and declared acceptance criteria.
- Current decisions, rejected alternatives, and unresolved questions.
- Repository identity, branch, base SHA, candidate head SHA, worktree state, and pending command state. Uncommitted work includes a diff digest.
- What is done, with evidence and confidence: verified, unproven, or not started.
- The single next action and who owns writes now.
- Files the receiver may edit and shared boundaries it may only read.
- Dependencies with exact versions or receipts.
- Tests already run, the revision they ran on, and what still needs execution.
- Constraints and approvals still in force. Do not widen them. Name any action that needs new approval.
- Model and effort last used, as observed. They are not a default pin for the next session.
- Rollback or recovery, and a stop condition.

Report in this order: the changed capability or decision; the evidence and its scope; the remaining gap and the next action plus the owner. Distinguish draft, verified fix, in review, landed, deployed, and live acceptance. Do not lead with a count of tests or files.

Transfer only necessary context. A summary points at recoverable artifacts. It does not replace them. If a prerequisite is missing, say which independent task can still proceed.

A completed contract is a note the next reader can use. It is not a lock, not a verified stop, and not permission to push, merge, send, or spend. Borrowed planner or worker seats end with the task. They do not create a standing boss.
