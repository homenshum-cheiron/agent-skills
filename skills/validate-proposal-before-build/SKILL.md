---
name: validate-proposal-before-build
description: "Use when a paper, card, design doc, transcript, or teammate proposal would change how an agent or system runs, and before building or evaluating it. Decode intent, research the claim, map it to what already exists, design the leanest test, and record a build, skip, or park verdict with why."
---
# Validate a proposal before building it

Spend no build or eval time on a change until you know what it intends, how it would run, what is already known, and which test would settle it. Do not dismiss a new idea without looking for the case where it really wins. End with a learning entry so the next scan is sharper.

Related skills in this repository, by name only: `criteria-before-choice` for tool or model selection, `match-methods` when a failure is about to be met with a new model or a heavier pipeline, `system-design-proposal` when the verdict is to write the full design, and `component-sla-register` for the failure-mode IDs a proposal must name.

## 0. Intake

Save the source link or path, the date, and the author. Stamp the system version the change would apply to (commit, prompts, skills, tools, model id). For transcripts, quote the sentences that state the proposal and mark inferences as inferences.

## 1. Decode intent and execution

Write, in plain words:

1. **Claimed outcome:** what gets better, for whom, and how it would be measured.
2. **Mechanism:** why the author believes it works.
3. **Execution path:** exactly what would change, what it would call, and when.
4. **Unstated assumptions:** volume, latency, model behavior, data, who maintains it.
5. **Open questions** the text does not answer. Do not invent the answers.

## 2. Map to what already exists

For each touched piece: does a host, skill, hook, test, or workflow already cover it? What is the current baseline and its noise? If a touched piece has no check, say so; it cannot advance past a desk review until it has one.

Name the failure-mode IDs the proposal moves, from a component SLA register (`component-sla-register`). For each: the current count or rate with its version stamp, the predicted change, and the signal that will show it. A proposal that cannot name an FM ID either targets an untracked failure (add it and its detection signal to the register first) or is not yet specific enough to test. If it moves a contract another team owns, name that owner.

## 3. Research the space (time-boxed, free first)

Cover each, and cite sources:

- Papers on the same mechanism, including negative or ablation results.
- Official guidance: vendor docs, API limits, migration notes.
- Write-ups from teams that shipped something similar.
- Public forums and issue trackers: quirks, failure modes, edge cases.
- Your own history: earlier trials, closed changes, traces. Was this tried before?

Record the gray box: non-obvious factors (prompt wording, tool descriptions, effort, caching, region, safety classifiers, fallbacks) that could make a result differ from the claim.

## 4. Options

List two to four ways to act, including the smallest version and "do nothing, or use a cheaper existing lever." For each: what changes, cost, risk, reversibility.

## 5. Predict, then design the leanest test

Per measure, predict direction and size for each option before testing. Climb only as far as needed: free gates, then a log or trace audit, then token counts, then single-step replays, then targeted cases plus controls, then an ablation of the one factor in doubt, then a power-sized eval whose decision value is written down. Name the cases where the proposal should win if it is right. If none exist, that is a finding.

Paid per-token runs need an explicit owner approval. A plan is not permission to spend.

## 6. Verdict

One of:

- **Build:** a test shows a win on named cases with no regression on shared measures. Write it up with `system-design-proposal` when the change is large.
- **Skip:** no case where it beats the current setup or a cheaper lever. State the evidence and what would change the verdict.
- **Park:** promising but blocked (data, access, a missing check). Name the trigger to revisit.

Then answer: if it wins, why didn't existing scans catch this sooner? If it doesn't, why did it look promising, and which assumption failed? Question the verdict once more: what context could still be missing, and what is the cheapest way to check it?

## 7. Feed the next scan

Add a dated row to a research register: source, verdict, evidence link, revisit trigger. Add any new detection signal so the next similar gap is found without waiting for a new proposal.

## Output

A short report: source and stamp, intent and execution (with open questions), the map to what exists, research with citations, options, predictions, the test and its cost, the verdict, the why, the register row. Before sending, ask: which model exactly? cheaper than what? measured how? who acts next?
