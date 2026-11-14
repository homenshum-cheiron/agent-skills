# Premise check

Run this before any recommendation: a finding, a research item, a decision, or a cross-comparison. It takes a few lines and it catches the case where an option is cheap only because it moves risk somewhere you did not look.

| Part | Question | Write down |
|---|---|---|
| 1. Volume | How much of this work actually happens? | A count in the project's own units (requests, screens, documents, runs) per year, with a source. |
| 2. Money | What does it save or cost per year? | The difference against the trusted baseline, with the arithmetic. |
| 3. Risk direction | Where does the benefit come from? | Which behaviour produces the saving, and whether that is the safe or the risky direction. |
| 4. Harm or gain | What does it do in real units? | The expected number of extra errors, misses, hours, or incidents per year, with the arithmetic. |

Label every input **OBS** (observed at a source you opened), **DER** (computed from labelled inputs, arithmetic shown) or **EST** (a judgement, said to be one). Never present an estimate as observed. Unknown is not zero.

Verdict: keep, downgrade, or drop. Downgrade or drop when the saving is small next to the harm, when the saving exists only in the risky direction, or when the arithmetic does not add up. Name the missing variables that could change the verdict: open pull requests, product direction, demand, headcount, compliance and validation.

## Illustrative example (synthetic numbers)

> At about 24,000 screens a year, the cheapest screener saves only about $130–370 a year over the incumbent model in the required region. It saves money only by clearing review flags, which is the risky direction. Missing just one extra percentage point of answers that need review means about 48 unflagged answers a year.

The arithmetic behind it: 24,000 screens × an estimated 20% that truly need review = 4,800 (DER from EST). One percentage point more misses = 48 a year (DER). The saving covers that only if each miss costs less than $370 ÷ 48 ≈ $8 (DER). Verdict: drop, and re-open only if the cheaper option matches the incumbent's recall on your own labelled cases, or volume grows by orders of magnitude.

The example is a teaching case. It is not a claim about any named model, provider, or deployment.
