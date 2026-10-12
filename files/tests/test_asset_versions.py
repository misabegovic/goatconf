"""Stylesheet and scripts carry a version stamp that follows their contents."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
meta = importlib.import_module("meta")

PAGE = """<html><head><title>T</title>
<meta name="description" content="D">
<link rel="stylesheet" href="goatconf.css">
</head><body><script src="album.js" defer></script></body></html>"""


def test_stamp_follows_the_file(tmp_path, monkeypatch):
    monkeypatch.setattr(meta, "SITE", tmp_path)
    (tmp_path / "goatconf.css").write_text("a {}")
    (tmp_path / "album.js").write_text("1")
    first = meta.tag(PAGE)
    assert f'href="goatconf.css?v={meta.version("goatconf.css")}"' in first
    assert f'src="album.js?v={meta.version("album.js")}"' in first
    assert meta.tag(first) == first
    (tmp_path / "goatconf.css").write_text("a { color: red }")
    second = meta.tag(first)
    assert second != first and second.count("goatconf.css?v=") == 1
