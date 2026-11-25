# Chat replies that report on work

A public talk on how high-performing teams use coding agents ([YouTube, 21 Nov 2026](https://youtu.be/81Jg17dQz1A), lesson on making work faster to review) showed a four-part opening: what needs the reader, whether the goal was met, a short path, and what went wrong. The shape below keeps that order and keeps this collection's existing rules: a decision block with numbered options, bold NOT DONE / NOT CHECKED / FAILED labels with a reason, per-claim verdicts that are never pooled, and a three-pass layout for long write-ups.

The talk is not copied. The on-screen template is paraphrased here.

## Template

```
**Needs you:** none | <one-line ask>
**Done?** Yes | No | Partly — <the goal as stated, in one clause>
**How:** <1-2 lines: what was read or run, in order, and the key choice>
**Problems:** none | **NOT DONE:** ... because ... / **NOT CHECKED:** ... because ... / **FAILED:** ... because ...

<optional detail, or a path to a full write-up>
```

If a decision is needed, the bold decision block goes under **Needs you**, with numbered options and a recommended pick, and never after **Done?**.

Rules:

- The four labels always appear, in that order. `none` is allowed; omitting a label is not.
- **Done?** is the goal the reader asked for, not "a message was sent". A started background job is `No`.
- Every NOT DONE / NOT CHECKED / FAILED item has a `because`.
- The four lines together stay under about 80 words, and the whole message under about 200 words, unless a file path or page link holds the rest.
- Per-claim verdicts (verified, unverified, inference, failed) stay in the detail. Never pool them into one score.
- Quick acknowledgements ("On it") are exempt.

Run the checker on a draft:

```sh
python3 skills/bluf-notes/scripts/lint_output_style.py path/to/reply.md
```

It exits 1 when the labels are missing or out of order, when `Done?` does not start with Yes / No / Partly, when a problem item has no reason, when a decision block appears after `Done?`, or when a long reply has no write-up link.

## Example A: status update

> **Needs you:** none.
> **Done?** No. Hourly CI watch is running; main is green, but one scheduled job is red.
> **How:** Read the last 6 runs on `509eaeef6` via the host's CI page; compared the failed step against the 5 passing runs.
> **Problems:** **NOT CHECKED:** the run logs, because the log download needs a machine that is offline. **FAILED:** `metadata-analysis-batch` timed out at 30 min at spawn/collect (the timeout, verified from the run page; "flaky" is inference).
>
> Next check 12:30 PM PT. Details: `docs/ci-watch-latest.md`

## Example B: a decision sits first

> **Needs you:**
> ## DECISION NEEDED
> **Adopt the four-line reply style?**
> 1. **Yes, for all work replies.** Recommended.
> 2. Yes, but only for task reports.
> 3. No, keep the current style.
>
> **Done?** Yes. Compared the talk's four parts against the saved reply rules.
> **How:** Read the captions, checked the on-screen template, then checked each part against the current rules.
> **Problems:** **NOT CHECKED:** the speaker's downloadable toolkit, because it is behind an email sign-up form.
>
> Full write-up: `docs/output-style.md`

The checker looks for the exact heading DECISION NEEDED so it can reject a block that appears after **Done?**.
