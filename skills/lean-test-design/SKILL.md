---
name: lean-test-design
description: "Use before spending money or quota on an eval that compares builds, prompts, models, fixes, or configs on test cases. Research first, map the non-model factors, build a coverage matrix, pick the smallest case set, climb a free-first ladder with cost caps and a stop rule, have the owner read the plan before the first paid run, and stamp every result with the pipeline version."
---

# Lean test design

The usual eval plan is "run every arm on every case, paired, a few times". It is expensive, and at typical case counts often too small to detect the gap that matters. Much of the answer is free: in documentation, field reports, stored traces, or a dry run that shows the feature never fired. Write the smallest plan that can settle the question, and spend only after cheaper rungs failed.

The plan is a record, not an approval. A plan, a matrix, or a CLI budget flag does not authorize a paid run.

## 0. Name the question and its decision value

Write one sentence: which arms, which measure, and what result would change which decision. Example: "a gap of at least X points on measure M decides between A and B, and that choice is worth about $Y a year." If no result would change a decision, do not test.

Stamp the plan with the pipeline version it applies to (see step 7).

## 1. Research before any spend

Time-box the desk research and fill [the research checklist](references/research-checklist.md) per arm. Read official docs, model and system cards, migration and prompting guides, and API limits. Then read field reports (Hacker News, Reddit, GitHub issues for the SDKs and CLIs in use), papers on the same mechanism (including negative results), and your own earlier runs. Label each claim official, paper, issue, or anecdote, with the count of independent reports. Stop here if the research settles the question.

## 2. Map the non-model factors

A score depends on more than the model: prompt phrasing, tool-call format and tool descriptions, skill text and loading, effort, caching, compaction, stop rules, retries, safety classifiers, provider, and region. For each factor, write "held equal" or "varied on purpose". A factor that differs by accident invalidates the comparison.

## 3. Coverage matrix and the smallest case set

Rows are candidate cases. Columns are the behaviors the arms could change, plus cost and time per case. Fill the cells from case metadata and past runs, never from the answer key. Then choose cases greedily: take the case that covers the most uncovered behaviors and repeat. Name every behavior that no case covers as a gap instead of padding the set. Rank the remaining cases into tiers for later expansion. [The plan template](references/plan-template.md) has the layout.

## 4. Cases per arm

There are no default paired full runs. Each arm runs only the cases whose behaviors it can change, plus one shared anchor case. The reference arm runs the full minimal set. Arms compared head to head run the same cases on the same build, back to back.

## 5. Free-first ladder

Climb only as far as needed. Stop at the first rung that settles the question.

1. Static audit of prompts, tool descriptions, skills, and request builders against the research ($0).
2. Dry run: print each arm's resolved config with no model calls ($0). Check that the feature under test is actually switched on.
3. Replay or stub: replay stored traces with model calls stubbed, and force rare paths in eval-only config so the feature actually fires ($0).
4. One representative paid case on the arms that matter most.
5. The minimal set at one run per case.
6. Repeats and the next tier, only on arms that differ from the reference, plus the reference on the same cases. Use the repeats to measure rerun noise.

A full eval comes last. It needs the decision value from step 0, a size that has the power to detect that gap given measured noise, and the owner's approval.

## 6. Caps, owner read, and stop rule

Set a cap per arm and a total cap. Report the plan's cost next to the naive cost (all arms × all cases × all repeats). The owner reads the written plan before the first paid run. Reading is not approval: each paid rung still needs whatever spend approval the destination project requires. Stop and report when:

- a cap is hit;
- tracing, grading, or the feature switch looks wrong;
- the one-case rung shows no arm differs from the reference;
- the remaining budget cannot reach the repeats the leading arms need.

A one-run difference is noise until it repeats. A one-run match is also noise: an arm that shows no difference at the one-case rung is parked, not ruled out.

## 7. Stamp, stale, same-version baseline

Stamp every result with the pipeline version: commit, prompts, skills, tool set, model ID, and grader version. When any of these changes, mark earlier results stale; they are references, not baselines. Compare only with a same-version baseline, apart from the one factor under test. Grade every arm with the same frozen grader.

## Related skills

By name: `validate-proposal-before-build` (is it worth testing?), `match-methods` (model-swap ladder), `criteria-before-choice` (premise check), `measure-the-path` (speed and cost claims), `component-sla-register` (failure modes an arm should move).

See the [synthetic worked example](examples/worked.md).
