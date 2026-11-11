# Nine coverage prompts

These prompts check whether a pull-request body gives a new reviewer enough to judge the change. They are not a demand for every artifact on every change, and they are not a quality rating.

Mark each applicable prompt supported or missing. Use N/A only with a concrete rationale tied to the change. Report **supported / applicable**, then list the N/A items and their reasons. Do not award a silent 9/9. Do not compare an applicability-adjusted score to a fixed nine. Missing evidence is not N/A. Do not write "6/9 with two N/A." Write "6/7 applicable, plus 2 N/A with reasons."

1. **plain_summary.** Two or three sentences in plain words: what changed and why. Leave no jargon unexplained.
2. **how_it_works.** The mechanism, step by step, plus every flag or environment variable with its default, its range, and what 0 or off does. If there are none, say so.
3. **flowchart.** When runtime paths need explanation, a Mermaid diagram of behavior before versus after. A chart of where the pull request sits in a stack is not a runtime diagram. Skip an unnecessary diagram with a rationale.
4. **test_command.** The exact command and pasted output from a run on the current head, with failing-before and passing-after output where possible. A command without output is missing.
5. **structured_io.** A full request, response, payload, or config showing the behavior change where a structured contract exists, including a relevant failure and side effects. Do not force JSON onto a change with no structured-data contract.
6. **code_lines.** The key lines, with file path and line number.
7. **live_evidence.** Relevant traces, measured timing, or subscription or API usage, and screenshots for UI. Label each with the exact build: this head, a named local tree, or a combined stack. Never invent numbers or add a paid measurement to fill the section.
8. **unproven_risks.** What has not been measured, the known risks, and how to roll back.
9. **stack_position.** The base branch, parent and child pull requests, and what has to land first. Say standalone when there are no dependencies.

Also follow the review rules for running-surface proof, combined-stack honesty, and live-proof N/A. Before asking for a human decision, account for each distinct actionable automated finding on the current tip: fixed with evidence, rejected with a reproducible reason, duplicate of a named finding, or unresolved. An unresolved material finding blocks a ready claim. Never claim agent-written text was handwritten. For a successor, link both identities and establish preserved SHAs or patch content after a rebase, squash, or cherry-pick. Paste evidence from a real command, trace, or file. Write "not yet measured" rather than inventing it.

`scripts/score_coverage.py` checks that the nine marks are complete and that a claimed report matches **supported / applicable**. Exit 0 means the marks are well formed, including a body that still has missing prompts. It does not check that a rationale is true, and it is not a merge gate.

The fixture `examples/coverage.json` is the comment-only teaching case: six supported prompts, live evidence left missing because nothing was attached and N/A was not justified, and two N/A prompts with reasons.
