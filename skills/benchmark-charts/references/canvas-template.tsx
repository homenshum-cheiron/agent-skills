// Benchmark chart template for WriteCanvas.
// Import only from grok/canvas. Custom functions may return SVG; kit blocks
// (Metrics, Segmented, Table, Heatmap, Text) stay directly in Page or Section.
// Replace the DATA constants with the contract JSON from make_chart_data.py.
// Source of these demo numbers: examples/chart_data.json, built from examples/raw_results.json.

import { Page, Section, Text, Callout, Table, Segmented, TableOfContents, Grid, LinkCards, Metrics, Heatmap, useState, useGrokTheme } from "grok/canvas";

type ArmId = "baseline" | "tool_loop" | "compact";
type CaseId = "AUTH-01" | "SEARCH-02" | "MIGRATE-03" | "REPORT-04";
type StageView = "tokens" | "time" | "cost";
type StoryId = "baseline" | "tool_loop" | "cost" | "left";
type Kind = "old" | "res" | "est";

type ArmResult = {
  verdict: "pass" | "fail" | "incomplete" | "not_measured";
  passed: number | null;
  n: number | null;
  cost: number | null;
  costLo?: number;
  costHi?: number;
  wall: number | null;
  tokens?: { planner: number; worker: number; tools: number };
  time?: { planner: number; worker: number; tools: number };
  costParts?: { planner: number; worker: number; tools: number };
  tests: { id: string; label: string }[];
};

type CaseRow = {
  id: CaseId;
  label: string;
  baseline: ArmResult;
  tool_loop: ArmResult;
  compact: ArmResult;
};

const CASES: CaseRow[] = [
  {
    id: "AUTH-01",
    label: "Login session refresh",
    baseline: { verdict: "pass", passed: 5, n: 5, cost: 2.4, wall: 312, tokens: { planner: 82000, worker: 410000, tools: 28000 }, time: { planner: 40, worker: 240, tools: 32 }, costParts: { planner: 0.4, worker: 1.85, tools: 0.15 }, tests: [{ id: "login", label: "pass" }, { id: "session", label: "pass" }, { id: "refresh", label: "pass" }, { id: "logout", label: "pass" }, { id: "lockout", label: "pass" }] },
    tool_loop: { verdict: "pass", passed: 5, n: 5, cost: 0.62, wall: 140, tokens: { planner: 18000, worker: 92000, tools: 14000 }, time: { planner: 18, worker: 102, tools: 20 }, costParts: { planner: 0.1, worker: 0.44, tools: 0.08 }, tests: [{ id: "login", label: "pass" }, { id: "session", label: "pass" }, { id: "refresh", label: "pass" }, { id: "logout", label: "pass" }, { id: "lockout", label: "pass" }] },
    compact: { verdict: "not_measured", passed: null, n: 5, cost: 0.55, costLo: 0.4, costHi: 0.55, wall: null, tests: [] }
  },
  {
    id: "SEARCH-02",
    label: "Catalog query filters",
    baseline: { verdict: "fail", passed: 4, n: 6, cost: 3.1, wall: 510, tokens: { planner: 110000, worker: 680000, tools: 45000 }, time: { planner: 55, worker: 410, tools: 45 }, costParts: { planner: 0.5, worker: 2.4, tools: 0.2 }, tests: [{ id: "exact", label: "pass" }, { id: "prefix", label: "pass" }, { id: "filter", label: "pass" }, { id: "sort", label: "pass" }, { id: "empty", label: "fail" }, { id: "pagination", label: "fail" }] },
    tool_loop: { verdict: "pass", passed: 6, n: 6, cost: 0.88, wall: 188, tokens: { planner: 22000, worker: 140000, tools: 20000 }, time: { planner: 22, worker: 140, tools: 26 }, costParts: { planner: 0.12, worker: 0.64, tools: 0.12 }, tests: [{ id: "exact", label: "pass" }, { id: "prefix", label: "pass" }, { id: "filter", label: "pass" }, { id: "sort", label: "pass" }, { id: "empty", label: "pass" }, { id: "pagination", label: "pass" }] },
    compact: { verdict: "not_measured", passed: null, n: 6, cost: 0.8, costLo: 0.6, costHi: 0.8, wall: null, tests: [] }
  },
  {
    id: "MIGRATE-03",
    label: "Schema migration",
    baseline: { verdict: "fail", passed: 5, n: 8, cost: 6.8, wall: 980, tokens: { planner: 195000, worker: 1420000, tools: 88000 }, time: { planner: 90, worker: 790, tools: 100 }, costParts: { planner: 1.1, worker: 5.2, tools: 0.5 }, tests: [{ id: "up", label: "pass" }, { id: "down", label: "pass" }, { id: "dry_run", label: "pass" }, { id: "backup", label: "pass" }, { id: "conflict", label: "fail" }, { id: "rollback", label: "fail" }, { id: "seed", label: "pass" }, { id: "perms", label: "fail" }] },
    tool_loop: { verdict: "fail", passed: 7, n: 8, cost: 1.45, wall: 290, tokens: { planner: 35000, worker: 310000, tools: 30000 }, time: { planner: 30, worker: 220, tools: 40 }, costParts: { planner: 0.18, worker: 1.07, tools: 0.2 }, tests: [{ id: "up", label: "pass" }, { id: "down", label: "pass" }, { id: "dry_run", label: "pass" }, { id: "backup", label: "pass" }, { id: "conflict", label: "pass" }, { id: "rollback", label: "pass" }, { id: "seed", label: "pass" }, { id: "perms", label: "fail" }] },
    compact: { verdict: "not_measured", passed: null, n: 8, cost: 1.4, costLo: 1.1, costHi: 1.4, wall: null, tests: [] }
  },
  {
    id: "REPORT-04",
    label: "Weekly digest export",
    baseline: { verdict: "fail", passed: 4, n: 7, cost: 5.2, wall: 840, tokens: { planner: 150000, worker: 980000, tools: 62000 }, time: { planner: 70, worker: 690, tools: 80 }, costParts: { planner: 0.8, worker: 3.95, tools: 0.45 }, tests: [{ id: "csv", label: "pass" }, { id: "pdf", label: "pass" }, { id: "empty", label: "pass" }, { id: "timezone", label: "fail" }, { id: "totals", label: "fail" }, { id: "access", label: "pass" }, { id: "schedule", label: "fail" }] },
    tool_loop: { verdict: "fail", passed: 6, n: 7, cost: 1.22, wall: 260, tokens: { planner: 28000, worker: 210000, tools: 24000 }, time: { planner: 24, worker: 200, tools: 36 }, costParts: { planner: 0.15, worker: 0.77, tools: 0.3 }, tests: [{ id: "csv", label: "pass" }, { id: "pdf", label: "pass" }, { id: "empty", label: "pass" }, { id: "timezone", label: "pass" }, { id: "totals", label: "pass" }, { id: "access", label: "pass" }, { id: "schedule", label: "fail" }] },
    compact: { verdict: "not_measured", passed: null, n: 7, cost: 1.2, costLo: 0.9, costHi: 1.2, wall: null, tests: [] }
  }
];

