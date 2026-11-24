#!/usr/bin/env python3
"""Decide the highest model tier a run may use right now, and log the decision. It selects no model and calls no provider.

Rule:
  In a deep block     only the active phase (phase_id in today.json) may use the top tier. Other runs are capped at mid.
  Outside a block     the top tier needs a phase tag (any phase id). A run with no tag is capped at mid.
Tiers are top, mid and cheap. Map your own models to tiers in your own router; this file knows no model names.
No active phase (today.json missing, unreadable, empty, or dated another day) means that in a block every run is capped.

Every run appends one line to <FOCUS_DIR>/models.jsonl: {ts, phase_id, tier, in_block, wanted, capped, reason}.
Deep blocks, zone, state folder and test clock: the same settings as focus_check.py (FOCUS_BLOCKS, FOCUS_TZ, FOCUS_DIR, FOCUS_NOW).

Usage: tier_route.py --want top|mid|cheap [--phase PHASE_ID] [--no-log]   |   --selftest
Prints one JSON line. Exit 0 also when the run is capped: read "tier" and "capped".
"""
import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import focus_check as fc   # noqa: E402  (same folder: blocks, clock, state folder)

ORDER = ("cheap", "mid", "top")


def active_phase(now):
    """(phase id or None, why there is none). Never raises: a broken file means no active phase."""
    try:
        today = fc.jf("today.json")
    except (OSError, ValueError):
        return None, "today.json is unreadable"
    if not isinstance(today, dict) or not fc.text(today.get("phase_id")):
        return None, "no phase is picked in today.json"
    if today.get("date") and today["date"] != now.astimezone(fc.zone()).date().isoformat():
        return None, f"today.json is dated {today['date']}, not today"
    return today["phase_id"].strip(), ""


def decide(want, phase=None, now=None):
    """Pure decision plus the row to log. want: the tier the caller would like. phase: the phase this run works on."""
    if want not in ORDER:
        raise ValueError(f"tier must be one of {ORDER}")
    now = now or fc.now()
    phase = fc.text(phase) or None
    inside = fc.in_block(now)
    active, why = active_phase(now)
    if inside:
        cap = phase is None or phase != active
        reason = (f"deep block and {phase} is the active phase: top allowed" if not cap else
                  f"deep block: top is only for the active phase ({active or 'none: ' + why}); this run is "
                  + (f"tagged {phase}" if phase else "untagged"))
    else:
        cap = phase is None
        reason = "outside deep blocks: " + (f"tagged {phase}, top allowed" if phase else "top needs a phase tag")
    tier = "mid" if cap and want == "top" else want
    return {"ts": now.astimezone(fc.zone()).isoformat(timespec="seconds"), "phase_id": phase, "tier": tier, "in_block": inside,
            "wanted": want, "capped": tier != want, "reason": reason}


def log(row):
    os.makedirs(fc.state_dir(), exist_ok=True)
    with open(fc.path("models.jsonl"), "a") as fh:
        fh.write(json.dumps(row) + "\n")


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.environ.update(FOCUS_DIR=d, FOCUS_BLOCKS="09:30-11:30,14:00-16:00", FOCUS_TZ="UTC")
        at = lambda s: fc.parse(s)
        tue, sat = "2031-03-04T", "2031-03-08T"
        with open(os.path.join(d, "today.json"), "w") as fh:
            json.dump({"phase_id": "P1"}, fh)
        assert decide("top", "P1", at(tue + "10:00:00+00:00"))["tier"] == "top"        # in block, active phase
        assert decide("top", "P2", at(tue + "10:00:00+00:00"))["tier"] == "mid"        # in block, other phase
        assert decide("top", None, at(tue + "10:00:00+00:00"))["capped"]               # in block, untagged
        assert decide("cheap", None, at(tue + "10:00:00+00:00"))["tier"] == "cheap"    # a cap never raises a tier
        assert decide("top", None, at(tue + "12:00:00+00:00"))["tier"] == "mid"        # outside, untagged
        assert decide("top", "P9", at(tue + "12:00:00+00:00"))["tier"] == "top"        # outside, any tag
        assert not decide("top", "P2", at(sat + "10:00:00+00:00"))["in_block"]         # weekend
        for hm, want in (("09:29", False), ("09:30", True), ("11:29", True), ("11:30", False), ("13:59", False), ("14:00", True), ("16:00", False)):
            assert decide("mid", "P1", at(f"{tue}{hm}:00+00:00"))["in_block"] is want, hm
        for broken in ("{not json", "[]", "{}"):
            with open(os.path.join(d, "today.json"), "w") as fh:
                fh.write(broken)
            row = decide("top", "P1", at(tue + "10:00:00+00:00"))
            assert row["tier"] == "mid" and "active phase (none" in row["reason"], row
        log(row)
        with open(os.path.join(d, "models.jsonl")) as fh:
            assert {"ts", "phase_id", "tier", "in_block"} <= set(json.loads(fh.read()))
    print("selftest: block, phase, weekend, boundary and broken-file cases behave as documented (synthetic state)")
    return 0


def main(argv):
    if argv[:1] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description="Highest model tier allowed now.")
    ap.add_argument("--want", required=True, choices=ORDER)
    ap.add_argument("--phase", default=os.environ.get("FOCUS_PHASE", ""))
    ap.add_argument("--no-log", action="store_true")
    args = ap.parse_args(argv)
    row = decide(args.want, args.phase)
    if not args.no_log:
        try:
            log(row)
        except OSError as e:
            print(f"could not append models.jsonl: {e}", file=sys.stderr)
    print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
