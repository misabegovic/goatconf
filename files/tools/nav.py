#!/usr/bin/env python3
"""The top bar: one navigation for every page of the site.

The bar sits between <!-- topbar --> and <!-- /topbar --> in each page and
marks the page you are on. The generators (program, extensions, speakers)
call bar() for their own pages.

  apply   write or refresh the bar in every site/*.html
  check   fail if a page's bar is missing or out of date

Usage: python3 tools/nav.py <apply|check>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
START, END = "<!-- topbar -->", "<!-- /topbar -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
LINKS = [("program.html", "Program"), ("speakers.html", "Speakers"), ("travel.html", "Travel"), ("supporters.html", "Supporters")]
ACTIONS = [("talk.html", "Give a talk", "topbar__cta"), ("register.html", "Register", "topbar__cta topbar__cta--main")]


def bar(current: str) -> str:
    def a(href, label, cls=""):
        attrs = f' class="{cls}"' if cls else ""
        here = ' aria-current="page"' if href == current else ""
        return f'<a{attrs} href="{href}"{here}>{label}</a>'
    links = "\n    ".join(a(h, l) for h, l in LINKS)
    actions = "\n    ".join(a(h, l, c) for h, l, c in ACTIONS)
    return f"""{START}
<a class="skip" href="#main">Skip to the content</a>
<header class="topbar">
  <a class="topbar__home" href="index.html" aria-label="GoatConf home"><img class="topbar__coin" src="brand/coin.svg" width="36" height="36" alt="">GoatConf <span class="topbar__year">2027</span></a>
  <nav aria-label="Main">
    {links}
    {actions}
  </nav>
</header>
{END}
"""


def place(text: str, current: str) -> str:
    """Put the bar right after the sprite (or <body>), replacing an old one."""
    text = BLOCK.sub("", text)
    m = re.search(r"<body>\n(<svg width=\"0\".*?</svg>\n)?", text, re.S)
    return text[:m.end()] + bar(current) + text[m.end():]


def pages():
    return sorted(SITE.glob("*.html"))


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    stale = 0
    for p in pages():
        old = p.read_text(encoding="utf-8")
        new = place(old, p.name)
        if cmd == "apply":
            if new != old:
                p.write_text(new, encoding="utf-8")
                print(f"wrote the top bar into site/{p.name}")
        elif new != old:
            print(f"site/{p.name}: top bar missing or out of date: run python3 tools/nav.py apply")
            stale += 1
    if cmd == "check":
        print(f"top bar: {stale} page(s) out of date")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
