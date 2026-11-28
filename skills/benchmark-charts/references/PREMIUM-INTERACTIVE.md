# Premium interactive charts: the standard

Every chart and node graph on a Page must meet this standard. `scripts/check_premium.py` checks it and exits 1 if anything is missing. Each item below names the lint rule that tests it (P0–P14). Items marked *review* need a human or agent eye, because a lint cannot see them.

Sources: Observable Plot's pointer transform (nearest-point hover), React Flow (pan, zoom, drag, groups), the MDN docs on `prefers-reduced-motion`, the W3C WAI-ARIA authoring practices (toggle buttons, live regions), Datawrapper and the FT chart style guides (direct labels, one highlight colour, hatched estimates), Tufte's data-ink ratio (no chart junk), and recent launch-post charts such as Cognition's SWE-2.1 post.

## Checklist

| # | Rule | Testable check |
|---|------|----------------|
| P0 | Shared primitives, no drift | The `// ==== PI:BEGIN` … `// ==== PI:END ====` block matches `references/premium-primitives.tsx` byte for byte. Re-paste the block; never fork it. |
| P1 | Tooltip with exact values and the source | Each chart renders `role="tooltip"` (via `ChartFrame`). Each `Tip` has `rows` with exact values and units, plus a `source` that names the file or contract field. |
| P2 | Hover on every data mark | Each bar, point, segment or node spreads `{...mark(c, tip)}`, or is reached through `NearestLayer`. |
| P3 | Visible active and focus ring | The active mark gets `t.border.focus` or a highlight row. *(warn)* |
| P4 | Click to pin, Escape to unpin | Clicking pins the tooltip. The chart shows an "Unpin (Esc)" button, and pressing `Escape` clears the pin. |
| P5 | Enter animation that respects reduced motion | Marks use `grow()` or `fade()` (a stagger of about 520 ms). `useReducedMotion()` turns the animation off when `prefers-reduced-motion: reduce` is set. |
| P6 | Legend chips toggle series; filters use segmented switches | The series chips are `aria-pressed` buttons, and the last visible series can't be hidden. Views and filters use `Segmented` or `Select`. A kit chart with no nearby control is a warn. |
| P7 | Keyboard and screen-reader support | Marks have `tabIndex=0` and `role="button"`. `Enter` or `Space` pins a mark. An `aria-label` states the value and the source. An `aria-live` region announces the active value. |
| P8 | Restrained palette, one highlight | There are no hex or rgb literals. The highlight is `t.dataviz.categorical[0]`, the baseline or "other" is `t.dataviz.other`, and the text and borders come from `t.text.*` and `t.border.*`. |
| P9 | Each chart is labelled | Every `<svg>` has an `aria-label` that states the claim. Interactive svgs use `role="group"`, not `role="img"`, so their children stay reachable. |
| P10 | Responsive layout | Every chart uses `width="100%"` with a `viewBox`, and no svg has a fixed pixel width. The tooltip position is computed as a percentage of the viewBox. |
| P11 | Estimates are hatched and labelled | Estimated marks use `hatchDef` fill or a dashed stroke, plus an `ESTIMATE` label. Tips set `est: true`, so the tooltip shows an ESTIMATE tag. |
| P12 | The reader can download or copy the data | `ChartFrame` provides a "Show data" table and "Copy CSV". The copy uses `navigator.clipboard` and falls back to the table. |
| P13 | Node graphs are interactive | Use `FlowGraph`, never a static `<Diagram>`. `FlowGraph` supports pan, zoom (+, −, Fit, Ctrl-wheel, keys + − 0) and dragging nodes. Groups collapse. Hovering a node highlights its neighbours. Clicking a node shows its details with From/To buttons, and Back (or Backspace) retraces the path. Opt out with `pi:allow-static-diagram` only for a purely decorative diagram. |
| P14 | No chart junk | No gradients, drop shadows, blur, 3-D or decorative images. Never draw a box around a chart. |

Review items the lint cannot see:

- **Typography and spacing scale.** Axis and tick labels are 11–12 px in `t.text.tertiary`, direct labels are 12 px in `t.text.primary`, and one caption line is in `t.text.secondary`. Chart titles go in the `Section` heading, not inside the svg. Spacing uses multiples of 4.
- **Direct labels beat legends.** Label bars and points where they sit, and say once which direction is better.
- **Crosshair or nearest point.** On lines and scatters, `NearestLayer` snaps to the nearest point within `maxR` (use `mode="x"` for lines) and `Crosshair` draws the guide.
- **Empty and loading states.** Page data is embedded, so a Page never loads. Hide or disable a filter option that matches 0 rows. Draw a missing value as a dashed "not measured" mark, never as zero. If a filter leaves a chart empty, show one line of text saying so.
- **Content does not change.** An interactivity upgrade keeps every number, label and caption, and only adds tooltips, toggles and the data table.

## Component recipe (canvas runtime)

Import from `grok/canvas` only, and paste the PI block from `references/premium-primitives.tsx`. Then:

```tsx
function MyChart() {
  const t = useGrokTheme();
  const series: SeriesKey[] = [{ id: "new", label: "New", color: t.dataviz.categorical[0] }, { id: "base", label: "Baseline", color: t.dataviz.other }];
  const c = useChart(series.map((s) => s.id));
  const W = 640, H = 300;
  const tips: Tip[] = ROWS.filter((r) => c.isOn(r.arm)).map((r) => ({
    key: r.id, series: r.arm, x: X(r.cost), y: Y(r.score), title: r.id,
    rows: [["Score", `${r.score}%`], ["Cost", `$${r.cost.toFixed(2)}`]],
    source: `chart_data.json · ${r.id}`, est: r.estimate,
  }));
  return (
    <ChartFrame label="Score versus cost" c={c} vb={[W, H]} series={series}
      data={{ columns: ["Case", "Score", "Cost"], rows: ROWS.map((r) => [r.id, r.score, r.cost]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Score versus cost; up and left is better">
        <defs>{hatchDef(t, "est")}</defs>
        {tips.map((p, i) => (
          <g key={p.key} {...mark(c, p)} style={{ ...mark(c, p).style, ...fade(c, t, i, c.dim(p.series, p.key)) }}>
            <circle cx={p.x} cy={p.y} r={isActive(c, p.key) ? 7 : 5} fill={p.est ? "url(#est)" : series.find((s) => s.id === p.series)!.color} />
          </g>
        ))}
        <NearestLayer c={c} tips={tips} x={40} y={20} w={W - 60} h={H - 50} W={W} H={H} />
      </svg>
    </ChartFrame>
  );
}
```

For a node graph, use `<FlowGraph label=… nodes={[{ id, label, detail, group, source }]} edges={[{ from, to }]} groups={[{ id, label }]} />`. Set `hulls={false}` when the members of a group are scattered across the layout.

Kit blocks (`Metrics`, `Table`, `Heatmap`) stay as they are, with a `Segmented` or `Select` placed next to them when the reader would want to explore.

To mark a helper as a primitive so the per-chart checks skip it, put `/* pi:primitive */` before the function.

## Running the check

```bash
python3 scripts/check_premium.py page.tsx            # exit 0 ok, 1 misses, 2 usage
python3 scripts/check_premium.py page.tsx --json     # machine-readable findings
```

Run it on the exact source you pass to `WriteCanvas`, or on the `ReadCanvas` output after the Page is written.
