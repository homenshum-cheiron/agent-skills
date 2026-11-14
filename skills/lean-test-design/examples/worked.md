# Worked example (synthetic): four arms on a document Q&A pipeline

Everything here is invented for illustration: the pipeline, the arms, the cases, the costs, and the results. No number below is a measurement. Model names are placeholders.

## Request

"We have four ideas to improve the `docqa` pipeline. Run all four against the reference on the 48-case eval, three times each, so we can compare."

Naive plan: 5 arms × 48 cases × 3 runs = 720 runs. At an illustrative $0.25 per run that is about $180, and several hours of wall time.

## Step 0: question and decision value

"Does any arm raise answer accuracy by at least 5 points without lowering citation accuracy?" Decision value (illustrative): the pipeline answers about 20,000 questions a year, so 5 points is about 1,000 fewer wrong answers a year. That justifies the maintenance of a change. A smaller gain does not.

Stamp: commit `aaaa111`, prompt v7, skills v3, tool set v2, model `model-a`, grader v4.

## Step 1: research

| Arm | Change | Research result | Label | Outcome |
|---|---|---|---|---|
| A1 | Swap to `model-b` | The migration guide says `model-b` rejects a forced tool choice. The pipeline forces one on the first turn. | official | Settled: a code fix, not an eval question. After the fix it goes through the model-swap ladder in `match-methods`. |
| A2 | Rewrite the search tool's description | Two independent issue threads report better tool selection with explicit "when to use" lines. The vendor's tool-use guide recommends the same pattern. | issue ×2, official | Test |
| A3 | Raise effort from medium to high | The model card says higher effort mainly helps multi-step reasoning. The eval has 9 multi-step cases. | official | Test, on multi-step cases only |
| A4 | Add "be concise" to the answer prompt | One forum post. No mechanism in an official source. | anecdote ×1 | Parked: one anecdote with no mechanism does not earn a paid run |

## Step 2: non-model factors

The prompt and the skills are held equal across A2, A3, and the reference. The dry run in rung 2 shows that A2's build still loads the old tool description from a cached skill bundle. The feature would not have fired. The bundle is rebuilt before any paid rung. Without the dry run, A2 would have looked like "no effect".

## Step 3: coverage and the minimal set

Seven behaviors. Cost per run is illustrative and the same for every arm here.

| Case | Multi-doc | Multi-step | Table | Scan | Long history | First-turn tool | Non-English | $ per run | Minutes |
|---|---|---|---|---|---|---|---|---|---|
| c04 | ✓ | | ✓ | | | ✓ | | 0.25 | 4 |
| c19 | | | | | ✓ | ✓ | ✓ | 0.25 | 3 |
| c31 | ✓ | ✓ | | | ✓ | | | 0.25 | 6 |
| c40 | | | ✓ | | | | ✓ | 0.25 | 3 |

Greedy order:

1. c04 adds 3 (multi-doc, table, first-turn tool).
2. c19 and c31 each add 2. The tie goes to c19, which is faster. c19 adds long history and non-English.
3. c31 adds 1 (multi-step).
4. c40 adds nothing new and goes to tier 2.

Named gap: no case covers a scanned page.

## Step 4: cases per arm

| Arm | Cases | Why |
|---|---|---|
| Reference | c04, c19, c31 | Full minimal set |
| A2 tool description | c04, c19 | Only first-turn tool choice can change. c04 is the anchor. |
| A3 effort | c04, c31 | c31 is the multi-step case. c04 is the anchor. |

## Steps 5 and 6: ladder, caps, owner read

Caps: $3 per arm, $10 total. The owner read the plan and approved paid rungs 4 to 6 up to the $10 cap. A full eval is outside that approval.

| Rung | Runs | Illustrative cost |
|---|---|---|
| 4: c04 on reference, A2, A3 | 3 | $0.75 |
| 5: the remaining minimal-set cases, one run each | 4 | $1.00 |
| 6: two more runs per case on A2, A3, and the reference on the same cases | 14 | $3.50 |
| Total | 21 | $5.25, against about $180 naive |

Illustrative outcome: A2 and A3 both differed from the reference at rung 4, so both climbed. At rung 6, the reference's own repeats showed how much a case moves between reruns. A3's gain stayed inside that rerun noise, so it is reported as "no detected difference", not "no effect". A2's gain held on c04 and c19 across all three runs. A2 goes forward to a full eval sized for a 5-point gap, which needs a new approval.

## Step 7: stamping

All results carry the stamp above. A week later, the grader moved to v5. Every result in this plan was then marked stale. The next comparison uses a new reference run on grader v5, not these numbers.

## What the reader of the report sees

- 4 arms planned: 1 settled by research, 1 parked at research, 1 no detected difference, 1 forward to a sized full eval.
- Spend: about $5.25 of a $10 cap, against about $180 naive (all illustrative).
- Gap: no scanned-page case. That behavior is untested by this plan.