const STORY: { id: StoryId; title: string; body: string }[] = [
  { id: "baseline", title: "The baseline run", body: "On the four frozen tickets the baseline agent passed 1 of 4 cases, spent $17.50 and took 44.0 minutes of wall time." },
  { id: "tool_loop", title: "The tool-loop run", body: "The tool-loop agent passed 2 of 4 cases, spent $4.17 and took 14.6 minutes. AUTH-01 stayed a pass. SEARCH-02 flipped from fail to pass." },
  { id: "cost", title: "Where the dollars went", body: "Of the $13.33 cut, $10.48 came from worker tokens, $2.25 from the planner, and $0.60 from tools. These are sums across cases, not a pooled score." },
  { id: "left", title: "What is still open", body: "MIGRATE-03 still misses the perms test. REPORT-04 still misses the schedule test. The compact-context cost is an estimate; its score is not measured." }
];

function fmtMin(s: number): string { return `${(s / 60).toFixed(1)} min`; }
function fmtUsd(n: number): string { return `$${n.toFixed(2)}`; }
function verdictCell(v: string) {
  if (v === "pass") return { text: v, tone: "success" as const };
  if (v === "incomplete") return { text: v, tone: "warning" as const };
  if (v === "not_measured") return "not measured";
  return { text: v, tone: "danger" as const };
}
function labelCell(l: string) {
  if (l === "pass") return { text: l, tone: "success" as const };
  if (l === "not_measured") return "not measured";
  return { text: l, tone: "danger" as const };
}

