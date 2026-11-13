# Research-first model swap (reference)

Use this reference when a failure, a slower score, or a new release is about to be met with a model swap. It extends the [parent skill](../SKILL.md): start from the outcome and the evidence already in hand, include "no change" as a candidate, and climb a cheap ladder before any full eval.

A model's score depends on more than its weights: prompts, tool schemas and descriptions, skill loading, effort and thinking settings, caching, stop rules, refusal classifiers, provider, and region. A harness tuned on one model can hurt another. A $0 check often removes a candidate first. Work down this ladder and stop as soon as one rung settles the question.

## 0. Hard gates ($0). Stop at the first "no."

- **Availability.** Is the model offered in every region and on the exact endpoint the workload needs?
- **API contract.** Diff request builders against the candidate's migration guide: thinking or effort, tool choice (some models reject a forced choice), temperature, structured outputs, token limits, endpoint shape. A mismatch is a code fix, not an eval question.
- **Safety classifiers.** Check for domain classifiers that can refuse legitimate work, and whether refusals are billed. Remove prompt lines that ask the model to write out hidden reasoning if that trips a classifier.
- **Price and lifecycle.** Legacy status, retirement date, introductory pricing.

## 1. Desk research (time-box; fill a candidate card)

Label every claim official, paper, issue, or anecdote, and note how many independent reports support it.

- Official: model page, migration guide, prompting guide, system or model card, per-endpoint feature table.
- Field: public forums and GitHub issues for the SDKs, gateways, and agent CLIs you use (search the model id plus `400`).
- Papers: model-by-harness studies since the last check.
- A single anecdote counts only if it matches a mechanism in an official source.

## 2. Predict, per measure, before you test ($0)

For each graded measure, write the expected direction, the mechanism, your confidence, and which existing labeled cases should show it. Record predictions before running anything; afterwards score them hit or miss.

## 3. Cheapest discriminating test, cheapest rung first

| Rung | Test | Typical cost |
|---|---|---|
| 3a | Static audit of prompts, skills, tool descriptions, and request builders against the candidate card | $0 |
| 3b | Mine existing traces: stop reasons, token-limit hits, refusals, tool-call errors, cache-hit rate, thinking tokens | $0 |
| 3c | Token-count real prompts and documents with the candidate tokenizer | about $0 |
| 3d | Single-step replay of recorded decision points | small; needs approval |
| 3e | Targeted cases the predictions point at, plus a few controls, with a few repeats | small API spend or subscription usage |
| 3f | Effort sweep on those targeted cases | same as 3e per level |

Replay holds the conversation prefix fixed: use it for local decisions, not long-run robustness. Repeats also measure rerun noise for any later full eval.

## 4. Full eval, only when all three hold

- Rungs 0–3 did not settle the question.
- You can write the decision value: a gap of at least X points changes the choice, and that is worth a stated amount per year.
- The eval is sized for adequate power on gap X using measured rerun noise. Published work has found that a modest task set detects a mid-size gap only about half the time, and that a rerun can flip a non-trivial share of tasks.

Paid per-token runs need explicit owner approval. A plan, a matrix, or a CLI flag is not that approval. Subscription-included agent-CLI arms are still not a license to start a new billed API eval.

## 5. After a swap

Prefer a shadow or canary where you can. Re-stamp the component list. A small fixed canary catches provider-side drift later.

## Traps that look like a model problem

- Silent model fallback in an agent CLI after a classifier flag. Read stream logs for reroutes before trusting a "bare" score.
- A text end-of-turn that is a progress report, not a finish.
- Compaction or history edits that break cache or thinking-block prefixes.
- Verify instructions that make a self-verifying model verify twice.
- "Minimize tool calls" wording that makes a model answer from memory.
- Stale-state readers: flat lookups on nested data, or fields the new model no longer emits.

## Coverage and second question

Never compare a bare score on one model with a harness score on another. When an arm is missing, say so, and say which rung would fill it most cheaply.

If research says change something, ask what evidence supports it, cheaper than what, and what it could break on models still in use. If it says change nothing, ask what that conclusion cannot see.

## Sources (public)

- Wu et al., JoMoHa, arXiv 2611.11499: a harness can lower success versus the same model run bare; a stale lookup can turn a short success into a timeout.
- "What Does a Harness Buy? Tokens, Mostly," arXiv 2610.04433: reruns flip a non-trivial share of tasks; small evals are underpowered for mid-size gaps.
- "Finding the Right Fit," arXiv 2610.00917: model rankings can reverse across harnesses.
- The candidate's official prompting guides, migration notes, and refusal or fallback docs.
