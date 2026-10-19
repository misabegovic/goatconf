"""tools/extensions.py: the record check and the generated page."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "tools" / "extensions.py"
GOOD = """---
name: Rust by the lake
kind: workshop
host: Tuzla Rustaceans
location: Slana banja park, Tuzla
start: 2027-06-02 10:00
end: 2027-06-02 13:00
cost: free
registration: https://example.org/rust
paid_by: The host
contact: https://example.org/contact
accepts: yes
accepted: yes
---

A morning of pairing on small Rust programs, for beginners.
"""


@pytest.fixture
def ext(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("extensions", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    (tmp_path / "extensions").mkdir()
    (tmp_path / "site").mkdir()
    shell = SCRIPT.parent.parent / "site" / "contact.html"
    (tmp_path / "site" / "contact.html").write_text(shell.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "RECORDS", tmp_path / "extensions")
    monkeypatch.setattr(mod, "PAGE", tmp_path / "site" / "extensions.html")
    monkeypatch.setattr(mod, "SHELL", tmp_path / "site" / "contact.html")
    return mod, tmp_path


def write(root, name, text, cards=True):
    """A record, and (unless told not to) the cards tools/shareables.py would render for it."""
    path = root / "extensions" / name
    path.write_text(text, encoding="utf-8")
    if cards:
        (root / "site" / "share").mkdir(exist_ok=True)
        for size in ("square", "wide", "preview"):
            (root / "site" / "share" / f"event-{path.stem}-{size}.png").write_bytes(b"png")
    return path


def test_no_records_passes(ext, capsys):
    mod, _ = ext
    assert mod.main(["check"]) == 0
    assert "no records yet" in capsys.readouterr().out


def test_good_record_passes(ext, capsys):
    mod, root = ext
    write(root, "rust.md", GOOD)
    assert mod.main(["check"]) == 0
    assert "ok: workshop, hosted by Tuzla Rustaceans" in capsys.readouterr().out


@pytest.mark.parametrize("change, message", [
    (("kind: workshop", "kind: party"), "is not one of"),
    (("accepts: yes", "accepts: no"), "accepts must be yes"),
    (("host: Tuzla Rustaceans\n", ""), "missing field: host"),
    (("end: 2027-06-02 13:00", "end: 2027-06-02 09:00"), "end comes before start"),
    (("2027-06-02 10:00", "2027-09-01 10:00"), "outside the GoatConf week"),
    (("name: Rust by the lake", "name: GoatConf presents Rust"), "reads as if the organiser runs it"),
    (("A morning of pairing on small Rust programs, for beginners.", ""), "no description"),
])
def test_bad_records_fail(ext, capsys, change, message):
    mod, root = ext
    write(root, "bad.md", GOOD.replace(*change))
    assert mod.main(["check"]) == 1
    assert message in capsys.readouterr().out


def test_something_else_is_a_kind(ext, capsys):
    mod, root = ext
    write(root, "quiz.md", GOOD.replace("kind: workshop", "kind: other"))
    assert mod.main(["check"]) == 0
    assert "ok: something else" in capsys.readouterr().out
    mod.main(["build"])
    assert "Something else" in (root / "site" / "extensions.html").read_text(encoding="utf-8")


def test_support_needs_a_supplier(ext, capsys):
    mod, root = ext
    write(root, "coffee.md", GOOD.replace("kind: workshop", "kind: support"))
    assert mod.main(["check"]) == 1
    assert "names the supplier" in capsys.readouterr().out


def test_outside_week_with_reason_passes(ext, capsys):
    mod, root = ext
    text = GOOD.replace("2027-06-02 10:00", "2027-07-01 10:00").replace("2027-06-02 13:00", "2027-07-01 13:00")
    write(root, "late.md", text.replace("accepts: yes", "accepts: yes\noutside_week_reason: a follow-up session"))
    assert mod.main(["check"]) == 0
    assert "with a reason" in capsys.readouterr().out


def test_template_and_readme_are_not_records(ext):
    mod, root = ext
    write(root, "README.md", "# not a record\n")
    write(root, "_template.md", GOOD.replace("kind: workshop", "kind: nonsense"))
    assert mod.records() == []


def test_build_lists_good_records_and_check_detects_staleness(ext):
    mod, root = ext
    assert mod.main(["build"]) == 0
    page = (root / "site" / "extensions.html").read_text(encoding="utf-8")
    assert "No events yet." in page
    write(root, "rust.md", GOOD)
    write(root, "bad.md", GOOD.replace("accepts: yes", "accepts: no").replace("Rust by the lake", "Broken"))
    assert mod.main(["build", "--check"]) == 1
    assert mod.main(["build"]) == 0
    page = (root / "site" / "extensions.html").read_text(encoding="utf-8")
    assert "Rust by the lake" in page and "Broken" not in page
    assert "2 June 2027, 10:00 to 13:00" in page
    assert mod.main(["build", "--check"]) == 0


def test_only_accepted_events_are_listed(ext):
    mod, root = ext
    write(root, "rust.md", GOOD.replace("accepted: yes\n", ""))
    write(root, "hack.md", GOOD.replace("Rust by the lake", "Lake hackathon").replace("kind: workshop", "kind: hackathon"))
    assert mod.main(["build"]) == 0
    page = (root / "site" / "extensions.html").read_text(encoding="utf-8")
    assert "Lake hackathon" in page and "Rust by the lake" not in page
    assert 'href="event-hack.html"' in page and "event-rust.html" not in page
    assert not (root / "site" / "event-rust.html").exists()
    event = (root / "site" / "event-hack.html").read_text(encoding="utf-8")
    assert "Hackathon, part of GoatConf 2027, run by Tuzla Rustaceans" in event
    problems, notes, _ = mod.check_record(root / "extensions" / "rust.md")
    assert not problems and any("not yet accepted" in n for n in notes)


def test_each_accepted_event_gets_its_own_page_that_links_out(ext):
    mod, root = ext
    write(root, "rust.md", GOOD.replace("contact: https://example.org/contact", "contact: hello@example.org"))
    assert mod.main(["build"]) == 0
    event = (root / "site" / "event-rust.html").read_text(encoding="utf-8")
    assert "<h1 class=\"sign\">Rust by the lake</h1>" in event
    assert '<a class="button" href="https://example.org/rust">Register with the host</a>' in event
    assert '<a href="mailto:hello@example.org">hello@example.org</a>' in event
    assert "A morning of pairing on small Rust programs, for beginners." in event
    assert '<link rel="canonical" href="https://goatconf.com/event-rust">' in event
    assert 'href="program.html#h-around"' in event  # 2 June is outside the three days
    assert 'aria-current="page"' in event and 'href="program.html" aria-current="page"' in event


def test_a_page_whose_event_is_gone_is_removed_and_caught(ext, capsys):
    mod, root = ext
    write(root, "rust.md", GOOD)
    assert mod.main(["build"]) == 0
    (root / "extensions" / "rust.md").unlink()
    assert mod.main(["build", "--check"]) == 1
    assert "belongs to no accepted event" in capsys.readouterr().out
    assert mod.main(["build"]) == 0
    assert not (root / "site" / "event-rust.html").exists()
    assert mod.main(["build", "--check"]) == 0


def test_the_file_name_becomes_an_address(ext, capsys):
    mod, root = ext
    write(root, "Rust Night.md", GOOD)
    assert mod.main(["check"]) == 1
    assert "lowercase words joined by hyphens" in capsys.readouterr().out


def test_an_accepted_event_needs_its_cards_and_its_page_offers_them(ext, capsys):
    mod, root = ext
    write(root, "rust.md", GOOD, cards=False)
    assert mod.main(["build"]) == 0
    event = (root / "site" / "event-rust.html").read_text(encoding="utf-8")
    assert "Cards to share" not in event and "image_src" not in event
    assert mod.main(["build", "--check"]) == 1
    assert "event-rust-preview.png is missing" in capsys.readouterr().out
    write(root, "rust.md", GOOD)
    assert mod.main(["build"]) == 0
    event = (root / "site" / "event-rust.html").read_text(encoding="utf-8")
    assert '<link rel="image_src" href="https://goatconf.com/share/event-rust-preview.png">' in event
    assert 'href="share/event-rust-square.png" download' in event and 'href="share/event-rust-wide.png" download' in event
    assert mod.main(["build", "--check"]) == 0


def test_the_event_page_links_its_host_supporters_profile(ext):
    mod, root = ext
    write(root, "rust.md", GOOD)
    assert mod.main(["build"]) == 0
    assert "supporter-" not in (root / "site" / "event-rust.html").read_text(encoding="utf-8")
    (root / "supporters").mkdir()
    (root / "supporters" / "rustaceans.md").write_text("---\nname: Tuzla Rustaceans\nevents: [rust]\n---\n", encoding="utf-8")
    assert mod.main(["build", "--check"]) == 1  # the supporter record changes the event page
    assert mod.main(["build"]) == 0
    event = (root / "site" / "event-rust.html").read_text(encoding="utf-8")
    assert '<dt>Run by</dt><dd><a href="supporter-rustaceans.html">Tuzla Rustaceans</a></dd>' in event
    assert 'is a supporter of GoatConf 2027. <a href="supporter-rustaceans.html">See their profile</a>' in event
