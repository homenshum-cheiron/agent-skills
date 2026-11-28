#!/usr/bin/env python3
"""Lint a canvas .tsx for the premium-interactive chart standard.

Usage: check_premium.py PAGE.tsx [--primitives references/premium-primitives.tsx] [--json]
Exit 0 when every rule passes, 1 on any failure, 2 on bad usage.
Rules are listed in references/PREMIUM-INTERACTIVE.md (ids P1..P14). Warnings never fail the run.
"""
import argparse, json, re, sys
from pathlib import Path

KIT_CHARTS = ("Bars", "Columns", "LineChart", "Pie", "StackedBars", "ColumnSeries", "Scatter", "Heatmap", "CalendarHeatmap", "Matrix2x2", "Venn")
CONTROLS = ("<Segmented", "<Select", "<Toggle", "aria-pressed")
JUNK = [
    (r"linear-gradient|radial-gradient|<linearGradient|<radialGradient", "gradient"),
    (r"boxShadow|box-shadow|drop-shadow|textShadow|text-shadow", "shadow"),
    (r"filter:\s*['\"]?blur|feGaussianBlur", "blur filter"),
    (r"perspective\(|rotateX\(|rotateY\(|preserve-3d", "3-D effect"),
]
HEX_COLOR = re.compile(r"""(?:fill|stroke|color|background|stopColor)\s*[=:]\s*\{?\s*["'](#[0-9a-fA-F]{3,8}|rgba?\(|hsla?\()""")


def functions(src):
    """Yield (name, start_line, body) for top-level `function Name(` blocks."""
    lines = src.split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(r"(export\s+default\s+)?function\s+\w+", l)]
    tops = [i for i, l in enumerate(lines) if re.match(r"(export\s|function\s|const\s|type\s|let\s|// ====)", l)]
    for s in starts:
        end = next((t for t in tops if t > s), len(lines))
        name = re.match(r"(?:export\s+default\s+)?function\s+(\w+)", lines[s]).group(1)
        yield name, s + 1, "\n".join(lines[s:end])


