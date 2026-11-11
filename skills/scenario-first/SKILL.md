---
name: scenario-first
description: "Use when planning a feature, investigation, or review that needs observable scenarios, a named current revision, and the cheapest honest verifier."
---

# Scenario first

Before dividing work, make the desired result falsifiable. Read what the system does today at a named commit. Do not take the current path from memory. A meeting claim stays a claim until it matches that code.

1. If the task is already obvious, such as a typo or a one-line fix whose input and output are settled, keep the plan to a few sentences. Say that a fuller packet does not apply.
2. If background, current versus desired behavior, a full request and response, the change shape, or a user interface is still unclear, write the smallest direction packet before the plan or the code. Name who is affected, the constraints, the acceptance checks, and what must not change. When a contract is unclear, show one complete input, the processing, the expected output, one failure or edge path, the error contract, and side effects, including none. Label teaching data synthetic. A picture is not runtime proof. The packet is not an approval gate and it is not the final formatting pass.
3. For each situation, write the actor, the starting state, the action, the expected observable output, what a broken build shows, and the verifier. Name the source of the expectation. A specification, an accepted example, or a domain reviewer is stronger than an answer the candidate generated. Mark a disputed expectation as a decision. Never leave status blank: measured, with a command or link, or unmeasured.
4. Find the smallest existing path that can exercise the scenario. Tag the cheapest honest rung. Use fixtures before network calls. A lower rung does not establish a higher one. Paid rungs wait for an explicit owner ask.
5. Mark each research finding measured, inferred, or unverified. When more than one approach survives, write non-negotiables first and mark each pass, fail, or unverified with evidence. Eliminate failures before scoring preferences. One successful example is a capability probe, not a bake-off.
6. Draw dependencies by artifact: which task needs which contract, schema, or tested output. Parallelize independent tasks. Reserve one writer per shared artifact.
7. Skip a later stage only when it plainly does not apply, and say so. A speed or cost claim needs the same scenarios measured before and after, with accuracy from that run. A behavior claim needs a check a reader can open on the named revision. Report the outcome, the evidence, and what is still open. Draft any message another person would receive, then stop. Do not start a paid comparison unless the owner asked. If a comparison breaks its own rules, every arm it touched is invalid.

Deliver a short work map: scenario, expected result, owner, dependency, check, current evidence, and unresolved decision. Scale detail to risk.

Use [the worked example](examples/worked.md). [The stage log](references/stages.md) shows the same order, including stages that were skipped on purpose. A formatted log is not a substitute for step 2 when step 2 applies.
