"""The program generator and the form-link tool, end to end on temp copies."""

import importlib
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))


def load(name):
    return importlib.reload(importlib.import_module(name))


SESSION = """---
title: Salt, goats and servers
speakers: Ana Example
format: talk
day: 2027-06-03
start: "12:00"
room: hall-first
accepted: yes
---

How a small town runs its own infrastructure.
"""


def test_session_record_lands_in_its_slot(tmp_path, monkeypatch):
    program = load("program")
    (tmp_path / "s.md").write_text(SESSION, encoding="utf-8")
    monkeypatch.setattr(program, "RECORDS", tmp_path)
    page = program.page()
    assert "Salt, goats and servers" in page
    assert "Talk, First-floor hall" in page
    held = len(program.reserved_cells(program.sessions()[0]))
    assert page.count('class="slot slot--session"') == 2 * 4 * len(program.ROOMS) - 1 - held
    assert page.count('class="slot slot--session slot--reserved"') == held
    assert "Džuma" not in page and "prayer" not in page


def test_cells_are_held_for_speakers_without_a_slot(tmp_path, monkeypatch):
    program = load("program")
    records, people = tmp_path / "program", tmp_path / "speakers"
    records.mkdir()
    people.mkdir()
    monkeypatch.setattr(program, "RECORDS", records)
    monkeypatch.setattr(program, "SPEAKER_RECORDS", people)
    for name, extra in (("ana", ""), ("ben", ""), ("cleo", "hold: not yet\n")):
        (people / f"{name}.md").write_text(f"---\nname: {name}\npublish: yes\n{extra}---\n", encoding="utf-8")
    page = program.page()
    assert page.count('slot--reserved"') == 2
    assert "1 of 7 rooms taken" in page
    (records / "s.md").write_text(SESSION.replace("format: talk", "profiles: [ana]\nformat: talk"), encoding="utf-8")
    assert program.page().count('slot--reserved"') == 1


def test_bad_and_clashing_records_fail(tmp_path, monkeypatch):
    program = load("program")
    (tmp_path / "a.md").write_text(SESSION, encoding="utf-8")
    (tmp_path / "b.md").write_text(SESSION, encoding="utf-8")
    (tmp_path / "c.md").write_text(SESSION.replace("2027-06-03", "2027-06-05"), encoding="utf-8")
    monkeypatch.setattr(program, "RECORDS", tmp_path)

    class A:
        files = []
    assert program.cmd_check(A()) == 1
    problems, _, _ = program.check_record(tmp_path / "c.md")
    assert any("core days" in p for p in problems)
    (tmp_path / "d.md").write_text(SESSION.replace("2027-06-03", "2027-06-04"), encoding="utf-8")
    problems, _, _ = program.check_record(tmp_path / "d.md")
    assert any("Friday" in p and "11:30" in p for p in problems)  # Friday runs on the half hour


def test_links_are_written_and_publish_needs_every_url(tmp_path, monkeypatch):
    site = load("formlinks")
    (tmp_path / "site").mkdir()
    page = tmp_path / "site" / "talk.html"
    page.write_text('<a class="button" data-form="talk" href="">Go</a>', encoding="utf-8")
    forms = tmp_path / "forms.yml"
    forms.write_text('talk: "https://forms.gle/abc"\nadd: ""\n', encoding="utf-8")
    monkeypatch.setattr(site, "SITE", tmp_path / "site")
    monkeypatch.setattr(site, "FORMS", forms)

    class A:
        publish = False
    assert site.cmd_check(A()) == 1
    site.cmd_links(A())
    assert 'href="https://forms.gle/abc"' in page.read_text(encoding="utf-8")
    assert site.cmd_check(A()) == 0
    A.publish = True
    assert site.cmd_check(A()) == 0
    page.write_text(page.read_text(encoding="utf-8") + '<a data-form="add" href="contact.html#forms-pending">x</a>', encoding="utf-8")
    assert site.cmd_check(A()) == 1


def test_each_session_gets_its_own_page_and_its_sticker_opens_it(tmp_path, monkeypatch):
    program = load("program")
    records, site = tmp_path / "program", tmp_path / "site"
    records.mkdir()
    site.mkdir()
    (records / "s.md").write_text(SESSION, encoding="utf-8")
    monkeypatch.setattr(program, "RECORDS", records)
    monkeypatch.setattr(program, "PAGE", site / "program.html")
    assert program.page_name({"title": "Salt, goats & šervers!"}) == "session-salt-goats-servers.html"
    assert program.cmd_build(type("A", (), {"check": False})()) == 0
    grid = (site / "program.html").read_text(encoding="utf-8")
    assert '<a class="sticker__open sticker__open--stretch" href="session-salt-goats-and-servers.html">Salt, goats and servers</a>' in grid
    page = (site / "session-salt-goats-and-servers.html").read_text(encoding="utf-8")
    assert '<h1 class="sign">Salt, goats and servers</h1>' in page
    assert "Thursday 3rd June 2027, 12:00 to 13:00" in page and "First-floor hall (100 seats)" in page
    assert "How a small town runs its own infrastructure." in page
    assert 'href="program.html" aria-current="page"' in page
    assert program.cmd_build(type("A", (), {"check": True})()) == 0
    (records / "s.md").unlink()
    assert program.cmd_build(type("A", (), {"check": True})()) == 1
    assert program.cmd_build(type("A", (), {"check": False})()) == 0
    assert not (site / "session-salt-goats-and-servers.html").exists()


def test_two_sessions_with_one_title_clash(tmp_path, monkeypatch):
    program = load("program")
    (tmp_path / "a.md").write_text(SESSION, encoding="utf-8")
    (tmp_path / "b.md").write_text(SESSION.replace('"12:00"', '"14:00"'), encoding="utf-8")
    monkeypatch.setattr(program, "RECORDS", tmp_path)
    _, clashes = program.sessions()
    assert len(clashes) == 1 and "would share the page" in clashes[0]


def test_an_accepted_event_on_the_program_opens_its_page(monkeypatch):
    import datetime as dt
    program = load("program")
    sat = dt.date(2027, 6, 5)
    meta = {"name": "Salt lake hike", "kind": "hike", "host": "Ana", "location": "Pannonica",
            "start": "2027-06-05 10:00", "end": "2027-06-05 13:00"}
    monkeypatch.setattr(program, "extension_days", lambda: {sat: [(dt.datetime(2027, 6, 5, 10), "salt-lake-hike", meta, "")]})
    assert '<a class="sticker__open" href="event-salt-lake-hike.html"><strong>Salt lake hike</strong>' in program.page()
