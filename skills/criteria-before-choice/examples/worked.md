# Example: choosing an extraction tool (synthetic)

Need: extract table rows locally, preserve cell coordinates, and run without sending documents to a service.

| Candidate | Local processing | Coordinates | Result |
|---|---|---|---|
| Library A | Pass: inspected local API | Unverified | Run one rotated-table fixture |
| Hosted B | Fail: requires upload | Pass: vendor claim | Eliminated for this task |
| Library C | Pass: inspected local API | Fail: returns text only | Eliminated |

Library A is the only candidate left to test, not yet the winner. The decisive fixture should include merged cells and a rotated page. Record expected rows before running it.
