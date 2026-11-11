# Example: schema and UI work (synthetic)

The API writer owns `events/schema.py`; the UI writer owns the event list. Both need a new `attempt_id` field.

Safe parallel work: API writer implements the accepted schema; UI writer builds rendering against the explicit provisional contract; reviewer writes independent repeated-run cases. Integration waits for the tested schema revision.

Unsafe shortcut: coordinator edits the schema in a second worktree while the API writer is still running, then asks everyone to rebase.

Handoff output: “API writer stopped at revision demo-v3 with a clean worktree. Receiver checked that SHA, accepted ownership, and will add the timeout case. UI writer remains read-only on schema files. Reviewer has not approved. No compare-and-swap authority is configured, so a second session does not take the branch automatically. The handoff does not grant a merge or a message send.”

A docs typo can start on a sibling branch while demo-v3 is occupied. It does not push onto the API writer's branch. If the API writer's stop cannot be verified, the sibling session keeps reading.

This is an example of what to verify, not evidence that a real process has stopped, and not a lock.
