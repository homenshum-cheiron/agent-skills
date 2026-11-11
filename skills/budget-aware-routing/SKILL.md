---
name: budget-aware-routing
description: "Use when choosing a model and reasoning effort for a task, or when a budget flag, a default lane, or a stronger-model ladder is about to be treated as policy."
---

# Budget-aware routing

Choose the model and the effort together for this task. A model name written in a skill is not proof that an account can run it today.

- This turn, read supported models and efforts from the host or account's sanctioned capability or usage surface. If you cannot, say that freshness is unknown. Treat the examples below as illustrations, not a catalog.
- Read shared capacity: session, all-model, and model-specific caps that draw on one account. Leave a context reserve and a usage reserve for a verify pass and a handoff note.
- Note the task, the risk, the acceptance criteria, any inherited knobs (record them; do not silently drop them), and any explicit user choice.
- Pick a model and an effort that the fresh read lists and that the remaining capacity can cover. Report the host, a generic account class, the model, the effort, and which source you read.
- There is no fixed planner lane, worker lane, boss lane, or cheap lane. A temporary split can still help: one outcome owner, clear inputs, acceptance criteria, an artifact boundary, and stop conditions. Borrowed planner or worker seats do not inherit auto-delegation or a permanent hierarchy. A smaller listed model is a fit when the inputs and the verifier are already clear. It is not the default because it is cheaper. A dated private config may hold account-specific pins. This public skill does not, and it does not publish a banned-model list.
- Do not auto-escalate from "this is harder" to the strongest model plus a fresh judge. Prefer an empirical check. A second reviewer is a separate decision.
- **Fable at medium effort** is one illustrative eligible profile. Choose it only when the current host and account list both Fable and medium effort and that pair fits the task, the risk, and the remaining capacity. It is not a universal default and not a role pin. If the host does not list it, pick another supported profile and say so.
- Estimate the full request cost, including system context, tools, cache creation, retries, and output. Several sessions do not imply several budgets.
- Verify when a budget is enforced. A tool can report an overrun after one oversized request. A post-request limit is accounting, not a hard pre-request guarantee.
- Spend personal budget only when the owner asked. A plan or a matrix is not permission. Do not start a paid comparison unless the owner asked. List-price arithmetic is not remaining capacity and not an invoice.
- When you report cost, keep three classes separate: included subscription allocation, overage or hybrid dollars confirmed by a supported billing or usage source, and list-price hypotheticals. A billed API path does not always mean the user supplied an API key. Check the configured path, or say you could not.
- Escalate after a diagnosed capability gap, not after every failed attempt. Repeated tool or environment errors need repair, not automatically a larger model. A dependency failure blocks dependent work.

Use [the example](examples/worked.md). This repository supplies a routing method, not a live scheduler, a model lock, or a spend limiter.
