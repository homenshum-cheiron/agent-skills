# Finding format

One finding per block. Rank the blocks by harm avoided first, then money.

```
- Finding: <one sentence: what is wasted or wrong, and where>
  - Pipeline / component: <pipeline>.<type>.<name>  (shared: used by <list>, if shared.*)
  - FM ID: FM-<component>-NN, count this run <n> of <failed rows>, tracking status <tracked and posted | tracked, not posted | untracked>
  - Evidence: <numbers>, <trace or run links>, version stamp <commit, prompts, skills, tools, model ID, grader>
  - Premise: volume/yr <n> (OBS|DER|EST, source) · change/yr at base <..> and high <..> · risk direction <..> · harm or gain in real units <..> · significance <n, test, interval, or "not significant">
  - Not covered: <no cases | no grader measure | no volume | dev-only traffic | list price, not invoice>
  - Proposed fix: <one change, tied to one lever: data, tool, prompt, check, output, orchestration, or model>
  - Alternative considered: <option> — why the main fix wins
  - Research: <source link> — why it applies here, and any mismatch (task, scale)
  - Test: <lean-test-design plan link>, owner who reads it
  - Owner who acts: <team or person, from a source; else TBD>
```

## Evidence to read first (free)

- **Cost:** traces grouped by pipeline over two windows (for example 30 and 7 days): trace count, total and per-run cost, main models, environment. Report unattributed and uncosted spans separately; never guess them into a pipeline.
- **Time and robustness:** per-phase timing, tool-call counts, retries, timeouts, rerun instability.
- **Quality:** failed rows from the latest eval on the current version, grouped by the measure they failed. Count confident-wrong answers separately.
- **What changed:** code, prompts, models, tools, and graders since the last lap.

A baseline is the latest graded run on the same version. Older figures are references.

## Self-review before anyone reads it

Answer each question in the finding text:

- Which component exactly, and is it the most upstream broken contract?
- Which model exactly? Cheaper than what?
- Production traffic or development traffic?
- Is the baseline on the same version?
- "Not covered" how: no cases, no grader, or no volume?
- Did a scoring rule drop rows that still belong in the FM count?
- Who acts?
- How would this be detected next time without a person reading the row? (Step 6 of the loop must answer this.)

A finding is a draft. It does not authorize a paid run, a production change, or a message to an owner.
