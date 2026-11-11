# Stage log for the import example (synthetic)

The order below is the plan for [the worked import example](../examples/worked.md). A stage that does not apply is skipped in writing, not silently.

- **Named revision.** The import path was read at invented SHA `synthetic-abc1234`. A meeting claim that "duplicates are already handled" stays a claim until it matches that code.
- **Direction packet.** Skipped. The request already names the CSV columns, the empty store, and the duplicate outcome. That skip is stated here. If the response shape or the UI were still unclear, the smallest contract and the relevant states would be written before implementation.
- **Scenarios.** R1: importing the same CSV twice leaves two contacts and reports zero new contacts on the second run. R2: a second import started while the first is open. The expected rejection, the unchanged store, and "no notification sent" are unresolved until the owner decides. Status of R2: unmeasured.
- **Research.** Measured: the current insert path at `synthetic-abc1234`. Unverified: whether a changed email updates a contact or creates one.
- **Options.** Not applicable. One approach is in scope, so no comparison table is built. Stated here.
- **Tool surface.** Not applicable. No new agent tool is proposed. Stated here.
- **Speed or cost.** Not applicable. No speed or cost claim is being made, so no phase table is required. Stated here.
- **Paid comparison.** Not applicable. Nobody asked for a model bake-off. Stated here.
- **Proof still open.** Two real calls on a named tip, compared with the frozen expected rows. A parser test would not close this stage.
- **Report.** The outcome is still unproven. The next action is the owner's identity decision. No message has been sent.

Formatting this log is not a substitute for the skipped direction packet. The packet was skipped because the request was already specific, and that reason is visible.
