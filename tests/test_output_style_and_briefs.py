"""Checkers for the four-line work reply and the four-part worker brief. Synthetic text only."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


STYLE = load("lint_output_style", ROOT / "skills/bluf-notes/scripts/lint_output_style.py")
BRIEF = load("lint_brief", ROOT / "skills/worker-brief/scripts/lint_brief.py")


def examples_from_chat_replies():
    text = (ROOT / "skills/bluf-notes/references/chat-replies.md").read_text()
    chunks = []
    current = []
    for line in text.splitlines():
        if line.startswith(">"):
            current.append(line[1:].lstrip())
        else:
            if current:
                chunks.append("\n".join(current))
                current = []
    if current:
        chunks.append("\n".join(current))
    return [c for c in chunks if "Needs you" in c]


GOOD_REPLY = """**Needs you:** none.
**Done?** Yes. The checker examples both pass.
**How:** Ran lint_output_style.py on the two reference replies.
**Problems:** none.
"""

BURIED_DECISION = """**Needs you:** none.
**Done?** Yes. The report is written.
**How:** Read the notes and drafted a summary.
**Problems:** none.

## DECISION NEEDED
1. Ship it.
2. Wait.
"""

NO_BECAUSE = """**Needs you:** none.
**Done?** Partly. The index builds, but one query misses.
**How:** Ran the frozen cases.
**Problems:** **NOT DONE:** the Hangul query.
"""

LONG_NO_LINK = "**Needs you:** none.\n**Done?** Yes. Filler.\n**How:** Read files.\n**Problems:** none.\n\n" + ("word " * 210)


class OutputStyleLint(unittest.TestCase):
    def test_reference_examples_pass(self):
        chunks = examples_from_chat_replies()
        self.assertGreaterEqual(len(chunks), 2)
        for chunk in chunks:
            self.assertEqual(STYLE.lint(chunk), [], chunk[:80])

    def test_good_reply_passes(self):
        self.assertEqual(STYLE.lint(GOOD_REPLY), [])

    def test_missing_label_fails(self):
        text = "**Needs you:** none.\n**Done?** Yes. Goal met.\n**How:** Ran tests.\n"
        errs = STYLE.lint(text)
        self.assertTrue(any("missing labels" in e for e in errs))

    def test_done_must_be_yes_no_partly(self):
        text = GOOD_REPLY.replace("Yes. The checker examples both pass.", "It is finished.")
        errs = STYLE.lint(text)
        self.assertTrue(any("Done?" in e for e in errs))

    def test_buried_decision_fails(self):
        errs = STYLE.lint(BURIED_DECISION)
        self.assertTrue(any("buried" in e for e in errs))

    def test_problem_without_reason_fails(self):
        errs = STYLE.lint(NO_BECAUSE)
        self.assertTrue(any("no reason" in e for e in errs))

    def test_long_reply_needs_a_writeup_link(self):
        errs = STYLE.lint(LONG_NO_LINK)
        self.assertTrue(any("no link" in e for e in errs))
        self.assertEqual(STYLE.lint(LONG_NO_LINK + "\nSee docs/full-writeup.md\n"), [])


class WorkerBriefLint(unittest.TestCase):
    def test_worked_example_and_template_pass(self):
        skill = ROOT / "skills/worker-brief"
        self.assertEqual(BRIEF.lint((skill / "examples/worked.md").read_text()), [])
        self.assertEqual(BRIEF.lint((skill / "references/template.md").read_text()), [])

    def test_missing_heading_fails(self):
        text = (ROOT / "skills/worker-brief/examples/worked.md").read_text()
        text = text.replace("## Why", "## Motive")
        errs = BRIEF.lint(text)
        self.assertTrue(any("missing headings" in e for e in errs))

    def test_empty_why_fails(self):
        text = (ROOT / "skills/worker-brief/examples/worked.md").read_text()
        text = text.replace(
            "Reviewers read top-down. A decision or a missed failure that sits at the end of a long reply is easy to skip. A checker that can fail makes the style enforceable, not just described.",
            "TBD",
        )
        errs = BRIEF.lint(text)
        self.assertTrue(any("Why" in e for e in errs))

    def test_guardrail_needs_because(self):
        text = (ROOT / "skills/worker-brief/examples/worked.md").read_text()
        text = text.replace(", because publication needs an explicit later yes.", ".")
        errs = BRIEF.lint(text)
        self.assertTrue(any("because" in e for e in errs))

    def test_job_of_numbered_steps_fails(self):
        text = """# Brief
## Job
1. Open the repo.
2. Edit the file.
3. Run the tests.
4. Commit the result.
## Why
This job exists so a later reviewer can trust the change was tested.
## Guardrails
- Do not push, because publication needs a later yes.
## Done means
- [ ] `python3 -m unittest discover -s tests` exits 0.
"""
        errs = BRIEF.lint(text)
        self.assertTrue(any("how-to" in e for e in errs))


class PackagesPresent(unittest.TestCase):
    def test_expected_files_exist(self):
        for rel in (
            "skills/bluf-notes/references/chat-replies.md",
            "skills/bluf-notes/scripts/lint_output_style.py",
            "skills/worker-brief/SKILL.md",
            "skills/meeting-action-drafts/SKILL.md",
            "skills/frozen-holdout-eval/SKILL.md",
            "skills/transcript-capture/SKILL.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
