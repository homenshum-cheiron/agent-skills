#!/usr/bin/env python3
"""Check a self-review gate record and say whether the agent may act.

Offline and standard library only. It checks bookkeeping: that each required
step was recorded, passed, and points at evidence. It does not run the checks,
judge whether the review was good, or grant permission the owner has not given.

Exit codes: 0 act, 1 blocked (fix and rerun), 2 needs the owner, 3 revert now.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

ACT, BLOCKED, NEEDS_OWNER, REVERT = "act", "blocked", "needs-owner", "revert"
EXIT = {ACT: 0, BLOCKED: 1, NEEDS_OWNER: 2, REVERT: 3}

# Categories that always need the owner, whatever tier the record claims.
OWNER_ONLY = {
    "external-send",      # chat, email, social, or any message other people read
    "shared-merge",       # merge, undraft, or queue on a repository other people own
    "secret",             # reading, printing, moving, or rotating a credential
    "paid-over-cap",      # spend above the owner's stated cap
    "delete-user-data",   # deleting data that is not a regenerable cache
    "kill-process",       # stopping a process the agent did not start
    "infra-restart",      # restarting a shared runtime, VM, or container host
    "answer-key",         # opening or editing sealed grading material
    "force-push",         # rewriting history that has been pushed
    "skip-checks",        # bypassing hooks, CI, or a pre-check
    "permission-change",  # widening the agent's own permissions or scope
}
FINDING_OK = {"fixed", "rejected", "duplicate"}
REVIEWER_KINDS = {"other-model", "fresh-context"}
SHA = re.compile(r"^[0-9a-f]{7,40}$")


def _nonempty(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _checks_pass(checks, label, tip, findings):
    if not isinstance(checks, list) or not checks:
        findings.append(f"{label}: no checks recorded")
        return False
    ok = True
    for i, check in enumerate(checks):
        where = f"{label}[{i}]"
        if not isinstance(check, dict):
            findings.append(f"{where}: not an object")
            ok = False
            continue
        if not _nonempty(check.get("command")):
            findings.append(f"{where}: command missing")
            ok = False
        if check.get("exit_code") != 0:
            findings.append(f"{where}: exit_code is {check.get('exit_code')!r}, not 0")
            ok = False
        if not _nonempty(check.get("observed")):
            findings.append(f"{where}: observed output missing")
            ok = False
        if tip and check.get("revision") not in (None, tip):
            findings.append(f"{where}: ran on {check.get('revision')}, not the tip {tip}")
            ok = False
    return ok


def check(record: dict) -> dict:
    """Return {'verdict', 'tier', 'findings'} for one gate record."""
    findings: list[str] = []
    if not isinstance(record, dict):
        return {"verdict": BLOCKED, "tier": None, "findings": ["record is not a JSON object"]}

    tier = record.get("tier")
    if tier not in (0, 1, 2):
        findings.append("tier must be 0, 1, or 2")
        return {"verdict": BLOCKED, "tier": tier, "findings": findings}

    categories = set(record.get("categories") or [])
    owner_hits = sorted(categories & OWNER_ONLY)
    if owner_hits:
        findings.append("owner-only categories: " + ", ".join(owner_hits))
    if record.get("reversible") is not True:
        findings.append("action is not marked reversible")
    if tier == 2 or owner_hits or record.get("reversible") is not True:
        return {"verdict": NEEDS_OWNER, "tier": 2, "findings": findings}

    if not _nonempty(record.get("action")):
        findings.append("action missing")
    if tier == 0:
        if not _nonempty(record.get("revert")):
            findings.append("revert path missing")
        verdict = ACT if not findings else BLOCKED
        return _after(record, verdict, 0, findings)

    # Tier 1: every step must be present and green before acting.
    tip = record.get("tip")
    if not (isinstance(tip, str) and SHA.match(tip)):
        findings.append("tip must be a commit SHA (a branch name is not a revision)")
        tip = None
    if not _nonempty(record.get("blast_radius")):
        findings.append("blast_radius missing")
    if not _nonempty(record.get("revert")):
        findings.append("revert path missing")
    _checks_pass(record.get("checks"), "checks", tip, findings)

    review = record.get("review")
    if not isinstance(review, dict):
        findings.append("review missing")
    else:
        if review.get("kind") not in REVIEWER_KINDS:
            findings.append("review.kind must be other-model or fresh-context")
        if review.get("author_is_reviewer") is not False:
            findings.append("review must come from an agent that did not write the change")
        if review.get("saw_author_reasoning") is not False:
            findings.append("reviewer must judge the diff and evidence, not the author's reasoning")
        if tip and review.get("revision") != tip:
            findings.append(f"review covers {review.get('revision')!r}, not the tip {tip}")
        if not _nonempty(review.get("evidence")):
            findings.append("review.evidence missing (path or link to the reviewer's output)")
        for i, item in enumerate(review.get("findings") or []):
            disposition = (item or {}).get("disposition")
            if disposition not in FINDING_OK:
                findings.append(f"review.findings[{i}] is {disposition!r}; unresolved findings block")
            elif disposition in {"fixed", "rejected"} and not _nonempty((item or {}).get("evidence")):
                findings.append(f"review.findings[{i}] is {disposition} without evidence")

    verdict = ACT if not findings else BLOCKED
    return _after(record, verdict, 1, findings)


def _after(record, verdict, tier, findings):
    """Apply the post-action check when one is recorded."""
    post = record.get("post_verify")
    if verdict == ACT and post is not None:
        post_findings: list[str] = []
        if not _checks_pass(post if isinstance(post, list) else [post], "post_verify", None, post_findings):
            findings.extend(post_findings)
            return {"verdict": REVERT, "tier": tier, "findings": findings}
    return {"verdict": verdict, "tier": tier, "findings": findings}


def _cell(value) -> str:
    text = re.sub(r"[\t\r\n]+", " ", str(value)).strip()
    return "'" + text if text[:1] in {"=", "+", "-", "@"} else text


def log_row(path: Path, record: dict, result: dict) -> None:
    """Append one decision-trail row (show-me-your-work TSV columns)."""
    header = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
    new = not path.exists() or path.stat().st_size == 0
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    why = "; ".join(result["findings"]) or f"tier {result['tier']} gate passed"
    evidence = record.get("evidence") or (record.get("review") or {}).get("evidence") or ""
    row = [ts, "gate", record.get("action", ""), why, evidence, result["verdict"]]
    with path.open("a", encoding="utf-8") as handle:
        if new:
            handle.write(header)
        handle.write("\t".join(_cell(c) for c in row) + "\n")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("record", type=Path, help="gate record JSON")
    parser.add_argument("--log", type=Path, help="append a row to this decisions TSV")
    args = parser.parse_args(argv)
    try:
        record = json.loads(args.record.read_text())
    except (OSError, json.JSONDecodeError) as error:
        print(f"blocked: cannot read record: {error}")
        return EXIT[BLOCKED]
    result = check(record)
    if args.log:
        log_row(args.log, record, result)
    print(f"{result['verdict']} (tier {result['tier']})")
    for finding in result["findings"]:
        print(f"- {finding}")
    return EXIT[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
