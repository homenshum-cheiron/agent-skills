---
name: budget-aware-routing
description: "Plan bounded planner/worker execution from verified capabilities, shared account limits, explicit budgets, and outcome-based escalation."
---

# Budget-aware routing

Use expensive reasoning where it changes the decision; give cheaper workers bounded execution with a verifier. Do not hard-code a model name as proof of capability.

- Discover available models and tools in the actual host. Resolve aliases to the effective model/provider, and distinguish a picker entry from a successful usable request.
- Separate planner, artifact writer, and independent reviewer. Workers receive clear inputs, acceptance criteria, an artifact boundary, and stop conditions. Dependency failures block dependent work instead of being silently ignored.
- Estimate full request cost, including system context, tools, cache creation, retries, and output. Track accounts that share a quota or billing pool; multiple sessions do not imply independent budgets.
- Verify when a budget is enforced. A CLI can report an overrun after one oversized request. Treat a post-request limit as accounting, not a hard pre-request guarantee.
- Start with an offline handoff rehearsal, then the smallest authorized live experiment. Record actual usage and whether it is provider billed, list-price estimated, or unavailable.
- Escalate after a diagnosed capability gap, not every failed attempt. Repeated tool or environment errors need repair, not automatically a larger model.

Use [the example](examples/worked.md). This repository supplies a routing method, not a live scheduler or spend limiter.
