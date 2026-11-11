# Trace record contract

Record the fields that can separate the live hypotheses. Unknown is not zero. Do not collect hidden chain-of-thought. Default export is minimal: ids, counts, timing, hashes, and status. Bodies are sampled only when the export policy is `authorized_sample` and a reason is recorded. Evidence references stay access-controlled. Record sampling rate, export completeness, and overhead so telemetry does not become the new bottleneck.

Availability of a field is one of: recorded on the inspected artifact, documented by the producer but not on this artifact, or only proposed. Do not promote a proposed field to recorded.

Each figure is measured, derived, judged, estimated, or missing.

## Identity and versions

Trace, task, parent, span, generation, tool, and attempt ids, plus dependency edges. Role is a temporary label. Model, effort, provider, host class, and version. Route or escalation reason. No fixed role map.

## Time

Request, enqueue, dequeue, execution, model start, first token, first supported useful output, final, and persist. Name the clock domain. Prefer monotonic durations. If first token was not observed, first-token latency is missing, not zero, and not proof of a slow model.

## Tools and tokens

Every tool span: on-path work, download, parse, result assembly, slot or rate-limit wait, and errors. Prompt-component tokens actually sent, not the installed catalog. Input, cache write, cache read, output, and reasoning tokens, with the provider's accounting meaning. A unique-generation ledger includes child cost once. A child already inside a parent must not be counted again. Overlapping spans are not wall time.

## Cache and provenance

When observable, record protected-prefix identity, cache TTL, scope, and hit or miss reason. Do not record secrets or an unsafe cross-tenant cache key. For a source: whether a URL was visible, upstream authority, document version or hash, size, truncation, and the chain source, parser, worker-visible context, claim, persist.

## Actions and outcome

Semantic purpose labels. Necessity judgments cite evidence or a rubric and allow a valid alternate path. Checks, judge verdict, failure, revision, escalation, and stop. The supported outcome is separate. A verdict is not permission.

## Optional tier

Compaction, handoff, and rework. Workload tags. Build, prompt, and tool pins. Omit the tier when it answers nothing.

The [checker](../scripts/check_trace_record.py) rejects a few dishonest shapes in a local JSON record. It does not certify a trace, a product, or an autonomous loop. The field list is [trace-record.schema.json](trace-record.schema.json). The toy record is [trace-hypothetical.json](../examples/trace-hypothetical.json).
