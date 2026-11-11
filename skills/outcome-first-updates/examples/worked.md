# Example: review request (synthetic)

Weak: “We made great progress across several parallel agents and all the checks look good.”

Useful draft, unsent: “Could you review the repeated-import fix? The new head passes parser and database retry tests, including two concurrent runs. The live connector path is not tested. I need a review focused on identity changes, and a note if cancellation cleanup looks wrong. Release ownership is still unassigned.”

Verified in that draft: the named local tests on that head. Unproven: the live connector. Not started: human approval, merge, deployment, and live use. A queued CI job would be reported as queued, not as green. A bot approval would not be reported as the human review.

For a completion update: “The concurrency regression now passes on revision demo-v4. The branch is pushed, but human review is pending; it has not been merged or deployed.”

The example describes message content, not authorization to send it. If the reviewer declines, the draft stays declined. It is not resent through another channel.
