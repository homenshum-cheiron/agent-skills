#!/usr/bin/env python3
"""Check package structure and common publication hazards; not a complete audit."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
# Detect common private paths and credentials without storing real examples.
PATTERNS = {
    "absolute home path": r"/(?:Users|home)/[A-Za-z][^\s/]+/",
    "private Slack message URL": r"https?://[^\s/]+\.slack\.com/archives/",
    "private Notion page URL": r"https?://(?:app\.)?notion\.(?:com|so)/p/",
    "credential-shaped value": r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})",
    "private key block": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
}


def validate(root=ROOT):
    errors = []
    root = Path(root).resolve()
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("No skills found.")
    for path in root.rglob("*"):
        if any(part in {".git", "__pycache__", ".venv"} for part in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            errors.append(f"Symlink not allowed: {path.relative_to(root)}")
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except (UnicodeError, OSError):
            errors.append(f"Unreadable or binary file requires review: {path.relative_to(root)}")
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, text):
                errors.append(f"Publication scan: {label} in {path.relative_to(root)}")
        if path.suffix != ".md":
            continue
        # All repository-authored Markdown links use inline targets without spaces.
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            destination = (path.parent / target.split("#", 1)[0]).resolve()
            if not destination.exists():
                errors.append(f"Broken link in {path.relative_to(root)}: {target}")
            try:
                destination.relative_to(root)
            except ValueError:
                errors.append(f"Link escapes repository: {path.relative_to(root)}: {target}")
            relative = path.relative_to(root)
            if relative.parts[0] == "skills":
                package = root / "skills" / relative.parts[1]
                try:
                    destination.relative_to(package)
                except ValueError:
                    errors.append(f"Skill link leaves package: {relative}: {target}")
    names = set()
    for path in skills:
        text = path.read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front:
            errors.append(f"Missing frontmatter: {path.relative_to(root)}")
            continue
        name = re.search(r"^name: ([a-z0-9-]+)$", front.group(1), re.M)
        desc = re.search(r'^description: "(.+)"$', front.group(1), re.M)
        if not name or name.group(1) != path.parent.name or len(name.group(1)) > 64:
            errors.append(f"Invalid package name: {path.relative_to(root)}")
        elif name.group(1) in names:
            errors.append(f"Duplicate name: {name.group(1)}")
        else:
            names.add(name.group(1))
        if not desc:
            errors.append(f"Missing description: {path.relative_to(root)}")
        if len(text.split()) > 900:
            errors.append(f"Entrypoint too large: {path.relative_to(root)}")
        if not (path.parent / "examples" / "worked.md").is_file():
            errors.append(f"Worked example missing: {path.parent.name}")
    return errors, len(skills)


if __name__ == "__main__":
    errors, count = validate()
    for error in errors:
        print(error)
    print(f"{count} skills checked; {len(errors)} issues. Structural checks are not semantic or privacy proof.")
    sys.exit(bool(errors))
