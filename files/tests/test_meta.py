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


def test_a_page_without_a_title_or_stylesheet_is_named_not_crashed():
    meta = importlib.reload(importlib.import_module("meta"))
    for broken, reason in ((PAGE.replace("<title>", "<x>").replace("</title>", "</x>"), "no <title>"),
                           (PAGE.replace('<link rel="stylesheet" href="goatconf.css">', ""), "no goatconf.css")):
        try:
            meta.tag(broken)
        except ValueError as err:
            assert reason in str(err)
        else:
            raise AssertionError("expected a ValueError")


def test_a_page_can_name_its_own_preview_image():
    meta = importlib.reload(importlib.import_module("meta"))
    own = PAGE.replace('<link rel="stylesheet"', '<link rel="image_src" href="https://goatconf.com/share/speaker-ana-preview.png">\n<link rel="stylesheet"')
    tagged = meta.tag(own)
    assert '<meta property="og:image" content="https://goatconf.com/share/speaker-ana-preview.png">' in tagged
    assert '<meta property="og:image:alt" content="Program: GoatConf &amp; friends">' in tagged
    assert "share/og.png" not in tagged
    assert meta.tag(tagged) == tagged
