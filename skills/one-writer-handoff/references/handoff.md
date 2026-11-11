# Handoff contract

Use only fields that matter to the actual task; do not create a bureaucracy for a small edit.

- Outcome and acceptance criteria.
- Current decisions, rejected alternatives, and unresolved questions.
- Exact repository/artifact, branch, revision, worktree state, and pending command state.
- Current writer and verified stop acknowledgement; receiver acceptance.
- Files the receiver may edit and shared boundaries it may only read.
- Dependencies with exact versions or receipts.
- Tests already run, their revision, and what still needs execution.
- Existing permission scope and any action that needs new approval.
- Rollback/recovery and a stop condition.

Transfer only necessary context. A summary should point to recoverable artifacts, not replace them. If a prerequisite is missing, say which independent task can still proceed.
