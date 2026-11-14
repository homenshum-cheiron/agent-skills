# Research claims

Use these rules when what you read becomes a claim someone will rely on, such as a requirement, a fee or a deadline.

- **Vague scope: infer, run, then confirm.** For a scope like "the large markets", choose the most defensible set and state it in one line. Run it and show the results, then ask whether the set is right. Ask before spending only if the inferred run would be unusually expensive or slow, and give the estimate and where it came from.
- **Primary first, and prove it.** Cite a secondary summary only with "according to" wording, and only after a primary-attempt log records each attempt: the primary URL tried, the failure type, the workaround tried (retry, alternate URL, index page, cached copy, OCR, a different fetcher) and the result. With no log or no workaround, go back to the primary.
- **Claims before prose.** Write one fact per claim, each with its source, exact quote and qualifiers. Then build the prose from the claims, and keep the claim IDs on each sentence. When an answer is wrong, the trace shows which claim, source or step failed.
- **Repair unsourced sentences.** A sentence with no source becomes a task to find one. Drop it only after real attempts fail, and say what was checked. Do not just label it unverified.
- **Never write "no rule exists".** Write "No rule found in:", list the source types checked, and nest under each type every source with its link and what it returned.

## Synthetic format

All names, URLs and values below are made up for illustration.

## Claim list (written before the prose)

| Claim | One fact | Source | Exact quote | Qualifiers |
|---|---|---|---|---|
| c_01 | Agency A fee for a type X application is 1,000 units | https://example.org/agency-a/fees | "Fee for type X applications: 1,000" | none |
| c_02 | Agency A requires a local study for category B products | https://example.org/agency-a/guidance/b | "Category B products require a local study" | "unless already approved in region R" |

Prose built from the list: "Agency A charges 1,000 units for a type X application [c_01]. It requires a local study for category B products unless they are already approved in region R [c_02]."

## Primary-attempt log (required before any secondary source)

| URL tried | Failure type | Workaround tried | Result |
|---|---|---|---|
| https://example.org/agency-a/notice-17 | HTTP 403 | Retry after 60 s, then a different fetcher | 403 again |
| https://example.org/agency-a/notices (index) | none | Opened the index page to find a mirror | Found a PDF copy; claim sourced from the primary |

A secondary summary may be cited ("according to Example Law Blog") only if every row ends in failure after a workaround.

## Absence wording

No rule found in: agency guidance index, agency notices (2024 to 2026).
- Agency guidance index
  - https://example.org/agency-a/guidance: searched "label insert", 0 relevant hits, checked 2026-11-12
- Agency notices
  - https://example.org/agency-a/notices: 2 of 2 pages read, no match
