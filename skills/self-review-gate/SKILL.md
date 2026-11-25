---
name: self-review-gate
description: "Use when the owner has delegated a reversible action, such as merging to a repository they alone own, editing local config, or tuning a routine without raising cost, and you would otherwise stop to ask. Run a recorded self-review that stands in for the human step, then act, verify, and revert on failure."
---

# Self-review gate

The owner is the bottleneck when every reversible step waits on them. This gate replaces their sign-off with evidence on the actions they have handed over, and only those. It never widens what they handed over. The destination project's declared gates still decide.

## Tiers

Sort the action before anything else. When unsure, pick the higher tier.

- **Tier 0, act.** Reversible, private, and inside your own workspace: local files, notes, drafts nobody else sees, a branch nobody else writes. Log a row and go.
- **Tier 1, gate then act.** Reversible but visible or shared with the owner's own systems: a merge to a repository the owner alone controls, a local config edit, a routine change that does not raise cost, a draft pull request on a shared repository. Run every step below.
- **Tier 2, owner only.** Anything another person reads or owns, anything irreversible, or anything in the checker's owner-only list: external messages, merges on shared repositories, credentials, spend over the cap, deleting user data, stopping processes you did not start, restarting shared infrastructure, sealed grading material, force-push, skipped checks, wider permissions. Draft it and ask. A passing gate never lowers a Tier 2 action.

The owner moves an action between tiers in writing. An agent's or reviewer's say-so never does. See [tier rules](references/tiers.md).

## Tier 1 steps

1. **State the change and its blast radius.** One line on what changes, and one on what else it could break. Name the one fact the change is safe because of and prove it if it is cheap. Freeze the tip as a commit SHA.
2. **Run the real check.** Run the repository's own tests and the live check the claim needs, on that tip. Record the command, the exit code, and what it printed. A green build is not a live check. Script the check when you can so the reviewer and you can rerun it.
3. **Get an adversarial second opinion.** Give a different model, or a fresh agent that never saw your session, only the diff, the intent in one sentence, and your recorded checks. Leave out your reasoning so it judges what you did, not what you said. Ask it to break the change and prove each finding with a run. Use subscription agents you already have; do not start a paid API run for this. See [reviewer brief](references/reviewer-brief.md).
4. **Dispose of every finding.** Each one is fixed with evidence, rejected with a reproducible reason, or a duplicate. An unresolved finding blocks. If you change the code, the tip moves: rerun step 2 and get the review again on the new tip.
5. **Record the decision.** Fill the [gate record](references/record-format.md) and run the checker. It appends one row to the decision log.
6. **Act.** Only on verdict `act`.
7. **Verify after acting.** Rerun the check against the landed result, for example the merge commit on the default branch. Add it as `post_verify` and rerun the checker.
8. **Revert on failure.** On verdict `revert`, run the recorded revert path at once, as a new commit or a restore, never a history rewrite. Log the revert and tell the owner.

## Checker

```sh
python3 skills/self-review-gate/scripts/check_gate.py gate.json --log decisions.tsv
```

Exit 0 means act, 1 blocked, 2 needs the owner, 3 revert now. Add `--rerun --cwd <repo>` to rerun each recorded check command instead of trusting the recorded exit code. The checker verifies bookkeeping: each step is recorded, green, on the same tip, with a reviewer verdict of PASS and evidence files that exist. It does not judge the review or grant permission.

## Done means

- [ ] `check_gate.py` exits 0 on the record before acting.
- [ ] The decision log has a `gate` row whose evidence path resolves.
- [ ] `post_verify` is recorded and the checker still exits 0 after acting.
- [ ] The report to the owner names the tier, the tip, the reviewer kind, and each finding's disposition.

## When not to use

Tier 2 work, product direction, or a choice the owner asked to make. A gate proves an action is safe to take. It does not prove it was the right thing to want.

See the [worked example](examples/worked.md) and its [record](examples/gate-record.json).
