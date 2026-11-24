---
name: principle-best-model-on-the-hardest-part
description: "Apply when a run is about to start in a deep block, or when the strongest model tier is being spent on side work. In a deep block only the active phase gets the top tier."
disable-model-invocation: true
---

# Best Model on the Hardest Part

The best hours and the strongest model both belong to the hardest part of the active phase. Side jobs are capped at a middle tier while a block runs. Outside a block, the top tier needs a phase tag. This rule is this collection's own. It has no research source.

**Pattern:**
- Map your own models to three tiers: top, mid and cheap. Do not name models in the rule; names go stale.
- In a deep block, the active phase may use top. Everything else is capped at mid.
- Do not starve the active phase: a cheap run on it in a block is also a failure.
- Log each decision, so the weekly review can see where the top tier went.

**Check:** `tier_route.py` and `model_tier` in **focus-routines**.
