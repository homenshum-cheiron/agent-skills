import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/install_skills.sh"


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        (self.home / ".claude").mkdir()
        self.env = {"HOME": str(self.home), "PATH": "/usr/bin:/bin"}

    def run_script(self, *args):
        return subprocess.run(["sh", str(SCRIPT), *args], env=self.env, capture_output=True, text=True)

    def test_dry_run_changes_nothing(self):
        done = self.run_script("--skill", "working-set")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("Dry run", done.stdout)
        self.assertFalse((self.home / ".claude/skills").exists())

    def test_only_existing_hosts_by_default_and_apply_links(self):
        done = self.run_script("--apply", "--skill", "working-set")
        self.assertEqual(done.returncode, 0, done.stderr)
        link = self.home / ".claude/skills/working-set"
        self.assertTrue(link.is_symlink())
        self.assertEqual(Path(os.readlink(link)), ROOT / "skills/working-set")
        self.assertFalse((self.home / ".codex").exists())

    def test_never_overwrites_and_remove_only_own_links(self):
        own = self.home / ".claude/skills/working-set"
        mine = self.home / ".claude/skills/context-check"
        mine.mkdir(parents=True)
        (mine / "SKILL.md").write_text("local copy\n")
        self.run_script("--apply", "--skill", "working-set", "--skill", "context-check")
        self.assertEqual((mine / "SKILL.md").read_text(), "local copy\n")
        self.run_script("--apply", "--remove", "--skill", "working-set", "--skill", "context-check")
        self.assertFalse(own.exists() or own.is_symlink())
        self.assertTrue((mine / "SKILL.md").is_file())

    def test_rejects_path_like_names_and_missing_values(self):
        done = self.run_script("--apply", "--skill", "../skills/working-set")
        self.assertIn("not a plain skill name", done.stderr)
        self.assertFalse((self.home / ".claude/skills").exists())
        done = self.run_script("--skill")
        self.assertEqual(done.returncode, 2)
        self.assertIn("needs a value", done.stderr)

    def test_env_override_and_copy(self):
        target = self.home / "custom"
        self.env["CODEX_SKILLS_DIR"] = str(target)
        done = self.run_script("--apply", "--copy", "--host", "codex", "--skill", "working-set")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue((target / "working-set/SKILL.md").is_file())
        self.assertFalse((target / "working-set").is_symlink())


if __name__ == "__main__":
    unittest.main()
