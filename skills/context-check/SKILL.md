---
name: context-check
description: "Use before consequential implementation, after a handoff or restart, when evidence contradicts the plan, and again before completion if acceptance may have moved. Produces a short five-check record, not a second research platform."
---

# Context check

A long chain of thought is not evidence that history was used correctly. Write five reviewable checks, and refresh them at event boundaries rather than on a timer.

1. **Purpose.** Who needs this, and what should become better? Evidence: the original request or the accepted criteria.
2. **Relevant history.** What was already decided, rejected, or replaced? Evidence: cited locations. If retrieval returns an older plan, it must also return the replacing decision, or the history is incomplete.
3. **Current implementation.** How does the work move through the actual system? Evidence: current code, schema, callers, and existing tests at a named revision.
4. **Failure and impact.** What could make the first explanation wrong? What else depends on this?
5. **Proof.** What observable result shows the change works?

These are not five compulsory tool calls. Use the smallest evidence that answers each check. One source may cover several checks. A one-line answer is enough for a small patch.

Refresh when a task starts; after compaction, handoff, or restart (reload the record and its sources; do not trust a summary alone); when evidence contradicts the plan; before a consequential action; and before completion. Between those boundaries, do not reread unchanged material. Keep source revisions with the record.

Never infer a binding decision from a similar-sounding chat. An agent suggestion stays a suggestion until it is accepted. If code disagrees with an approved requirement, report the mismatch. Do not treat the code as the intent. If a source is unavailable, mark the conclusion unverified.

Do not start a second graph service or a fleet of agents for this record. A tool log that says a file was opened is not understanding. The useful score is whether the right requirements were preserved.

Use [the worked example](examples/worked.md).
