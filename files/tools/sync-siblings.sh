#!/usr/bin/env bash
# sync-siblings — fetch each sibling repo, list commits since the last
# brain ingest/mine line that named that repo. Output is read by /lint
# and /mine to decide what's worth re-ingesting.
#
# Usage: tools/sync-siblings.sh [repo1 repo2 ...]
#   No args = sweep every repo named in AGENTS.md's "Sibling repos" list.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$REPO_ROOT/log/log.md"
# brain.py reads BRAIN_PROJECTS_ROOT from the machine-local .env; this script
# did not, so on a machine whose root is set only there the sweep looked in
# ~/projects and reported every sibling as "not a git repo" (found
# 2026-09-21, the first time the sweep could run since the root moved).
if [[ -z "${BRAIN_PROJECTS_ROOT:-}" && -f "$REPO_ROOT/.env" ]]; then
  BRAIN_PROJECTS_ROOT="$(sed -n 's/^BRAIN_PROJECTS_ROOT=//p' "$REPO_ROOT/.env" | tail -1)"
fi
PROJECTS="${BRAIN_PROJECTS_ROOT:-$HOME/projects}"

# Default sibling list — read from AGENTS.md § Active scope, every row
# marked `active`. Derived rather than hardcoded: the list used to be a
# literal array here and fell out of date silently. It sat at eleven
# repos while active scope was thirteen, so two active repos were simply
# never swept, and nothing reported their absence: a sweep that skips a
# repo looks exactly like a sweep where that repo had no commits. Found
# 2026-08-03.
#
# Fails closed: if the table cannot be parsed the sweep aborts rather
# than quietly walking zero repos, because "no output" and "nothing
# changed" must not look alike.
agents_active_repos() {
  awk '
    /^###? *Active scope/      { inscope = 1; next }
    inscope && /^##[^#]/       { exit }
    inscope && /^\| *`[a-z0-9-]+` *\|/ {
      if ($0 ~ /\| *(\*\*)?active(\*\*)? *\|/) {
        line = $0
        sub(/^\| *`/, "", line)
        sub(/`.*$/, "", line)
        print line
      }
    }
  ' "$REPO_ROOT/AGENTS.md"
}

if [[ $# -gt 0 ]]; then
  SIBLINGS=("$@")
else
  mapfile -t SIBLINGS < <(agents_active_repos)
  if [[ ${#SIBLINGS[@]} -eq 0 ]]; then
    echo "sync-siblings: could not parse any active repo from" \
         "AGENTS.md § Active scope — refusing to sweep nothing." >&2
    exit 64
  fi
fi

# For each sibling, find the most recent log line that names it after
# a "mine —" or "ingest —" prefix. We want the date so we can ask git
# "what's happened since then." If we can't find one, fall back to 30d.
last_touch_date() {
  local repo="$1"
  local d
  d=$(grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2} (mine|ingest) — .*${repo}" "$LOG" \
        2>/dev/null | tail -n1 | awk '{print $1}' || true)
  if [[ -z "$d" ]]; then
    d=$(date -d '30 days ago' +%Y-%m-%d)
  fi
  echo "$d"
}

for repo in "${SIBLINGS[@]}"; do
  path="$PROJECTS/$repo"
  if [[ ! -d "$path/.git" ]]; then
    printf "%-22s  (skipped — not a git repo at %s)\n" "$repo" "$path"
    continue
  fi

  since=$(last_touch_date "$repo")

  # Fetch quietly. Don't fail the whole sweep if one repo's remote is
  # unreachable.
  if ! git -C "$path" fetch --quiet --all 2>/dev/null; then
    printf "%-22s  (fetch failed)\n" "$repo"
    continue
  fi

  # Per AGENTS.md § Sibling-repo handling — first step is to land on
  # main + pull latest, so the brain processes the canonical state.
  # *Unless* the repo has uncommitted changes (user is mid-work) or
  # is on a non-main / non-master branch (user is on a feature branch).
  # In that case, leave the working tree alone and report so the
  # operator knows the data may be stale relative to remote main.
  default=""
  for cand in main master; do
    if git -C "$path" show-ref --verify --quiet "refs/heads/$cand"; then
      default="$cand"
      break
    fi
  done
  if [[ -z "$default" ]]; then
    printf "%-22s  (no main/master branch)\n" "$repo"
    continue
  fi

  current=$(git -C "$path" symbolic-ref --short HEAD 2>/dev/null || echo "(detached)")
  dirty=$(git -C "$path" status --porcelain 2>/dev/null | head -n 1)

  if [[ "$current" != "$default" ]]; then
    printf "%-22s  (skipped main checkout — on '%s'; user work)\n" \
      "$repo" "$current"
  elif [[ -n "$dirty" ]]; then
    printf "%-22s  (skipped main pull — uncommitted changes)\n" "$repo"
  else
    if ! git -C "$path" pull --ff-only --quiet 2>/dev/null; then
      printf "%-22s  (pull --ff-only failed; not fast-forward?)\n" "$repo"
    fi
  fi

  # Count commits on the default branch's tracking branch since `since`.
  default_branch=$(git -C "$path" symbolic-ref --short HEAD 2>/dev/null || echo "main")
  upstream=$(git -C "$path" rev-parse --abbrev-ref "${default_branch}@{upstream}" 2>/dev/null || echo "$default_branch")

  count=$(git -C "$path" log --oneline --since="$since" "$upstream" 2>/dev/null | wc -l || echo 0)

  printf "%-22s  since %s on %-30s  %3d commits\n" \
    "$repo" "$since" "$upstream" "$count"

  if [[ "$count" -gt 0 ]]; then
    # -n 5 rather than `| head -n 5`: under `set -o pipefail` an early
    # head exit sends git SIGPIPE and the pipeline reports 141, which
    # aborts the script. It only fired when a repo had more than five
    # new commits, so it read as intermittent for as long as nobody
    # looked. Letting git do the limiting removes the pipe entirely.
    git -C "$path" log --since="$since" --oneline --abbrev-commit -n 5 "$upstream" 2>/dev/null \
      | sed 's/^/    /'
    if [[ "$count" -gt 5 ]]; then
      echo "    ... +$((count - 5)) more"
    fi
  fi
done
