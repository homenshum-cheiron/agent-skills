# Example: a corrected retry rule (synthetic)

The owner corrects "retry should resend immediately" to "queue once, and never send from the preview."

Before any further edit, a ledger line is appended. It cites the evidence and links to the line it replaces. The older resend line stays in place:

```
2026-03-28  id: digest-retry-resend
  retry should resend immediately
  sources: earlier draft R4 (untrusted)

2026-04-02  id: digest-retry
  queue once, and never send from the preview
  sources: owner correction R12 (trusted)
  supersedes: digest-retry-resend
```

The next session searches that ledger. A hit on `digest-retry-resend` is not the answer: the read follows `supersedes` to `digest-retry`, then reads R12, and only then answers. The March line is shown as history after the current rule. A reply that only repeated the correction in chat, or that answered from the first hit without following the link or reading the cited evidence, would have failed this skill.
