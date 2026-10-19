"""The HTML check: a clean page passes, and each kind of breakage is named."""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

GOOD = """<!doctype html><html lang="en"><head><title>t</title></head><body>
<header class="topbar"><a href="index.html">Home</a></header>
<main id="main"><div class="page-head"><h1>Title</h1></div>
<p><a href="#main">Up</a> <a href="https://example.com/x">Out</a> <img src="a.png" alt=""></p>
<svg><path d="M0 0"/></svg></main>
<footer><p>End</p></footer></body></html>
"""


def run(tmp_path, monkeypatch, page):
    lint = importlib.reload(importlib.import_module("site_lint"))
    (tmp_path / "a.png").write_bytes(b"")
    (tmp_path / "index.html").write_text(page, encoding="utf-8")
    monkeypatch.setattr(lint, "SITE", tmp_path)
    pages = {p.name: lint.parse(p) for p in sorted(tmp_path.glob("*.html"))}
    return [x for p in pages.values() for x in p.problems] + lint.check_links(pages)


def test_a_clean_page_passes(tmp_path, monkeypatch):
    assert run(tmp_path, monkeypatch, GOOD) == []


def test_each_breakage_is_named(tmp_path, monkeypatch):
    cases = [
        ('<p><a href="#main">Up</a>', '<div><a href="#main">Up</a>', "is not closed"),
        ('<a href="#main">Up</a>', '<a href="#nowhere">Up</a>', "#nowhere"),
        ('<img src="a.png" alt="">', '<img src="b.png" alt="">', "does not exist"),
        ('<img src="a.png" alt="">', '<img src="a.png">', "no alt"),
        ('<div class="page-head"><h1>Title</h1></div>', '<div class="page-head"><h1 id="main">Title</h1></div>', "used twice"),
        ('<footer>', '<header>Second</header><footer>', "banners"),
        ('<h1>Title</h1>', '<h2>Title</h2>', "<h1> elements"),
    ]
    for old, new, expect in cases:
        problems = run(tmp_path, monkeypatch, GOOD.replace(old, new, 1))
        assert any(expect in p for p in problems), (expect, problems)
