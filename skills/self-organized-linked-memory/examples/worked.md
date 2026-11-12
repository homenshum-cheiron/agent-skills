# Worked example (synthetic)

Evidence in `workspace/source/records.jsonl`:

- R1 (5 March): "Let's plan the reading group for March 18 at the Riverside Library."
- R2 (12 March): "Let's hold the March 18 meeting at the Community Center instead; the library is under repair."

Notes in `workspace/topics/community/reading-group.md`:

- `^venue-v1` says Riverside Library and cites R1.
- `^venue-v2` says Community Center because of the repair, cites R1 and R2, and has `supersedes: venue-v1`.

Question: "Where is the March 18 meeting and why did it move?"

```sh
python3 scripts/linkmem.py validate examples/workspace
python3 scripts/linkmem.py packet examples/workspace "Where is the March 18 meeting and why did it move?"
```

The search ranks the old unit `^venue-v1` first. The walk does not stop there. It moves to `^venue-v2`, adds the linked note about snacks, the evidence R1 to R4, and only then the history line `[HISTORY ^venue-v1, superseded by ^venue-v2]`.

Answer: "The Community Center, because the library is under repair (R2, 12 March). It was planned for the Riverside Library before (R1)."

What a flat list of facts tends to do here: it shows both sentences with similar weight, and the reader has to notice the dates.

Edits the check refuses:

- changing the text of R1 (the source is append-only);
- deleting `^venue-v1` with no unit that supersedes it;
- a footnote citing R99, a time such as `2026-13`, or a link to a missing id;
- `^venue-v1` and `^venue-v2` superseding each other.
