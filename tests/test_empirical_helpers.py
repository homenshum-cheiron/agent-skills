"""Independent deterministic boundary probes; not model-behavior evidence."""
import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_helpers import ROOT, packet, timing

class EmpiricalIntervalTests(unittest.TestCase):
    def test_integer_grid_oracle_250_cases(self):
        rng = random.Random(71031)
        for case in range(250):
            lo, hi = -10, 30
            pairs = [tuple(sorted((rng.randint(lo, hi), rng.randint(lo, hi)))) for _ in range(rng.randint(1, 15))]
            doc = {"window_start": lo, "window_end": hi, "spans": [{"name": str(i), "start": a, "end": b} for i, (a, b) in enumerate(pairs)]}
            result = timing.summarize(doc)
            cells = {i for a, b in pairs for i in range(a, b)}
            with self.subTest(case=case):
                self.assertEqual(result["covered_time"], len(cells))
                self.assertEqual(result["summed_work"], sum(b-a for a,b in pairs))
                self.assertEqual(result["unexplained_time"], hi-lo-len(cells))
                self.assertEqual(sum(b-a for a,b in result["gaps"]), hi-lo-len(cells))

    def test_translation_and_scale_50_cases(self):
        rng = random.Random(219)
        for case in range(50):
            pairs = [tuple(sorted((rng.randint(0, 20), rng.randint(0, 20)))) for _ in range(8)]
            def build(scale, offset):
                return {"window_start": offset, "window_end": 20*scale+offset, "spans": [{"name": str(i), "start": a*scale+offset, "end": b*scale+offset} for i,(a,b) in enumerate(pairs)]}
            a, b = timing.summarize(build(1,0)), timing.summarize(build(3,-7))
            with self.subTest(case=case):
                for key in ("wall_time", "covered_time", "summed_work", "unexplained_time"):
                    self.assertEqual(b[key], a[key]*3)

class EmpiricalPacketTests(unittest.TestCase):
    def test_huge_integer_json_returns_structured_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"packet.json"
            p.write_text('{"schema_version":'+"1"*5000+'}')
            r=subprocess.run([sys.executable, str(ROOT/"skills/proof-before-review/scripts/check_packet.py"), str(p)], text=True, capture_output=True)
            self.assertEqual(r.returncode, 3, r.stderr)
            self.assertEqual(json.loads(r.stdout)["status"], "invalid")
            self.assertNotIn("Traceback", r.stderr)

    def test_deep_json_returns_structured_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "nested.json"
            p.write_text("[" * 2000 + "0" + "]" * 2000)
            for script, code in (("skills/proof-before-review/scripts/check_packet.py", 3), ("skills/measure-the-path/scripts/summarize_intervals.py", 1)):
                with self.subTest(script=script):
                    r = subprocess.run([sys.executable, str(ROOT / script), str(p)], text=True, capture_output=True)
                    self.assertEqual(r.returncode, code, r.stderr)
                    self.assertIsInstance(json.loads(r.stdout), dict)
                    self.assertNotIn("Traceback", r.stderr)

    def test_json_shape_grid_never_claims_complete(self):
        values=[None, True, False, 0, 1, "", "x", [], {}, [1]]
        for value in values:
            with self.subTest(value=value):
                self.assertNotEqual(packet.evaluate(value, ROOT)["status"], "complete")

if __name__ == "__main__":
    unittest.main()
