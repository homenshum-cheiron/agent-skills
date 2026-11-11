# Helper commands

All commands take one local UTF-8 text or Markdown file and print JSON. Exit code 0 means a result. Exit code 2 means a bad request; the reason is on standard error. Line endings are read as `\n`, so offsets refer to the normalised text.

Add `--numbered` to any command to treat lines such as `3.2 Title` as headings as well as Markdown `#` headings. Use the same flag on every call for one document, because section ids depend on it.

## outline

`outline FILE [--depth N]`

Returns `source` (`headings`, or `windows` when the file has no headings and 80-line windows are used), totals, and one row per section:

| Field | Meaning |
|---|---|
| `id` | Position in the tree, for example `1.2.2`. Not the number printed in the title |
| `path` | Titles from the root to this section |
| `line_start`, `line_end` | 1-based, inclusive. A parent's range covers its children |
| `char_start`, `char_end` | Offsets into the text, end exclusive |
| `page_start`, `page_end` | Pages split on the form feed character. A file without one is page 1 |
| `est_tokens` | Characters divided by 4. An estimate |

## find

`find FILE PATTERN [--regex] [--ignore-case] [--limit 20]`

The pattern is literal unless `--regex` is given. Returns `total`, `shown`, and for each hit its line, character range, page, section id, section path and the line text (first 240 characters). `total` is the true count even when fewer are shown.

## read

`read FILE` with exactly one range:

| Option | Reads |
|---|---|
| `--section ID [--to-section ID]` | One section, or from the start of the first to the end of the second |
| `--line N [--scope section\|parent\|lines] [--before 5] [--after 5]` | The section that holds line N, its parent, or a line window around it |
| `--lines A:B` | Lines A to B, inclusive |
| `--pages A:B` | Pages A to B |
| `--chars A:B` | Characters A to B, end exclusive |

`--max-chars` (default 8000) limits the returned text. A longer range is cut at a line end, `truncated` is true, and `next.chars` holds the range that continues the read. Reading each `next` in turn returns the range exactly once.

The result always holds `text` (verbatim), its character, line and page range, and the section path at its start. `text` equals the file's normalised text at `char_start:char_end`.

## Limits

- No PDF, HTML or scanned-page conversion. Convert first and keep form feeds between pages if page numbers matter.
- Numbered-heading detection is a pattern. It can take a numbered list item for a heading. Check the outline before relying on it.
- Section ids change when the document changes. Store offsets together with a hash of the file if a citation must survive an update.
