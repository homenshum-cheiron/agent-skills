# Worked example (synthetic): one weekly review

A developer runs two coding-agent hosts. Each host loads a standing instruction file and shares a skills folder.

## Stage 1 report (excerpt)

- Host B instruction file: 39,000 bytes against a 32,768-byte loader limit. The last 6,232 bytes are not loaded. They include the research-claims rule.
- Conflict, topic "effort": host A line 22 says "workers at max"; host A line 9 (newer, dated) says "effort never above high".
- Conflict, topic "model": a shared rule file says "model X banned"; two other files say "model X allowed" with a later date.
- Superseded: "Decision needed: cloud agents?" dated three weeks ago; a later dated line records the decision.
- Launcher mismatch: host B tells gate work to "print ESCALATE and stop", but the last 20 launches were plain CLI calls with no wrapper.
- Never loaded in 30 days: 9 of 41 skills, including `fresh-review`.

## Stage 2 decisions

- Host B file: move three long reference sections verbatim to an archive with pointers (binding by reference). Result: 29,600 bytes.
- "workers at max": retire, superseded by the dated effort ceiling.
- "model X banned": retire; the later decision wins.
- "Decision needed": retire with the decision date.
- Escalate rule: rewrite as "under a plain launcher, finish at the given effort or report the blocker".
- The shared rule file belongs to another team: proposed patch only.

## Underuse

- `fresh-review` loaded 1 time in 30 days. Misses: a design review where the reviewer had read the whole build chat; a research summary shipped with two unverified claims.
- Trigger rule: when a deep-research report or decision document is marked final, start a fresh-context reviewer that reads only the document and its sources.
- Next week's check: count `fresh-review` loads and list each research report finished without one.
