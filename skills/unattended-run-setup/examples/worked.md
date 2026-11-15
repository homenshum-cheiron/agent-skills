# Worked example (synthetic): setting up an overnight refactor

A maintainer wants a coding agent to split a 2,000-line module into four files overnight.

## Before

The prompt says "refactor the parser module and make it clean". The host file says "always use the strongest model at max effort" and "never touch CI files". A worker definition has no model pin. The instruction file also tells workers to print `ESCALATE` when a task feels hard, but the job is started by a plain CLI call.

Next morning: the run stopped after two files with "Remaining: split lexer, update imports". Three subagents ran on the most expensive model to read single files. The report says "refactor mostly done".

## Setup written instead

- Mode: unattended, lead at high. Workers: one per file split, model pinned, medium effort.
- Done when: `pytest -q` passes; `python -c "import parser"` works; four new files exist; no file over 600 lines; the public API list in `docs/api.md` is unchanged (diff empty).
- Places: `src/parser/**`, `tests/parser/**`, new branch `refactor/parser-split`, draft pull request. Ask before: editing CI files, deleting any test.
- Decisions asked up front: keep the old import path as a shim? (Answer recorded: yes, for one release.)
- Subagent note in the lead brief: "Each worker costs about a fresh session plus your re-read. Split only the four independent files; do imports yourself."
- Launcher: plain CLI. "No escalate lines; finish or report the blocker."
- Final report: test output, `git diff --stat`, list of every renamed symbol, what was not done.

## Result to check

The morning report lists 4 of 4 files, the passing test output, 11 renamed internal symbols, and one open item with its reason ("CI config references old path; ask-before rule, not edited").
