#!/usr/bin/env python3
"""Check a qualitative autonomy map. A passing file is not an autonomy proof."""
import argparse
import json
from pathlib import Path

LIMIT = (
    "Map bookkeeping only. A passing file is not a measured autonomy rate, "
    "not a demonstration that a loop ran, and not permission to deploy one."
)
STATUSES = {"documented", "offline_partial", "unknown", "not_demonstrated", "demonstrated"}
BLOCKED = {"unknown", "not_demonstrated", "offline_partial"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def invalid(findings):
    return {"status": "invalid", "findings": findings, "limit": LIMIT}


def check_map(document):
    if not isinstance(document, dict):
        return invalid(["Map must be an object."])
    findings = []
    if document.get("numeric_chart_allowed") is True:
        findings.append("A numeric autonomy chart is not allowed while required counts are unknown.")
    if isinstance(document.get("autonomy_percent"), (int, float)) and not isinstance(document.get("autonomy_percent"), bool):
        findings.append("An autonomy percentage is not a substitute for missing denominators.")
    stages = document.get("stages")
    if not isinstance(stages, list):
        return invalid(findings + ["stages must be a list."])
    by_id = {}
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            findings.append(f"stages[{index}] must be an object.")
            continue
        sid = stage.get("id")
        status = stage.get("status")
        if status not in STATUSES:
            findings.append(f"stages[{index}]: status is not a known qualitative claim.")
            continue
        by_id[sid] = stage
        if status == "demonstrated":
            sample = document.get("sample") if isinstance(document.get("sample"), dict) else {}
            if not nonempty(stage.get("evidence_note")) or not isinstance(sample.get("n_eligible_attempts"), int):
                findings.append(f"Stage {sid} cannot be demonstrated without an evidence note and an eligible-attempt count.")
    claims = document.get("prose_claims", [])
    if not isinstance(claims, list):
        findings.append("prose_claims must be a list.")
        claims = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            findings.append(f"prose_claims[{index}] must be an object.")
            continue
        stage = by_id.get(claim.get("stage_id"))
        if stage is None or stage.get("status") != claim.get("status"):
            findings.append(f"prose_claims[{index}] does not match the stage record.")
    edges = document.get("diagram_edges", [])
    if not isinstance(edges, list):
        findings.append("diagram_edges must be a list.")
        edges = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            findings.append(f"diagram_edges[{index}] must be an object.")
            continue
        if edge.get("style") in {"solid", "green", "reachable"}:
            findings.append(f"diagram_edges[{index}] draws a reachable path.")
        target = by_id.get(edge.get("to"))
        if target is None or target.get("status") in BLOCKED or target.get("status") != "demonstrated":
            findings.append("diagram edge %s points at a stage that is not demonstrated." % index)
    sample = document.get("sample") if isinstance(document.get("sample"), dict) else {}
    interventions = sample.get("interventions") if isinstance(sample.get("interventions"), dict) else {}
    if "policy_approval" not in interventions:
        findings.append("Required policy approval is missing from the human-burden record.")
    if document.get("policy_approval_is_capability_failure") is True:
        findings.append("A required policy approval is not a capability failure.")
    if findings:
        return invalid(findings)
    return {"status": "ok", "findings": [], "limit": LIMIT}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        result = check_map(json.loads(args.document.read_text()))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = invalid([str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "ok" else 3


if __name__ == "__main__":
    raise SystemExit(main())
