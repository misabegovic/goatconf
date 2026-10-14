"""The home page's generated parts and the shared top bar."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def test_renumber_runs_one_sequence():
    home = importlib.reload(importlib.import_module("home"))
    text = '<span class="num">7</span> <span class="num num--printed">2</span> <span class="num">9</span>'
    assert home.renumber(text) == '<span class="num">1</span> <span class="num num--printed">2</span> <span class="num">3</span>'


def test_days_follow_the_day_plan():
    home = importlib.reload(importlib.import_module("home"))
    program = importlib.import_module("program")
    html = home.days()
    for day, plan in program.DAY_PLAN.items():
        assert f'{plan["slots"][0]} to {plan["end"]}' in html
    assert "Saturday 5th June" in html


def test_top_bar_marks_the_current_page_and_replaces_itself():
    nav = importlib.reload(importlib.import_module("nav"))
    page = '<html><body>\n<svg width="0" height="0"><defs></defs></svg>\n<main id="main"></main></body></html>'
    once = nav.place(page, "speakers.html")
    assert '<a href="speakers.html" aria-current="page">Speakers</a>' in once
    assert once.count("<!-- topbar -->") == 1
    assert nav.place(once, "speakers.html") == once


def test_a_speaker_page_marks_speakers_and_nav_agrees(tmp_path, monkeypatch):
    nav = importlib.reload(importlib.import_module("nav"))
    assert nav.section("speaker-ana-example.html") == "speakers.html"
    assert nav.section("program.html") == "program.html"
    monkeypatch.setattr(nav, "SITE", tmp_path)
    page = '<html><body>\n<main id="main"></main></body></html>'
    (tmp_path / "speaker-ana-example.html").write_text(nav.place(page, "speakers.html"), encoding="utf-8")
    assert nav.main(["check"]) == 0


def test_top_bar_fits_a_body_with_attributes_and_names_a_page_without_one():
    nav = importlib.reload(importlib.import_module("nav"))
    page = '<html><body class="album">\n<main id="main"></main></body></html>'
    assert nav.place(page, "index.html").count("<!-- topbar -->") == 1
    try:
        nav.place("<html><main></main></html>", "index.html")
    except ValueError as err:
        assert "no <body>" in str(err)
    else:
        raise AssertionError("expected a ValueError")