function HeroCard(props: { title: string; unit: string; bars: { label: string; value: number | null; display: string; kind: Kind }[]; max: number }) {
  const t = useGrokTheme();
  const W = 400, H = 230, base = 180, top = 34, bw = 82, gap = 34, x0 = (W - (3 * bw + 2 * gap)) / 2;
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={props.title}>
      <defs>
        <pattern id={`hatch-${props.unit}`} width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" stroke={t.dataviz.categorical[0]} strokeWidth="2" opacity="0.55" />
        </pattern>
      </defs>
      <line x1="8" x2={W - 8} y1={base} y2={base} stroke={t.border.default} strokeWidth="1" />
      {props.bars.map((b, i) => {
        const x = x0 + i * (bw + gap);
        if (b.value === null) {
          return (
            <g key={b.label}>
              <rect x={x} y={base - 60} width={bw} height={60} fill="none" stroke={t.text.tertiary} strokeDasharray="4 4" />
              <text x={x + bw / 2} y={base - 26} textAnchor="middle" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>{b.display}</text>
              <text x={x + bw / 2} y={base + 20} textAnchor="middle" fontSize="13" fill={t.text.secondary}>{b.label}</text>
            </g>
          );
        }
        const h = Math.max(3, (b.value / props.max) * (base - top));
        const fill = b.kind === "res" ? t.dataviz.categorical[0] : b.kind === "old" ? t.dataviz.other : `url(#hatch-${props.unit})`;
        return (
          <g key={b.label}>
            <rect x={x} y={base - h} width={bw} height={h} fill={fill} stroke={b.kind === "est" ? t.dataviz.categorical[0] : "none"} strokeDasharray={b.kind === "est" ? "4 3" : undefined} />
            <text x={x + bw / 2} y={base - h - 8} textAnchor="middle" fontFamily={t.font.mono} fontSize="15" fontWeight={b.kind === "res" ? 600 : 400} fill={t.text.primary}>{b.display}</text>
            <text x={x + bw / 2} y={base + 20} textAnchor="middle" fontSize="13" fill={b.kind === "res" ? t.text.primary : t.text.secondary}>{b.label}</text>
          </g>
        );
      })}
      <text x={W / 2} y={H - 6} textAnchor="middle" fontSize="11" fill={t.text.tertiary}>{props.unit}</text>
    </svg>
  );
}

function ScoreCost() {
  const t = useGrokTheme();
  const W = 1240, H = 420, L = 80, R = 40, T = 70, B = 60;
  const lx = (v: number) => L + ((Math.log10(v) - Math.log10(1)) / (Math.log10(40) - Math.log10(1))) * (W - L - R);
  const ly = (m: number) => T + (1 - m / 4) * (H - T - B);
  const ticksX = [1, 2, 5, 10, 20, 40];
  const ticksY = [0, 1, 2, 3, 4];
  const old = { x: lx(17.5), y: ly(1) }, res = { x: lx(4.17), y: ly(2) };
  const laneY = 36;
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Cases passed versus four-case cost">
      {ticksY.map((m) => (<g key={m}><line x1={L} x2={W - R} y1={ly(m)} y2={ly(m)} stroke={t.border.subtle} /><text x={L - 12} y={ly(m) + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>{m}</text></g>))}
      {ticksX.map((v) => (<g key={v}><line x1={lx(v)} x2={lx(v)} y1={T} y2={H - B} stroke={t.border.subtle} /><text x={lx(v)} y={H - B + 22} textAnchor="middle" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>${v}</text></g>))}
      <text x={(L + W - R) / 2} y={H - 12} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Whole-harness cost for the four cases (log scale)</text>
      <text x={18} y={T - 14} fontSize="12" fill={t.text.secondary}>Cases passed (of 4)</text>
      <defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={t.text.tertiary} /></marker></defs>
      <line x1={old.x} y1={old.y} x2={res.x + 10} y2={res.y + 8} stroke={t.text.tertiary} strokeDasharray="5 4" markerEnd="url(#arr)" />
      <text x={(old.x + res.x) / 2 + 20} y={(old.y + res.y) / 2 - 14} textAnchor="middle" fontSize="13" fill={t.text.secondary}>76.2% cheaper, +1 case passed</text>
      <circle cx={old.x} cy={old.y} r="9" fill={t.dataviz.other} />
      <text x={old.x + 14} y={old.y + 22} fontSize="14" fill={t.text.primary}>Baseline agent (1 Oct)</text>
      <text x={old.x + 14} y={old.y + 40} fontFamily={t.font.mono} fontSize="13" fill={t.text.secondary}>1 / 4 · $17.50</text>
      <circle cx={res.x} cy={res.y} r="11" fill={t.dataviz.categorical[0]} />
      <text x={res.x - 16} y={res.y - 18} textAnchor="end" fontSize="14" fontWeight={600} fill={t.text.primary}>Tool-loop agent (15 Oct)</text>
      <text x={res.x - 16} y={res.y - 2} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.secondary}>2 / 4 · $4.17</text>
      <rect x={lx(3.0)} y={laneY - 9} width={lx(3.95) - lx(3.0)} height={18} fill="none" stroke={t.dataviz.categorical[0]} strokeDasharray="4 3" />
      <line x1={lx(3.0)} x2={lx(3.0)} y1={laneY + 9} y2={H - B} stroke={t.dataviz.categorical[0]} strokeDasharray="2 5" opacity="0.6" />
      <line x1={lx(3.95)} x2={lx(3.95)} y1={laneY + 9} y2={H - B} stroke={t.dataviz.categorical[0]} strokeDasharray="2 5" opacity="0.6" />
      <text x={lx(3.95) + 10} y={laneY - 2} fontSize="13" fontWeight={600} fill={t.text.primary}>Compact-context: ESTIMATE</text>
      <text x={lx(3.95) + 10} y={laneY + 15} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>$3.00–$3.95 · score not measured</text>
    </svg>
  );
}

