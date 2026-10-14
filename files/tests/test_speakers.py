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


def test_role_shows_everywhere_the_name_does(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch, SPEAKER.replace("name: Ana Example\n", "name: Ana Example\nrole: Engineer at A&B\n"))
    assert speakers.cmd_check(Args()) == 0
    assert '<span class="speaker__role">Engineer at A&amp;B</span>' in speakers.speakers_page()
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], speakers.sessions_by_speaker(detail=True)["ana-example"], speakers.supporters())
    assert '<span class="lede__role">Engineer at A&amp;B</span>' in page
    assert 'content="Ana Example (Engineer at A&amp;B) speaks at GoatConf 2027' in page
    home = importlib.reload(importlib.import_module("home"))
    assert '<small class="sticker__role">Engineer at A&amp;B</small>' in home.speaker_sticker(0, "ana-example", speakers.speakers()["ana-example"][0])


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
