# Loading owner-routed-brief on each host

The folder follows the open Agent Skills layout: a `SKILL.md` with `name` and `description` frontmatter, plus `references/`, `examples/` and `scripts/`. Hosts that read that layout load it as is. For a host that only reads always-on rules, paste [PORTABLE.md](PORTABLE.md) into its rules file or system prompt instead. Paths below were read from each host's public docs on 17 Nov 2026; re-check them after a host update.

| Host | Where the folder goes | How to call it | Status |
|---|---|---|---|
| Claude Code | `~/.claude/skills/owner-routed-brief/` (personal) or `<repo>/.claude/skills/` (project) | Ask for an owner-routed brief, or `/owner-routed-brief` | verified (Claude Code skills docs) |
| Codex CLI and IDE | `~/.agents/skills/owner-routed-brief/` or `<repo>/.agents/skills/`. `~/.codex/skills/` still loads but is the legacy path | `$owner-routed-brief` or `/skills` | verified (Codex "Build skills" docs and loader source) |
| Cursor | `~/.cursor/skills/` or `~/.agents/skills/` (personal); `<repo>/.cursor/skills/` or `<repo>/.agents/skills/` (project) | Mention the skill or let the agent match the description | verified (Cursor Agent Skills docs) |
| Grok Bot | Save it as a user skill from this folder's `SKILL.md` body | `/owner-routed-brief` in chat, or name it in a routine | verified for the bot's own skill store; helper files must sit on the bot's machine or be pasted |
| Hermes Agent | `~/.hermes/skills/<category>/owner-routed-brief/`, or add `~/.agents/skills` under `skills.external_dirs` in `~/.hermes/config.yaml`. Project `.agents/skills` loads only for trusted project dirs | Natural request or slash command | verified (Hermes skills docs) |
| OpenClaw | `<workspace>/skills/`, `<project>/.agents/skills/`, `~/.agents/skills/` or `~/.openclaw/skills/` | `/owner-routed-brief`; check with `openclaw skills list` | verified (OpenClaw skills docs). Its docs ask for a one-line description under 160 characters, so this description may be shortened in its picker |
| Devin | `<repo>/.agents/skills/owner-routed-brief/`, or install the repo as a skills-only plugin | `@skills:owner-routed-brief` | verified (Devin AGENTS.md, playbooks-to-skills and release notes) |
| Google Antigravity | Project skills: `<workspace>/.agents/skills/`. User skills: the `skills` directory under the Gemini configuration folder in the home directory (the path the Antigravity docs give). The Antigravity App, CLI, and IDE discover installed skills from that folder. This skill does not open that folder, does not read host configuration, and must not print secrets. One level deep only | `/owner-routed-brief` or description match | verified (Antigravity skills and customization-discovery docs) |
| DeepSeek Harness (`dsh`) | `<repo>/.dsh/skills/` or `<repo>/.agents/skills/`. One level deep only | `/owner-routed-brief`; the model loads it with its skill tool | verified from the project's GitHub docs; not run |
| Muse Code | `<repo>/.agents/skills/owner-routed-brief/`; check with `muse skills validate` | Description match | verified from Muse Code SDK docs; not run. Another product named Muse was not checked: unverified |
| Any other agent that reads `AGENTS.md` | Put a pointer in `AGENTS.md`: "For daily or nightly owner briefs, read `.agents/skills/owner-routed-brief/SKILL.md` and follow it." | Ask for the brief | fallback |
| A chat model with no file access | Paste `PORTABLE.md` as the system prompt, then paste the day's sources | Ask for the brief | fallback |

Notes:
- "Verified" means the documented path was read. It does not mean this skill was run on that host. Only the eval-scorecard script has tests.
- Every path in the table is a host skill-install location for the operator. This skill does not read those folders, does not open agent configuration directories, and must not print secrets or credentials.
- The config file holds names and sources. Each host binds its own connectors; never copy tokens or connector configs between hosts.
- Hosts that scan one level deep need the folder directly under `skills/`, not inside a category folder.
