# Worked example (invented)

A weekly planning huddle ends at 10:30 AM. The chat app has an AI notes canvas and a transcript file. The capture job:

1. Writes `notes/planning-2026-03-02.md` and `transcript/planning-2026-03-02.txt` into a local raw folder.
2. Records both sha256 values in a manifest.
3. Refuses to overwrite the notes file when the same content is fetched again (status: unchanged).
4. When a later chat message arrives in a related thread, appends only the new message and checks that the previous bytes are unchanged.

A freshness test that same afternoon lists the two files, matches both shas, and confirms that a locator into the line "I worry about vendor lock-in" round-trips to that exact sentence. A week later the chat app still has the meeting, but the local copy is what search and action-item drafts use, because it will still be there if the app drops it.
