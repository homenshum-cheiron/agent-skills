---
name: outcome-first-updates
description: "Use when writing a status, review request, or handoff, and when a message another person would read is about to be sent. Lead with the outcome, the evidence limit, and the next decision."
---

# Outcome-first updates

Tell the reader what changed and what they need to do, not how many agents were busy.

- Lead with the outcome, the blocker, or the explicit ask: the capability or decision the reader now has. For a small update, one or two sentences may be enough. Tests and docs can be real enabling outcomes; name them as enabling. They do not replace acceptance in use.
- Label each item verified, unproven, or not started, and point at the evidence. A running process is not a confirmed outcome. If part of the status is already known, say it and mark the rest as still being gathered. Do not copy an old status forward without re-checking the live source. If nothing material changed, say nothing.
- Name the actual artifact and state. Proposed, implemented locally, tested, in review, landed, deployed, and live-verified are different facts. Queued or running CI is not green. A passing check, a bot approval, and a human approval are different facts.
- Attribute people only with source-supported roles: owner, reviewer, participant, mentioned person, or unknown. An account name or a shared repository does not establish ownership.
- Include the shortest useful evidence link and revision. Explain what the checks prove and what remains untested. Do not inflate a sample into full coverage. Claim done only against the declared acceptance criteria, preferably actual use. A count of skills or checklist rows is not done.
- Make dependencies and the next decision visible, including who owns the next action. If work is stopped, say so rather than implying background progress.
- Fit the reader before you send. These rules come from repeated owner corrections:
  - Match the format and length the audience already uses there. If peers answer a stand-up thread with three one-line bullets, answer the same way, not with a long card.
  - Use plain words. Replace an internal label with a short description and one line of background, or drop it.
  - Give the full denominator, then the split: "40 sources tried: 12 working, 15 cut short, 13 failing", not a 12-source headline.
  - Skip what the reader already knows. Give the overall picture, then only what is new.
  - Look values up live. If a version, price, or status was not checked this time, write "not verified" with the last-known value and its date.
  - For a large sweep (disk, logs, traces, a pull-request list), say in two or three sentences how it was done and its caveats, such as truncation or a size filter.
  - For an owner who reads later, use a checklist: each open item has an owner and a next action. List the decisions needed separately, each with its options and the default if nobody answers.
- Humans send. Draft the recipient, the channel, and the full body, then stop. For a short ask, use a warm specific question, optional details, and two short bullets. A declined or blocked send is final. Do not retry it through another tool, script, or account. Loading this skill does not grant permission to send, tag, publish, or change pull-request state.

Use [the worked example](examples/worked.md). Match the recipient and channel rather than filling a template. This skill does not require a particular typography. A long answer that only needs scanning is a formatting pass, not a status.
