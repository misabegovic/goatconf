#!/usr/bin/env bash
# tools/setup-local.sh: one command from a fresh clone to working local CI.
#
# Checks the prerequisites, creates the venv, installs the git hooks (so
# every push runs tools/ci-local.sh), and ends by running the CI once so a
# fresh clone proves itself. goatconf has no remote CI; this is where it
# starts (sources/conversations/2026-10-07--brain--local-ci-only.md).
#
# What follows is inherited from claude-brain's script:
#
# Why this exists:
#   tools/preflight.sh and the PreToolUse hook in .claude/settings.json
#   look for python3 at ~/.local/share/mempalace-venv/bin/python3 and
#   fall back to system python3 when missing. The fallback works for
#   validate / check; the venv carries tiktoken and pytest as CI does,
#   so brain.py's token counts and the test suite agree with CI.
#
#   This script creates the venv and installs the deps validate.yml
#   uses (pyyaml + tiktoken + pytest), so local preflight and CI
#   converge.
#
# Idempotent: re-running re-installs the deps against the existing venv.
#
# Two installers, because the stdlib path is not always available. A
# uv-created venv ships without pip, and Debian/Ubuntu split ensurepip
# into python3-venv — so on a machine with uv and a stock python3, the
# pip path fails at both venv creation and dependency install while
# everything actually works fine. uv is preferred when present.
#
# Usage: tools/setup-local.sh

set -euo pipefail

VENV=~/.local/share/mempalace-venv
PY_SYS=${PYTHON:-python3}

echo "setup-local ▶ prerequisites"
missing=0
need() { if command -v "$1" >/dev/null 2>&1; then echo "  $1: ok"; else echo "  $1: missing ($2)" >&2; missing=1; fi; }
want() { if command -v "$1" >/dev/null 2>&1; then echo "  $1: ok"; else echo "  $1: not found ($2)"; fi; }
need git "required"
need "$PY_SYS" "required: Python 3.10 or newer"
want jq "optional: sharper matching in the push guard hook"
want npx "optional: impeccable's installer; the skill itself needs no Node"
want tabula "optional: when present, preflight uses tabula index and tabula check"
if command -v "$PY_SYS" >/dev/null 2>&1 && ! "$PY_SYS" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  echo "  $PY_SYS is older than 3.10" >&2; missing=1
fi
[ "$missing" = 0 ] || { echo "setup-local ✗ install the missing prerequisites, then re-run" >&2; exit 1; }
REQS="$(cd "$(dirname "$0")/.." && pwd)/requirements-dev.txt"

if command -v uv >/dev/null 2>&1; then
  INSTALLER=uv
elif command -v "$PY_SYS" >/dev/null 2>&1; then
  INSTALLER=pip
else
  echo "setup-local: neither uv nor $PY_SYS found on PATH" >&2
  exit 1
fi

echo "setup-local ▶ installer: $INSTALLER"

if [ "$INSTALLER" = pip ] && ! "$PY_SYS" -c 'import ensurepip' 2>/dev/null; then
  cat >&2 <<EOF
setup-local: $PY_SYS lacks ensurepip — venv creation will fail.

Either install uv (https://docs.astral.sh/uv/), which this script
prefers and which needs no system packages, or install the missing
Debian/Ubuntu package:
  sudo apt-get install -y python3-venv python3-pip

Then re-run: tools/setup-local.sh
EOF
  exit 1
fi

if [ ! -x "$VENV/bin/python3" ]; then
  echo "setup-local ▶ creating venv at $VENV"
  mkdir -p "$(dirname "$VENV")"
  if [ "$INSTALLER" = uv ]; then
    uv venv "$VENV"
  else
    "$PY_SYS" -m venv "$VENV"
  fi
else
  echo "setup-local ▶ venv exists at $VENV"
fi

VENV_PY="$VENV/bin/python3"

echo "setup-local ▶ installing from requirements-dev.txt"
if [ "$INSTALLER" = uv ]; then
  VIRTUAL_ENV="$VENV" uv pip install --quiet -r "$REQS"
else
  "$VENV_PY" -m pip install --quiet --upgrade pip
  "$VENV_PY" -m pip install --quiet -r "$REQS"
fi

echo "setup-local ▶ verifying tiktoken"
"$VENV_PY" -c 'import tiktoken; tiktoken.get_encoding("cl100k_base"); print("tiktoken OK", tiktoken.__version__)'

# Git hooks are committed to the repo but the install symlink is
# per-checkout, so nothing installed them and both guards sat inert
# in this clone until 2026-08-03 — including the LOCAL_FIRST
# promotion guard added after the 2026-07-31 unasked-push incident.
# Symlinked (not copied) so edits to tools/git-hooks/ flow into
# installed hooks without re-running setup.
echo "setup-local ▶ installing git hooks"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if HOOK_DIR="$(git -C "$ROOT" rev-parse --git-path hooks 2>/dev/null)"; then
  case "$HOOK_DIR" in /*) ;; *) HOOK_DIR="$ROOT/$HOOK_DIR" ;; esac
  mkdir -p "$HOOK_DIR"
  for hook in pre-commit pre-push; do
    src="$ROOT/tools/git-hooks/$hook"
    [ -e "$src" ] || continue
    dest="$HOOK_DIR/$hook"
    if [ -L "$dest" ] && [ "$(readlink -f "$dest")" = "$(readlink -f "$src")" ]; then
      echo "  $hook already installed"
    elif [ -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "  $hook: a non-symlink hook already exists — left alone, install by hand if intended" >&2
    else
      ln -sfn "$src" "$dest"
      echo "  $hook installed"
    fi
  done
else
  echo "  not a git checkout — skipping hook install" >&2
fi

echo "setup-local ▶ running local CI once"
cd "$ROOT"
git fetch -q origin main 2>/dev/null || true
if PYTHON="$VENV_PY" bash tools/ci-local.sh; then
  cat <<EOF

setup-local ✓ ready: hooks installed, local CI passes.

Every git push now runs tools/ci-local.sh first and is refused if it
fails. Run it by hand any time:

  bash tools/ci-local.sh

EOF
else
  echo "setup-local ✗ local CI failed on this clone; fix the step it named" >&2
  exit 1
fi