function LatencyBars() {
  const t = useGrokTheme();
  const W = 1240, rowH = 64, L = 150, R = 150, T = 10;
  const H = T + CASES.length * rowH + 10;
  const max = 1000;
  const sx = (s: number) => (s / max) * (W - L - R);
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Wall time per case">
      {CASES.map((c, i) => {
        const y = T + i * rowH;
        const speed = ((c.baseline.wall ?? 0) / (c.tool_loop.wall ?? 1)).toFixed(1);
        return (
          <g key={c.id}>
            <text x={L - 14} y={y + 26} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{c.id}</text>
            <rect x={L} y={y + 6} width={sx(c.baseline.wall ?? 0)} height={20} fill={t.dataviz.other} />
            <text x={L + sx(c.baseline.wall ?? 0) + 8} y={y + 21} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>{fmtMin(c.baseline.wall ?? 0)}</text>
            <rect x={L} y={y + 30} width={sx(c.tool_loop.wall ?? 0)} height={20} fill={t.dataviz.categorical[0]} />
            <text x={L + sx(c.tool_loop.wall ?? 0) + 8} y={y + 45} fontFamily={t.font.mono} fontSize="12" fontWeight={600} fill={t.text.primary}>{fmtMin(c.tool_loop.wall ?? 0)}</text>
            <text x={W - 10} y={y + 33} textAnchor="end" fontFamily={t.font.mono} fontSize="14" fill={t.text.primary}>{speed}× faster</text>
          </g>
        );
      })}
    </svg>
  );
}

function StageBars(props: { mode: StageView }) {
  const t = useGrokTheme();
  const W = 1240, rowH = 64, L = 150, R = 200, T = 8;
  const H = T + CASES.length * rowH + 6;
  const c0 = t.dataviz.categorical[0], c1 = t.dataviz.categorical[1], c2 = t.dataviz.categorical[2], gray = t.dataviz.other;
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Breakdown by stage">
      {CASES.map((c, i) => {
        const y = T + i * rowH;
        const name = <text x={L - 14} y={y + 22} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{c.id}</text>;
        if (props.mode === "tokens") {
          const max = 1_800_000;
          const sx = (v: number) => (v / max) * (W - L - R);
          const b = c.baseline.tokens, n = c.tool_loop.tokens;
          if (!b || !n) return <g key={c.id}>{name}</g>;
          const bt = b.planner + b.worker + b.tools, nt = n.planner + n.worker + n.tools;
          return (
            <g key={c.id}>{name}
              <rect x={L} y={y + 6} width={sx(b.planner)} height={18} fill={gray} />
              <rect x={L + sx(b.planner)} y={y + 6} width={sx(b.worker)} height={18} fill={c1} />
              <rect x={L + sx(b.planner + b.worker)} y={y + 6} width={sx(b.tools)} height={18} fill={c2} />
              <text x={L + sx(bt) + 8} y={y + 20} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>{(bt / 1000).toFixed(0)}k now</text>
              <rect x={L} y={y + 28} width={sx(n.planner)} height={18} fill={gray} opacity="0.7" />
              <rect x={L + sx(n.planner)} y={y + 28} width={sx(n.worker)} height={18} fill={c0} />
              <rect x={L + sx(n.planner + n.worker)} y={y + 28} width={sx(n.tools)} height={18} fill={c2} />
              <text x={L + sx(nt) + 8} y={y + 42} fontFamily={t.font.mono} fontSize="12" fontWeight={600} fill={t.text.primary}>{(nt / 1000).toFixed(0)}k tool-loop</text>
            </g>
          );
        }
        if (props.mode === "time") {
          const max = 1000;
          const sx = (v: number) => (v / max) * (W - L - R);
          const b = c.baseline.time, n = c.tool_loop.time;
          if (!b || !n) return <g key={c.id}>{name}</g>;
          return (
            <g key={c.id}>{name}
              <rect x={L} y={y + 6} width={sx(b.planner + b.worker + b.tools)} height={18} fill={gray} />
              <text x={L + sx(b.planner + b.worker + b.tools) + 8} y={y + 20} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>{fmtMin(c.baseline.wall ?? 0)} wall</text>
              <rect x={L} y={y + 28} width={sx(n.planner)} height={18} fill={c1} />
              <rect x={L + sx(n.planner)} y={y + 28} width={sx(n.worker)} height={18} fill={c0} />
              <rect x={L + sx(n.planner + n.worker)} y={y + 28} width={sx(n.tools)} height={18} fill={c2} />
              <text x={L + sx(n.planner + n.worker + n.tools) + 8} y={y + 42} fontFamily={t.font.mono} fontSize="12" fontWeight={600} fill={t.text.primary}>{n.planner}+{n.worker}+{n.tools}s stages</text>
            </g>
          );
        }
        const max = 8;
        const sx = (v: number) => (v / max) * (W - L - R);
        const b = c.baseline.costParts, n = c.tool_loop.costParts;
        if (!b || !n || c.baseline.cost === null || c.tool_loop.cost === null) return <g key={c.id}>{name}</g>;
        return (
          <g key={c.id}>{name}
            <rect x={L} y={y + 6} width={sx(b.planner)} height={18} fill={gray} />
            <rect x={L + sx(b.planner)} y={y + 6} width={sx(b.worker)} height={18} fill={gray} opacity="0.7" />
            <rect x={L + sx(b.planner + b.worker)} y={y + 6} width={sx(b.tools)} height={18} fill={gray} opacity="0.4" />
            <text x={L + sx(c.baseline.cost) + 8} y={y + 20} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>old {fmtUsd(c.baseline.cost)}</text>
            <rect x={L} y={y + 28} width={sx(n.planner)} height={18} fill={c1} />
            <rect x={L + sx(n.planner)} y={y + 28} width={sx(n.worker)} height={18} fill={c0} />
            <rect x={L + sx(n.planner + n.worker)} y={y + 28} width={sx(n.tools)} height={18} fill={c2} />
            <text x={L + sx(c.tool_loop.cost) + 8} y={y + 42} fontFamily={t.font.mono} fontSize="12" fontWeight={600} fill={t.text.primary}>tool-loop {fmtUsd(c.tool_loop.cost)}</text>
          </g>
        );
      })}
    </svg>
  );
}

