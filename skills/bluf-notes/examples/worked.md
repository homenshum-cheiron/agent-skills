# Worked example (synthetic)

Raw note: "lunch w/ vendor eng — cached agent + bash = weird edge cases, keep sep. also 99% cache reuse goal??"

Weak card: "Caching: keep bash separate (vendor). 99% reuse."

BLUF card:

- **Owner:** Priya, who is designing the agent rollout.
- **Situation:** Our coordinator agent keeps a long, cached prompt so later calls are cheaper. The rollout plan also lets it run shell commands.
- **Scenario:** Example: the coordinator writes scratch files while answering, and its job widens until odd failures appear mid-run.
- **Bottom line:** Put shell and file work in a separate sandboxed helper from the start.
- **Why it matters:** Impact unknown in dollars until cost per task is measured; the vendor's target was about 99% cache reuse.
- **Evidence:** Vendor engineer at lunch, as paraphrased in our notes.
- **Next step:** Priya writes the helper into the rollout design this week.
- **Confidence:** Inference. The advice is a paraphrase, and the design is a proposal.