def check(src, primitives=None):
    fails, warns = [], []
    def fail(rule, line, msg): fails.append({"rule": rule, "line": line, "msg": msg})
    def warn(rule, line, msg): warns.append({"rule": rule, "line": line, "msg": msg})

    charts = []
    for name, line, body in functions(src):
        if "/* pi:primitive */" in body:
            continue
        if "<svg" in body:
            charts.append((name, line, body))

    uses_frame = "<ChartFrame" in src or "<FlowGraph" in src
    for name, line, body in charts:
        framed = "<ChartFrame" in body or "<FlowGraph" in body
        for m in re.finditer(r"<svg\b[^>]*>", body, re.S):
            tag = m.group(0)
            if 'aria-hidden="true"' in tag:
                continue
            if "aria-label" not in tag:
                fail("P9", line, f"{name}: <svg> has no aria-label")
            if re.search(r'\swidth=\{?["\']?\d', tag) and 'width="100%"' not in tag:
                fail("P10", line, f"{name}: <svg> has a fixed pixel width; use width=\"100%\" and a viewBox")
            if "viewBox" not in tag:
                fail("P10", line, f"{name}: <svg> has no viewBox")
        if not (framed or 'role="tooltip"' in body):
            fail("P1", line, f"{name}: no tooltip (wrap the chart in <ChartFrame> or render role=\"tooltip\")")
        if not ("{...mark(" in body or re.search(r"onMouseEnter|onPointerMove|onPointerEnter", body)):
            fail("P2", line, f"{name}: data marks have no hover handler (spread {{...mark(c, tip)}} on each mark)")
        if not ("{...mark(" in body or ("tabIndex" in body and "onKeyDown" in body)):
            fail("P7", line, f"{name}: marks are not keyboard-focusable (tabIndex plus onKeyDown, or mark())")
        if not ("{...mark(" in body or "pin(" in body or "onClick" in body):
            fail("P4", line, f"{name}: no click-to-pin")
        if not ("source:" in body or "source=" in body or "<FlowGraph" in body):
            fail("P1", line, f"{name}: tooltip rows carry no source")
        if not re.search(r"grow\(|fade\(|transition", body):
            fail("P5", line, f"{name}: no enter animation or transition")
        if re.search(r"ESTIMATE|est:\s*true|kind === \"est\"|\.est\b", body) and not re.search(r"hatchDef\(|<pattern|strokeDasharray", body):
            fail("P11", line, f"{name}: estimates are not hatched or dashed")
        if not ("isActive(" in body or "border.focus" in body or "Crosshair" in body):
            warn("P3", line, f"{name}: no visible active or focus ring on marks")

    if charts or uses_frame:
        if "prefers-reduced-motion" not in src:
            fail("P5", 0, "no prefers-reduced-motion handling (include useReducedMotion)")
        for needle, rule, msg in [
            ('role="tooltip"', "P1", "no tooltip element"),
            ("aria-pressed", "P6", "no series toggles (aria-pressed buttons)"),
            ("aria-live", "P7", "no live region announcing the active value"),
            ('"Escape"', "P4", "no Escape to unpin"),
            ("clipboard", "P12", "no Copy data action"),
            ("Show data", "P12", "no Show data table fallback"),
        ]:
            if needle not in src:
                fail(rule, 0, msg)

    if re.search(r"<Diagram\b", src) and "pi:allow-static-diagram" not in src:
        for m in re.finditer(r"<Diagram\b", src):
            fail("P13", src[:m.start()].count("\n") + 1, "static <Diagram>; node graphs use <FlowGraph> (pan, zoom, drag, collapse, details, Back)")

    for pat, what in JUNK:
        for m in re.finditer(pat, src):
            fail("P14", src[:m.start()].count("\n") + 1, f"chart junk: {what}")
    for m in HEX_COLOR.finditer(src):
        ln = src[:m.start()].count("\n") + 1
        if "palette" in src.split("\n")[ln - 1]:
            continue
        fail("P8", ln, f"hard-coded colour {m.group(1)}; take colours from useGrokTheme()")

    for k in KIT_CHARTS:
        for m in re.finditer(r"<%s\b" % k, src):
            ln = src[:m.start()].count("\n") + 1
            window = "\n".join(src.split("\n")[max(0, ln - 12): ln + 3])
            if not any(c in window for c in CONTROLS):
                warn("P6", ln, f"kit <{k}> has no view control nearby; add a Segmented or Select if the reader would explore")

    if primitives is not None:
        block = primitives.strip()
        if "// ==== PI:BEGIN" in src:
            a = src.index("// ==== PI:BEGIN"); b = src.find("// ==== PI:END", a)
            got = src[a:b + len("// ==== PI:END ====")].strip() if b >= 0 else ""
            if got != block:
                fail("P0", src[:a].count("\n") + 1, "PI:BEGIN..PI:END block differs from references/premium-primitives.tsx; re-paste it")
        elif uses_frame:
            warn("P0", 0, "primitives not marked with PI:BEGIN/PI:END; drift cannot be checked")
    return fails, warns


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("page")
    ap.add_argument("--primitives", help="premium-primitives.tsx to compare the PI block against")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    p = Path(a.page)
    if not p.is_file():
        print(f"no such file: {p}", file=sys.stderr); return 2
    prim = Path(a.primitives).read_text() if a.primitives else None
    fails, warns = check(p.read_text(), prim)
    if a.json:
        print(json.dumps({"file": str(p), "ok": not fails, "fails": fails, "warnings": warns}, indent=2))
    else:
        for f in fails: print(f"FAIL {f['rule']} {p}:{f['line']}: {f['msg']}")
        for w in warns: print(f"warn {w['rule']} {p}:{w['line']}: {w['msg']}")
        print(f"{'ok' if not fails else 'FAILED'}: {len(fails)} failures, {len(warns)} warnings")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
