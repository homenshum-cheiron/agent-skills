#!/usr/bin/env python3
"""Stage 1 of instruction-hygiene-review: a deterministic, offline scan.

Reads only the instruction and skill files you point it at. It makes no model
calls, no network calls, and does not read transcripts, configs or credentials.
Every finding is a candidate for a person or a fresh-context reviewer, not a verdict.

Configuration (flags win over environment variables):
  --root PATH            file or folder to scan; repeatable.
                         env INSTRUCTION_SCAN_ROOTS (os.pathsep-separated).
                         Default: common host locations under $HOME (see DEFAULT_ROOTS).
  --out DIR              report folder. env INSTRUCTION_SCAN_OUT.
                         Default: $HOME/.local/state/instruction-hygiene
  --limit NAME=BYTES     loader size limit for files with that base name; repeatable.
                         env INSTRUCTION_SCAN_LIMITS ("AGENTS.md=32768,CLAUDE.md=40000").
                         Default: AGENTS.md=32768. Check your host's current docs.
  --effort-cap LEVEL     highest allowed reasoning effort. env INSTRUCTION_SCAN_EFFORT_CAP.
                         Default: high.
  --today YYYY-MM-DD     date used for "past date" checks (tests); default local today.
  --dup-min N            report two files as duplicates only when they share at least N
                         long lines (default 3; one shared line is usually boilerplate).
  --fail-on-findings     exit 1 when any candidate is found (default exit 0).
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_ROOTS = [
    "~/.codex/AGENTS.md",
    "~/.claude/CLAUDE.md",
    "~/AGENTS.md",
    "~/.cursor/rules",
    "~/.claude/skills",
    "~/.codex/skills",
    "~/.agents/skills",
]
INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md", "SKILL.md", "GEMINI.md"}
EFFORTS = ["minimal", "low", "medium", "high", "xhigh", "max", "ultra"]
NEGATION = re.compile(r"\b(no|not|never|don'?t|do not|avoid|ban(?:ned)?|instead of|retired?|superseded|above|past|beyond)\b", re.I)
EFFORT_WORD = re.compile(r"\b(xhigh|max|ultra|high|medium|low|minimal)\b", re.I)
EFFORT_CONTEXT = re.compile(r"\b(effort|reasoning)\b", re.I)
PENDING = re.compile(r"\b(until|pending|decision needed|for now|temporar(?:y|ily)|TODO)\b", re.I)
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
HOME_PATH = re.compile(r"(?<![\w/])~/(?:[\w.-]+/)*[\w.-]+")
POLARITY = re.compile(r"`?([A-Za-z][\w.-]{2,40})`?\s*(?:is\s+|are\s+)?\b(banned|allowed|forbidden|permitted)\b", re.I)
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}


def parse_limits(values):
    limits = {"AGENTS.md": 32768}
    for item in values:
        for part in filter(None, (p.strip() for p in item.split(","))):
            name, _, size = part.partition("=")
            if not name or not size.isdigit():
                raise SystemExit(f"bad --limit value: {part!r} (want NAME=BYTES)")
            limits[name] = int(size)
    return limits


def is_instruction(path):
    return path.name in INSTRUCTION_NAMES or path.suffix in (".mdc",) or path.name.endswith(".rules.md")


def collect(roots):
    files, missing = [], []
    for raw in roots:
        root = Path(os.path.expanduser(raw))
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            for base, dirs, names in os.walk(root, followlinks=True):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                files.extend(Path(base) / n for n in sorted(names) if is_instruction(Path(base) / n))
        else:
            missing.append(str(root))
    seen, unique = set(), []
    for f in files:
        key = os.path.realpath(f)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique, missing


def effort_above_cap(line, cap):
    if not EFFORT_CONTEXT.search(line):
        return None
    cap_i = EFFORTS.index(cap)
    for m in EFFORT_WORD.finditer(line):
        level = m.group(1).lower()
        if EFFORTS.index(level) <= cap_i:
            continue
        before = line[max(0, m.start() - 40):m.start()]
        if before[-1:] in "\"'`\u201c":  # a quoted word is a mention, not a setting
            continue
        if NEGATION.search(before) or re.search(r"\bcap\b", before, re.I):
            continue
        return level
    return None


def scan(roots, limits, cap, today, home, dup_min=3):
    files, missing = collect(roots)
    findings, polarity, long_lines = [], {}, {}
    sizes = {}
    for path in files:
        try:
            size = path.stat().st_size
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append({"type": "unreadable", "path": str(path), "detail": type(exc).__name__})
            continue
        sizes[str(path)] = size
        limit = limits.get(path.name)
        if limit and size >= 0.9 * limit:
            findings.append({"type": "size-near-loader-limit", "path": str(path), "bytes": size, "limit": limit,
                             "detail": "over limit: tail is not loaded" if size > limit else "within 10% of limit"})
        for number, line in enumerate(text.splitlines(), 1):
            where = {"path": str(path), "line": number}
            level = effort_above_cap(line, cap)
            if level:
                findings.append(dict(where, type="effort-above-cap", level=level, cap=cap))
            dates = [d for d in DATE.findall(line) if d < today]
            if PENDING.search(line) and dates:
                findings.append(dict(where, type="stale-pending", dates=dates))
            for ref in HOME_PATH.findall(line):
                ref = ref.rstrip(".,;:")
                if "<" in ref or "*" in ref or ref.endswith(("-", "_")):
                    continue
                if not (home / ref[2:]).exists():
                    findings.append(dict(where, type="missing-path", reference=ref))
            for m in POLARITY.finditer(line):
                value = "banned" if m.group(2).lower() in ("banned", "forbidden") else "allowed"
                polarity.setdefault(m.group(1).lower(), {}).setdefault(value, []).append(where)
            stripped = line.strip()
            if len(stripped) >= 100:
                long_lines.setdefault(stripped, []).append(where)
    for subject, values in sorted(polarity.items()):
        if values.get("banned") and values.get("allowed"):
            findings.append({"type": "polarity-conflict", "subject": subject,
                             "banned": values["banned"][:5], "allowed": values["allowed"][:5]})
    pairs = {}
    for places in long_lines.values():
        paths = sorted({p["path"] for p in places})
        for i, first in enumerate(paths):
            for second in paths[i + 1:]:
                row = pairs.setdefault((first, second), {"shared_lines": 0, "first_line": None})
                row["shared_lines"] += 1
                if row["first_line"] is None:
                    row["first_line"] = next(p["line"] for p in places if p["path"] == first)
    for (first, second), row in sorted(pairs.items()):
        if row["shared_lines"] < dup_min:
            continue
        findings.append({"type": "duplicate-instruction", "path": first, "line": row["first_line"],
                         "also_in": second, "shared_long_lines": row["shared_lines"]})
    return {"files": sizes, "missing_roots": missing, "findings": findings}


def unique_name(out, stem):
    for n in range(0, 1000):
        suffix = "" if n == 0 else f"-{n}"
        md, js = out / f"{stem}{suffix}.md", out / f"{stem}{suffix}.json"
        if not md.exists() and not js.exists():
            return md, js
    raise SystemExit("too many reports for one day")


def render(record):
    counts = {}
    for f in record["findings"]:
        counts[f["type"]] = counts.get(f["type"], 0) + 1
    lines = [f"# Instruction hygiene scan · {record['date']}", "",
             f"Scanned {len(record['files'])} files. Candidates: {len(record['findings'])}. Effort cap: {record['effort_cap']}.",
             "Candidates are not verdicts. A fresh-context reviewer decides keep, retire, merge, or rewrite.", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(counts.items())] or ["- none"]
    if record["missing_roots"]:
        lines += ["", "Missing roots (not an error):"] + [f"- {m}" for m in record["missing_roots"]]
    lines += ["", "## Candidates", ""]
    for f in record["findings"][:200]:
        loc = f"{f['path']}:{f['line']}" if "line" in f else f.get("path", f.get("subject", ""))
        extra = {k: v for k, v in f.items() if k not in ("type", "path", "line")}
        lines.append(f"- **{f['type']}** {loc} {json.dumps(extra, sort_keys=True) if extra else ''}".rstrip())
    if len(record["findings"]) > 200:
        lines.append(f"- ... {len(record['findings']) - 200} more in the JSON file")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", action="append", default=[])
    ap.add_argument("--out")
    ap.add_argument("--limit", action="append", default=[])
    ap.add_argument("--effort-cap")
    ap.add_argument("--today")
    ap.add_argument("--dup-min", type=int, default=3)
    ap.add_argument("--fail-on-findings", action="store_true")
    a = ap.parse_args(argv)
    home = Path(os.path.expanduser("~"))
    env_roots = [r for r in os.environ.get("INSTRUCTION_SCAN_ROOTS", "").split(os.pathsep) if r]
    roots = a.root or env_roots or DEFAULT_ROOTS
    out = Path(os.path.expanduser(a.out or os.environ.get("INSTRUCTION_SCAN_OUT") or "~/.local/state/instruction-hygiene"))
    limits = parse_limits(a.limit or [os.environ.get("INSTRUCTION_SCAN_LIMITS", "")])
    cap = (a.effort_cap or os.environ.get("INSTRUCTION_SCAN_EFFORT_CAP") or "high").lower()
    if cap not in EFFORTS:
        raise SystemExit(f"unknown effort cap {cap!r}; use one of {', '.join(EFFORTS)}")
    today = a.today or dt.date.today().isoformat()
    result = scan(roots, limits, cap, today, home, a.dup_min)
    record = {"schema_version": 1, "date": today, "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
              "effort_cap": cap, "limits": limits, "roots": roots, **result}
    out.mkdir(parents=True, exist_ok=True)
    md, js = unique_name(out, f"instruction-scan-{today}")
    js.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    md.write_text(render(record))
    print(f"{md}\n{js}\nfiles={len(record['files'])} candidates={len(record['findings'])}")
    return 1 if (a.fail_on_findings and record["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
