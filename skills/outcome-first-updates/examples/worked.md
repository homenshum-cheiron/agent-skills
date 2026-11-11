# Example: review request (synthetic)

Weak: “We made great progress across several parallel agents and all the checks look good.”

Useful: “Could you review the repeated-import fix? The new head passes parser and database retry tests, including two concurrent runs. The live connector path is not tested. Please focus on identity changes and cancellation cleanup; release ownership is still unassigned.”

For a completion update: “The concurrency regression now passes on revision demo-v4. The branch is pushed, but human review is pending; it has not been merged.”

The example describes message content, not authorization to send it.
