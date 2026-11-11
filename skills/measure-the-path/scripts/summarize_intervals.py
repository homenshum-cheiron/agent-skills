#!/usr/bin/env python3
"""Summarize observed interval coverage without inferring a critical path."""
import argparse
import json
import math
from pathlib import Path


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def summarize(document):
    if not isinstance(document, dict):
        raise ValueError("Input must be an object.")
    lo, hi = document.get("window_start"), document.get("window_end")
    if not number(lo) or not number(hi) or hi < lo:
        raise ValueError("A finite, ordered observation window is required.")
    spans = document.get("spans")
    if not isinstance(spans, list) or not spans:
        raise ValueError("spans must be a nonempty list.")
    intervals = []
    for span in spans:
        if not isinstance(span, dict) or not isinstance(span.get("name"), str) or not span["name"].strip():
            raise ValueError("Every span needs a name.")
        start, end = span.get("start"), span.get("end")
        if not number(start) or not number(end) or not lo <= start <= end <= hi:
            raise ValueError("Span times must be finite, ordered and inside the window.")
        intervals.append((start, end))
    merged = []
    for start, end in sorted(intervals):
        if end == start:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(end, merged[-1][1])
        else:
            merged.append([start, end])
    gaps, cursor = [], lo
    for start, end in merged:
        if start > cursor:
            gaps.append([cursor, start])
        cursor = end
    if cursor < hi:
        gaps.append([cursor, hi])
    covered = sum(end - start for start, end in merged)
    work = sum(end - start for start, end in intervals)
    if not all(number(value) for value in (hi - lo, covered, work)):
        raise ValueError("Calculated duration exceeds finite numeric range.")
    return {"wall_time": hi - lo,
            "summed_work": work,
            "covered_time": covered,
            "unexplained_time": hi - lo - covered,
            "gaps": gaps,
            "limit": "Coverage only; overlapping and nested work are not exclusive time or causal attribution."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = summarize(json.loads(args.input.read_text()))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
