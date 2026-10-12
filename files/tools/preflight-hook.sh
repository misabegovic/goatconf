#!/usr/bin/env bash
# tools/preflight-hook.sh — PreToolUse guard that runs tools/preflight.sh
# before a `git push` / `gh pr create` Bash call in a brain checkout.
#
# Wired from the PreToolUse.Bash matcher in .claude/settings.json. Reads
# the hook payload on stdin, exits 0 to allow the tool call and 2 to
# block it.
#
# Why this is a script and not a one-liner in settings.json: the inline
# version resolved the repo with `git rev-parse` against the *session*
# cwd, then skipped silently when the resulting tools/preflight.sh did
# not exist. A session rooted anywhere other than the brain checkout —
# ~/projects, say, which is not a git repo at all — therefore fell
# straight through the `if [ -x "$script" ]` guard and allowed every
# push unchecked. It failed open, and silently, which is the worst of
# both. Diagnosed 2026-08-03 after brain PR #620 pushed with a red
# `check --no-net`; the same symptom was recorded on PR #454 and
# misread as a fluke.
#
# Two rules follow from that:
#
#   1. Locate the brain by marker, not by cwd. Several candidates are
#      tried, including any `cd <path>` in the command itself, because
#      agents routinely write `cd ~/projects/brain && git push` from a
#      session rooted elsewhere.
#   2. Fail closed *once a brain checkout is identified*. A brain push
#      with an unusable preflight is blocked, not waved through. But a
#      push in some other repo is none of this hook's business, so an
#      unidentifiable target exits 0 — sibling repos have their own CI.
#
# Note preflight.sh mirrors only three of the CI gates (validate,
# check --no-net, views+diff). The PR-only gates — check-home-fresh,
# check-readme-fresh, check-no-notion-writes, pytest, ui-build — are
# not covered here and still need running before a PR. Passing this
# hook is not the same as green CI.

set -uo pipefail

payload=$(cat)
. "$(dirname "${BASH_SOURCE[0]}")/hooks/journal-block.sh"

cmd=""
sid=""
if command -v jq >/dev/null 2>&1; then
  cmd=$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null)
  sid=$(printf '%s' "$payload" | jq -r '.session_id // empty' 2>/dev/null)
fi
# jq absent or payload unparseable: fall back to matching the raw JSON,
# so a missing jq degrades to a coarser match rather than no guard.
[ -z "$cmd" ] && cmd="$payload"

case "$cmd" in
  *"git push"*|*"gh pr create"*) ;;
  *) exit 0 ;;
esac

is_brain() {
  [ -n "${1:-}" ] && [ -d "$1" ] && [ -f "$1/files/AGENTS.md" ] && [ -f "$1/files/tools/brain.py" ]
}

# Candidates in precedence order: an explicit BRAIN_DIR, any path the
# command cd's into, the cwd's repo, the session project dir, and a
# brain/ child of it (the ~/projects-rooted session layout).
candidates=()
[ -n "${BRAIN_DIR:-}" ] && candidates+=("$BRAIN_DIR")
cd_target=$(printf '%s' "$cmd" | sed -n 's/.*cd[[:space:]]\{1,\}\([^ &;|]*\).*/\1/p' | head -n 1)
if [ -n "$cd_target" ]; then
  case "$cd_target" in "~"*) cd_target="$HOME${cd_target#\~}" ;; esac
  candidates+=("$cd_target")
fi
toplevel=$(git rev-parse --show-toplevel 2>/dev/null) && candidates+=("$toplevel")
[ -n "${CLAUDE_PROJECT_DIR:-}" ] && candidates+=("$CLAUDE_PROJECT_DIR" "$CLAUDE_PROJECT_DIR/brain")

root=""
for c in "${candidates[@]+"${candidates[@]}"}"; do
  if is_brain "$c"; then root="$c"; break; fi
done

# Not a brain push — not this hook's call to make.
[ -z "$root" ] && exit 0

script="$root/files/tools/preflight.sh"
if [ ! -x "$script" ]; then
  journal_block "$root" "$sid" preflight "no runnable files/tools/preflight.sh at $root"
  cat >&2 <<EOF

✗ Blocked: brain checkout at $root has no runnable files/tools/preflight.sh.

  This hook fails closed on purpose: an unusable preflight used to be
  indistinguishable from a passing one. Restore the script (or run
  files/tools/setup-local.sh) before pushing.

EOF
  exit 2
fi

if ! "$script" >&2; then
  journal_block "$root" "$sid" preflight "files/tools/preflight.sh failed for $root"
  cat >&2 <<EOF

✗ Blocked: files/tools/preflight.sh failed for $root.

  Fix the gate it named, then retry. Remember preflight covers only
  validate / check --no-net / views: the PR-only gates
  (check-home-fresh --base origin/main, check-readme-fresh, pytest,
  ui-build) still need running separately.

EOF
  exit 2
fi

exit 0
