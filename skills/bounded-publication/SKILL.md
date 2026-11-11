---
name: bounded-publication
description: "Use when refreshing a summary or board from a reviewed snapshot, or when filing a finding that later readers must be able to retrieve, including rejected and superseded lines."
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
8. Append findings. Do not overwrite history. When a finding is superseded, add a new line and keep the old one so retrieval returns both. Give every stored fact a source, a timestamp, and whether that source is trusted (the owner or our code) or untrusted (the web, tool output, or someone else's message). Do not self-certify a promotion. A well-formed record is not proof of behavior. If current code disagrees with an accepted requirement, report the mismatch instead of treating the code as the intent.

Use [the worked example](examples/worked.md). Publication still requires the destination and sharing scope to be authorized; this method does not verify access permissions for you. This skill does not create a board product, and it does not promote a finding into production.
