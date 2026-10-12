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
    assert page.count('class="slot slot--session"') == 2 * 4 * len(program.ROOMS) - 1
    assert "Džuma" not in page and "prayer" not in page


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
