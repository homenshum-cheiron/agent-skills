# Worked example (synthetic)

Everything below is invented for teaching. No real service, company, quota, or price is described.

## Header

**Nightly summary jobs — isolated runs, bounded provider use, verified cleanup**

- Status: Proposed. A local prototype exists; nothing is deployed.
- Date: 2030-03-04. Revision 1, consolidating the design review of 2030-03-02.
- Scope: the job scheduler and its run namespace. Out of scope: the web console redesign and production tenants.

## What this is

1. An operator picks a dataset and a prompt version and starts a run.
2. Each dataset row becomes one job; results stream to the console.

Non-negotiables:

- **Isolation:** one run cannot read or delete another run's rows.
- **Bounded use:** admitted runs stay under 85% of the verified provider quota.
- **Reproducible:** a queued run never follows a later prompt edit.

This is a target and delta, not a claim that anything is deployed. Numbers are illustrative.

## Current state and evidence

| Repository (pinned) | Responsibility |
|---|---|
| `console@a1b2c3d` | Operator UI and sign-in |
| `worker@d4e5f6a` | Current single-process batch runner |

The runner has a per-process concurrency cap. That does not establish a cross-process quota guard.

## Gap table

| Requirement | Foundation / limitation | Target change |
|---|---|---|
| One job per row | Single process loops rows | Scheduler launches row jobs, at most C active |
| Quota-aware admission | Per-process cap only | Shared reservation at 85% of verified quota |

## Budget math (illustrative)

Volume: 1,200 rows/night × 365 = 438,000 rows/yr. At $0.04/row: $48/night, $17,520/yr. High scenario 3,000 rows/night: $43,800/yr.

| Dimension | Quota | 85% ceiling | Reserved | Per new slot | Slots fitting |
|---|---:|---:|---:|---:|---:|
| Requests/min | 600 | 510 | 150 | 40 | 9 |
| Tokens/min | 400,000 | 340,000 | 100,000 | 45,000 | **5** |

Tokens are tightest: 100,000 + 5 × 45,000 = 325,000 fits; 6 slots need 370,000 > 340,000.

## Flow

```text
start run → authorize → freeze dataset and prompt hash → reserve or queue (FIFO)
 → prepare once → one job per row, at most C → persist result → stream → release reservation
```

Edge cases: a retried job whose first attempt finishes late is fenced by attempt ID; a cancel during preparation drains before cleanup; a lost provider response is retried as a new attempt, not counted as success.

## Roadmap

| Phase | Deliverable | Gate |
|---|---|---|
| 1 | Scheduler with row jobs | 11 rows, C = 5, no cross-row writes |
| 2 | Quota reservation | Synthetic check admits 5, rejects 6 |

## Self-review answers

- Exact model and owner: "example-model-v2", owned by the platform team; next action: the platform lead reviews by Friday.
- Cheaper than what: the current runner at the same 1,200 rows/night; this proposal does not change per-row cost, it bounds the rate.
- Measured versus illustrative: all numbers are illustrative; phase 2 measures the per-slot demand.
- Not established: the prototype does not prove the cluster has capacity for C = 5.
