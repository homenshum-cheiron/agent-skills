---
name: measure-the-path
description: "Explain latency and cost using actual spans, overlap-aware wall-clock accounting, comparable baselines, and visible measurement gaps."
---

# Measure the path

Do not turn architecture into a speed claim.

- Freeze a trivial case and a representative real task. Record input, revision, model/provider, environment, warm/cold state, and run identity.
- Capture actual start/end times and usage. Separate time to first output, time to usable completion, and cleanup that still blocks the user.
- Break the path into phases and label measured versus estimated data. Record input, cached, and output tokens and the pricing basis when available. Unknown cost is not zero. Keep included subscription allocation, confirmed overage or hybrid dollars, and list-price hypotheticals in separate sentences. A list-price figure is not an invoice.
- Reconcile the observation window with the union of spans. Sum of work includes overlap; it is not user latency. Nested parent and child spans also double-count work.
- Include an unexplained-gap row rather than assigning that time to a model or a network without evidence. Mark each phase sequential, parallel, or blocking. Compare the sum of phases with user-perceived time. Record accuracy on the same run as the time and cost. A gain that changes the answer is a regression.
- Tie each proposed fix to a row. Rerun the same trivial case and the same realistic case, and show the before and after tables, before claiming a speed or cost win. A live process with no table does not prove the win. Separate a one-run change from a stable effect across repeated runs.

Use [the example](examples/worked.md) and [interval format](references/intervals.md). The [offline calculator](scripts/summarize_intervals.py) computes coverage only; it does not infer the critical path or causal attribution.
