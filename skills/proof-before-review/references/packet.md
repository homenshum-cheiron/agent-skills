# Proof packet v1

The JSON packet records a narrow reviewed scope. Required fields:

- `schema_version`: `1`.
- `artifact_revision` and `reviewed_revision`: nonempty exact identities. They must match for a complete result.
- `scope`: nonempty description of the actual claim.
- `checks`: nonempty list. Each check has a unique `id`, `status` (`passed`, `failed`, `blocked`, or `not_run`), `command`, and `evidence`.
- `exit_code`: required integer for an executed check. A passed check must have zero; failed checks may have any integer (some tests detect a semantic failure despite zero exit).
- `reason`: required for blocked or not-run checks; those checks must not supply an exit code.
- `evidence`: list of local objects with `path` and lowercase `sha256`. Executed checks require at least one nonempty evidence file. Paths must resolve under the packet's directory, with no symlinks or traversal.

Run `python3 scripts/check_packet.py path/to/packet.json` from the skill folder, or provide the script's full path.

Output states and exit codes: `complete` (0), `failed` (1), `inconclusive` (2), or `invalid` (3). Revision mismatch, blocked checks, and missing/changed evidence are inconclusive. Invalid fields are invalid. A declared failure remains failed unless the packet itself is invalid.

**Limits:** the checker validates consistency and bytes, not whether a command ran, evidence is authentic, the test is relevant, or the listed checks cover the claim. Even `complete` is not “approved” or “merge-ready.” Human review and release permission remain separate.
