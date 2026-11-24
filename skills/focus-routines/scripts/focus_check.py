#!/usr/bin/env python3
"""Checks for the focus routines. Each one can fail, so a rule is more than a wish.

Reads small state files in one folder (FOCUS_DIR, default ~/.focus). Shapes: references/state-files.md.
Verdicts: passed / failed / unverified (no data to judge) / inconclusive (a state file is unreadable).
Exit code: 1 if any check failed; else 2 if any is unverified or inconclusive; else 0. Usage error: 64.
Missing data is never "passed". The checks prove shape and timing. They do not prove that a file tells the truth.

Settings (environment):
  FOCUS_DIR          state folder
  FOCUS_BLOCKS       deep blocks, clock time, start included and end excluded. Default 09:30-11:30,14:00-16:00 (an example)
  FOCUS_TZ           zone name for the blocks and for "today". Default: the system zone
  FOCUS_SWITCH_CAP   active threads allowed outside a block (default 3). In a block the cap is 1
  FOCUS_CRITIC_KINDS source kinds the critic must read. Default messages,reviews,calendar,state
  FOCUS_NOW          a fixed clock for tests (ISO time)
Deep blocks apply Monday to Friday.

Usage: focus_check.py all | <check>... | gate-open <phase_id> | --selftest
"""
import datetime as dt
import json
import os
import re
import sys
import tempfile

P, F, U = "passed", "failed", "unverified"
STALE_H = 26      # a snapshot or a critic run older than this is stale
WINDOW_H = 24     # log checks read this many hours back
TIERS = {"top", "mid", "cheap"}
VERDICTS = {"in_phase", "batch", "park", "no"}
PLAN_FILE = re.compile(r"(^|/)(today|phases)\.json$|(^|/)plan[^/]*\.(md|json)$", re.I)


def state_dir():
    return os.environ.get("FOCUS_DIR") or os.path.join(os.path.expanduser("~"), ".focus")


def blocks():
    raw = os.environ.get("FOCUS_BLOCKS") or "09:30-11:30,14:00-16:00"
    return tuple(tuple(x.strip() for x in b.split("-", 1)) for b in raw.split(",") if "-" in b)


def zone():
    name = os.environ.get("FOCUS_TZ")
    if not name:
        return None   # the system zone
    from zoneinfo import ZoneInfo
    return ZoneInfo(name)


def parse(s):
    t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=zone()) if zone() else t.astimezone()


def now():
    return parse(os.environ["FOCUS_NOW"]) if os.environ.get("FOCUS_NOW") else dt.datetime.now().astimezone()


def in_block(t):
    """True when the aware datetime t is inside a deep block."""
    local = t.astimezone(zone())
    hm = local.strftime("%H:%M")
    return local.weekday() < 5 and any(a <= hm < b for a, b in blocks())


def path(name):
    return os.path.join(state_dir(), name)


def has(name):
    return os.path.exists(path(name))


def jf(name, default=None):
    if not has(name):
        return default
    with open(path(name)) as f:
        return json.load(f)


def jl(name):
    if not has(name):
        return []
    with open(path(name)) as f:
        return [json.loads(line) for line in f if line.strip()]


def text(x):
    return x.strip() if isinstance(x, str) else ""


def age_h(s):
    return (now() - parse(s)).total_seconds() / 3600


def recent(rows):
    return [r for r in rows if "ts" not in r or age_h(r["ts"]) <= WINDOW_H]


def row_in_block(r):
    """The clock decides. The logged in_block flag counts only for a row with no time."""
    return in_block(parse(r["ts"])) if "ts" in r else bool(r.get("in_block"))


def active_ids():
    return [p.get("id") for p in jf("phases.json", []) if p.get("status") == "active"]


def v(ok):
    return P if ok else F


def one_active():
    if not has("phases.json"):
        return U, "phases.json missing: no phase list yet"
    a = active_ids()
    return v(len(a) == 1), f"{len(a)} active phases (need exactly 1): {a}"


def done_picture():
    t = jf("today.json")
    if not t:
        return F, "today.json missing or empty: no phase picked"
    first = t.get("first_step") or {}
    today = now().astimezone(zone()).date().isoformat()
    miss = [k for k, ok in ((f"date == {today}", t.get("date") == today),
                            ("done_picture", text(t.get("done_picture"))),
                            ("first_step.when", text(first.get("when"))),
                            ("first_step.action", text(first.get("action"))),
                            ("phase_id == the active phase", t.get("phase_id") in active_ids())) if not ok]
    return v(not miss), f"today.json missing or wrong: {miss}"


