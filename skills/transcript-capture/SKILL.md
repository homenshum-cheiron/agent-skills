---
name: transcript-capture
description: "Use when meeting notes or transcripts would otherwise live only in a chat app or a host that deletes them: keep an append-only local copy under your control, with locators and a freshness check."
---

# Transcript capture

Search and drafts are only as good as the raw text you can still open. Chat apps, meeting tools, and some local coding hosts keep transcripts for you until they do not. Keep a copy you control.

## What to copy

- Meeting notes and the matching raw transcript, as soon as the meeting ends.
- Chat threads that the notes rely on, if you already have a right to keep them.
- Local session logs from a coding host, if that host deletes them after a fixed period. Public documentation for at least one widely used host defaults to 30 days from last activity. If you run more than one local profile, the copy job must cover every profile, not only the default one.

Do not copy anything you do not have a right to keep. Do not publish the copy.

## How to store it

- One raw file per meeting, thread, or session, append-only. New messages are added; existing bytes do not change. If a tool rewrites a file, move the previous bytes to a versions folder so an old locator still resolves.
- Record a locator `{file, char_start, char_end}` for every leaf you will later search or cite.
- Keep a manifest of file, sha256, and length. A freshness check fails when a raw file is missing, extra, or no longer matches its sha.
- Resolve display names at index time if you must, but never let a summary replace the raw text.

A later retrieval layer can sit on top of this store. It is not a substitute for the store. See the hybrid index in the context-walk repository.

## Operational checks

- Count meetings that ended today against notes saved today. A missing pair fails the check.
- The copy job writes a heartbeat. A missed heartbeat is a failed run, not a quiet skip.
- A host cleanup window is a deadline. Copy first; changing a retention setting, if you choose to, is a separate decision.

See the [worked example](examples/worked.md).
