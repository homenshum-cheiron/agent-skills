#!/usr/bin/env python3
"""Check that a report record matches its claims. Not a quality verdict or a permission."""
import argparse
import json
from pathlib import Path

LIMIT = (
    "Report bookkeeping only. A passing record is not permission to act, "
    "not evidence a method works, and not a rendered Notion page."
)
KINDS = {
    "decision-brief",
    "method-comparison",
    "trace-diagnosis",
    "experiment-result",
    "negative-result",
}
CLASSES = {"measured", "derived", "judged", "estimated", "missing"}
AUDIENCES = {"company", "product", "app_qa", "pipeline"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float)


def invalid(findings):
    return {"status": "invalid", "findings": findings, "limit": LIMIT}


def has_number(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, dict):
        return any(has_number(item) for item in value.values())
    if isinstance(value, list):
        return any(has_number(item) for item in value)
    return False


def check_report(document):
    if not isinstance(document, dict):
        return invalid(["Report must be an object."])
    if document.get("schema_version") != 1:
        return invalid(["schema_version must be 1."])
    findings = []
    if document.get("kind") not in KINDS:
        findings.append("kind must be a known report type.")
    audience = document.get("audience")
    if audience is not None and audience not in AUDIENCES:
        findings.append("audience must be company, product, app_qa, pipeline, or omitted.")
    if not isinstance(document.get("current"), dict) or not isinstance(document.get("desired"), dict):
        findings.append("current and desired must be separate objects.")
    figures = {}
    raw_figures = document.get("figures", [])
    if not isinstance(raw_figures, list):
        findings.append("figures must be a list.")
        raw_figures = []
    for index, figure in enumerate(raw_figures):
        if not isinstance(figure, dict) or not nonempty(figure.get("id")):
            findings.append(f"figures[{index}] needs an id.")
            continue
        kind = figure.get("class")
        if kind not in CLASSES:
            findings.append(f"{figure['id']}: unknown class.")
            continue
        if figure.get("basis") == "hypothesis" and kind == "measured":
            findings.append(f"{figure['id']}: a hypothesis is not measured.")
        if kind == "missing" and figure.get("value") is not None:
            findings.append(f"{figure['id']}: missing is not a number.")
        if kind == "measured" and not number(figure.get("value")):
            findings.append(f"{figure['id']}: measured needs a number.")
        figures[figure["id"]] = figure
    for index, claim in enumerate(document.get("prose_claims", [])):
        if not isinstance(claim, dict):
            findings.append(f"prose_claims[{index}] must be an object.")
            continue
        figure = figures.get(claim.get("figure_id"))
        if figure is None or figure.get("value") != claim.get("value") or figure.get("class") != claim.get("class"):
            findings.append(f"prose_claims[{index}] does not match the figure record.")
    hypothesis_only = document.get("data_status") == "hypothesis-only"
    visuals = document.get("visuals", [])
    if not isinstance(visuals, list):
        findings.append("visuals must be a list.")
        visuals = []
    for index, visual in enumerate(visuals):
        label = f"visuals[{index}]"
        if not isinstance(visual, dict):
            findings.append(f"{label} must be an object.")
            continue
        table = visual.get("table")
        if not isinstance(table, list):
            findings.append(f"{label} needs a table.")
            table = []
        if not nonempty(visual.get("units")) or not nonempty(visual.get("denominator")):
            findings.append(f"{label} needs units and a denominator.")
        if "sample_size" not in visual and visual.get("sample_size_class") != "missing":
            findings.append(f"{label} needs sample_size or sample_size_class missing.")
        series = visual.get("series", table)
        if series != table:
            findings.append(f"{label}: chart series does not match its table.")
        if hypothesis_only and has_number(table):
            findings.append(f"{label}: a hypothesis-only report does not get a numeric chart.")
        if visual.get("class") == "measured" and hypothesis_only:
            findings.append(f"{label}: hypothesis-only data is not measured.")
    for index, action in enumerate(document.get("actions", [])):
        if not isinstance(action, dict):
            findings.append(f"actions[{index}] must be an object.")
            continue
        if action.get("authority") == "granted" and action.get("authority_source") not in {"explicit_owner", "preexisting"}:
            findings.append(f"{action.get('id', index)}: a verdict or recommendation is not permission.")
    if findings:
        return invalid(findings)
    return {"status": "ok", "findings": [], "limit": LIMIT}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        result = check_report(json.loads(args.report.read_text()))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = invalid([str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "ok" else 3


if __name__ == "__main__":
    raise SystemExit(main())
