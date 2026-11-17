#!/usr/bin/env python3
"""Eval scorecard: per-case verdict counts, latency percentiles, throughput and cost per task.

Standard library only (Python 3.9+). Reads a CSV with one row per case.

Columns (header names, case-insensitive):
  case_id      required
  verdict      required: passed | failed | unverified | inconclusive
  duration_s   optional: seconds from start to finish of that case
  cost_usd     optional: dollars for that case; say what it covers with --cost-scope
  finished     optional: true/false, whether the case produced every required output
  cache_write_usd optional: dollars spent writing prompt cache for that case

Rules this script enforces:
  - Four verdicts are counted separately. No pooled score is printed.
  - A blank number is missing, never zero. Totals say how many rows they cover.
  - Throughput is measured only when --wall-seconds is given (the real batch window).
    Otherwise it prints a serial-equivalent figure labelled as an estimate.
  - Percentiles use the nearest-rank method, named in the output.

Exit codes: 0 ok, 2 bad input (unknown verdict, missing column, unreadable number).
"""
from __future__ import annotations

import argparse
import csv
import math
import sys

VERDICTS = ("passed", "failed", "unverified", "inconclusive")
TRUE = {"true", "yes", "1", "y"}
FALSE = {"false", "no", "0", "n"}


class InputError(Exception):
    pass


def nearest_rank(sorted_values, pct):
    if not sorted_values:
        return None
    rank = max(1, math.ceil(pct / 100.0 * len(sorted_values)))
    return sorted_values[rank - 1]


def number(row, key, line):
    raw = (row.get(key) or "").strip()
    if raw == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        raise InputError(f"line {line}: {key} is not a number: {raw!r}")
    if value < 0 or not math.isfinite(value):
        raise InputError(f"line {line}: {key} must be a non-negative number")
    return value


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise InputError("empty file")
        fields = {name.strip().lower(): name for name in reader.fieldnames}
        for needed in ("case_id", "verdict"):
            if needed not in fields:
                raise InputError(f"missing column: {needed}")
        rows, seen = [], set()
        for line, raw in enumerate(reader, start=2):
            row = {key: raw.get(original) for key, original in fields.items()}
            case = (row.get("case_id") or "").strip()
            if not case:
                raise InputError(f"line {line}: empty case_id")
            if case in seen:
                raise InputError(f"line {line}: duplicate case_id {case}")
            seen.add(case)
            verdict = (row.get("verdict") or "").strip().lower()
            if verdict not in VERDICTS:
                raise InputError(f"line {line}: verdict must be one of {', '.join(VERDICTS)}, got {verdict!r}")
            finished_raw = (row.get("finished") or "").strip().lower()
            if finished_raw in TRUE:
                finished = True
            elif finished_raw in FALSE:
                finished = False
            elif finished_raw == "":
                finished = None
            else:
                raise InputError(f"line {line}: finished must be true or false")
            rows.append({
                "case_id": case,
                "verdict": verdict,
                "duration_s": number(row, "duration_s", line),
                "cost_usd": number(row, "cost_usd", line),
                "cache_write_usd": number(row, "cache_write_usd", line),
                "finished": finished,
            })
    if not rows:
        raise InputError("no cases")
    return rows


def fmt_s(value):
    if value is None:
        return "missing"
    return f"{value:,.0f} s ({value / 60:.1f} min)"


def fmt_usd(value):
    return "missing" if value is None else f"${value:,.2f}"


