# Worked example (synthetic)

All names, numbers, and revisions here are invented.

**Request.** The owner wrote earlier: "Merging my own repositories is on you once tests pass." The agent has pull request 7 open on such a repository, adding one skill folder.

**Sort.** A merge to a repository only the owner controls, reversible with `git revert`. No owner-only category applies. Tier 1.

**Blast radius.** The diff adds a folder and a test file and changes no existing script. The one fact it is safe because of: the validator and the suite read every file the diff touches. Proven by running both on the tip.

**Real check.** On tip `3f9c2a1`: the validator printed `37 skills checked; 0 issues.` and the suite printed `Ran 130 tests ... OK`.

**Second opinion.** A different model got the diff, the one-line intent, and the check output, with no chat history. It reported one finding with a repro: a `post_verify` entry with `"exit_code": "0"` (a string) passed. The agent reproduced it, fixed the comparison, added `test_post_verify_string_exit`, reran both checks on the new tip, and sent the new diff back. The reviewer answered PASS.

**Record and act.** `check_gate.py examples/gate-record.json --log decisions.tsv` printed `act (tier 1)` and appended a `gate` row. The agent merged.

**Verify after acting.** On the merge commit on main, both checks were rerun and added as `post_verify`. The checker still printed `act`. Had either failed, it would have printed `revert (tier 1)` and exited 3, and the agent would have run the recorded `git revert` as a new commit and told the owner.

**Report.** "Merged pull request 7 (Tier 1). Tip 3f9c2a1, reviewed by another model, one finding fixed with a test, post-merge checks green on main."

**What the gate would have refused.** The same pull request on a repository shared with a team is `shared-merge`: the checker prints `needs-owner (tier 2)` and exits 2 however green the checks are.
