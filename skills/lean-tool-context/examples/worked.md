# Example: a document loader (synthetic)

Problem: agents repeatedly save whole documents to files and grep them, losing section identity and using more tokens.

First inspect the existing fetch API: does it return stable document IDs, version, section anchors, pagination, and attachment metadata? If it already does, use those capabilities. If it does not, define the missing contract and test it rather than calling the save-and-grep experiment a completed loader.

Expected result for “read section 4”: exact section text, document/version identity, source location, and an explicit partial/truncated flag. A search hit is discovery, not the full section.
