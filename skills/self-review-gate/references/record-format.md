# Gate record

One JSON object per action, with no duplicate fields. Fields the checker reads:

| Field | Tier | Meaning |
|---|---|---|
| `action` | all | One line: what you are about to do. |
| `tier` | all | 0, 1, or 2, as you sorted it. |
| `reversible` | all | `true` only when a recorded command undoes it fully. |
| `categories` | all | Owner-only tags, if any. Any tag forces Tier 2. |
| `revert` | 0, 1 | The exact command or steps that undo the action. |
| `tip` | 1 | Commit SHA the checks and review ran on. |
| `blast_radius` | 1 | What else it could break, and the one fact it is safe because of. |
| `checks` | 1 | List of `{command, exit_code, observed, revision}`. `exit_code` must be the integer 0 and `revision` must equal `tip`. |
| `review` | 1 | `{kind, author_is_reviewer, saw_author_reasoning, revision, evidence, verdict, findings}`. `verdict` must be `PASS` on this tip. `evidence` must be a saved file that says `Reviewed revision: <tip>`, names no other revision, has no more `Finding:` lines than `findings` entries, and ends with a line reading only `PASS`. `findings` is required, empty when there were none. |
| `review.findings` | 1 | List of `{title, disposition, evidence}`; disposition is fixed, rejected, duplicate, or unresolved. |
| `post_verify` | after acting | One check object, or a list, run against the landed result. A failure returns `revert` whatever else the record says. |
| `evidence` | optional | Pointer for the log row; defaults to `review.evidence`. |

`categories` is a list of strings. An unknown tag blocks, so a typo cannot slip past. Owner-only categories: external-send, shared-merge, secret, paid-over-cap, delete-user-data, kill-process, infra-restart, answer-key, force-push, skip-checks, permission-change.
