# Verification scope

The included checks can establish local package consistency and helper behavior. They cannot establish that any model will follow every instruction, that an external service works, or that a product is ready to release.

## Reproduce

```sh
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/proof-before-review/scripts/check_packet.py skills/proof-before-review/examples/packet.json
python3 skills/measure-the-path/scripts/summarize_intervals.py skills/measure-the-path/examples/spans.json
```

The packet command checks a deliberately synthetic local example. It must not be represented as evidence for a real pull request.

## What the checks cover

- Frontmatter names and required descriptions; bounded entrypoint size; every skill has a worked example.
- Local Markdown link existence, in-folder skill links, and no symlinks.
- Proof packet malformed inputs, revision drift, missing/changed evidence, failed/not-run/blocked checks, and pass bookkeeping.
- Interval overlap, nesting, gaps, invalid numbers, and a specified observation window.

## What remains human or runtime work

- Whether a scenario matches the user's actual goal and the expected output is independent.
- Whether a test is meaningful, a receipt is authentic, or declared check coverage is complete.
- Whether a handoff has stopped the old writer; a JSON field is not a lock.
- Actual host installation/discovery, model behavior, live provider compatibility, authorization, and spending controls.
- Confidentiality and legal review. The publication scan flags common patterns but is not a complete secret or privacy audit.

A successful local check is necessary evidence for its own narrow claim, not permission to publish or merge.
