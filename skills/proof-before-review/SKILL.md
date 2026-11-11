---
name: proof-before-review
description: "Review a change using executed checks tied to the exact revision, independent expected outcomes, and explicit untested scope."
---

# Proof before review

A review without executed relevant tests is a code-only review. Say so. Do not convert skipped CI into a pass.

1. Freeze the artifact revision, diff, scenario scope, and accepted outcomes before judging the change. Read the repository's current instructions and test commands.
2. Inspect the changed path and adjacent failure modes. Check both the intended fix and what the fix could break: repeated calls, interruption, concurrency, stale data, and error handling when applicable.
3. Run the cheapest relevant checks, then the integration checks needed by the claim. For a fix or improvement claim, compare the candidate with the previous stable version on the same frozen inputs; show whether the old failure is reproduced and the new result changes it. If a required environment is unavailable, mark that check blocked and explain the missing prerequisite. Do not run a paid or production experiment merely to complete the matrix.
4. Separate the builder's claims from the reviewer's observations. Where practical, give the reviewer raw inputs, acceptance criteria, artifacts, and receipts rather than a persuasive conclusion.
5. Recheck after changes, rebases, or dependency updates. Record passed, failed, blocked, and not-run checks individually. Distinguish patch-equivalence from tests run on the new revision.
6. Report findings by impact with a reproduction, expected/actual output, exact evidence, and proposed next action. A passing test suite and an approval are separate; neither authorizes release.

Use [the proof packet format](references/packet.md) for machine-checkable receipts and [the worked example](examples/worked.md) to avoid overstating focused tests. The [checker](scripts/check_packet.py) only validates bookkeeping and evidence hashes; it cannot judge test relevance or authenticity.
