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



def test_days_link_to_the_program_open_the_evenings_and_list_what_people_add(monkeypatch):
    import datetime as dt
    home = importlib.reload(importlib.import_module("home"))
    program = importlib.import_module("program")
    thu, wed, sat, later = dt.date(2027, 6, 3), dt.date(2027, 6, 2), dt.date(2027, 6, 5), dt.date(2027, 6, 9)
    ext = {thu: [(dt.datetime(2027, 6, 3, 19, 0), "ruby", {"name": "Ruby & beer"}, "")],
           wed: [(dt.datetime(2027, 6, 2, 18, 30), "before", {"name": "The night before"}, "")],
           sat: [(dt.datetime(2027, 6, 5), "hike", {"name": "Salt lake hike"}, "")],
           later: [(dt.datetime(2027, 6, 9), "late", {"name": "Too late"}, "")]}
    monkeypatch.setattr(program, "extension_days", lambda: ext)
    html = home.days()
    for day in (*program.DAY_PLAN, sat):
        assert f'href="program.html#{day.isoformat()}"' in html
    assert html.count(home.EVENING) == len(program.DAY_PLAN)
    assert "Hours off: the cafés on Freedom Square and lunch in town." in html
    assert '<small class="day__added">Added: Ruby &amp; beer, 19:00</small>' in html
    assert '<small class="day__added">Added: Salt lake hike</small>' in html
    assert html.index("The night before") > html.index('href="add.html"')
    assert "Too late" not in html

def test_top_bar_marks_the_current_page_and_replaces_itself():
    nav = importlib.reload(importlib.import_module("nav"))
    page = '<html><body>\n<svg width="0" height="0"><defs></defs></svg>\n<main id="main"></main></body></html>'
    once = nav.place(page, "speakers.html")
    assert '<a href="speakers.html" aria-current="page">Speakers</a>' in once
    assert once.count("<!-- gen:topbar tools/nav.py -->") == 1
    assert nav.place(once, "speakers.html") == once


def test_a_speaker_page_marks_speakers_and_nav_agrees(tmp_path, monkeypatch):
    nav = importlib.reload(importlib.import_module("nav"))
    assert nav.section("speaker-ana-example.html") == "speakers.html"
    assert nav.section("program.html") == "program.html"
    assert nav.section("event-rust-night.html") == "program.html"
    assert nav.section("session-salt-goats-and-servers.html") == "program.html"
    monkeypatch.setattr(nav, "SITE", tmp_path)
    page = '<html><body>\n<main id="main"></main></body></html>'
    (tmp_path / "speaker-ana-example.html").write_text(nav.place(page, "speakers.html"), encoding="utf-8")
    assert nav.main(["check"]) == 0


def test_top_bar_fits_a_body_with_attributes_and_names_a_page_without_one():
    nav = importlib.reload(importlib.import_module("nav"))
    page = '<html><body class="album">\n<main id="main"></main></body></html>'
    assert nav.place(page, "index.html").count("<!-- gen:topbar tools/nav.py -->") == 1
    try:
        nav.place("<html><main></main></html>", "index.html")
    except ValueError as err:
        assert "no <body>" in str(err)
    else:
        raise AssertionError("expected a ValueError")


def test_home_plans_eight_places_and_invites_proposals_for_the_open_ones(monkeypatch):
    home = importlib.reload(importlib.import_module("home"))
    speakers = importlib.import_module("speakers")
    def people(n):
        return {f"s{i}": ({"name": f"Speaker {i}", "order": i + 1}, "Bio.") for i in range(n)}
    monkeypatch.setattr(speakers, "speakers", lambda: people(6))
    html = home.speakers_block()
    assert html.count("sticker--speaker") == 6 and html.count("slot--open") == 2
    assert html.count('href="talk.html"') == 2 and "Meet the speakers" in html
    monkeypatch.setattr(speakers, "speakers", lambda: people(9))
    html = home.speakers_block()
    assert html.count("sticker--speaker") == 8 and "slot--open" not in html and "All 9 speakers" in html
    monkeypatch.setattr(speakers, "speakers", lambda: {})
    assert "The first speaker could be you" in home.speakers_block()


def test_accepted_events_sit_above_kinds_that_all_stay_open(monkeypatch):
    import datetime as dt
    home = importlib.reload(importlib.import_module("home"))
    extensions = importlib.import_module("extensions")
    meetup = {"name": "BH Professionals Meetup", "kind": "meetup", "host": "BHFF", "start": "2027-06-05 18:00", "end": "2027-06-05 21:00"}
    second = dict(meetup, name="Rust meetup", host="Rustaceans", start="2027-06-04 19:00", end="2027-06-04 21:00")
    monkeypatch.setattr(extensions, "accepted", lambda: [(dt.datetime(2027, 6, 4, 19), "rust-meetup", second, ""),
                                                         (dt.datetime(2027, 6, 5, 18), "bh-professionals-meetup", meetup, "")])
    html = home.kinds_block()
    assert html.index("Accepted so far") < html.index("Rust meetup") < html.index("BH Professionals Meetup") < html.index('class="slots slots--kinds"')
    assert 'href="event-bh-professionals-meetup.html"' in html and 'href="event-rust-meetup.html"' in html
    assert html.count('<span class="stamp">Yours?</span>') == len(home.HOME_KINDS)
    assert "More than one of each is welcome" in html
    monkeypatch.setattr(extensions, "accepted", lambda: [])
    assert "Accepted so far" not in home.kinds_block()


def test_the_follow_links_sit_in_every_footer_and_in_marked_spots_once():
    nav = importlib.reload(importlib.import_module("nav"))
    page = ('<html><body>\n<main id="main"><!-- gen:follow tools/nav.py --><!-- /gen:follow --></main>\n'
            '<footer class="footer">\n  <p class="footer__links"><a href="index.html">Home</a></p>\n</footer></body></html>')
    once = nav.place(page, "contact.html")
    assert once.count('<p class="follow">') == 2  # the marked spot and the footer
    assert '<a class="follow__link" href="https://www.linkedin.com/company/goatconf/">' in once
    assert '<a class="follow__link" href="https://x.com/goatconf">' in once and 'aria-hidden="true"' in once
    assert once.index('class="footer__links"') < once.rindex('<p class="follow">') < once.index("</footer>")
    assert nav.place(once, "contact.html") == once
