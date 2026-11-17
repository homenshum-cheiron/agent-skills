# Worked example (synthetic)

Pipeline: a support-ticket agent with three layers. Revision `abc1234` (synthetic).

| Depends on | Layer | What it does | How to build the test case and key | Parallel pattern | Runs as | Original stage | Status |
|---|---|---|---|---|---|---|---|
| none | L1 Intake | The agent calls `classify_ticket(text) -> {product, urgency}`, which tags the ticket. It checks the intake checklist (product known, urgency set) and stops when both are set or after 2 tries, then asks a person. Contexts: 1 the fixed product list, 2 the ticket text. Verdict: sufficient, `intake.py:41`. | Freeze the raw ticket. Key: product and urgency, written by a support lead, stored offline. Pass: exact match on both fields; time and cost per case recorded. | none | one agent | "triage" | code fact |
| L1 | L2 Lookup | The agent calls `search_kb(product, query) -> [article_id]`. It fans out one worker per product area when the ticket names more than one, then merges. Stops at 5 articles or budget. Verdict: insufficient for real use because empty results are saved as "no answer", `lookup.py:88`. | Freeze L1 output from a past trace. Key: the article ids a lead would cite. Pass: recall at 5 of at least 0.8. | fan-out per area | worker pool | "search" | proposed fix |
| L2 | L3 Reply | The agent drafts a reply citing L2 articles. Self-judge: every claim cites an article; a conditional edge sends it back to L2 once, then to a person. | Freeze L2 articles. Key: required facts. Pass: judge-scored support, invalid output fails. | none | one agent | "answer" | open |
