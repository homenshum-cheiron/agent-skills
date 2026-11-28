// Benchmark chart template for WriteCanvas, premium-interactive by default.
// Import only from grok/canvas. Custom charts are components that return divs and SVG,
// wrapped in ChartFrame; kit blocks (Metrics, Segmented, Table, Heatmap, Text) stay directly in Page or Section.
// Replace the DATA constants with the contract JSON from make_chart_data.py.
// The PI:BEGIN..PI:END block is references/premium-primitives.tsx verbatim; check_premium.py checks it has not drifted.
// Source of these demo numbers: examples/chart_data.json, built from examples/raw_results.json.

import { Page, Section, Text, Callout, Table, Segmented, TableOfContents, Grid, LinkCards, Metrics, Heatmap, Fragment, useState, useEffect, useMemo, useRef, useGrokTheme, computeDAGLayout } from "grok/canvas";
import type { ReactNode, CSSProperties, KeyboardEvent, PointerEvent } from "grok/canvas";

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


// ==== PI:BEGIN premium-interactive primitives (paste whole block; see references/PREMIUM-INTERACTIVE.md) ====
// Needs from grok/canvas: useState, useEffect, useMemo, useRef, useGrokTheme, computeDAGLayout,
// and the types ReactNode, CSSProperties, KeyboardEvent, PointerEvent.
type GT = ReturnType<typeof useGrokTheme>;
type TipRow = [string, string];
type Tip = { key: string; x: number; y: number; title: string; rows: TipRow[]; source: string; est?: boolean; series?: string };
type SeriesKey = { id: string; label: string; color: string; est?: boolean; dashed?: boolean };
type CsvData = { columns: string[]; rows: (string | number)[][] };
type Chart = {
  hidden: Record<string, boolean>;
  toggle: (id: string) => void;
  isOn: (id: string) => boolean;
  active: Tip | null;
  pinned: Tip | null;
  hover: (tip: Tip | null) => void;
  pin: (tip: Tip) => void;
  unpin: () => void;
  dim: (series: string, key?: string) => number;
  reduced: boolean;
  entered: boolean;
};

const ENTER_MS = 520;

function useReducedMotion(): boolean {
  /* pi:primitive */
  const [reduced, setReduced] = useState<boolean>(false);
  useEffect(() => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(mq.matches);
    const onChange = (e: { matches: boolean }) => setReduced(e.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);
  return reduced;
}

function useChart(seriesIds: string[]): Chart {
  /* pi:primitive */
  const reduced = useReducedMotion();
  const [hidden, setHidden] = useState<Record<string, boolean>>({});
  const [hov, setHov] = useState<Tip | null>(null);
  const [pinned, setPinned] = useState<Tip | null>(null);
  const [entered, setEntered] = useState<boolean>(false);
  useEffect(() => {
    const id = window.requestAnimationFrame(() => setEntered(true));
    return () => window.cancelAnimationFrame(id);
  }, []);
  const active = pinned ?? hov;
  const visible = seriesIds.filter((s: string) => !hidden[s]).length;
  return {
    hidden,
    // Never hide the last visible series: a chart is never empty.
    toggle: (id: string) => setHidden((h: Record<string, boolean>) => (!h[id] && visible <= 1 ? h : { ...h, [id]: !h[id] })),
    isOn: (id: string) => !hidden[id],
    active,
    pinned,
    hover: (tip: Tip | null) => setHov(tip),
    pin: (tip: Tip) => setPinned((p: Tip | null) => (p && p.key === tip.key ? null : tip)),
    unpin: () => setPinned(null),
    dim: (series: string, key?: string) => {
      if (!active) return 1;
      if (key !== undefined && active.key === key) return 1;
      return active.series === series ? 0.9 : 0.3;
    },
    reduced,
    entered: entered || reduced
  };
}

// Spread onto the <g> of one data mark: hover, focus, click-to-pin, Enter/Space/Escape, aria.
function mark(c: Chart, tip: Tip) {
  return {
    tabIndex: 0,
    role: "button" as const,
    "aria-label": `${tip.title}: ${tip.rows.map((r: TipRow) => `${r[0]} ${r[1]}`).join(", ")}${tip.est ? ", ESTIMATE" : ""}. Source: ${tip.source}`,
    "aria-pressed": c.pinned !== null && c.pinned.key === tip.key,
    onMouseEnter: () => c.hover(tip),
    onMouseLeave: () => c.hover(null),
    onFocus: () => c.hover(tip),
    onBlur: () => c.hover(null),
    onClick: () => c.pin(tip),
    onKeyDown: (e: KeyboardEvent<SVGGElement>) => {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); c.pin(tip); }
      else if (e.key === "Escape") c.unpin();
    },
    style: { cursor: "pointer", outline: "none" } as CSSProperties
  };
}

function isActive(c: Chart, key: string): boolean { return c.active !== null && c.active.key === key; }

// Enter animation: marks grow from their baseline, staggered; off under reduced motion.
function grow(c: Chart, t: GT, axis: "x" | "y", i: number, opacity?: number): CSSProperties {
  return {
    transformBox: "fill-box",
    transformOrigin: axis === "x" ? "left center" : "center bottom",
    transform: c.entered ? "scale(1, 1)" : axis === "x" ? "scale(0, 1)" : "scale(1, 0)",
    opacity: opacity ?? 1,
    transition: c.reduced ? "none" : `transform ${ENTER_MS}ms ${t.motion.easing} ${i * 45}ms, opacity ${t.motion.hover} ${t.motion.easing}`
  };
}
function fade(c: Chart, t: GT, i: number, opacity?: number): CSSProperties {
  return {
    opacity: c.entered ? opacity ?? 1 : 0,
    transition: c.reduced ? "none" : `opacity ${ENTER_MS}ms ${t.motion.easing} ${i * 45}ms`
  };
}

// Pointer position in viewBox units (the svg is width 100% with a viewBox).
function toVB(e: PointerEvent<SVGRectElement>, W: number, H: number): [number, number] {
  const svg = e.currentTarget.ownerSVGElement;
  if (!svg) return [0, 0];
  const r = svg.getBoundingClientRect();
  return [((e.clientX - r.left) / Math.max(1, r.width)) * W, ((e.clientY - r.top) / Math.max(1, r.height)) * H];
}

// Transparent hit area: nearest point (2-D, or x-only for time series) within maxR viewBox units.
function NearestLayer(props: { c: Chart; tips: Tip[]; x: number; y: number; w: number; h: number; W: number; H: number; mode?: "xy" | "x"; maxR?: number }) {
  /* pi:primitive */
  const pick = (e: PointerEvent<SVGRectElement>): Tip | null => {
    const [px, py] = toVB(e, props.W, props.H);
    let best: Tip | null = null, bd = props.maxR ?? 90;
    for (const tp of props.tips) {
      const d = props.mode === "x" ? Math.abs(tp.x - px) : Math.hypot(tp.x - px, tp.y - py);
      if (d < bd) { bd = d; best = tp; }
    }
    return best;
  };
  return (
    <rect x={props.x} y={props.y} width={props.w} height={props.h} fill="transparent" aria-hidden="true"
      onPointerMove={(e: PointerEvent<SVGRectElement>) => props.c.hover(pick(e))}
      onPointerLeave={() => props.c.hover(null)}
      onPointerDown={(e: PointerEvent<SVGRectElement>) => { const p = pick(e); if (p) props.c.pin(p); }} />
  );
}

// Dashed crosshair through the active mark, clipped to the plot area.
function Crosshair(props: { c: Chart; x0: number; x1: number; y0: number; y1: number }) {
  /* pi:primitive */
  const t = useGrokTheme();
  const a = props.c.active;
  if (!a || a.x < props.x0 || a.x > props.x1) return null;
  return (
    <g aria-hidden="true" pointerEvents="none">
      <line x1={a.x} x2={a.x} y1={props.y0} y2={props.y1} stroke={t.text.tertiary} strokeDasharray="3 4" />
      <line x1={props.x0} x2={props.x1} y1={a.y} y2={a.y} stroke={t.text.tertiary} strokeDasharray="3 4" />
    </g>
  );
}

// Hatch for estimates: <defs>{hatchDef(t, "id")}</defs>, then fill="url(#id)". Always label ESTIMATE too.
function hatchDef(t: GT, id: string, color?: string) {
  return (
    <pattern id={id} width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke={color ?? t.dataviz.categorical[0]} strokeWidth="2" opacity="0.6" />
    </pattern>
  );
}

