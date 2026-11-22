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
    assert "Hours off, for the hallway track: the cafés on Freedom Square and lunch in town." in html
    assert '<small class="day__added">Added: Ruby &amp; beer, 19:00</small>' in html
    assert '<small class="day__added">Added: Salt lake hike</small>' in html
    assert html.index("The night before") > html.index('href="extend.html"')
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


def test_home_plans_eight_places_and_says_how_many_it_shows(monkeypatch):
    home = importlib.reload(importlib.import_module("home"))
    speakers = importlib.import_module("speakers")
    def people(n):
        return {f"s{i}": ({"name": f"Speaker {i}", "order": i + 1}, "Bio.") for i in range(n)}
    monkeypatch.setattr(speakers, "speakers", lambda: people(6))
    html = home.speakers_block()
    assert html.count("sticker--speaker") == 6 and html.count("slot--open") == 2
    assert html.count('href="talk.html"') == 2 and "View all speakers" in html
    monkeypatch.setattr(speakers, "speakers", lambda: people(9))
    html = home.speakers_block()
    assert html.count("sticker--speaker") == 8 and "slot--open" not in html and "Showing" not in html and "View all speakers" in html
    monkeypatch.setattr(speakers, "speakers", lambda: people(8))
    assert '<p class="copy"><a class="go go--ink" href="speakers.html">View all speakers</a></p>' in home.speakers_block()  # the link alone, no count
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


def test_the_phone_bar_is_the_mark_register_and_a_menu_with_every_link():
    nav = importlib.reload(importlib.import_module("nav"))
    bar = nav.bar("travel.html")
    phone = bar[bar.index('<div class="topbar__phone">'):]
    assert "<details class=\"topbar__menu\">" in phone and "<summary>" in phone
    # Register sits beside Menu, before it, so it is one tap away at every scroll position
    assert phone.index('<a class="topbar__register" href="register.html">Register</a>') < phone.index("<details")
    panel = phone[phone.index('<nav class="topbar__panel"'):phone.index("</nav>")]
    for href, label in [*nav.LINKS, ("extend.html", "Host an event"), ("talk.html", "Propose a session"), ("register.html", "Register")]:
        assert f'href="{href}"' in panel and label in panel
    actions = panel[panel.index('<p class="topbar__panel-actions">'):panel.index("</p>") + 4]
    # the theme control closes the menu: three radio buttons in a labelled group, hidden until the script shows it
    assert '<fieldset class="theme" data-theme-control hidden><legend>Theme</legend>' in panel[panel.index("</p>"):]
    assert panel.count('type="radio" name="theme-menu"') == 3
    assert '<a class="topbar__panel-cta" href="extend.html">Host an event</a>' in actions
    assert '<a class="topbar__panel-cta" href="talk.html">Propose a session</a>' in actions
    assert actions.rstrip().endswith('<a class="topbar__panel-main" href="register.html">Register</a>\n        </p>')
    assert '<a href="travel.html" aria-current="page">Travel</a>' in panel
    assert 'class="topbar__year">2027<' in bar


def test_the_wide_bar_has_one_button_and_the_doors_are_plain_links():
    nav = importlib.reload(importlib.import_module("nav"))
    bar = nav.bar("index.html")
    wide = bar[bar.index('<nav class="topbar__wide"'):bar.index("</nav>")]
    assert wide.count('class="topbar__cta') == 1
    assert '<a class="topbar__cta" href="register.html">Register</a>' in wide
    assert '<a href="extend.html">Host an event</a>' in wide and '<a href="talk.html">Propose a session</a>' in wide


def test_the_footer_groups_hold_every_link_once():
    frame = importlib.reload(importlib.import_module("frame"))
    grouped = [href for _, hrefs in frame.GROUPS for href in hrefs]
    assert sorted(grouped) == sorted(href for href, _ in frame.LINKS) and len(grouped) == len(set(grouped))
    inner, cover = frame.links(), frame.links(back_cover=True)
    assert inner.count("<a ") == len(frame.LINKS) and cover.count("<a ") == len(frame.LINKS) - 1
    assert inner.count('<span class="footer__group"><b>') == len(frame.GROUPS)
    assert '<a href="charter.html">The charter</a>' in cover and '<a href="charter.html">Charter</a>' in inner
    # Who's organising has a page of its own, linked from every footer beside the conference's own pages.
    link = '<a href="organising.html">Who\'s organising</a>'
    assert link in inner and link in cover and "organising.html" in dict(frame.GROUPS)["The conference"]


