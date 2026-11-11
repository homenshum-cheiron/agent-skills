import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "skill-report.yml"
CONFIG = ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml"
TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}
OPTIONAL = {
    "environment",
    "reproduction",
    "expected",
    "actual",
    "failure_stage",
    "measurement",
    "workaround",
    "evidence",
    "lesson",
}


def blocks(text):
    parts = re.split(r"\n  - type: ", text)
    found = []
    for part in parts[1:]:
        type_name = part.split("\n", 1)[0].strip()
        ident = re.search(r"\n    id: ([A-Za-z0-9_-]+)", part)
        required = re.search(r"\n    validations:\n      required: (true|false)(?:\n|$)", part)
        found.append((type_name, None if ident is None else ident.group(1), None if required is None else required.group(1) == "true"))
    return found


class IssueFormTests(unittest.TestCase):
    def test_form_shape_and_optional_metrics(self):
        text = FORM.read_text()
        self.assertNotIn("http://", text)
        self.assertNotIn("https://", text)
        self.assertIsNone(re.search(r"[A-Za-z0-9._%+-]+@", text))
        self.assertNotIn("slack.com", text)
        items = blocks(text)
        self.assertTrue(items)
        self.assertTrue(all(item[0] in TYPES for item in items))
        required = {item[1] for item in items if item[2]}
        self.assertEqual(required, {"skill_version", "outcome"})
        present = {item[1] for item in items if item[1]}
        self.assertTrue(OPTIONAL <= present)
        for ident in OPTIONAL:
            match = [item for item in items if item[1] == ident]
            self.assertEqual(match, [(match[0][0], ident, False)])

    def test_blank_issues_stay_available(self):
        text = CONFIG.read_text()
        self.assertIn("blank_issues_enabled: true", text)
        self.assertNotIn("contact_links", text)

    def test_yaml_parses_when_pyyaml_is_present(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed; structural checks already ran.")
        form = yaml.safe_load(FORM.read_text())
        config = yaml.safe_load(CONFIG.read_text())
        self.assertEqual(form["name"], "Skill report")
        self.assertEqual(config["blank_issues_enabled"], True)
        self.assertNotIn("contact_links", config)


if __name__ == "__main__":
    unittest.main()
