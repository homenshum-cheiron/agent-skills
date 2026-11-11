# The decisions behind the setup

This is a curated first edition of reusable decisions, not a complete transcript or a claim that every system below is implemented. The methods are distilled into original public writing; examples are synthetic.

| Tempting shortcut | Decision | Why it matters | Where it lives |
|---|---|---|---|
| Start by naming services and agents | Start with an input, expected output, and observable failure | A plan can be evaluated before implementation | [Scenario first](../skills/scenario-first/SKILL.md) |
| Let the implementation define its own answer key | Freeze acceptance separately, then compare a baseline and candidate | Prevents a changed implementation from grading itself | [Proof before review](../skills/proof-before-review/SKILL.md) |
| Call a code read a full review | Run relevant tests and expose untested scope | Plausible code and green shortcuts do not prove behavior | [Proof before review](../skills/proof-before-review/SKILL.md) |
| Create another stack when work is already assigned | Verify the existing owner, branch, and dependencies first | Avoids two writers and duplicate integration | [One-writer handoff](../skills/one-writer-handoff/SKILL.md) |
| Use the strongest model for every task | Match bounded work to demonstrated capability and cost | Cheap workers are useful only with clear inputs and verification | [Budget-aware routing](../skills/budget-aware-routing/SKILL.md) |
| Treat a CLI budget flag as a hard cap | Verify when spending is checked, including the first request | Post-request accounting can exceed a nominal limit | [Budget-aware routing](../skills/budget-aware-routing/SKILL.md) |
| Choose a tool from a feature list | Write non-negotiables first, then test the decisive unknown | Avoids buying the best brochure | [Criteria before choice](../skills/criteria-before-choice/SKILL.md) |
| Sum every span and call it latency | Separate wall time, overlap, and unexplained gaps | Parallel work cannot be counted twice as user delay | [Measure the path](../skills/measure-the-path/SKILL.md) |
| Load everything into every agent | Give a bounded task and retrieve the missing context | More context can add cost and unrelated instructions | [Lean tool context](../skills/lean-tool-context/SKILL.md) |
| Repair every failure in the crawler | Separate data operations from agent behavior and evaluation | Owners, SLAs, and safe remedies differ | [Route failures](../skills/route-failures/SKILL.md) |
| Expose internal source-health controls in answers by accident | Define an explicit product-specific exposure policy, separate from incident detection | A missing ingest must not silently change answer semantics | [Route failures](../skills/route-failures/SKILL.md) |
| Rewrite a recap from whatever is live | Review a bounded snapshot, then publish against the expected prior version | Prevents stale review from overwriting new work | [Bounded publication](../skills/bounded-publication/SKILL.md) |
| Describe activity as completion | Report what changed, what proves it, and what is still open | Readers can make the next decision without reconstructing the session | [Outcome-first updates](../skills/outcome-first-updates/SKILL.md) |

## Keep the layers separate

- **Skills** guide decisions. They are not authorization or enforcement.
- **Host configuration** provides tools, account access, and discovery.
- **Execution infrastructure** owns real isolation, concurrency, quotas, and durable state.
- **Verification** evaluates an exact artifact and its stated scope.
- **Release decisions** remain explicit and separate from test results.

If a practice becomes friction without protecting a real invariant, simplify it. Do not replace a removed guard with an undocumented automatic action.
