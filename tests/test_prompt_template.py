import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "prompts" / "finish-within-authority.md"
README = ROOT / "README.md"


class PromptTemplateTests(unittest.TestCase):
    def text(self):
        return TEMPLATE.read_text()

    def test_template_is_linked_and_bounded(self):
        text = self.text()
        readme = README.read_text()
        self.assertIn("docs/prompts/finish-within-authority.md", readme)
        for phrase in (
            "Who needs what result",
            "Acceptance:",
            "Known attempts",
            "Allowed mutation scope",
            "Current permissions",
            "Budget:",
            "Checkpoint:",
            "Escalate when",
            "Rollback:",
        ):
            self.assertIn(phrase, text)
        self.assertIn("Fable 5.2", text)
        self.assertIn("not a default", text)
        self.assertIn("does not demonstrate task autonomy", text)
        self.assertIn("does not override", text)
        self.assertIn("required approval", text.lower())
        self.assertIn("until the acceptance checks pass or a budget", text)

    def test_template_does_not_grant_blanket_authority(self):
        lowered = self.text().lower()
        self.assertNotIn("full authority to correct or alter anything", lowered)
        self.assertNotIn("proceed autonomously until you", lowered)
        self.assertIn("not a grant of permission", lowered)


if __name__ == "__main__":
    unittest.main()
