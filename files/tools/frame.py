#!/usr/bin/env python3
"""The frame every page of the site shares: the goat sprite, the footer, and
the page around a generated page's main part.

The generators build their pages with page(). The hand-written pages carry
the footer between <!-- gen:footer tools/frame.py --> and
<!-- /gen:footer --> (the home page carries its back cover's links between
<!-- gen:back-cover-links tools/frame.py --> and its end), which `apply`
writes and `check` checks, as tools/nav.py does for the top bar. The goat
sprite sits right after <body> on every page that uses it (href="#goat"),
and on no other.

  apply     write the footer, the back cover's links and the sprite on every page
  check     fail if a page's footer, links or sprite are not current

Usage: python3 tools/frame.py <apply|check>
(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blocks  # noqa: E402
import goats  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Every page's footer links, in order. The home page's back cover leaves out
# Home and names two of them in full.
LINKS = [("index.html", "Home"), ("program.html", "Program"), ("speakers.html", "Speakers"),
         ("talk.html", "Propose a session"), ("extend.html", "Host an event"), ("register.html", "Register"),
         ("travel.html", "Travel"), ("supporters.html", "Supporters"), ("charter.html", "Charter"),
         ("code-of-conduct.html", "Code of conduct"), ("brand.html", "Brand"),
         ("access.html", "Accessibility"), ("contact.html", "Contact")]
BACK_COVER = {"charter.html": "The charter", "code-of-conduct.html": "The code of conduct"}
LINE = ("GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3–5 June 2027. "
        'Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.')

LINE_GOAT = """<symbol id="goat" viewBox="0 0 124 100">
      <g fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M27 49c-1-11 9-17 24-17.5 14-.5 25 .5 31 5.5 4 3.5 5.5 10 3.5 16.5-2.5 8-11 11.5-24 11.5-15 0-27-2-31.5-6.5C27.5 56.5 27 53 27 49z" fill="var(--goat-fill, #f2f6f1)"/>
        <path d="M80 39c2-7 5.5-13 10-16.5 4.5-3.5 11-3 14.5 1 3 3.5 5 8 4.5 11-.5 2.5-3 3.5-6 3-3-.5-5 1-6.5 4.5-1.5 3.5-3 6.5-5.5 7.5" fill="var(--goat-fill, #f2f6f1)"/>
        <path d="M93 21c-3-6-8.5-11-15-11.5-3.5-.3-6 1-7 3.5 5-.5 9.5 2.5 13 7.5"/>
        <path d="M97 22.5c-.5-6-4-11-9-13.5"/>
        <path d="M92.5 28c-3.5 1-7 3.5-9.5 3"/>
        <path d="M107 38.5c.5 4-1 9-4 12"/>
        <path d="M35 63l-2.5 22.5M45 64.5l.5 21M69 64.5l2 21M78.5 61.5l3.5 23.5"/>
        <path d="M29.5 45c-5-2-8-6-7-11"/>
      </g>
      <circle cx="99.5" cy="27.5" r="2" fill="currentColor"/>
      <path d="M31 85.5h4M44 85.5h4M69.5 85.5h4M80.5 85h4" stroke="currentColor" stroke-width="4.5" stroke-linecap="round"/>
    </symbol>
"""

# The goat mascot (ADR wiki/org/adrs/goat-mascot.md): one flat goat drawn in
# parts, cream coat, ink outline, yellow horns curled back. A peek shows its
# horns, ears, eyes and front hooves over an open slot's top edge; a role is a
# small layer on the same goat. PEEK_BY_KIND says which role each kind of slot
# gets. The faint line goat (#goat) stays until every slot peeks.
INK = goats.INK
_LINE = goats.LINE
GOAT_PARTS = (f'<g id="gm-horns">{goats.HORNS}</g>\n      <g id="gm-ears">{goats.EARS}</g>\n      '
              f'<g id="gm-face">{goats.HEAD}{goats.CURL}{goats.BLUSHES}{goats.EYES}</g>\n      '
              f'<g id="gm-hooves"><rect x="52" y="80" width="22" height="12" rx="6" fill="{INK}"/><rect x="126" y="80" width="22" height="12" rx="6" fill="{INK}"/></g>\n      '
              '<clipPath id="gm-edge"><rect x="0" y="-10" width="200" height="96"/></clipPath>')
# Each role's layers: those on the head (in the head's own coordinates) and
# those in front, held over the edge.
ROLES = {
    "goat": ("", ""),
    "speaker": ("", f'<path d="M62 84 48 62" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="45" cy="57" r="8" fill="#ffd400" {_LINE}/><path d="M30 46q-6 8 0 16M22 40q-11 14 0 28" fill="none" stroke="#ffd400" stroke-width="3" stroke-linecap="round"/>'),
    "host": (f'<path d="M84 50l4-22h24l4 22z" fill="#d7263d" {_LINE}/><path d="M100 28c6 2 9 9 8 18" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
             f'<path d="M128 62h22l-3 14a8 8 0 0 1-8 6 8 8 0 0 1-8-6z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M131 68h16" stroke="#2f6fd6" stroke-width="3"/><path d="M135 56c-3-4 3-6 0-10M142 56c-3-4 3-6 0-10" fill="none" stroke="#9aa9c7" stroke-width="2.5" stroke-linecap="round"/>'),
    "coder": (f'<g fill="none" stroke="{INK}" stroke-width="3"><circle cx="82" cy="90" r="14"/><circle cx="118" cy="90" r="14"/><path d="M96 89h8"/></g>',
              f'<rect x="66" y="78" width="68" height="10" rx="2" fill="#ffd400" {_LINE}/>'),
    "pirate": (f'<path d="M56 60C66 22 134 22 144 60c-12-8-30-8-44-2-14-6-32-6-44 2z" fill="#0b3d91" {_LINE}/><path d="M62 55c12-7 30-7 38-1 8-6 26-6 38 1" fill="none" stroke="#ffd400" stroke-width="3" stroke-linecap="round"/><path d="M60 74l78 24" stroke="{INK}" stroke-width="3"/><ellipse cx="118" cy="91" rx="13" ry="12" fill="{INK}"/>', ""),
}
# The hidden goat, as the man in Tuzla hid his: only its horns, ears and the
# top of its eyes show, and no hooves.
PEEK_HIDDEN = '<symbol id="peek-hidden" viewBox="0 -6 200 98"><g clip-path="url(#gm-edge)"><g transform="translate(0 -10)"><use href="#gm-ears"/><use href="#gm-horns"/><use href="#gm-face"/></g></g></symbol>'
# Which role peeks over each kind of open slot (ADR § Decision 2).
PEEK_BY_KIND = {"session": "speaker", "talk": "speaker", "panel": "speaker", "podcast": "speaker", "karaoke": "speaker",
                "event": "host", "evening-event": "host", "meetup": "host", "workshop": "coder", "hackathon": "coder",
                "trip": "pirate", "other": "hidden"}


def _peek_symbol(role: str) -> str:
    head, front = ROLES[role]
    return (f'<symbol id="peek-{role}" viewBox="0 -6 200 98"><g clip-path="url(#gm-edge)"><g transform="translate(0 -24)">'
            f'<use href="#gm-ears"/><use href="#gm-horns"/><use href="#gm-face"/>{head}</g></g><use href="#gm-hooves"/>{front}</symbol>')


def peek(kind: str = "") -> str:
    """The goat peeking over an open slot, in the role its kind gets."""
    role = PEEK_BY_KIND.get(kind, "goat")
    return f'<svg class="peek" aria-hidden="true" focusable="false" viewBox="0 -6 200 98"><use href="#peek-{role}"/></svg>'


SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
          + LINE_GOAT + "\n      " + GOAT_PARTS + "\n      " + "".join(_peek_symbol(r) for r in ROLES) + PEEK_HIDDEN + "\n    </defs></svg>")


def block(name: str, body: str) -> str:
    return blocks.wrap(name, "tools/frame.py", body)


def links(back_cover: bool = False) -> str:
    return " ".join(f'<a href="{href}">{BACK_COVER.get(href, label) if back_cover else label}</a>'
                    for href, label in LINKS if not (back_cover and href == "index.html"))


def footer() -> str:
    return block("footer", f"""<footer class="footer">
  <p>{LINE}</p>
  <p class="footer__links">{links()}</p>
  {nav.follow()}
</footer>""")


def back_cover_links() -> str:
    return block("back-cover-links", f'    <p class="back-cover__links">{links(back_cover=True)}</p>')


def page(canonical: str, title: str, description: str, photo, h1: str, lede: str, main: str, made_by: str,
         preview: str = "", photo_class: str = "", photo_style: str = "") -> str:
    """A generated page around its main part: head, sprite, page head, main, footer."""
    src, width, height, alt = photo
    image = f'\n<link rel="image_src" href="https://goatconf.com/share/{preview}">' if preview else ""
    return frame(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0b3d91">
<link rel="canonical" href="https://goatconf.com/{canonical}">{image}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="goatconf.css">
</head>
<body>
<!-- Generated by {made_by}. Edit the records, not this page. -->
<main id="main">
<div class="page-head">
  <img class="page-head__photo{photo_class}"{photo_style} src="{src}" width="{width}" height="{height}" alt="{alt}" decoding="async">
  <h1 class="sign">{h1}</h1>
  <p class="lede">{lede}</p>
</div>
{main}
</main>
{footer()}
<script src="album.js" defer></script>
</body>
</html>
""")


