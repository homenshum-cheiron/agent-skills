# Example: one paragraph split into a scan (synthetic)

Before: a single paragraph explaining that unmapped environment variables can break rendering mid-run and that a state listener would help.

After:

#### Critical initialization step

**Ensure environment variables are fully mapped before initialization begins.**

> Failing to map variables can break rich-text rendering and lose track of long responses mid-execution.

- **The risk:** Rich text fails, and the agent loses long responses mid-execution.
- **The fix:** Add a dedicated state listener on the execution-loop buffer.

The warning and the fix are easier to find. No new claim was added, and no emoji was required. A two-sentence chat reply would have been left as prose.
