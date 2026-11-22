#!/usr/bin/env python3
"""The top bar: one navigation for every page of the site.

The bar sits between <!-- gen:topbar tools/nav.py --> and its end in each page and
marks the page you are on. The same pass writes GoatConf's social accounts
(SOCIAL) into each footer, after its links, and into any <!-- gen:follow -->
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blocks  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
START, END = blocks.marks("topbar", "tools/nav.py")
BLOCK = blocks.pattern("topbar", trailing_newline=True)
# GoatConf's own accounts, live on 2026-10-15 (sources/web/social/goatconf-linkedin-2026-10-15.md,
# sources/web/social/goatconf-x-2026-10-15.md). Icons: Simple Icons, CC0.
SOCIAL = (
    ("LinkedIn", "https://www.linkedin.com/company/goatconf/",
     "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"),
    ("X", "https://x.com/goatconf",
     "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"),
)
FOLLOW = blocks.pattern("follow")
FOOTER_LINKS = re.compile(r'(<footer\b.*?<p class="(?:footer|back-cover)__links">.*?</p>)', re.S)
LINKS = [("program.html", "Program"), ("speakers.html", "Speakers"), ("travel.html", "Travel"), ("supporters.html", "Supporters")]
# Register is the bar's one button. The two doors are plain links on wide screens, so the bar has one ask, and
# stay buttons in the phone menu, as the organiser set them (sources/conversations/2026-10-23--org--phone-menu.md,
# sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md).
DOORS = [("extend.html", "Host an event"), ("talk.html", "Propose a session")]
REGISTER = ("register.html", "Register")


# The visitor's theme (sources/conversations/2026-11-21--org--minimal-chosen-phone-hooves-light-and-dark.md): the
# site follows the system setting; a stored choice of light or dark is put on <html> before the page paints. The
# control is three radio buttons in a labelled group, hidden until the script shows it, so with scripting off it
# is not there and the system setting still applies.
THEME_BOOT = ('<script>try{var t=localStorage.getItem("theme");if(t==="light"||t==="dark")'
              'document.documentElement.dataset.theme=t}catch(e){}</script>')
# The sections of a page that open and close (site/album.js; a page opts in with data-folds on its main). Before the
# page is painted this marks which sections are closed, so nothing shows and then vanishes: a section is closed unless
# its markup says it starts open (data-fold="open") or never closes (data-fold="never"), and what the visitor last
# chose, kept in this browser under the key "folds" beside "theme", wins over both. A link to a section opens it. It
# marks each section as the parser adds it, which is before the first paint. Without the script nothing is closed.
# If site/album.js never arrives, everything opens again when the page has loaded, so nothing is left shut with no control.
# Nothing is sent anywhere (sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md).
FOLD_BOOT = ('<script>(function(){try{var d=document,h=d.documentElement,f={},x="";'
             'try{x=decodeURIComponent(location.hash.slice(1))}catch(e){}'
             'try{var p=(location.pathname.split("/").pop()||"index").replace(/\\.html$/,"")||"index",'
             'a=JSON.parse(localStorage.getItem("folds")||"{}");if(a&&a[p]&&typeof a[p]==="object")f=a[p]}catch(e){}'
             'h.classList.add("folds-on");'
             'var o=new MutationObserver(function(m){for(var i=0;i<m.length;i++)for(var j=0;j<m[i].addedNodes.length;j++){'
             'var n=m[i].addedNodes[j];if(n.nodeType!==1||!n.id)continue;'
             'if(n.tagName==="SECTION"&&n.parentNode&&n.parentNode.hasAttribute("data-folds")&&n.getAttribute("data-fold")!=="never"){'
             'var s=f[n.id]==="open"||f[n.id]==="closed"?f[n.id]:n.getAttribute("data-fold")==="open"?"open":"closed";'
             'if(s==="closed"&&x!==n.id)n.classList.add("is-closed")}'
             'else if(n.tagName==="DETAILS"&&n.classList.contains("photo-fold")&&f[n.id]==="open")n.open=true}});'
             'o.observe(h,{childList:true,subtree:true});'
             'd.addEventListener("DOMContentLoaded",function(){o.disconnect()});'
             'addEventListener("load",function(){if(!h.classList.contains("folds-ready"))h.classList.remove("folds-on")})'
             '}catch(e){}})()</script>')


def theme_control(where: str) -> str:
    opts = "".join(f'<input type="radio" name="theme-{where}" id="theme-{where}-{v}" value="{v}"{" checked" if v == "system" else ""}>'
                   f'<label for="theme-{where}-{v}">{label}</label>' for v, label in (("system", "System"), ("light", "Light"), ("dark", "Dark")))
    return f'<fieldset class="theme" data-theme-control hidden><legend>Theme</legend>{opts}</fieldset>'


def bar(current: str) -> str:
    def a(href, label, cls=""):
        attrs = f' class="{cls}"' if cls else ""
        here = ' aria-current="page"' if href == current else ""
        return f'<a{attrs} href="{href}"{here}>{label}</a>'
    links = "\n    ".join(a(h, l) for h, l in LINKS + DOORS)
    actions = a(*REGISTER, "topbar__cta")
    # On phones the bar is the mark, Register and a Menu that opens every link, the three actions as buttons at
    # the end, Register filled (the organiser, 2026-10-23, sources/conversations/2026-10-23--org--phone-menu.md).
    # Register sits beside Menu so it is one tap away wherever the page is scrolled to. A <details> opens the
    # menu without a script.
    panel = "\n        ".join(a(h, l) for h, l in LINKS)
    panel_actions = "\n          ".join([a(h, l, "topbar__panel-cta") for h, l in DOORS] + [a(*REGISTER, "topbar__panel-main")])
    register = a(*REGISTER, "topbar__register")
    return f"""{START}
{THEME_BOOT}{FOLD_BOOT}
<a class="skip" href="#main">Skip to the content</a>
<header class="topbar">
  <a class="topbar__home" href="index.html" aria-label="GoatConf home"><img class="topbar__coin" src="brand/coin.svg" width="36" height="36" alt="">GoatConf <span class="topbar__year">2027</span></a>
  <nav class="topbar__wide" aria-label="Main">
    {links}
    {actions}
  </nav>
  <div class="topbar__phone">
    {register}
    <details class="topbar__menu">
      <summary><span class="topbar__open">Menu</span><span class="topbar__close">Close</span></summary>
      <nav class="topbar__panel" aria-label="Menu">
        {panel}
        <p class="topbar__panel-actions">
          {panel_actions}
        </p>
        {theme_control("menu")}
      </nav>
    </details>
  </div>
</header>
{END}
"""


def follow() -> str:
    """GoatConf's accounts as small labelled icons, for every footer and any <!-- gen:follow --> spot."""
    links = " ".join(f'<a class="follow__link" href="{url}"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="{path}"/></svg>{name}</a>'
                     for name, url, path in SOCIAL)
    return blocks.wrap("follow", "tools/nav.py", f'<p class="follow"><span class="follow__label">Follow GoatConf</span> {links}</p>', sep="")


def place(text: str, current: str) -> str:
    """Put the bar right after the sprite (or <body>), replacing an old one, and the follow links
    in the footer, after its links, and in any <!-- gen:follow --> spot."""
    text = BLOCK.sub("", text)
    m = re.search(r"<body[^>]*>\n(<svg width=\"0\".*?</svg>\n)?", text, re.S)
    if not m:
        raise ValueError("no <body> tag on its own line to put the top bar after")
    text = text[:m.end()] + bar(current) + text[m.end():]
    text = FOLLOW.sub(lambda _m: follow(), text)
    footer = FOOTER_LINKS.search(text)
    if footer and "<!-- gen:follow " not in text[footer.start():text.find("</footer>", footer.start())]:
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
