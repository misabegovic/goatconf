"""Goatchi installable, with reminders made on the device (ADR wiki/org/adrs/goatchi-full-game.md): the manifest keeps
the app to the Goatchi page, and the service worker reminds only about a goat whose player asked, when it sulks, once
a day."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import goatchi  # noqa: E402

SW = ROOT / "site" / "goatchi-sw.js"
H = 3600e3
NOW = 1_800_000_000_000


def test_the_app_is_the_goatchi_page_only():
    m = json.loads(goatchi.manifest())
    assert m["start_url"] == "goatchi.html" and m["scope"] == "goatchi"
    assert m["display"] == "standalone"
    assert any(i.get("purpose") == "maskable" for i in m["icons"])
    for src, *_ in goatchi.ICONS:
        assert any(i["src"] == src for i in m["icons"])


def test_the_page_links_its_manifest_and_hides_install_and_reminders_until_they_can_work():
    html = goatchi.page()
    assert '<link rel="manifest" href="goatchi.webmanifest">' in html
    assert '<p class="goatchi__install" hidden>' in html
    assert '<p class="goatchi__remind goatchi__mode" hidden>' in html


def test_no_other_page_registers_a_worker():
    pages = [p for p in (ROOT / "site").glob("*.js") if p.name not in ("goatchi.js", "goatchi-sw.js")]
    for p in pages:
        assert "serviceWorker" not in p.read_text(encoding="utf-8"), p.name


def goat(hours_ago=0.0, level=1.0, remind=True, challenge=False):
    then = NOW - hours_ago * H
    return {"name": "The pirate", "remind": remind, "challenge": challenge,
            "needs": {n: [level, then] for n in ("food", "play", "sleep")}}


CASES = {
    # name: (goat, last told, expected)
    "a happy goat": (goat(hours_ago=1), None, False),
    "a sulking goat": (goat(hours_ago=30), None, True),
    "a sulking goat, told an hour ago": (goat(hours_ago=30), NOW - 1 * H, False),
    "a sulking goat, told a day ago": (goat(hours_ago=30), NOW - 25 * H, True),
    "a sulking goat whose player turned reminders off": (goat(hours_ago=30, remind=False), None, False),
    "no goat at all": (None, None, False),
    "a challenge goat, sulking, still here": (goat(hours_ago=40, challenge=True), None, True),
    "a challenge goat that wandered off": (goat(hours_ago=24 * 6, challenge=True), None, False),
    "a goat left alone for a week, not in challenge mode": (goat(hours_ago=24 * 7), None, True),
}


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
@pytest.mark.parametrize("name", list(CASES))
def test_the_worker_reminds_only_when_it_should(name):
    g, told, want = CASES[name]
    script = (f"const sw = require({json.dumps(str(SW))});"
              f"process.stdout.write(JSON.stringify(sw.shouldRemind({json.dumps(g)}, {json.dumps(told)}, {NOW})));")
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True).stdout
    assert json.loads(out) is want, name


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_the_reminder_names_the_goat_and_warns_a_challenge_goat():
    script = (f"const sw = require({json.dumps(str(SW))});"
              f"process.stdout.write(JSON.stringify([sw.reminder({json.dumps(goat())}), sw.reminder({json.dumps(goat(challenge=True))})]));")
    plain, challenge = json.loads(subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True).stdout)
    assert plain["title"] == "The pirate is sulking"
    assert "hills" not in plain["body"] and "hills" in challenge["body"]
