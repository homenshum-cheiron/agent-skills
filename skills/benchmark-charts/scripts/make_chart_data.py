#!/usr/bin/env python3
"""Turn a raw results file into a BenchmarkChartDataset, or validate one.

Every number must trace to a source id or a named formula. Estimates must be
flagged. Missing values become status=not_measured with display "not measured".
Sums across cases are labeled as sums, never as a pooled quality score.

Usage:
  python3 scripts/make_chart_data.py build --input examples/raw_results.json --output examples/chart_data.json
  python3 scripts/make_chart_data.py validate examples/chart_data.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"
NOT_MEASURED_DISPLAY = "not measured"
SUMS_NOTE = (
    "Additive sums for the headline strip only. These are not a pooled quality "
    "score. Case verdicts stay per case; nested subunit counts are a sum across "
    "cases and must not be used as the headline score."
)

Number = int | float


class ValidationError(Exception):
    """One or more contract violations. The message lists every issue."""


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _round_money(value: Number) -> float:
    return round(float(value), 2)


def missing_metric() -> dict[str, Any]:
    return {"status": "not_measured", "value": None, "display": NOT_MEASURED_DISPLAY}


def measured(value: Number, source: str, unit: str | None = None) -> dict[str, Any]:
    metric: dict[str, Any] = {"status": "measured", "value": value, "source": source}
    if unit:
        metric["unit"] = unit
    return metric


def estimate(
    value: Number,
    source: str,
    low: Number | None = None,
    high: Number | None = None,
    unit: str | None = None,
) -> dict[str, Any]:
    metric: dict[str, Any] = {"status": "estimate", "value": value, "source": source}
    if low is not None:
        metric["low"] = low
    if high is not None:
        metric["high"] = high
    if unit:
        metric["unit"] = unit
    metric["display"] = _estimate_display(metric, unit or "")
    return metric


def derived(
    value: Number,
    derived_from: list[str],
    formula: str,
    unit: str | None = None,
    status: str = "measured",
    low: Number | None = None,
    high: Number | None = None,
) -> dict[str, Any]:
    metric: dict[str, Any] = {
        "status": status,
        "value": value,
        "source": "derived",
        "derived_from": list(derived_from),
        "formula": formula,
    }
    if unit:
        metric["unit"] = unit
    if low is not None:
        metric["low"] = low
    if high is not None:
        metric["high"] = high
    if status == "estimate":
        metric["display"] = _estimate_display(metric, unit or "")
    return metric


def _estimate_display(metric: dict[str, Any], unit: str) -> str:
    low, high = metric.get("low"), metric.get("high")
    prefix = "$" if unit == "usd" or unit == "" and "usd" in str(metric.get("unit", "")) else ""
    if unit == "usd":
        prefix = "$"
    if low is not None and high is not None:
        if prefix == "$":
            return f"{prefix}{float(low):.2f}–{prefix}{float(high):.2f} ESTIMATE"
        return f"{low:g}–{high:g} ESTIMATE"
    value = metric.get("value")
    if prefix == "$" and _is_number(value):
        return f"{prefix}{float(value):.2f} ESTIMATE"
    return f"{value} ESTIMATE"


def display_metric(metric: dict[str, Any] | None, kind: str = "") -> str:
    if not metric or metric.get("status") == "not_measured":
        return NOT_MEASURED_DISPLAY
    if metric.get("status") == "estimate":
        return metric.get("display") or _estimate_display(metric, metric.get("unit") or kind)
    value = metric.get("value")
    unit = metric.get("unit") or kind
    if unit == "usd" and _is_number(value):
        return f"${value:.2f}"
    if unit == "s" and _is_number(value):
        return f"{value / 60:.1f} min" if value >= 60 else f"{value:g} s"
    if _is_number(value):
        return str(value)
    return NOT_MEASURED_DISPLAY


def _wrap_metric(raw: Any, source: str, unit: str | None = None) -> dict[str, Any]:
    if raw is None:
        return missing_metric()
    if isinstance(raw, dict):
        status = raw.get("status")
        if status == "not_measured" or (raw.get("value") is None and "low" not in raw and status is None):
            return missing_metric()
        if status == "estimate" or "low" in raw or "high" in raw:
            value = raw.get("value", raw.get("high", raw.get("low")))
            if value is None:
                return missing_metric()
            return estimate(value, raw.get("source") or source, raw.get("low"), raw.get("high"), raw.get("unit") or unit)
        if "value" in raw and status == "measured":
            return measured(raw["value"], raw.get("source") or source, raw.get("unit") or unit)
        if "value" in raw and raw["value"] is None:
            return missing_metric()
        raise ValidationError(f"untraceable metric object: {raw!r}")
    if _is_number(raw):
        return measured(raw, source, unit)
    raise ValidationError(f"untraceable metric value: {raw!r}")


def _source_ids(doc: dict[str, Any]) -> set[str]:
    return {str(item["id"]) for item in doc.get("sources", [])} | {"derived"}


def _walk_metrics(node: Any, path: str, found: list[tuple[str, dict[str, Any]]]) -> None:
    if isinstance(node, dict):
        if "status" in node and set(node).issubset(
            {"status", "value", "low", "high", "unit", "source", "derived_from", "formula", "display"}
        ):
            found.append((path, node))
            return
        for key, value in node.items():
            _walk_metrics(value, f"{path}.{key}" if path else key, found)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _walk_metrics(value, f"{path}[{index}]", found)


def _bare_numbers(node: Any, path: str, found: list[str], *, inside_metric: bool = False) -> None:
    """Collect numbers that are not inside a metric object."""
    metric_keys = {"status", "value", "low", "high", "unit", "source", "derived_from", "formula", "display"}
    if isinstance(node, dict):
        is_metric = "status" in node and set(node) <= metric_keys
        for key, value in node.items():
            # Structural identifiers and labels are not measurements.
            if key in {"schema_version"}:
                continue
            _bare_numbers(value, f"{path}.{key}" if path else key, found, inside_metric=is_metric)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _bare_numbers(value, f"{path}[{index}]", found, inside_metric=inside_metric)
    elif _is_number(node) and not inside_metric:
        found.append(path)


def validate(doc: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["document is not an object"]
    if doc.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for key in (
        "title",
        "score_unit",
        "subunit_kind",
        "highlight_arm",
        "baseline_arm",
        "pass_labels",
        "arms",
        "cases",
        "sources",
    ):
        if key not in doc:
            errors.append(f"missing required field: {key}")
    arms = doc.get("arms") or []
    arm_ids = [a.get("id") for a in arms if isinstance(a, dict)]
    if len(arm_ids) != len(set(arm_ids)):
        errors.append("duplicate arm id")
    if len(arms) < 2:
        errors.append("need at least two arms")
    if doc.get("highlight_arm") not in arm_ids:
        errors.append("highlight_arm is not in arms")
    if doc.get("baseline_arm") not in arm_ids:
        errors.append("baseline_arm is not in arms")
    roles = {a.get("id"): a.get("role") for a in arms if isinstance(a, dict)}
    if roles.get(doc.get("baseline_arm")) not in {"baseline", None} and doc.get("baseline_arm") in roles:
        if roles.get(doc.get("baseline_arm")) != "baseline":
            errors.append("baseline_arm should have role=baseline")
    if roles.get(doc.get("highlight_arm")) not in {"highlight", None} and doc.get("highlight_arm") in roles:
        if roles.get(doc.get("highlight_arm")) != "highlight":
            errors.append("highlight_arm should have role=highlight")
    source_ids = _source_ids(doc)
    if "sources" in doc and not doc["sources"]:
        errors.append("sources must not be empty")
    case_ids: list[str] = []
    for index, case in enumerate(doc.get("cases") or []):
        if not isinstance(case, dict) or not case.get("id"):
            errors.append(f"cases[{index}] missing id")
            continue
        case_ids.append(case["id"])
        results = case.get("results") or {}
        if not results:
            errors.append(f"case {case['id']} has no results")
        for arm_id, result in results.items():
            if arm_id not in arm_ids:
                errors.append(f"case {case['id']} has unknown arm {arm_id}")
            if not isinstance(result, dict):
                errors.append(f"case {case['id']} arm {arm_id} is not an object")
                continue
            prefix = f"cases.{case['id']}.{arm_id}"
            verdict = result.get("verdict")
            if verdict not in {"pass", "fail", "incomplete", "not_measured"}:
                errors.append(f"{prefix}.verdict is invalid")
            score = result.get("score")
            if not isinstance(score, dict) or "passed" not in score or "n" not in score:
                errors.append(f"{prefix}.score must have passed and n")
            else:
                errors.extend(_metric_errors(score["passed"], f"{prefix}.score.passed", source_ids, allow_missing=True))
                errors.extend(_metric_errors(score["n"], f"{prefix}.score.n", source_ids, allow_missing=True))
                passed, n = score["passed"], score["n"]
                if (
                    passed.get("status") != "not_measured"
                    and n.get("status") != "not_measured"
                    and _is_number(passed.get("value"))
                    and _is_number(n.get("value"))
                    and passed["value"] > n["value"]
                ):
                    errors.append(f"{prefix}.score passed exceeds n")
            for field, unit in (("cost_usd", "usd"), ("wall_s", "s")):
                if field in result:
                    errors.extend(_metric_errors(result[field], f"{prefix}.{field}", source_ids, allow_missing=True))
            for group in ("tokens_by_stage", "time_by_stage", "cost_by_stage"):
                stages = result.get(group) or {}
                if isinstance(stages, dict):
                    for name, metric in stages.items():
                        errors.extend(_metric_errors(metric, f"{prefix}.{group}.{name}", source_ids, allow_missing=True))
                if group == "cost_by_stage" and isinstance(stages, dict) and result.get("cost_usd"):
                    parts = [m.get("value") for m in stages.values() if m.get("status") != "not_measured"]
                    total = result["cost_usd"]
                    if (
                        total.get("status") == "measured"
                        and parts
                        and all(_is_number(v) for v in parts)
                        and abs(sum(parts) - float(total["value"])) > 0.02
                    ):
                        errors.append(f"{prefix}.cost_by_stage does not sum to cost_usd")
            subunits = result.get("subunits")
            if subunits:
                labels = [s.get("label") for s in subunits]
                passed_metric = (result.get("score") or {}).get("passed") or {}
                n_metric = (result.get("score") or {}).get("n") or {}
                if n_metric.get("status") == "measured" and n_metric.get("value") != len(subunits):
                    errors.append(f"{prefix}.score.n does not match subunit count")
                if passed_metric.get("status") == "measured":
                    expected = sum(1 for s in subunits if s.get("passed") is True or s.get("label") in set(doc.get("pass_labels") or []))
                    # passed may be computed from labels; compare if boolean present, else labels
                    has_bool = any(s.get("passed") is not None for s in subunits)
                    if has_bool:
                        expected = sum(1 for s in subunits if s.get("passed") is True)
                    if passed_metric.get("value") != expected:
                        errors.append(f"{prefix}.score.passed does not match subunits ({expected})")
    if len(case_ids) != len(set(case_ids)):
        errors.append("duplicate case id")

    sums = doc.get("sums")
    if sums:
        if "note" not in sums:
            errors.append("sums.note is required so totals are not read as a pooled score")
        elif "not a pooled" not in sums["note"].lower() and "not a pooled quality" not in sums["note"].lower():
            if "pooled" not in sums["note"].lower() or "not" not in sums["note"].lower():
                errors.append("sums.note must say these totals are not a pooled quality score")
        if sums.get("subunits_passed") and sums.get("subunits_passed_not_a_score") is not True:
            errors.append("sums.subunits_passed_not_a_score must be true: subunit sums are not the headline score")
        for group in ("cost_usd", "wall_s", "cases_passed", "subunits_passed", "subunits_n"):
            block = sums.get(group) or {}
            if isinstance(block, dict):
                for arm_id, metric in block.items():
                    if arm_id in arm_ids or True:
                        errors.extend(_metric_errors(metric, f"sums.{group}.{arm_id}", source_ids, allow_missing=True))
        for name in ("cost_cut_pct", "time_cut_pct"):
            if name in sums:
                errors.extend(_metric_errors(sums[name], f"sums.{name}", source_ids, allow_missing=True))
        errors.extend(_check_sums_match_cases(doc))

    waterfall = doc.get("waterfall")
    if waterfall:
        errors.extend(_metric_errors(waterfall.get("start_value") or {}, "waterfall.start_value", source_ids))
        running = (waterfall.get("start_value") or {}).get("value")
        for index, step in enumerate(waterfall.get("steps") or []):
            errors.extend(_metric_errors(step.get("delta") or {}, f"waterfall.steps[{index}].delta", source_ids))
            if _is_number(running) and _is_number((step.get("delta") or {}).get("value")):
                running = _round_money(running + step["delta"]["value"])
        highlight = (doc.get("highlight_arm"),)
        if _is_number(running) and sums and sums.get("cost_usd", {}).get(doc.get("highlight_arm")):
            expected = sums["cost_usd"][doc["highlight_arm"]].get("value")
            if _is_number(expected) and abs(running - float(expected)) > 0.02:
                errors.append(
                    f"waterfall steps end at {running}, but highlight cost sum is {expected}"
                )

    metrics: list[tuple[str, dict[str, Any]]] = []
    _walk_metrics(doc, "", metrics)
    for path, metric in metrics:
        errors.extend(_metric_errors(metric, path or "metric", source_ids, allow_missing=True))

    bare: list[str] = []
    _bare_numbers(doc, "", bare)
    # Allow a few structural integers already checked (none should remain).
    for path in bare:
        errors.append(f"untraceable number at {path}: every number must live in a metric with a source or formula")

    return errors


def _metric_errors(metric: Any, path: str, source_ids: set[str], allow_missing: bool = False) -> list[str]:
    if not isinstance(metric, dict) or "status" not in metric:
        return [f"{path} is not a metric object"]
    errors: list[str] = []
    status = metric["status"]
    if status not in {"measured", "estimate", "not_measured"}:
        errors.append(f"{path}.status is invalid")
    if status == "not_measured":
        if metric.get("value") not in (None,):
            errors.append(f"{path}: not_measured must not carry a value")
        if metric.get("display") not in (None, NOT_MEASURED_DISPLAY):
            errors.append(f"{path}: not_measured display must be '{NOT_MEASURED_DISPLAY}'")
        return errors
    if metric.get("value") is None and metric.get("low") is None:
        errors.append(f"{path}: measured or estimate metric needs a value")
    if status == "estimate":
        display = metric.get("display") or ""
        if "ESTIMATE" not in display:
            errors.append(f"{path}: estimate must include an ESTIMATE label in display")
        if "low" in metric and "high" in metric and metric["low"] > metric["high"]:
            errors.append(f"{path}: estimate low is greater than high")
    source = metric.get("source")
    derived_from = metric.get("derived_from") or []
    formula = metric.get("formula")
    if source not in source_ids and not (derived_from and formula):
        errors.append(f"{path}: untraceable number (need a source id or derived_from + formula)")
    if source and source not in source_ids:
        errors.append(f"{path}: unknown source {source}")
    if derived_from and not formula:
        errors.append(f"{path}: derived_from requires formula")
    if formula and not derived_from:
        errors.append(f"{path}: formula requires derived_from")
    return errors


def _check_sums_match_cases(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    sums = doc.get("sums") or {}
    arms = [a["id"] for a in doc.get("arms") or []]
    cases = doc.get("cases") or []

    def collect(arm_id: str, field: str) -> tuple[str, float | None]:
        values = []
        statuses = []
        for case in cases:
            result = (case.get("results") or {}).get(arm_id) or {}
            metric = result.get(field)
            if not metric:
                continue
            statuses.append(metric.get("status"))
            if metric.get("status") == "not_measured":
                continue
            if _is_number(metric.get("value")):
                values.append(float(metric["value"]))
        if not values and (not statuses or set(statuses) <= {"not_measured"}):
            return "not_measured", None
        status = "estimate" if "estimate" in statuses else "measured"
        return status, sum(values)

    for arm_id in arms:
        status, total = collect(arm_id, "cost_usd")
        listed = (sums.get("cost_usd") or {}).get(arm_id)
        if listed and status != "not_measured" and _is_number(total) and _is_number(listed.get("value")):
            if abs(listed["value"] - _round_money(total) if status != "estimate" else listed["value"] - total) > 0.05:
                # For estimate ranges, value may be the high; compare highs below.
                if listed.get("status") == "measured" and abs(listed["value"] - _round_money(total)) > 0.02:
                    errors.append(f"sums.cost_usd.{arm_id} is {listed['value']}, case sum is {_round_money(total)}")
        status, total = collect(arm_id, "wall_s")
        listed = (sums.get("wall_s") or {}).get(arm_id)
        if listed and listed.get("status") == "measured" and _is_number(total) and _is_number(listed.get("value")):
            if abs(listed["value"] - total) > 0.6:
                errors.append(f"sums.wall_s.{arm_id} is {listed['value']}, case sum is {total}")

        passed = 0
        known = 0
        for case in cases:
            result = (case.get("results") or {}).get(arm_id) or {}
            verdict = result.get("verdict")
            if verdict in {"pass", "fail", "incomplete"}:
                known += 1
                if verdict == "pass":
                    passed += 1
        listed = (sums.get("cases_passed") or {}).get(arm_id)
        if listed and listed.get("status") == "measured" and listed.get("value") != passed:
            errors.append(f"sums.cases_passed.{arm_id} is {listed.get('value')}, counted {passed}")
    return errors


def build(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValidationError("raw input is not an object")
    source_default = None
    sources = raw.get("sources") or []
    if sources:
        source_default = sources[0]["id"]
    if not source_default:
        raise ValidationError("raw input needs at least one source")

    cases_out: list[dict[str, Any]] = []
    for case in raw.get("cases") or []:
        results_out: dict[str, Any] = {}
        for arm_id, result in (case.get("results") or {}).items():
            source = result.get("source") or source_default
            results_out[arm_id] = _build_arm_result(result, source, raw.get("pass_labels") or ["pass"])
        cases_out.append({"id": case["id"], "label": case.get("label", case["id"]), "results": results_out})

    doc: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "title": raw["title"],
        "summary": raw.get("summary", ""),
        "last_updated": raw.get("last_updated", ""),
        "score_unit": raw["score_unit"],
        "subunit_kind": raw["subunit_kind"],
        "highlight_arm": raw["highlight_arm"],
        "baseline_arm": raw["baseline_arm"],
        "pass_labels": list(raw["pass_labels"]),
        "arms": raw["arms"],
        "sources": sources,
        "stage_names": raw.get("stage_names") or {},
        "cases": cases_out,
    }
    if raw.get("story_steps"):
        doc["story_steps"] = raw["story_steps"]
    if raw.get("findings"):
        doc["findings"] = raw["findings"]
    doc["sums"] = _build_sums(doc)
    if raw.get("waterfall"):
        doc["waterfall"] = _build_waterfall(raw["waterfall"], doc, source_default)
    errors = validate(doc)
    if errors:
        raise ValidationError("\n".join(errors))
    return doc


def _build_arm_result(result: dict[str, Any], source: str, pass_labels: list[str]) -> dict[str, Any]:
    subunits = []
    for item in result.get("subunits") or []:
        label = item["label"]
        passed = item.get("passed")
        if passed is None:
            passed = label in pass_labels if label != "not_measured" else None
        subunits.append({"id": item["id"], "label": label, "passed": passed})

    verdict = result.get("verdict", "not_measured")
    n_raw = result.get("n")
    passed_raw = result.get("passed")
    if subunits and n_raw is None:
        n_raw = len(subunits)
    if subunits and passed_raw is None and verdict != "not_measured":
        passed_raw = sum(1 for s in subunits if s["passed"] is True)

    out: dict[str, Any] = {
        "verdict": verdict,
        "score": {
            "passed": _wrap_metric(passed_raw, source),
            "n": _wrap_metric(n_raw, source),
        },
    }
    if "cost_usd" in result:
        out["cost_usd"] = _wrap_metric(result["cost_usd"], source, "usd")
    else:
        out["cost_usd"] = missing_metric()
    if "wall_s" in result:
        out["wall_s"] = _wrap_metric(result["wall_s"], source, "s")
    else:
        out["wall_s"] = missing_metric()
    for group, unit in (("tokens_by_stage", "tokens"), ("time_by_stage", "s"), ("cost_by_stage", "usd")):
        if group in result and isinstance(result[group], dict):
            out[group] = {name: _wrap_metric(value, source, unit) for name, value in result[group].items()}
    if subunits:
        out["subunits"] = subunits
    return out


def _build_sums(doc: dict[str, Any]) -> dict[str, Any]:
    arms = [a["id"] for a in doc["arms"]]
    cases = doc["cases"]
    sums: dict[str, Any] = {
        "note": SUMS_NOTE,
        "subunits_passed_not_a_score": True,
        "cost_usd": {},
        "wall_s": {},
        "cases_passed": {},
        "subunits_passed": {},
        "subunits_n": {},
    }

    def add_metric_group(field: str, dest: str, unit: str, money: bool = False) -> None:
        for arm_id in arms:
            statuses = []
            values = []
            lows = []
            highs = []
            paths = []
            for case in cases:
                metric = (case["results"].get(arm_id) or {}).get(field)
                if not metric:
                    continue
                paths.append(f"cases.{case['id']}.{arm_id}.{field}")
                statuses.append(metric["status"])
                if metric["status"] == "not_measured":
                    continue
                if _is_number(metric.get("value")):
                    values.append(float(metric["value"]))
                if _is_number(metric.get("low")):
                    lows.append(float(metric["low"]))
                elif _is_number(metric.get("value")):
                    lows.append(float(metric["value"]))
                if _is_number(metric.get("high")):
                    highs.append(float(metric["high"]))
                elif _is_number(metric.get("value")):
                    highs.append(float(metric["value"]))
            if not paths or set(statuses) <= {"not_measured"} or not values:
                sums[dest][arm_id] = missing_metric()
                continue
            status = "estimate" if "estimate" in statuses else "measured"
            total = sum(values)
            if money:
                total = _round_money(total)
            formula = f"sum({dest} over cases)"
            if status == "estimate":
                sums[dest][arm_id] = derived(
                    _round_money(sum(highs)) if highs else total,
                    paths,
                    formula,
                    unit,
                    status="estimate",
                    low=_round_money(sum(lows)) if lows else None,
                    high=_round_money(sum(highs)) if highs else None,
                )
            else:
                sums[dest][arm_id] = derived(total, paths, formula, unit)

    add_metric_group("cost_usd", "cost_usd", "usd", money=True)
    add_metric_group("wall_s", "wall_s", "s")

    for arm_id in arms:
        passed_cases = 0
        known = 0
        passed_sub = 0
        n_sub = 0
        paths_c = []
        paths_s = []
        any_measured = False
        for case in cases:
            result = case["results"].get(arm_id) or {}
            verdict = result.get("verdict")
            if verdict in {"pass", "fail", "incomplete"}:
                known += 1
                any_measured = True
                paths_c.append(f"cases.{case['id']}.{arm_id}.verdict")
                if verdict == "pass":
                    passed_cases += 1
            score = result.get("score") or {}
            if score.get("passed", {}).get("status") != "not_measured" and _is_number(score.get("passed", {}).get("value")):
                passed_sub += int(score["passed"]["value"])
                paths_s.append(f"cases.{case['id']}.{arm_id}.score.passed")
            if score.get("n", {}).get("status") != "not_measured" and _is_number(score.get("n", {}).get("value")):
                n_sub += int(score["n"]["value"])
        if not any_measured:
            sums["cases_passed"][arm_id] = missing_metric()
        else:
            sums["cases_passed"][arm_id] = derived(
                passed_cases, paths_c, "count of case verdicts equal to pass", unit="cases"
            )
        if not paths_s:
            sums["subunits_passed"][arm_id] = missing_metric()
            sums["subunits_n"][arm_id] = missing_metric()
        else:
            sums["subunits_passed"][arm_id] = derived(
                passed_sub, paths_s, "sum of per-case subunit passes (not a pooled score)", unit="tests"
            )
            sums["subunits_n"][arm_id] = derived(
                n_sub, paths_s, "sum of per-case subunit counts (not a pooled score)", unit="tests"
            )

    base = doc["baseline_arm"]
    high = doc["highlight_arm"]
    base_cost = sums["cost_usd"].get(base, {})
    high_cost = sums["cost_usd"].get(high, {})
    if base_cost.get("status") == "measured" and high_cost.get("status") == "measured":
        cut = (base_cost["value"] - high_cost["value"]) / base_cost["value"] * 100
        sums["cost_cut_pct"] = derived(
            round(cut, 1),
            ["sums.cost_usd." + base, "sums.cost_usd." + high],
            "(baseline - highlight) / baseline * 100",
            unit="pct",
        )
    else:
        sums["cost_cut_pct"] = missing_metric()
    base_wall = sums["wall_s"].get(base, {})
    high_wall = sums["wall_s"].get(high, {})
    if base_wall.get("status") == "measured" and high_wall.get("status") == "measured":
        cut = (base_wall["value"] - high_wall["value"]) / base_wall["value"] * 100
        sums["time_cut_pct"] = derived(
            round(cut, 1),
            ["sums.wall_s." + base, "sums.wall_s." + high],
            "(baseline - highlight) / baseline * 100",
            unit="pct",
        )
    else:
        sums["time_cut_pct"] = missing_metric()
    return sums


def _build_waterfall(raw: dict[str, Any], doc: dict[str, Any], source_default: str) -> dict[str, Any]:
    source = raw.get("source") or source_default
    start = doc["sums"]["cost_usd"][doc["baseline_arm"]]
    return {
        "title": raw["title"],
        "source": source,
        "start_label": raw["start_label"],
        "start_value": start,
        "end_label": raw["end_label"],
        "steps": [{"label": step["label"], "delta": _wrap_metric(step["delta"], source, "usd")} for step in raw["steps"]],
    }


def _load(path: Path) -> Any:
    return json.loads(path.read_text())


def _dump(doc: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    build_p = sub.add_parser("build", help="Build and validate a contract JSON from raw results")
    build_p.add_argument("--input", required=True)
    build_p.add_argument("--output", required=True)
    val_p = sub.add_parser("validate", help="Validate an existing contract JSON")
    val_p.add_argument("path")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "build":
            raw = _load(Path(args.input))
            doc = build(raw)
            _dump(doc, Path(args.output))
            print(f"wrote {args.output}")
            _print_headline(doc)
            return 0
        doc = _load(Path(args.path))
        errors = validate(doc)
        if errors:
            print("validation failed:", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            return 2
        print("ok")
        return 0
    except ValidationError as exc:
        print("validation failed:", file=sys.stderr)
        for line in str(exc).splitlines():
            print(f"  {line}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"bad input: {exc}", file=sys.stderr)
        return 2


def _print_headline(doc: dict[str, Any]) -> None:
    sums = doc["sums"]
    base, high = doc["baseline_arm"], doc["highlight_arm"]
    print("cases_passed", {k: display_metric(v) for k, v in sums["cases_passed"].items()})
    print("cost_usd", {k: display_metric(v, "usd") for k, v in sums["cost_usd"].items()})
    print("wall_s", {k: display_metric(v, "s") for k, v in sums["wall_s"].items()})
    print("cost_cut_pct", display_metric(sums.get("cost_cut_pct")))
    print("time_cut_pct", display_metric(sums.get("time_cut_pct")))


if __name__ == "__main__":
    sys.exit(main())
