# Visual-story styles for eval and benchmark pages

A catalogue of presentation patterns drawn from recent public posts and sites. Cite the source. Copy no proprietary assets, palettes, logos or chart images. Rebuild the *idea* with canvas kit components and `useGrokTheme()` tokens.

The default treatment for an eval or A/B Page is still the Cognition-style core in `templates/canvas-template.tsx`: a headline strip, small-multiple bars, a score-versus-cost scatter, paired latency bars, a stage breakdown and a per-case drilldown. Use this file to pick extra forms when the story needs them.

Every style below still obeys the data contract: per-case results come first, pooled scores are never the headline, estimates render hatched with an `ESTIMATE` label, and missing values render as `not measured`.

## When-to-use picker

| If you need to show… | Use | On the demo Page? |
|---|---|---|
| Two or four additive headlines (cost, time) plus case-level quality | Headline stat strip | Yes (core) |
| The same metric on two or three arms, side by side | Small-multiple bars | Yes (core) |
| Quality against spend, and which arm is more efficient | Score-versus-cost scatter / Pareto frontier | Yes (core) |
| Wall time on the same cases, with a speed-up label | Paired latency bars | Yes (core) |
| Before-and-after values and the gap, many rows | Dumbbell plot | Yes |
| Before-and-after change for a handful of cases, crossings included | Slope chart | Yes |
| Rank over three or more versions or dates | Bump chart | Catalogue only |
| How a total cost or token bill walks from A to B | Waterfall | Yes |
| Where tokens or dollars flow between stages | Sankey | Yes |
| A case × test (or market) pass/fail matrix | Heatmap | Yes |
| A few dates, runs or milestones with notes | Annotated timeline | Catalogue only |
| One claim at a time, then the chart changes | Step-reveal (scrolly analogue) | Yes |
| Tokens, time or dollars by stage, reader-picked view | Stage breakdown with a toggle | Yes (core) |
| Nested labels for one case at a time | Per-case drilldown | Yes (core) |
| A cumulative solve rate as time or compute grows | Test-time scaling curve | Catalogue only |
| A live board of many models, one row per model | Leaderboard table | Catalogue only |
| A grouped capability table (coding, knowledge, …) | Category comparison table | Catalogue only |
| The reader’s guess, then the measured line | You-draw-it | Catalogue only (rarely for internal evals) |

## Styles

### 1. Headline stat strip

**Pattern.** Open with one sentence, then three or four large figures. Quality is a case-level count (cases passed), not a pooled subunit rate. Additive sums (cost, wall time) may sit beside it when the caption says they are sums.

**When it fits.** The reader should leave with the comparison in under ten seconds.

