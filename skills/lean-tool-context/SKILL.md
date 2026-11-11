---
name: lean-tool-context
description: "Use when designing or simplifying agent tools and context. Widen an existing tool before adding one, and test the current capability before adding a wrapper, store, or large prompt."
---

# Lean tool context

Start with the smallest tool and context surface that can complete the user's scenario.

1. Inventory existing tools, identifiers, retrieval, file access, and durable stores. For each new capability, ask whether an optional parameter or a richer return on an existing tool covers it. A new tool, store, or pipeline needs a written reason why widening failed. Borrow one idea from an external system rather than importing its framework. A change on someone else's stack stays a proposal until that owner agrees. Test the missing capability before assuming another wrapper is needed. When the prompt itself is the growing surface, keep at most 16 one-line working rows and retrieve the rest by handle.
2. Separate discovery from payload. Return a small index first, then fetch exact documents or sections by stable identity. Preserve source version and location when truncating.
3. Avoid sending the whole conversation to every worker. Supply the task, accepted decisions, rejected alternatives, necessary artifacts, ownership, and verification. Retrieve details on demand.
4. Keep model context separate from operational diagnostics. A health-control field should not accidentally become answer evidence or a prompt instruction.
5. Test relevant failures: large attachments, duplicate names, stale IDs, partial results, pagination, retries, and interrupted writes. A happy-path example does not establish a complete loader.
6. Compare the simpler baseline on the same scenario. Measure outcome, latency, tokens, and operational burden before keeping a new layer.

Use [the example](examples/worked.md). A skill can describe a capability that still needs implementation; label that gap instead of claiming the tool exists.
