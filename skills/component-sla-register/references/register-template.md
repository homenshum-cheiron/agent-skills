# Component SLA register (template)

Stamp: <date> · built on component registry <commit> · system version <commit/prompt/model/grader>
Labels: OBS observed · DER derived · EST estimate · INF inferred · NV not verified · TBD no source
Status: T+P tracked and posted · T tracked, not posted · U untracked

## Components
| ID (`<pipeline>.<type>.<name>` or `shared.*`) | Responsibility (one line) | In → Out contract | SLA metric (target · source/date, or "TBD: set by <measurement>") | Owner (source) | Blast radius | Used by |
|---|---|---|---|---|---|---|

Include agent-framework components: context handoff · tool definitions + instructions · skills · sub-agent dispatch + scope · allow/ask/deny policy · agent↔sub-agent transition · judge/verifier.

## Failure modes
| FM-<component>-NN | Symptom signature | Keywords / trace and log signals | Grader measure (or none) | Status |
|---|---|---|---|---|

## Attribution walk
0 stamp → 1 finished? → 2 valid output? → 3 which measure failed? → 4 evidence chain upstream, stop at first "no" → 5 one line per row with FM ID → 6 count per FM per run (including rows a scoring rule drops)

## Keyword → component index
| Keyword / signal | FM ID | Component |
|---|---|---|

## Gaps (no detection today), ranked
| Rank | FM ID | Why undetected | Evidence and math (rate × volume) | Expected impact |
|---|---|---|---|---|

## Self-review
Which component exactly? Measured or guessed? Who owns it? How would we detect it next time?
