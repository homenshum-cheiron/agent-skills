---
name: route-failures
description: "Separate data-operation incidents from agent/tool/reasoning failures, with distinct owners, evidence, recovery paths, and service objectives."
---

# Route failures

A missing answer can originate in collection, ingestion, retrieval, tools, or reasoning. Do not route all of them to one repair loop.

1. Capture the observable failure and expected result, then locate the first boundary where actual behavior diverges. Preserve “unknown cause” until evidence supports a cause. If the timeline, the failure boundary, or the recovered state is still unclear, write that smallest packet before choosing a repair. Reading back an unchanged status does not need a new packet.
2. Use the [routing guide](references/taxonomy.md) to separate data operations from agent execution/evaluation. Each system owns its own service objectives, incident state, and repair policy; do not invent SLA values.
3. Define the exposure policy separately from failure detection: which diagnostics belong in admin incidents, internal observability, user status, or model context? Follow the product's explicit contract rather than silently leaking operational fields into answers. In a product that keeps source health admin-only, enforce that boundary in responses, prompts, and traces. Preserve ordinary source/version citations needed for the product, and never turn “not ingested” into “does not exist.”
4. Record scope, run/revision, timestamps, observed evidence, suspected cause, owner or owner-unknown, attempt history, and next permitted action. Capture durable start and terminal state when implementing run tracking; a row written only after success cannot detect a missing start.
5. Retry only when the cause, idempotency, limits, and permissions support it. Respect site refusal; do not treat it as permission to evade controls. Escalate unknown or repeated failures rather than looping indefinitely.
6. Keep code-quality tests separate from runtime availability checks. A temporary site outage should not be a product-code CI failure; a deterministic parser regression still belongs in tests.

Use [the worked example](examples/worked.md). This skill is a design method, not an installed monitor or automatic repair service.
