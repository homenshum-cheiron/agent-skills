# Example: review request (synthetic)

Weak: “We made great progress across several parallel agents and all the checks look good.”

Useful draft, unsent: “Could you review the repeated-import fix? The new head passes parser and database retry tests, including two concurrent runs. The live connector path is not tested. I need a review focused on identity changes, and a note if cancellation cleanup looks wrong. Release ownership is still unassigned.”

Verified in that draft: the named local tests on that head. Unproven: the live connector. Not started: human approval, merge, deployment, and live use. A queued CI job would be reported as queued, not as green. A bot approval would not be reported as the human review.

For a completion update: “The concurrency regression now passes on revision demo-v4. The branch is pushed, but human review is pending; it has not been merged or deployed.”

## Stand-up thread reply (synthetic)

Peers in the thread wrote three short bullets each.

Weak: a twelve-line card that repeats yesterday's context, says "the triage budget is tuned", and reports "12 sources working".

Useful draft, unsent:
- Crawler test: 40 sources tried. 12 work end to end, 15 stop early, 13 fail. Next: fix the 13 failing ones, starting with sign-in pages.
- Cost: capped spending on the model calls that check whether a crawled page is relevant. Measured on one run only.
- Blocked: none.

Not verified in that draft: whether the cap holds across more runs. The reader already knew the test goal, so it is not repeated.

The example describes message content, not authorization to send it. If the reviewer declines, the draft stays declined. It is not resent through another channel.