def switch_cap():
    rows = recent(jl("switches.jsonl"))
    if not rows:
        return U, f"no switch samples in the last {WINDOW_H} h"
    cap = lambda r: 1 if row_in_block(r) else int(os.environ.get("FOCUS_SWITCH_CAP", "3"))
    bad = [r for r in rows if len(set(r["active_threads"])) > cap(r)]   # a later clean sample does not erase a breach
    return v(not bad), f"{len(bad)} of {len(rows)} samples over the cap (1 in a deep block, else {os.environ.get('FOCUS_SWITCH_CAP', '3')})"


def no_interrupt():
    if not has("parking.jsonl"):
        return U, "parking.jsonl missing: the say-no step has not run"
    rows = recent(jl("parking.jsonl"))
    unknown = [r.get("verdict") for r in rows if r.get("verdict") not in VERDICTS]
    if unknown:
        return F, f"{len(unknown)} rows with an unknown verdict: {unknown[:5]}"
    if not rows:   # an empty log cannot tell a quiet day from a step that did not run
        return U, f"no asks logged in the last {WINDOW_H} h"
    bad = [r for r in rows if r.get("surfaced_during_block") and r["verdict"] != "in_phase" and r.get("urgent") is not True]
    return v(not bad), f"{len(bad)} asks that were not phase work and not urgent reached the person during a deep block ({len(rows)} rows)"


def snapshot_fresh():
    if not has("phases.json"):
        return U, "phases.json missing"
    bad = []
    for p in jf("phases.json"):
        if p.get("status") == "closed":
            continue
        step = p.get("next_step") or {}
        if not text(step.get("when")) or not text(step.get("action")):
            bad.append(f"{p.get('id')}: no next step")
        elif "updated" not in p or age_h(p["updated"]) > STALE_H:
            bad.append(f"{p.get('id')}: stale")
    return v(not bad), f"open phases with no concrete next step, or older than {STALE_H} h: {bad}"


def model_tier():
    if not has("models.jsonl"):
        return U, "models.jsonl missing: no run was logged"
    rows = recent(jl("models.jsonl"))
    unknown = [r.get("tier") for r in rows if r.get("tier") not in TIERS]
    if unknown:
        return F, f"{len(unknown)} rows with an unknown tier: {unknown[:5]}"
    act = set(active_ids())
    inside = [r for r in rows if row_in_block(r)]
    off = [r for r in inside if r["tier"] == "top" and r.get("phase_id") not in act]
    under = [r for r in inside if r.get("phase_id") in act and r["tier"] == "cheap"]
    untagged = [r for r in rows if not row_in_block(r) and r["tier"] == "top" and not text(r.get("phase_id"))]
    return (v(not off and not under and not untagged),
            f"in a block: {len(off)} top runs off the active phase, {len(under)} cheap runs on it; "
            f"outside: {len(untagged)} top runs with no phase tag ({len(rows)} rows)")


def critic_blind():
    """The critic must rank from its own search, not from the plan. This trusts the critic's own source list."""
    c = jf("critic.json")
    if not c:
        return U, "no critic run yet"
    if "ts" not in c or age_h(c["ts"]) > STALE_H:
        return F, f"critic.json has no time or is older than {STALE_H} h"
    need = {k.strip() for k in (os.environ.get("FOCUS_CRITIC_KINDS") or "messages,reviews,calendar,state").split(",") if k.strip()}
    src = c.get("sources_read") or []
    kinds = {s.get("kind") for s in src if text(s.get("ref"))}
    leaked = [s["ref"] for s in src if PLAN_FILE.search(os.path.normpath(str(s.get("ref", ""))).replace(os.sep, "/"))]
    items = c.get("ranking") or []
    thin = [i.get("id") for i in items if not text(i.get("bigger_picture")) or not text(i.get("block")) or not i.get("evidence")]
    ok = need <= kinds and not leaked and bool(items) and not thin
    return v(ok), (f"kinds read {sorted(k for k in kinds if k)} (need {sorted(need)}); plan files read {leaked}; "
                   f"{len(items)} ranked items; items with no bigger picture, block or evidence {thin}; source list is self-reported")


def gate_open(pid):
    if not has("phases.json"):
        return U, "phases.json missing"
    for p in jf("phases.json"):
        if p.get("status") == "active" and p.get("id") != pid:
            crit, met = p.get("exit_criteria") or [], p.get("exit_met") or []
            if not crit or len(met) != len(crit) or not all(m is True for m in met):
                return F, f"phase {p.get('id')} is still open: finish it or park it first"
            return F, f"phase {p.get('id')} met its exit criteria but is still active: close it first"
    return P, f"ok to open {pid}"


CHECKS = {"one_active": one_active, "done_picture": done_picture, "switch_cap": switch_cap, "no_interrupt": no_interrupt,
          "snapshot_fresh": snapshot_fresh, "model_tier": model_tier, "critic_blind": critic_blind}


