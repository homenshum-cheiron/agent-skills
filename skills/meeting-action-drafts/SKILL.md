---
name: meeting-action-drafts
description: "Use when a meeting has ended and action items should become drafts: extract items from notes, cite the transcript, draft the work or a nudge, and send nothing."
---

# Meeting action drafts

The useful outcome of a meeting is not a longer summary. It is a short review queue: one draft per open item, ready to check, with nothing sent.

## When it runs

On a schedule, or right after a meeting ends, look only at notes that have not already been handled. If no meeting has ended since the last run, stay silent. Do not re-draft old meetings.

## For each new notes file

1. Read the notes and, when it exists, the matching raw transcript from a local copy you control.
2. Take every unchecked item (lines matching `* [ ]`). Record the owner mentions and the exact locator `{file, char_start, char_end}`.
3. Ground each item in nearby raw text (the line, plus a short retrieve of the matching transcript or thread). Do not invent owners, dates, or wording.
4. Write one draft per item:
   - If the item is yours, draft the work itself.
   - If it belongs to someone else, draft a short nudge the owner could send, and stop.
5. Mark each item as one of: drafted, needs a person, or not ours. An item with no state has failed the run.
6. After the drafts are saved, mark the notes file as handled so the next run skips it.

## Hard limits

- Drafts only. Nothing is posted, mailed, or sent in chat. A declined or blocked send is final.
- Cite the locator on every draft. A draft without a source is not done.
- Do not silently drop an item. If the notes are too thin to draft from, say so and leave the item as needs a person.
- The scheduled job should fail in a visible way if a source could not be read, not fail in the background.

A small offline extractor that follows this shape, over invented notes, lives in the context-walk repository as `action_items.py`. See the [worked example](examples/worked.md).
