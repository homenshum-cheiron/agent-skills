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
