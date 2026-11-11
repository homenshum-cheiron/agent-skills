import json
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "autonomy-map.json"


def load():
    spec = importlib.util.spec_from_file_location("autonomy", ROOT / "scripts" / "check_autonomy_map.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


autonomy = load()


class AutonomyMapTests(unittest.TestCase):
    def document(self):
        return json.loads(MAP.read_text())

    def test_published_map_matches_qualitative_claims(self):
        document = self.document()
        result = autonomy.check_map(document)
        self.assertEqual(result["status"], "ok")
        self.assertIn("not a measured autonomy", result["limit"])
        self.assertFalse(document["numeric_chart_allowed"])
        self.assertEqual(document["diagram_edges"], [])
        statuses = {stage["id"]: stage["status"] for stage in document["stages"]}
        self.assertEqual(statuses[1], "documented")
        self.assertEqual(statuses[2], "offline_partial")
        self.assertEqual(statuses[3], "unknown")
        self.assertEqual(statuses[4], "not_demonstrated")
        self.assertEqual(statuses[5], "not_demonstrated")
        self.assertIsNone(document["sample"]["n_eligible_attempts"])

    def test_unknown_stage_cannot_become_a_percent(self):
        document = self.document()
        document["numeric_chart_allowed"] = True
        document["autonomy_percent"] = 40
        result = autonomy.check_map(document)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("percent" in finding or "numeric" in finding for finding in result["findings"]))

    def test_diagram_cannot_reach_an_unknown_stage(self):
        document = self.document()
        document["diagram_edges"] = [{"from": 2, "to": 3, "style": "solid"}]
        result = autonomy.check_map(document)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("reachable" in finding or "not demonstrated" in finding for finding in result["findings"]))

    def test_demonstrated_label_needs_a_census(self):
        document = self.document()
        document["stages"][2]["status"] = "demonstrated"
        document["prose_claims"][2]["status"] = "demonstrated"
        result = autonomy.check_map(document)
        self.assertEqual(result["status"], "invalid")
        self.assertTrue(any("demonstrated" in finding for finding in result["findings"]))

    def test_policy_approval_is_not_a_capability_failure(self):
        document = self.document()
        document["policy_approval_is_capability_failure"] = True
        self.assertEqual(autonomy.check_map(document)["status"], "invalid")

    def test_prose_cannot_disagree_with_the_stage(self):
        document = self.document()
        document["prose_claims"][2]["status"] = "documented"
        self.assertEqual(autonomy.check_map(document)["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
