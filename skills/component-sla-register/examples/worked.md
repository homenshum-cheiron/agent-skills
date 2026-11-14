# Worked example (synthetic): a regulation lookup pipeline

Everything here is invented for illustration: the pipeline, the sources, the counts, and the owners. No number below is a measurement.

## Setting

A question-answering pipeline, `lookup`, answers "what does agency X require for Y?" for a list of countries. An evaluation run on 40 cases has 12 failed rows. The first draft of the report says "the model hallucinated on 12 rows; try a stronger model."

## Register excerpt

Stamp: illustrative date · component list at commit `aaaa111` · system version `bbbb222`, prompt v3, model M, grader v2.

| ID | Responsibility | In → Out contract | SLA metric | Owner | Blast radius | Used by |
|---|---|---|---|---|---|---|
| `shared.tool.web_fetch` | Read one official page | URL → text, or a typed error (blocked, unreachable, timeout, not found) | Typed-error share of failures: target TBD, set by one week of fetch logs | Platform team (from the service catalog) | answer, grader | `lookup`, `monitor` |
| `lookup.data.corpus` | Hold admitted documents per country | Source list → documents with dates | Missing-day count per country: target 0 (from the runbook) | Data team | retrieval, answer | `lookup` |
| `lookup.prompt.answer` | Write the answer from evidence | Evidence + question → answer that states any known gap | Gap-stated rate on rows with a known gap: target TBD | TBD | user | `lookup` |

| FM ID | Symptom | Signals | Grader measure | Status |
|---|---|---|---|---|
| `FM-shared.tool.web_fetch-01` | Answer is blank or generic; the fetch span shows an empty body, not an error | `status=200 len=0`, "no documents" | none | untracked |
| `FM-lookup.data.corpus-01` | Answer cites an older version of the rule | newest document date older than the agency's change log | citation freshness | tracked, not posted |
| `FM-lookup.prompt.answer-01` | Evidence is missing and the answer does not say so | answer has no "could not confirm" line while retrieval is empty | gap stated | tracked and posted |

## Attribution walk (3 of the 12 rows shown)

| Case | Measure failed | Walk (stop at the first "no") | FM ID | Evidence | Label |
|---|---|---|---|---|---|
| c07 | accuracy | Finished: yes. Valid output: yes. Right source tried: yes. Live read returned text or a typed error: **no**, empty body with status 200. Answer stated the gap: no. | `FM-shared.tool.web_fetch-01` (upstream), `FM-lookup.prompt.answer-01` (second) | trace span id, fetch log line | observed |
| c15 | accuracy | Right source tried: yes. Live read: typed `blocked`. In corpus: **no**, the source was registered but has collected nothing for nine days. | `FM-lookup.data.corpus-01` | corpus listing | observed |
| c22 | accuracy | Evidence present and correct; the answer misread a date. | none fits: add `FM-lookup.prompt.answer-02` before writing the finding | trace | inferred |

## Counts for this run

12 failed rows: 6 under `FM-shared.tool.web_fetch-01`, 3 under `FM-lookup.data.corpus-01`, 2 under `FM-lookup.prompt.answer-02` (new), 1 unattributed because the trace was missing. Five of the six fetch rows also count under `FM-lookup.prompt.answer-01` as a second fault.

The scoring rule removes "failed only because the source is unreachable" rows from accuracy. Four of the six fetch rows were removed that way. They still appear in the FM count above.

## What changed in the report

- "The model hallucinated on 12 rows" became "at most 2 of 12 rows point at the answer prompt; 9 point at upstream data contracts."
- The model-swap proposal was parked. A proposal for a typed fetch error now names `FM-shared.tool.web_fetch-01`, its current count (6 of 40, version `bbbb222`), the predicted change (the blank answers become stated gaps), and the signal (typed-error share in fetch logs). Because the fetch tool is shared, the test plan covers both `lookup` and `monitor`.
- The top-ranked gap is `FM-shared.tool.web_fetch-01`: no grader measure catches it today.
