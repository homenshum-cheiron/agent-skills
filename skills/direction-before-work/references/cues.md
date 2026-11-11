# Cues worth adding

Pick a row only when its question is still open.

| Uncertainty | Useful cues | Omit when |
|---|---|---|
| System boundaries | Context or container view; ownership and trust or tenant boundaries | A sentence already establishes them |
| Backend API behavior | Full request, processing, and response; happy and failure paths; errors and side effects; call sequence if order matters | The contract is already explicit and unchanged |
| Data transformation | Source, transform, and store; a complete fixture input and output; schema or lineage | A single obvious mapping is enough |
| UI experience | Current and expected screens; an annotated screenshot, wireframe, or HTML preview; loading, empty, success, error, and permission states; keyboard, focus, labels, contrast, and responsive behavior where they matter | There is no UI, or layout and interaction are already unambiguous |
| Agent orchestration | Temporary roles, write scopes, tool input and output, artifact handoff, stop, retry, and the error path | One agent already has a clear bounded task |
| Incident recovery | An evidence-backed timeline, actual versus expected, the failure boundary, and the recovered state | You are only reading back an unchanged status |
| Code or change shape | A focused current and proposed excerpt; boundary and compatibility examples | Prose already makes the change precise |
| Quantity, comparison, or timing | A table, chart, or timeline tied to source data and units | There is no numeric uncertainty. Never invent measurements |

Mermaid is enough for many flow, sequence, and state questions. Other public tools are optional building blocks. On 11 Nov 2026 the GitHub license field for Mermaid, Yantra, wireframe-doc, and visual-spec reported MIT. Recheck before adopting one. None of them is installed or runtime-tested here.
