# Worked example (synthetic): four arms on a document Q&A pipeline

Everything here is invented for illustration: the pipeline, the arms, the cases, the costs, and the results. No number below is a measurement. Model names are placeholders.

## Request

"We have four ideas to improve the `docqa` pipeline. Run all four against the reference on the 48-case eval, three times each, so we can compare."

Naive plan: 5 arms × 48 cases × 3 runs = 720 runs. At an illustrative $0.25 per run that is about $180, and several hours of wall time.

## Step 0: question and decision value

"Does any arm raise answer accuracy by at least 5 points without lowering citation accuracy? A 5-point gain would justify the change; anything smaller is not worth the maintenance." Stamp: commit `aaaa111`, prompt v7, skills v3, tool set v2, model `model-a`, grader v4.

## Step 1: research

| Arm | Change | Research result | Label |
|---|---|---|---|
| A1 | Swap to `model-b` | The migration guide says `model-b` rejects a forced tool choice. The pipeline forces one on the first turn. | official |
| A2 | Rewrite the search tool's description | Two independent issue threads report better tool selection with explicit "when to use" lines. No official source. | issue ×2 |
| A3 | Raise effort from medium to high | The model card says higher effort mainly helps multi-step reasoning. The eval has 9 such cases. | official |
| A4 | Add "be concise" to the answer prompt | One forum post. No mechanism in an official source. | anecdote ×1 |

A1 is settled without a run: the forced tool choice is a code fix, not an eval question. It returns to the queue after the fix. A4 stays in, but at low priority.

## Step 2: non-model factors

The prompt and the skills are held equal across A2 and A3. The dry run in rung 2 shows that A2's build still loads the old tool description from a cached skill bundle. The feature would not have fired. The bundle is rebuilt before any paid rung. Without the dry run, A2 would have looked like "no effect".

## Step 3: coverage and the minimal set

Six behaviors: multi-document answer, table reading, scanned page, long history, tool choice on the first turn, non-English question.

| Case | Multi-doc | Table | Scan | Long history | First-turn tool | Non-English |
|---|---|---|---|---|---|---|
| c04 | ✓ | ✓ | | | ✓ | |
| c19 | | | | ✓ | ✓ | ✓ |
| c31 | ✓ | | | ✓ | | |
| c40 | | ✓ | | | | ✓ |

Greedy order: c04 (3 new), c19 (2 new), c31 (adds nothing new, kept as a second multi-step case for A3). Named gap: no case covers a scanned page. c40 goes to tier 2.

## Step 4: cases per arm

| Arm | Cases | Why |
|---|---|---|
| Reference | c04, c19, c31 | Full minimal set |
| A2 tool description | c04, c19 | Only first-turn tool choice can change; c04 is the anchor |
| A3 effort | c04, c31 | Multi-step cases; c04 is the anchor |
| A4 concise | c04 | Anchor only, until it shows a difference |

## Steps 5 and 6: ladder, caps, owner read

Caps: $3 per arm, $10 total. The plan costs about 8 runs at rung 5 plus up to 12 repeats at rung 6, about $5 at the illustrative rate, against about $180 naive. The owner read the plan before rung 4.

Illustrative outcome: at rung 4, A4 matched the reference on c04 and stopped there. A2 and A3 differed, so they ran the minimal set and then three repeats. A3's gain did not repeat. It was inside the rerun noise from the repeats, so it was reported as "no detected difference". A2's gain repeated on c04 and c19. A2 goes forward to a full eval sized for a 5-point gap, which needs a separate approval.

## Step 7: stamping

All results carry the stamp above. A week later, the grader moved to v5. Every result in this plan was then marked stale. The next comparison uses a new reference run on grader v5, not these numbers.

## What the reader of the report sees

- 4 arms planned: 1 settled by research, 1 stopped at one case, 1 no detected difference, 1 forward to a sized full eval.
- Spend: about $5 of a $10 cap, against about $180 naive (all illustrative).
- Gap: no scanned-page case. That behavior is untested by this plan.
