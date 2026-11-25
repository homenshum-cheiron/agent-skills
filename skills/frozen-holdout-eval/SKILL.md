---
name: frozen-holdout-eval
description: "Use when iterating a retriever, prompt, or pipeline against questions: freeze holdout cases from raw sources before changing code, compare a baseline to the candidate, and adopt only changes that do not regress earlier sets."
---

# Frozen holdout eval

A change that is tuned on the same questions it is graded on will look better than it is. Write the next test set from the raw sources first, freeze it, then change the code.

## Loop

1. **Look up, then write cases.** Open the raw notes, transcripts, or documents. Write each question with a gold locator or a gold substring taken from that text. Do not write cases from memory, from a summary, or from what you expect the code to do.
2. **Freeze before any edit.** Hash the case file. After this point the cases do not move, even if a later run is disappointing.
3. **Score two systems.** Run a frozen baseline and the current candidate on every earlier set and on the new holdout. Report each set separately. Do not pool them into one score.
4. **Adopt or drop.** Keep a change only when it does not regress a previous set, or when you can name the loss and accept it. If the candidate lost a baseline strength, merge that strength in and re-score.
5. **Stop.** Stop when a new holdout no longer improves, or when the remaining misses need a different kind of evidence (for example a per-speaker gist, not another keyword tweak).

A case that cannot be traced to a raw span is not a case. A holdout written after seeing the candidate's errors is not a holdout.

## What to record

For each round: the case-file hash, the code revision, each set's score with a denominator, and a short cause for every miss. A miss is a fact about that question, not a reason to edit the question.

The context-walk repository uses this loop on a tiny invented corpus (`examples/synthetic-corpus/eval/cases.jsonl`) and documents the method in `docs/hybrid-retrieval.md`. Private scores stay private.

See the [worked example](examples/worked.md).
