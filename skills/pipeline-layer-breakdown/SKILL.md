---
name: pipeline-layer-breakdown
description: "Use when breaking an agent pipeline into layers, a layer table, a node map, or a stage-by-stage explanation that a reader with no context can follow, including how to build an isolated test and an answer key for each layer."
---

# Pipeline layer breakdown

Goal: a layer table a newcomer can follow. Each row tells a concrete story: what the agent does, which tools it calls and what it reads, how it decides to keep going, how to test that layer alone, and whether it is good enough for a real user.

## 1. Pin the source

Check out the exact commit and record the full revision at the top. Every code claim gets a `file:line` reference at that revision. Name the primary spec and say which older specs are outdated. When layers are renumbered, write a crosswalk from old to new ids instead of rewriting history.

## 2. Use framework vocabulary

Use the terms of the agent framework you run (agent, tool, guardrail, handoff, state, checklist, map-reduce fan-out, conditional edge, self-judge, human-in-the-loop interrupt, evals). Do not coin labels. Link each framework concept to its documentation the first time, and check the link resolves.

## 3. Table columns

Depends on | Layer | What it does | How to build the test case and key | Parallel pattern | Runs as | Original stage | Status and source notes

## 4. "What it does" cell, in order

1. **Tool contract:** `tool_name(inputs) -> outputs`, then one sentence on behavior.
2. **Checklist and self-judge:** which earlier checklist the agent uses to track progress and decide whether to continue.
3. **Real data for one named example case:** real connector, store and document types from the code. Never answer-key values.
4. **Contexts:** list each input as context 1, 2, and so on, and say whether it is fixed (the same for every user) or extracted per user.
5. **Fan-out:** when the agent sends one worker per document, chunk or item, then reduces.
6. **Stop rule and heal:** when it stops (checklist met, item held, or budget spent), which conditional edge retries which layer, the cap, then the human interrupt.
7. **Verdict:** "Insufficient for real use because ..." or "Sufficient because ...", with `file:line`.

## 5. "How to build the test case and key" cell

- **Isolated case:** which upstream state to freeze so this layer runs alone, plus variants (a perturbed input, an item added or removed, a missing document).
- **Answer key:** which fields it holds and who writes it. Keys stay offline and are never shown to the agent.
- **Metric and pass rule:** exact match per field, recall and precision against keyed ids, citation-in-pool rate, judge-scored support, repeat-run consistency, schema validity. Invalid output never counts as a win. Record time and cost per case on the same run.
- **Status today:** where the eval runs now, with `file:line`, or "proposed".
- **Input data:** where real inputs come from, how to freeze upstream state from a past trace, how to synthesize missing data (labeled synthetic), who supplies what, and where it is stored offline.

## 6. Status and delivery

Label every claim as code fact (with `file:line`), proposed, open, agreed or suspicion. A feature behind a flag that is off is not a malfunction. Say plainly what runs today and what is the target. Add a flow diagram of the layers with proposed edges dashed, and keep the table and diagram in one revision. Write "not recorded" when data is missing; never invent numbers or line references.

See the [worked example](examples/worked.md).