**Sources.** [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1); [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5); [Introducing Mistral Large 4](https://mistral.ai/news/mistral-large-4/).

**On a canvas.** One lead `Text`, then one `Metrics` block (never two, and never as the first child of the page). Estimates get an `ESTIMATE` word in `detail`. Missing figures say `not measured`.

### 2. Small-multiple bars

**Pattern.** The same three-bar chart, repeated for cost, time and quality, with one highlight colour and a gray baseline. Empty or unknown arms are an outlined slot labeled `not measured`. Estimates are hatched.

**When it fits.** Two or three arms and a few headline metrics that should be compared at a glance.

**Sources.** [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1); [Gemini](https://deepmind.google/models/gemini/) (family of compact comparison panels).

**On a canvas.** A `Grid` of custom `HeroCard` SVGs. Highlight arm uses `theme.dataviz.categorical[0]`; baseline uses `theme.dataviz.other`. Hatch with a `pattern` and an `ESTIMATE` label.

### 3. Score-versus-cost scatter / Pareto frontier

**Pattern.** Each arm is a labelled point. Cost is on a log x-axis. Better is up and to the left. A short takeaway sits on the chart, not in a caption that restates the axes. A projected arm is a dashed band or a hatched marker with `ESTIMATE`, never a fake score.

**When it fits.** You are arguing efficiency, not only a higher score.

**Sources.** [FrontierCode leaderboard](https://cognition.com/frontiercode); [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) (accuracy versus cost at each effort); [Introducing Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5); [CursorBench 4.1](https://cursor.com/cursorbench); [How we compare model quality in Cursor](https://cursor.com/blog/cursorbench); [Developer Habits Report](https://cursor.com/insights/developer-habits); [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index).

**On a canvas.** Custom SVG (kit `Scatter` has no log axis). Label every point. Draw a takeaway in `theme.text.secondary`. Optional dashed frontier through undominated measured points.

### 4. Paired latency bars

**Pattern.** One row per case, two bars (baseline gray, highlight blue), a `N× faster` label at the right.

**When it fits.** Wall time is part of the claim and cases differ in size, so a single total would hide the pattern.

**Sources.** [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1).

**On a canvas.** Custom `LatencyBars` SVG. Missing wall time on one arm renders `not measured` instead of a bar.

### 5. Dumbbell plot

**Pattern.** One row per case. Two dots and a connecting line show the before and after value. The gap is the story. Label both ends.

**When it fits.** Many cases, two arms, and you care about the size of the change (score, cost or time) more than a rank crossing.

**Sources.** [FT Visual Vocabulary](https://ft-interactive.github.io/visual-vocabulary/); [Charts that work](https://www.ft.com/content/c7bb24c9-964d-479f-ba24-03a2b2df6e85); [Dumbbell chart guide](https://plotly.com/blog/dumbbell-chart-guide/).

**On a canvas.** Custom `DumbbellPlot` SVG. Highlight colour on the new arm, `theme.dataviz.other` on the baseline.

### 6. Slope chart

**Pattern.** Two vertical axes (baseline and highlight). One line per case. The slope is the change; a crossing is a rank swap.

**When it fits.** A handful of cases (about four to twelve) and two arms. Prefer a bump chart once you have three or more dates.

**Sources.** [FT Visual Vocabulary](https://ft-interactive.github.io/visual-vocabulary/); [Charts that work](https://www.ft.com/content/c7bb24c9-964d-479f-ba24-03a2b2df6e85); [Slope chart guide](https://plotly.com/blog/slope-chart-guide/).

**On a canvas.** Custom `SlopeChart` SVG. Direct case labels. Do not use a legend of coloured lines if four labels will fit on the axes.

### 7. Bump chart

**Pattern.** Rank on the y-axis (1 at the top), versions or dates on the x-axis, one line per arm or per case. Overtakes are visible.

**When it fits.** Three or more comparable runs and the story is who moved in the ranking, not the raw score.

**Sources.** [FT Visual Vocabulary](https://ft-interactive.github.io/visual-vocabulary/); [LMArena](https://lmarena.ai/) (Elo over time); [Epoch Capabilities Index](https://epoch.ai/eci).

**On a canvas.** Custom SVG, or a `LineChart` with inverted rank values and labels on every series. Keep to a few series. Not drawn on the TicketFix-4 demo, which has only two measured arms.

### 8. Waterfall cost breakdown

**Pattern.** A starting total, signed steps, and an ending total. Negative steps (savings) and positive steps (added cost) are visually distinct.

**When it fits.** You can attribute the difference between two arm totals to named stages.

**Sources.** Common in finance and in FT/Upshot budget explainers; used here for eval cost walks. See the FT vocabulary’s “deviation” family: [FT Visual Vocabulary](https://ft-interactive.github.io/visual-vocabulary/).

**On a canvas.** Custom `WaterfallChart` SVG. Steps come from the contract’s `waterfall` block and must land on the highlight arm’s cost sum.

### 9. Stage breakdown with a view toggle

**Pattern.** The same cases, three encodings (tokens, time, dollars), switched by the reader.

**When it fits.** The interesting question is *where* the spend or the time went, and the answer changes with the unit.

**Sources.** [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1) (test-time / long-horizon breakdowns); [How we compare model quality in Cursor](https://cursor.com/blog/cursorbench) (tokens as a compute proxy).

**On a canvas.** A `Segmented` control in the `Section`, then a custom `StageBars` SVG. Do not wrap the `Segmented` inside a custom component.

### 10. Sankey token-flow

**Pattern.** A flow from a source (input context or total tokens) into stages (planner, worker, tools) for one arm, or a paired comparison of two arms’ flows.

**When it fits.** The mix of stages matters more than a single stacked bar, and volumes differ by an order of magnitude.

**Sources.** Familiar from energy and budget explainers; see also stage-flow thinking in [How we built our multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system). Rebuild, do not copy any asset.

**On a canvas.** Custom `SankeyFlow` SVG with `theme.dataviz.categorical` colours and labelled link widths. Missing stages are omitted, not drawn at width zero.

### 11. Case × subunit heatmap

**Pattern.** A matrix of pass/fail (or a graded score) with cases or tests on one axis and arms or subunits on the other. The eye finds clusters of failures.

**When it fits.** Nested results matter and a table of labels is too wide to scan.

**Sources.** [Gemini model cards](https://deepmind.google/models/gemini/) and [Introducing Claude Fable 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2) (dense comparison matrices); eval leaderboards such as [CursorBench 4.1](https://cursor.com/cursorbench).

**On a canvas.** Kit `Heatmap` for numeric grids. For a selected case, rows are tests and columns are measured arms; values are 1 (pass) or 0 (fail). An arm with no labels is left out and noted as `not measured`.

### 12. Per-case drilldown

**Pattern.** A case picker, then that case’s verdict, cost, time and nested labels. Never a single pooled score in place of this section.

**When it fits.** Always, when cases have nested units. This is a contract rule, not only a style.

**Sources.** The same launch posts above, which still publish per-benchmark tables under the headline charts: [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1); [Introducing OpenAI o3 and o4-mini](https://openai.com/index/introducing-o3-and-o4-mini/).

**On a canvas.** `Segmented` to pick a case, then a `Table` of metrics and a `Table` of subunit labels with `tone` on pass/fail.

### 13. Step-reveal (scrolly analogue)

**Pattern.** One short claim per step. The figure updates with the step. The reader can go backwards. On a Page there is no scroll-jacking; a step control replaces sticky scrollytelling.

**When it fits.** A sequence of findings would be misread if all charts appeared at once, or you are teaching a mechanism.

**Sources.** [The Pudding, “Making Internet Things, part 3: Storytelling”](https://pudding.cool/process/how-to-make-dope-shit-part-3/); [Communicating with Interactive Articles](https://distill.pub/2020/communicating-with-interactive-articles/) on Distill.

**On a canvas.** A `Segmented` (or prev/next `Button`s) and a `Text` body that switch together, next to or above the figure for that step. Keep the control in the `Section`, not inside a custom component.

### 14. Annotated timeline

**Pattern.** A time or version axis with a few marked events and a short note at each mark.

**When it fits.** Runs happened on known dates, or a change is tied to a release, and the dates themselves are part of the story.

**Sources.** [Our World in Data explorers](https://ourworldindata.org/explorers); [LMArena](https://lmarena.ai/); [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1) (test-time scaling over a horizon).

**On a canvas.** Kit `LineChart` with `annotations`, or a small custom SVG. Prefer this over a bump chart when the y-axis is a value, not a rank.

### 15. Test-time scaling curve

**Pattern.** Cumulative score or flags captured against time or compute, often on a log-x axis, with a slope comparison to a baseline.

**When it fits.** The claim is that longer or more expensive rollouts still add solves.

**Sources.** [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1) (ExploitGym flags versus time).

**On a canvas.** `LineChart` or a custom log-x SVG. Do not invent a curve for an arm that was not run; label it `not measured`.

### 16. Leaderboard table

**Pattern.** One row per model or arm, sortable columns for score, cost, tokens, steps. A chart may sit above the table, but the table is the authority.

**When it fits.** Many arms, and the reader will want to sort or scan a column.

**Sources.** [FrontierCode leaderboard](https://cognition.com/frontiercode); [CursorBench 4.1](https://cursor.com/cursorbench); [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index); [LMArena](https://lmarena.ai/); [Epoch Capabilities Index](https://epoch.ai/eci).

**On a canvas.** Kit `Table` on a `wide` page. Keep headers short. Do not replace the per-case drilldown with this table.

### 17. Category comparison table

**Pattern.** Benchmarks grouped by category (coding, knowledge work, computer use), with one column per model. Dashes mean not reported, not zero.

**When it fits.** A launch-style overview across several suites, each with its own methodology note.

**Sources.** [Gemini](https://deepmind.google/models/gemini/); [Introducing Claude Fable 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2); [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5); [Introducing Mistral Large 4](https://mistral.ai/news/mistral-large-4/).

**On a canvas.** Kit `Table`. Write `not measured` rather than a blank or a zero when a cell was not run.

### 18. You-draw-it, then reveal

**Pattern.** The reader sketches a line or picks a guess; the page then reveals the measured series.

**When it fits.** External storytelling, teaching, or a public explainer where the surprise is the point. It is usually a poor fit for an internal eval report, where the job is to show the evidence first.

**Sources.** [NYT Upshot, “You Draw It: How Family Income Affects Children’s College Chances”](https://www.nytimes.com/interactive/2015/05/28/upshot/you-draw-it-how-family-income-affects-childrens-college-chances.html); [Communicating with Interactive Articles](https://distill.pub/2020/communicating-with-interactive-articles/).

**On a canvas.** An `Input` or pointer path, a `Button` to reveal, and then the measured `LineChart`. Never treat a guess as data.

## Shared rules

These rules are shared with `SKILL.md` and with the Cognition post that set the default look: [Introducing SWE-2.1](https://cognition.com/blog/swe-2-1).

- One highlight colour (`theme.dataviz.categorical[0]`) and a gray baseline (`theme.dataviz.other`).
- Label points and bars directly. A legend is only for shared series in a `Grid`.
- Up and to the left is better on a score-versus-cost chart. Say so once.
- Estimates are hatched or dashed and carry an `ESTIMATE` label. Missing values are `not measured`.
- Per-case nested results come first. A sum across cases may appear in the headline strip only when the caption says it is a sum, not a pooled score.
- Cite every source. Copy no proprietary assets.
