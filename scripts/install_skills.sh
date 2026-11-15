#!/bin/sh
# Link (or copy) skill folders from this repository into the skill folders your hosts read.
# Dry run by default: it prints the plan and changes nothing until you pass --apply.
# It never overwrites an existing folder or file; it only creates links or copies that are missing,
# and --remove deletes only links that point back into this repository.
#
# Usage: scripts/install_skills.sh [--apply] [--copy] [--remove] [--host NAME]... [--skill NAME]...
#   --host     claude | codex | cursor | agents (repeatable). Default: every host whose
#              parent folder already exists (for example ~/.claude for claude).
#   --skill    one skill folder name (repeatable). Default: all skills in skills/.
#   --copy     copy folders instead of symlinking (use on hosts that do not follow links).
#   --remove   remove links this script created (links into this repository only).
# Target folders (override any of them):
#   CLAUDE_SKILLS_DIR  default $HOME/.claude/skills
#   CODEX_SKILLS_DIR   default ${CODEX_HOME:-$HOME/.codex}/skills
#   CURSOR_SKILLS_DIR  default $HOME/.cursor/skills
#   AGENTS_SKILLS_DIR  default $HOME/.agents/skills   (shared folder some hosts also read)
# Check your host version's documentation for the folder it reads; folders change between releases.
set -eu
REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
APPLY=0; COPY=0; REMOVE=0; HOSTS=""; SKILLS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --copy) COPY=1 ;;
    --remove) REMOVE=1 ;;
    --host|--skill)
      [ $# -ge 2 ] || { echo "$1 needs a value" >&2; exit 2; }
      if [ "$1" = --host ]; then HOSTS="$HOSTS $2"; else SKILLS="$SKILLS $2"; fi
      shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
target_for() {
  case "$1" in
    claude) echo "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}" ;;
    codex) echo "${CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}" ;;
    cursor) echo "${CURSOR_SKILLS_DIR:-$HOME/.cursor/skills}" ;;
    agents) echo "${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}" ;;
    *) echo "unknown host: $1" >&2; exit 2 ;;
  esac
}
if [ -z "$HOSTS" ]; then
  for h in claude codex cursor agents; do
    t=$(target_for "$h")
    [ -d "$(dirname -- "$t")" ] && HOSTS="$HOSTS $h"
  done
fi
[ -n "$HOSTS" ] || { echo "no host folders found; pass --host or set *_SKILLS_DIR" >&2; exit 1; }
if [ -z "$SKILLS" ]; then
  for d in "$REPO"/skills/*/; do [ -f "$d/SKILL.md" ] && SKILLS="$SKILLS $(basename -- "$d")"; done
fi
[ $APPLY -eq 1 ] || echo "Dry run. Re-run with --apply to make these changes."
for h in $HOSTS; do
  t=$(target_for "$h")
  for s in $SKILLS; do
    case "$s" in */*|.*|"") echo "skip $s: not a plain skill name" >&2; continue ;; esac
    src="$REPO/skills/$s"; dst="$t/$s"
    [ -f "$src/SKILL.md" ] || { echo "skip $s: not a skill in this repository" >&2; continue; }
    if [ $REMOVE -eq 1 ]; then
      if [ -L "$dst" ] && [ "$(readlink -- "$dst")" = "$src" ]; then
        echo "remove link $dst"
        if [ $APPLY -eq 1 ]; then rm -- "$dst"; fi
      fi
      continue
    fi
    if [ -L "$dst" ] && [ "$(readlink -- "$dst")" = "$src" ]; then echo "ok   $dst"; continue; fi
    if [ -e "$dst" ] || [ -L "$dst" ]; then echo "keep $dst (already exists; not touched)"; continue; fi
    if [ $COPY -eq 1 ]; then echo "copy $src -> $dst"; else echo "link $dst -> $src"; fi
    if [ $APPLY -eq 1 ]; then
      mkdir -p -- "$t"
      if [ $COPY -eq 1 ]; then cp -R -- "$src" "$dst"; else ln -s -- "$src" "$dst"; fi
    fi
  done
done
