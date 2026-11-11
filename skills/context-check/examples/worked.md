# Example: decision record (synthetic)

```text
## Decision record — digest retry
- Chosen: queue at most one retry; never send from the preview
- Supported by: request text; handler at handler.ts:80 at synthetic SHA abc1234; fixture 202 and 409
- Uncertain: vendor daily cap
- Supersedes: earlier note that a retry should immediately resend
- Proof plan: a duplicate click returns 409 and leaves state unchanged
- Passed: fixtures on synthetic tip bbb2222
- Unproven: vendor cap
```

A reading of only the superseded "just resend" note would be the wrong history. The replacing decision has to come back with it. The SHA and the handler path are invented teaching labels, not a reviewed repository tip.