def safe(name, fn, *args):
    try:
        verdict, detail = fn(*args)
    except Exception as e:   # an unreadable file must not look like a verdict on the rule
        verdict, detail = "inconclusive", f"state unreadable: {type(e).__name__}: {e}"
    return {"check": name, "verdict": verdict, "pass": verdict == P, "detail": detail}


def exit_code(results):
    verdicts = {r["verdict"] for r in results}
    return 1 if F in verdicts else 2 if verdicts - {P} else 0


def selftest():
    """Synthetic state in a temporary folder: every fail path fires, missing data is unverified, and one clean day passes."""
    with tempfile.TemporaryDirectory() as d:
        os.environ.update(FOCUS_DIR=d, FOCUS_NOW="2031-03-04T10:00:00+00:00", FOCUS_BLOCKS="09:30-11:30", FOCUS_TZ="UTC")
        put = lambda n, o: open(os.path.join(d, n), "w").write(o if isinstance(o, str) else json.dumps(o))
        line = lambda **k: json.dumps(k) + "\n"
        iso = "2031-03-04T09:45:00+00:00"   # a Tuesday, inside the block
        assert all(safe(n, f)["verdict"] in (U, F) for n, f in CHECKS.items()), "an empty folder must not pass anything"
        put("phases.json", [{"id": "P1", "status": "active", "exit_criteria": ["a", "b"], "exit_met": [True, False],
                             "next_step": {"when": "10:30", "action": "open the parser test"}, "updated": iso},
                            {"id": "P2", "status": "queued", "next_step": {"when": "", "action": ""}, "updated": iso}])
        put("today.json", {"date": "2031-03-04", "phase_id": "P1", "done_picture": "parser test green",
                           "first_step": {"when": "09:30", "where": "desk", "action": "open the parser test"}})
        assert one_active()[0] == P and done_picture()[0] == P
        assert snapshot_fresh()[0] == F and gate_open("P2")[0] == F          # P2 has no next step; P1 is still open
        put("switches.jsonl", line(ts=iso, active_threads=["a", "b"]));       assert switch_cap()[0] == F
        put("parking.jsonl", line(ts=iso, ask="q", verdict="park", surfaced_during_block=True)); assert no_interrupt()[0] == F
        put("models.jsonl", line(ts=iso, phase_id="P2", tier="top", in_block=False)); assert model_tier()[0] == F   # the clock wins over the flag
        put("critic.json", {"ts": iso, "sources_read": [{"kind": "reviews", "ref": "r1"}, {"kind": "state", "ref": "focus/today.json"}],
                            "ranking": [{"id": "x", "bigger_picture": "", "block": "deep1", "evidence": ["r1"]}]})
        assert critic_blind()[0] == F
        put("today.json", "{not json");                                       assert safe("done_picture", done_picture)["verdict"] == "inconclusive"
        # one clean day
        put("phases.json", [{"id": "P1", "status": "active", "exit_criteria": ["a"], "exit_met": [False],
                             "next_step": {"when": "10:30", "action": "open the parser test"}, "updated": iso}])
        put("today.json", {"date": "2031-03-04", "phase_id": "P1", "done_picture": "parser test green",
                           "first_step": {"when": "09:30", "where": "desk", "action": "open the parser test"}})
        put("switches.jsonl", line(ts=iso, active_threads=["P1"]))
        put("parking.jsonl", line(ts=iso, ask="q", verdict="batch", surfaced_during_block=False))
        put("models.jsonl", line(ts=iso, phase_id="P1", tier="top", in_block=True))
        put("critic.json", {"ts": iso, "sources_read": [{"kind": k, "ref": k + "-1"} for k in ("messages", "reviews", "calendar", "state")],
                            "ranking": [{"id": "x", "bigger_picture": "ship the parser", "block": "deep1", "evidence": ["reviews-1"]}]})
        results = [safe(n, f) for n, f in CHECKS.items()]
        assert exit_code(results) == 0, results
    print("selftest: 8 fail paths, 1 inconclusive path and 1 clean day behave as documented (synthetic state)")
    return 0


def main(argv):
    argv = argv or ["all"]
    if argv[0] == "--selftest":
        return selftest()
    if argv[0] == "gate-open":
        if len(argv) != 2:
            print("usage: focus_check.py gate-open <phase_id>", file=sys.stderr)
            return 64
        results = [safe("phase_gate", gate_open, argv[1])]
    else:
        names = list(CHECKS) if argv[0] == "all" else argv
        unknown = [n for n in names if n not in CHECKS]
        if unknown:
            print(f"unknown check(s) {unknown}; known: {sorted(CHECKS)}", file=sys.stderr)
            return 64
        results = [safe(n, CHECKS[n]) for n in names]
    for r in results:
        print(json.dumps(r))
    return exit_code(results)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
