# Public comparison and a small test plan

Read what is already public before opening a new benchmark.

1. Restate the decision the comparison is supposed to support.
2. Search current public reviews, docs, and published results. Cite the revision or the access date. Mark each source public and dated.
3. Say what those sources answer, and what they do not: a different version, a different workload, or a marketing-only claim.
4. If a public source is enough, stop. Do not run a private benchmark for completeness.
5. If a new comparison is still required, write the smallest honest plan and wait for the owner to ask before any personal-budget spend. Writing the plan is not approval.
6. If you do run something, keep the public notes beside the new results. Do not hide a disagreement.
7. If a pilot breaks its own rules, drop every arm that pilot touched. Do not keep a winner from an invalid comparison.

Synthetic illustration: the question is whether invented library A is still a reasonable default for sequence diagrams. Public docs and the library's MIT repository, as dated in the note, already show that it is maintained and documented. No paid render bake-off starts. Residual unknown: runtime on a 10k-node graph, explicitly unproven. This paragraph is a teaching scene, not a benchmark this repository ran.

## Smallest honest matrix

Use this only when a comparison is actually in scope.

- Write the plan down. The owner reads it before any paid run.
- Rows are candidate cases. Columns are behaviors the arms could change. Fill cells from past runs or metadata, not from hidden answer files. Mark cost and time as measured or estimated.
- Take the case that covers the most uncovered behaviors, and repeat until every behavior is covered or only named gaps remain.
- Each arm runs the cases whose behaviors it can change, plus one shared anchor. The reference arm runs the full minimal set. Model-versus-model arms use the same build and the same cases.
- Climb a free ladder first: dry-run configuration with no model calls, then stub or replay offline, then one representative paid case only after the owner asks, then the minimal set. Expand only on arms that differ from the reference.
- Put a cost cap on each arm and a hard total. Stop when a cap is hit, instrumentation looks wrong, early paid or live stages show no difference, or the remaining budget cannot finish a fair comparison. Treat an n=1 delta as noise until it repeats. Use the same base commit and the same grader version under every arm.
- Report the minimal plan's cost next to the naive all-arms plan, and report per-case regressions, not only an average.

Synthetic illustration: four build arms times twenty cases would be 80 naive runs. The matrix shows five behaviors. Three fixture cases cover four of them. "Scan of large attachments" stays a named gap. Offline replay shows one arm never fired its feature, so no paid run is requested. These counts are teaching numbers, not a measured experiment.
