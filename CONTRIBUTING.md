# Contributing

Start with one concrete failure or costly ambiguity. Explain the decision the skill should change, give a small input/output example, and remove advice that an ordinary competent agent already knows.

A skill needs a `SKILL.md` with `name` and `description` frontmatter. Add a reference or script only when it helps the actual task. Keep linked resources inside the skill folder so a single folder can be copied safely.

For changes to scripts, add a regression test that would fail under the old behavior. Test negative and inconclusive outcomes as well as success. Never call a fixture result a live integration result.

Before publication:

- Run the README checks on the final files.
- Inspect every changed file for private material and licensing issues. Pattern checks are only a supplement.
- Review examples without the author's intended answer when practical.
- State untested hosts, unavailable dependencies, and pending human decisions.

Do not commit execution logs from real tasks. Use synthetic evidence under examples instead.
