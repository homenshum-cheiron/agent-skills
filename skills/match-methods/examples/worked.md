# Hypothetical examples

These scenes are structural teaching fiction. They are not traces, scores, savings, or permission to implement.

## The right document, the wrong section

A frozen case finds the official document and misses the deciding sentence in the next section. A generic search ran before the official-source search. First-token timing was never recorded. No cross-document relation is demonstrated.

- Outcome: a supported answer that includes the deciding sentence. Guards: an invalid quote still fails, and the source span is kept.
- Evidence in hand: the document id and the missed sentence's location. Missing: first-token latency. That gap stays missing.
- Candidates: no change; expose a source URL if the tool result lacks one; route to the official source when the task requires it; a capped query-time read of the neighbor section. Index-time contextual retrieval is a different candidate and is not a substitute for that neighbor read. A graph has no demonstrated relation to explain.
- Falsifier: if the deciding sentence is already in the worker context, the neighbor read is not the first repair.
- Check, only if already authorized: inspect the exported result shape offline. A replay does not prove a live model would quote the sentence. A falling retry counter would be a fire signal, not the outcome.

## Quotation checks reject a document already in hand

The official document is present. Support checks reject the draft. The same document is reread. No supported assessment is produced.

- Primary outcome: a supported assessment, with an invalid quote still failing.
- Competing causes: paraphrase; the parser dropped the span; the quote is exact but false; the gate is mislocated; the deciding text was never sent because it sits in a neighbor section.
- Falsifier: if the original span is in the parser output and in the worker context, parser loss is rejected. If it exists only in the neighbor section, a query-time walk is in scope and disabling the quote check is not.
- Smallest correction, if diagnosis supports a location problem and implementation is already authorized: keep the lead nonbinding, return the original text by a stable span, and keep the support check.

## Several workers, and the user still waits

Helpers run together. The user still waits for a supported result.

- Primary outcome: wall-clock time to that supported result. Guards: evidence and a correctness floor.
- Diagnostics, each marked measured or missing: the delaying branch, the sum of child work (not a substitute for the wait), queue age, and pool or rate-limit wait.
- Falsifier: if the wait matches one necessary dependency and the shared pools are idle, adding workers is the wrong repair. If adding workers raises queue age and the critical path does not shrink, "not enough parallelism" is rejected.
- More workers starting is a fire signal. It is not the outcome.
