# Example: coverage arithmetic for a typo fix (synthetic)

The change is a comment-only typo on a standalone branch. Head `ccc3333` is an invented label. The body has:

- Supported: plain summary, how it works (no flags; that absence is stated), a lint command with output pasted from that head, the changed line with its path, unproven risks (missed instances of the same typo), and stack position (standalone).
- Missing, and not N/A: live evidence. No trace, screenshot, or usage reading was attached, and the body gives no reason that would make the prompt non-applicable.
- N/A with reasons: flowchart, because there is no runtime path change; structured input/output, because there is no structured-data contract.

Answer key for `coverage.json`, checked by `score_coverage.py`: **6/7 applicable, plus 2 N/A with reasons.** The missing seventh applicable prompt is live evidence. Do not write "6/9 with two N/A," and do not write "9/9."

This score is coverage arithmetic for a fixture. It is not a certification that the typo fix is good, and the lint output is not included here because this file does not invent a command log.
