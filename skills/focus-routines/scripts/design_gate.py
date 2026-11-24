#!/usr/bin/env python3
"""Design-first gate: fail a branch unless a design file landed in a commit BEFORE the first code commit.

Order is commit position in base..head (oldest first), not commit time. A rebase rewrites times; position survives it.
Design file = a file ADDED in base..head that is under docs/design/, or named DESIGN*.md / PLAN*.md / *.design.md / *.mmd,
has at least DESIGN_MIN_LINES non-blank lines (default 3), and still exists at head.
A design kept outside the repository also counts: put a reference string (8+ characters) in the body, and record it in the
ledger file (DESIGN_LEDGER, default <FOCUS_DIR or ~/.focus>/design-ledger.jsonl) as {"ref": "...", "created": "<ISO time>"}.
It counts when "created" is before the first code commit's time. The ledger is trusted as written.
Code = any changed file that is not a design file and not prose or an image (.md .mmd .txt .rst .png .svg .jpg .gif .pdf).
Exempt only if the total changed lines are at most DESIGN_EXEMPT_LINES (default 30), nothing binary changed, and the body
has a line "design-exempt: <reason>".
Verdicts: passed (exit 0) / failed (exit 1) / inconclusive (git or the body is unreadable, exit 2). Usage error: 64.

Usage: design_gate.py <repo_dir> <base> <head> [--body FILE]   |   --selftest
The body is the pull request text or the commit messages of the branch.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile

PROSE = r"\.(md|mmd|txt|rst|png|svg|jpe?g|gif|pdf)$"
DESIGN = re.compile(r"(^|/)(docs/design/[^/].*|DESIGN[^/]*\.md|PLAN[^/]*\.md|[^/]+\.design\.md|[^/]+\.mmd)$")
NOT_CODE = re.compile(PROSE, re.I)


def setting(name, default):
    return int(os.environ.get(name) or default)


def ledger_path():
    home = os.environ.get("FOCUS_DIR") or os.path.join(os.path.expanduser("~"), ".focus")
    return os.environ.get("DESIGN_LEDGER") or os.path.join(home, "design-ledger.jsonl")


def git(repo, *args, ok_fail=False):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode and not ok_fail:
        raise RuntimeError(f"git {args[0]} failed")
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def commits(repo, base, head):
    out = git(repo, "log", "--reverse", "--topo-order", "--no-renames", "--format=@%H %ct", "--name-status", f"{base}..{head}")
    found, cur = [], None
    for line in out.splitlines():
        if line.startswith("@"):
            sha, when = line[1:].split()
            cur = {"sha": sha, "t": int(when), "files": []}
            found.append(cur)
        elif line.strip():
            status, *paths = line.split("\t")
            cur["files"].append((status[0], paths[-1]))
    return found


def real_design(repo, sha, head, path):
    """Added design file with content that is still there at the tip."""
    blob = git(repo, "show", f"{sha}:{path}", ok_fail=True) or ""
    enough = sum(1 for line in blob.splitlines() if line.strip()) >= setting("DESIGN_MIN_LINES", 3)
    return enough and git(repo, "cat-file", "-e", f"{head}:{path}", ok_fail=True) is not None


def ledger_time(body):
    best = None
    if not os.path.exists(ledger_path()):
        return None
    with open(ledger_path()) as fh:
        for line in fh:
            try:
                row = json.loads(line)
                ref = row["ref"]
                t = dt.datetime.fromisoformat(row["created"].replace("Z", "+00:00"))
            except (ValueError, KeyError, TypeError, AttributeError):
                continue   # a bad row gives no credit
            if isinstance(ref, str) and len(ref.strip()) >= 8 and ref in body:
                stamp = int((t if t.tzinfo else t.astimezone()).timestamp())
                best = stamp if best is None else min(best, stamp)
    return best


def check(repo, base, head, body=""):
    found = commits(repo, base, head)
    is_code = lambda f: not DESIGN.search(f) and not NOT_CODE.search(f)
    code_i = next((i for i, c in enumerate(found) if any(is_code(f) for _, f in c["files"])), None)
    if code_i is None:
        return "passed", "no code commits"
    binary, lines = False, 0
    for row in git(repo, "diff", "--numstat", f"{base}...{head}").splitlines():
        added, removed, *_ = row.split("\t")
        if added == "-":
            binary = True
        else:
            lines += int(added) + int(removed)
    limit = setting("DESIGN_EXEMPT_LINES", 30)
    if lines <= limit and not binary and re.search(r"(?m)^design-exempt:[ \t]*\S", body):
        return "passed", f"exempt ({lines} changed lines, limit {limit})"
    recorded = ledger_time(body)
    if recorded is not None and recorded < found[code_i]["t"]:
        return "passed", "a design recorded in the ledger is older than the first code commit"
    named = [(i, c, f) for i, c in enumerate(found) for status, f in c["files"] if status == "A" and DESIGN.search(f)]
    good = [(i, c, f) for i, c, f in named if real_design(repo, c["sha"], head, f)]
    if not good:
        thin = f"; {len(named)} design-named file(s) were too short or are gone at the tip" if named else ""
        return "failed", "no design file in the branch or the ledger" + thin
    i, _, f = good[0]
    if i == code_i:
        return "failed", f"design {f} landed in the same commit as the first code; it must come before"
    if i > code_i:
        return "failed", f"design {f} landed {i - code_i} commit(s) after the first code commit"
    return "passed", f"design {f} landed {code_i - i} commit(s) before the first code commit"


def selftest():
    """Builds a throwaway repository in a temporary folder. Every commit gets the same time, so only position can decide."""
    with tempfile.TemporaryDirectory() as d:
        env = {**os.environ, "GIT_AUTHOR_DATE": "@1900000000 +0000", "GIT_COMMITTER_DATE": "@1900000000 +0000"}
        run = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, env=env)
        run("init", "-q")
        run("config", "user.email", "selftest@example.invalid")
        run("config", "user.name", "selftest")
        os.environ["DESIGN_LEDGER"] = os.path.join(d, "no-ledger.jsonl")

        def commit(path, content):
            full = os.path.join(d, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as fh:
                fh.write(content)
            run("add", ".")
            run("commit", "-qm", f"add {path}")

        design, code = "# Design\n\nWhat changes.\nWhy.\n", "print(1)\n" * 40
        commit("README.md", "seed\n")
        base = git(d, "rev-parse", "HEAD").strip()
        branch = lambda name: run("checkout", "-q", "-b", name, base)
        commit("src/a.py", code); commit("docs/design/a.md", design)
        assert check(d, base, "HEAD") == ("failed", "design docs/design/a.md landed 1 commit(s) after the first code commit")
        branch("before"); commit("docs/design/b.md", design); commit("src/b.py", code)
        assert check(d, base, "HEAD")[0] == "passed"
        branch("none"); commit("src/c.py", code)
        assert check(d, base, "HEAD")[0] == "failed"
        branch("thin"); commit("DESIGN.md", "todo\n"); commit("src/d.py", code)
        assert "too short" in check(d, base, "HEAD")[1]
        branch("tiny"); commit("src/e.py", "x = 1\n")
        assert check(d, base, "HEAD")[0] == "failed" and check(d, base, "HEAD", "design-exempt: typo")[0] == "passed"
        assert check(d, base, "HEAD", "design-exempt:")[0] == "failed"          # a reason is required
        branch("big"); commit("src/f.py", "x = 1\n" * 31)
        assert check(d, base, "HEAD", "design-exempt: not small")[0] == "failed"
        branch("docs"); commit("notes.md", "words\n")
        assert check(d, base, "HEAD") == ("passed", "no code commits")
        try:
            check(d, base, "no-such-ref")
            raise AssertionError("a missing ref must raise")
        except RuntimeError:
            pass
    print("selftest: after, none, thin, tiny, bare exempt and over-limit fail; before, exempt and docs-only pass; a bad ref raises")
    return 0


def main(argv):
    usage = "usage: design_gate.py <repo_dir> <base> <head> [--body FILE] | --selftest"
    if argv and argv[0] == "--selftest":
        return selftest()
    body_file = None
    if "--body" in argv:
        i = argv.index("--body")
        if i + 1 >= len(argv):
            print(usage, file=sys.stderr)
            return 64
        body_file = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 3:
        print(usage, file=sys.stderr)
        return 64
    try:
        body = ""
        if body_file:
            with open(body_file) as fh:
                body = fh.read()
        verdict, detail = check(argv[0], argv[1], argv[2], body)
    except (RuntimeError, OSError, ValueError) as e:
        verdict, detail = "inconclusive", f"could not read the repository, the refs or the body: {type(e).__name__}"
    print(json.dumps({"check": "design_first", "verdict": verdict, "pass": verdict == "passed", "detail": detail}))
    return {"passed": 0, "failed": 1}.get(verdict, 2)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