function DumbbellPlot() {
  const t = useGrokTheme();
  const W = 1240, rowH = 56, L = 150, R = 80, T = 8;
  const H = T + CASES.length * rowH + 8;
  const max = 8;
  const sx = (v: number) => L + (v / max) * (W - L - R);
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Cost per case, baseline to tool-loop">
      {CASES.map((c, i) => {
        const y = T + i * rowH + 28;
        const a = c.baseline.cost ?? 0, b = c.tool_loop.cost ?? 0;
        const x1 = sx(a), x2 = sx(b);
        return (
          <g key={c.id}>
            <text x={L - 14} y={y + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{c.id}</text>
            <line x1={x2} x2={x1} y1={y} y2={y} stroke={t.dataviz.other} strokeWidth="3" />
            <circle cx={x1} cy={y} r="7" fill={t.dataviz.other} />
            <circle cx={x2} cy={y} r="8" fill={t.dataviz.categorical[0]} />
            <text x={x1 + 12} y={y - 12} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>{fmtUsd(a)}</text>
            <text x={x2 - 12} y={y - 12} textAnchor="end" fontFamily={t.font.mono} fontSize="12" fontWeight={600} fill={t.text.primary}>{fmtUsd(b)}</text>
          </g>
        );
      })}
    </svg>
  );
}

function SlopeChart() {
  const t = useGrokTheme();
  const W = 1240, H = 360, L = 180, R = 180, T = 28, B = 36;
  const x0 = L, x1 = W - R;
  const ly = (v: number) => T + (1 - (v - 3) / 5) * (H - T - B);
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Tests passed per case, baseline to tool-loop">
      <line x1={x0} x2={x0} y1={T} y2={H - B} stroke={t.border.default} />
      <line x1={x1} x2={x1} y1={T} y2={H - B} stroke={t.border.default} />
      <text x={x0} y={H - 8} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Baseline</text>
      <text x={x1} y={H - 8} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Tool-loop</text>
      {CASES.map((c) => {
        const a = c.baseline.passed ?? 0, b = c.tool_loop.passed ?? 0;
        const y0 = ly(a), y1 = ly(b);
        return (
          <g key={c.id}>
            <line x1={x0} x2={x1} y1={y0} y2={y1} stroke={t.dataviz.categorical[0]} strokeWidth="2" />
            <circle cx={x0} cy={y0} r="6" fill={t.dataviz.other} />
            <circle cx={x1} cy={y1} r="6" fill={t.dataviz.categorical[0]} />
            <text x={x0 - 12} y={y0 + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{c.id} {a}/{c.baseline.n}</text>
            <text x={x1 + 12} y={y1 + 4} fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{b}/{c.tool_loop.n}</text>
          </g>
        );
      })}
    </svg>
  );
}

