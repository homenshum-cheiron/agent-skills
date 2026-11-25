#!/usr/bin/env python3
"""Fail (exit 1) if a worker brief is missing required parts.

Usage: lint_brief.py FILE|-
"""
import re
import sys

HEADINGS = [
    ("Job", re.compile(r"^#{1,3}\s+job\b", re.I)),
    ("Why", re.compile(r"^#{1,3}\s+why\b", re.I)),
    ("Guardrails", re.compile(r"^#{1,3}\s+guardrails?\b", re.I)),
    ("Done means", re.compile(r"^#{1,3}\s+done\s*(means|when|criteria)\b", re.I)),
]


def sections(text):
    lines = text.splitlines()
    found = {}
    order = []
    for i, line in enumerate(lines):
        for name, pat in HEADINGS:
            if name not in found and pat.match(line.strip()):
                found[name] = i
                order.append(name)
    # collect bodies until the next heading (any # heading)
    bodies = {}
    keys = sorted(found, key=lambda k: found[k])
    for i, name in enumerate(keys):
        start = found[name] + 1
        end = found[keys[i + 1]] if i + 1 < len(keys) else len(lines)
        # if another brief heading of a later type isn't next, still stop at next # of same or higher
        bodies[name] = "\n".join(lines[start:end]).strip()
    return found, bodies


def lint(text):
    errs = []
    found, bodies = sections(text)
    missing = [n for n, _ in HEADINGS if n not in found]
    if missing:
        errs.append(f"missing headings: {missing}")
        return errs
    order = [found[n] for n, _ in HEADINGS]
    if order != sorted(order):
        errs.append("headings out of order (want Job, Why, Guardrails, Done means)")
    why = re.sub(r"\s+", " ", bodies.get("Why", "")).strip()
    if len(why.split()) < 5:
        errs.append("Why is empty or too short")
    job = bodies.get("Job", "")
    job_lines = [l for l in job.splitlines() if l.strip()]
    numbered = [l for l in job_lines if re.match(r"\s*\d+[\.)]\s+", l)]
    if job_lines and len(numbered) / len(job_lines) > 0.5:
        errs.append("Job is more than half numbered how-to steps")
    guards = [l for l in bodies.get("Guardrails", "").splitlines() if re.match(r"\s*[-*]\s+", l)]
    if not guards:
        errs.append("Guardrails has no bullet items")
    else:
        for g in guards:
            if not re.search(r"\bbecause\b", g, re.I):
                errs.append(f"guardrail has no because: {g.strip()[:80]}")
    done = bodies.get("Done means", "")
    checks = [
        l for l in done.splitlines()
        if re.match(r"\s*[-*]\s+(\[[ xX]\]\s+)?", l) and re.search(
            r"\b(check|exit|pass|fail|equals|contains|run|lint|test|verify)\b", l, re.I
        )
    ]
    # Also accept checkbox or command-like lines
    if not checks:
        checks = [
            l for l in done.splitlines()
            if re.search(r"\[ \]|`[^`]+`|exit \d", l)
        ]
    if not checks:
        errs.append("Done means has no testable check")
    return errs


if __name__ == "__main__":
    t = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else open(sys.argv[1]).read()
    e = lint(t)
    print("PASS" if not e else "FAIL\n- " + "\n- ".join(e))
    sys.exit(1 if e else 0)
