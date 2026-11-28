import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "benchmark-charts"
sys.path.insert(0, str(ROOT / "scripts"))
import check_premium as cp  # noqa: E402

TEMPLATE = (ROOT / "references" / "canvas-template.tsx").read_text()
PRIMS = (ROOT / "references" / "premium-primitives.tsx").read_text()
PLAIN = (ROOT / "tests" / "fixtures" / "plain_chart.tsx").read_text()


def rules(fails):
    return {f["rule"] for f in fails}


class TemplatePasses(unittest.TestCase):
    def test_template_has_no_failures(self):
        fails, warns = cp.check(TEMPLATE, PRIMS)
        self.assertEqual(fails, [], fails)

    def test_primitives_block_is_verbatim_in_template(self):
        self.assertIn(PRIMS.strip(), TEMPLATE)

    def test_template_charts_all_use_chart_frame(self):
        charts = [n for n, _, b in cp.functions(TEMPLATE) if "<svg" in b and "/* pi:primitive */" not in b]
        self.assertGreaterEqual(len(charts), 8)
        for name, _, body in cp.functions(TEMPLATE):
            if name in charts:
                self.assertIn("<ChartFrame", body, name)

    def test_cli_exit_zero_on_template(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_premium.py"), str(ROOT / "references" / "canvas-template.tsx"), "--primitives", str(ROOT / "references" / "premium-primitives.tsx")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class PlainFails(unittest.TestCase):
    def test_plain_fixture_fails_expected_rules(self):
        fails, _ = cp.check(PLAIN)
        got = rules(fails)
        for r in ["P1", "P2", "P4", "P5", "P7", "P8", "P9", "P10", "P11", "P13", "P14"]:
            self.assertIn(r, got, f"missing {r} in {sorted(got)}")

    def test_cli_exit_one_on_plain(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_premium.py"), str(ROOT / "tests" / "fixtures" / "plain_chart.tsx")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAILED", r.stdout)

    def test_missing_file_exit_two(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_premium.py"), "/nonexistent.tsx"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


class SingleRules(unittest.TestCase):
    def test_drifted_primitives_fail_p0(self):
        drifted = TEMPLATE.replace("const ENTER_MS = 520;", "const ENTER_MS = 900;")
        self.assertIn("P0", rules(cp.check(drifted, PRIMS)[0]))

    def test_removing_reduced_motion_fails_p5(self):
        src = TEMPLATE.replace("prefers-reduced-motion", "prefers-color-scheme")
        self.assertIn("P5", rules(cp.check(src)[0]))

    def test_shadow_is_chart_junk(self):
        src = TEMPLATE.replace('padding: "10px 12px", color: t.text.primary', 'padding: "10px 12px", boxShadow: "0 2px 8px", color: t.text.primary')
        self.assertIn("P14", rules(cp.check(src)[0]))

    def test_static_diagram_allowed_with_marker(self):
        src = 'import { Diagram } from "grok/canvas";\n// pi:allow-static-diagram two-node legend only\nexport default function App() { return <Diagram nodes={[]} edges={[]} />; }\n'
        self.assertNotIn("P13", rules(cp.check(src)[0]))

    def test_kit_chart_without_control_warns_only(self):
        src = 'import { Page, Bars } from "grok/canvas";\nexport default function App() { return <Page title="x"><Bars bars={[]} /></Page>; }\n'
        fails, warns = cp.check(src)
        self.assertEqual(fails, [])
        self.assertIn("P6", rules(warns))

    def test_palette_literal_is_allowed(self):
        src = 'import { Page } from "grok/canvas";\nexport default function App() { return <Page title="x" palette={["#0B2545"]} />; }\n'
        self.assertNotIn("P8", rules(cp.check(src)[0]))


if __name__ == "__main__":
    unittest.main()