function csvOf(d: CsvData): string {
  const cell = (v: string | number) => { const s = String(v); return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
  return [d.columns, ...d.rows].map((r: (string | number)[]) => r.map(cell).join(",")).join("\n");
}

// Wraps one custom chart: series toggles, tooltip with exact values and source, pinned detail,
// live region, hint line, Show data table and Copy CSV. Divs only, so the page keeps its rhythm.
function ChartFrame(props: { label: string; c: Chart; vb: [number, number]; series?: SeriesKey[]; data: CsvData; hint?: string; children?: ReactNode }) {
  /* pi:primitive */
  const t = useGrokTheme();
  const [showData, setShowData] = useState<boolean>(false);
  const [status, setStatus] = useState<string>("");
  const a = props.c.active;
  const [W, H] = props.vb;
  const say = (msg: string) => { setStatus(msg); window.setTimeout(() => setStatus(""), 2200); };
  const copy = () => {
    const text = csvOf(props.data);
    try {
      if (typeof navigator !== "undefined" && navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
        navigator.clipboard.writeText(text).then(() => say("Copied CSV"), () => { setShowData(true); say("Copy is blocked here; the table is shown instead"); });
      } else { setShowData(true); say("Copy is unavailable here; the table is shown instead"); }
    } catch (_e) { setShowData(true); say("Copy is unavailable here; the table is shown instead"); }
  };
  const btn = (on: boolean): CSSProperties => ({
    display: "inline-flex", alignItems: "center", gap: 6, padding: "4px 10px", borderRadius: t.radius.full,
    border: `1px solid ${on ? t.border.strong : t.border.subtle}`, background: on ? t.fill.secondary : "transparent",
    color: on ? t.text.primary : t.text.tertiary, fontFamily: t.font.family, fontSize: t.font.label.fontSize, lineHeight: t.font.label.lineHeight,
    cursor: "pointer", transition: props.c.reduced ? "none" : `background ${t.motion.hover} ${t.motion.easing}, color ${t.motion.hover} ${t.motion.easing}`
  });
  const left = a ? Math.min(80, Math.max(20, (a.x / W) * 100)) : 0;
  const top = a ? Math.min(100, Math.max(0, (a.y / H) * 100)) : 0;
  const below = top < 34;
  return (
    <div role="group" aria-label={props.label} style={{ position: "relative", fontFamily: t.font.family }}
      onKeyDown={(e: KeyboardEvent<HTMLDivElement>) => { if (e.key === "Escape") props.c.unpin(); }}>
      {props.series && props.series.length > 1 ? (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 12 }} aria-label="Series">
          {props.series.map((s: SeriesKey) => {
            const on = props.c.isOn(s.id);
            return (
              <button key={s.id} type="button" aria-pressed={on} onClick={() => props.c.toggle(s.id)} style={btn(on)}>
                <svg width="14" height="10" viewBox="0 0 14 10" aria-hidden="true">
                  <defs>{hatchDef(t, `sw-${s.id}`, s.color)}</defs>
                  <rect x="0.5" y="0.5" width="13" height="9" rx="2" fill={s.est ? `url(#sw-${s.id})` : on ? s.color : "transparent"} stroke={s.color} strokeDasharray={s.dashed || s.est ? "2 2" : undefined} />
                </svg>
                {s.label}
              </button>
            );
          })}
        </div>
      ) : null}
      <div style={{ position: "relative" }}>
        {props.children}
        {a ? (
          <div role="tooltip" style={{
            position: "absolute", left: `${left}%`, top: `${top}%`, zIndex: 3,
            transform: below ? "translate(-50%, 16px)" : "translate(-50%, calc(-100% - 16px))",
            pointerEvents: props.c.pinned ? "auto" : "none", minWidth: 180, maxWidth: 300,
            background: t.bg.elevated, border: `1px solid ${props.c.pinned ? t.border.strong : t.border.default}`, borderRadius: t.radius.md,
            padding: "10px 12px", color: t.text.primary
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "baseline" }}>
              <span style={{ fontSize: t.font.body2.fontSize, lineHeight: t.font.body2.lineHeight, fontWeight: t.weight.semibold }}>{a.title}</span>
              {a.est ? <span style={{ fontFamily: t.font.mono, fontSize: t.font.caption.fontSize, color: t.text.secondary, border: `1px dashed ${t.border.strong}`, borderRadius: t.radius.sm, padding: "0 4px" }}>ESTIMATE</span> : null}
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "auto auto", columnGap: 16, rowGap: 2, marginTop: 6 }}>
              {a.rows.map((r: TipRow) => (
                <Fragment key={r[0]}>
                  <span style={{ fontSize: t.font.label.fontSize, color: t.text.secondary }}>{r[0]}</span>
                  <span style={{ fontFamily: t.font.mono, fontSize: t.font.label.fontSize, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>{r[1]}</span>
                </Fragment>
              ))}
            </div>
            <div style={{ marginTop: 6, fontSize: t.font.caption.fontSize, lineHeight: t.font.caption.lineHeight, color: t.text.tertiary }}>Source: {a.source}</div>
            {props.c.pinned ? (
              <button type="button" onClick={() => props.c.unpin()} style={{ ...btn(false), marginTop: 8 }}>Unpin (Esc)</button>
            ) : null}
          </div>
        ) : null}
      </div>
      <div aria-live="polite" style={{ position: "absolute", width: 1, height: 1, overflow: "hidden", clip: "rect(0 0 0 0)", whiteSpace: "nowrap" }}>
        {a ? `${a.title}. ${a.rows.map((r: TipRow) => `${r[0]} ${r[1]}`).join(". ")}${a.est ? ". ESTIMATE" : ""}` : ""}
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12, alignItems: "center" }}>
        <span style={{ fontSize: t.font.caption.fontSize, color: t.text.tertiary, marginRight: "auto" }}>{props.hint ?? "Hover or Tab to a mark for exact values. Click or Enter pins it; Esc unpins."}</span>
        <button type="button" aria-expanded={showData} onClick={() => setShowData(!showData)} style={btn(showData)}>{showData ? "Hide data" : "Show data"}</button>
        <button type="button" onClick={copy} style={btn(false)}>Copy CSV</button>
        {status ? <span role="status" style={{ fontSize: t.font.caption.fontSize, color: t.text.secondary }}>{status}</span> : null}
      </div>
      {showData ? (
        <div style={{ overflowX: "auto", marginTop: 8 }}>
          <table style={{ borderCollapse: "collapse", fontSize: t.font.label.fontSize, color: t.text.primary }}>
            <thead><tr>{props.data.columns.map((h: string, i: number) => <th key={h} style={{ textAlign: i === 0 ? "left" : "right", padding: "4px 10px", color: t.text.secondary, fontWeight: t.weight.medium, borderBottom: `1px solid ${t.border.default}` }}>{h}</th>)}</tr></thead>
            <tbody>{props.data.rows.map((r: (string | number)[], ri: number) => <tr key={ri}>{r.map((v: string | number, ci: number) => <td key={ci} style={{ textAlign: ci === 0 ? "left" : "right", padding: "4px 10px", fontFamily: ci === 0 ? t.font.family : t.font.mono, borderBottom: `1px solid ${t.border.subtle}` }}>{String(v)}</td>)}</tr>)}</tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}

// React Flow-style node graph: drag the background to pan, drag nodes, +/-/Fit zoom
// (Ctrl or Cmd + wheel too), collapsible groups, hover highlights neighbours,
// click opens details with neighbour links, Back walks the selection history.
type FlowNode = { id: string; label: string; detail?: string; group?: string; source?: string; est?: boolean };
type FlowEdge = { from: string; to: string; label?: string; dashed?: boolean };
type FlowGroup = { id: string; label: string };
function FlowGraph(props: { label: string; nodes: FlowNode[]; edges: FlowEdge[]; groups?: FlowGroup[]; hulls?: boolean; height?: number; direction?: "vertical" | "horizontal" }) {
  /* pi:primitive */
  const t = useGrokTheme();
  const reduced = useReducedMotion();
  const W = 1240, H = props.height ?? 560, NW = 176, NH = 52;
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});
  const [moved, setMoved] = useState<Record<string, [number, number]>>({});
  const [view, setView] = useState<{ x: number; y: number; k: number }>({ x: 0, y: 0, k: 1 });
  const [hover, setHover] = useState<string>("");
  const [sel, setSel] = useState<string>("");
  const [hist, setHist] = useState<string[]>([]);
  const drag = useRef<{ kind: "pan" | "node"; id: string; sx: number; sy: number; ox: number; oy: number; dist: number } | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const groupOf = (id: string): string | undefined => props.nodes.find((n: FlowNode) => n.id === id)?.group;
  const vis = (id: string): string => { const g = groupOf(id); return g && collapsed[g] ? `group:${g}` : id; };
  const graph = useMemo(() => {
    const ns: FlowNode[] = [];
    const seen: Record<string, boolean> = {};
    for (const n of props.nodes) {
      const v = vis(n.id);
      if (seen[v]) continue;
      seen[v] = true;
      if (v === n.id) ns.push(n);
      else {
        const g = (props.groups ?? []).find((x: FlowGroup) => `group:${x.id}` === v);
        const members = props.nodes.filter((m: FlowNode) => m.group === n.group);
        ns.push({ id: v, label: g ? g.label : v, detail: `${members.length} steps collapsed: ${members.map((m: FlowNode) => m.label).join(", ")}`, group: n.group });
      }
    }
    const es: FlowEdge[] = [];
    const ek: Record<string, boolean> = {};
    for (const e of props.edges) {
      const a = vis(e.from), b = vis(e.to);
      if (a === b || ek[`${a}>${b}`]) continue;
      ek[`${a}>${b}`] = true;
      es.push({ ...e, from: a, to: b });
    }
    const lay = computeDAGLayout({ nodes: ns.map((n: FlowNode) => ({ id: n.id })), edges: es.map((e: FlowEdge) => ({ from: e.from, to: e.to })), direction: props.direction ?? "vertical", nodeWidth: NW, nodeHeight: NH, rankGap: 64, nodeGap: 28, padding: 24 });
    const pos: Record<string, [number, number]> = {};
    for (const p of lay.nodes) pos[p.id] = [p.x, p.y];
    return { ns, es, pos, w: Math.max(lay.width, NW + 48), h: Math.max(lay.height, NH + 48) };
  }, [collapsed, props.nodes, props.edges]);
  const at = (id: string): [number, number] => moved[id] ?? graph.pos[id] ?? [0, 0];
  const fit = () => { const k = Math.min(1.4, Math.min(W / graph.w, H / graph.h) * 0.92); setView({ k, x: (W - graph.w * k) / 2, y: (H - graph.h * k) / 2 }); };
  useEffect(() => { fit(); }, [graph.w, graph.h]);
  const zoom = (f: number) => setView((v: { x: number; y: number; k: number }) => { const k = Math.min(2.5, Math.max(0.3, v.k * f)); return { k, x: W / 2 - ((W / 2 - v.x) * k) / v.k, y: H / 2 - ((H / 2 - v.y) * k) / v.k }; });
  const scale = (): number => { const r = svgRef.current?.getBoundingClientRect(); return r && r.width > 0 ? W / r.width : 1; };
  const select = (id: string) => { if (id === sel) return; if (sel) setHist((h: string[]) => [...h, sel]); setSel(id); };
  const back = () => { setHist((h: string[]) => { const prev = h[h.length - 1]; setSel(prev ?? ""); return h.slice(0, -1); }); };
  const onDown = (kind: "pan" | "node", id: string) => (e: PointerEvent<SVGElement>) => {
    (e.currentTarget as Element).setPointerCapture?.((e.nativeEvent as unknown as { pointerId: number }).pointerId);
    const [ox, oy] = kind === "pan" ? [view.x, view.y] : at(id);
    drag.current = { kind, id, sx: e.clientX, sy: e.clientY, ox, oy, dist: 0 };
    e.stopPropagation();
  };
  const onMove = (e: PointerEvent<SVGElement>) => {
    const d = drag.current; if (!d) return;
    const s = scale(), dx = (e.clientX - d.sx) * s, dy = (e.clientY - d.sy) * s;
    d.dist = Math.max(d.dist, Math.hypot(dx, dy));
    if (d.kind === "pan") setView((v: { x: number; y: number; k: number }) => ({ ...v, x: d.ox + dx, y: d.oy + dy }));
    else setMoved((m: Record<string, [number, number]>) => ({ ...m, [d.id]: [d.ox + dx / view.k, d.oy + dy / view.k] }));
  };
  const onUp = () => { const d = drag.current; drag.current = null; if (d && d.kind === "node" && d.dist < 4) select(d.id); if (d && d.kind === "pan" && d.dist < 4) setSel(""); };
  const near = (id: string): boolean => !hover || hover === id || graph.es.some((e: FlowEdge) => (e.from === hover && e.to === id) || (e.to === hover && e.from === id));
  const selNode = graph.ns.find((n: FlowNode) => n.id === sel);
  const ins = graph.es.filter((e: FlowEdge) => e.to === sel).map((e: FlowEdge) => e.from);
  const outs = graph.es.filter((e: FlowEdge) => e.from === sel).map((e: FlowEdge) => e.to);
  const labelOf = (id: string): string => graph.ns.find((n: FlowNode) => n.id === id)?.label ?? id;
  const btn: CSSProperties = { padding: "4px 10px", borderRadius: t.radius.full, border: `1px solid ${t.border.subtle}`, background: "transparent", color: t.text.secondary, fontFamily: t.font.family, fontSize: t.font.label.fontSize, cursor: "pointer" };
  const groups = props.groups ?? [];
  const ease = reduced ? "none" : `opacity ${t.motion.hover} ${t.motion.easing}`;
  return (
    <div role="group" aria-label={props.label} style={{ fontFamily: t.font.family }}
      onKeyDown={(e: KeyboardEvent<HTMLDivElement>) => {
        if (e.key === "+" || e.key === "=") zoom(1.2); else if (e.key === "-") zoom(1 / 1.2); else if (e.key === "0") fit();
        else if (e.key === "Escape") setSel(""); else if (e.key === "Backspace" && hist.length) { e.preventDefault(); back(); }
      }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 10, alignItems: "center" }}>
        <button type="button" style={btn} onClick={() => zoom(1.2)} aria-label="Zoom in">+</button>
        <button type="button" style={btn} onClick={() => zoom(1 / 1.2)} aria-label="Zoom out">−</button>
        <button type="button" style={btn} onClick={() => { setMoved({}); fit(); }}>Fit and reset</button>
        <button type="button" style={{ ...btn, opacity: hist.length ? 1 : 0.4 }} disabled={!hist.length} onClick={back}>Back</button>
        {groups.map((g: FlowGroup) => (
          <button key={g.id} type="button" aria-pressed={!collapsed[g.id]} style={{ ...btn, color: collapsed[g.id] ? t.text.tertiary : t.text.primary, borderColor: collapsed[g.id] ? t.border.subtle : t.border.strong }}
            onClick={() => setCollapsed((c: Record<string, boolean>) => ({ ...c, [g.id]: !c[g.id] }))}>{collapsed[g.id] ? `Expand ${g.label}` : `Collapse ${g.label}`}</button>
        ))}
      </div>
      <svg ref={svgRef} width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label={`${props.label}. Drag to pan, Tab to nodes, Enter for details.`}
        style={{ touchAction: "none", border: `1px solid ${t.border.subtle}`, borderRadius: t.radius.lg }}
        onPointerMove={onMove} onPointerUp={onUp} onPointerLeave={onUp}
        onWheel={(e: { ctrlKey: boolean; metaKey: boolean; deltaY: number; preventDefault: () => void }) => { if (e.ctrlKey || e.metaKey) { e.preventDefault(); zoom(e.deltaY < 0 ? 1.1 : 1 / 1.1); } }}>
        <defs>
          <marker id="fg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9" fill="none" stroke={t.text.tertiary} strokeWidth="1.5" /></marker>
          <pattern id="fg-dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill={t.border.subtle} /></pattern>
          {hatchDef(t, "fg-hatch")}
        </defs>
        <rect x="0" y="0" width={W} height={H} fill="url(#fg-dots)" style={{ cursor: drag.current ? "grabbing" : "grab" }} onPointerDown={onDown("pan", "")} />
        <g transform={`translate(${view.x} ${view.y}) scale(${view.k})`}>
          {groups.filter((g: FlowGroup) => (props.hulls ?? true) && !collapsed[g.id]).map((g: FlowGroup) => {
            const ps = graph.ns.filter((n: FlowNode) => n.group === g.id).map((n: FlowNode) => at(n.id));
            if (!ps.length) return null;
            const x0 = Math.min(...ps.map((p: [number, number]) => p[0])) - NW / 2 - 14, x1 = Math.max(...ps.map((p: [number, number]) => p[0])) + NW / 2 + 14;
            const y0 = Math.min(...ps.map((p: [number, number]) => p[1])) - NH / 2 - 26, y1 = Math.max(...ps.map((p: [number, number]) => p[1])) + NH / 2 + 12;
            return (
              <g key={g.id} aria-hidden="true">
                <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} rx={14} fill={t.fill.secondary} opacity="0.5" stroke={t.border.subtle} />
                <text x={x0 + 12} y={y0 + 17} fontSize="12" fill={t.text.tertiary}>{g.label}</text>
              </g>
            );
          })}
          {graph.es.map((e: FlowEdge) => {
            const [ax, ay] = at(e.from), [bx, by] = at(e.to);
            const vert = (props.direction ?? "vertical") === "vertical";
            const sx = vert ? ax : ax + NW / 2, sy = vert ? ay + NH / 2 : ay, tx = vert ? bx : bx - NW / 2 - 6, ty = vert ? by - NH / 2 - 6 : by;
            const d = vert ? `M ${sx} ${sy} C ${sx} ${(sy + ty) / 2}, ${tx} ${(sy + ty) / 2}, ${tx} ${ty}` : `M ${sx} ${sy} C ${(sx + tx) / 2} ${sy}, ${(sx + tx) / 2} ${ty}, ${tx} ${ty}`;
            const lit = hover !== "" && (e.from === hover || e.to === hover);
            return (
              <g key={`${e.from}>${e.to}`} style={{ opacity: !hover || lit ? 1 : 0.18, transition: ease }} aria-hidden="true">
                <path d={d} fill="none" stroke={lit ? t.dataviz.categorical[0] : t.text.tertiary} strokeWidth={lit ? 2.2 : 1.5} strokeDasharray={e.dashed ? "5 4" : undefined} markerEnd="url(#fg-arrow)" />
                {e.label ? <text x={(sx + tx) / 2 + 8} y={(sy + ty) / 2} fontSize="11" fill={t.text.tertiary}>{e.label}</text> : null}
              </g>
            );
          })}
          {graph.ns.map((n: FlowNode) => {
            const [x, y] = at(n.id);
            const on = sel === n.id, grp = n.id.startsWith("group:");
            return (
              <g key={n.id} tabIndex={0} role="button" aria-pressed={on} aria-label={`${n.label}${n.detail ? `: ${n.detail}` : ""}${n.est ? ", ESTIMATE" : ""}`}
                style={{ cursor: "grab", outline: "none", opacity: near(n.id) ? 1 : 0.3, transition: ease }}
                onPointerDown={onDown("node", n.id)} onMouseEnter={() => setHover(n.id)} onMouseLeave={() => setHover("")}
                onFocus={() => setHover(n.id)} onBlur={() => setHover("")}
                onKeyDown={(e: KeyboardEvent<SVGGElement>) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); if (grp && n.group) setCollapsed((c: Record<string, boolean>) => ({ ...c, [n.group as string]: false })); else select(n.id); } }}
                onDoubleClick={() => { if (grp && n.group) setCollapsed((c: Record<string, boolean>) => ({ ...c, [n.group as string]: false })); }}>
                <title>{n.label}</title>
                <rect x={x - NW / 2} y={y - NH / 2} width={NW} height={NH} rx={grp ? 20 : 10} fill={n.est ? "url(#fg-hatch)" : t.bg.base}
                  stroke={on || hover === n.id ? t.border.focus : grp ? t.border.strong : t.border.default} strokeWidth={on || hover === n.id ? 2 : 1} strokeDasharray={grp || n.est ? "5 3" : undefined} />
                <rect x={x - NW / 2} y={y - NH / 2 + 8} width={3} height={NH - 16} rx={1.5} fill={on ? t.dataviz.categorical[0] : t.dataviz.other} />
                <text x={x - NW / 2 + 14} y={y - 3} fontSize="13" fontWeight={600} fill={t.text.primary}>{n.label.length > 22 ? `${n.label.slice(0, 21)}…` : n.label}</text>
                <text x={x - NW / 2 + 14} y={y + 14} fontSize="11" fill={t.text.tertiary}>{grp ? "Enter or double-click to expand" : n.est ? "ESTIMATE" : (n.detail ?? "").slice(0, 26)}</text>
              </g>
            );
          })}
        </g>
      </svg>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 8, fontSize: t.font.caption.fontSize, color: t.text.tertiary }}>
        <span>Drag the background to pan and a node to move it. Ctrl or Cmd + wheel zooms; + − 0 on the keyboard too. Click a node for details.</span>
      </div>
      {selNode ? (
        <div aria-live="polite" style={{ marginTop: 10, padding: "12px 14px", border: `1px solid ${t.border.default}`, borderRadius: t.radius.md }}>
          <div style={{ fontSize: t.font.body2.fontSize, fontWeight: t.weight.semibold, color: t.text.primary }}>{selNode.label}{selNode.est ? " · ESTIMATE" : ""}</div>
          {selNode.detail ? <div style={{ fontSize: t.font.label.fontSize, color: t.text.secondary, marginTop: 4 }}>{selNode.detail}</div> : null}
          {selNode.source ? <div style={{ fontSize: t.font.caption.fontSize, color: t.text.tertiary, marginTop: 4 }}>Source: {selNode.source}</div> : null}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8, alignItems: "center" }}>
            {ins.length ? <span style={{ fontSize: t.font.caption.fontSize, color: t.text.tertiary }}>From</span> : null}
            {ins.map((id: string) => <button key={`in-${id}`} type="button" style={btn} onClick={() => select(id)}>{labelOf(id)}</button>)}
            {outs.length ? <span style={{ fontSize: t.font.caption.fontSize, color: t.text.tertiary }}>To</span> : null}
            {outs.map((id: string) => <button key={`out-${id}`} type="button" style={btn} onClick={() => select(id)}>{labelOf(id)}</button>)}
          </div>
        </div>
      ) : null}
    </div>
  );
}
// ==== PI:END ====

