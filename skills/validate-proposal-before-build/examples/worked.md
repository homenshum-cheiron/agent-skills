# Worked example (synthetic): a viral "harness loop" card

This example is synthetic in its wording and is not a transcript. It follows a real public pattern: a short card that compresses a longer article about coding-agent loops into a "paste this tonight" checklist.

## Source (intake)

- A public social post and an accompanying card titled along the lines of "a unified framework for harness loops and task graphs."
- The card's author account later became unavailable; the longer article is from a different public author on the same day.
- Proposed target, as written: any coding agent. The card says to paste the framework into a strong model "tonight."

Quoted elements of the proposal (paraphrased, not copied at length): treat the agent as model plus harness; write a contract `(goal, constraints, done)`; define `done` as a repo script such as `./check.sh`; run a produce / check / correct loop with a small retry cap; if the same error appears twice, write `STATE.md` and stop; give each failed node a scoped return value; set `{allow, ask, deny}` gates by undo cost; auto-append repeated failures into a standing project file; run the check from a stop hook and block completion when it fails.

## Intent and execution

- **Claimed outcome:** fewer stalled loops, a mechanical done-signal, and safer tool use, without new measurements on the card.
- **Mechanism:** move judgment out of the model and into hooks, scripts, and a short contract.
- **Execution path:** new or heavier stop hooks, a universal check script, a retry cap, a standing-file auto-append, and a single-model overnight trial.
- **Unstated assumptions:** that a script can grade every task; that "the same error twice" is a stall even when the plan changed; that a stop hook is a hard gate; that the named model is available and appropriate for every workload.
- **Open questions:** which official hook contract is assumed? what is the evidence for the retry cap? who protects the check script from being edited?

## Map to what already exists

Most coding-agent hosts already ship pieces of this: stop or session-end hooks, permission allow/ask/deny lists, worktrees or isolated checkouts, project instruction files, and handoff notes. A host that already writes a handoff on compact or takeover does not need a second handoff format. A host that already has a permission or auto-review layer does not need a new "gate framework."

What is usually missing is narrower: a stall stop when the *same command* fails with the *same error* and the plan has not changed; a deny or ask rule that stops the agent editing the check or its gold fixtures; and a hook that uses the worktree working directory rather than the main checkout path.

## Research (short)

- Official hook docs: a stop hook that exits 2 may continue the turn, can fire at the end of a turn rather than only at "task done," and may have a consecutive-block cap. A missing script is often non-blocking. After entering a worktree, a project-root environment variable may still point at the main checkout, while the hook's working directory follows the worktree.
- Papers: intrinsic self-correction can *hurt* without an external signal (Huang et al., arXiv 2310.01798). A harness can add noise; reruns flip a non-trivial share of tasks (arXiv 2610.04433). A harness tuned on one model can hurt another (JoMoHa, arXiv 2611.11499).
- Field: public issues document stop-hook loops when the condition is fuzzy. Writers warn that agents will weaken tests if the check is editable.
- The longer source article already carries caveats the card drops: some quality is not scriptable; promote repeats into hooks or tests and keep standing files short; a stall is two rounds with no progress, not a magic retry number.

## Options

1. Do nothing: keep native hooks, permissions, worktrees, and existing handoff skills.
2. Adopt three small, reversible pieces: same-command stall stop plus a handoff file; protect the check from edits; audit hooks and permissions for worktree awareness.
3. Adopt the whole card, including auto-append into the standing file and a script-only done-signal for every task.
4. Run a large paid eval of the named model overnight.

## Lean test

Free first: read official hook and permission docs; inventory the current hook and permission files (do not print secrets); mine existing session logs for same-command retries versus changed-plan recovery. Do not start a paid model eval until those $0 rungs are done.

In a local log audit of this pattern, the second identical command sometimes recovered; a third identical try did not pay off in a small sample; recovery after a repeated error was common only when the command or plan changed. Treat those as method examples, not as a published benchmark.

## Verdict

- Skip the card as a package, the auto-append into standing project files, a script-only done-signal for work a script cannot grade, and an unmeasured "paste into a named model tonight" step.
- Adopt, as drafts only, the three small pieces in option 2, and only for tasks that already have a deterministic check.
- Park a hard-coded retry cap until a larger log sample exists; park a stop-hook check until it uses the hook working directory, honors any official "stop hook already active" flag, and stays inside any block cap.

**Why it looked stronger than it is:** the card compressed a careful article into a slogan and dropped the caveats.

**Why this was not already standard:** scans often watch product graders and model swaps, not coding-loop stall exits. The missing signal was a cheap same-command retry count.

**What would change the verdict:** a powered eval on a named workload, or a log mine that shows third identical retries regularly succeeding. Neither revives script-only done for unscriptable quality, or an overnight paste into a model that the account or region cannot use.

## Register row (pattern)

Source, date, "skip the package / adopt three small drafts / park the cap," link to the research note, revisit if a larger $0 log mine lands.
