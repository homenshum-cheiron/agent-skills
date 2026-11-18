# BLUF page template

```markdown
> **What this is.** <2-4 sentences: the page, its source and date, the one question it answers.>

### Top takeaways
1. **<Owner>** should <action>, because <reason with impact>. ([Card A](#card-a))

### Cards
#### <a id="card-a"></a>A. <Insight in plain words>
- **Owner:** <name> (<why>)
- **Situation:** <background a newcomer needs>
- **Scenario:** <one concrete case>
- **Bottom line:** <one sentence: what to do or believe>
- **Why it matters:** <dollars, hours or risk, with the number already computed when the data exists, or "impact unknown">
- **Evidence:** <source 1>; <source 2>
- **Next step:** <who, what, by when; "now" if it can start today>
- **Confidence:** <verified | inference | unverified>, <why>

### Findings (when a card exposes a problem)
- **Before:** <today's state at a named commit, with links>
  - **GAP:** <what is missing or broken, and the root cause if known>
    - **FIX PLAN:** <owner, steps, and the proof test that shows it worked>
- **After:** <proposed or target state; not proven until a rerun>

When findings span several owners or a system design, put the detail in one self-contained artifact (see [findings, artifacts and evidence](findings-artifacts-evidence.md)) and keep this page's post short, with a link to it.

### Glossary
- **<Term>:** <one plain sentence>
- First mentions: <Acme Robotics (company)>; <Jordan Lee (Staff Engineer), or "(role unverified)">

<details><summary>Appendix: raw notes</summary>

<unchanged original notes>
</details>
```
