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
    # name: (goat, last told, told it left, expected)
    "a happy goat": (goat(hours_ago=1), None, False, None),
    "a sulking goat": (goat(hours_ago=30), None, False, "need"),
    "a sulking goat, told an hour ago": (goat(hours_ago=30), NOW - 1 * H, False, None),
    "a sulking goat, told a day ago": (goat(hours_ago=30), NOW - 25 * H, False, "need"),
    "a sulking goat whose player turned reminders off": (goat(hours_ago=30, remind=False), None, False, None),
    "no goat at all": (None, None, False, None),
    "a challenge goat, sulking, still here": (goat(hours_ago=40, challenge=True), None, False, "need"),
    "a challenge goat that just wandered off": (goat(hours_ago=24 * 6, challenge=True), NOW - 1 * H, False, "left"),
    "a challenge goat that wandered off, already told": (goat(hours_ago=24 * 6, challenge=True), None, True, None),
    "a goat left alone for a week, not in challenge mode": (goat(hours_ago=24 * 7), None, False, "need"),
}


def node(expr: str):
    script = f"const sw = require({json.dumps(str(SW))}); process.stdout.write(JSON.stringify({expr}));"
    return json.loads(subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True).stdout)


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
@pytest.mark.parametrize("name", list(CASES))
def test_the_worker_reminds_only_when_it_should(name):
    g, told, gone, want = CASES[name]
    assert node(f"sw.remindOf({json.dumps(g)}, {json.dumps(told)}, {json.dumps(gone)}, {NOW})") == want, name


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_the_reminder_names_the_need_the_goat_lacks_most():
    hungry = goat(hours_ago=30)
    hungry["needs"]["play"] = [1, NOW - 2 * H]
    hungry["needs"]["sleep"] = [1, NOW - 2 * H]
    sleepy = goat(hours_ago=30)
    sleepy["needs"]["food"] = [1, NOW - 2 * H]
    sleepy["needs"]["play"] = [1, NOW - 2 * H]
    assert node(f"sw.reminder({json.dumps(hungry)}, 'need', {NOW})")["title"] == "The pirate is hungry"
    assert node(f"sw.reminder({json.dumps(sleepy)}, 'need', {NOW})")["title"] == "The pirate is sleepy"
    challenge = goat(hours_ago=30, challenge=True)
    assert "hills" in node(f"sw.reminder({json.dumps(challenge)}, 'need', {NOW})")["body"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_a_goat_that_wandered_off_is_told_once_with_its_days():
    g = goat(hours_ago=24 * 6, challenge=True)
    g["since"] = NOW - 24 * 9 * H
    note = node(f"sw.reminder({json.dumps(g)}, 'left', {NOW})")
    assert note["title"] == "The pirate went exploring"
    # every need ran out at 6 - 1.5 days ago, it left three days later: kept 9 - 1.5 = 7.5 days, so 7
    assert "kept it for 7 days" in note["body"]
