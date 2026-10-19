#!/usr/bin/env python3
"""The top bar: one navigation for every page of the site.

The bar sits between <!-- topbar --> and <!-- /topbar --> in each page and
marks the page you are on. The same pass writes GoatConf's social accounts
(SOCIAL) into each footer, after its links, and into any <!-- follow -->
spot, such as the one on the contact page. The generators (program, extensions, speakers)
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
# GoatConf's own accounts, live on 2026-10-15 (sources/web/social/goatconf-linkedin-2026-10-15.md,
# sources/web/social/goatconf-x-2026-10-15.md). Icons: Simple Icons, CC0.
SOCIAL = (
    ("LinkedIn", "https://www.linkedin.com/company/goatconf/",
     "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"),
    ("X", "https://x.com/goatconf",
     "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"),
)
FOLLOW = re.compile(r"<!-- follow -->.*?<!-- /follow -->", re.S)
FOOTER_LINKS = re.compile(r'(<footer\b.*?<p class="(?:footer|back-cover)__links">.*?</p>)', re.S)
LINKS = [("program.html", "Program"), ("speakers.html", "Speakers"), ("travel.html", "Travel"), ("supporters.html", "Supporters")]
ACTIONS = [("talk.html", "Propose a session", "topbar__cta"), ("register.html", "Register", "topbar__cta topbar__cta--main")]


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


def follow() -> str:
    """GoatConf's accounts as small labelled icons, for every footer and any <!-- follow --> spot."""
    links = " ".join(f'<a class="follow__link" href="{url}"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}"/></svg>{name}</a>'
                     for name, url, path in SOCIAL)
    return f'<!-- follow --><p class="follow"><span class="follow__label">Follow GoatConf</span> {links}</p><!-- /follow -->'


def place(text: str, current: str) -> str:
    """Put the bar right after the sprite (or <body>), replacing an old one, and the follow links
    in the footer, after its links, and in any <!-- follow --> spot."""
    text = BLOCK.sub("", text)
    m = re.search(r"<body[^>]*>\n(<svg width=\"0\".*?</svg>\n)?", text, re.S)
    if not m:
        raise ValueError("no <body> tag on its own line to put the top bar after")
    text = text[:m.end()] + bar(current) + text[m.end():]
    text = FOLLOW.sub(lambda _m: follow(), text)
    footer = FOOTER_LINKS.search(text)
    if footer and "<!-- follow -->" not in text[footer.start():text.find("</footer>", footer.start())]:
        text = text[:footer.end()] + "\n  " + follow() + text[footer.end():]
    return text


def pages():
    return sorted(SITE.glob("*.html"))


def section(name: str) -> str:
    """The link a page marks as current: a speaker's own page sits under Speakers,
    a supporter's under Supporters, an event's or a session's under Program."""
    if name.startswith("speaker-"):
        return "speakers.html"
    if name.startswith("supporter-"):
        return "supporters.html"
    return "program.html" if name.startswith(("event-", "session-")) else name


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    stale = 0
    for p in pages():
        old = p.read_text(encoding="utf-8")
        try:
            new = place(old, section(p.name))
        except ValueError as err:
            print(f"site/{p.name}: {err}")
            stale += 1
            continue
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
