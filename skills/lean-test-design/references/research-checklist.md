# Research checklist (per arm)

Fill one card per arm before any paid run. Time-box it. A card that settles the question ends the plan.

## Card header

- Arm: what differs from the reference, in one line.
- Pipeline version the arm applies to: commit, prompts, skills, tool set, model ID, grader.
- Date of the research, and who did it.

## Sources to check

| Kind | Where to look | What to extract |
|---|---|---|
| Official | Product or model page, model card, system card, release notes | Supported features, known limits, refusal behavior, lifecycle and retirement dates |
| Official | Migration guide and prompting guide for the candidate | Parameters that changed or were removed, prompt patterns the vendor recommends or warns against |
| Official | API reference and per-endpoint feature table | Which features exist on the exact endpoint and region you use |
| Field | Hacker News search, Reddit, community forums | Reports on tool use, prompt sensitivity, effort settings, regressions. Count independent reports. |
| Field | GitHub issues for the SDKs, gateways, and agent CLIs in use | Search the exact model or library ID with the error text, for example `"<id>" 400` |
| Papers | Studies of the same mechanism or the same harness and model pairing | Effect sizes, noise between reruns, ablations, negative results |
| History | Your own earlier runs, closed pull requests, traces | Was this tried? On which version? What happened? |

Label every claim: **official**, **paper**, **issue**, or **anecdote**, plus the count of independent reports. One anecdote counts only if it matches a mechanism in an official source.

## Non-model factor map

For each factor, write "held equal" or "varied on purpose", and how you checked.

| Factor | Why it matters | Cheap check |
|---|---|---|
| Prompt phrasing | Literal models apply qualitative bars ("only flag if…") strictly. "Minimize tool calls" can make a model answer from memory. | Read the prompt diff between arms |
| Tool-call format and tool descriptions | Schema shape, forced tool choice, and description wording change which tool is picked | Diff request builders and tool definitions |
| Skill text and loading | A skill that loads on one arm and not the other is a second change | Dry-run the loader and list loaded skills |
| Effort or thinking settings | Same model, different effort, different score and cost | Print resolved config |
| Caching and compaction | History edits can break cache prefixes and change cost and behavior | Replay a stored trace and read cache-hit counts |
| Stop rules, turn caps, retries, timeouts | A turn cap can look like a model failure | Count cap and timeout hits per arm in stored traces |
| Safety classifiers and silent fallback | A flagged request may be refused or rerouted to another model | Search stream logs for reroutes and refusals |
| Provider and region | Feature parity is not guaranteed across providers | Check the per-endpoint table; replay one case per provider |

## Model swaps

When the arm is a model swap, use the research-first ladder in the `match-methods` skill (its model-swap reference) for the hard gates, the candidate card, and the per-measure predictions. This checklist does not repeat them.
