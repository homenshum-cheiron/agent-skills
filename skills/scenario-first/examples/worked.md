# Example: repeated import (synthetic)

Request: “Import this CSV twice without duplicating contacts.”

Input: an empty test store and a CSV containing two distinct rows; run the same import twice.

Expected output: two contacts, two attempt records, and a second-run result that says zero new contacts. The user must decide whether a changed email updates an existing contact or creates a new one; do not hide that identity decision in a test.

Work map:

| Work | Owner | Dependency | Evidence |
|---|---|---|---|
| Freeze duplicate/identity examples | Product owner | None | Accepted fixture |
| Add import deduplication | Import writer | Identity contract | Unit + real database tests |
| Add result rendering | UI writer | Response schema | Empty/success/retry states |
| Verify combined repeated flow | Reviewer | Both candidates | Two real calls, final records |

Failure still to decide: the same CSV is imported while the first attempt is open. A complete contract would name the rejection, the unchanged store, and the side effect, including no notification. Until the owner decides, that row stays unresolved rather than picking a convenient expected output.

A parser test proves that the rows can be read. It does not prove that two imports leave two records. The stage log in this skill records which later checks do not apply.
