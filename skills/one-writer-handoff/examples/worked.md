# Example: schema and UI work (synthetic)

The API writer owns `events/schema.py`; the UI writer owns the event list. Both need a new `attempt_id` field.

Safe parallel work: API writer implements the accepted schema; UI writer builds rendering against the explicit provisional contract; reviewer writes independent repeated-run cases. Integration waits for the tested schema revision.

Unsafe shortcut: coordinator edits the schema in a second worktree while the API writer is still running, then asks everyone to rebase.

Handoff output: “API writer stopped at revision demo-v3 with a clean worktree. Receiver checked it, accepted ownership, and will add the timeout case. UI writer remains read-only on schema files. Reviewer has not approved.”

This is an example of what to verify, not evidence that a real process has stopped.
