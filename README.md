# Agent skills

Small, portable habits for getting useful work **finished and proved**.

This is Homen Shum's collection of working methods for coding agents: start with a real scenario, make ownership explicit, test the actual change, measure rather than guess, and report the outcome. It captures the decisions behind a multi-agent setup without requiring a particular model, host, vendor, or private infrastructure.

## Start with the problem

| When the work gets stuck | Use |
|---|---|
| The plan is a list of components, not an outcome | [Scenario first](skills/scenario-first/SKILL.md) |
| A PR looks plausible, but nobody ran the relevant tests | [Proof before review](skills/proof-before-review/SKILL.md) |
| Several agents might write the same branch | [One-writer handoff](skills/one-writer-handoff/SKILL.md) |
| A cheaper model or tool looks promising | [Criteria before choice](skills/criteria-before-choice/SKILL.md) |
| A request is slow or expensive | [Measure the path](skills/measure-the-path/SKILL.md) |
| The tool list and context keep growing | [Lean tool context](skills/lean-tool-context/SKILL.md) |
| Runtime failures are mixed with agent reasoning failures | [Route failures](skills/route-failures/SKILL.md) |
| Planner/worker routing costs more than expected | [Budget-aware routing](skills/budget-aware-routing/SKILL.md) |
| A recap could overwrite a newer result | [Bounded publication](skills/bounded-publication/SKILL.md) |
| An update says lots of activity but no outcome | [Outcome-first updates](skills/outcome-first-updates/SKILL.md) |
| Search found the document but not the deciding passage | [Walk the document](skills/walk-the-document/SKILL.md) |

Each folder is self-contained. Read its `SKILL.md`, then only the linked examples or references relevant to the task. The examples are synthetic, not disclosures of private projects.

## Try one skill

1. Inspect the skill and its scripts.
2. Copy **one complete folder** from `skills/` into the skill directory supported by your agent host, or give the agent its local `SKILL.md` path. Directory discovery differs by host; this repository does not configure it.
3. Try the example request. Check the result, not whether the agent recited the instructions.
4. Adapt the practice to the repository's real commands, risks, and permissions.

For example: “Use `proof-before-review` to review this diff. Run the relevant tests and separate passed, failed, blocked, and not-run checks.”

These skills do not grant permission to publish, spend, modify production, or send messages. They supplement the user's current request and the host's permissions. They are guidance, not a universal guard or a new CI gate for another project.

## What is implemented here

- Eleven written workflows, each with a worked example.
- An offline proof-packet checker that verifies declared check status, revision, and local evidence hashes. It does **not** independently judge the evidence.
- An interval calculator that separates summed work from wall-clock coverage.
- An offline document reader that outlines one local text file, finds exact strings, and reads sections, pages, lines or character ranges with exact offsets. It does **not** rank, embed, call a model, or convert PDF or HTML.
- Repository checks for package structure and local links, plus unit tests.

**Not implemented:** a live orchestration service, a model router, spend enforcement, distributed locking, a production monitor, or an auto-fix agent. An example handoff or incident record does not create those systems.

Run the local checks with Python 3.10+ and no third-party dependencies:

```sh
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
```

See [verification scope](docs/verification.md), [the decisions](docs/decisions.md), and [the contributor guide](CONTRIBUTING.md).

## Relationship to the setup kit

The [host setup kit](https://github.com/HomenShum/codex-claude-cursor-setup) covers installation and host configuration. This repository is the method layer: reusable, selectively loaded workflows. It does not copy private bootstrap code or replace host configuration.

## Inspiration and license

[Benji Taylor's skills repository](https://github.com/benjitaylor/skills) demonstrates a valuable shape: a skill can ship references, examples, tools, and a verification loop together. This collection applies that packaging idea to engineering and coordination. It contains original writing and code, not copied Stageshow code or assets.

Original content is [MIT licensed](LICENSE). External projects retain their own licenses and trademarks.
