# Worked example (synthetic)

## Notes card

Raw note: "lunch w/ vendor eng — cached agent + bash = weird edge cases, keep sep. also 99% cache reuse goal??"

Weak card: "Caching: keep bash separate (vendor). 99% reuse."

BLUF card:

- **Owner:** Priya, who is designing the agent rollout.
- **Situation:** Our coordinator agent keeps a long, cached prompt so later calls are cheaper. The rollout plan also lets it run shell commands.
- **Scenario:** Example: the coordinator writes scratch files while answering, and its job widens until odd failures appear mid-run.
- **Bottom line:** Put shell and file work in a separate sandboxed helper from the start.
- **Why it matters:** Impact unknown in dollars until cost per task is measured; the vendor's target was about 99% cache reuse.
- **Evidence:** Vendor engineer at lunch, as paraphrased in our notes.
- **Next step:** Priya writes the helper into the rollout design this week.
- **Confidence:** Inference. The advice is a paraphrase, and the design is a proposal.

## Engineering write-up

Headline: Fix the date parser in the literature-search client so one research query stops retrying every five minutes; needs one review.

Background:

- We already run research jobs through one in-house client, and we are not standing up a second job runner just for this source.
- One saved query keeps failing, and the retry loop has been waking a worker every five minutes.
- The parser treats a year-only publication date as invalid, so the job never records a success.

Items:

1. **The client retries forever when a result has a year-only publication date.**
   - **Cause:** `parse_published_on` in the client accepts only a full calendar date, then treats a parse miss as a transient error.
   - **Status:** fixed in this branch; see the new tests in `tests/test_parse_published_on.py`.
   - **Docs:** the source's public API documents year-only dates as valid. Link checked before posting.

Asks or to-dos:

- [ ] Reviewer confirms the parser accepts a year-only date and still rejects a truly malformed string.
- [ ] Maintainer ships after the unit tests above pass locally (`python3 -m unittest tests.test_parse_published_on`).

Out of scope / unverified: other date formats and the retry budget itself were not changed. Live traffic after deploy is unverified.

How it was tested: `python3 -m unittest tests.test_parse_published_on` exited 0. Risk if wrong: a malformed date could be stored instead of raising, so the tests include a reject case.
