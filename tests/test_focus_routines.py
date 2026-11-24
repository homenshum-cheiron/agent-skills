"""Focus routines: state checks, design-first gate, tier decision and the example hook, on synthetic state and throwaway
repositories. This proves the helpers behave as documented. It is not evidence that the routines shorten real work."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "focus-routines"
SCRIPTS = SKILL / "scripts"
TUE = "2031-03-04"                       # a Tuesday
IN_BLOCK = TUE + "T10:00:00+00:00"
STAMP = TUE + "T09:45:00+00:00"
SETTINGS = {"FOCUS_BLOCKS": "09:30-11:30,14:00-16:00", "FOCUS_TZ": "UTC"}
STRAY = ("FOCUS_PHASE", "FOCUS_SWITCH_CAP", "FOCUS_CRITIC_KINDS", "DESIGN_LEDGER", "DESIGN_MIN_LINES",
         "DESIGN_EXEMPT_LINES", "DESIGN_GATE_LANES")


def env(state, now=IN_BLOCK, **extra):
    base = {k: v for k, v in os.environ.items() if k not in STRAY}
    return {**base, **SETTINGS, "FOCUS_DIR": str(state), "FOCUS_NOW": now, **extra}


def script(name, *args, **kw):
    r = subprocess.run([sys.executable, str(SCRIPTS / name), *args], capture_output=True, text=True, **kw)
    rows = [json.loads(line) for line in r.stdout.splitlines() if line.startswith("{")]
    return r.returncode, rows, r.stderr


def put(folder, name, value):
    Path(folder, name).write_text(value if isinstance(value, str) else json.dumps(value))


def rows(*items):
    return "".join(json.dumps(i) + "\n" for i in items)


def clean_day(d):
    put(d, "phases.json", [{"id": "P1", "status": "active", "exit_criteria": ["a"], "exit_met": [False],
                            "next_step": {"when": "10:30", "action": "open the parser test"}, "updated": STAMP}])
    put(d, "today.json", {"date": TUE, "phase_id": "P1", "done_picture": "parser test green",
                          "first_step": {"when": "09:30", "where": "desk", "action": "open the parser test"}})
    put(d, "switches.jsonl", rows({"ts": STAMP, "active_threads": ["P1"]}))
    put(d, "parking.jsonl", rows({"ts": STAMP, "ask": "q", "verdict": "batch", "surfaced_during_block": False}))
    put(d, "models.jsonl", rows({"ts": STAMP, "phase_id": "P1", "tier": "top", "in_block": True}))
    put(d, "critic.json", {"ts": STAMP,
                           "sources_read": [{"kind": k, "ref": k + "-1"} for k in ("messages", "reviews", "calendar", "state")],
                           "ranking": [{"id": "x", "bigger_picture": "ship the parser", "block": "deep1", "evidence": ["reviews-1"]}]})


class Folder(unittest.TestCase):
    def test_files_present(self):
        for relative in ("SKILL.md", "DESIGN.md", "references/routines.md", "references/state-files.md", "examples/worked.md",
                         "examples/pre-push", "examples/design-gate.conf.example", "scripts/focus_check.py",
                         "scripts/design_gate.py", "scripts/tier_route.py"):
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_frontmatter_and_principle_index(self):
        text = (SKILL / "SKILL.md").read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
        self.assertIn("name: focus-routines", front)
        indexed = re.findall(r"\(\*\*(principle-[a-z0-9-]+)\*\*\)", text)
        self.assertEqual(sorted(indexed), [p.parent.name for p in PRINCIPLES])
        self.assertEqual(len(indexed), 11)


PRINCIPLES = sorted((ROOT / "skills").glob("principle-*/SKILL.md"))
FOCUS_PRINCIPLES = [p for p in PRINCIPLES if "focus-routines" in p.read_text()]


class Principles(unittest.TestCase):
    """One principle per skill, pstack-style: short body, Apply-when trigger, named check, synthetic example."""

    def test_every_principle_skill_belongs_to_focus_routines(self):
        self.assertEqual(PRINCIPLES, FOCUS_PRINCIPLES)
        self.assertEqual(len(PRINCIPLES), 11)

    def test_frontmatter_parses(self):
        for path in PRINCIPLES:
            text = path.read_text()
            front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
            self.assertIsNotNone(front, path)
            fields = dict(line.split(": ", 1) for line in front.group(1).splitlines())
            self.assertEqual(set(fields), {"name", "description", "disable-model-invocation"}, path)
            self.assertEqual(fields["name"], path.parent.name)
            self.assertEqual(fields["disable-model-invocation"], "true")
            desc = json.loads(fields["description"])
            self.assertTrue(desc.startswith("Apply "), path)

    def test_short_body_names_its_check(self):
        for path in PRINCIPLES:
            body = path.read_text().split("---\n", 2)[2]
            self.assertLess(len(body.split()), 220, path)
            self.assertRegex(body, r"\*\*Check:\*\* .*\*\*focus-routines\*\*", path)

    def test_worked_example_synthetic_and_listed_in_readme(self):
        readme = (ROOT / "README.md").read_text()
        for path in PRINCIPLES:
            self.assertIn("synthetic", (path.parent / "examples" / "worked.md").read_text().splitlines()[0])
            self.assertIn(f"skills/{path.parent.name}/SKILL.md", readme)

    def test_worked_example_is_labelled_synthetic(self):
        self.assertIn("synthetic", (SKILL / "examples" / "worked.md").read_text().splitlines()[0])

    def test_selftests(self):
        for name in ("focus_check.py", "design_gate.py", "tier_route.py"):
            with tempfile.TemporaryDirectory() as d:
                code, _, err = script(name, "--selftest", env=env(d))
                self.assertEqual(code, 0, f"{name}: {err}")


class FocusCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d = self.tmp.name

    def run_check(self, *args, **extra):
        code, out, err = script("focus_check.py", *args, env=env(self.d, **extra))
        return code, {r["check"]: r["verdict"] for r in out}, err

    def test_empty_folder_passes_nothing(self):
        code, verdicts, _ = self.run_check("all")
        self.assertEqual(len(verdicts), 7)
        self.assertNotIn("passed", verdicts.values())
        self.assertEqual(code, 1)          # done_picture fails outright when no phase is picked
        self.assertEqual(verdicts["no_interrupt"], "unverified")

    def test_clean_day_passes(self):
        clean_day(self.d)
        code, verdicts, _ = self.run_check("all")
        self.assertEqual((code, set(verdicts.values())), (0, {"passed"}))

    def test_unverified_alone_exits_2(self):
        clean_day(self.d)
        os.remove(os.path.join(self.d, "parking.jsonl"))
        code, verdicts, _ = self.run_check("all")
        self.assertEqual((code, verdicts["no_interrupt"]), (2, "unverified"))

    def test_broken_file_is_inconclusive(self):
        clean_day(self.d)
        put(self.d, "today.json", "{not json")
        code, verdicts, _ = self.run_check("done_picture")
        self.assertEqual((code, verdicts["done_picture"]), (2, "inconclusive"))

    def test_each_rule_can_fail(self):
        cases = {
            "one_active": ("phases.json", [{"id": "P1", "status": "active"}, {"id": "P2", "status": "active"}]),
            "done_picture": ("today.json", {"date": "2031-03-03", "phase_id": "P1", "done_picture": "x",
                                            "first_step": {"when": "09:30", "action": "a"}}),
            "switch_cap": ("switches.jsonl", rows({"ts": STAMP, "active_threads": ["a", "b"]})),
            "no_interrupt": ("parking.jsonl", rows({"ts": STAMP, "ask": "q", "verdict": "park", "surfaced_during_block": True})),
            "snapshot_fresh": ("phases.json", [{"id": "P1", "status": "active", "next_step": {"when": "", "action": ""}, "updated": STAMP}]),
            "model_tier": ("models.jsonl", rows({"ts": STAMP, "phase_id": "P2", "tier": "top", "in_block": False})),
            "critic_blind": ("critic.json", {"ts": STAMP, "sources_read": [{"kind": "state", "ref": "x/today.json"}], "ranking": []}),
        }
        for check, (name, value) in cases.items():
            with self.subTest(check):
                clean_day(self.d)
                put(self.d, name, value)
                code, verdicts, _ = self.run_check(check)
                self.assertEqual((code, verdicts[check]), (1, "failed"))

    def test_urgent_ask_in_block_is_allowed(self):
        clean_day(self.d)
        put(self.d, "parking.jsonl", rows({"ts": STAMP, "ask": "outage", "verdict": "park", "urgent": True, "surfaced_during_block": True}))
        self.assertEqual(self.run_check("no_interrupt")[0], 0)

    def test_switch_cap_outside_block_and_setting(self):
        clean_day(self.d)
        noon = TUE + "T12:00:00+00:00"
        put(self.d, "switches.jsonl", rows({"ts": noon, "active_threads": ["a", "b", "c"]}))
        self.assertEqual(self.run_check("switch_cap", FOCUS_NOW=noon)[0], 0)
        self.assertEqual(self.run_check("switch_cap", FOCUS_NOW=noon, FOCUS_SWITCH_CAP="2")[0], 1)

    def test_stale_snapshot_fails(self):
        clean_day(self.d)
        code, verdicts, _ = self.run_check("snapshot_fresh", FOCUS_NOW="2031-03-05T12:00:00+00:00")
        self.assertEqual((code, verdicts["snapshot_fresh"]), (1, "failed"))

    def test_phase_gate(self):
        clean_day(self.d)
        self.assertEqual(self.run_check("gate-open", "P2")[0], 1)     # P1 is still open
        self.assertEqual(self.run_check("gate-open", "P1")[0], 0)     # the active phase itself
        put(self.d, "phases.json", [{"id": "P1", "status": "closed"}])
        self.assertEqual(self.run_check("gate-open", "P2")[0], 0)

    def test_usage_errors(self):
        self.assertEqual(self.run_check("no_such_check")[0], 64)
        self.assertEqual(self.run_check("gate-open")[0], 64)


class TierRoute(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.d = self.tmp.name
        put(self.d, "today.json", {"date": TUE, "phase_id": "P1"})

    def route(self, *args, now=IN_BLOCK, **extra):
        code, out, _ = script("tier_route.py", *args, env=env(self.d, now=now, **extra))
        self.assertEqual(code, 0)
        return out[0]

    def test_in_block(self):
        self.assertEqual(self.route("--want", "top", "--phase", "P1")["tier"], "top")
        other = self.route("--want", "top", "--phase", "P2")
        self.assertEqual((other["tier"], other["capped"], other["in_block"]), ("mid", True, True))
        self.assertEqual(self.route("--want", "top")["tier"], "mid")
        self.assertEqual(self.route("--want", "cheap")["tier"], "cheap")     # a cap never raises a tier

    def test_outside_block(self):
        noon = TUE + "T12:00:00+00:00"
        self.assertEqual(self.route("--want", "top", now=noon)["tier"], "mid")
        self.assertEqual(self.route("--want", "top", "--phase", "P9", now=noon)["tier"], "top")
        self.assertEqual(self.route("--want", "top", now=noon, FOCUS_PHASE="P9")["tier"], "top")

    def test_weekend_and_boundaries(self):
        self.assertFalse(self.route("--want", "top", "--phase", "P2", now="2031-03-08T10:00:00+00:00")["in_block"])
        for hm, inside in (("09:29", False), ("09:30", True), ("11:29", True), ("11:30", False)):
            self.assertIs(self.route("--want", "mid", now=f"{TUE}T{hm}:00+00:00")["in_block"], inside, hm)

    def test_stale_or_broken_today_means_no_active_phase(self):
        for value in ({"date": "2031-03-03", "phase_id": "P1"}, "{not json", []):
            with self.subTest(value=value):
                put(self.d, "today.json", value)
                self.assertEqual(self.route("--want", "top", "--phase", "P1", "--no-log")["tier"], "mid")

    def test_log_feeds_the_model_tier_check(self):
        put(self.d, "phases.json", [{"id": "P1", "status": "active"}])
        self.route("--want", "top", "--phase", "P1")
        self.route("--want", "top", "--phase", "P2")          # capped to mid, so the log stays clean
        self.route("--want", "top", "--no-log")
        logged = Path(self.d, "models.jsonl").read_text().splitlines()
        self.assertEqual(len(logged), 2)
        self.assertLessEqual({"ts", "phase_id", "tier", "in_block"}, set(json.loads(logged[0])))
        code, out, _ = script("focus_check.py", "model_tier", env=env(self.d))
        self.assertEqual((code, out[0]["verdict"]), (0, "passed"))


CODE = "print(1)\n" * 40
DESIGN = "# Design\n\nWhat changes.\nWhy.\n"


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class GitCase(unittest.TestCase):
    """A bare 'remote', and a clone under a 'lanes' folder with one seed commit on main."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name).resolve()
        self.lanes, self.remote = root / "lanes", root / "remote.git"
        self.repo = self.lanes / "work"
        self.repo.mkdir(parents=True)
        self.clock = 1900000000
        self.env = {**env(root / "state"), "DESIGN_LEDGER": str(root / "ledger.jsonl"),
                    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True, capture_output=True, env=self.env)
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "test")
        self.git("remote", "add", "origin", str(self.remote))
        self.commit("README.md", "seed\n")
        self.git("push", "-q", "origin", "main")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()

    def git(self, *args, check=True, cwd=None):
        return subprocess.run(["git", *args], cwd=cwd or self.repo, check=check, capture_output=True, text=True, env=self.env)

    def commit(self, path, content, message=None, same_second=False):
        if not same_second:
            self.clock += 60
        full = self.repo / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
        stamp = f"@{self.clock} +0000"
        self.env.update(GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
        self.git("add", ".")
        self.git("commit", "-qm", message or f"add {path}")

    def branch(self, name):
        self.git("checkout", "-q", "-b", name, self.base)


class DesignGate(GitCase):
    def gate(self, body=None, head="HEAD", **extra):
        args = [str(self.repo), self.base, head]
        if body is not None:
            put(self.tmp.name, "body.txt", body)
            args += ["--body", os.path.join(self.tmp.name, "body.txt")]
        code, out, _ = script("design_gate.py", *args, env={**self.env, **extra})
        return code, (out[0]["detail"] if out else "")

    def test_design_before_code_passes(self):
        self.branch("b"); self.commit("docs/design/b.md", DESIGN); self.commit("src/b.py", CODE)
        self.assertEqual(self.gate()[0], 0)

    def test_design_after_or_with_code_fails(self):
        self.branch("after"); self.commit("src/a.py", CODE); self.commit("DESIGN.md", DESIGN)
        code, why = self.gate()
        self.assertEqual(code, 1)
        self.assertIn("after the first code commit", why)
        self.branch("same"); (self.repo / "PLAN.md").write_text(DESIGN); self.commit("src/s.py", CODE)
        code, why = self.gate()
        self.assertEqual(code, 1)
        self.assertIn("same commit", why)

    def test_same_second_commits_are_ordered_by_position(self):
        self.branch("fast"); self.commit("src/a.py", CODE); self.commit("DESIGN.md", DESIGN, same_second=True)
        self.assertEqual(self.gate()[0], 1)
        self.branch("fast-ok"); self.commit("DESIGN.md", DESIGN); self.commit("src/a.py", CODE, same_second=True)
        self.assertEqual(self.gate()[0], 0)

    def test_no_design_thin_design_and_deleted_design_fail(self):
        self.branch("none"); self.commit("src/c.py", CODE)
        self.assertEqual(self.gate()[0], 1)
        self.branch("thin"); self.commit("DESIGN.md", "todo\n"); self.commit("src/d.py", CODE)
        self.assertIn("too short", self.gate()[1])
        self.assertEqual(self.gate(DESIGN_MIN_LINES="1")[0], 0)
        self.branch("gone"); self.commit("DESIGN.md", DESIGN); self.commit("src/e.py", CODE)
        self.git("rm", "-q", "DESIGN.md"); self.git("commit", "-qm", "drop the design")
        self.assertEqual(self.gate()[0], 1)

    def test_exemption_needs_a_reason_and_a_small_change(self):
        self.branch("tiny"); self.commit("src/e.py", "x = 1\n")
        self.assertEqual(self.gate()[0], 1)
        self.assertEqual(self.gate("design-exempt: typo\n")[0], 0)
        self.assertEqual(self.gate("design-exempt:\n")[0], 1)
        self.assertEqual(self.gate("see design-exempt: typo\n")[0], 1)       # must start the line
        self.branch("edge"); self.commit("src/f.py", "x = 1\n" * 30)
        self.assertEqual(self.gate("design-exempt: small\n")[0], 0)
        self.branch("big"); self.commit("src/g.py", "x = 1\n" * 31)
        self.assertEqual(self.gate("design-exempt: not small\n")[0], 1)
        self.assertEqual(self.gate("design-exempt: raised limit\n", DESIGN_EXEMPT_LINES="40")[0], 0)

    def test_prose_only_branch_passes(self):
        self.branch("docs"); self.commit("notes.md", "words\n")
        self.assertEqual(self.gate(), (0, "no code commits"))

    def test_ledger_design_must_be_older_than_the_code(self):
        self.branch("ledger"); self.commit("src/h.py", CODE)
        ledger = Path(self.env["DESIGN_LEDGER"])
        ledger.write_text(rows({"ref": "design-note-0042", "created": "2030-01-01T00:00:00+00:00"}) + "not json\n")
        self.assertEqual(self.gate("see design-note-0042\n")[0], 0)
        self.assertEqual(self.gate("no reference here\n")[0], 1)
        ledger.write_text(rows({"ref": "design-note-0042", "created": "2031-01-01T00:00:00+00:00"}))   # after the commit
        self.assertEqual(self.gate("see design-note-0042\n")[0], 1)
        ledger.write_text(rows({"ref": "short", "created": "2030-01-01T00:00:00+00:00"}))
        self.assertEqual(self.gate("short\n")[0], 1)

    def test_bad_ref_or_body_is_inconclusive_and_usage_is_64(self):
        self.assertEqual(self.gate(head="no-such-ref")[0], 2)
        code, _, _ = script("design_gate.py", str(self.repo), self.base, "HEAD", "--body", "/no/such/file", env=self.env)
        self.assertEqual(code, 2)
        self.assertEqual(script("design_gate.py", str(self.repo), env=self.env)[0], 64)


class Hook(GitCase):
    """Real pushes to the throwaway bare repository through the example hook."""

    def setUp(self):
        super().setUp()
        self.hooks = self.repo / ".git" / "hooks"
        self.hooks.mkdir(exist_ok=True)
        shutil.copy(SKILL / "examples" / "pre-push", self.hooks / "pre-push")
        os.chmod(self.hooks / "pre-push", 0o755)
        shutil.copy(SCRIPTS / "design_gate.py", self.hooks / "design_gate.py")
        self.conf("2000-01-01T00:00:00+00:00")

    def conf(self, enable, lanes=None):
        put(self.hooks, "design-gate.conf", f"# test\nLANES_ROOTS={lanes or self.lanes}\nENABLE_TS={enable}\nMAIN_REF=origin/main\n")

    def push(self, name, *flags):
        r = self.git("push", *flags, "origin", name, check=False)
        return r.returncode, r.stderr

    def landed(self, name):
        return self.git("ls-remote", "origin", f"refs/heads/{name}").stdout.strip() != ""

    def test_blocks_code_without_design_then_passes_after_fix(self):
        self.branch("feat"); self.commit("src/a.py", CODE)
        code, err = self.push("feat")
        self.assertNotEqual(code, 0)
        self.assertIn("design-gate: BLOCKED refs/heads/feat", err)
        self.assertFalse(self.landed("feat"))
        self.branch("feat2"); self.commit("docs/design/a.md", DESIGN); self.commit("src/a.py", CODE)
        self.assertEqual(self.push("feat2")[0], 0)
        self.assertTrue(self.landed("feat2"))

    def test_exempt_line_in_a_commit_message_passes(self):
        self.branch("typo"); self.commit("src/a.py", "x = 1\n", "fix a typo\n\ndesign-exempt: one-line typo")
        self.assertEqual(self.push("typo")[0], 0)

    def test_out_of_scope_and_missing_conf_pass(self):
        self.branch("feat"); self.commit("src/a.py", CODE)
        self.conf("2000-01-01T00:00:00+00:00", lanes=str(self.lanes) + "-elsewhere")
        self.assertEqual(self.push("feat")[0], 0)
        self.branch("feat3"); self.commit("src/b.py", CODE)
        os.remove(self.hooks / "design-gate.conf")
        self.assertEqual(self.push("feat3")[0], 0)

    def test_scope_can_come_from_the_environment(self):
        self.conf("2000-01-01T00:00:00+00:00", lanes=str(self.lanes) + "-elsewhere")
        self.env["DESIGN_GATE_LANES"] = str(self.lanes)
        self.branch("feat"); self.commit("src/a.py", CODE)
        self.assertNotEqual(self.push("feat")[0], 0)

    def test_old_branch_is_grandfathered(self):
        self.conf("2099-01-01T00:00:00+00:00")
        self.branch("old"); self.commit("src/a.py", CODE)
        code, err = self.push("old")
        self.assertEqual(code, 0)
        self.assertIn("grandfathered", err)

    def test_broken_setup_blocks_in_scope_pushes(self):
        self.conf("not a time")
        self.branch("feat"); self.commit("docs/design/a.md", DESIGN); self.commit("src/a.py", CODE)
        code, err = self.push("feat")
        self.assertNotEqual(code, 0)
        self.assertIn("not set up correctly", err)

    def test_chained_hook_runs_first_and_can_fail_the_push(self):
        marker = self.hooks / "ran"
        chained = self.hooks / "pre-push.chained-2031"
        chained.write_text(f"#!/bin/sh\ncat > '{marker}'\nexit 0\n")
        os.chmod(chained, 0o755)
        self.branch("ok"); self.commit("docs/design/a.md", DESIGN); self.commit("src/a.py", CODE)
        self.assertEqual(self.push("ok")[0], 0)
        self.assertIn("refs/heads/ok", marker.read_text())                  # the chained hook got the same stdin
        chained.write_text("#!/bin/sh\nexit 7\n")
        self.branch("ok2"); self.commit("docs/design/b.md", DESIGN); self.commit("src/b.py", CODE)
        self.assertNotEqual(self.push("ok2")[0], 0)
        self.assertFalse(self.landed("ok2"))

    def test_delete_push_is_not_checked(self):
        self.branch("gone"); self.commit("docs/design/a.md", DESIGN); self.commit("src/a.py", CODE)
        self.assertEqual(self.push("gone")[0], 0)
        self.assertEqual(self.push("gone", "--delete")[0], 0)
        self.assertFalse(self.landed("gone"))


if __name__ == "__main__":
    unittest.main()
