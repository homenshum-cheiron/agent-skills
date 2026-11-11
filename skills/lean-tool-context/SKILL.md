---
name: lean-tool-context
description: "Design or simplify agent tools and context loading by testing existing capabilities before adding wrappers, stores, or large prompts."
---

# Lean tool context

Start with the smallest tool and context surface that can complete the user's scenario.

1. Inventory existing tools, identifiers, retrieval, file access, and durable stores. Test the missing capability before assuming another wrapper is needed.
2. Separate discovery from payload. Return a small index first, then fetch exact documents or sections by stable identity. Preserve source version and location when truncating.
3. Avoid sending the whole conversation to every worker. Supply the task, accepted decisions, rejected alternatives, necessary artifacts, ownership, and verification. Retrieve details on demand.
4. Keep model context separate from operational diagnostics. A health-control field should not accidentally become answer evidence or a prompt instruction.
5. Test relevant failures: large attachments, duplicate names, stale IDs, partial results, pagination, retries, and interrupted writes. A happy-path example does not establish a complete loader.
6. Compare the simpler baseline on the same scenario. Measure outcome, latency, tokens, and operational burden before keeping a new layer.

Use [the example](examples/worked.md). A skill can describe a capability that still needs implementation; label that gap instead of claiming the tool exists.
