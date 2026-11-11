#!/usr/bin/env python3
"""Validate local proof bookkeeping, not test authenticity or review quality."""
import argparse
import hashlib
import json
from pathlib import Path
import re

STATES = {"complete": 0, "failed": 1, "inconclusive": 2, "invalid": 3}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def evaluate(packet, base):
    invalid, gaps, failures = [], [], []
    base = Path(base).resolve()
    if not isinstance(packet, dict):
        return {"status": "invalid", "findings": ["Packet must be an object."]}
    if type(packet.get("schema_version")) is not int or packet["schema_version"] != 1:
        invalid.append("schema_version must be 1.")
    for key in ("artifact_revision", "reviewed_revision", "scope"):
        if not nonempty(packet.get(key)):
            invalid.append(f"{key} must be a nonempty string.")
    if packet.get("artifact_revision") != packet.get("reviewed_revision"):
        gaps.append("The reviewed revision differs from the artifact revision.")
    checks = packet.get("checks")
    if not isinstance(checks, list) or not checks:
        return {"status": "invalid", "findings": invalid + ["checks must be a nonempty list."]}
    ids = set()
    for index, check in enumerate(checks):
        label = f"checks[{index}]"
        if not isinstance(check, dict):
            invalid.append(f"{label} must be an object.")
            continue
        cid = check.get("id")
        if not nonempty(cid) or cid in ids:
            invalid.append(f"{label} needs a unique nonempty id.")
        else:
            ids.add(cid)
            label = cid
        status = check.get("status")
        if not isinstance(status, str) or status not in {"passed", "failed", "blocked", "not_run"}:
            invalid.append(f"{label}: invalid status.")
        if not nonempty(check.get("command")):
            invalid.append(f"{label}: command is required.")
        if isinstance(status, str) and status in {"passed", "failed"}:
            if type(check.get("exit_code")) is not int:
                invalid.append(f"{label}: executed check needs integer exit_code.")
            elif status == "passed" and check["exit_code"] != 0:
                invalid.append(f"{label}: passed check has nonzero exit_code.")
            if status == "failed":
                failures.append(f"{label}: declared failed.")
        elif isinstance(status, str) and status in {"blocked", "not_run"}:
            if not nonempty(check.get("reason")):
                invalid.append(f"{label}: missing reason for {status}.")
            if "exit_code" in check:
                invalid.append(f"{label}: unexecuted check cannot have exit_code.")
            gaps.append(f"{label}: {status}.")
        evidence = check.get("evidence")
        if not isinstance(evidence, list):
            invalid.append(f"{label}: evidence must be a list.")
            continue
        if isinstance(status, str) and status in {"passed", "failed"} and not evidence:
            gaps.append(f"{label}: executed check has no evidence.")
        for item in evidence:
            if not isinstance(item, dict) or not nonempty(item.get("path")):
                invalid.append(f"{label}: evidence needs a relative path.")
                continue
            digest = item.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                invalid.append(f"{label}: invalid evidence sha256.")
                continue
            rel = Path(item["path"])
            if rel.is_absolute() or ".." in rel.parts:
                invalid.append(f"{label}: evidence path escapes packet directory.")
                continue
            target = base / rel
            # Reject links before resolve, including links in parent directories.
            cursor = base
            unsafe = False
            for part in rel.parts:
                cursor = cursor / part
                if cursor.is_symlink():
                    unsafe = True
                    break
            if unsafe:
                invalid.append(f"{label}: symlink evidence is not accepted.")
                continue
            try:
                target.resolve().relative_to(base)
                if not target.is_file():
                    gaps.append(f"{label}: evidence file missing: {rel}.")
                    continue
                data = target.read_bytes()
            except (OSError, ValueError):
                gaps.append(f"{label}: evidence file unreadable: {rel}.")
                continue
            if not data:
                gaps.append(f"{label}: evidence file empty: {rel}.")
            elif hashlib.sha256(data).hexdigest() != digest:
                gaps.append(f"{label}: evidence hash differs: {rel}.")
    status = "invalid" if invalid else "failed" if failures else "inconclusive" if gaps else "complete"
    return {"status": status, "findings": invalid + failures + gaps,
            "limit": "Bookkeeping only; test relevance, authenticity, coverage and release approval are not established."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.packet.read_text()), args.packet.parent)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"status": "invalid", "findings": [str(exc)]}
    print(json.dumps(result, indent=2))
    return STATES[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
