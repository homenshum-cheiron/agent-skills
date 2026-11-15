# Worked example (synthetic): a validator module after a rule change

A team replaced a packet validator's hash check with a stricter schema-first check. The validator's test module has 53 tests. Two fail after the change; the other 51 pass.

## Classification (one pass, pinned mid-tier model, medium effort)

- 46 behavior-pinning, 3 coverage-theater, 3 implementation-coupled, 1 over-strict.
- Coverage-theater example: `test_empty_evidence_is_inconclusive` writes an empty evidence file. The empty file also changes the hash, so the hash-mismatch branch still returns `inconclusive` even if the "empty file" branch is deleted.
- Implementation-coupled example: `test_na_without_rationale_is_invalid` edits `items[2]` by index and asserts only that some finding contains "rationale". Setting a blank rationale on a different item makes the test pass through a different rule.
- Over-strict example: `test_fixed_claim_is_invalid` pins `findings[0]` to the exact message text. The validator's documented contract promises a status and a finding per failed rule, not message wording or order, and no consumer parses the text; that check is cited in the classification. Had the message been a documented user-facing code, the exact assertion would have stayed.
- Mutation checks run in a temporary copy of the module; each records the test's exit status on the mutant (fail) and on restored code (pass).

## Spot-check by script (3 of 7 flagged)

- Empty-evidence rewrite: set the digest to the hash of the empty bytes, assert status `inconclusive` and a finding naming the empty file. The mutation (delete the empty branch) now turns it red.
- N/A-rationale rewrite: look the item up by identifier and assert the finding names that identifier.
- One flagged test (`test_actual_repository`) was judged a false positive: it is an intended repository hygiene gate that fails on any broken link. It stays, reclassified as behavior-pinning for that gate.

## Report

"53 in scope: 47 behavior-pinning (after reclassification), 3 coverage-theater rewritten, 2 implementation-coupled rewritten, 1 over-strict rewritten. 6 rewrites, each with a mutation that turns it red. 0 deleted; 6 originals marked skipped with pointers until review. Suite: 90 run (84 old + 6 rewrites), 83 passed, 7 skipped (6 marked originals, 1 missing optional dependency, unchanged)."
