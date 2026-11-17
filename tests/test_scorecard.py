"""Eval scorecard and owner-routed brief packages: honest-number rules on synthetic CSVs; not model-behavior evidence."""
import importlib.util
import io
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "owner-routed-brief"
SCORE = ROOT / "skills" / "eval-scorecard"
SPEC = importlib.util.spec_from_file_location("scorecard", SCORE / "scripts" / "scorecard.py")
scorecard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scorecard)

HEADER = "case_id,verdict,duration_s,cost_usd,finished,cache_write_usd\n"


def run(text, *args):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "cases.csv"
        path.write_text(text)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = scorecard.main([str(path), *args])
        return code, out.getvalue(), err.getvalue()


class OwnerRoutedBriefFolder(unittest.TestCase):
    def test_files_present(self):
        for relative in ("SKILL.md", "config.example.yaml", "HOSTS.md", "PORTABLE.md",
                         "references/card-template.md", "examples/worked.md", "agents/openai.yaml"):
            self.assertTrue((SKILL / relative).is_file(), relative)
        self.assertTrue((SCORE / "scripts" / "scorecard.py").is_file())

    def test_frontmatter_names_folder_and_says_when(self):
        text = (SKILL / "SKILL.md").read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S).group(1)
        self.assertIn("name: owner-routed-brief", front)
        self.assertRegex(front, r'description: "Use when .+Daily.+Nightly.+"')

    def test_generic_recipe_names_no_team_specifics(self):
        text = (SKILL / "SKILL.md").read_text() + (SKILL / "PORTABLE.md").read_text()
        for word in ("#backend", "#qa", "answer-key.json"):
            self.assertNotIn(word, text)

    def test_metrics_block_required_in_template(self):
        text = (SKILL / "references" / "card-template.md").read_text()
        for field in ("p50", "p95", "Tasks finished per hour", "per passed task", "Cache-write share"):
            self.assertIn(field, text)


class Scorecard(unittest.TestCase):
    def test_counts_four_verdicts_and_never_pools(self):
        code, out, _ = run(HEADER + "a,passed,60,1,true,0.5\nb,failed,120,2,true,1\n"
                           "c,inconclusive,600,3,false,1.5\nd,unverified,,,,\n")
        self.assertEqual(code, 0)
        for line in ("| Passed | 1 |", "| Failed | 1 |", "| Unverified | 1 |", "| Inconclusive | 1 |"):
            self.assertIn(line, out)
        self.assertNotIn("%  |", out.split("Cache-write")[0])
        self.assertNotIn("pass rate", out.lower())

    def test_missing_numbers_are_missing_not_zero(self):
        code, out, _ = run(HEADER + "a,passed,,,,\n")
        self.assertEqual(code, 0)
        self.assertIn("| Latency p50 per case (nearest rank) | missing |", out)
        self.assertIn("| Cost per case | missing |", out)
        self.assertNotIn("$0.00", out)

    def test_throughput_is_an_estimate_without_a_window(self):
        rows = HEADER + "a,passed,1800,4,true,\nb,failed,1800,4,true,\n"
        _, out, _ = run(rows)
        self.assertIn("serial equivalent", out)
        self.assertIn("estimate", out)
        _, out, _ = run(rows, "--wall-seconds", "1800")
        self.assertIn("| Tasks finished per hour | 4.00 |", out)

    def test_nearest_rank_percentiles(self):
        values = sorted(float(v) for v in range(1, 32))
        self.assertEqual(scorecard.nearest_rank(values, 50), 16.0)
        self.assertEqual(scorecard.nearest_rank(values, 90), 28.0)
        self.assertEqual(scorecard.nearest_rank(values, 95), 30.0)

    def test_cost_per_passed_needs_every_cost(self):
        _, out, _ = run(HEADER + "a,passed,10,2,true,\nb,failed,10,,true,\n")
        self.assertIn("| Cost per passed case | missing |", out)
        _, out, _ = run(HEADER + "a,passed,10,2,true,1\nb,failed,10,2,true,1\n")
        self.assertIn("| Cost per passed case | $4.00 |", out)
        self.assertIn("| Cache-write share of cost | 50% |", out)

    def test_nonfinite_and_invalid_window_rejected(self):
        for value in ("nan", "inf", "-1"):
            code, _, _ = run(HEADER + f"a,passed,{value},2,true,1\n")
            self.assertEqual(code, 2)
        for value in ("nan", "inf", "0", "-1"):
            code, _, _ = run(HEADER + "a,passed,1,2,true,1\n", "--wall-seconds", value)
            self.assertEqual(code, 2)

    def test_cache_share_requires_paired_nonzero_costs(self):
        for rows in ("a,passed,1,2,true,\nb,failed,1,,true,1\n",
                     "a,passed,1,0,true,0\n"):
            _, out, _ = run(HEADER + rows)
            self.assertIn("| Cache-write share of cost | missing |", out)

    def test_bad_input_exits_2(self):
        for text in (HEADER + "a,pass,1,1,true,\n",          # unknown verdict
                     "case_id,duration_s\na,1\n",             # missing verdict column
                     HEADER + "a,passed,fast,1,true,\n",      # not a number
                     HEADER + "a,passed,1,1,true,\na,failed,1,1,true,\n"):  # duplicate id
            code, _, err = run(text)
            self.assertEqual(code, 2, text)
            self.assertIn("bad input", err)


if __name__ == "__main__":
    unittest.main()