function WaterfallChart() {
  const t = useGrokTheme();
  const W = 1240, H = 360, L = 70, R = 40, T = 40, B = 50, base = H - B;
  const steps = [
    { label: "Baseline", value: 17.5, kind: "start" as const },
    { label: "Planner", value: -2.25, kind: "delta" as const },
    { label: "Worker", value: -10.48, kind: "delta" as const },
    { label: "Tools", value: -0.6, kind: "delta" as const },
    { label: "Tool-loop", value: 4.17, kind: "end" as const }
  ];
  const max = 18;
  const sy = (v: number) => (v / max) * (base - T);
  const bw = 120, gap = 80;
  const x0 = L + 40;
  let running = 17.5;
  const placed = steps.map((s, i) => {
    const top = s.kind === "delta" ? running : s.value;
    const height = s.kind === "delta" ? Math.abs(s.value) : s.value;
    const y = s.kind === "delta" && s.value < 0 ? base - sy(running) : base - sy(s.kind === "delta" ? running + s.value : s.value);
    if (s.kind === "delta") running += s.value;
    return { ...s, x: x0 + i * (bw + gap), y, height: sy(height), top };
  });
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Cost waterfall from baseline to tool-loop">
      <line x1={L} x2={W - R} y1={base} y2={base} stroke={t.border.default} />
      {placed.map((s, i) => {
        const fill = s.kind === "start" ? t.dataviz.other : s.kind === "end" ? t.dataviz.categorical[0] : t.dataviz.categorical[1];
        const label = s.kind === "delta" ? `−${fmtUsd(Math.abs(s.value))}` : fmtUsd(s.value);
        const prev = placed[i - 1];
        return (
          <g key={s.label}>
            {prev ? <line x1={prev.x + bw} x2={s.x} y1={s.kind === "end" ? s.y : s.y} y2={s.kind === "end" ? s.y : s.y} stroke={t.text.tertiary} strokeDasharray="4 3" /> : null}
            <rect x={s.x} y={s.y} width={bw} height={Math.max(3, s.height)} fill={fill} />
            <text x={s.x + bw / 2} y={s.y - 8} textAnchor="middle" fontFamily={t.font.mono} fontSize="14" fill={t.text.primary}>{label}</text>
            <text x={s.x + bw / 2} y={base + 22} textAnchor="middle" fontSize="13" fill={t.text.secondary}>{s.label}</text>
          </g>
        );
      })}
    </svg>
  );
}

