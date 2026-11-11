# Example: a document loader (synthetic)

Problem: agents repeatedly save whole documents to files and grep them, losing section identity and using more tokens.

First inspect the existing fetch API: does it return stable document IDs, version, section anchors, pagination, and attachment metadata? If it already does, use those capabilities. If it does not, define the missing contract and test it rather than calling the save-and-grep experiment a completed loader.

Expected result for “read section 4”: exact section text, document/version identity, source location, and an explicit partial/truncated flag. A search hit is discovery, not the full section.

A request for a new neighbors tool is declined when the existing fetch can take `include=neighbors` and return adjacent ids. No new store is added. A size cap remains inside the tool as a safety net. If widening cannot express the job, the written reason is what justifies a new tool. A checklist that says "zero new tools" is not automatically the right product decision.