def summarize(rows, wall_seconds=None, cost_scope="not stated"):
    n = len(rows)
    if wall_seconds is not None and (not math.isfinite(wall_seconds) or wall_seconds <= 0):
        raise InputError("wall-seconds must be finite and greater than zero")
    counts = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}
    durations = sorted(r["duration_s"] for r in rows if r["duration_s"] is not None)
    costs = [r["cost_usd"] for r in rows if r["cost_usd"] is not None]
    cache = [r["cache_write_usd"] for r in rows if r["cache_write_usd"] is not None]
    finished_known = [r for r in rows if r["finished"] is not None]
    finished = sum(1 for r in finished_known if r["finished"])
    out = []
    out.append("| Metric | Value | Label |")
    out.append("|---|---|---|")
    out.append(f"| Cases | {n} | measured |")
    for v in VERDICTS:
        out.append(f"| {v.capitalize()} | {counts[v]} | judged |")
    if finished_known:
        out.append(f"| Finished every required output | {finished} of {len(finished_known)} | measured |")
    else:
        out.append("| Finished every required output | missing | missing |")
    timed = f"{len(durations)} of {n} cases timed"
    for pct in (50, 90, 95):
        out.append(f"| Latency p{pct} per case (nearest rank) | {fmt_s(nearest_rank(durations, pct))} | measured, {timed} |")
    out.append(f"| Slowest case | {fmt_s(durations[-1] if durations else None)} | measured |")
    busy = sum(durations) if durations else None
    if wall_seconds:
        done = finished if finished_known else None
        rate = None if done is None else done / (wall_seconds / 3600.0)
        out.append(f"| Batch wall-clock window | {fmt_s(wall_seconds)} | measured (given) |")
        out.append(f"| Tasks finished per hour | {'missing' if rate is None else f'{rate:.2f}'} | derived from the window |")
    elif busy:
        base = finished if finished_known else n
        what = "finished cases" if finished_known else "cases"
        out.append(f"| Sum of case durations | {fmt_s(busy)} | measured, includes overlap if cases ran in parallel |")
        out.append(f"| Tasks finished per hour, serial equivalent | {base / (busy / 3600.0):.2f} {what}/h | estimate: assumes one case at a time; real window unknown |")
    else:
        out.append("| Tasks finished per hour | missing | missing |")
    if costs:
        total = sum(costs)
        out.append(f"| Total cost ({cost_scope}) | {fmt_usd(total)} | measured, {len(costs)} of {n} cases |")
        out.append(f"| Cost per case, mean | {fmt_usd(total / len(costs))} | derived |")
        out.append(f"| Cost per case, median | {fmt_usd(sorted(costs)[(len(costs) - 1) // 2] if len(costs) % 2 else (sorted(costs)[len(costs)//2 - 1] + sorted(costs)[len(costs)//2]) / 2)} | derived |")
        passed_cost_known = len(costs) == n
        if counts["passed"] and passed_cost_known:
            out.append(f"| Cost per passed case | {fmt_usd(total / counts['passed'])} | derived: all spend divided by passed cases |")
        else:
            out.append("| Cost per passed case | missing | needs a cost on every case and at least one pass |")
        unfinished = [r["cost_usd"] for r in rows if r["finished"] is False and r["cost_usd"] is not None]
        if finished_known:
            out.append(f"| Spend on unfinished cases | {fmt_usd(sum(unfinished))} | measured |")
    else:
        out.append("| Cost per case | missing | missing |")
    paired = [r for r in rows if r["cost_usd"] is not None and r["cache_write_usd"] is not None]
    if costs and len(paired) == len(costs) and sum(costs) > 0:
        cache_total = sum(r["cache_write_usd"] for r in paired)
        out.append(f"| Cache-write share of cost | {100 * cache_total / sum(costs):.0f}% | derived, {len(paired)} of {n} cases |")
    else:
        out.append("| Cache-write share of cost | missing | needs cache_write_usd on every costed case |")
    return "\n".join(out), counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv")
    parser.add_argument("--wall-seconds", type=float, default=None,
                        help="real start-to-end window of the whole batch, if known")
    parser.add_argument("--cost-scope", default="not stated",
                        help="what cost_usd covers, for example 'model only'")
    args = parser.parse_args(argv)
    try:
        rows = load(args.csv)
        table, _ = summarize(rows, args.wall_seconds, args.cost_scope)
    except (InputError, OSError) as error:
        print(f"bad input: {error}", file=sys.stderr)
        return 2
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
