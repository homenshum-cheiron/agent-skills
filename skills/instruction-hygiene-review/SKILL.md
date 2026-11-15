---
name: instruction-hygiene-review
description: "Use weekly, or when agents act on contradictory or outdated standing instructions: scan instruction files and skills for size-limit truncation, conflicting model or effort pins, superseded dates, dead references, and never-used skills; retire stale rules into an archive instead of deleting them; and run an underuse review that finds methods which should have fired but did not, with a trigger rule for each."
---

# Instruction hygiene review

Standing instructions pile up. Old delegation, routing, and operations rules stay next to the rules that replaced them, and routers and workers then follow whichever line they read first. Separately, good methods sit unused because nothing triggers them. This review handles both, on a schedule, in two stages: a deterministic scan with no model calls, then a short judged pass.

## Stage 1: deterministic scan (no model calls)

Run a script that writes a dated report (Markdown plus JSON) with:

1. **Size versus loader limits.** Byte size of every instruction file the hosts load, next to each host's documented limit. A file over its limit is silently truncated: the tail rules are not in effect. Flag files above 90% of a limit.
2. **Conflicts.** The same topic with different values: model pins, effort levels, allowed or banned lists, caps, dates. Group by topic keyword and print each line with its file and line number.
3. **Superseded dates.** Lines that say "until", "pending", or "decision needed" whose date is past, or that a later dated line contradicts.
4. **Dead references.** Paths that do not exist, commands not on the PATH, model names not on the current supported list.
5. **Never-loaded skills.** Skills with no load event in the last N days, from local session logs.
6. **Launcher mismatch.** Instructions that rely on a wrapper (for example, "print an escalate marker") while the launcher logs show plain calls.

The scan proposes nothing on its own. It lists candidates with evidence.

## Stage 2: judged pass

Use a reviewer in a fresh session, which reads the report and the cited lines, not the history of the files.

- For each candidate, choose **keep, retire, merge, or rewrite**, with one reason.
- **Retire, never delete.** Move the text verbatim to an archive file with the original location, date, reason, and the rule that supersedes it. Leave a one-line pointer where the text was. Retirement must be reversible by copy.
- Rewrite "never X" lines as "ask before X" where a person wants the final say; keep "never" for true hard lines.
- One owner per file. Changes to files another agent or person owns go in as proposed patches, not edits.
- Changes to public or shared repositories are drafts for the owner. The routine never merges or publishes them.

## Underuse review

1. **Inventory** the methods and skills the instructions promise (for example: fresh-context review, deep research, premise checks).
2. **Count usage** from logs: load events, run logs, artifacts the method produces. Give the count, the window, and the last use.
3. **Find misses.** For each underused method, name two or more concrete past moments where it should have fired, with the evidence (a review that shared the builder's context, a claim shipped without research).
4. **Propose a trigger rule** that fires on an observable condition, not on memory. Example pairing: run a context-rich draft and a fresh-context review (the elephant-and-goldfish pattern described at `github.com/google/elephant-goldfish-model`) whenever a deep-research report or a decision document is finished. The goldfish reads only the report and its sources and returns every claim it cannot verify.
5. **Check next week** whether the trigger fired. A trigger that never fires is itself a finding.

## Done when

- The dated report exists, and every file over 90% of a loader limit has a size plan.
- Every candidate has keep, retire, merge, or rewrite, with a reason.
- Every retirement has an archive entry with all four fields and a pointer.
- The underuse section names counts, misses, and one trigger rule per flagged method.

Related: `encode-corrections` (record decisions so later rules do not drift), `unattended-run-setup` (rules to check against), `context-check`.

See the [synthetic worked example](examples/worked.md).
