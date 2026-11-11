# Failure routing guide

Categories guide investigation; they are not proof of cause. Several may contribute to one incident.

| System | Failure class | Distinguishing evidence | Typical repair boundary |
|---|---|---|---|
| Data operations | Untracked source | No registered source/schedule | Coverage registry owner |
| Data operations | Trigger absent or late | Expected attempt missing | Scheduler/workflow owner |
| Data operations | Crawl/ingest failed | Run reached a stage but did not finish | Stage owner |
| Data operations | Network failure | DNS, connection, timeout evidence | Transport/retry policy |
| Data operations | Site refusal | Explicit denial/rate limit | Access policy, authorized backoff |
| Data operations | Site/schema changed | Successful fetch, changed structure | Parser/contract owner |
| Data operations | Unknown new blocker | Observed failure, cause not established | Triage, preserve evidence |
| Agent execution | Tool error | Tool response or contract mismatch | Tool implementation/integration |
| Agent execution | Instruction/skill error | Wrong procedure despite adequate facts | Instruction owner and regression case |
| Agent evaluation | Context pollution | Unrelated/stale content changes decision | Retrieval/context selection |
| Agent evaluation | Unsupported claim | Output lacks supporting evidence | Grounding/verifier design |
| Agent evaluation | Model recall failure | Relevant facts present, not used | Controlled model/case comparison |
| Agent execution | Compaction/attention loss | Facts dropped or obscured in handoff | Context lifecycle owner |

Also check storage corruption, partial pagination, clock skew, identity collisions, duplicate retries, missing authorization, dependency outage, and monitoring failure itself. Do not label a parser failure “hallucination” or a model failure “network” without evidence.

Choose explicit service objectives for each system. Record unknown ownership; do not infer it from a folder or username. Recovery can be automated only within the approved action scope and with a bounded stop condition.