function SankeyFlow(props: { arm: "baseline" | "tool_loop" }) {
  const t = useGrokTheme();
  const totals = { baseline: { planner: 537000, worker: 3490000, tools: 223000, all: 4250000 }, tool_loop: { planner: 103000, worker: 752000, tools: 88000, all: 943000 } };
  const d = totals[props.arm];
  const W = 600, H = 280, xL = 20, xR = 380, nodeW = 16;
  const scale = 200 / 3490000;
  const leftH = Math.max(24, d.all * scale);
  const leftY = (H - leftH) / 2;
  const right = [
    { name: "planner", v: d.planner, color: t.dataviz.categorical[1] },
    { name: "worker", v: d.worker, color: t.dataviz.categorical[0] },
    { name: "tools", v: d.tools, color: t.dataviz.categorical[2] }
  ];
  let acc = 36;
  const rights = right.map((r) => {
    const h = Math.max(10, r.v * scale);
    const y = acc;
    acc += h + 18;
    return { ...r, y, h };
  });
  let lAcc = leftY;
  const links = rights.map((r) => {
    const h = Math.max(10, r.v * scale);
    const y1 = lAcc;
    lAcc += h;
    return { ...r, y1, h };
  });
  return (
    <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${props.arm} token flow`}>
      <rect x={xL} y={leftY} width={nodeW} height={leftH} fill={t.dataviz.other} />
      <text x={xL} y={leftY - 8} fontSize="12" fill={t.text.secondary}>Total {(d.all / 1000).toFixed(0)}k</text>
      {links.map((r, i) => {
        const y2 = rights[i].y;
        const path = `M ${xL + nodeW} ${r.y1} C ${(xL + xR) / 2} ${r.y1}, ${(xL + xR) / 2} ${y2}, ${xR} ${y2} L ${xR} ${y2 + r.h} C ${(xL + xR) / 2} ${y2 + r.h}, ${(xL + xR) / 2} ${r.y1 + r.h}, ${xL + nodeW} ${r.y1 + r.h} Z`;
        return <path key={r.name} d={path} fill={r.color} opacity="0.55" />;
      })}
      {rights.map((r) => (
        <g key={r.name}>
          <rect x={xR} y={r.y} width={nodeW} height={r.h} fill={r.color} />
          <text x={xR + nodeW + 8} y={r.y + r.h / 2 + 4} fontSize="13" fill={t.text.primary}>{r.name} {(r.v / 1000).toFixed(0)}k</text>
        </g>
      ))}
    </svg>
  );
}

export default function App() {
  const [cs, setCs] = useState<CaseId>("SEARCH-02");
  const [stage, setStage] = useState<StageView>("tokens");
  const [story, setStory] = useState<StoryId>("baseline");
  const sel = CASES.find((c) => c.id === cs) ?? CASES[0];
  const step = STORY.find((s) => s.id === story) ?? STORY[0];
  const heatRows = sel.baseline.tests.map((t) => t.id);
  const heatValues = sel.baseline.tests.map((row, i) => {
    const b = row.label === "pass" ? 1 : 0;
    const n = sel.tool_loop.tests[i]?.label === "pass" ? 1 : 0;
    return [b, n];
  });
  return (
    <Page width="wide" title="TicketFix-4: tool-loop vs baseline" summary="A synthetic four-ticket issue-fixing bench used to prove the benchmark chart kit. All figures are invented. Last updated: Fri 27 Nov 2026, 3:40 AM PT.">
      <TableOfContents items={[{ label: "Headline numbers" }, { label: "Score vs cost" }, { label: "Latency per case" }, { label: "Cost dumbbells" }, { label: "Tests-passed slopes" }, { label: "Where the tokens, time and dollars go" }, { label: "Cost waterfall" }, { label: "Token flow" }, { label: "Test heatmap" }, { label: "Per-case results" }, { label: "Step-by-step" }, { label: "Sources" }]} />
      <Section heading="Headline numbers" caption="Four frozen tickets, same grader. Hatched or dashed marks are estimates. Cost and wall time are sums across cases, not a pooled score. Quality is cases passed.">
        <Text>The tool-loop agent passed one more case than the baseline, cost less, and took less wall time. A compact-context design has a cost estimate only; its score is not measured.</Text>
        <Metrics metrics={[{ value: "76.2%", label: "cheaper", detail: "$17.50 → $4.17, sum of case costs" }, { value: "66.8%", label: "less wall time", detail: "44.0 min → 14.6 min, sum of case wall times" }, { value: "2 vs 1", label: "cases passed of 4", detail: "the quality headline; per case below" }, { value: "not measured", label: "compact-context score", detail: "cost $3.00–$3.95 ESTIMATE" }]} />
        <Text>Gray bars: baseline agent (1 Oct). Blue bars: tool-loop agent (15 Oct). Hatched bars: compact-context design, an ESTIMATE.</Text>
        <Grid columns={3}>
          <Section heading="Cost, four cases">
            <HeroCard title="Cost" unit="USD, summed" max={18} bars={[{ label: "Baseline", value: 17.5, display: "$17.50", kind: "old" }, { label: "Tool-loop", value: 4.17, display: "$4.17", kind: "res" }, { label: "Compact (EST)", value: 3.95, display: "$3.00–$3.95", kind: "est" }]} />
          </Section>
          <Section heading="Wall time, four cases">
            <HeroCard title="Wall time" unit="minutes, summed per case" max={50} bars={[{ label: "Baseline", value: 44.0, display: "44.0 min", kind: "old" }, { label: "Tool-loop", value: 14.6, display: "14.6 min", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} />
          </Section>
          <Section heading="Cases passed">
            <HeroCard title="Cases passed" unit="of 4 tickets" max={4} bars={[{ label: "Baseline", value: 1, display: "1", kind: "old" }, { label: "Tool-loop", value: 2, display: "2", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} />
          </Section>
        </Grid>
      </Section>
      <Section heading="Score vs cost" caption="Up and to the left is better. The compact-context design has a cost estimate only; its score is not measured.">
        <ScoreCost />
      </Section>
      <Section heading="Latency per case" caption="Wall time per case, first span to last. Gray is the baseline, blue is tool-loop.">
        <LatencyBars />
      </Section>
      <Section heading="Cost dumbbells" caption="One row per case. Gray is the baseline cost, blue is tool-loop. The gap is the saving.">
        <DumbbellPlot />
      </Section>
      <Section heading="Tests-passed slopes" caption="Two axes, one line per case. Nested test counts are shown here as a per-case change, not as a pooled score.">
        <SlopeChart />
      </Section>
      <Section heading="Where the tokens, time and dollars go">
        <Segmented options={[{ value: "tokens", label: "Tokens by stage" }, { value: "time", label: "Time by stage" }, { value: "cost", label: "Dollars by stage" }]} value={stage} onChange={(x: StageView) => setStage(x)} />
        <Text>{stage === "tokens" ? "Top row per case is the baseline: gray planner, yellow worker, cyan tools. Bottom row is tool-loop, with the worker in blue." : stage === "time" ? "Gray is baseline wall time. The blue row splits tool-loop into planner, worker and tools. Stage seconds may overlap, so they need not sum to wall time." : "Top row is baseline cost by stage. Bottom row is tool-loop."}</Text>
        <StageBars mode={stage} />
      </Section>
      <Section heading="Cost waterfall" caption="How the summed four-case cost walks from the baseline total to the tool-loop total.">
        <WaterfallChart />
      </Section>
      <Section heading="Token flow" caption="Input tokens into planner, worker and tools. Widths follow token counts from the synthetic run log.">
        <Grid columns={2}>
          <Section heading="Baseline">
            <SankeyFlow arm="baseline" />
          </Section>
          <Section heading="Tool-loop">
            <SankeyFlow arm="tool_loop" />
          </Section>
        </Grid>
      </Section>
      <Section heading="Test heatmap" caption="Pass is 1, fail is 0, for the selected case. The compact-context arm has no labels and is omitted (not measured).">
        <Segmented options={CASES.map((c) => ({ value: c.id, label: c.id }))} value={cs} onChange={(x: CaseId) => setCs(x)} />
        <Heatmap rows={heatRows} columns={["Baseline", "Tool-loop"]} values={heatValues} max={1} />
      </Section>
      <Section heading="Per-case results" caption="Never pooled. Each test keeps its own label; green passes, red fails.">
        <Segmented options={CASES.map((c) => ({ value: c.id, label: c.id }))} value={cs} onChange={(x: CaseId) => setCs(x)} />
        <Table columns={["", "Baseline", "Tool-loop", "Compact-context"]} emphasis={2} rows={[
          ["Case verdict", verdictCell(sel.baseline.verdict), verdictCell(sel.tool_loop.verdict), "not measured"],
          ["Tests passed", sel.baseline.passed === null ? "not measured" : `${sel.baseline.passed} / ${sel.baseline.n}`, sel.tool_loop.passed === null ? "not measured" : `${sel.tool_loop.passed} / ${sel.tool_loop.n}`, "not measured"],
          ["Cost", sel.baseline.cost === null ? "not measured" : fmtUsd(sel.baseline.cost), sel.tool_loop.cost === null ? "not measured" : fmtUsd(sel.tool_loop.cost), "$" + (sel.compact.costLo ?? 0).toFixed(2) + "–$" + (sel.compact.costHi ?? 0).toFixed(2) + " ESTIMATE"],
          ["Wall time", sel.baseline.wall === null ? "not measured" : fmtMin(sel.baseline.wall), sel.tool_loop.wall === null ? "not measured" : fmtMin(sel.tool_loop.wall), "not measured"]
        ]} />
        <Table columns={["Test", "Baseline", "Tool-loop"]} emphasis={2} rows={sel.baseline.tests.map((row, i) => [row.id, labelCell(row.label), labelCell(sel.tool_loop.tests[i]?.label ?? "not_measured")])} />
      </Section>
      <Section heading="Step-by-step" caption="A Page stands in for scrollytelling with a step control. One claim per step. All figures are synthetic.">
        <Segmented options={STORY.map((s) => ({ value: s.id, label: s.title }))} value={story} onChange={(x: StoryId) => setStory(x)} />
        <Text>{step.body}</Text>
        {story === "cost" ? <WaterfallChart /> : story === "left" ? <HeroCard title="Cases passed" unit="of 4 tickets" max={4} bars={[{ label: "Baseline", value: 1, display: "1", kind: "old" }, { label: "Tool-loop", value: 2, display: "2", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} /> : <ScoreCost />}
      </Section>
      <Section heading="Sources">
        <LinkCards links={[
          { title: "Introducing SWE-2.1", site: "Cognition", href: "https://cognition.com/blog/swe-2-1" },
          { title: "FrontierCode leaderboard", site: "Cognition", href: "https://cognition.com/frontiercode" },
          { title: "Introducing Claude Sonnet 5.5", site: "Anthropic", href: "https://www.anthropic.com/claude-sonnet-5-5" },
          { title: "CursorBench 4.1", site: "Cursor", href: "https://cursor.com/cursorbench" },
          { title: "FT Visual Vocabulary", site: "Financial Times", href: "https://ft-interactive.github.io/visual-vocabulary/" },
          { title: "Communicating with Interactive Articles", site: "Distill", href: "https://distill.pub/2020/communicating-with-interactive-articles/" },
          { title: "Making Internet Things, part 3: Storytelling", site: "The Pudding", href: "https://pudding.cool/process/how-to-make-dope-shit-part-3/" }
        ]} />
        <Text>Chart numbers are invented and live in examples/chart_data.json, built by scripts/make_chart_data.py from examples/raw_results.json. The full style catalogue, including leaderboards, bump charts and Our World in Data timelines, is in references/STYLES.md. Chart style follows the Cognition SWE-2.1 post: https://cognition.com/blog/swe-2-1</Text>
      </Section>
      <Callout lead="These figures are synthetic.">TicketFix-4 is a made-up bench for trying the kit. Do not treat the numbers as a real eval.</Callout>
    </Page>
  );
}
