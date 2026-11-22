#!/usr/bin/env bash
# The browser check for the sections that open and close (tests/browser/folds.mjs), in one command:
# serves site/ on a free port, starts the Chrome that tools/brand.py finds, headless, runs the check
# and stops both by their process ids. It needs Node 22 or later and a Chrome, which the local CI does
# not, so it is run by hand before shipping a change to the folds:
#
#   bash tools/check-folds.sh
set -u
cd "$(dirname "$0")/.."
PY="${PYTHON:-$HOME/.local/share/mempalace-venv/bin/python3}"
[ -x "$PY" ] || PY=python3
command -v node >/dev/null || { echo "check-folds: skipped, no node on the path"; exit 3; }
CHROME="$("$PY" -c "import sys; sys.path.insert(0, 'tools'); import brand; print(brand.chrome() or '')" 2>/dev/null)"
[ -n "$CHROME" ] || { echo "check-folds: skipped, no Chrome found"; exit 3; }
read -r SITE_PORT CHROME_PORT < <("$PY" -c "
import socket
s = [socket.socket() for _ in range(2)]
[x.bind(('127.0.0.1', 0)) for x in s]
print(*[x.getsockname()[1] for x in s])")
PROFILE="$(mktemp -d)"
"$PY" -m http.server "$SITE_PORT" --bind 127.0.0.1 --directory site >/dev/null 2>&1 &
SERVER=$!
"$CHROME" --headless=new --no-first-run --disable-gpu --remote-debugging-port="$CHROME_PORT" --user-data-dir="$PROFILE" about:blank >/dev/null 2>&1 &
BROWSER=$!
trap 'kill "$SERVER" "$BROWSER" 2>/dev/null; wait "$SERVER" "$BROWSER" 2>/dev/null; rm -rf "$PROFILE"' EXIT
WS=""
for _ in $(seq 1 50); do
  WS="$("$PY" -c "
import json, urllib.request
print(json.load(urllib.request.urlopen('http://127.0.0.1:$CHROME_PORT/json/version', timeout=1))['webSocketDebuggerUrl'])" 2>/dev/null)"
  [ -n "$WS" ] && break
  "$PY" -c "import time; time.sleep(0.2)"
done
[ -n "$WS" ] || { echo "check-folds: the browser did not start"; exit 1; }
node tests/browser/folds.mjs "$WS" "http://127.0.0.1:$SITE_PORT"
