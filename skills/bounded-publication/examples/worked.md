# Example: two daily boards (synthetic)

Snapshot captured at 09:00 covers yesterday's events. The weekly board writes successfully and passes readback; the day board conflicts because someone added notes at 09:02.

Correct result: weekly board published, day board pending conflict, original day board preserved. Do not claim “both synced” or retry the whole pair. Fetch the day board again, preserve the human notes, and prepare a new targeted update only if still authorized.

At 09:10, new activity arrives. It belongs in a newer-activity section or a later reviewed snapshot, not silently inside the 09:00 receipt.

An older line that said "retry should resend immediately" stays in the record, marked superseded by "queue once, never send from the preview." Deleting the old line would hide the replacement. The new line does not promote itself to production. Its evidence path and its falsifier still have to be retrieved with it. The resend wording here is synthetic teaching data.
