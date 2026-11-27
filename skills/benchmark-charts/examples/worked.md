# Worked example (synthetic)

A team compares two builds of a ticket-fixing agent on four frozen tickets, then wants a Page rather than a table.

Weak report: "The new agent scores 92% and is cheaper and faster."

That hides three things. "92%" is 24 tests passed of 26, summed across tickets: it is not a case-level score, and it treats the two remaining misses as a rounding error. The baseline passed 18 of those 26 tests but only 1 of 4 tickets. Cost and time are real gains ($17.50 to $4.17, 44.0 min to 14.6 min) and should be shown as sums, not as a reason to skip the misses.

Contract build (all figures invented):

```bash
python3 scripts/make_chart_data.py build --input examples/raw_results.json --output examples/chart_data.json
```

Headline the Page may use, each traced to `examples/raw_results.json`:

- 76.2% cheaper (sum of case costs: $17.50 to $4.17)
- 66.8% less wall time (sum of case wall times: 44.0 min to 14.6 min)
- 2 vs 1 cases passed of 4 (the quality headline)
- Compact-context cost $3.00–$3.95 ESTIMATE; its score and wall time are not measured

Per-case nested results stay in the drilldown. SEARCH-02 flips from fail to pass. MIGRATE-03 still misses `perms`. REPORT-04 still misses `schedule`. A compact-context arm is shown as a hatched cost bar and as `not measured` on quality and time.

The Page also shows a score-versus-cost scatter, paired latency bars, a cost waterfall, a token-flow Sankey, a test-by-arm heatmap, dumbbell and slope charts, and a four-step reveal. Styles and sources are in [the catalogue](../references/STYLES.md).
