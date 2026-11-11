---
name: bounded-publication
description: "Refresh summaries or boards from reviewed immutable snapshots while preserving human edits, dates, independent statuses, and newer content."
---

# Bounded publication

Review one bounded snapshot, not a moving stream that never settles.

1. Freeze evidence, scope, capture time, source hashes, and the current destination version. Distinguish source event time, evidence capture time, review time, and publication time.
2. Write claims against that snapshot. Label requests, proposals, reported work, verified outcomes, contradictions, and unknowns separately. Include omitted coverage.
3. Validate the complete intended artifact before publication. For multiple parts, track each part separately; do not call independent writes atomic.
4. Fetch the destination freshly. Preserve human notes and unrelated sections. Use a compare-and-swap/version precondition when supported; otherwise do not pretend a fetch-then-write is atomic.
5. On uncertain write outcome, fetch and reconcile before retrying. On conflicts or failed quality checks, retain the last good primary.
6. Verify readback and save a receipt identifying source snapshot, reviewed artifact, destination version, and per-part outcome. Show newer unreviewed activity separately.
7. If sources are offline, keep last-synced snapshots with their original dates and limits. Do not relabel them current or invent an empty report. Missing periods remain unreviewed.

Use [the worked example](examples/worked.md). Publication still requires the destination and sharing scope to be authorized; this method does not verify access permissions for you.
