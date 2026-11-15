---
name: modernize-tests-after-method-change
description: "Use as the last stage after a pipeline component's method changes (new algorithm, model, retrieval step, or parser), and whenever old tests fail for a correct change or pass suspiciously. Classify the component's tests as behavior-pinning, over-strict, coverage-theater, or implementation-coupled, prove the keepers can fail, rewrite the rest to pin the behavior contract, and report counts."
---

# Modernize tests after a method change

After a component gets a better method, its old tests often pin the old method's outputs: exact messages, list positions, intermediate values. They then fail for a correct change, or they pass while checking nothing. The usual fix, loosening assertions until green, produces coverage theater. This stage replaces that with a short, checkable pass.

Place in a pipeline: find a gap → research a better method → build it → **modernize the tests** → fresh-context review.

## Inputs

- The component's behavior contract: what callers rely on, in 3 to 10 lines, written before you touch tests.
- The diff of the method change, and the test results from before the change.

## Steps

1. **Baseline.** Run the suite before the change and save the pass/fail list.
2. **Scope.** List every test that exercises the changed component. One module per pass.
3. **Classify** each test with a one-line reason that cites the asserted line:
   - *behavior-pinning*: asserts the contract (inputs to outputs a caller relies on);
   - *over-strict*: asserts message wording, ordering, intermediate values, or the old method's internals;
   - *coverage-theater*: still passes if the behavior it names is removed, or passes through a different rule;
   - *implementation-coupled*: depends on fixture positions, environment, or file layout rather than the contract. An intentional environment gate (for example a repository hygiene check) is behavior-pinning for that gate; say so.
4. **Prove keepers can fail.** For each behavior-pinning test, break the new code in one small way that matters (off-by-one threshold, flipped comparison, removed branch). Confirm red, then restore. A test that stays green moves to coverage-theater.
5. **Rewrite.** Over-strict and implementation-coupled tests pin the contract instead: look items up by identifier, assert the status and the reason that matters, not the full message. Strengthen coverage-theater tests until the step 4 mutation turns them red.
6. **Never delete a test.** Mark a replaced test skipped with a reason and the name of its replacement until review accepts it.
7. **A comparison that cannot run is a failure, not a skip.** Report how many cases executed; zero means not proven.

## Done when

- Every in-scope test has a class and a cited reason.
- Every kept or rewritten behavior-pinning test has a recorded mutation that turns it red.
- The suite passes on the new method, with no new skips except marked replacements.
- The report lists counts per class, each rewrite with its mutation result, and tests left unchanged on purpose.

## Cost rules

- Run the classifier on a mid-tier model at medium effort and pin the model; an unpinned subagent can inherit the parent's model.
- A reviewer in a fresh session checks the rewrites against the contract and the diff, not against the classification conversation.
- Spot-check at least three classifications yourself with a script before accepting the rest. Classifiers produce false positives (see the example).

## Credit

The test principles ("the legacy code is the oracle", "a comparison that cannot run is a failure", "prove the tests can fail") follow the `test-engineer` agent in Anthropic's `code-modernization` plugin (Apache-2.0). That agent writes characterization tests before a rewrite; this skill applies the same principles to auditing existing tests after a method change.

Related: `lean-test-design` (planning paid evals, a different question), `pipeline-inefficiency-loop` (finds the change that triggers this stage), `proof-before-review`.

See the [synthetic worked example](examples/worked.md).
