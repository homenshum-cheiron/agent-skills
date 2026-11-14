---
name: component-sla-register
description: "Use before attributing pipeline failures or proposing a fix for an agent or LLM pipeline. Build or refresh a register of components, their input-to-output contracts, service targets, owners, and numbered failure modes, then blame each failed row on the first broken contract and count it under a failure-mode ID."
---

# Component SLA register

A failed row is usually blamed on the last component that touched it. Often the real fault is upstream: a fetch returned nothing, a document never reached the corpus, or a scoring rule dropped the row. Keep one register of what each component promises, and walk each failure upstream to the first broken promise.

The register is a working record, not a monitor or a merge gate. A target in it does not change a production setting.

## 1. Build or refresh the register

Copy [the template](references/register-template.md). Stamp it with the date, the commit of the component list it is built on, and the system version (code, prompts and skills, model ID, grader).

**Components.** Name each one `<pipeline>.<type>.<name>`. Useful types: orchestration, model, prompt, tool, retrieval, data, output, check, grade. A part used by two or more pipelines is `shared.<type>.<name>` and carries a used-by list. Extend one list; do not fork it per pipeline. Per component, write:

- responsibility, in one line;
- the input-to-output contract, including what it returns on failure;
- a service metric with a sourced target, or "target TBD" plus the measurement that would set it;
- the owner, from a source, otherwise TBD;
- blast radius: the downstream components a failure here corrupts.

Agent-framework parts are components too: context handoff, tool definitions and their instructions, skills, sub-agent dispatch and scope, the allow, ask, and deny policy, the agent-to-sub-agent transition, and any judge or verifier.

Split a coarse component, such as "the crawler", until each failure mode points to one owner.

**Failure modes.** Give each one an ID, `FM-<component>-NN`. Record the symptom signature, searchable keywords and trace or log signals, the grader measure that catches it (or "none"), and a status: tracked and posted, tracked but not posted, or untracked.

**Keyword index.** Map each keyword or log signal to an FM ID and its component. Start every attribution here, then confirm in traces or code.

## 2. Attribute each failure to the first broken contract

Blame the most upstream component whose output contract was broken. A downstream component that handled bad input correctly is not at fault. It can own a second failure if it hid the problem.

0. Stamp the row: commit, prompts and skills, model ID, grader, case. No stamp, no attribution.
1. Did the run finish? If not, look at orchestration: runtime, worker, child return.
2. Is the output valid? If not, look at the output schema.
3. Which grader measure failed? A wrong answer with the right evidence points at the prompt, a check, or reference data. Missing evidence, a refusal, or a blank goes to step 4. Slow or costly only points at caching, compaction, fan-out, or repeated fetches.
4. Walk the evidence chain upstream and stop at the first "no". Did the agent try the right source? Did the live read return text, or a typed error? Was the document in the corpus? Is the source registered and collecting? Was the original readable? Was it admitted? Did it reach this deployment's copy? Given a known gap, did the answer state it? Not stating a known gap is a second, downstream fault.
5. Write one line per row: case, unit, measure failed, FM ID, evidence link, observed or inferred. When two FMs apply, list both and mark the upstream one.
6. Count rows per FM ID per run. A row that a scoring rule removes, such as "failed only because the source is unreachable", is still counted under its FM ID.

If no FM fits, add one to the register before you write the finding. If the component is `shared.*`, a fix must be tested on every pipeline in its used-by list.

## 3. Carry FM IDs forward

- **Findings** name the component, the FM ID, the current count with its version stamp, and the tracking status.
- **Proposals** name the FM IDs they move: for each, the current count or rate, the predicted change, and the signal that will show it. A proposal that cannot name an FM ID either targets an untracked failure (add it to the register first) or is not yet specific enough to test. When the contract belongs to another team, name that owner.

## 4. Rank the gaps

List the failure modes with no detection today. For each: why it goes undetected, the evidence, the arithmetic (rate times volume, with each input labelled observed, derived, or estimated), and the expected impact. Rank by harm first, then cost.

## Self-review

- Which component exactly, and is it the most upstream broken contract?
- Is the number measured or guessed? Is the baseline on the same version?
- Who owns it, according to which source?
- Did a scoring rule drop rows that still belong in an FM count?
- How would this failure be detected next time without a person reading the row?

Building the register is free analysis. It does not authorize paid runs, production changes, or messages to owners. See the [synthetic worked example](examples/worked.md).
