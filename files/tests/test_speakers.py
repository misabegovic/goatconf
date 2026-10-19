"""Speaker profiles and supporters, end to end on temp copies."""

import importlib
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

SESSION = """---
title: Salt, goats and servers
speakers: Ana Example
profiles: [ana-example]
format: talk
day: 2027-06-03
start: "12:00"
room: hall-first
accepted: yes
---

How a small town runs its own infrastructure.
"""

SPEAKER = """---
name: Ana Example
links:
  - https://example.com/ana
publish: yes
---

Ana builds small systems for small towns.
"""

SUPPORTER = """---
name: Acme
logo: img/supporters/acme.svg
url: https://acme.example
funds: Online supporter
---
"""

TALKING = """---
name: Ana Example
links:
  - https://example.com/ana
publish: yes
talk: Salt, goats and servers
talk_about: |
  How a small town runs its own infrastructure.

  For everyone who likes goats.
---

Ana builds small systems for small towns.
"""


def setup(tmp_path, monkeypatch, speaker=SPEAKER):
    program = importlib.reload(importlib.import_module("program"))
    speakers = importlib.reload(importlib.import_module("speakers"))
    for d in ("program", "speakers", "supporters", "site/img/supporters"):
        (tmp_path / d).mkdir(parents=True)
    (tmp_path / "program" / "s.md").write_text(SESSION, encoding="utf-8")
    (tmp_path / "speakers" / "ana-example.md").write_text(speaker, encoding="utf-8")
    (tmp_path / "supporters" / "acme.md").write_text(SUPPORTER, encoding="utf-8")
    (tmp_path / "site" / "img" / "supporters" / "acme.svg").write_text("<svg/>", encoding="utf-8")
    monkeypatch.setattr(program, "RECORDS", tmp_path / "program")
    monkeypatch.setattr(program, "SPEAKER_RECORDS", tmp_path / "speakers")
    monkeypatch.setattr(speakers, "SPEAKERS", tmp_path / "speakers")
    monkeypatch.setattr(speakers, "SUPPORTERS", tmp_path / "supporters")
    monkeypatch.setattr(speakers, "SITE", tmp_path / "site")
    return program, speakers


class Args:
    check = False


def test_profile_session_and_supporter_link_up(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch)
    assert speakers.cmd_check(Args()) == 0
    people = speakers.speakers_page()
    assert 'id="ana-example"' in people
    assert "Salt, goats and servers" in people
    assert "speaker__goat" in people  # no photo: the goat stands in
    assert "pay their own travel" not in people  # travel terms live on the talk page, not under the speakers
    wall = speakers.supporters_page()
    assert 'id="acme"' in wall and "Online supporter" in wall and "500 euro" in wall
    assert '<a href="speaker-ana-example.html">Ana Example</a>' in program.page()
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], speakers.sessions_by_speaker(detail=True)["ana-example"], speakers.supporters())
    assert "<h1 class=\"sign\">Ana Example</h1>" in page and "Salt, goats and servers" in page
    assert "funded by" not in page


