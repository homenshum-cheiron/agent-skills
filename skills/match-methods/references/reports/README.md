# Report formats

Choose one shape. Omit empty sections. These are original templates. They follow the four outcome types in Notion's public format-selection guide (quick brief, research summary, comparison, comprehensive report) without copying that guide's template bodies. Notion import of these Markdown files was not tested. Mermaid renders on GitHub. Notion may show the diagram source as code and may not draw a native chart. The table is the fallback. Do not promise a Notion chart.

The machine record is a JSON sidecar using the same figure ids as the prose. The field list is [report.schema.json](report.schema.json). [check_report.py](../../scripts/check_report.py) rejects a prose claim that disagrees with the figure, a hypothesis labeled measured, a numeric chart on a hypothesis-only report, a chart series that disagrees with its table, and a verdict treated as permission. A passing check is not permission to act.

| Need | Template | Notion-shaped type |
|---|---|---|
| A decision and the next authorized step | [Decision brief](decision-brief.md) | Quick brief |
| Methods against one another, including no change | [Method comparison](method-comparison.md) | Comparison |
| A trace, an experiment, or a negative result | [Investigation](investigation.md) | Research summary. Use the comprehensive depth only when the audience asked for it |

Audience, when it changes the page, is one of company, product, app QA, or pipeline. Do not force all four.

Pick a visual only when the evidence supports it. Carry the table, units, denominator, sample size or an explicit missing sample, the evidence class, and a caption. Never invent a series to fill a chart. Architecture and dependency diagrams can be Mermaid. Latency can be a waterfall or a critical-path versus summed-work table. Token or cost stacks only when the components reconcile with the unique ledger. A quality-cost-latency plot needs uncertainty, or it stays a table.

A [hypothetical brief](../../examples/hypothetical-brief.md) uses toy numbers that match [report-hypothetical.json](../../examples/report-hypothetical.json). A [hypothesis-only note](../../examples/hypothesis-only.md) has no chart.
