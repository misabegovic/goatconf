#!/usr/bin/env bash
# tools/preflight.sh: the gates a push is held behind, run locally.
#
# Inherited from claude-brain's preflight on 2026-10-07 and cut to what a
# brain with no code cluster needs:
#   1. brain.py validate         frontmatter and required sections
#   2. citations                 `tabula check` if tabula is installed,
#                                `brain.py check --no-net` otherwise
#   3. views regen + diff        `tabula index` if installed, `brain.py views`
#                                otherwise; a drift in wiki/_views/ fails
#
# Called by tools/preflight-hook.sh before any `git push` / `gh pr create`,
# and by tools/ci-local.sh. Exits non-zero on the first failing gate.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || { echo "preflight: cannot resolve the brain root from $0" >&2; exit 64; }
cd "$ROOT" || exit 64
[ -f tools/brain.py ] || { echo "preflight: $ROOT does not look like a brain checkout (no tools/brain.py)" >&2; exit 64; }

PY=~/.local/share/mempalace-venv/bin/python3
[ -x "$PY" ] || PY=python3

step() { echo "preflight ▶ $*"; }
fail() { echo "preflight ✗ $*" >&2; exit 1; }

TB="${TABULA:-${TABULA_BIN:-$(command -v tabula || true)}}"

step "brain.py validate"
"$PY" tools/brain.py validate >/dev/null || fail "brain.py validate failed: fix frontmatter / required sections / references, then re-run."

# Determinism note (2026-10-08): preflight used to prefer a `tabula` binary
# on PATH over brain.py. The binary now on this machine's PATH is another
# organisation's build (its template text is baked in, e.g. "cross-Teamtailor"),
# so `tabula index` never reproduces the committed views and every push was
# refused. The committed views are brain.py-generated; preflight therefore
# pins the generator to this repo's own brain.py.
step "brain.py check --no-net"
"$PY" tools/brain.py check --no-net >/dev/null || fail "brain.py check --no-net failed: a sources: citation does not resolve."

step "brain.py views (regen + diff)"
"$PY" tools/brain.py views >/dev/null || fail "brain.py views errored."
if ! git diff --exit-code --quiet wiki/_views/; then
  echo "preflight ✗ wiki/_views/ regenerated to a new state: commit the diff before pushing." >&2
  exit 1
fi

echo "preflight ✓ all gates passed"
