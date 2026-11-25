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


if __name__ == "__main__":
    unittest.main()
