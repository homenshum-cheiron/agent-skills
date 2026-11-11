# Example: choosing an extraction tool (synthetic)

Need: extract table rows locally, preserve cell coordinates, and run without sending documents to a service.

| Candidate | Local processing | Coordinates | Result |
|---|---|---|---|
| Library A | Pass: inspected local API | Unverified | Run one rotated-table fixture |
| Hosted B | Fail: requires upload | Pass: vendor claim | Eliminated for this task |
| Library C | Pass: inspected local API | Fail: returns text only | Eliminated |

Library A is the only candidate left to test, not yet the winner. The decisive fixture should include merged cells and a rotated page. Record expected rows before running it. One passing fixture would show that the local API can read that page. It would not crown a general winner.

Public documentation already eliminated Hosted B on the upload constraint, so no paid bake-off is opened to re-check that failure. If a later pilot compared libraries on mismatched builds, every arm in that pilot would be discarded.
