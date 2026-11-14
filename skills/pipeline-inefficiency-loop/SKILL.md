---
name: pipeline-inefficiency-loop
description: "Use when asked to find waste, cost, latency, or quality gaps in an agent or LLM pipeline and improve it repeatedly. Pin findings to component and failure-mode IDs, run premise math, validate before building, test lean, fix one change at a time against a stamped baseline, then record why the gap was missed and update the detector so the next scan catches it. Bounded by stop rules, a budget, and human gates."
---

# Pipeline inefficiency loop

A one-off review finds a few gaps and leaves the next person to find the same kind again. This loop fixes one gap at a time, then changes what the scan looks for, so the next lap catches that class of gap without a person reading rows. It improves the pipeline and the detector. It never edits its own stop rules, budget, or gates.

This is a written procedure for a person or an agent. It is not a running service. Following it does not demonstrate repeated improvement; that needs a recorded lineage of laps with held-out confirmation.

## 0. Bound the loop before lap one

Write down, before any scan:

- **Budget:** a cap in money, quota, or hours for the whole loop and per lap.
- **Human gates:** a named owner approves every paid run and every merge. A finding, a plan, or a passing test is not that approval.
- **Premise threshold:** the smallest yearly harm avoided or saving that is worth a lap.
- **Stop rules:** stop when the budget is spent, when two laps in a row find nothing above the threshold, when a fix cannot be shown on a same-version baseline, or when the owner says stop.
- **Frozen parts:** the grader, the answer key, the case list, and these bounds. A lap that needs to change one of them stops and asks.

## 1. Scan: find and pin

Read free evidence first: traces per pipeline (cost, phase timing, tool calls, retries, timeouts), failed eval rows by measure, and what changed since the last lap.

Pin every finding to a component and failure-mode (FM) ID from a component SLA register (`component-sla-register`). Use its walk: blame each failed row on the first broken contract upstream, and count rows per FM ID, including rows a scoring rule drops. If no ID fits, add one to the register first. "The pipeline is slow" is not a finding. Use [the finding format](references/finding-format.md) and its self-review questions.

## 2. Premise math, then rank

For each finding, write the premise check (`criteria-before-choice`):

- volume per year in the pipeline's own units, with a source;
- the money or time change per year against a same-version baseline, at base and high volume;
- the risk direction: does the saving come from dropping a check or from a cheaper, less accurate step?
- the expected harm or gain in real units, such as wrong answers per year.

Label inputs observed, derived, or estimated. Rank by harm avoided first, then by money. Drop or downgrade findings where the saving is small next to the harm, or where the math does not add up.

## 3. Validate before building

Take the top finding only. Run `validate-proposal-before-build` on the proposed fix: decode what would change, research it, list options including "do nothing", predict per measure, and reach build, skip, or park. A skip or park still goes to step 6.

## 4. Lean test

Design the test with `lean-test-design`: research first, map non-model factors, smallest case set, free rungs before paid ones, caps, and a stop rule. The owner reads the plan before the first paid run. For a speed or cost claim, measure the path (`measure-the-path`).

## 5. Fix one at a time against a stamped baseline

Make one change per lap. Stamp the baseline and the candidate with the same version fields (commit, prompts, skills, tools, model ID, grader), apart from the change. Adopt only when:

- the target FM count moves in the predicted direction, beyond rerun noise;
- no graded measure gets worse on any pipeline that shares the component;
- confident-wrong answers do not rise;
- the owner approves the merge.

Otherwise revert it. When a change ships, mark older results stale and re-stamp the register.

## 6. Encode the lesson

Every lap ends here, whatever the verdict. Write a short lesson entry ([template](references/lesson-entry.md)):

- **Why was this not found sooner?** Pick the cause: no signal existed, the signal existed but nobody read it, a scoring rule hid the rows, the failure mode was not in the register, the component was too coarse, or the baseline was on another version.
- **What changes so the next scan catches it?** Update one or more of: a detector query or log signal, the register (new FM ID, keyword, finer component), the scan checklist in this lap's notes, or the relevant skill.
- **Replay the detector change** on stored traces from earlier laps before relying on it. It must flag this lap's rows and must not flood earlier clean rows.

A lesson that changes nothing the next scan reads is not encoded.

## 7. Next lap or stop

Check the stop rules. If none fires, start the next lap at step 1 with the updated detector. Report each lap in one block, using the lap summary in the lesson template.

See the [synthetic worked example](examples/worked.md).
