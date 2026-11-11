# Verification scope

The included checks can establish local package consistency and helper behavior. They cannot establish that any model will follow every instruction, that an external service works, or that a product is ready to release.

## Reproduce

```sh
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 skills/proof-before-review/scripts/check_packet.py skills/proof-before-review/examples/packet.json
python3 skills/proof-before-review/scripts/score_coverage.py skills/proof-before-review/examples/coverage.json
python3 skills/measure-the-path/scripts/summarize_intervals.py skills/measure-the-path/examples/spans.json
python3 skills/walk-the-document/scripts/docwalk.py outline skills/walk-the-document/examples/sample-guideline.md --depth 2
```

The packet command checks a deliberately synthetic local example. The coverage command checks mark arithmetic for another synthetic example. Neither is evidence for a real pull request. Exit 0 from the coverage scorer means the nine marks are well formed. It does not mean every prompt was supported.

## What the checks cover

- Frontmatter names and required descriptions; bounded entrypoint size; every skill has a worked example.
- The root README links to every skill entrypoint.
- Local Markdown link existence, in-folder skill links, and no symlinks.
- Proof packet malformed inputs, revision drift, missing/changed evidence, failed/not-run/blocked checks, and pass bookkeeping.
- Coverage marks: unknown or duplicate prompts, N/A without a rationale, a claimed report that does not match supported/applicable, and the fixture's 6/7 result.
- Interval overlap, nesting, gaps, invalid numbers, and a specified observation window.
- Document reader: section nesting, exact offsets for find and read, budget cuts with a continuing cursor, page and line ranges, files without headings, non-ASCII text, and refused requests.

## What remains human or runtime work

- Whether a scenario matches the user's actual goal and the expected output is independent.
- Whether a test is meaningful, a receipt is authentic, a coverage rationale is true, or declared check coverage is complete.
- Whether a handoff has stopped the old writer; a JSON field is not a lock.
- Whether reading a document by place improves answers or cost on real long documents; no benchmark result is included.
- Whether a method match improves a real task. `match-methods` ships no runner and no score. Publishing it is not a product improvement.
- Actual host installation/discovery, model behavior, live provider compatibility, authorization, and spending controls.
- Confidentiality and legal review. The publication scan flags common patterns but is not a complete secret or privacy audit.

A successful local check is necessary evidence for its own narrow claim, not permission to publish or merge.
