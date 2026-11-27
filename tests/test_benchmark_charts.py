"""Benchmark-charts package: contract builder and honest-number rules on a synthetic fixture."""
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "benchmark-charts"
SPEC = importlib.util.spec_from_file_location("make_chart_data", SKILL / "scripts" / "make_chart_data.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

RAW = json.loads((SKILL / "examples" / "raw_results.json").read_text())


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = mod.main(args)
    return code, out.getvalue(), err.getvalue()


class BenchmarkChartsFolder(unittest.TestCase):
    def test_files_present(self):
        for relative in (
            "SKILL.md",
            "scripts/make_chart_data.py",
            "references/benchmark-chart-dataset.schema.json",
            "references/STYLES.md",
            "references/canvas-template.tsx",
            "examples/raw_results.json",
            "examples/chart_data.json",
            "examples/worked.md",
        ):
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_frontmatter_names_folder_and_says_when(self):
        import re
        text = (SKILL / "SKILL.md").read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
        self.assertIn("name: benchmark-charts", front)
        self.assertRegex(front, r'description: "Use when .+Page.+"')

    def test_generic_recipe_names_no_team_specifics(self):
        suffixes = {".md", ".py", ".json", ".tsx", ".txt"}
        text = ""
        for path in SKILL.rglob("*"):
            if path.is_file() and path.suffix in suffixes and "__pycache__" not in path.parts:
                text += path.read_text() + "\n"
        for word in ("Cheiron", "Phnyx", "Tavily", "Boryung", "/workspace"):
            self.assertNotIn(word, text, word)


class ChartDataBuilder(unittest.TestCase):
    def test_example_builds_and_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "chart_data.json"
            code, stdout, err = run(
                ["build", "--input", str(SKILL / "examples" / "raw_results.json"), "--output", str(out)]
            )
            self.assertEqual(code, 0, err)
            self.assertIn("76.2", stdout)
            doc = json.loads(out.read_text())
            self.assertEqual(doc["sums"]["cost_usd"]["baseline"]["value"], 17.5)
            self.assertEqual(doc["sums"]["cost_usd"]["tool_loop"]["value"], 4.17)
            self.assertEqual(doc["sums"]["cost_usd"]["compact"]["status"], "estimate")
            self.assertIn("ESTIMATE", doc["sums"]["cost_usd"]["compact"]["display"])
            self.assertEqual(doc["sums"]["wall_s"]["compact"]["status"], "not_measured")
            self.assertEqual(doc["sums"]["wall_s"]["compact"]["display"], "not measured")
            self.assertEqual(doc["sums"]["cases_passed"]["baseline"]["value"], 1)
            self.assertEqual(doc["sums"]["cases_passed"]["tool_loop"]["value"], 2)
            self.assertEqual(doc["sums"]["cases_passed"]["compact"]["status"], "not_measured")
            self.assertTrue(doc["sums"]["subunits_passed_not_a_score"])
            self.assertEqual(mod.validate(doc), [])
            committed = json.loads((SKILL / "examples" / "chart_data.json").read_text())
            self.assertEqual(committed["sums"]["cost_cut_pct"]["value"], doc["sums"]["cost_cut_pct"]["value"])
            code, _, err = run(["validate", str(out)])
            self.assertEqual(code, 0, err)
            code, _, err = run(["validate", str(SKILL / "examples" / "chart_data.json")])
            self.assertEqual(code, 0, err)

    def test_untraceable_number_fails(self):
        doc = mod.build(copy.deepcopy(RAW))
        doc["cases"][0]["results"]["baseline"]["secret_cost"] = 9.99
        errors = mod.validate(doc)
        self.assertTrue(any("untraceable" in e for e in errors), errors)

    def test_estimate_without_label_fails(self):
        doc = mod.build(copy.deepcopy(RAW))
        doc["sums"]["cost_usd"]["compact"]["display"] = "$3.00–$3.95"
        errors = mod.validate(doc)
        self.assertTrue(any("ESTIMATE" in e for e in errors), errors)

    def test_not_measured_cannot_carry_a_value(self):
        doc = mod.build(copy.deepcopy(RAW))
        doc["sums"]["wall_s"]["compact"] = {"status": "not_measured", "value": 12, "display": "not measured"}
        errors = mod.validate(doc)
        self.assertTrue(any("not_measured must not carry a value" in e for e in errors), errors)

    def test_passed_exceeds_n_fails(self):
        raw = copy.deepcopy(RAW)
        raw["cases"][0]["results"]["baseline"]["passed"] = 9
        raw["cases"][0]["results"]["baseline"]["subunits"] = []
        with self.assertRaises(mod.ValidationError) as caught:
            mod.build(raw)
        self.assertIn("passed exceeds n", str(caught.exception))

    def test_cost_stages_must_sum(self):
        raw = copy.deepcopy(RAW)
        raw["cases"][0]["results"]["baseline"]["cost_by_stage"]["worker"] = 99
        with self.assertRaises(mod.ValidationError) as caught:
            mod.build(raw)
        self.assertIn("cost_by_stage does not sum", str(caught.exception))

    def test_unknown_source_fails(self):
        raw = copy.deepcopy(RAW)
        raw["cases"][0]["results"]["baseline"]["source"] = "not-a-source"
        with self.assertRaises(mod.ValidationError) as caught:
            mod.build(raw)
        self.assertIn("unknown source", str(caught.exception))

    def test_subunit_sum_must_be_flagged_not_a_score(self):
        doc = mod.build(copy.deepcopy(RAW))
        del doc["sums"]["subunits_passed_not_a_score"]
        errors = mod.validate(doc)
        self.assertTrue(any("subunits_passed_not_a_score" in e for e in errors), errors)

    def test_missing_raw_is_not_measured(self):
        raw = copy.deepcopy(RAW)
        del raw["cases"][0]["results"]["compact"]["cost_usd"]
        doc = mod.build(raw)
        self.assertEqual(doc["cases"][0]["results"]["compact"]["cost_usd"]["status"], "not_measured")
        self.assertEqual(doc["cases"][0]["results"]["compact"]["cost_usd"]["display"], "not measured")


if __name__ == "__main__":
    unittest.main()