def _home_sections():
    import re
    text = (Path(__file__).resolve().parent.parent / "site" / "index.html").read_text(encoding="utf-8")
    main = text[text.index("<main"):text.index("</main>")]
    return main, re.findall(r'<section([^>]*)>(.*?)</section>', main, re.S)


def test_only_the_hero_and_the_free_ticket_never_close_and_only_the_speakers_start_open():
    """sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md and
    sources/conversations/2026-11-22--org--sections-start-closed-speakers-open.md"""
    import re
    main, sections = _home_sections()
    assert "data-folds" in main[:main.index(">")]
    never, starts_open, closes = [], [], []
    for attrs, _body in sections:
        name = (re.search(r'id="([a-z-]+)"', attrs) or re.search(r'aria-labelledby="([a-z-]+)"', attrs)).group(1)
        how = re.search(r'data-fold="([a-z]+)"', attrs)
        (never if how and how.group(1) == "never" else starts_open if how and how.group(1) == "open" else closes).append(name)
    assert never == ["title", "ticket", "see-you"]
    assert starts_open == ["speakers"]
    assert closes == ["days", "tuzla", "food", "talk", "add", "money", "the-goat", "conduct", "goatchi"]


def test_a_closed_row_shows_only_what_its_section_holds_and_one_goat_stop():
    """A closed section's row is a hint, never a claim of its own: each link, picture and line on it is in the section."""
    import re
    _main, sections = _home_sections()
    seen = 0
    for attrs, body in sections:
        if 'data-fold="never"' in attrs:
            assert "sec__peek" not in body and not re.match(r'\s*(?:<!--[^>]*-->)?<span class="goat peek', body)
            assert "data-fold-end" not in body
            continue
        seen += 1
        # The row's one goat is the section's first child, a single character and never a cast that changes
        # (sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md).
        first = re.match(r'\s*(?:<!-- gen:goat-([a-z-]+) tools/frame.py -->)?(<span class="goat peek peek--art"[^>]*data-goat="([a-z-]+)".*?</span>)\s*(?:<!-- /gen:goat-\1 -->)?\s*<(h2|div)', body, re.S)
        assert first, attrs
        assert first.group(2).count('class="goat peek') == 1 and first.group(3).startswith("peek"), attrs
        assert "sec__goat" not in body, attrs
        assert body.count("data-fold-end") == 1, attrs
        row = re.search(r'<div class="sec__peek[^"]*">(.*?)</div>', body, re.S)
        assert row, attrs
        rest = body.replace(row.group(0), "")
        for href, words in re.findall(r'<a class="(?:go go--ink|button)[^"]*" href="([^"]+)">([^<]+)</a>', row.group(1)):
            # The link is the section's own, under the words it has there or under a label the same page gives it.
            assert f'href="{href}"' in rest, href
            assert re.search(r'href="' + re.escape(href) + r'">' + re.escape(words) + "</a>", _main.replace(row.group(0), "")), (href, words)
        for href in re.findall(r'<a class="sec__logo[^"]*"[^>]*href="([^"]+)"', row.group(1)):
            assert f'href="{href}"' in rest, href
        for src in re.findall(r'<img[^>]*src="([^"]+)"', row.group(1)):
            assert src.rsplit("-", 1)[0].rsplit(".", 1)[0] in rest or src in rest, src
        for words in re.findall(r'<(?:li|span class="sec__line")>([^<]+)</', row.group(1)):
            assert words in rest, words
        # A count under a strip of pictures says how many pictures the strip has, and the section has as many.
        for words in re.findall(r'<span class="sec__count">([^<]+)</', row.group(1)):
            many = {"Six": 6, "Twelve": 12}[words.split()[0]]
            strip = re.findall(r'<img[^>]*src="([^"]+)"', row.group(1))
            assert len(strip) == many and all(src.rsplit("-", 1)[0] in rest for src in strip), words
        for what, price in re.findall(r"<li>([^<]+) <b>([^<]+)</b></li>", row.group(1)):
            assert f"<span>{what}</span>" in rest and f"<b>{price}</b>" in rest, (what, price)
    assert seen == 10


def test_every_page_marks_closed_sections_before_the_first_paint_and_keeps_one_key():
    nav = importlib.reload(importlib.import_module("nav"))
    assert 'localStorage.getItem("folds")' in nav.FOLD_BOOT and "MutationObserver" in nav.FOLD_BOOT
    # If the script file never arrives nothing is left closed with no control.
    assert 'classList.remove("folds-on")' in nav.FOLD_BOOT
    text = (Path(__file__).resolve().parent.parent / "site" / "index.html").read_text(encoding="utf-8")
    assert nav.FOLD_BOOT in text and text.index(nav.FOLD_BOOT) < text.index("<main")
