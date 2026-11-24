# State files and settings

All state is plain JSON in one folder: `FOCUS_DIR`, default `~/.focus`. One routine writes each file. The checks only read.

| File | Written by | Shape |
|---|---|---|
| `phases.json` | phase pick, residual snapshot | `[{id, title, status: active/queued/closed, exit_criteria: [text], exit_met: [true/false], est_min, actual_min, next_step: {when, action}, updated}]` |
| `today.json` | phase pick | `{date: YYYY-MM-DD, phase_id, done_picture, first_step: {when, where, action}}` |
| `critic.json` | priority critic | `{ts, sources_read: [{kind, ref}], ranking: [{id, bigger_picture, block, evidence: [text]}]}` |
| `parking.jsonl` | say-no gate | one row per ask: `{ts, ask, source, verdict: in_phase/batch/park/no, urgent: true/false, surfaced_during_block: true/false}` |
| `switches.jsonl` | switch counter | `{ts, active_threads: [text]}` |
| `models.jsonl` | your router, or `tier_route.py` | `{ts, phase_id, tier: top/mid/cheap, in_block: true/false}` |
| `design-ledger.jsonl` | the owner, by hand | `{ref, created}` for a design kept outside the repository |

Times are ISO 8601 with a zone offset. A `.jsonl` file holds one JSON object per line and is only appended to.

If the state is copied from another machine, treat the copy as read-only and say which side is the source of truth. A stale `today.json` (its `date` is not today) counts as no phase picked.

## Settings

| Variable | Meaning | Default |
|---|---|---|
| `FOCUS_DIR` | state folder | `~/.focus` |
| `FOCUS_BLOCKS` | deep blocks, clock time, start included, end excluded | `09:30-11:30,14:00-16:00` (an example) |
| `FOCUS_TZ` | zone for the blocks and for "today" | the system zone |
| `FOCUS_SWITCH_CAP` | active threads allowed outside a block | `3` (in a block: 1) |
| `FOCUS_CRITIC_KINDS` | source kinds the critic must read | `messages,reviews,calendar,state` |
| `FOCUS_PHASE` | phase tag for `tier_route.py` when `--phase` is not given | none |
| `FOCUS_NOW` | fixed clock for tests | the real clock |
| `DESIGN_LEDGER` | ledger file for the design gate | `<FOCUS_DIR>/design-ledger.jsonl` |
| `DESIGN_MIN_LINES` | non-blank lines a design file needs | `3` |
| `DESIGN_EXEMPT_LINES` | largest change the exempt line covers | `30` |

Deep blocks apply Monday to Friday.

## Verdicts and exit codes

| Script | 0 | 1 | 2 | 64 |
|---|---|---|---|---|
| `focus_check.py` | every check passed | a check failed | nothing failed, but a check is unverified or inconclusive | usage error |
| `design_gate.py` | passed | failed | inconclusive (git or the body is unreadable) | usage error |
| `tier_route.py` | decision printed (read `tier` and `capped`) | | | |

A log check decides "in a block" from the row's time. The `in_block` flag in a row is used only when the row has no time.
