# All Code Is Slop (Except Mine)

- Talk: [All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI](https://www.youtube.com/watch?v=O_zcc6Xl12g)
- Speaker: Lauren Tan ([poteto](https://github.com/poteto); [x.com/poteto](https://x.com/poteto))
- Channel: [AI Engineer](https://www.youtube.com/channel/UCLKPca3kwwd-B59HNr-_lvA)
- Length: 17 minutes 31 seconds
- Published: 14 Nov 2026, 10:30 AM PT (America/Los_Angeles)
- Also listed by the speaker: [cursor/plugins pstack](https://github.com/cursor/plugins/tree/main/pstack)

This page is an original notes file. It is not a transcript, and it is not affiliated with the talk, the speaker, or the speaker's employer. Figures below are the speaker's reported claims from the talk. They were not independently verified here, and they are not results for this repository. Short quotations are from the English auto-generated captions and may contain errors.

## Summary

The talk's thesis is that the job of a software engineer, once agents can produce a high volume of changes, is to keep or improve code quality while that volume rises. The path is not "blind trust" and not a software factory first. It is an investment in the agent's environment so the agent is constrained to do the right thing by default.

The speaker describes that environment as an inverse pyramid. The bottom layers are deterministic and live in the code itself: API design, architecture, refactoring, lint rules, type systems, compilers, and tests. Those layers constrain what an agent can do. Runtime and formal verification sit above them, to find bugs, check invariants, and test whether the agent understood the intent. Prose — rules, skills, `AGENTS.md` — comes last, for judgment that cannot be encoded as a check.

A correction should become one of those deterministic checks, or a change in API or architecture that removes the class of mistake, rather than another line in a rule file. Comments and markdown are easy escape hatches: they go stale, they are not enforceable, and agents use them to justify a workaround. The talk's closing warning is that if the inner coding loop produces slop, automating that loop only produces more slop, at a higher token cost. Foundations come before a factory.

## Key takeaways and how they map here

| Takeaway from the talk | Closest skill in this collection | What maps, and what does not |
|---|---|---|
| Treat the codebase as a primary agent input. Workarounds, deprecated paths, and other "weeds" get copied because they look like the established pattern. | [Encode corrections](../../skills/encode-corrections/SKILL.md), [Context check](../../skills/context-check/SKILL.md) | Both skills insist that a durable, retrievable record — not a chat correction — is what the next session sees. They do not, by themselves, turn that record into a lint rule or an API change. |
| When you correct an agent, prefer a deterministic check (lint, types, compiler, test) or a categorical API or architecture change over another prose rule. | [Host-loop guards](../../skills/host-loop-guards/SKILL.md), [Encode corrections](../../skills/encode-corrections/SKILL.md) | Host-loop guards already prefer an enforceable host primitive over pasted checklist prose, and they warn that a check the agent can edit is worthless. Encode corrections records the decision. Neither skill is a procedure for writing the lint rule or removing the anti-pattern from the tree. That gap is noted below. |
| Ban or constrain APIs that need too much nuance to use well, and enforce boundaries in the directory and dependency graph (the talk's examples: a client framework with encoded lint rules, a ban on a frequently misused effect hook in product code, and a forbidden import between process directories). | [System design proposal](../../skills/system-design-proposal/SKILL.md), [Component SLA register](../../skills/component-sla-register/SKILL.md) | A proposal and a contract register make the intended boundary reviewable and name the failure mode it protects. They do not install the lint rule. |
| Comments and justification markdown are not enforceable, go stale, and can spread a workaround. Prefer a lint message that points at the root cause. | [Encode corrections](../../skills/encode-corrections/SKILL.md), [First principles](../../skills/first-principles/SKILL.md) | Encode corrections keeps a superseded line retrievable instead of deleting history, which is the right move for a decision log. First principles is for when a written procedure and the actual goal disagree. Neither is a "prefer lint over comments" rule for product code. |
| Shrink code review toward verification artifacts (recordings, screenshots, diagrams, model checks) on a named revision, not a visual read of every line. | [Proof before review](../../skills/proof-before-review/SKILL.md) | Proof before review already requires the surface the claim needs, named base, merge-base, and tip, and it refuses to treat a bot approval or green CI as done. The talk is an argument for making that surface richer (runtime and formal artifacts). It is not a license to skip declared project gates or human approval where those are required. |
| Give the agent a way to run the product and the same debugging tools a person would use. A "feature map" is a user-facing inventory of features so the agent does not have to guess at shared names. Reuse a small, testable driver or CLI rather than rediscovering the path in each prompt. | [Direction before work](../../skills/direction-before-work/SKILL.md), [Scenario first](../../skills/scenario-first/SKILL.md), [Lean tool context](../../skills/lean-tool-context/SKILL.md) | Direction and scenario skills want a complete input, output, and shared vocabulary before the work starts. Lean tool context prefers widening an existing tool over adding a new surface, which matches the talk's reusable CLI. This repository does not ship a feature-map format or a product driver. |
| Formal methods and property-based tests are another layer, not a silver bullet. The talk reports early use of TLA+ for cross-device flows, Lean for a custom algorithm, and a property-based UI library, and says bugs were found, with the work still experimental. | [Lean test design](../../skills/lean-test-design/SKILL.md), [Match methods](../../skills/match-methods/SKILL.md), [Validate a proposal before building](../../skills/validate-proposal-before-build/SKILL.md) | Those skills already say: characterize the method, run the cheapest discriminating check, and do not treat a promising tool as an automatic upgrade. They do not adopt TLA+, Lean, or any named UI library. |
| Spend a large share of tokens on verification, not only on generating more code. The talk cites a public follow-up, about six months after a post about subtle bugs slipping through, in which most of that author's daily tokens went to verification, and the speaker said that mix also matched their own use. | [Measure the path](../../skills/measure-the-path/SKILL.md), [Subscription usage](../../skills/subscription-usage/SKILL.md), [Budget-aware routing](../../skills/budget-aware-routing/SKILL.md) | Measure and report what a run spent and what that spend bought, and choose model and effort from a fresh read. A cited token mix from another team is not a default for this collection, and it is not permission to start a paid run. |
| Do not build the outer automation loop until the inner loop is constrained and the verification story is strong. Automating slop scales slop. | [Validate a proposal before building](../../skills/validate-proposal-before-build/SKILL.md), [Pipeline inefficiency loop](../../skills/pipeline-inefficiency-loop/SKILL.md), [Match methods](../../skills/match-methods/SKILL.md) | Validate-before-build and match-methods already reject jumping to a heavier pipeline before the outcome and the current path are named. Pipeline inefficiency loop is a bounded way to fix one gap and change the scan so it does not return. None of them is a factory runtime, and this repository does not auto-merge anything. |

## What the talk reports, and what this page does not claim

The speaker reported, as team results for the month discussed in the talk: on the order of three thousand pull requests shipped personally, about eleven thousand pull requests shipped by the team, a revert rate of about half a percent, a new stable client about once a day, 227 people with at least one pull request in October, and performance that stayed stable or improved on startup, typing, and chat switching. The speaker also said it took about six months to reach a point where thousands of pull requests, some unattended, were possible, and that later work became possible because the foundations were already in place, including an example in which a release kicks off a fuzz of the build and opens fix pull requests.

Those figures are the speaker's. This repository has not reproduced them. A notes page is not a capability claim, a performance claim, or a reason to turn on auto-merge.

## Short quotations

From the auto-generated captions, lightly punctuated:

> Not blind trust but investing in your agent's environment so you can trust that your agents are going to do the right thing.

> Whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules or your agents.md.

> The worst part about comments though is that they're not enforceable.

> If your inner coding loop produces slop, then automating that loop just produces more slop.

## What this page is not

- It is not a new skill. The contributing guide says to extend an existing workflow when the lesson fits, and to add a folder only when the outcome is distinct. Several skills already cover proof, measurement, enforceable host guards, and recording corrections. The remaining distinct method — turn each correction into a lint rule, type, test, or API change, keep prose last, and refuse to automate the outer loop until that inner loop is tight — is real, but it is not published here as a standalone folder in this change. A later writer can add that skill with a worked synthetic example and a decision-log row if it still looks distinct after a review.
- It does not copy the talk, the slides, or a caption dump.
- It does not import Dune, pstack, TLA+, Lean, Bombadil, or any other tool named in the talk.
- It does not grant permission to auto-merge, skip review, or spend.
