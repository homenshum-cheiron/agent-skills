---
name: direction-before-work
description: "Use before planning or building when background, behavior, interactions, change shape, or the expected interface is still unclear for UI, API, data, agent, or incident work. Skip a full packet for a short change that is already obvious."
---

# Direction before work

Resolve the uncertainty that would make the build wrong. Use the smallest packet that answers it. Skip the packet for a typo, a copy edit, or an obvious one-line fix, and say that you skipped it.

A short direction still names the request, the relevant code, doc, or trace, and when that source was confirmed. Separate current evidence, reported claims, stale evidence, and synthetic examples. State current versus desired behavior, who is affected, why it matters, constraints, acceptance checks, unresolved questions, and what must not change.

Before adding a diagram, mock, or excerpt, name the question it answers. If it answers none, omit it. Prefer one or two diagrams. Label data flow versus control flow. Mermaid is a lightweight default when it is enough. A picture is not proof that the system behaves that way.

When a contract is unclear, give one complete concrete input, the processing, the expected output, at least one failure or edge path, the error contract, and side effects, including none. Label teaching data synthetic. Fragments and ellipses are not a contract.

Choose the preview the uncertainty actually needs:

- None, when there is no interface or the interaction is already clear.
- A static or click-through mock for layout, copy, and state switching, with no real backend.
- A functional prototype with synthetic fixtures only when reviewers must exercise behavior a mock cannot explain.

Say which behavior is simulated and which is implemented. Use HTML only when it is the useful format, under the host's ordinary page and security rules. Never imitate another service's sign-in and never collect credentials, secrets, or payment details. Show a labeled signed-in or permission state instead. A preview never authorizes a real send, write, or purchase. Include the accessibility that the change depends on: keyboard focus, labels, contrast, and the relevant loading, empty, success, error, and permission states.

Before proceeding, ask whether the recipient could explain the intended result, the main failure path, the boundaries, and the acceptance checks, and whether the cues still match their cited source. Record what is still unknown. Remove decorative artifacts.

Optional public building blocks, not required installs: Mermaid, Yantra, wireframe-doc, and visual-spec. A public-docs pass recorded on 10 Nov 2026 found no all-in-one direction-packet platform in that search. That is not a claim that none exists, and this repository has not re-run that search. Recheck license and fit before adopting any dependency.

This skill grants no permissions and does not add an approval gate or a required tool. It does not assign a model or an effort. The [cue table](references/cues.md) and the [synthetic digest example](examples/worked.md) show how to keep the packet small.
