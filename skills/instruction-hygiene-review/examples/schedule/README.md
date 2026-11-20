# Optional weekly schedule examples

These files are examples for an operator who already decided to run the offline instruction scan on a weekly schedule. This skill does not install a cron job, a LaunchAgent, or any other persistence mechanism, and it does not write to the home directory by itself.

- `weekly-scan.crontab` is a sample crontab line. Install it only after you review the command, change `AGENT_SKILLS_DIR` to your clone, and edit your own crontab.
- `weekly-scan.launchd.plist` is a sample macOS LaunchAgent. Copy it into your LaunchAgents folder and load it with `launchctl` only after you review the program arguments and set the clone path (launchd does not expand `$HOME` in EnvironmentVariables, so the sample wraps the path in `/bin/sh`).

The scanner's default report directory is `~/.local/state/instruction-hygiene`. That path is only an output folder for dated Markdown and JSON reports, created when you run the scanner, and you can point it somewhere else with `--out` or `INSTRUCTION_SCAN_OUT`. It is not a hidden agent, login item, or keepalive.

Do not enable either example without explicit user consent.