const SRC = "examples/chart_data.json";
const ARM_SERIES = (t: GT): SeriesKey[] => [
  { id: "baseline", label: "Baseline agent", color: t.dataviz.other },
  { id: "tool_loop", label: "Tool-loop agent", color: t.dataviz.categorical[0] },
  { id: "compact", label: "Compact-context (ESTIMATE)", color: t.dataviz.categorical[0], est: true }
];

function HeroCard(props: { title: string; unit: string; field: string; bars: { label: string; value: number | null; display: string; kind: Kind }[]; max: number }) {
  const t = useGrokTheme();
  const c = useChart(props.bars.map((b) => b.label));
  const W = 400, H = 230, base = 180, top = 34, bw = 82, gap = 34, x0 = (W - (3 * bw + 2 * gap)) / 2;
  const hid = `hatch-${props.field}`;
  return (
    <ChartFrame label={`${props.title}, ${props.unit}`} c={c} vb={[W, H]} hint="Hover, Tab or tap a bar. Click pins it."
      data={{ columns: ["Arm", props.title], rows: props.bars.map((b) => [b.label, b.display]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label={`${props.title}: ${props.bars.map((b) => `${b.label} ${b.display}`).join(", ")}`}>
        <defs>{hatchDef(t, hid)}</defs>
        <line x1="8" x2={W - 8} y1={base} y2={base} stroke={t.border.default} strokeWidth="1" />
        {props.bars.map((b, i) => {
          const x = x0 + i * (bw + gap);
          const tip: Tip = { key: b.label, x: x + bw / 2, y: base - (b.value === null ? 60 : Math.max(3, (b.value / props.max) * (base - top))), title: `${b.label} · ${props.title}`, rows: [[props.unit, b.display]], source: `${SRC} · headline.${props.field}`, est: b.kind === "est", series: b.label };
          const on = isActive(c, b.label);
          if (b.value === null) {
            return (
              <g key={b.label} {...mark(c, tip)} opacity={c.dim(b.label, b.label)} style={{ ...mark(c, tip).style, ...fade(c, t, i, c.dim(b.label, b.label)) }}>
                <rect x={x} y={base - 60} width={bw} height={60} fill="none" stroke={on ? t.border.focus : t.text.tertiary} strokeWidth={on ? 2 : 1} strokeDasharray="4 4" />
                <text x={x + bw / 2} y={base - 26} textAnchor="middle" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>{b.display}</text>
                <text x={x + bw / 2} y={base + 20} textAnchor="middle" fontSize="13" fill={t.text.secondary}>{b.label}</text>
              </g>
            );
          }
          const h = Math.max(3, (b.value / props.max) * (base - top));
          const fill = b.kind === "res" ? t.dataviz.categorical[0] : b.kind === "old" ? t.dataviz.other : `url(#${hid})`;
          return (
            <g key={b.label} {...mark(c, tip)} style={{ ...mark(c, tip).style, opacity: c.dim(b.label, b.label), transition: c.reduced ? "none" : `opacity ${t.motion.hover} ${t.motion.easing}` }}>
              <rect x={x - 6} y={top - 10} width={bw + 12} height={base - top + 34} fill="transparent" />
              <rect x={x} y={base - h} width={bw} height={h} rx={3} fill={fill} stroke={on ? t.border.focus : b.kind === "est" ? t.dataviz.categorical[0] : "none"} strokeWidth={on ? 2 : 1} strokeDasharray={b.kind === "est" && !on ? "4 3" : undefined} style={grow(c, t, "y", i)} />
              <text x={x + bw / 2} y={base - h - 8} textAnchor="middle" fontFamily={t.font.mono} fontSize="15" fontWeight={b.kind === "res" ? 600 : 400} fill={t.text.primary} style={fade(c, t, i + 2)}>{b.display}</text>
              <text x={x + bw / 2} y={base + 20} textAnchor="middle" fontSize="13" fill={b.kind === "res" ? t.text.primary : t.text.secondary}>{b.label}</text>
            </g>
          );
        })}
        <text x={W / 2} y={H - 6} textAnchor="middle" fontSize="11" fill={t.text.tertiary}>{props.unit}</text>
      </svg>
    </ChartFrame>
  );
}

function ScoreCost() {
  const t = useGrokTheme();
  const c = useChart(["baseline", "tool_loop", "compact"]);
  const W = 1240, H = 420, L = 80, R = 40, T = 70, B = 60;
  const lx = (v: number) => L + ((Math.log10(v) - Math.log10(1)) / (Math.log10(40) - Math.log10(1))) * (W - L - R);
  const ly = (m: number) => T + (1 - m / 4) * (H - T - B);
  const ticksX = [1, 2, 5, 10, 20, 40];
  const ticksY = [0, 1, 2, 3, 4];
  const old = { x: lx(17.5), y: ly(1) }, res = { x: lx(4.17), y: ly(2) };
  const laneY = 36;
  const allTips: Tip[] = [
    { key: "baseline", series: "baseline", x: old.x, y: old.y, title: "Baseline agent (1 Oct)", rows: [["Cases passed", "1 / 4"], ["Cost, 4 cases", "$17.50"], ["Wall time", "44.0 min"]], source: `${SRC} · arms.baseline` },
    { key: "tool_loop", series: "tool_loop", x: res.x, y: res.y, title: "Tool-loop agent (15 Oct)", rows: [["Cases passed", "2 / 4"], ["Cost, 4 cases", "$4.17"], ["Wall time", "14.6 min"]], source: `${SRC} · arms.tool_loop` },
    { key: "compact", series: "compact", x: (lx(3.0) + lx(3.95)) / 2, y: laneY, title: "Compact-context design", rows: [["Cases passed", "not measured"], ["Cost, 4 cases", "$3.00–$3.95"]], source: `${SRC} · arms.compact.cost_range`, est: true }
  ];
  const tips: Tip[] = allTips.filter((p: Tip) => c.isOn(p.series ?? ""));
  return (
    <ChartFrame label="Cases passed versus four-case cost" c={c} vb={[W, H]} series={ARM_SERIES(t)}
      data={{ columns: ["Arm", "Cases passed", "Cost USD", "Kind"], rows: [["Baseline agent", 1, 17.5, "measured"], ["Tool-loop agent", 2, 4.17, "measured"], ["Compact-context", "not measured", "3.00-3.95", "ESTIMATE"]] }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Cases passed versus four-case cost, log scale. Up and to the left is better.">
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill={t.text.tertiary} /></marker>
          {hatchDef(t, "sc-hatch")}
        </defs>
        {ticksY.map((m) => (<g key={m}><line x1={L} x2={W - R} y1={ly(m)} y2={ly(m)} stroke={t.border.subtle} /><text x={L - 12} y={ly(m) + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>{m}</text></g>))}
        {ticksX.map((v) => (<g key={v}><line x1={lx(v)} x2={lx(v)} y1={T} y2={H - B} stroke={t.border.subtle} /><text x={lx(v)} y={H - B + 22} textAnchor="middle" fontFamily={t.font.mono} fontSize="12" fill={t.text.tertiary}>${v}</text></g>))}
        <text x={(L + W - R) / 2} y={H - 12} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Whole-harness cost for the four cases (log scale)</text>
        <text x={18} y={T - 14} fontSize="12" fill={t.text.secondary}>Cases passed (of 4) · up and to the left is better</text>
        <Crosshair c={c} x0={L} x1={W - R} y0={T} y1={H - B} />
        {c.isOn("baseline") && c.isOn("tool_loop") ? (
          <g style={fade(c, t, 4)}>
            <line x1={old.x} y1={old.y} x2={res.x + 10} y2={res.y + 8} stroke={t.text.tertiary} strokeDasharray="5 4" markerEnd="url(#arr)" />
            <text x={(old.x + res.x) / 2 + 20} y={(old.y + res.y) / 2 - 14} textAnchor="middle" fontSize="13" fill={t.text.secondary}>76.2% cheaper, +1 case passed</text>
          </g>
        ) : null}
        {c.isOn("baseline") ? (
          <g {...mark(c, tips[0])} style={{ ...mark(c, tips[0]).style, ...fade(c, t, 0, c.dim("baseline", "baseline")) }}>
            <circle cx={old.x} cy={old.y} r={isActive(c, "baseline") ? 12 : 9} fill={t.dataviz.other} stroke={isActive(c, "baseline") ? t.border.focus : "none"} strokeWidth="2" />
            <text x={old.x + 14} y={old.y + 22} fontSize="14" fill={t.text.primary}>Baseline agent (1 Oct)</text>
            <text x={old.x + 14} y={old.y + 40} fontFamily={t.font.mono} fontSize="13" fill={t.text.secondary}>1 / 4 · $17.50</text>
          </g>
        ) : null}
        {c.isOn("tool_loop") ? (
          <g {...mark(c, tips.find((p: Tip) => p.key === "tool_loop") ?? tips[0])} style={{ cursor: "pointer", outline: "none", ...fade(c, t, 1, c.dim("tool_loop", "tool_loop")) }}>
            <circle cx={res.x} cy={res.y} r={isActive(c, "tool_loop") ? 14 : 11} fill={t.dataviz.categorical[0]} stroke={isActive(c, "tool_loop") ? t.border.focus : "none"} strokeWidth="2" />
            <text x={res.x - 16} y={res.y - 18} textAnchor="end" fontSize="14" fontWeight={600} fill={t.text.primary}>Tool-loop agent (15 Oct)</text>
            <text x={res.x - 16} y={res.y - 2} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.secondary}>2 / 4 · $4.17</text>
          </g>
        ) : null}
        {c.isOn("compact") ? (
          <g {...mark(c, tips[tips.length - 1])} style={{ cursor: "pointer", outline: "none", ...fade(c, t, 2, c.dim("compact", "compact")) }}>
            <rect x={lx(3.0)} y={laneY - 9} width={lx(3.95) - lx(3.0)} height={18} fill="url(#sc-hatch)" stroke={isActive(c, "compact") ? t.border.focus : t.dataviz.categorical[0]} strokeDasharray="4 3" />
            <line x1={lx(3.0)} x2={lx(3.0)} y1={laneY + 9} y2={H - B} stroke={t.dataviz.categorical[0]} strokeDasharray="2 5" opacity="0.6" />
            <line x1={lx(3.95)} x2={lx(3.95)} y1={laneY + 9} y2={H - B} stroke={t.dataviz.categorical[0]} strokeDasharray="2 5" opacity="0.6" />
            <text x={lx(3.95) + 10} y={laneY - 2} fontSize="13" fontWeight={600} fill={t.text.primary}>Compact-context: ESTIMATE</text>
            <text x={lx(3.95) + 10} y={laneY + 15} fontFamily={t.font.mono} fontSize="12" fill={t.text.secondary}>$3.00–$3.95 · score not measured</text>
          </g>
        ) : null}
        <NearestLayer c={c} tips={tips} x={L} y={T - 40} w={W - L - R} h={H - B - T + 40} W={W} H={H} />
      </svg>
    </ChartFrame>
  );
}

function LatencyBars() {
  const t = useGrokTheme();
  const c = useChart(["baseline", "tool_loop"]);
  const W = 1240, rowH = 64, L = 150, R = 150, T = 10;
  const H = T + CASES.length * rowH + 10;
  const max = 1000;
  const sx = (s: number) => (s / max) * (W - L - R);
  return (
    <ChartFrame label="Wall time per case" c={c} vb={[W, H]} series={ARM_SERIES(t).slice(0, 2)}
      data={{ columns: ["Case", "Baseline s", "Tool-loop s", "Speed-up"], rows: CASES.map((cs) => [cs.id, cs.baseline.wall ?? "not measured", cs.tool_loop.wall ?? "not measured", `${((cs.baseline.wall ?? 0) / (cs.tool_loop.wall ?? 1)).toFixed(1)}x`]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Wall time per case, baseline versus tool-loop">
        {CASES.map((cs, i) => {
          const y = T + i * rowH;
          const speed = ((cs.baseline.wall ?? 0) / (cs.tool_loop.wall ?? 1)).toFixed(1);
          const arms: { arm: "baseline" | "tool_loop"; dy: number; color: string; v: number }[] = [
            { arm: "baseline", dy: 6, color: t.dataviz.other, v: cs.baseline.wall ?? 0 },
            { arm: "tool_loop", dy: 30, color: t.dataviz.categorical[0], v: cs.tool_loop.wall ?? 0 }
          ];
          return (
            <g key={cs.id}>
              <text x={L - 14} y={y + 26} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{cs.id}</text>
              {arms.filter((a) => c.isOn(a.arm)).map((a, j) => {
                const key = `${cs.id}-${a.arm}`;
                const tip: Tip = { key, series: a.arm, x: L + sx(a.v), y: y + a.dy, title: `${cs.id} · ${a.arm === "baseline" ? "Baseline" : "Tool-loop"}`, rows: [["Wall time", fmtMin(a.v)], ["Seconds", String(a.v)], ["Speed-up", `${speed}×`]], source: `${SRC} · cases[${cs.id}].${a.arm}.wall` };
                return (
                  <g key={key} {...mark(c, tip)} style={{ ...mark(c, tip).style, opacity: c.dim(a.arm, key), transition: c.reduced ? "none" : `opacity ${t.motion.hover} ${t.motion.easing}` }}>
                    <rect x={L} y={y + a.dy - 2} width={W - L - R} height={24} fill="transparent" />
                    <rect x={L} y={y + a.dy} width={sx(a.v)} height={20} rx={3} fill={a.color} stroke={isActive(c, key) ? t.border.focus : "none"} strokeWidth="2" style={grow(c, t, "x", i * 2 + j)} />
                    <text x={L + sx(a.v) + 8} y={y + a.dy + 15} fontFamily={t.font.mono} fontSize="12" fontWeight={a.arm === "tool_loop" ? 600 : 400} fill={a.arm === "tool_loop" ? t.text.primary : t.text.secondary}>{fmtMin(a.v)}</text>
                  </g>
                );
              })}
              <text x={W - 10} y={y + 33} textAnchor="end" fontFamily={t.font.mono} fontSize="14" fill={t.text.primary}>{speed}× faster</text>
            </g>
          );
        })}
      </svg>
    </ChartFrame>
  );
}

function StageBars(props: { mode: StageView }) {
  const t = useGrokTheme();
  const c = useChart(["planner", "worker", "tools"]);
  const W = 1240, rowH = 64, L = 150, R = 200, T = 8;
  const H = T + CASES.length * rowH + 6;
  const colors: Record<string, string> = { planner: t.dataviz.categorical[1], worker: t.dataviz.categorical[0], tools: t.dataviz.categorical[2] };
  const max = props.mode === "tokens" ? 1_800_000 : props.mode === "time" ? 1000 : 8;
  const sx = (v: number) => (v / max) * (W - L - R);
  const fmt = (v: number) => (props.mode === "tokens" ? `${(v / 1000).toFixed(0)}k tok` : props.mode === "time" ? `${v}s` : fmtUsd(v));
  const parts = (r: ArmResult) => (props.mode === "tokens" ? r.tokens : props.mode === "time" ? r.time : r.costParts);
  const stages = ["planner", "worker", "tools"] as const;
  const series: SeriesKey[] = stages.map((s) => ({ id: s, label: s[0].toUpperCase() + s.slice(1), color: colors[s] }));
  return (
    <ChartFrame label={`Breakdown by stage, ${props.mode}`} c={c} vb={[W, H]} series={series}
      data={{ columns: ["Case", "Arm", "Planner", "Worker", "Tools"], rows: CASES.flatMap((cs) => (["baseline", "tool_loop"] as const).map((arm) => { const p = parts(cs[arm]); return [cs.id, arm, p ? p.planner : "not measured", p ? p.worker : "not measured", p ? p.tools : "not measured"]; })) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label={`Breakdown by stage, ${props.mode}, baseline row above tool-loop row`}>
        {CASES.map((cs, i) => {
          const y = T + i * rowH;
          return (
            <g key={cs.id}>
              <text x={L - 14} y={y + 22} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{cs.id}</text>
              {(["baseline", "tool_loop"] as const).map((arm, j) => {
                const p = parts(cs[arm]);
                if (!p) return null;
                let acc = 0;
                const dy = j === 0 ? 6 : 28;
                const total = stages.filter((s) => c.isOn(s)).reduce((sum: number, s) => sum + p[s], 0);
                return (
                  <g key={arm} opacity={arm === "baseline" ? 0.72 : 1}>
                    {stages.filter((s) => c.isOn(s)).map((s, k) => {
                      const x = L + sx(acc); acc += p[s];
                      const key = `${cs.id}-${arm}-${s}`;
                      const tip: Tip = { key, series: s, x: x + sx(p[s]) / 2, y: y + dy, title: `${cs.id} · ${arm === "baseline" ? "Baseline" : "Tool-loop"} · ${s}`, rows: [[props.mode, fmt(p[s])], ["Share of row", `${((p[s] / Math.max(1e-9, total)) * 100).toFixed(0)}%`]], source: `${SRC} · cases[${cs.id}].${arm}.${props.mode === "cost" ? "costParts" : props.mode}.${s}` };
                      return (
                        <g key={key} {...mark(c, tip)} style={{ ...mark(c, tip).style, opacity: c.dim(s, key), transition: c.reduced ? "none" : `opacity ${t.motion.hover} ${t.motion.easing}` }}>
                          <rect x={x} y={y + dy} width={Math.max(1, sx(p[s]))} height={18} fill={colors[s]} stroke={isActive(c, key) ? t.border.focus : "none"} strokeWidth="2" style={grow(c, t, "x", i * 3 + k)} />
                        </g>
                      );
                    })}
                    <text x={L + sx(total) + 8} y={y + dy + 14} fontFamily={t.font.mono} fontSize="12" fontWeight={arm === "tool_loop" ? 600 : 400} fill={arm === "tool_loop" ? t.text.primary : t.text.secondary}>{fmt(total)} {arm === "baseline" ? "baseline" : "tool-loop"}</text>
                  </g>
                );
              })}
            </g>
          );
        })}
      </svg>
    </ChartFrame>
  );
}

function DumbbellPlot() {
  const t = useGrokTheme();
  const c = useChart(["baseline", "tool_loop"]);
  const W = 1240, rowH = 56, L = 150, R = 80, T = 8;
  const H = T + CASES.length * rowH + 8;
  const max = 8;
  const sx = (v: number) => L + (v / max) * (W - L - R);
  const tips: Tip[] = CASES.flatMap((cs, i) => {
    const y = T + i * rowH + 28;
    const a = cs.baseline.cost ?? 0, b = cs.tool_loop.cost ?? 0;
    const saving = `${fmtUsd(a - b)} (${(((a - b) / Math.max(1e-9, a)) * 100).toFixed(0)}%)`;
    return [
      { key: `${cs.id}-baseline`, series: "baseline", x: sx(a), y, title: `${cs.id} · Baseline`, rows: [["Cost", fmtUsd(a)], ["Saving vs tool-loop", saving]] as TipRow[], source: `${SRC} · cases[${cs.id}].baseline.cost` },
      { key: `${cs.id}-tool_loop`, series: "tool_loop", x: sx(b), y, title: `${cs.id} · Tool-loop`, rows: [["Cost", fmtUsd(b)], ["Saving vs baseline", saving]] as TipRow[], source: `${SRC} · cases[${cs.id}].tool_loop.cost` }
    ];
  }).filter((p: Tip) => c.isOn(p.series ?? ""));
  return (
    <ChartFrame label="Cost per case, baseline to tool-loop" c={c} vb={[W, H]} series={ARM_SERIES(t).slice(0, 2)}
      data={{ columns: ["Case", "Baseline USD", "Tool-loop USD"], rows: CASES.map((cs) => [cs.id, cs.baseline.cost ?? "not measured", cs.tool_loop.cost ?? "not measured"]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Cost per case, baseline to tool-loop, one row per case">
        {CASES.map((cs, i) => {
          const y = T + i * rowH + 28;
          const a = cs.baseline.cost ?? 0, b = cs.tool_loop.cost ?? 0;
          return (
            <g key={cs.id} style={fade(c, t, i)}>
              <text x={L - 14} y={y + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{cs.id}</text>
              {c.isOn("baseline") && c.isOn("tool_loop") ? <line x1={sx(b)} x2={sx(a)} y1={y} y2={y} stroke={t.dataviz.other} strokeWidth="3" /> : null}
            </g>
          );
        })}
        {tips.map((p: Tip, i: number) => (
          <g key={p.key} {...mark(c, p)} style={{ ...mark(c, p).style, ...fade(c, t, i, c.dim(p.series ?? "", p.key)) }}>
            <circle cx={p.x} cy={p.y} r={isActive(c, p.key) ? 11 : p.series === "tool_loop" ? 8 : 7} fill={p.series === "tool_loop" ? t.dataviz.categorical[0] : t.dataviz.other} stroke={isActive(c, p.key) ? t.border.focus : "none"} strokeWidth="2" />
            <text x={p.series === "tool_loop" ? p.x - 12 : p.x + 12} y={p.y - 12} textAnchor={p.series === "tool_loop" ? "end" : "start"} fontFamily={t.font.mono} fontSize="12" fontWeight={p.series === "tool_loop" ? 600 : 400} fill={p.series === "tool_loop" ? t.text.primary : t.text.secondary}>{p.rows[0][1]}</text>
          </g>
        ))}
        <NearestLayer c={c} tips={tips} x={L} y={T} w={W - L - R} h={H - T * 2} W={W} H={H} maxR={40} />
      </svg>
    </ChartFrame>
  );
}

function SlopeChart() {
  const t = useGrokTheme();
  const c = useChart(CASES.map((cs) => cs.id));
  const W = 1240, H = 360, L = 180, R = 180, T = 28, B = 36;
  const x0 = L, x1 = W - R;
  const ly = (v: number) => T + (1 - (v - 3) / 5) * (H - T - B);
  const series: SeriesKey[] = CASES.map((cs) => ({ id: cs.id, label: cs.id, color: t.dataviz.categorical[0] }));
  return (
    <ChartFrame label="Tests passed per case, baseline to tool-loop" c={c} vb={[W, H]} series={series}
      data={{ columns: ["Case", "Baseline passed", "Tool-loop passed", "Tests"], rows: CASES.map((cs) => [cs.id, cs.baseline.passed ?? "not measured", cs.tool_loop.passed ?? "not measured", cs.baseline.n ?? "not measured"]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Tests passed per case, baseline to tool-loop, one line per case">
        <line x1={x0} x2={x0} y1={T} y2={H - B} stroke={t.border.default} />
        <line x1={x1} x2={x1} y1={T} y2={H - B} stroke={t.border.default} />
        <text x={x0} y={H - 8} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Baseline</text>
        <text x={x1} y={H - 8} textAnchor="middle" fontSize="12" fill={t.text.secondary}>Tool-loop</text>
        {CASES.filter((cs) => c.isOn(cs.id)).map((cs, i) => {
          const a = cs.baseline.passed ?? 0, b = cs.tool_loop.passed ?? 0;
          const y0 = ly(a), y1 = ly(b);
          const tip: Tip = { key: cs.id, series: cs.id, x: x1, y: y1, title: `${cs.id} · ${cs.label}`, rows: [["Baseline", `${a} / ${cs.baseline.n}`], ["Tool-loop", `${b} / ${cs.tool_loop.n}`], ["Change", `${b - a >= 0 ? "+" : ""}${b - a} tests`]], source: `${SRC} · cases[${cs.id}].*.passed` };
          const on = isActive(c, cs.id);
          return (
            <g key={cs.id} {...mark(c, tip)} style={{ ...mark(c, tip).style, ...fade(c, t, i, c.dim(cs.id, cs.id)) }}>
              <line x1={x0} x2={x1} y1={y0} y2={y1} stroke="transparent" strokeWidth="16" />
              <line x1={x0} x2={x1} y1={y0} y2={y1} stroke={t.dataviz.categorical[0]} strokeWidth={on ? 3.5 : 2} />
              <circle cx={x0} cy={y0} r={on ? 8 : 6} fill={t.dataviz.other} />
              <circle cx={x1} cy={y1} r={on ? 8 : 6} fill={t.dataviz.categorical[0]} stroke={on ? t.border.focus : "none"} strokeWidth="2" />
              <text x={x0 - 12} y={y0 + 4} textAnchor="end" fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{cs.id} {a}/{cs.baseline.n}</text>
              <text x={x1 + 12} y={y1 + 4} fontFamily={t.font.mono} fontSize="13" fill={t.text.primary}>{b}/{cs.tool_loop.n}</text>
            </g>
          );
        })}
      </svg>
    </ChartFrame>
  );
}

function WaterfallChart() {
  const t = useGrokTheme();
  const c = useChart(["steps"]);
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
    const height = s.kind === "delta" ? Math.abs(s.value) : s.value;
    const y = s.kind === "delta" && s.value < 0 ? base - sy(running) : base - sy(s.kind === "delta" ? running + s.value : s.value);
    const before = running;
    if (s.kind === "delta") running += s.value;
    return { ...s, x: x0 + i * (bw + gap), y, height: sy(height), before, after: running };
  });
  return (
    <ChartFrame label="Cost waterfall from baseline to tool-loop" c={c} vb={[W, H]}
      data={{ columns: ["Step", "USD"], rows: steps.map((s) => [s.label, s.value]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label="Cost waterfall from baseline to tool-loop: planner, worker and tools savings">
        <line x1={L} x2={W - R} y1={base} y2={base} stroke={t.border.default} />
        {placed.map((s, i) => {
          const fill = s.kind === "start" ? t.dataviz.other : s.kind === "end" ? t.dataviz.categorical[0] : t.dataviz.categorical[1];
          const label = s.kind === "delta" ? `−${fmtUsd(Math.abs(s.value))}` : fmtUsd(s.value);
          const prev = placed[i - 1];
          const tip: Tip = { key: s.label, series: "steps", x: s.x + bw / 2, y: s.y, title: s.kind === "delta" ? `${s.label} saving` : `${s.label} total`, rows: s.kind === "delta" ? [["Change", label], ["Running total", `${fmtUsd(s.before)} → ${fmtUsd(s.after)}`], ["Share of cut", `${((Math.abs(s.value) / 13.33) * 100).toFixed(0)}%`]] : [["Total, 4 cases", label]], source: `${SRC} · waterfall.${s.label.toLowerCase()}` };
          return (
            <g key={s.label} {...mark(c, tip)} style={{ ...mark(c, tip).style, opacity: c.dim("steps", s.label), transition: c.reduced ? "none" : `opacity ${t.motion.hover} ${t.motion.easing}` }}>
              {prev ? <line x1={prev.x + bw} x2={s.x} y1={s.y} y2={s.y} stroke={t.text.tertiary} strokeDasharray="4 3" style={fade(c, t, i + 3)} /> : null}
              <rect x={s.x - 10} y={T - 20} width={bw + 20} height={base - T + 44} fill="transparent" />
              <rect x={s.x} y={s.y} width={bw} height={Math.max(3, s.height)} rx={3} fill={fill} stroke={isActive(c, s.label) ? t.border.focus : "none"} strokeWidth="2" style={grow(c, t, "y", i)} />
              <text x={s.x + bw / 2} y={s.y - 8} textAnchor="middle" fontFamily={t.font.mono} fontSize="14" fill={t.text.primary} style={fade(c, t, i + 2)}>{label}</text>
              <text x={s.x + bw / 2} y={base + 22} textAnchor="middle" fontSize="13" fill={t.text.secondary}>{s.label}</text>
            </g>
          );
        })}
      </svg>
    </ChartFrame>
  );
}

function SankeyFlow(props: { arm: "baseline" | "tool_loop" }) {
  const t = useGrokTheme();
  const c = useChart(["planner", "worker", "tools"]);
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
  const rights = right.map((r) => { const h = Math.max(10, r.v * scale); const y = acc; acc += h + 18; return { ...r, y, h }; });
  let lAcc = leftY;
  const links = rights.map((r) => { const y1 = lAcc; lAcc += r.h; return { ...r, y1 }; });
  return (
    <ChartFrame label={`${props.arm === "baseline" ? "Baseline" : "Tool-loop"} token flow`} c={c} vb={[W, H]} hint="Hover or Tab to a band."
      data={{ columns: ["Stage", "Tokens", "Share"], rows: right.map((r) => [r.name, r.v, `${((r.v / d.all) * 100).toFixed(1)}%`]) }}>
      <svg width="100%" viewBox={`0 0 ${W} ${H}`} role="group" aria-label={`${props.arm} token flow from total into planner, worker and tools`}>
        <rect x={xL} y={leftY} width={nodeW} height={leftH} fill={t.dataviz.other} />
        <text x={xL} y={leftY - 8} fontSize="12" fill={t.text.secondary}>Total {(d.all / 1000).toFixed(0)}k</text>
        {links.map((r, i) => {
          const y2 = rights[i].y;
          const path = `M ${xL + nodeW} ${r.y1} C ${(xL + xR) / 2} ${r.y1}, ${(xL + xR) / 2} ${y2}, ${xR} ${y2} L ${xR} ${y2 + r.h} C ${(xL + xR) / 2} ${y2 + r.h}, ${(xL + xR) / 2} ${r.y1 + r.h}, ${xL + nodeW} ${r.y1 + r.h} Z`;
          const tip: Tip = { key: r.name, series: r.name, x: (xL + xR) / 2, y: (r.y1 + y2) / 2 + r.h / 2, title: `${props.arm === "baseline" ? "Baseline" : "Tool-loop"} · ${r.name}`, rows: [["Tokens", `${(r.v / 1000).toFixed(0)}k`], ["Share", `${((r.v / d.all) * 100).toFixed(1)}%`]], source: `${SRC} · token_flow.${props.arm}.${r.name}` };
          return (
            <g key={r.name} {...mark(c, tip)} style={{ ...mark(c, tip).style, ...fade(c, t, i, isActive(c, r.name) ? 0.85 : c.active ? 0.2 : 0.55) }}>
              <path d={path} fill={r.color} stroke={isActive(c, r.name) ? t.border.focus : "none"} strokeWidth="1.5" />
              <rect x={xR} y={rights[i].y} width={nodeW} height={r.h} fill={r.color} />
              <text x={xR + nodeW + 8} y={rights[i].y + r.h / 2 + 4} fontSize="13" fill={t.text.primary}>{r.name} {(r.v / 1000).toFixed(0)}k</text>
            </g>
          );
        })}
      </svg>
    </ChartFrame>
  );
}

const PIPE_NODES: FlowNode[] = [
  { id: "ticket", label: "Ticket in", detail: "Frozen ticket text and repo snapshot", group: "intake", source: SRC },
  { id: "plan", label: "Planner", detail: "Writes a step plan; 18k–35k tokens per case", group: "intake", source: SRC },
  { id: "search", label: "Code search", detail: "Tool call: ripgrep over the snapshot", group: "loop", source: SRC },
  { id: "edit", label: "Worker edit", detail: "Patch proposal; most tokens land here", group: "loop", source: SRC },
  { id: "test", label: "Run tests", detail: "Per-case unit tests, 5–8 per ticket", group: "loop", source: SRC },
  { id: "compact", label: "Compact context", detail: "Proposed: trims history between loop turns", group: "loop", est: true, source: SRC },
  { id: "grade", label: "Grader", detail: "Same grader for every arm; per-test labels", group: "score", source: SRC },
  { id: "report", label: "Chart contract", detail: "make_chart_data.py output, embedded in this Page", group: "score", source: SRC }
];
const PIPE_EDGES: FlowEdge[] = [
  { from: "ticket", to: "plan" }, { from: "plan", to: "search" }, { from: "search", to: "edit" }, { from: "edit", to: "test" },
  { from: "test", to: "compact", label: "estimate", dashed: true }, { from: "compact", to: "search", dashed: true }, { from: "test", to: "grade" }, { from: "grade", to: "report" }
];

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
    <Page width="wide" title="TicketFix-4: tool-loop vs baseline" summary="A synthetic four-ticket issue-fixing bench used to prove the benchmark chart kit. Every chart is interactive: hover or Tab for exact values and sources, click to pin, toggle series, show or copy the data. All figures are invented. Last updated: Fri 27 Nov 2026, 3:46 PM PT.">
      <TableOfContents items={[{ label: "Headline numbers" }, { label: "Score vs cost" }, { label: "Latency per case" }, { label: "Cost dumbbells" }, { label: "Tests-passed slopes" }, { label: "Where the tokens, time and dollars go" }, { label: "Cost waterfall" }, { label: "Token flow" }, { label: "Pipeline graph" }, { label: "Test heatmap" }, { label: "Per-case results" }, { label: "Step-by-step" }, { label: "Sources" }]} />
      <Section heading="Headline numbers" caption="Four frozen tickets, same grader. Hatched or dashed marks are estimates. Cost and wall time are sums across cases, not a pooled score. Quality is cases passed.">
        <Text>The tool-loop agent passed one more case than the baseline, cost less, and took less wall time. A compact-context design has a cost estimate only; its score is not measured.</Text>
        <Metrics metrics={[{ value: "76.2%", label: "cheaper", detail: "$17.50 → $4.17, sum of case costs" }, { value: "66.8%", label: "less wall time", detail: "44.0 min → 14.6 min, sum of case wall times" }, { value: "2 vs 1", label: "cases passed of 4", detail: "the quality headline; per case below" }, { value: "not measured", label: "compact-context score", detail: "cost $3.00–$3.95 ESTIMATE" }]} />
        <Text>Gray bars: baseline agent (1 Oct). Blue bars: tool-loop agent (15 Oct). Hatched bars: compact-context design, an ESTIMATE.</Text>
        <Grid columns={3}>
          <Section heading="Cost, four cases">
            <HeroCard title="Cost" unit="USD, summed" field="cost" max={18} bars={[{ label: "Baseline", value: 17.5, display: "$17.50", kind: "old" }, { label: "Tool-loop", value: 4.17, display: "$4.17", kind: "res" }, { label: "Compact (EST)", value: 3.95, display: "$3.00–$3.95", kind: "est" }]} />
          </Section>
          <Section heading="Wall time, four cases">
            <HeroCard title="Wall time" unit="minutes, summed per case" field="wall" max={50} bars={[{ label: "Baseline", value: 44.0, display: "44.0 min", kind: "old" }, { label: "Tool-loop", value: 14.6, display: "14.6 min", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} />
          </Section>
          <Section heading="Cases passed">
            <HeroCard title="Cases passed" unit="of 4 tickets" field="cases" max={4} bars={[{ label: "Baseline", value: 1, display: "1", kind: "old" }, { label: "Tool-loop", value: 2, display: "2", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} />
          </Section>
        </Grid>
      </Section>
      <Section heading="Score vs cost" caption="Up and to the left is better. The compact-context design has a cost estimate only; its score is not measured.">
        <ScoreCost />
      </Section>
      <Section heading="Latency per case" caption="Wall time per case, first span to last.">
        <LatencyBars />
      </Section>
      <Section heading="Cost dumbbells" caption="One row per case. The gap is the saving.">
        <DumbbellPlot />
      </Section>
      <Section heading="Tests-passed slopes" caption="Two axes, one line per case. Nested test counts are shown as a per-case change, not as a pooled score.">
        <SlopeChart />
      </Section>
      <Section heading="Where the tokens, time and dollars go">
        <Segmented options={[{ value: "tokens", label: "Tokens by stage" }, { value: "time", label: "Time by stage" }, { value: "cost", label: "Dollars by stage" }]} value={stage} onChange={(x: StageView) => setStage(x)} />
        <Text>{stage === "time" ? "Top row per case is the baseline, bottom row is tool-loop. Stage seconds may overlap, so they need not sum to wall time." : "Top row per case is the baseline, bottom row is tool-loop. Toggle a stage to compare the rest."}</Text>
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
      <Section heading="Pipeline graph" caption="React Flow-style: pan, zoom, drag nodes, collapse groups, click a node for details, Back to retrace. The dashed node is a proposed step (ESTIMATE).">
        <FlowGraph label="TicketFix-4 agent pipeline" nodes={PIPE_NODES} edges={PIPE_EDGES} groups={[{ id: "intake", label: "Intake" }, { id: "loop", label: "Tool loop" }, { id: "score", label: "Scoring" }]} height={620} />
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
        {story === "cost" ? <WaterfallChart /> : story === "left" ? <HeroCard title="Cases passed" unit="of 4 tickets" field="story" max={4} bars={[{ label: "Baseline", value: 1, display: "1", kind: "old" }, { label: "Tool-loop", value: 2, display: "2", kind: "res" }, { label: "Compact", value: null, display: "not measured", kind: "est" }]} /> : <ScoreCost />}
      </Section>
      <Section heading="Sources">
        <LinkCards links={[
          { title: "Introducing SWE-2.1", site: "Cognition", href: "https://cognition.com/blog/swe-2-1" },
          { title: "FrontierCode leaderboard", site: "Cognition", href: "https://cognition.com/frontiercode" },
          { title: "Introducing Claude Sonnet 5.5", site: "Anthropic", href: "https://www.anthropic.com/claude-sonnet-5-5" },
          { title: "CursorBench 4.1", site: "Cursor", href: "https://cursor.com/cursorbench" },
          { title: "FT Visual Vocabulary", site: "Financial Times", href: "https://ft-interactive.github.io/visual-vocabulary/" },
          { title: "Communicating with Interactive Articles", site: "Distill", href: "https://distill.pub/2020/communicating-with-interactive-articles/" },
          { title: "Making Internet Things, part 3: Storytelling", site: "The Pudding", href: "https://pudding.cool/process/how-to-make-dope-shit-part-3/" },
          { title: "Pointer transform (nearest-point hover, click-to-stick)", site: "Observable Plot", href: "https://observablehq.github.io/plot/interactions/pointer" },
          { title: "Charts and graphs accessibility best practices", site: "ACCESSIBILITY.md", href: "https://mgifford.github.io/ACCESSIBILITY.md/examples/CHARTS_GRAPHS_ACCESSIBILITY_BEST_PRACTICES.html" },
          { title: "React Flow: pan, zoom, drag and sub-flows", site: "xyflow", href: "https://reactflow.dev/learn" }
        ]} />
        <Text>Chart numbers are invented and live in examples/chart_data.json, built by scripts/make_chart_data.py from examples/raw_results.json. The full style catalogue is in references/STYLES.md, and the interaction standard every chart here meets is references/PREMIUM-INTERACTIVE.md. Chart style follows the Cognition SWE-2.1 post: https://cognition.com/blog/swe-2-1</Text>
      </Section>
      <Callout lead="These figures are synthetic.">TicketFix-4 is a made-up bench for trying the kit. Do not treat the numbers as a real eval.</Callout>
    </Page>
  );
}
