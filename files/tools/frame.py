#!/usr/bin/env python3
"""The frame every page of the site shares: the goat mascot, the footer, and
the page around a generated page's main part.

The generators build their pages with page(). The hand-written pages carry
the footer between <!-- gen:footer tools/frame.py --> and
<!-- /gen:footer --> (the home page carries its back cover's links between
<!-- gen:back-cover-links tools/frame.py --> and its end), which `apply`
writes and `check` checks, as tools/nav.py does for the top bar. The goat
is the illustrated mascot in site/img/goat/, which peek() and sitting() place.

  apply     write the footer and the back cover's links on every page
  check     fail if a page's footer or links are not current

Usage: python3 tools/frame.py <apply|check>
(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blocks  # noqa: E402
import goat_atlas  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# Every page's footer links, in order. The home page's back cover leaves out
# Home and names two of them in full.
LINKS = [("index.html", "Home"), ("program.html", "Program"), ("speakers.html", "Speakers"),
         ("talk.html", "Propose a session"), ("extend.html", "Host an event"), ("register.html", "Register"),
         ("travel.html", "Travel"), ("supporters.html", "Supporters"), ("charter.html", "Charter"),
         ("code-of-conduct.html", "Code of conduct"), ("brand.html", "Brand"), ("stickers.html", "Stickers"),
         ("access.html", "Accessibility"), ("contact.html", "Contact")]
BACK_COVER = {"charter.html": "The charter", "code-of-conduct.html": "The code of conduct"}
LINE = ("GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3–5 June 2027. "
        'Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.')

# The goat mascot (ADR wiki/org/adrs/goat-mascot.md): the illustrated
# watercolour goat, painted from its sprite sheet (tools/goat_atlas.py) with its
# closed eyes laid over it for a blink. It peeks over every open slot, in the
# role the slot's kind gets, and sits where a speaker or a venue has no photo yet.
# Which role peeks over each kind of open slot (ADR § Decision 2).
PEEK_BY_KIND = {"session": "speaker", "talk": "speaker", "panel": "speaker", "podcast": "speaker", "karaoke": "speaker",
                "event": "host", "evening-event": "host", "meetup": "host", "workshop": "coder", "hackathon": "coder",
                "trip": "pirate", "food": "cook", "other": "hidden"}


def _beat(key: str) -> int:
    """Each goat blinks on its own beat, so a row of goats never blinks at once."""
    return sum(map(ord, key)) % 7


def sitting() -> str:
    """The whole goat, sitting, where a speaker or a venue has no photo yet."""
    return goat_atlas.goat("sitting", "goat-sit")


def peek(kind: str = "") -> str:
    """The goat peeking over an open slot, its hooves on the edge, in the role the slot's kind gets."""
    role = PEEK_BY_KIND.get(kind)
    return goat_atlas.goat(f"peek-{role}" if role else "peeking", "peek peek--art", _beat(kind or "peeking"))


def speaker_peek(slug: str) -> str:
    """A speaker's own painted goat peeking over their card, or the speaker goat while theirs is not painted yet."""
    pose = f"speaker-{slug}"
    if goat_atlas.has(pose):
        return goat_atlas.goat(pose, "peek peek--face", _beat(slug))
    return goat_atlas.goat("peek-speaker", "peek peek--face", _beat(slug))


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


PHOTO_RE = re.compile(r'(<figure class="sticker sticker--photo"[^>]*>)(.*?)(</figure>)', re.S)
SCENE_RE = re.compile(r'<span class="goat goat-scene"[^>]*>.*?</span>')


def scenes(text: str) -> str:
    """Each Tuzla or food photo with a painted scene carries it, for the companion goat to visit (ADR goat-mascot)."""
    def one(m):
        body = SCENE_RE.sub("", m.group(2))
        src = re.search(r'<img src="([^"]+)"', body)
        poses = goat_atlas.SCENES.get(src.group(1), ()) if src else ()
        return m.group(1) + body + "".join(goat_atlas.goat(p, "goat-scene", _beat(p)) for p in poses) + m.group(3)
    return PHOTO_RE.sub(one, text)


GOAT_SPOT_RE = re.compile(r"(<!-- gen:goat-([a-z+-]+) tools/frame.py -->).*?(<!-- /gen:goat-\2 -->)", re.S)


def spots(text: str) -> str:
    """A goat a page places by hand, between <!-- gen:goat-POSE tools/frame.py --> and its end: a scene (the waving
    goat) or a goat peeking over the element it sits in (ADR goat-mascot)."""
    def one(m):
        # Several poses joined by "+" are one spot the companion shows a different one of each visit.
        out = ""
        for pose in m.group(2).split("+"):
            scene = goat_atlas.sheet_of(pose) == "scenes"
            out += goat_atlas.goat(pose, "goat-scene" if scene else "peek peek--art", _beat(pose))
        return m.group(1) + out + m.group(3)
    return GOAT_SPOT_RE.sub(one, text)


def frame(text: str) -> str:
    """The page with its footer and back cover's links current, its photos' goat scenes, and no goat sprite left
    from before."""
    text = spots(scenes(SPRITE_RE.sub("", text)))
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
