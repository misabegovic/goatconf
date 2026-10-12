"""Link-preview tags: built from the page's own title, description and canonical link."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

PAGE = """<head><title>Program: GoatConf &amp; friends</title>
<meta name="description" content="Two core days.">
<link rel="canonical" href="https://goatconf.com/program.html">
<link rel="stylesheet" href="goatconf.css">
</head>"""


def test_tags_are_added_once_and_refreshed():
    meta = importlib.reload(importlib.import_module("meta"))
    once = meta.tag(PAGE)
    assert '<meta property="og:title" content="Program: GoatConf &amp; friends">' in once
    assert '<meta property="og:url" content="https://goatconf.com/program.html">' in once
    assert '<meta property="og:image" content="https://goatconf.com/share/og.png">' in once
    assert meta.tag(once) == once  # idempotent
    changed = meta.tag(once.replace("Two core days.", "Three days."))
    assert changed.count("og:description") == 1 and 'content="Three days."' in changed
