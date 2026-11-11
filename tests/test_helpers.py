import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packet = load("packet", "skills/proof-before-review/scripts/check_packet.py")
timing = load("timing", "skills/measure-the-path/scripts/summarize_intervals.py")
repo = load("repo", "scripts/validate_repo.py")


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.log = self.base / "log.txt"
        self.log.write_text("synthetic test observation\n")
        self.doc = {"schema_version": 1, "artifact_revision": "v1", "reviewed_revision": "v1",
                    "scope": "synthetic test", "checks": [{"id": "test", "status": "passed",
                    "command": "example command", "exit_code": 0,
                    "evidence": [{"path": "log.txt", "sha256": hashlib.sha256(self.log.read_bytes()).hexdigest()}]}]}

    def result(self):
        return packet.evaluate(self.doc, self.base)["status"]

    def test_complete_is_bookkeeping_only(self):
        result = packet.evaluate(self.doc, self.base)
        self.assertEqual(result["status"], "complete")
        self.assertIn("authenticity", result["limit"])

    def test_revision_drift_is_inconclusive(self):
        self.doc["artifact_revision"] = "v2"
        self.assertEqual(self.result(), "inconclusive")

    def test_missing_evidence_is_inconclusive(self):
        self.log.unlink()
        self.assertEqual(self.result(), "inconclusive")

    def test_empty_evidence_is_inconclusive(self):
        self.log.write_text("")
        self.assertEqual(self.result(), "inconclusive")

    def test_changed_evidence_is_inconclusive(self):
        self.log.write_text("different")
        self.assertEqual(self.result(), "inconclusive")

    def test_no_evidence_is_inconclusive(self):
        self.doc["checks"][0]["evidence"] = []
        self.assertEqual(self.result(), "inconclusive")

    def test_blocked_and_not_run_are_inconclusive(self):
        for state in ("blocked", "not_run"):
            with self.subTest(state=state):
                self.doc["checks"][0] = {"id": "test", "status": state, "command": "example",
                                         "reason": "test environment unavailable", "evidence": []}
                self.assertEqual(self.result(), "inconclusive")

    def test_unexecuted_cannot_have_exit_code(self):
        self.doc["checks"][0]["status"] = "blocked"
        self.doc["checks"][0]["reason"] = "unavailable"
        self.assertEqual(self.result(), "invalid")

    def test_fail_remains_failed(self):
        self.doc["checks"][0]["status"] = "failed"
        self.doc["checks"][0]["exit_code"] = 1
        self.assertEqual(self.result(), "failed")

    def test_nonzero_pass_is_invalid(self):
        self.doc["checks"][0]["exit_code"] = 2
        self.assertEqual(self.result(), "invalid")

    def test_boolean_exit_is_not_integer(self):
        self.doc["checks"][0]["exit_code"] = False
        self.assertEqual(self.result(), "invalid")

    def test_duplicate_check_ids_invalid(self):
        self.doc["checks"].append(copy.deepcopy(self.doc["checks"][0]))
        self.assertEqual(self.result(), "invalid")

    def test_traversal_and_absolute_paths_invalid(self):
        for path in ("../outside", str(self.log)):
            with self.subTest(path=path):
                self.doc["checks"][0]["evidence"][0]["path"] = path
                self.assertEqual(self.result(), "invalid")

    def test_symlink_inside_directory_is_invalid(self):
        (self.base / "alias.txt").symlink_to(self.log)
        self.doc["checks"][0]["evidence"][0]["path"] = "alias.txt"
        self.assertEqual(self.result(), "invalid")

    def test_invalid_digest(self):
        self.doc["checks"][0]["evidence"][0]["sha256"] = "x"
        self.assertEqual(self.result(), "invalid")

    def test_empty_check_list_invalid(self):
        self.doc["checks"] = []
        self.assertEqual(self.result(), "invalid")

    def test_wrong_field_types_do_not_crash(self):
        for field in ("status", "id", "evidence", "command", "exit_code"):
            for value in (None, [], {}, True):
                with self.subTest(field=field, value=value):
                    doc = copy.deepcopy(self.doc)
                    doc["checks"][0][field] = value
                    self.assertNotEqual(packet.evaluate(doc, self.base)["status"], "complete")

    def test_malformed_json_cli(self):
        bad = self.base / "bad.json"
        bad.write_text("{")
        result = subprocess.run([sys.executable, str(ROOT / "skills/proof-before-review/scripts/check_packet.py"), str(bad)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["status"], "invalid")


class TimingTests(unittest.TestCase):
    def document(self, spans, lo=0, hi=10):
        return {"window_start": lo, "window_end": hi,
                "spans": [{"name": str(i), "start": a, "end": b} for i, (a, b) in enumerate(spans)]}

    def test_parallel_spans(self):
        result = timing.summarize(self.document([(1, 6), (2, 8), (8, 10)]))
        self.assertEqual(result["wall_time"], 10)
        self.assertEqual(result["summed_work"], 13)
        self.assertEqual(result["covered_time"], 9)
        self.assertEqual(result["gaps"], [[0, 1]])

    def test_nested_spans_not_double_counted(self):
        result = timing.summarize(self.document([(0, 10), (2, 4)]))
        self.assertEqual(result["summed_work"], 12)
        self.assertEqual(result["covered_time"], 10)

    def test_disjoint_spans_and_gaps(self):
        result = timing.summarize(self.document([(1, 2), (4, 6), (8, 9)]))
        self.assertEqual(result["gaps"], [[0, 1], [2, 4], [6, 8], [9, 10]])
        self.assertEqual(result["unexplained_time"], 6)

    def test_zero_duration_covers_nothing(self):
        result = timing.summarize(self.document([(5, 5)]))
        self.assertEqual(result["covered_time"], 0)
        self.assertEqual(result["gaps"], [[0, 10]])

    def test_invalid_spans_rejected(self):
        for pair in ((2, 1), (-1, 4), (2, 11), (float("nan"), 3), (2, float("inf")), (False, 3), (0, 10**400)):
            with self.subTest(pair=pair), self.assertRaises(ValueError):
                timing.summarize(self.document([pair]))

    def test_invalid_window_rejected(self):
        for lo, hi in ((3, 2), (False, 10), (0, float("nan"))):
            with self.subTest(lo=lo, hi=hi), self.assertRaises(ValueError):
                timing.summarize(self.document([(1, 2)], lo, hi))

    def test_window_subtraction_overflow_rejected(self):
        with self.assertRaises(ValueError):
            timing.summarize(self.document([(-1e308, 1e308)], -1e308, 1e308))

    def test_summed_work_overflow_rejected(self):
        with self.assertRaises(ValueError):
            timing.summarize(self.document([(0, 1e308), (0, 1e308)], 0, 1e308))

    def test_empty_spans_rejected(self):
        with self.assertRaises(ValueError):
            timing.summarize(self.document([]))

    def test_reordering_spans_preserves_result(self):
        spans = [(1, 6), (2, 8), (8, 10)]
        self.assertEqual(timing.summarize(self.document(spans)), timing.summarize(self.document(list(reversed(spans)))))


class RepositoryTests(unittest.TestCase):
    def test_actual_repository(self):
        errors, count = repo.validate()
        self.assertEqual(errors, [])
        self.assertGreater(count, 0)

    def test_broken_link_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[missing](not-here.md)")
            errors, _ = repo.validate(root)
            self.assertTrue(any("Broken link" in error for error in errors))

    def test_cross_package_link_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "skills/example"
            package.mkdir(parents=True)
            (root / "README.md").write_text("root")
            (package / "SKILL.md").write_text('---\nname: example\ndescription: "Example."\n---\n[bad](../../README.md)')
            errors, _ = repo.validate(root)
            self.assertTrue(any("leaves package" in error for error in errors))

    def test_publication_hazard_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("/" + "Users" + "/example/private")
            errors, _ = repo.validate(root)
            self.assertTrue(any("Publication scan" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
