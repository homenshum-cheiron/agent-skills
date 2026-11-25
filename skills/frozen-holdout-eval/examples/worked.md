# Worked example (invented)

A retriever is being changed to favour a speaker's own turns when the question is "what did Alice say".

Before touching the ranker, eight new questions are written from the raw transcript, each with a gold substring, and the file is hashed. The baseline is scored on that file and on two earlier frozen sets.

After the change:

| Set | Baseline | Candidate |
|---|---|---|
| Original 12 | 8 / 12 | 10 / 12 |
| Holdout 1 (already frozen) | 3 / 8 | 3 / 8 |
| Holdout 2 (frozen this round) | 2 / 8 | 5 / 8 |

The candidate is kept because no earlier set fell. One of the three remaining misses is an English question about a Hangul turn; that is recorded as a miss, and the gold substring is not edited to make the run look better. The next holdout will be written before any Hangul-specific change.
