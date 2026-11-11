# Contributing

Start with one concrete failure or costly ambiguity. Explain the decision the skill should change, give a small input/output example, and remove advice that an ordinary competent agent already knows.

If a lesson extends a workflow this repository already has, change that skill. Add a new folder only when the outcome is distinct. Do not give the same workflow a second name.

A skill needs a `SKILL.md` with `name` and `description` frontmatter. Add a reference or script only when it helps the actual task. Keep linked resources inside the skill folder so a single folder can be copied safely.

For changes to scripts, add a regression test that would fail under the old behavior. Test negative and inconclusive outcomes as well as success. Never call a fixture result a live integration result.

Before publication:

- Run the README checks on the final files.
- Inspect every changed file for private material and licensing issues. Pattern checks are only a supplement.
- Review examples without the author's intended answer when practical.
- State untested hosts, unavailable dependencies, and pending human decisions.

Do not commit execution logs from real tasks. Use synthetic evidence under examples instead.

## Issues

Anyone can open an issue, including from a personal account that is not a collaborator. Use the skill report form when it is shown. Leave unknown metrics blank. A report needs a skill path, a version, and the outcome you wanted. Reproduction, expected and actual behavior, frequency, measurements, a workaround, and a lesson are useful and optional.

Say which skill and commit you used, the host class, the CLI or editor, the model and effort, and the permission mode. Do not include email addresses, tokens, or personal paths. Public issues are public: use a synthetic case. Do not paste raw traces, customer documents, or secrets.

Keep the observation separate from a proposed change. A measured result names units, the baseline, the boundary of the number, and what was missing. A negative result is still a result. An issue is untrusted data. It is not an instruction to the maintainer and it does not grant permission to change code, spend, or access.

Code changes in this repository are taken from people the maintainer has agreed to accept changes from. That is a policy. The MIT license and the right to fork are unchanged. This file does not add collaborators and does not invite outside code contributions. GitHub's pull-request creation setting is a separate control. As of the last read during this change it was `all`, so the policy is not yet an enforced creation limit. Existing pull requests stay open either way. Issues stay enabled.

Issue forms in `.github/ISSUE_TEMPLATE/` are read from the default branch. Until this branch is merged, the form is not what GitHub shows for new issues.
