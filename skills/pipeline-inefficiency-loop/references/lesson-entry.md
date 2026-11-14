# Lesson entry and lap summary

Every lap writes one lesson entry, whatever the verdict (adopted, rejected, skipped, parked). Append it. Do not edit an earlier entry; a correction is a new entry that names the one it replaces.

## Lesson entry

```
Lap <n> · <date> · version stamp <commit, prompts, skills, tools, model ID, grader>
Finding: <one line> · FM ID <..> · verdict <adopted | rejected | skipped | parked>

Why was it not found sooner? (pick one or more, with evidence)
  [ ] no signal existed for this failure
  [ ] a signal existed but no scan or person read it
  [ ] a scoring rule removed the rows from the count
  [ ] the failure mode was not in the register
  [ ] the component was too coarse to point at one owner
  [ ] the baseline was on another version, so the change looked like noise
  [ ] other: <..>

What changes so the next scan catches it?
  Detector: <query, log signal, or metric added or changed>
  Register: <new FM ID, keyword, finer component, new owner source>
  Scan checklist: <line added to the per-lap scan>
  Skill: <which skill text changed, if any>

Replay check on stored traces from earlier laps:
  Flags this lap's rows: <n of n>
  Flags earlier rows that were clean: <n of n>  (a flood means the detector is too broad)

If the verdict was reject or skip: which assumption failed, and why did the finding look promising?
Open clue still unchecked, and its cheapest check: <..>
```

A lesson that changes nothing the next scan reads is not encoded. Write "not encoded" and the reason instead of claiming a lesson.

## What the loop may and may not change

| May change in step 6 | May not change without the owner |
|---|---|
| Detector queries and log signals | The grader or the answer key |
| The register: FM IDs, keywords, component splits | The case list used for adopt decisions |
| The per-lap scan checklist | The budget, the stop rules, the human gates |
| Skill text, through the normal review path | Production settings |

## Lap summary (one block per lap, for the owner)

```
Lap <n>: <finding> (<component>, <FM ID>)
  Premise: <volume/yr> · <change/yr> · risk <direction> · harm <units>
  Test: <rungs climbed>, spend <amount> of cap <amount>
  Verdict: <..>; FM count <before> -> <after> on <version>
  Lesson: <why not sooner> -> <what the detector now catches>
  Next: <next lap's top finding | stop, and which stop rule fired>
```
