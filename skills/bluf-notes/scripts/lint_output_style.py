#!/usr/bin/env python3
"""Fail (exit 1) if a reply does not follow the four-line work-reply style.

Usage: lint_output_style.py FILE|-
"""
import re
import sys

LABELS = ["Needs you", "Done?", "How", "Problems"]
# A write-up link: URL, home path, or a path containing a slash.
WRITEUP = re.compile(r"(https?://|~/|[A-Za-z0-9._-]+/)")


def lint(text):
    errs = []
    lines = [l.lstrip("> ").strip() for l in text.splitlines()]
    pos = {}
    for i, l in enumerate(lines):
        for lab in LABELS:
            if lab not in pos and re.match(r"\**" + re.escape(lab) + r":?\**:?", l):
                pos[lab] = i
    missing = [l for l in LABELS if l not in pos]
    if missing:
        errs.append(f"missing labels: {missing}")
    else:
        order = [pos[l] for l in LABELS]
        if order != sorted(order):
            errs.append("labels out of order")
        done = re.sub(r"^\**Done\?\**:?\**\s*", "", lines[pos["Done?"]])
        if not re.match(r"(Yes|No|Partly)\b", done):
            errs.append("Done? must start with Yes/No/Partly")
        dn = [i for i, l in enumerate(lines) if "DECISION NEEDED" in l]
        if dn and dn[0] > pos["Done?"]:
            errs.append("DECISION NEEDED appears after Done? (buried)")
        head = " ".join(lines[pos["Needs you"]: pos["Problems"] + 1])
        if len(head.split()) > 80 + (60 if dn else 0):
            errs.append(f"four-line head too long ({len(head.split())} words)")
    for m in re.finditer(r"\*\*(NOT DONE|NOT CHECKED|FAILED):\*\*([^*]*)", text):
        if not re.search(r"\bbecause\b|\(.*\)", m.group(2)):
            errs.append(f"{m.group(1)} item has no reason: {m.group(2).strip()[:60]}")
    words = len(text.split())
    if words > 200 and not WRITEUP.search(text):
        errs.append(f"{words} words and no link to a full write-up")
    return errs


if __name__ == "__main__":
    t = sys.stdin.read() if len(sys.argv) < 2 or sys.argv[1] == "-" else open(sys.argv[1]).read()
    e = lint(t)
    print("PASS" if not e else "FAIL\n- " + "\n- ".join(e))
    sys.exit(1 if e else 0)