def test_profile_without_consent_is_refused_and_not_linked(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes", "publish: no"))
    assert speakers.cmd_check(Args()) == 1
    assert 'id="ana-example"' not in speakers.speakers_page()
    page = program.page()
    assert "speaker-ana-example.html" not in page
    assert "Ana Example" in page  # the plain name from the session record


def test_unknown_supporter_and_missing_logo_fail(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("acme", "nobody"))
    (tmp_path / "site" / "img" / "supporters" / "acme.svg").unlink()
    assert speakers.cmd_check(Args()) == 1
    problems, _, _ = speakers.check_supporter(tmp_path / "supporters" / "acme.md")
    assert any("logo file not found" in p for p in problems)


def test_session_registration_links_everywhere(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch)
    rec = tmp_path / "program" / "s.md"
    rec.write_text(rec.read_text().replace("accepted: yes", "accepted: yes\nsignup: https://app.goatconf.com/s/abc123"), encoding="utf-8")
    assert '<a class="session__register" href="https://app.goatconf.com/s/abc123">Save a seat</a>' in program.page()
    detail = speakers.sessions_by_speaker(detail=True)["ana-example"]
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert "https://app.goatconf.com/s/abc123" in page


def test_session_signup_link_must_be_https(tmp_path, monkeypatch):
    program, _ = setup(tmp_path, monkeypatch)
    rec = tmp_path / "program" / "s.md"
    rec.write_text(rec.read_text().replace("accepted: yes", "accepted: yes\nsignup: http://example.com/x"), encoding="utf-8")
    problems, _, _ = program.check_record(rec)
    assert any("signup must be" in p for p in problems)


def test_a_talk_shows_before_it_has_a_slot(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, TALKING)
    (tmp_path / "program" / "s.md").unlink()  # no session on the program yet
    assert speakers.cmd_check(Args()) == 0
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], [], speakers.supporters())
    assert "<strong>Salt, goats and servers</strong>" in page
    assert "<p>How a small town runs its own infrastructure.</p>" in page
    assert "<p>For everyone who likes goats.</p>" in page  # a paragraph each, as written
    assert "The session will be on the program soon." not in page
    assert 'content="Ana Example speaks at GoatConf 2027 in Tuzla, 3–5 June 2027: Salt, goats and servers."' in page
    assert "Talk: Salt, goats and servers" in speakers.speakers_page()


def test_the_talk_fields_come_off_once_the_session_is_on_the_program(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, TALKING)
    assert speakers.cmd_check(Args()) == 1  # the session record now carries it: the talk fields are spent
    assert any("remove talk, talk_about" in p for p in speakers.talk_problems())


def test_talk_needs_a_title_and_talk_about_stays_short(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes\n", "publish: yes\ntalk_about: A sentence.\n"))
    record = tmp_path / "speakers" / "ana-example.md"
    problems, _, _ = speakers.check_speaker(record, {})
    assert any("talk_about needs talk" in p for p in problems)
    record.write_text(SPEAKER.replace("publish: yes\n", "publish: yes\ntalk: " + "x" * 81 + "\ntalk_about: " + " ".join(["y"] * 301) + "\n"), encoding="utf-8")
    problems, _, _ = speakers.check_speaker(record, {})
    assert any("talk must be" in p for p in problems) and any("longer than 300 words" in p for p in problems)


def test_role_shows_everywhere_the_name_does(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("name: Ana Example\n", "name: Ana Example\nrole: Engineer at A&B\n"))
    assert speakers.cmd_check(Args()) == 0
    assert '<span class="speaker__role">Engineer at A&amp;B</span>' in speakers.speakers_page()
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], speakers.sessions_by_speaker(detail=True)["ana-example"], speakers.supporters())
    assert '<span class="lede__role">Engineer at A&amp;B</span>' in page
    assert 'content="Ana Example (Engineer at A&amp;B) speaks at GoatConf 2027' in page
    home = importlib.reload(importlib.import_module("home"))
    assert '<span class="speaker__role">Engineer at A&amp;B</span>' in home.speakers_block()



def card(html: str) -> str:
    """A speaker's card, without what differs by page: its number, its tilt and the speakers page's anchor."""
    import re
    li = re.search(r'<li class="sticker sticker--speaker".*?</li>', html, re.S).group(0)
    return re.sub(r' id="[^"]*"| style="[^"]*"|<span class="num">\d+</span>', "", li)


