---
name: measure-the-path
description: "Explain latency and cost using actual spans, overlap-aware wall-clock accounting, comparable baselines, and visible measurement gaps."
---

# Measure the path

Do not turn architecture into a speed claim.

- Freeze a trivial case and a representative real task. Record input, revision, model/provider, environment, warm/cold state, and run identity.
- Capture actual start/end times and usage. Separate time to first output, time to usable completion, and cleanup that still blocks the user.
- Break the path into phases and label measured versus estimated data. Record input, cached, output tokens and pricing basis when available. Unknown cost is not zero; list-price estimates are not invoices.
- Reconcile the observation window with the union of spans. Sum of work includes overlap; it is not user latency. Nested parent and child spans also double-count work.
- Include unexplained gaps rather than assigning them to a model or network without evidence.
- Tie optimizations to specific phases and rerun identical cases under comparable conditions. Separate a one-run improvement from a stable effect across repeated runs.

Use [the example](examples/worked.md) and [interval format](references/intervals.md). The [offline calculator](scripts/summarize_intervals.py) computes coverage only; it does not infer the critical path or causal attribution.
