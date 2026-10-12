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
travel_funded_by: acme
---

Ana builds small systems for small towns.
"""

SUPPORTER = """---
name: Acme
logo: img/supporters/acme.svg
url: https://acme.example
funds: Travel for one speaker
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


def test_profile_session_and_travel_supporter_link_up(tmp_path, monkeypatch):
    program, speakers = setup(tmp_path, monkeypatch)
    assert speakers.cmd_check(Args()) == 0
    people = speakers.speakers_page()
    assert 'id="ana-example"' in people
    assert "Salt, goats and servers" in people
    assert "Travel funded by Acme" in people
    assert "speaker__goat" in people  # no photo: the goat stands in
    wall = speakers.supporters_page()
    assert 'id="acme"' in wall and "Travel for <a" in wall
    assert '<a href="speaker-ana-example.html">Ana Example</a>' in program.page()
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], speakers.sessions_by_speaker(detail=True)["ana-example"], speakers.supporters())
    assert "<h1 class=\"sign\">Ana Example</h1>" in page and "Salt, goats and servers" in page and "funded by Acme" in page


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
    rec.write_text(rec.read_text().replace("accepted: yes", "accepted: yes\nluma: https://luma.com/abc123"), encoding="utf-8")
    assert '<a class="session__register" href="https://luma.com/abc123">Register for this session</a>' in program.page()
    detail = speakers.sessions_by_speaker(detail=True)["ana-example"]
    page = speakers.speaker_page("ana-example", *speakers.speakers()["ana-example"], detail, speakers.supporters())
    assert "https://luma.com/abc123" in page


def test_session_registration_link_must_be_luma(tmp_path, monkeypatch):
    program, _ = setup(tmp_path, monkeypatch)
    rec = tmp_path / "program" / "s.md"
    rec.write_text(rec.read_text().replace("accepted: yes", "accepted: yes\nluma: https://example.com/x"), encoding="utf-8")
    problems, _, _ = program.check_record(rec)
    assert any("luma must be" in p for p in problems)
