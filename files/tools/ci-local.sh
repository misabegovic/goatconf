#!/usr/bin/env bash
# tools/ci-local.sh: the brain's CI, run on this machine.
#
# The only CI goatconf has (organiser's decision, 2026-10-07,
# sources/conversations/2026-10-07--brain--local-ci-only.md). One GitHub
# Actions workflow only publishes the site, checked here by tools/pages.py
# (amended 2026-10-12, sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md).
# Inherited from claude-brain and extended with the rule checks in
# tools/ci_checks.py. tools/git-hooks/pre-push runs it before every push
# and refuses the push if any step fails; tools/setup-local.sh installs
# that hook.
#
# Usage: bash tools/ci-local.sh [--base REF]   (default base: origin/main)
set -uo pipefail

cd "$(dirname "$0")/.." || exit 2
PY="${PYTHON:-$HOME/.local/share/mempalace-venv/bin/python3}"
[ -x "$PY" ] || PY=python3
BASE="origin/main"
[ "${1:-}" = "--base" ] && BASE="${2:?--base needs a ref}"

failed=()
run() {
  local name="$1"; shift
  printf 'ci-local ▶ %s\n' "$name"
  if ! "$@"; then printf 'ci-local ✗ %s\n' "$name" >&2; failed+=("$name"); fi
}

git fetch -q origin 2>/dev/null || true

run "preflight (validate, citations, views)" bash tools/preflight.sh
run "Notion writes deny-listed" "$PY" tools/brain.py check-no-notion-writes
run "rules against $BASE (sources additive, confidence floor, no em dashes, no AI attribution)" "$PY" tools/ci_checks.py all --base "$BASE"
run "extensions (records valid, page current)" sh -c "\"$PY\" tools/extensions.py check && \"$PY\" tools/extensions.py build --check"
run "program (records valid, page current)" sh -c "\"$PY\" tools/program.py check && \"$PY\" tools/program.py build --check"
run "speakers and supporters (records valid, pages current)" sh -c "\"$PY\" tools/speakers.py check && \"$PY\" tools/speakers.py build --check"
run "brand files current" "$PY" tools/brand.py build --check
run "link previews current" "$PY" tools/meta.py check
run "top bar current" "$PY" tools/nav.py check
run "home page current" "$PY" tools/home.py build --check
run "travel page places current" "$PY" tools/places.py build --check
run "photos have their WebP copies, and pages use them" "$PY" tools/images.py check
run "agent files current (llms.txt, program.json, calendar, sitemap)" "$PY" tools/agents.py build --check
run "form links filled (every merge to main publishes)" "$PY" tools/formlinks.py check --publish
run "site form links current" "$PY" tools/formlinks.py check
run "only the publish workflow, unchanged" "$PY" tools/pages.py build --check
run "home page paired with wiki/ edits" "$PY" tools/brain.py check-home-fresh --base "$BASE"
run "README paired with significant changes" "$PY" tools/brain.py check-readme-fresh --base "$BASE"
if "$PY" -c "import pytest" 2>/dev/null; then
  run "pytest" "$PY" -m pytest tests/ -q
else
  run "pytest" uvx --with pyyaml --with tiktoken pytest tests/ -q
fi

if [ ${#failed[@]} -gt 0 ]; then
  printf '\nci-local ✗ %d step(s) failed: %s\n' "${#failed[@]}" "$(IFS=';'; echo "${failed[*]}")" >&2
  exit 1
fi
printf '\nci-local ✓ every step passed against %s\n' "$BASE"
