#!/usr/bin/env python3
"""Link previews: give every page the tags that social sites and chats read.

Each page already has a <title>, a meta description and a canonical link.
This adds Open Graph and Twitter card tags built from them, pointing at the
shared preview image site/share/og.png (made by tools/shareables.py).

  apply           add or refresh the tags in every site/*.html
  check           fail if a page's tags are missing or out of date

It also stamps the stylesheet and scripts with a short hash of their
contents (goatconf.css?v=1a2b3c4d), so phones fetch them again whenever they
change instead of keeping an old copy for ten minutes.

The generators (program, extensions, speakers) call tag() on their output,
so their pages stay current without a separate step.

Usage: python3 tools/meta.py <apply|check>
"""

from __future__ import annotations

import hashlib
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
IMAGE = "https://goatconf.com/share/og.png"
START, END = "<!-- link preview -->", "<!-- /link preview -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def tags(text: str) -> str:
    title = re.search(r"<title>(.*?)</title>", text, re.S).group(1).strip()
    desc_m = re.search(r'<meta name="description" content="([^"]*)">', text)
    url_m = re.search(r'<link rel="canonical" href="([^"]*)">', text)
    desc = desc_m.group(1) if desc_m else ""
    url = url_m.group(1) if url_m else "https://goatconf.com/"
    t = html.escape(html.unescape(title), quote=True)
    return (f"{START}\n"
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="GoatConf">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{IMAGE}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="GoatConf 2027, Tuzla, 3–5 June 2027, free. The GoatConf seal: the one that feeds the community.">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f"{END}\n")


ASSETS = ("goatconf.css", "album.js")


def version(name: str) -> str:
    path = SITE / name
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8] if path.exists() else "0"


def stamp(text: str) -> str:
    """Point every link to a stylesheet or script at its current version."""
    for name in ASSETS:
        text = re.sub(r'(href|src)="' + re.escape(name) + r'(\?v=[0-9a-f]+)?"', lambda m: f'{m.group(1)}="{name}?v={version(name)}"', text)
    return text


def tag(text: str) -> str:
    """Return the page with its link-preview block added or refreshed, just before the stylesheet,
    and its stylesheet and scripts stamped with their current version."""
    text = BLOCK.sub("", text)
    text = re.sub(r'<link rel="stylesheet" href="goatconf\.css(\?v=[0-9a-f]+)?">', '<link rel="stylesheet" href="goatconf.css">', text)
    anchor = '<link rel="stylesheet" href="goatconf.css">'
    return stamp(text.replace(anchor, tags(text) + anchor, 1))


def pages():
    return sorted(p for p in SITE.glob("*.html") if p.name != "404.html")


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    stale = 0
    for p in pages():
        old = p.read_text(encoding="utf-8")
        new = tag(old)
        if cmd == "apply":
            if new != old:
                p.write_text(new, encoding="utf-8")
                print(f"tagged site/{p.name}")
        elif new != old:
            print(f"site/{p.name}: link-preview tags missing or out of date: run python3 tools/meta.py apply")
            stale += 1
    if cmd == "check":
        print(f"link previews: {stale} page(s) need tags")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
