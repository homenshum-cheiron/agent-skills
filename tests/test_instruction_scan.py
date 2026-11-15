import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/instruction-hygiene-review/scripts/scan_instructions.py"
spec = importlib.util.spec_from_file_location("scan_instructions", SCRIPT)
scan_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan_mod)


class InstructionScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / "home"
        self.rules = self.home / "rules"
        self.rules.mkdir(parents=True)
        (self.home / "exists.md").write_text("x\n")
        shared = [f"This shared synthetic rule line number {i} is long enough to count as a duplicated standing instruction in both files." for i in range(3)]
        (self.rules / "AGENTS.md").write_text("\n".join([
            "Reasoning effort: xhigh for judges.",
            "Effort cap: high. Never set effort above high (no xhigh, no max).",
            "Old note: the word \"max\" effort was retired.",
            "Cloud agents refused until on-demand (2020-01-02).",
            "See ~/exists.md and ~/missing/file.md.",
            "Tool-x is banned.",
            *shared,
        ]) + "\n")
        (self.rules / "CLAUDE.md").write_text("\n".join(["tool-x is allowed.", *shared]) + "\n")
        (self.rules / "notes.txt").write_text("Reasoning effort: max\n")

    def run_scan(self, **kw):
        return scan_mod.scan([str(self.rules)], {"AGENTS.md": 400}, kw.get("cap", "high"), "2026-01-01", self.home)

    def types(self, result):
        return [f["type"] for f in result["findings"]]

    def test_flags_effort_above_cap_but_not_negated_or_quoted(self):
        result = self.run_scan()
        hits = [f for f in result["findings"] if f["type"] == "effort-above-cap"]
        self.assertEqual([(Path(f["path"]).name, f["line"], f["level"]) for f in hits], [("AGENTS.md", 1, "xhigh")])

    def test_ignores_non_instruction_files(self):
        result = self.run_scan()
        self.assertEqual(sorted(Path(p).name for p in result["files"]), ["AGENTS.md", "CLAUDE.md"])

    def test_cap_is_configurable(self):
        result = self.run_scan(cap="xhigh")
        self.assertNotIn("effort-above-cap", self.types(result))

    def test_stale_pending_missing_path_polarity_duplicate_and_size(self):
        result = self.run_scan()
        found = self.types(result)
        for kind in ("stale-pending", "missing-path", "polarity-conflict", "duplicate-instruction", "size-near-loader-limit"):
            self.assertIn(kind, found)
        missing = [f["reference"] for f in result["findings"] if f["type"] == "missing-path"]
        self.assertEqual(missing, ["~/missing/file.md"])

    def test_cli_writes_dated_reports_without_overwriting(self):
        out = Path(self.tmp.name) / "out"
        env = {"HOME": str(self.home), "PATH": "/usr/bin:/bin", "INSTRUCTION_SCAN_ROOTS": str(self.rules)}
        for _ in range(2):
            done = subprocess.run([sys.executable, "-B", str(SCRIPT), "--out", str(out), "--today", "2026-01-01"],
                                  env=env, capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
        names = sorted(p.name for p in out.iterdir())
        self.assertEqual(names, ["instruction-scan-2026-01-01-1.json", "instruction-scan-2026-01-01-1.md",
                                 "instruction-scan-2026-01-01.json", "instruction-scan-2026-01-01.md"])
        record = json.loads((out / "instruction-scan-2026-01-01.json").read_text())
        self.assertEqual(record["schema_version"], 1)
        self.assertTrue(record["findings"])

    def test_fail_on_findings_exit_code(self):
        out = Path(self.tmp.name) / "out2"
        done = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.rules), "--out", str(out),
                               "--fail-on-findings"], env={"HOME": str(self.home), "PATH": "/usr/bin:/bin"},
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 1, done.stderr)


if __name__ == "__main__":
    unittest.main()
