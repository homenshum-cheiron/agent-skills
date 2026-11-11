# Example: parallel retrieval (synthetic)

Observation window: 0–10 seconds. Retrieval A runs 1–6, retrieval B 2–8, answer generation 8–10.

Summed work is 13 seconds, but user-visible time is 10 seconds. Span coverage is 9 seconds, with a 1-second unexplained gap at the beginning. Faster retrieval A alone may save nothing because retrieval B gates answer generation.

The supplied `spans.json` represents this example. Run the calculator and compare its output with these values. The calculator does not produce the hypothetical table below.

Hypothetical phase table, synthetic teaching numbers, not a run of this repository and not calculator output: prep is 1.8 s, of which 0.6 s and 0.4 s are spanned and 0.8 s is an unspanned gap. The model call is 2.1 s to first output and 3.4 s to completion. User-perceived time is 5.6 s, leaving a further 0.4 s unexplained. No accuracy figure is attached, so these numbers do not support a quality-neutral speed claim. Cost in the story is included allocation from a usage page, not a list-price bill. No optimization is proposed until the same two scenarios exist as a before table and an after table.
