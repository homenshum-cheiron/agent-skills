---
name: principle-fixed-times-for-messages
description: "Apply when messages, pings or review requests keep arriving during focused work. Decide once when messages get read, instead of deciding again on every ping."
disable-model-invocation: true
---

# Fixed Times for Messages

Each ping is a small decision: read now or later. Making that decision once, ahead of time, removes all of the small ones.

**Pattern:**
- Pick fixed message times outside the deep blocks.
- Decide ahead of time what counts as urgent, for example an outage or a deadline under four hours. Only that breaks a block.
- Everything else waits for the next batch.

**Check:** `no_interrupt` in **focus-routines**.
