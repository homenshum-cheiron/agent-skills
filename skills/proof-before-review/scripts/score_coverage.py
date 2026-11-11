#!/usr/bin/env python3
"""Score nine coverage marks. Arithmetic only; not a quality certification."""
import argparse
import json
from pathlib import Path

PROMPTS = (
    "plain_summary",
    "how_it_works",
    "flowchart",
    "test_command",
    "structured_io",
    "code_lines",
    "live_evidence",
    "unproven_risks",
    "stack_position",
)
MARKS = {"supported", "missing", "na"}
LIMIT = (
    "Coverage arithmetic only. Not a quality certification, approval, "
    "or proof that rationales are true."
)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def invalid(findings):
    return {"status": "invalid", "findings": findings, "limit": LIMIT}


def score(document):
    if not isinstance(document, dict):
        return invalid(["Document must be an object."])
    items = document.get("items")
    if not isinstance(items, list):
        return invalid(["items must be a list."])
    findings = []
    seen = {}
    attempted = set()
    for index, item in enumerate(items):
        label = f"items[{index}]"
        if not isinstance(item, dict):
            findings.append(f"{label} must be an object.")
            continue
        prompt_id = item.get("id")
        if prompt_id not in PROMPTS:
            findings.append(f"{label} has an unknown id.")
            continue
        attempted.add(prompt_id)
        if prompt_id in seen:
            findings.append(f"{prompt_id} is duplicated.")
            continue
        mark = item.get("mark")
        if mark not in MARKS:
            findings.append(f"{prompt_id}: mark must be supported, missing, or na.")
            continue
        rationale = item.get("rationale")
        if mark == "na":
            if not nonempty(rationale):
                findings.append(f"{prompt_id}: N/A requires a rationale.")
                continue
            rationale = rationale.strip()
        elif rationale is not None and not nonempty(rationale):
            findings.append(f"{prompt_id}: rationale must be a nonempty string when present.")
            continue
        seen[prompt_id] = {"mark": mark, "rationale": rationale}
    for prompt_id in PROMPTS:
        if prompt_id not in seen and prompt_id not in attempted:
            findings.append(f"{prompt_id} is missing from items.")
    if "claimed_report" in document and not isinstance(document.get("claimed_report"), str):
        findings.append("claimed_report must be a string.")
    if findings:
        return invalid(findings)
    supported = [prompt_id for prompt_id in PROMPTS if seen[prompt_id]["mark"] == "supported"]
    missing = [prompt_id for prompt_id in PROMPTS if seen[prompt_id]["mark"] == "missing"]
    na_items = [
        {"id": prompt_id, "rationale": seen[prompt_id]["rationale"]}
        for prompt_id in PROMPTS
        if seen[prompt_id]["mark"] == "na"
    ]
    applicable = len(supported) + len(missing)
    suffix = " with reasons" if na_items else ""
    report = f"{len(supported)}/{applicable} applicable, plus {len(na_items)} N/A{suffix}"
    claimed = document.get("claimed_report")
    if isinstance(claimed, str) and claimed != report:
        return {
            "status": "invalid",
            "findings": [f"claimed_report does not match computed report {report}."],
            "supported": len(supported),
            "applicable": applicable,
            "report": report,
            "limit": LIMIT,
        }
    return {
        "status": "scored",
        "supported": len(supported),
        "applicable": applicable,
        "missing": missing,
        "na": na_items,
        "report": report,
        "findings": [],
        "limit": LIMIT,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        result = score(json.loads(args.document.read_text()))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = invalid([str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "scored" else 3


if __name__ == "__main__":
    raise SystemExit(main())
