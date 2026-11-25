# Brief: add a four-line reply checker

## Job

Add a checker that can fail a work reply which is missing the four opening labels, buries a decision, or has a problem line with no reason, and document the style next to the existing notes skill.

## Why

Reviewers read top-down. A decision or a missed failure that sits at the end of a long reply is easy to skip. A checker that can fail makes the style enforceable, not just described.

## Guardrails

- Do not push to a public remote, because publication needs an explicit later yes.
- Use only invented examples, because a public skill must not carry private meeting text.
- Do not rewrite unrelated skills, because the change should be reviewable on its own.

## Done means

- [ ] `python3 skills/bluf-notes/scripts/lint_output_style.py` exits 0 on the two examples in `references/chat-replies.md` and exits 1 on a reply that puts a decision after Done? or drops a because.
- [ ] `python3 scripts/validate_repo.py` exits 0.
- [ ] `python3 -m unittest discover -s tests` exits 0.
