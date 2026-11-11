# Review, CI, and landing state

Say which fact you have. Follow the project's declared gates instead of inventing a stricter public policy.

- Where a human approval is required, a bot review with state APPROVED is not that human approval. Record the reviewer type, the head SHA the review binds to, and the required policy. A bot comment that says "no issues," or a successful check, is also not human approval.
- Honor an explicitly configured bot-owned gate where the host supports it. That gate is not a separate human gate, and it does not grant merge authority.
- Before calling a tip ready for human review, account for each distinct actionable automated finding with current-tip evidence, a reasoned rejection, a named duplicate, or an unresolved mark. Unresolved material findings stay visible. Do not churn on unsupported nitpicks, and do not page a human for bot-only activity.
- Queued or in-progress checks are not green. Keep these facts separate: tests completed successfully, skipped checks, unfinished checks, human approval, queue state, content landed, deployment, and live verification.
- Re-read check and review revisions against the current head before landing, under the declared gates. If the head moved, a prior result counts only when that gate says it still applies, for example a non-semantic follow-up. Do not invent a rule that every new commit needs a fresh human. Do not treat a stale review as current when the head moved in a way the gate cares about.
- For a successor, link the old and new identities. After a squash or cherry-pick, verify preserved SHAs or patch content. Distinguish carried-over work from an independently authored replacement. Closed-unmerged can still mean the content landed elsewhere. A merged successor is not proof of deployment or live use.
- Waiting on a gate does not grant a send, a paid run, or a new permission.

Synthetic illustration: tip `ddd4444` has a configured bot-owned lint gate passing and one human review still pending. CI is queued. The honest report is: lint gate passing (bot-owned), human approval missing, CI not green, not landed, not deployed, not live. A later squash successor `eee5555` links to the old pull request and notes patch-content lineage because the SHA changed.

Those SHAs are teaching labels. This folder does not install a merge bot.
