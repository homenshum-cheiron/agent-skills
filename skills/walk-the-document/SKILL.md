---
name: walk-the-document
description: "Read a long document that search has already found by place: outline it, find the exact string, read the smallest enclosing section, then widen or narrow with exact offsets kept for citation."
---

# Walk the document

Search finds the document. It rarely returns the deciding passage whole. A ranked list of fragments cuts a clause mid-list, drops the table row that shares no word with the question, and invites the same document to be fetched again with new wording.

Once a document is in hand, stop searching it and start reading it by place.

1. **Outline first.** Get headings with their line, character and page ranges and an estimated size. Treat it as a map, not as evidence. If the document has no headings, say so and use fixed windows; do not invent sections.
2. **Locate.** Search the full text for an exact string taken from the question or from a fragment search returned: a code, an article number, a defined term. Every hit reports its section path. A literal find is cheap and does not depend on ranking.
3. **Read the smallest enclosing unit.** Read the whole section that holds the hit, not a window of ranked fragments. A list, a table and its lead-in sentence belong together.
4. **Widen or narrow on evidence.**
   - Widen to the parent or the next section when the text points elsewhere ("see 2.3", "as defined in"), when a table continues, or when the section states a rule and the exception sits beside it.
   - Narrow to a line range when the section is larger than the remaining budget and the hit is a single row.
   - Stop when the passage answers the question and names its own conditions. Stop as well when two widenings add nothing; report "not found in this document" instead of reading on.
5. **Respect a budget.** Each read has a size limit. A cut read returns a cursor for the rest. Count every read, including the outline, against the task's total. Large budgets hide bad navigation.
6. **Cite by offset.** Quote only text returned by a read, with its character range, line range, page and section path. An outline entry, a summary or a remembered phrase is never the cited span. After stitching several reads, keep each piece's own range.

## What this does not settle

- It does not find the document. Use search for that.
- It does not judge which section is right when several match. That is the reader's decision; record the reason.
- Headings can mislead. A row can sit under a heading that contradicts it. Read the row and the text that refers to it.
- Scanned pages, script-loaded pages and broken extraction need a faithful text copy first. Check that the copy holds the passage before trusting an empty find.
- This is query-time reading by place. It is not index-time contextual retrieval, which prepends chunk-specific context before embedding or lexical indexing, and it is not a graph. Widen one step when the text points beside the hit. Do not load the whole document because a neighbor might matter.

## Helper

The [offline helper](scripts/docwalk.py) works on one local text or Markdown file. It needs Python 3.10+ and no packages. It prints JSON.

```sh
python3 scripts/docwalk.py outline FILE --depth 2
python3 scripts/docwalk.py find FILE "B.4.c"
python3 scripts/docwalk.py read FILE --section 1.2.2
python3 scripts/docwalk.py read FILE --line 31 --scope parent
python3 scripts/docwalk.py read FILE --chars 812:2400 --max-chars 4000
```

See [the commands](references/commands.md) and [a worked example](examples/worked.md) on a [synthetic guideline](examples/sample-guideline.md).

The helper is a reading tool, not a retrieval system. It does no ranking, no embedding and no model call, and it does not convert PDF or HTML. Token counts are estimates (characters divided by 4). This folder ships no benchmark result; do not cite it as measured proof that the method beats another.
