---
name: benchmark-charts
description: "Use when presenting an eval, benchmark or A/B comparison as a shareable Page: build contract JSON, then Cognition-style charts (headline strip, small multiples, score-versus-cost, latency bars, stage breakdown, per-case drilldown) with estimates hatched and missing values shown as not measured."
---

# Benchmark charts

Turn per-case results into a presentation-grade Page instead of rebuilding charts by hand. The default look follows [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1). Other forms live in [the styles catalogue](references/STYLES.md).

Pair this with the eval-scorecard skill when you still need four verdicts, percentiles and dollars per task in a table. This skill is the Page.

## Steps

1. **Pin the comparison.** Name the arms, the case list, the grader or judge and its version, and what cost covers. One arm is `baseline`, one is `highlight`.
2. **Write raw results, then build the contract.** Put per-case nested results first (tests, markets or other subunits). Run:

```bash
python3 scripts/make_chart_data.py build --input examples/raw_results.json --output examples/chart_data.json
```

The script exits 2 on an untraceable number, an estimate with no `ESTIMATE` label, a missing value that is not `not_measured`, a pooled score used as the headline, or sums that do not match the cases. Fix the data; do not hand-edit the totals.
3. **Pick styles.** Start with the core set in [the canvas template](references/canvas-template.tsx): headline strip, small-multiple bars, score-versus-cost (log cost, labelled points, one takeaway), paired latency bars, stage breakdown with a view toggle, and per-case drilldown. Add forms from [the styles catalogue](references/STYLES.md) only when the picker says they fit. The template also ships dumbbell, slope, waterfall, heatmap, Sankey and a step-reveal.
4. **Write a Page.** `Read` the canvas skill, then `WriteCanvas` a `wide` Page. Paste components from the template. Embed the contract JSON in the module. Import only from `grok/canvas`. Custom SVGs may be components; kit blocks (`Metrics`, `Segmented`, `Table`, `Heatmap`) stay directly in the `Page` or `Section`.
5. **Check the Page.** Run `scripts/check_premium.py` on the source; it must exit 0. The Page must render. Every visible number must trace to the contract and from there to a source file. Estimates are hatched or dashed and labelled `ESTIMATE`. Missing values say `not measured`. Case results, not a pooled subunit rate, are the quality headline. Cite sources. Copy no proprietary assets.

## Premium interactive standard

Every chart and node graph must meet [the premium interactive standard](references/PREMIUM-INTERACTIVE.md), checklist P0–P14. In short:

- Paste the shared primitives from `references/premium-primitives.tsx` unchanged.
- Wrap each chart in `ChartFrame`, and spread `mark(c, tip)` on every data mark.
- Tooltips show exact values and the source. Lines and scatters snap to the nearest point.
- Click pins the tooltip and Escape unpins it. Legend chips toggle the series.
- Enter animations turn off under reduced motion.
- Charts work with the keyboard and announce values through aria-live.
- Charts are `width="100%"` with a `viewBox`, and take theme colours only, with one highlight.
- Estimates are hatched. Every chart has "Show data" and "Copy CSV".
- Node graphs use `FlowGraph` (pan, zoom, drag, collapse, details, Back).
- No chart junk.

Check it with:

```bash
python3 scripts/check_premium.py page.tsx   # exit 0 ok, 1 misses
```

## Style rules

Taken from [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1) and the catalogue:

- One highlight colour (`theme.dataviz.categorical[0]`) and a gray baseline (`theme.dataviz.other`).
- Label points and bars directly.
- On score-versus-cost, up and to the left is better; say so once.
- Headline `Metrics` follows a lead sentence and appears once. Cost and wall-time figures may be sums; the caption must say so. The quality figure is cases passed (or the named case-level unit), never a pooled subunit rate.
- Per-case nested results stay visible in the drilldown.

## Done checks

- The Page renders and its link is the deliverable.
- `scripts/check_premium.py` exits 0 on the Page source.
- `make_chart_data.py validate` exits 0 on the embedded contract.
- Every number traces to a file listed in `sources`.
- Estimates are marked; missing values read `not measured`.
- No pooled score is used as the headline.

See the [synthetic worked example](examples/worked.md).
