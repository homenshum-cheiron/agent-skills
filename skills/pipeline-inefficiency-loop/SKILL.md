---
name: pipeline-inefficiency-loop
description: "Use when asked to find waste, cost, latency, or quality gaps in an agent or LLM pipeline and improve it repeatedly. Pin findings to component and failure-mode IDs, run premise math, validate before building, test lean, fix one change at a time against a stamped baseline, then record why the gap was missed and update the detector so the next scan can catch it. Bounded by stop rules, a budget, a lap cap, and human gates."
---

# Pipeline inefficiency loop

A one-off review leaves the next person to find the same kind of gap again. This loop fixes one gap per lap, then changes what the scan looks for, so a later lap can catch that class of gap without a person reading rows. It improves the pipeline and the detector. It must not edit its own bounds.

This is a written procedure for a person or an agent. It is not a running service. Following it does not demonstrate repeated improvement; that needs a recorded lineage of laps with held-out confirmation.

## 0. Bound the loop before lap one

Write down, before any scan, and have the owner read:

- **Budget and lap cap:** a money or quota cap for the loop and per lap, and a maximum number of laps.
- **Premise threshold:** the smallest yearly harm avoided or saving worth a lap.
- **False-flag ceiling:** the most earlier clean rows a new detector may flag.
- **Human gates:** a named owner approves every paid run and every merge. A finding, a plan, or a passing test is not that approval.
- **Stop rules:** budget or lap cap reached; two laps in a row with nothing above the threshold; no same-version baseline exists for the top finding; the owner says stop.
- **Frozen for the whole loop:** grader, answer key, adopt case list, and these bounds. A lap that needs to change one stops and asks.

## 1. Scan: find and pin

Read free evidence first: traces per pipeline (cost, phase timing, tool calls, retries, timeouts), failed eval rows by measure, and what changed since the last lap.

Pin every finding to a component and failure-mode (FM) ID from a component SLA register (`component-sla-register`), using its first-broken-contract walk and its per-FM counts. "The pipeline is slow" is not a finding. Use [the finding format](references/finding-format.md).

The register and detector definitions are frozen from here to step 5. Changes from step 6 apply from the next lap. Adoption is counted under the baseline's definitions, so reclassifying rows cannot pass for a fix.

## 2. Premise math, then rank

Write the premise check from `criteria-before-choice` for each finding: volume per year with a source, money or time change per year against a same-version baseline, risk direction, and harm or gain in real units. Label inputs observed, derived, or estimated. Show the arithmetic. When an estimate decides whether a finding crosses the threshold, the owner checks that estimate.

Rank by harm avoided first, then money. Drop or downgrade a finding when the saving is small next to the harm, when the saving exists only in the risky direction, or when the math does not add up.

## 3. Validate before building

Take the top finding only. Run the desk steps of `validate-proposal-before-build` on the proposed fix: decode what would change, research it, list options including "do nothing", and predict per measure. Go on to step 4 only if it is worth testing. Otherwise record skip or park and go to step 6. Its build verdict comes after the test.

## 4. Lean test

Design the test with `lean-test-design`: research first, smallest case set, free rungs first, caps. The owner reads the plan before the first paid run. For a speed or cost claim, use `measure-the-path`.

## 5. Fix one at a time against a stamped baseline

Make one change per lap. Stamp the baseline and the candidate with the same version fields (commit, prompts, skills, tools, model ID, grader), apart from the change. Adopt only when:

- the target FM count moves in the predicted direction, beyond rerun noise;
- no graded measure gets worse on any pipeline that shares the component;
- confident-wrong answers do not rise;
- the owner approves the merge.

Otherwise revert it. When a change ships, mark older results stale and re-stamp the register.

## 6. Encode the lesson

Every lap ends here, whatever the verdict. Fill [the lesson entry](references/lesson-entry.md):

- **Why was this not found sooner?** Pick the cause with evidence: no signal, an unread signal, rows hidden by a scoring rule, a missing FM, a coarse component, or a baseline on another version.
- **What changes so a later scan can catch it?** A detector query or log signal, a register entry, a scan checklist line, or a skill, through normal review.
- **Replay the detector change** on stored traces from earlier laps. It must stay under the false-flag ceiling. Flagging this lap's rows is a sanity check only, because the detector was built from them. Fresh rows in later laps are the real test.

A lesson that changes nothing a later scan reads is not encoded.

## 7. Next lap or stop

Check the stop rules. If none fires, start the next lap at step 1 with the updated detector. Report each lap with the lap summary in the lesson template.

See the [synthetic worked example](examples/worked.md).
