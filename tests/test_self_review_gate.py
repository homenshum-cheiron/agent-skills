"""Self-review gate checker. Synthetic records only."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "skills/self-review-gate"
spec = importlib.util.spec_from_file_location("check_gate", PKG / "scripts/check_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

EXAMPLE = json.loads((PKG / "examples/gate-record.json").read_text())


def record(**changes):
    data = copy.deepcopy(EXAMPLE)
    data.update(changes)
    return data


class GateTests(unittest.TestCase):
    def test_worked_example_acts(self):
        result = gate.check(record())
        self.assertEqual(result["verdict"], "act", result["findings"])

    def test_owner_only_category_cannot_be_lowered(self):
        result = gate.check(record(categories=["shared-merge"], tier=1))
        self.assertEqual(result["verdict"], "needs-owner")
        self.assertEqual(result["tier"], 2)

    def test_irreversible_goes_to_owner(self):
        self.assertEqual(gate.check(record(reversible=False))["verdict"], "needs-owner")

    def test_tier_two_always_needs_owner_even_when_green(self):
        self.assertEqual(gate.check(record(tier=2))["verdict"], "needs-owner")

    def test_failing_check_blocks(self):
        data = record()
        data["checks"][1]["exit_code"] = 1
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_check_on_old_revision_blocks(self):
        data = record()
        data["checks"][0]["revision"] = "aaaaaaa"
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_branch_name_is_not_a_tip(self):
        self.assertEqual(gate.check(record(tip="main"))["verdict"], "blocked")

    def test_self_review_does_not_count(self):
        data = record()
        data["review"]["author_is_reviewer"] = True
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_reviewer_that_read_author_reasoning_does_not_count(self):
        data = record()
        data["review"]["saw_author_reasoning"] = True
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_stale_review_blocks(self):
        data = record()
        data["review"]["revision"] = "bbbbbbb"
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_unresolved_finding_blocks(self):
        data = record()
        data["review"]["findings"].append({"title": "x", "disposition": "unresolved"})
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_fixed_finding_needs_evidence(self):
        data = record()
        data["review"]["findings"][0]["evidence"] = ""
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_missing_revert_blocks(self):
        self.assertEqual(gate.check(record(revert=""))["verdict"], "blocked")

    def test_failed_post_verify_means_revert(self):
        data = record(post_verify={"command": "python3 -m unittest", "exit_code": 1, "observed": "FAILED (failures=1)"})
        self.assertEqual(gate.check(data)["verdict"], "revert")

    def test_post_verify_string_exit(self):
        data = record(post_verify={"command": "python3 -m unittest", "exit_code": "0", "observed": "OK"})
        self.assertEqual(gate.check(data)["verdict"], "revert")

    def test_green_post_verify_still_acts(self):
        data = record(post_verify=[{"command": "python3 -m unittest", "exit_code": 0, "observed": "OK"}])
        self.assertEqual(gate.check(data)["verdict"], "act")

    def test_tier_zero_needs_only_revert(self):
        data = {"action": "edit a local note", "tier": 0, "reversible": True, "revert": "git checkout -- note.md"}
        self.assertEqual(gate.check(data)["verdict"], "act")

    def test_bad_tier_blocks(self):
        self.assertEqual(gate.check(record(tier=5))["verdict"], "blocked")

    def test_cli_exit_codes_and_log_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "review").mkdir()
            (tmp / "review/pr7-reviewer.txt").write_text("tip 3f9c2a1\nPASS\n")
            good = tmp / "good.json"
            good.write_text(json.dumps(record()))
            shared = tmp / "shared.json"
            shared.write_text(json.dumps(record(categories=["external-send"])))
            log = tmp / "decisions.tsv"
            self.assertEqual(gate.main([str(good), "--log", str(log)]), 0)
            self.assertEqual(gate.main([str(shared), "--log", str(log)]), 2)
            rows = log.read_text().splitlines()
            self.assertEqual(rows[0].split("\t"), ["ts", "phase", "decision", "why", "evidence", "result"])
            self.assertEqual(len(rows), 3)
            self.assertTrue(rows[1].endswith("\tact"))
            self.assertTrue(rows[2].endswith("\tneeds-owner"))
            self.assertTrue(all(len(r.split("\t")) == 6 for r in rows))

    def test_log_cells_cannot_start_a_formula(self):
        self.assertEqual(gate._cell("=SUM(A1)"), "'=SUM(A1)")
        self.assertEqual(gate._cell("a\tb\nc"), "a b c")

    def test_scalar_or_padded_owner_tag_still_needs_owner(self):
        self.assertEqual(gate.check(record(categories="external-send"))["verdict"], "needs-owner")
        self.assertEqual(gate.check(record(categories=[" External-Send "]))["verdict"], "needs-owner")

    def test_unknown_category_blocks(self):
        self.assertEqual(gate.check(record(categories=["external_send"]))["verdict"], "blocked")

    def test_check_without_revision_blocks(self):
        data = record()
        del data["checks"][0]["revision"]
        self.assertEqual(gate.check(data)["verdict"], "blocked")
        data["checks"][0]["revision"] = None
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_boolean_exit_code_is_not_success(self):
        data = record()
        data["checks"][0]["exit_code"] = False
        self.assertEqual(gate.check(data)["verdict"], "blocked")
        data = record(post_verify={"command": "x", "exit_code": False, "observed": "failed"})
        self.assertEqual(gate.check(data)["verdict"], "revert")

    def test_review_verdict_must_be_pass(self):
        data = record()
        del data["review"]["verdict"]
        self.assertEqual(gate.check(data)["verdict"], "blocked")

    def test_missing_evidence_file_blocks_when_base_given(self):
        data = record()
        data["review"]["evidence"] = "review/missing.txt"
        self.assertEqual(gate.check(data, base=PKG / "examples")["verdict"], "blocked")
        self.assertEqual(gate.check(record(), base=PKG / "examples")["verdict"], "act")

    def test_evidence_file_saying_block_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "r.txt").write_text("Finding: x\nBLOCK\n")
            data = record()
            data["review"]["evidence"] = "r.txt"
            data["review"]["findings"] = []
            self.assertEqual(gate.check(data, base=Path(tmp))["verdict"], "blocked")

    def test_failed_post_verify_reverts_even_when_record_is_stale(self):
        data = record(post_verify={"command": "x", "exit_code": 1, "observed": "FAILED"})
        data["review"]["revision"] = "bbbbbbb"
        self.assertEqual(gate.check(data)["verdict"], "revert")

    def test_rerun_catches_a_fabricated_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "review").mkdir()
            (tmp / "review/pr7-reviewer.txt").write_text("tip 3f9c2a1\nPASS\n")
            data = record()
            data["checks"] = [{"command": "python3 -c 'import sys; sys.exit(0)'", "exit_code": 0, "observed": "ok", "revision": data["tip"]},
                              {"command": "python3 -c 'import sys; sys.exit(2)'", "exit_code": 0, "observed": "OK", "revision": data["tip"]}]
            path = tmp / "gate.json"
            path.write_text(json.dumps(data))
            self.assertEqual(gate.main([str(path)]), 0)
            self.assertEqual(gate.main([str(path), "--rerun", "--cwd", str(tmp)]), 1)

    def test_duplicate_fields_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "dup.json")
            path.write_text('{"action": "send", "tier": 0, "categories": ["external-send"], "categories": [], "reversible": true, "revert": "x"}')
            self.assertEqual(gate.main([str(path)]), 1)

    def test_review_output_must_be_current_and_end_in_pass(self):
        cases = {"empty.txt": "", "old.txt": "tip aaaaaaa\nPASS\n", "cut.txt": "tip 3f9c2a1\nFinding: unresolved x\n"}
        with tempfile.TemporaryDirectory() as tmp:
            for name, text in cases.items():
                Path(tmp, name).write_text(text)
                data = record()
                data["review"]["evidence"] = name
                self.assertEqual(gate.check(data, base=Path(tmp))["verdict"], "blocked", name)

    def test_recorded_post_failure_reverts_before_any_other_rule(self):
        failed = {"command": "x", "exit_code": 7, "observed": "unhealthy"}
        for change in ({"tier": 2}, {"categories": ["external-send"]}, {"reversible": False}, {"tier": 9}):
            data = record(post_verify=failed, **change)
            self.assertEqual(gate.check(data)["verdict"], "revert", change)

    def _git_repo(self, tmp):
        import subprocess
        subprocess.run(["git", "init", "-q", str(tmp)], check=True)
        Path(tmp, "f").write_text("1")
        subprocess.run(["git", "-C", str(tmp), "add", "f"], check=True)
        subprocess.run(["git", "-C", str(tmp), "-c", "user.name=t", "-c", "user.email=t@example.invalid",
                        "commit", "-q", "-m", "c"], check=True)
        return subprocess.run(["git", "-C", str(tmp), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def test_rerun_requires_the_tip_checked_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            head = self._git_repo(tmp)
            (tmp / "r.txt").write_text(f"tip {head[:7]}\nPASS\n")
            data = record(tip=head[:7])
            for c in data["checks"]:
                c["revision"] = head[:7]
                c["command"] = "true"
            data["review"].update(revision=head[:7], evidence="r.txt")
            path = tmp / "gate.json"
            path.write_text(json.dumps(data))
            self.assertEqual(gate.main([str(path), "--rerun", "--cwd", str(tmp)]), 0)
            data["checks"][1]["command"] = "exit 2"  # recorded as passing, actually fails at the tip
            path.write_text(json.dumps(data))
            self.assertEqual(gate.main([str(path)]), 0)
            self.assertEqual(gate.main([str(path), "--rerun", "--cwd", str(tmp)]), 1)
            data["checks"][1]["command"] = "true"
            path.write_text(json.dumps(data))
            data2 = json.loads(path.read_text())
            data2["tip"] = "1234567"
            for c in data2["checks"]:
                c["revision"] = "1234567"
            data2["review"]["revision"] = "1234567"
            (tmp / "r.txt").write_text("tip 1234567\nPASS\n")
            path.write_text(json.dumps(data2))
            self.assertEqual(gate.main([str(path), "--rerun", "--cwd", str(tmp)]), 1)

    def test_rerun_reruns_post_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "review").mkdir()
            (tmp / "review/pr7-reviewer.txt").write_text("tip 3f9c2a1\nPASS\n")
            data = record(post_verify={"command": "exit 7", "exit_code": 0, "observed": "healthy"})
            path = tmp / "gate.json"
            path.write_text(json.dumps(data))
            self.assertEqual(gate.main([str(path)]), 0)
            self.assertEqual(gate.main([str(path), "--rerun", "--cwd", str(tmp)]), 3)


if __name__ == "__main__":
    unittest.main()
