#!/usr/bin/env python3
"""Check a trace record for honest missingness and unique costs. Not a runtime."""
import argparse
import json
from pathlib import Path

LIMIT = (
    "Bookkeeping for a trace record only. It does not show that a product improved, "
    "that telemetry is complete, or that any loop may run itself."
)
CLASSES = {"measured", "derived", "judged", "estimated", "missing"}
BANNED_EXPORTS = ("prompt_body", "chain_of_thought", "tool_result_body", "secret")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float)


def invalid(findings):
    return {"status": "invalid", "findings": findings, "limit": LIMIT}


def covered(spans):
    merged = []
    total = 0
    for span in spans:
        start, end = span["start_ms"], span["end_ms"]
        total += end - start
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return total, sum(end - start for start, end in merged)


def check_trace(document):
    if not isinstance(document, dict):
        return invalid(["Record must be an object."])
    if document.get("schema_version") != 1:
        return invalid(["schema_version must be 1."])
    findings = []
    policy = document.get("export_policy", "minimal")
    if policy not in {"minimal", "authorized_sample"}:
        findings.append("export_policy must be minimal or authorized_sample.")
    if policy == "authorized_sample" and not nonempty(document.get("sample_reason")):
        findings.append("authorized_sample needs a sample_reason.")
    if policy != "authorized_sample":
        for key in BANNED_EXPORTS:
            if key in document and document.get(key) not in (None, "", []):
                findings.append(f"{key} is not exported under the minimal policy.")
    ledger = document.get("ledger")
    if not isinstance(ledger, list):
        findings.append("ledger must be a list.")
        ledger = []
    seen = set()
    for index, entry in enumerate(ledger):
        label = f"ledger[{index}]"
        if not isinstance(entry, dict):
            findings.append(f"{label} must be an object.")
            continue
        gid = entry.get("generation_id")
        if nonempty(gid):
            label = gid
            if gid in seen and entry.get("counts_once", True):
                findings.append(f"{gid} is counted more than once.")
            seen.add(gid)
        else:
            findings.append(f"ledger[{index}] needs a generation_id.")
        if entry.get("already_inside") and entry.get("counts_once", True):
            findings.append(f"{label} double-counts tokens already inside {entry.get('already_inside')}.")
        kind = entry.get("class", "measured")
        if kind not in CLASSES:
            findings.append(f"{label}: class must be measured, derived, judged, estimated, or missing.")
            continue
        tokens = entry.get("tokens")
        if kind == "missing" and tokens is not None:
            findings.append(f"{label}: missing tokens must be null, not a number.")
        elif kind == "measured" and not number(tokens):
            findings.append(f"{label}: measured tokens need a number.")
        if entry.get("basis") == "hypothesis" and kind == "measured":
            findings.append(f"{label}: a hypothesis is not a measured figure.")
    spans = document.get("spans", [])
    parsed = []
    if not isinstance(spans, list):
        findings.append("spans must be a list.")
        spans = []
    missing_first = False
    for index, span in enumerate(spans):
        if not isinstance(span, dict) or not number(span.get("start_ms")) or not number(span.get("end_ms")):
            findings.append(f"spans[{index}] needs numeric start_ms and end_ms.")
            continue
        if span["end_ms"] < span["start_ms"]:
            findings.append(f"spans[{index}] ends before it starts.")
            continue
        parsed.append(span)
        if span.get("first_token_ms") is None and span.get("kind") == "model":
            missing_first = True
    claimed = document.get("claimed_wall_ms")
    if parsed and claimed is not None:
        if not number(claimed):
            findings.append("claimed_wall_ms must be a number when present.")
        else:
            total, wall = covered(sorted(parsed, key=lambda item: (item["start_ms"], item["end_ms"])))
            if claimed == total and wall < total:
                findings.append("Overlapping spans were summed and reported as wall time.")
    figures = document.get("figures", [])
    if not isinstance(figures, list):
        findings.append("figures must be a list.")
        figures = []
    for index, figure in enumerate(figures):
        if not isinstance(figure, dict):
            findings.append(f"figures[{index}] must be an object.")
            continue
        kind = figure.get("class")
        if kind not in CLASSES:
            findings.append(f"figures[{index}]: unknown class.")
            continue
        if kind == "missing" and figure.get("value") is not None:
            findings.append(f"{figure.get('id', index)}: missing is not a number.")
        if kind == "measured" and not number(figure.get("value")):
            findings.append(f"{figure.get('id', index)}: measured needs a number.")
        if figure.get("basis") == "hypothesis" and kind == "measured":
            findings.append(f"{figure.get('id', index)}: a hypothesis is not measured.")
        if figure.get("name") == "ttft" and missing_first and kind == "measured":
            findings.append("Missing first-token time was recorded as measured.")
    for index, action in enumerate(document.get("actions", [])):
        if not isinstance(action, dict):
            findings.append(f"actions[{index}] must be an object.")
            continue
        source = action.get("authority_source")
        if action.get("authority") == "granted" and source not in {"explicit_owner", "preexisting"}:
            findings.append(f"{action.get('id', index)}: a verdict or recommendation is not permission.")
    if findings:
        return invalid(findings)
    return {"status": "ok", "findings": [], "limit": LIMIT}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        result = check_trace(json.loads(args.record.read_text()))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = invalid([str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "ok" else 3


if __name__ == "__main__":
    raise SystemExit(main())
