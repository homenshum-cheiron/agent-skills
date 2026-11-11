# Revision-bound handoff

Landing by branch name can accept code nobody reviewed. Bind evidence to an immutable revision, and re-read that binding before land.

1. Record the repository identity, the base SHA, the branch, and the candidate head SHA with every test log and review.
2. Uncommitted work needs a diff digest. It cannot claim a review of a committed revision.
3. Right before landing, re-read the pull-request head and the revisions of the required checks and reviews, following the project's declared gates. Stale evidence stops the landing when the gate requires a current binding. A non-semantic follow-up follows those same gates. Do not invent a stricter rule.
4. Keep candidate, reviewed, landed, deployed, and live-verified as separate states.
5. A ledger or a template is not authentication, not a merge gate, and not a spend authorization.

Synthetic illustration: review and CI passed on `bbb2222`. A new commit `fff6666` is on the branch. Landing waits until the required checks and review are rebound to `fff6666`, unless the declared gate explicitly treats that follow-up as covered. After merge, record landed. Deployed and live stay unproven until those surfaces are checked. Both SHAs are teaching labels.

A longer public treatment of long-running requests and revision-bound handoffs is the setup kit document at <https://github.com/HomenShum/codex-claude-cursor-setup/blob/20c3c62f775e36560ab092e5b249b3da44a14fa6/docs/long-running-goals.md> (MIT), pin inspected 10 Nov 2026 and file presence rechecked 11 Nov 2026. That document is cited, not copied. This skill does not configure branch protection, and it does not modify the setup kit.
