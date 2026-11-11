---
name: proof-before-review
description: "Use when reviewing a change, stack, or claim that tests pass, and when scoring a pull-request body or reading CI and approval state."
---

# Proof before review

A review without the relevant executed checks is a code-only review. Say so. Do not convert skipped, queued, or running CI into a pass.

1. Freeze the target-base SHA, the merge-base SHA, and the tip SHA, plus the diff, the scenario scope, and the accepted outcomes. A branch name is not a revision. Uncommitted work needs a diff digest and cannot claim a review of a committed tip. Read the repository's current instructions and test commands.
2. Inspect the changed path and adjacent failure modes: repeated calls, interruption, concurrency, stale data, and error handling when they apply.
3. Run the cheapest relevant checks, then the integration check the claim needs. For a fix or improvement, compare the named baseline and the tip on the same frozen inputs. Record the command, the build or deployment identity, the config path, environment variable names only, the observed output, and the pass or fail criterion. If a required environment is unavailable, mark that check blocked and name the missing prerequisite. Do not run a paid or production experiment merely to fill a matrix.
4. Match the surface to the claim. A unit test, a green CI job, or a bot summary does not prove a running API, UI, or CLI behavior. Evidence that includes unmerged parent work is combined-stack evidence: name the parent and the composition you ran. Do not pretend a dependent child is isolated, and do not require isolation the stack makes impossible. A documentation or comment-only change may record live-proof N/A with a reason and the SHA. Missing required proof is unproven or blocked, not N/A.
5. Separate the builder's claims from the reviewer's observations. Where practical, give the reviewer the raw inputs, the acceptance criteria, the artifacts, and the receipts rather than a persuasive conclusion.
6. Recheck after changes, rebases, or dependency updates. Record passed, failed, blocked, and not-run checks individually. Patch equivalence is not a test run on the new revision. Follow the project's declared gates for whether an older review still covers a non-semantic follow-up. Do not invent a stricter fresh-human rule, and do not treat a stale review as current when the head moved in a way that gate cares about.
7. Keep candidate, reviewed, landed, deployed, and live-verified separate. A bot approval is not a human approval. Honor a configured bot-owned gate as that gate. Give each distinct actionable automated finding on the current tip a disposition: fixed with evidence, rejected with a reproducible reason, duplicate of a named finding, or unresolved. An unresolved material finding blocks a ready claim. See [review state](references/review-state.md).
8. When writing or checking the pull-request body, score the nine coverage prompts as supported over applicable, and list N/A only with a reason. Coverage is not a quality certification. See [coverage prompts](references/pr-coverage.md).

Report findings by impact with a reproduction, the expected and actual output, the exact evidence, and the next action. A passing suite and an approval are separate facts. Neither authorizes release. Prefer an empirical check over an abstract opinion. A second reviewer is a separate decision, not an automatic companion of a stronger model.

Use [the proof packet format](references/packet.md), [the worked review](examples/worked.md), and [the coverage example](examples/coverage-scored.md). The [checker](scripts/check_packet.py) validates bookkeeping and evidence hashes only. The [coverage scorer](scripts/score_coverage.py) checks that the nine marks add up. Neither judges relevance, authenticity, or quality.
