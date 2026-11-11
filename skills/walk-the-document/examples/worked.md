# Example: one table row under the wrong heading (synthetic)

Question: "We want to widen an approved specification limit. What category is that, and what do we file?"

The document is [a synthetic guideline](sample-guideline.md). It is invented and names no real authority. The numbers below are the helper's output on that file.

## Without the walk

A fragment search for "widen specification limit category" returns the lead-in of section 2.2 "Moderate changes" and the definitions. A reader who trusts the heading answers "moderate, file a notification". That is wrong.

## With the walk

1. Outline, depth 3: ten sections, about 361 estimated tokens in all. Section `1.2` "2 Change categories" spans lines 10 to 35.
2. Find the exact phrase `specification limit`, ignoring case: 3 hits. Lines 26 and 28 are in section `1.2.2` "2.2 Moderate changes"; line 50 is in "4 Definitions".
3. Read section `1.2.2` whole: characters 492 to 840, about 87 estimated tokens. The table row at line 28 reads `B.4.c | Widening of an approved specification limit | Major`. The row contradicts its heading.
4. Widen on that evidence. Find `B.4.c`: a second hit at line 34 in section `1.2.3` "2.3 Major changes". Read it: the text states that row B.4.c is a major change and that the holder must wait for approval.
5. Follow the consequence. Read section `1.3.2` "3.2 For prior approval": characters 1245 to 1364.
6. Stop. The answer names its category, its condition and its filing list.

Answer, with the spans it rests on:

- Category: major (line 28, characters 778 to 783 for the code; confirmed at line 34, section "2.3 Major changes").
- File: a comparison of old and new limits, batch data for three batches, and a justification (section "3.2 For prior approval", characters 1245 to 1364).

Three reads, about 171 estimated tokens of document text, out of about 361. On a document this small, reading everything is cheaper and just as good. The walk pays when the document is many times larger than the budget for one read.

## What the example does not show

- It is one invented document with one planted trap. It is not a measurement of accuracy or cost.
- The reader still had to notice that the row and the heading disagree. The helper only made both visible with their place.
