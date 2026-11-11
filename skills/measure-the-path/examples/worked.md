# Example: parallel retrieval (synthetic)

Observation window: 0–10 seconds. Retrieval A runs 1–6, retrieval B 2–8, answer generation 8–10.

Summed work is 13 seconds, but user-visible time is 10 seconds. Span coverage is 9 seconds, with a 1-second unexplained gap at the beginning. Faster retrieval A alone may save nothing because retrieval B gates answer generation.

The supplied `spans.json` represents this example. Run the calculator and compare its output with these values. Actual optimization needs dependency data and repeated before/after runs.
