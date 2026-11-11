# Example: a corrected retry rule (synthetic)

The owner corrects "retry should resend immediately" to "queue once, and never send from the preview."

Before any further edit, a ledger line is appended: the date, the topic `digest-retry`, the decision in one sentence, and the source "owner correction." The older resend line stays in place and is marked superseded by the new line.

The next session searches that ledger, finds both lines, and does not revive the resend plan. A reply that only repeated the correction in chat, with nothing appended, would have failed this skill.
