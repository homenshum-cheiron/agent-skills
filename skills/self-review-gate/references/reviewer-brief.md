# Reviewer brief

Send this to a different model or a fresh agent that never saw your session. Attach the diff, the frozen tip, the one-line intent, and the recorded check output. Do not attach your reasoning or your chat.

> Job: Try to break this change. The intent is: INTENT. The tip is TIP.
>
> Why: The author wants to act without a human approver. Your review is the only second look this change gets, so be skeptical. Authors grade their own work generously.
>
> Guardrails: Read only, because you are reviewing, not fixing. Keep any repro in a scratch folder, because the author's tree must stay as frozen. Leave out style, naming, and hypothetical future risks, because only findings you ran can block.
>
> Done means: For each finding, give a title, the exact command, the output it printed, and the output the intent requires. Say "no verified findings" when none survive. Name the tip you reviewed. End with one line reading only BLOCK or PASS.

Record the reviewer's raw output to a file and point `review.evidence` at it. If the reviewer cannot run code, mark `kind` as `fresh-context` and treat each finding without a run as a question to answer with your own run, not as a pass.
