# Example: concurrent test runners (synthetic)

A change adds a database bootstrap helper. One isolated run passes 120 selected tests. The helper uses a fixed database name and drops it on exit.

Relevant scenario: start two independent runs simultaneously. Input: two processes, identical command, same database server. Expected: neither can destroy the other's database. Actual in a controlled fixture: one run terminates when the other drops the shared database.

Review statement: “120 selected tests passed in isolation. A concurrent-run reproduction failed: both processes share one database. Use a per-run database identity and test simultaneous startup and cleanup. Full application tests and production deployment were not run.”

Name the revisions in that statement. For this teaching scene they are baseline `aaa1111`, merge-base `aaa1111`, and tip `bbb2222`, all invented labels. The isolated unit run is a lower-level check. It is not proof of a running API. If the fixture also contained an unmerged parent change, say so and name that parent; do not present the result as isolated proof of this diff alone.

Do not say “all tests pass” or approve based on the single-run result. The fixture packet in this folder is synthetic bookkeeping, not a receipt for those 120 tests. Queued CI on a later commit would not make this review green.
