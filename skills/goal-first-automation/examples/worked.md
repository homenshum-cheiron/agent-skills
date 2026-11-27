# Example: freelance invoice follow-up (synthetic)

Invented teaching data, not a live client or inbox. The question is how to turn a messy process dump into a held plan, then a routine, without treating "I sent the reminder" as done.

## Goal

`goal := overdue invoices get a correct follow-up and the client knows the balance for this freelance billing work`

Name: invoice-nudge. Serves cost (fewer uncollected hours, less rework). The user said the goal was right after one clarifying question: "Do you want money in the account, or a correct shared record plus a client confirmation?" They chose the second.

## Process dump (left messy, then restated)

Collected from a voice dump: steps (export unpaid rows, write a reminder, mark the row), watch_outs (do not nudge a client who already paid), tools (email and the invoicing app), check_work ("I sent it"), info_from (email and the invoicing app), feedback_from (client replies and a occasional one-star review).

Three examples walked, including a failure: a client emailed "paid yesterday" while the invoicing app still showed unpaid; a second reminder went out the same day.

Restatement, held before any send or routine save: "Once a week, I will look at invoices older than seven days. If email and the app disagree, email wins. I will update the app, write the reminder, and I am done only when the invoice row is correct and the client has a confirmation. I will not open a second follow-up while one is waiting."

## Rules that were missing from the dump

- Source conflict: email versus the invoicing app. Email wins. The app is updated before any reminder.
- Done: saved (the invoice row is present and correct) and confirmed (the client received the statement). "Sent" is not done.
- Waiting: one in-flight reminder per invoice ID. Resume when the client replies or seven days pass. Never create a duplicate.

## Feedback loop

A complaint arrived on the same invoice ID (`INV-104`). That day's records were pulled by invoice ID. The gap: the reminder was sent, but the app still showed the old balance, so the client's confirmation did not match the record.

If those day records had been missing, the next step would have been a small log (invoice ID, source used, saved at, confirmed at), not more reminders.

## Routine and return

Proposed trigger: a weekday morning schedule, plus an email trigger on client replies that mention an invoice ID. Not saved in this example.

Return:

- goal: overdue invoices have a correct record and a client confirmation
- process: weekly unpaid sweep, email wins on conflict, one in-flight reminder per invoice
- rules: source = email over app; done = saved + confirmed; wait without duplicates
- routine: proposed, not saved
- next_step: wait for the user to accept the restatement, then save the log and the routine