SPRITE_RE = re.compile(r'<svg width="0" height="0" style="position:absolute".*?</svg>\n', re.S)
BODY = re.compile(r"<body[^>]*>\n")


def frame(text: str) -> str:
    """The page with its sprite (only where it is used), footer and back cover's links current."""
    text = SPRITE_RE.sub("", text)
    if 'href="#goat"' in text or 'href="#peek-' in text:
        m = BODY.search(text)
        if not m:
            raise ValueError("no <body> tag on its own line to put the sprite after")
        text = text[:m.end()] + SPRITE + "\n" + text[m.end():]
    for name, make in (("footer", footer), ("back-cover-links", back_cover_links)):
        text = blocks.pattern(name).sub(lambda _m: make(), text)
    return text


def pages():
    return sorted(SITE.glob("*.html"))


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["check"])[0]
    stale = 0
    for p in pages():
        old = p.read_text(encoding="utf-8")
        try:
            new = frame(old)
        except ValueError as err:
            print(f"site/{p.name}: {err}")
            stale += 1
            continue
        missing = "gen:back-cover-links" if p.name == "index.html" else "gen:footer"
        if missing not in new:
            print(f"site/{p.name} has no <!-- {missing} tools/frame.py --> block")
            stale += 1
        if cmd == "apply" and new != old:
            p.write_text(new, encoding="utf-8")
            print(f"wrote the frame into site/{p.name}")
        elif cmd != "apply" and new != old:
            print(f"site/{p.name}: the frame is out of date: run python3 tools/frame.py apply")
            stale += 1
    if cmd != "apply" and not stale:
        print("the frame is current on every page")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