def test_the_home_page_shows_the_same_speaker_card_as_the_speakers_page(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    home = importlib.reload(importlib.import_module("home"))
    assert card(home.speakers_block()) == card(speakers.speakers_page())
    assert "Talk, Thursday 3rd June at 12:00" in card(home.speakers_block())
    assert 'id="ana-example"' in speakers.speakers_page() and 'id="ana-example"' not in home.speakers_block()
    (tmp_path / "program" / "s.md").unlink()
    (tmp_path / "speakers" / "ana-example.md").write_text(FLAVORED, encoding="utf-8")
    assert card(home.speakers_block()) == card(speakers.speakers_page())
    assert '<span class="tag tag--area">Business of software</span>' in home.speakers_block()
    assert '<b>For:</b> founders before their first hire' in home.speakers_block()


def test_role_must_be_one_short_line(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("name: Ana Example\n", "name: Ana Example\nrole: " + "x" * 81 + "\n"))
    assert speakers.cmd_check(Args()) == 1


def test_speakers_are_listed_in_the_organisers_order(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    folder = tmp_path / "speakers"
    for slug, name, order in (("zed-first", "Zed First", "order: 1\n"), ("bea-second", "Bea Second", "order: 2\n"), ("al-unranked", "Al Unranked", "")):
        (folder / f"{slug}.md").write_text(f"---\nname: {name}\n{order}publish: yes\n---\n\nA bio.\n", encoding="utf-8")
    assert [s for s, _ in speakers.listed(speakers.speakers())] == ["zed-first", "bea-second", "al-unranked", "ana-example"]
    page = speakers.speakers_page()
    assert page.index('id="zed-first"') < page.index('id="bea-second"') < page.index('id="al-unranked"')
    assert speakers.cmd_check(Args()) == 0


def test_two_speakers_cannot_share_an_order(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes", "order: 1\npublish: yes"))
    (tmp_path / "speakers" / "bo-other.md").write_text("---\nname: Bo Other\norder: 1\npublish: yes\n---\n\nA bio.\n", encoding="utf-8")
    assert speakers.cmd_check(Args()) == 1
    record = tmp_path / "speakers" / "bo-other.md"
    record.write_text(record.read_text().replace("order: 1", "order: first"), encoding="utf-8")
    problems, _, _ = speakers.check_speaker(record, {})
    assert any("order must be" in p for p in problems)


def test_a_held_speaker_leaves_the_site_and_comes_back_without_the_line(tmp_path, monkeypatch, capsys):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes\n", "hold: waiting for his employer's approval\npublish: yes\n"))
    (tmp_path / "program" / "s.md").unlink()  # no session yet: the hold is the only thing keeping him off
    monkeypatch.setattr(speakers, "PAGES", {"speakers": tmp_path / "site" / "speakers.html", "supporters": tmp_path / "site" / "supporters.html"})
    assert speakers.cmd_check(Args()) == 0  # held, not a failure
    assert "note: held from the site" in capsys.readouterr().out
    assert "ana-example" not in speakers.speakers()
    assert 'id="ana-example"' not in speakers.speakers_page()
    home = importlib.reload(importlib.import_module("home"))
    assert "Ana Example" not in home.speakers_block()
    speakers.cmd_build(Args())
    stale = tmp_path / "site" / "speaker-ana-example.html"
    stale.write_text("old page", encoding="utf-8")
    assert speakers.cmd_build(type("A", (), {"check": True})()) == 1  # the stale page is named, not served
    speakers.cmd_build(Args())
    assert not stale.exists()
    (tmp_path / "speakers" / "ana-example.md").write_text(SPEAKER, encoding="utf-8")  # the hold line comes off
    assert "ana-example" in speakers.speakers()
    assert 'id="ana-example"' in speakers.speakers_page()


def test_a_held_speaker_with_a_session_on_the_program_fails_the_check(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes\n", "hold: waiting for his employer's approval\npublish: yes\n"))
    assert speakers.cmd_check(Args()) == 1  # the program record still names the profile: the session must come off too
    assert any("not a published speaker record" in p for p in speakers.session_problems())


def test_a_held_speaker_keeps_their_order_in_the_clash_check(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes\n", "order: 4\nhold: waiting for his employer's approval\npublish: yes\n"))
    (tmp_path / "program" / "s.md").unlink()
    (tmp_path / "speakers" / "bo-other.md").write_text("---\nname: Bo Other\norder: 4\npublish: yes\n---\n\nA bio.\n", encoding="utf-8")
    assert speakers.cmd_check(Args()) == 1
    assert any("order 4 is given to more than one speaker" in p for p in speakers.order_problems())


def test_hold_must_be_one_short_line(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes\n", "publish: yes\nhold: " + "x" * 81 + "\n"))
    problems, _, _ = speakers.check_speaker(tmp_path / "speakers" / "ana-example.md", {})
    assert any("hold must be" in p for p in problems)


def test_travel_funded_by_is_refused(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch)
    record = tmp_path / "speakers" / "ana-example.md"
    record.write_text(record.read_text(encoding="utf-8").replace("publish: yes\n", "publish: yes\ntravel_funded_by: acme\n"), encoding="utf-8")
    assert speakers.cmd_check(Args()) == 1


def test_a_speaker_page_shares_their_own_card_and_the_check_wants_it(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    meta = importlib.import_module("meta")
    monkeypatch.setattr(speakers, "PAGES", {"speakers": tmp_path / "site" / "speakers.html", "supporters": tmp_path / "site" / "supporters.html"})
    detail = speakers.sessions_by_speaker(detail=True)["ana-example"]
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert "image_src" not in page  # no card yet: the generic banner
    assert speakers.cmd_build(type("A", (), {"check": True})()) == 1
    (tmp_path / "site" / "share").mkdir()
    (tmp_path / "site" / "share" / "speaker-ana-example-preview.png").write_bytes(b"png")
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert '<link rel="image_src" href="https://goatconf.com/share/speaker-ana-example-preview.png">' in page
    assert 'og:image" content="https://goatconf.com/share/speaker-ana-example-preview.png"' in meta.tag(page)


HOST = """---
name: Zeta Academy
logo: img/supporters/zeta.png
logo_on: dark
url: https://zeta.example
funds: "Host and partner: the rooms"
host: yes
---
"""


def test_the_host_leads_the_supporters_and_the_invitation_stays_until_a_company_supports(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    (tmp_path / "supporters" / "zeta-academy.md").write_text(HOST, encoding="utf-8")
    (tmp_path / "site" / "img" / "supporters" / "zeta.png").write_bytes(b"png")
    assert speakers.cmd_check(Args()) == 0
    assert [s for s, _ in speakers.listed_supporters(speakers.supporters())] == ["zeta-academy", "acme"]  # host first, though Z
    wall = speakers.supporters_page()
    assert wall.index('id="zeta-academy"') < wall.index('id="acme"')
    assert "supporter__logo--dark" in wall and "<strong>Your logo</strong>" not in wall  # a paying supporter exists
    (tmp_path / "supporters" / "acme.md").unlink()
    wall = speakers.supporters_page()
    assert "Be the first supporter." in wall  # only the host: keep inviting
    home = importlib.reload(importlib.import_module("home"))
    block = home.supporters_block()
    assert "supporter-chip--dark" in block and "<strong>Your logo</strong>" in block


def test_host_and_logo_background_are_checked(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    rec = tmp_path / "supporters" / "zeta-academy.md"
    rec.write_text(HOST.replace("host: yes", "host: maybe").replace("logo_on: dark", "logo_on: purple"), encoding="utf-8")
    (tmp_path / "site" / "img" / "supporters" / "zeta.png").write_bytes(b"png")
    problems, _, _ = speakers.check_supporter(rec)
    assert any("host must be yes" in p for p in problems) and any("logo_on must be" in p for p in problems)


def test_each_supporter_has_a_profile_with_their_cards(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    monkeypatch.setattr(speakers, "PAGES", {"speakers": tmp_path / "site" / "speakers.html", "supporters": tmp_path / "site" / "supporters.html"})
    wall = speakers.supporters_page()
    assert '<strong><a href="supporter-acme.html">Acme</a></strong>' in wall and 'href="https://acme.example"' not in wall
    home = importlib.reload(importlib.import_module("home"))
    assert 'href="supporter-acme.html"' in home.supporters_block()
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert '<h1 class="sign">Acme</h1>' in page and 'href="https://acme.example">acme.example</a>' in page
    assert "The thank-you card" not in page and "image_src" not in page  # no cards rendered yet
    assert speakers.cmd_build(type("A", (), {"check": False})()) == 0
    assert (tmp_path / "site" / "supporter-acme.html").exists()
    (tmp_path / "site" / "share").mkdir()
    for size in ("square", "wide"):
        (tmp_path / "site" / "share" / f"supporter-acme-{size}.png").write_bytes(b"png")
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert 'href="share/supporter-acme-square.png" download' in page and 'href="share/supporter-acme-wide.png" download' in page
    assert '<link rel="image_src" href="https://goatconf.com/share/supporter-acme-wide.png">' in page
    (tmp_path / "supporters" / "acme.md").unlink()
    assert speakers.cmd_build(type("A", (), {"check": False})()) == 0
    assert not (tmp_path / "site" / "supporter-acme.html").exists()


def test_a_supporter_lists_only_accepted_events_and_shows_them(tmp_path, monkeypatch):
    import datetime as dt
    _, speakers = setup(tmp_path, monkeypatch)
    extensions = importlib.import_module("extensions")
    meetup = {"name": "Lake meetup", "kind": "meetup", "host": "Acme", "start": "2027-06-05 18:00", "end": "2027-06-05 21:00"}
    monkeypatch.setattr(extensions, "accepted", lambda: [(dt.datetime(2027, 6, 5, 18), "lake-meetup", meetup, "")])
    rec = tmp_path / "supporters" / "acme.md"
    rec.write_text(SUPPORTER.replace("funds: Online supporter", "funds: Funding and organising the Lake meetup\nevents: [nope]"), encoding="utf-8")
    problems, _, _ = speakers.check_supporter(rec)
    assert any("events must list accepted events" in p and "lake-meetup" in p for p in problems)
    rec.write_text(SUPPORTER.replace("funds: Online supporter", "funds: Funding and organising the Lake meetup\nevents: [lake-meetup]"), encoding="utf-8")
    assert speakers.check_supporter(rec)[0] == []
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert "Their event" in page and 'href="event-lake-meetup.html"' in page
    (tmp_path / "site" / "share").mkdir()
    (tmp_path / "site" / "share" / "supporter-acme-wide.png").write_bytes(b"png")
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert 'image_src" href="https://goatconf.com/share/supporter-acme-wide.png"' in page  # no event card yet
    (tmp_path / "site" / "share" / "event-lake-meetup-preview.png").write_bytes(b"png")
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert 'image_src" href="https://goatconf.com/share/event-lake-meetup-preview.png"' in page  # their event's card


def test_who_they_are_and_how_to_support_them_show_on_the_profile_only(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch)
    rec = tmp_path / "supporters" / "acme.md"
    rec.write_text(SUPPORTER.replace("funds: Online supporter", "funds: Online supporter\nsupport_them:\n  - {text: Work with Acme, url: https://acme.example/jobs}")
                   + "\nAcme makes anvils for coyotes.\n", encoding="utf-8")
    assert speakers.check_supporter(rec)[0] == []
    page = speakers.supporter_page("acme", *speakers.supporters()["acme"])
    assert "Who they are" in page and "Acme makes anvils for coyotes." in page
    assert '<li><a href="https://acme.example/jobs">Work with Acme</a></li>' in page
    assert "Acme makes anvils" not in speakers.supporters_page()
    rec.write_text(SUPPORTER.replace("funds: Online supporter", "funds: Online supporter\nsupport_them:\n  - {text: Jobs, url: http://acme.example/jobs}"), encoding="utf-8")
    assert any("support_them must list" in p for p in speakers.check_supporter(rec)[0])


def test_a_speaker_page_says_who_they_are_and_how_to_support_them(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("publish: yes", "publish: yes\nsupport_them:\n  - {text: Read her book, url: https://example.com/book}"))
    detail = speakers.sessions_by_speaker(detail=True)["ana-example"]
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert '<h2 class="band" id="h-about">Who they are</h2>' in page
    assert '<h2 class="band" id="h-support-them">How to support them</h2>' in page
    assert '<li><a href="https://example.com/book">Read her book</a></li>' in page
    _, speakers = setup(tmp_path / "bad", monkeypatch, SPEAKER.replace("publish: yes", "publish: yes\nsupport_them: buy the book"))
    problems, _, _ = speakers.check_speaker(tmp_path / "bad" / "speakers" / "ana-example.md", speakers.supporters())
    assert any("support_them must list" in p for p in problems)


FLAVORED = TALKING.replace("talk_about: |", "talk_area: business\ntalk_for: founders before their first hire\ntalk_about: |")


def test_a_talk_shows_its_area_and_who_it_is_for(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, FLAVORED)
    (tmp_path / "program" / "s.md").unlink()  # no session on the program yet
    assert speakers.cmd_check(Args()) == 0
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], [], speakers.supporters())
    assert '<span class="tag tag--area">Business of software</span>' in page
    assert '<p class="for-line"><b>For:</b> founders before their first hire</p>' in page
    listing = speakers.speakers_page()
    assert '<span class="tag tag--area">Business of software</span>' in listing
    assert '<span class="for-line"><b>For:</b> founders before their first hire</span>' in listing


def test_area_format_and_who_it_is_for_are_checked(tmp_path, monkeypatch):
    _, speakers = setup(tmp_path, monkeypatch, FLAVORED.replace("business", "marketing").replace("talk_area:", "talk_format: keynote\ntalk_area:")
                        .replace("founders before their first hire", "x" * 101))
    problems, _, _ = speakers.check_speaker(tmp_path / "speakers" / "ana-example.md", {})
    assert any("talk_area must be one of" in p for p in problems)
    assert any("talk_format must be one of" in p for p in problems)
    assert any("talk_for must be one line" in p for p in problems)
    (tmp_path / "speakers" / "ana-example.md").write_text(SPEAKER.replace("publish: yes\n", "publish: yes\ntalk_area: research\n"), encoding="utf-8")
    problems, _, _ = speakers.check_speaker(tmp_path / "speakers" / "ana-example.md", {})
    assert any("need talk" in p for p in problems)


def test_a_scheduled_session_carries_its_area_and_who_it_is_for(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch)
    (tmp_path / "program" / "s.md").write_text(SESSION.replace("accepted: yes", "accepted: yes\narea: leadership\nfor: anyone leading a team of five or more"), encoding="utf-8")
    assert speakers.cmd_check(Args()) == 0
    table, _ = program.sessions()
    (key, (meta, body)), = table.items()
    session = program.session_page(key, meta, body)
    assert "<dt>Area</dt><dd>Leadership</dd>" in session and "<dt>For</dt><dd>anyone leading a team of five or more</dd>" in session
    assert '<span class="tag tag--area">Leadership</span>' in program.cell(1, (meta, body), key[2])
    detail = speakers.sessions_by_speaker(detail=True)["ana-example"]
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert '<p class="for-line"><b>For:</b> anyone leading a team of five or more</p>' in page
    assert '<span class="tag tag--area">Leadership</span>' in speakers.speakers_page()
    (tmp_path / "program" / "s.md").write_text(SESSION.replace("accepted: yes", "accepted: yes\narea: sales"), encoding="utf-8")
    problems, _, _ = program.check_record(tmp_path / "program" / "s.md")
    assert any("area must be one of" in p for p in problems)
