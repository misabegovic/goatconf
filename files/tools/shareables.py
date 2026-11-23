#!/usr/bin/env python3
"""GoatConf shareables: banners, covers, link previews and posts, in one look.

Every image is an HTML card in the site's own type and colours, with the seal
from site/brand/, rendered to PNG by headless Chrome into site/share/:

  banners   LinkedIn profile banner, LinkedIn page cover (4200 x 700), a 3:1 header for
            X, Bluesky and Mastodon, the Luma event cover
  og.png    the link preview every page uses
  posts     save the date, run a session, registration, add something,
            the first speakers and the drumbeat's posts to June 2027, some
            with a credited photo of Tuzla, each square (1080) and wide (1200 x 675)
  records   an "I'm speaking" card per published speaker (square, wide, and a
            1200 x 630 preview that their page's link preview shows) and
            GoatConf's "Confirmed speaker" card announcing them (square and wide), a
            "thank you" card and a "proud supporter" card per supporter, and a card per accepted event
            (square, wide, and a 1200 x 630 preview for the event's page),
            built from speakers/, supporters/ and extensions/

  render [--only NAME]   write the PNG files (needs Chrome and Pillow)
  list                   print what would be rendered

Usage: python3 tools/shareables.py <render|list> [--only NAME]
"""

from __future__ import annotations

import argparse
import io
import math
import re
import html
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand  # noqa: E402
import extensions  # noqa: E402
import goat_atlas  # noqa: E402
import program  # noqa: E402
import speakers  # noqa: E402

# the core days' times, from the program's day plan
THURSDAY, FRIDAY = (program.DAY_PLAN[d] for d in program.CORE_DAYS)

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "share"
# The cards take the site's chosen look (sources/conversations/2026-11-21--org--minimal-chosen-phone-hooves-light-and-dark.md)
# and come in two versions (sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md). The light
# card is paper with hoof marks, blue lettering and ink text; it keeps the name it always had, so no shared link
# breaks. The dark card is the same card on the night ground with pale lettering, its name ending in -dark. Both keep
# the seal and the yellow rule along the foot. The values are DESIGN.md's theme tokens.
YELLOW, NIGHT = brand.YELLOW, brand.NIGHT
THEMES = {
    "light": {"BLUE": brand.BLUE, "SOFT": "#46557a", "PAPER": "#edf2fb", "INK": brand.INK,
              "ACCENT": brand.BLUE, "HOOF": "0b3d91", "HOOF_A": ".13"},
    "dark": {"BLUE": "#f3f6ff", "SOFT": "#b6c5e8", "PAPER": "#051534", "INK": "#e8eefc",
             "ACCENT": "#a9c4ff", "HOOF": "a9c4ff", "HOOF_A": ".1"},
}
FACTS = "Tuzla · 3–5 June 2027 · Free to attend"
URL = "goatconf.com"
esc = html.escape


def hooves(fill: str, alpha: str) -> str:
    return ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E"
            f"%3Cg fill='%23{fill}' fill-opacity='{alpha}'%3E%3Cpath d='M30 40c-5 0-7 6-7 11s3 8 6 8c2 0 2-2 2-3z'/%3E"
            "%3Cpath d='M34 40c5 0 7 6 7 11s-3 8-6 8c-2 0-2-2-2-3z'/%3E%3Cpath d='M112 104c-5 0-7 6-7 11s3 8 6 8c2 0 2-2 2-3z'/%3E"
            "%3Cpath d='M116 104c5 0 7 6 7 11s-3 8-6 8c-2 0-2-2-2-3z'/%3E%3C/g%3E%3C/svg%3E\")")


def use(theme: str) -> None:
    """The colours every card built after this call is drawn in: "light" or "dark"."""
    global THEME, BLUE, SOFT, PAPER, INK, ACCENT, HOOVES
    t = THEMES[theme]
    THEME, BLUE, SOFT, PAPER, INK, ACCENT = theme, t["BLUE"], t["SOFT"], t["PAPER"], t["INK"], t["ACCENT"]
    HOOVES = hooves(t["HOOF"], t["HOOF_A"])


use("light")


dark = extensions.dark_card


def goat_src(pose: str) -> str:
    """A painted goat for a card: its master where the masters are (the organiser's machine), else the copy the
    site already publishes."""
    master = goat_atlas.ART / (pose + ".webp")
    return (master if master.exists() else SITE / "img" / "goat" / (pose + ".webp")).as_uri()


def missing(doc: str) -> list[str]:
    """The local pictures a card's page names that are not on this machine: such a card is not rendered."""
    import urllib.parse
    paths = (urllib.parse.unquote(urllib.parse.urlparse(u).path) for u in re.findall(r'(?:src="|url\(["\']?)(file://[^"\')]+)', doc))
    return sorted({p for p in paths if not Path(p).exists()})


def page(w: int, h: int, body: str, bg: str | None = None, hoofs: str | None = None, rule: bool = True) -> str:
    """A card's page. `bg` and `hoofs` replace the theme's ground and hoof marks, and without `rule` the yellow rule
    along the foot is left to the card, which draws its own yellow band."""
    bg = bg or PAPER
    hoofs = hoofs or HOOVES
    fonts = (SITE / "fonts").as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; }}
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin-ext.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; unicode-range: U+0100-02BA; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{fonts}/atkinson-latin.woff2") format("woff2"); font-weight: 200 800; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{fonts}/atkinson-latin-ext.woff2") format("woff2"); font-weight: 200 800; unicode-range: U+0100-02BA; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{ background: {bg} {hoofs}; color: {INK}; font-family: "Atkinson Hyperlegible Next", sans-serif; position: relative; }}
.word {{ color: {BLUE}; font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 75%; line-height: .86; letter-spacing: .005em; text-transform: uppercase; }}
.sub {{ font-family: "Bricolage Grotesque"; font-weight: 700; font-stretch: 85%; color: {ACCENT}; }}
body::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: {max(8, h // 60) if rule else 0}px; background: {YELLOW}; }}
.disp {{ font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 75%; line-height: .86; letter-spacing: .005em; text-transform: uppercase; }}
.tab {{ display: inline-block; background: {YELLOW}; color: {NIGHT}; font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 80%; line-height: 1; text-transform: uppercase; border-radius: .22em; padding: .16em .34em .2em; }}
.fit {{ white-space: nowrap; overflow: hidden; }}
.url {{ font-weight: 700; color: {SOFT}; }}
.seal {{ position: absolute; display: block; }}
.rule {{ height: 6px; background: {YELLOW}; border-radius: 3px; }}
</style></head><body>{body}</body></html>"""


def seal(size: int, style: str, which: str = "seal.svg") -> str:
    return f'<img class="seal" src="{(SITE / "brand" / which).as_uri()}" width="{size}" height="{size}" style="{style}" alt="">'


# The cards' look (sources/conversations/2026-11-23--org--speaker-cards-photo-first.md, chosen for the speaker cards,
# and sources/conversations/2026-11-23--org--other-cards-follow-the-speaker-cards.md, for the rest): what the card is
# about first, as a sticker tilted like the album's, on a yellow block; lettering in two tones, as large as its room
# allows; a yellow band along the foot with the date, the town and "Free" in a dark pill. The light card is on paper,
# the dark one on the album's blue: per version the ground, its hoof marks, the first and second tone of the
# lettering, the text, the accent line and the wordmark. The banners and the covers follow
# (sources/conversations/2026-11-23--org--banners-and-covers-follow.md), and the site's link preview and the Goatchi
# card (sources/conversations/2026-11-23--org--link-preview-and-goatchi-follow.md).
CARD_TONES = {
    "light": ("#edf2fb", ("0b3d91", ".13"), brand.INK, brand.BLUE, brand.INK, brand.BLUE, brand.BLUE),
    "dark": (brand.BLUE, ("ffffff", ".07"), "#ffffff", YELLOW, "#ffffff", YELLOW, "#ffffff"),
}
CARD_TILT = -2.5
CARD_WHEN = "3–5 June 2027 · Tuzla"
# The generic goat of a card that is about no speaker: the plain one, sitting.
CARD_GOAT = "sitting"
# Lettering marked data-fit is set at its largest size and stepped down until it fits its line; lines that share a
# data-group then take the smallest of their sizes, so a title's lines stay one size. It runs once the fonts are in.
FIT = """<script>
document.fonts.ready.then(() => {
  const groups = {};
  document.querySelectorAll('[data-fit]').forEach(el => {
    let s = parseFloat(getComputedStyle(el).fontSize);
    const min = parseFloat(el.dataset.fit) || 40;
    while (el.scrollWidth > el.clientWidth && s > min) { s -= 2; el.style.fontSize = s + 'px'; }
    if (el.dataset.group) (groups[el.dataset.group] = groups[el.dataset.group] || []).push([el, s]);
  });
  Object.values(groups).forEach(g => { const m = Math.min(...g.map(x => x[1])); g.forEach(([el]) => { el.style.fontSize = m + 'px'; }); });
});
</script>"""
SUB = "font-family:'Bricolage Grotesque'; font-weight:700; font-stretch:85%; text-wrap:balance"


def card(w: int, h: int, body: str) -> str:
    """A card in the look above: its version's ground and hoof marks, no yellow rule (the band replaces it), and the
    script that fits the lettering."""
    ground, hoof, *_ = CARD_TONES[THEME]
    return page(w, h, body + "\n" + FIT, ground, hooves(*hoof), rule=False)


def wordmark(px: int, colour: str, year: float = 1.0) -> str:
    """GoatConf and the year in its yellow tab, on one line: the top bar's mark. On a banner, where the mark is the
    largest thing, `year` sets the tab's lettering smaller than the name's so the tab stands no taller than the name."""
    return (f'<span class="disp" style="font-size:{px}px; color:{colour}; vertical-align:middle">GoatConf</span>'
            f'<span class="tab" style="font-size:{px * year:.0f}px; margin-left:{px * .22:.0f}px; vertical-align:middle; font-stretch:75%">2027</span>')


def sticker(inner: str, left: int, top: int, wide: int, tall: int, off: int = 18, radius: int = 26, ring: int = 8,
            ground: str = YELLOW) -> str:
    """What a card is about, as a sticker: a rounded shape with a white edge on a yellow block set down and to the
    right, the two tilted together about the sticker's centre. A photo fills it; a logo sits on its own ground."""
    box = f"position:absolute; left:{left}px; top:{top}px; width:{wide}px; height:{tall}px; border-radius:{radius}px"
    return (f'<div style="position:absolute; left:0; top:0; width:0; height:0; transform-origin:{left + wide / 2:.0f}px {top + tall / 2:.0f}px; '
            f'transform:rotate({CARD_TILT}deg)">'
            f'<div style="{box}; background:{YELLOW}; transform:translate({off}px,{off}px)"></div>'
            f'<div style="{box}; overflow:hidden; background:{ground}; box-shadow:0 0 0 {ring}px #fff">{inner}</div></div>')


def snapshot(photo: str, left: int, top: int, size: int, off: int, radius: int, ring: int) -> str:
    """A speaker's photo as a square sticker."""
    return sticker(photo, left, top, size, size, off, radius, ring)


def label(text: str, px: int, left: int, top: int, tilt: float = CARD_TILT) -> str:
    """The yellow tab that says which card this is: on a sticker's lower edge it tilts with the sticker."""
    return (f'<div style="position:absolute; left:{left}px; top:{top}px; transform:rotate({tilt}deg); transform-origin:0 50%">'
            f'<span class="tab" style="font-size:{px}px; box-shadow:0 6px 14px -6px rgb(5 29 71 / .6)">{text}</span></div>')


def foot_band(left: int, band: int, address: str, free: bool, px: int, small: int, lift: int, low: int) -> str:
    """The yellow band along the foot: when and where, "Free" in a dark pill, and the page's address under them."""
    pill = (f' · <span style="background:{NIGHT}; color:{YELLOW}; border-radius:.2em; padding:.03em .3em .06em; margin-left:.06em">Free</span>'
            if free else "")
    return (f'<div style="position:absolute; left:0; right:0; bottom:0; height:{band}px; background:{YELLOW}"></div>'
            f'<div class="disp" style="position:absolute; left:{left}px; bottom:{lift}px; font-size:{px}px; color:{NIGHT}; white-space:nowrap">{CARD_WHEN}{pill}</div>'
            f'<div style="position:absolute; left:{left}px; bottom:{low}px; font-size:{small}px; font-weight:700; color:{NIGHT}">{address}</div>')


def band_square(address: str, free: bool = True) -> str:
    """The foot of a square card: the band, and the seal at its right end."""
    return foot_band(72, 124, address, free, 56, 22, 50, 16) + seal(100, "right:64px; bottom:12px")


def band_wide(address: str, band: int, left: int = 50, free: bool = True) -> str:
    """The foot of a wide card: the seal, then the band's lines."""
    return foot_band(left + 110, band, address, free, 52, 20, 48, 17) + seal(88, f"left:{left}px; bottom:{(band - 88) // 2}px")


def card_goat(tall: int, place: str) -> tuple[str, float]:
    """The plain goat sitting on a card that is about no speaker, and how wide it stands; nothing where its picture
    is not on this machine's atlas."""
    if not goat_atlas.has(CARD_GOAT):
        return "", 0
    shape = goat_atlas.manifest()[CARD_GOAT]
    wide = tall * shape["w"] / shape["h"]
    return f'<img src="{goat_src(CARD_GOAT)}" style="position:absolute; {place}; width:{wide:.0f}px">', wide


def two_tone(words: str, first: str, second: str) -> str:
    """A name in the card's two tones: its first word, then the rest."""
    head, _, rest = words.partition(" ")
    return f'<span style="color:{first}">{esc(head)}</span>' + (f' <span style="color:{second}">{esc(rest)}</span>' if rest else "")


def title_lines(title: str, px: int, first: str, second: str, least: int = 70, most: int = 0) -> str:
    """A title on its set lines, every line one size, the last line in the second tone. With `most`, the lines
    before the last are joined until no more than that many are left."""
    lines = [t.strip() for t in title.split("<br>")]
    while most and len(lines) > most:
        lines[:2] = [f"{lines[0]} {lines[1]}"]
    return "".join(
        f'<div class="disp fit" data-fit="{least}" data-group="title" style="font-size:{px}px; '
        f'color:{second if (i == len(lines) - 1 and len(lines) > 1) else first}; margin-top:{6 if i else 0}px">{line}</div>'
        for i, line in enumerate(lines))


def title_line(title: str, first: str, second: str) -> str:
    """A title on one line: its last set line, or its last word, in the second tone."""
    parts = [t.strip() for t in title.split("<br>")]
    if len(parts) == 1:
        head, _, tail = parts[0].rpartition(" ")
        parts = [head, tail] if head else parts
    if len(parts) == 1:
        return f'<span style="color:{first}">{parts[0]}</span>'
    return f'<span style="color:{first}">{" ".join(parts[:-1])}</span> <span style="color:{second}">{parts[-1]}</span>'


TAGLINE = "Any programming language, any stack."


def brand_band(w: int, h: int, left: int, top: int, mark: int, tag: int, band: int, facts: int, small: int,
               goat: int, right: int, band_left: int | None = None, tile: int = 0) -> str:
    """A banner or a cover in the cards' look: the wordmark and the line under it, the yellow band along the foot
    with when, where, "Free" and the address, the seal at the band's right end and the plain goat sitting on the band
    beside it. `left` keeps the lettering clear of what a platform lays over the bottom left (a profile photo, a
    page's logo), and `band_left` does so for the band's lines where only they are covered; `right` keeps the seal
    inside what a phone trims; `tile` sets the hoof marks' size on a very large cover."""
    _, _, _, _, ink, _, colour = CARD_TONES[THEME]
    coin = round(band * .8)
    animal, wide = card_goat(goat, f"right:{right + coin + round(band * .35)}px; bottom:{band - round(goat * .02)}px")
    return card(w, h, f"""
{f'<style>body {{ background-size: {tile}px {tile}px; }}</style>' if tile else ''}
<div style="position:absolute; left:{left}px; top:{top}px; color:{ink}">
  <div style="white-space:nowrap">{wordmark(mark, colour, .72)}</div>
  <div style="{SUB}; font-size:{tag}px; line-height:1.15; margin-top:{round(tag * .6)}px">{TAGLINE}</div>
</div>
{foot_band(left if band_left is None else band_left, band, URL, True, facts, small, round(band * .4), round(band * .13))}
{seal(coin, f"right:{right}px; bottom:{(band - coin) // 2}px")}
{animal}""")


def page_cover(w: int = 4200, h: int = 700) -> str:
    """The LinkedIn company page cover, at LinkedIn's 4200 x 700.

    LinkedIn lays the page's square logo over the bottom left of the cover and
    the phone app trims both sides, so the lettering starts past the logo's quarter
    and the seal sits well inside the right edge."""
    return brand_band(w, h, left=1240, top=84, mark=230, tag=80, band=180, facts=96, small=40, goat=430, right=360, tile=600)


def luma_cover(w: int = 1080, h: int = 1080) -> str:
    """The Luma event's cover: the name on two lines, the line under it, the whole seal beside them, and the plain
    goat sitting on the band. The band carries no second seal."""
    _, _, _, _, ink, _, colour = CARD_TONES[THEME]
    animal, _ = card_goat(400, "right:200px; bottom:118px")
    return card(w, h, f"""
<div style="position:absolute; left:72px; top:84px; color:{ink}">
  <div class="disp" style="font-size:178px; color:{colour}">GoatConf</div>
  <div><span class="tab" style="font-size:150px; font-stretch:75%; margin-top:20px">2027</span></div>
  <div style="{SUB}; font-size:50px; line-height:1.15; margin-top:48px; max-width:520px">{TAGLINE}</div>
</div>
{seal(330, "right:64px; top:72px")}
{animal}
{foot_band(72, 124, URL, True, 56, 22, 50, 16)}""")


def post(w: int, h: int, title: str, line: str, square: bool) -> str:
    """A post of words: the title large on its set lines, its line under it, and the plain goat sitting on the band."""
    _, _, first, second, ink, _, mark = CARD_TONES[THEME]
    if square:
        goat, wide = card_goat(380, "right:56px; bottom:118px")
        return card(w, h, f"""
<div style="position:absolute; left:72px; top:64px; white-space:nowrap">{wordmark(46, mark)}</div>
<div style="position:absolute; left:72px; right:72px; top:176px">{title_lines(title, 190, first, second)}</div>
<div style="position:absolute; left:72px; right:{72 + wide + 30:.0f}px; bottom:190px; color:{ink}">
  <div style="{SUB}; font-size:46px; line-height:1.15">{line}</div>
</div>
{goat}
{band_square(URL)}""")
    band = 116
    goat, wide = card_goat(300, f"right:44px; bottom:{band - 6}px")
    return card(w, h, f"""
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
<div style="position:absolute; left:60px; width:760px; top:54px">{title_lines(title, 136, first, second, 60, most=2)}</div>
<div style="position:absolute; left:60px; right:{44 + wide + 40:.0f}px; bottom:{band + 40}px; color:{ink}">
  <div style="{SUB}; font-size:36px; line-height:1.15">{line}</div>
</div>
{goat}
{band_wide(URL, band, 60)}""")


def goats_post(w: int, h: int, square: bool, crowd_in: bool = True) -> str:
    """The painted goats, as a crowd: the post that shows them off (ADR goat-mascot)."""
    def g(pose, width, style):
        return f'<img src="{goat_src(pose)}" style="position:absolute; width:{width}px; {style}">'
    if square:
        crowd = (g("sticker-salt-lakes", 255, "left:30px; top:392px")
                 + g("sticker-hike", 230, "left:290px; top:372px")
                 + g("sticker-cevapi", 230, "left:540px; top:384px")
                 + g("sticker-pannonian-sea", 250, "right:30px; top:380px")
                 + g("sticker-host", 245, "left:24px; bottom:28px")
                 + g("sticker-coder", 265, "left:278px; bottom:24px")
                 + g("sticker-pirate", 245, "left:552px; bottom:28px")
                 + g("sticker-cook", 230, "right:30px; bottom:30px"))
        return page(w, h, f"""
<div style="position:absolute; left:84px; top:80px; right:84px">
  <div class="word" style="font-size:118px">The goats<br>are in</div>
  <div class="sub" style="font-size:38px; margin-top:26px">goatconf.com</div>
</div>
{seal(190, "right:84px; top:84px")}{crowd if crowd_in else ""}""")
    crowd = (g("sticker-salt-lakes", 230, "left:470px; bottom:250px")
             + g("sticker-hike", 190, "left:700px; bottom:262px")
             + g("sticker-pannonian-sea", 210, "right:40px; bottom:252px")
             + g("sticker-host", 190, "left:470px; bottom:22px")
             + g("sticker-coder", 205, "left:660px; bottom:18px")
             + g("sticker-pirate", 190, "left:870px; bottom:22px")
             + g("sticker-cook", 170, "right:24px; bottom:24px"))
    return page(w, h, f"""
<div style="position:absolute; left:72px; top:72px; width:400px">
  <div class="word" style="font-size:104px">The goats<br>are in</div>
  <div class="sub" style="font-size:32px; margin-top:24px">goatconf.com</div>
</div>
{seal(170, "left:72px; bottom:64px")}{crowd if crowd_in else ""}""")


def goatchi_card(w: int = 1200, h: int = 630, square: bool = False, url: str = "goatconf.com/goatchi.html") -> str:
    """Goatchi's link preview and its post, in the cards' look: its name and what you do, and on the band the goat
    eating burek and the plain goat saying hello."""
    _, _, first, _, ink, _, mark = CARD_TONES[THEME]

    def g(pose, width, style):
        return f'<img src="{goat_src(pose)}" style="position:absolute; width:{width}px; {style}">'

    def baaa(px, style):
        return (f'<div class="sub" style="position:absolute; {style}; padding:{px * .25:.0f}px {px * .58:.0f}px {px * .3:.0f}px; '
                f'border-radius:{px * .7:.0f}px {px * .7:.0f}px {px * .7:.0f}px {px * .13:.0f}px; background:{YELLOW}; color:{NIGHT}; '
                f'font-size:{px}px; font-weight:800">Baaa!</div>')
    words = "Keep a GoatConf goat. Feed it, play with it, let it sleep."
    if square:
        return card(w, h, f"""
<div style="position:absolute; left:72px; top:64px; white-space:nowrap">{wordmark(46, mark)}</div>
<div style="position:absolute; left:72px; right:72px; top:170px; color:{ink}">
  <div class="disp" style="font-size:210px; color:{first}">Goatchi</div>
  <div style="{SUB}; font-size:48px; line-height:1.15; margin-top:34px; max-width:15em">{words}</div>
</div>
{g("sticker-burek", 320, "left:64px; bottom:112px")}
{g(CARD_GOAT, 290, "right:170px; bottom:116px")}
{baaa(46, "right:420px; bottom:410px")}
{band_square(url)}""")
    band = 116 if h >= 675 else 108
    return card(w, h, f"""
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
<div style="position:absolute; left:60px; width:560px; top:70px; color:{ink}">
  <div class="disp" style="font-size:150px; color:{first}">Goatchi</div>
  <div style="{SUB}; font-size:38px; line-height:1.15; margin-top:26px">{words}</div>
</div>
{g("sticker-burek", 250, f"left:610px; bottom:{band - 10}px")}
{g(CARD_GOAT, 270, f"right:50px; bottom:{band - 6}px")}
{baaa(38, f"right:250px; bottom:{band + 330}px")}
{band_wide(url, band, 60)}""")


POSTS = {
    "save-the-date": ("Save<br>the date", "Two days of talks in every room of IPI Academy, then a day for the community."),
    "run-a-session": ("Run a<br>session", "A talk, a panel, a workshop or something else. One hour, one room."),
    "register": ("Get your<br>free ticket", "Thursday and Friday for the talks, Saturday for the community."),
    "add-something": ("Propose<br>an event", "A workshop, a meetup, a dinner, a hike: run it around GoatConf."),
    "first-speakers": ("The first<br>speakers<br>are here", "Eight speakers so far, each with an hour at IPI Academy on 3 or 4 June."),
    # The drumbeat to June 2027 (wiki/org/outreach/drumbeat.md)
    "your-first-talk": ("Your<br>first talk?", "First-time speakers are welcome. A strong idea counts for more than a famous name."),
    "see-you-in-june": ("See you<br>in June", "Two days of talks in Tuzla, then a day for the community."),
    "not-only-engineers": ("Not only<br>engineers", "AI/ML, data, UX/UI, product, research, business, leadership: for people who build and sell software."),
    "support-goatconf": ("Support<br>GoatConf", "One level, 500 euro, online only. Nothing at the venue."),
    "with-or-without-meat": ("With or<br>without<br>meat", "Ask for posno: made without meat."),
    "access": ("Coming with<br>a disability?", "Step-free main hall and first floor. Tell us what you need."),
    "what-we-wont-do": ("What we<br>won't do", "No paid talks, no attendee list for sale, no supporters at the venue."),
    "last-call": ("Last call<br>for sessions", "The rooms are filling up. Propose yours now."),
    "before-you-travel": ("Before<br>you travel", "Papers, phone, health, money: a short checklist."),
    "pick-your-sessions": ("Pick your<br>sessions", "Each room has only so many seats."),
    "see-you-thursday": ("See you<br>Thursday", f"Welcome at {THURSDAY['welcome']}, IPI Academy, Kulina bana 2, Tuzla."),
    "day-one": ("Day<br>one", "Seven rooms, four sessions each, an hour off after every one."),
    "day-two": ("Day<br>two", f"Starting at {FRIDAY['slots'][0]}, welcome at {FRIDAY['welcome']}."),
    "community-day": ("The<br>community's<br>day", "The salt lakes and the evening meetup."),
    "thank-you": ("Thank<br>you", "To everyone who spoke, supported, hosted, volunteered and came."),
    # The Tuesday Tuzla posts (wiki/org/outreach/drumbeat.md)
    "where-to-run-it": ("58 places<br>to run<br>yours", "From cafés on Freedom Square to halls for a few hundred people."),
    "salt-square": ("Salt<br>Square", "An Ottoman salt well from 1476, now an open-air museum."),
}

# Posts with a photo given for GoatConf, each with the credit line its giver asked for, or none where the organiser
# chose no credit (wiki/org/tuzla-images.md). The food photos are not freely licensed, so none is here. An optional
# fifth item says where to hold the photo in the square and in the wide crop (CSS object-position).
PHOTO_POSTS = {
    "getting-to-tuzla": ("Getting<br>to Tuzla", "Fly to Tuzla or Sarajevo, or come by bus.", "img/city-square-mosque-summer.jpg", "Photo: Grad Tuzla"),
    "an-hour-off": ("An hour<br>off", "After every session: Freedom Square, five minutes away.", "img/city-square-fountain-summer.jpg", "Photo: Grad Tuzla"),
    "where-to-stay": ("Where<br>to stay", "Hotels and guest houses a short walk from IPI Academy.", "img/city-korzo-clock.jpg", "Photo: Grad Tuzla"),
    "saturday": ("Saturday<br>at the lakes", "The salt lakes and what people add.", "img/city-lakes-aerial-summer.jpg", "Photo: Grad Tuzla"),
    "next-week": ("Next week<br>in Tuzla", "The salt lakes open for the season on 1 June.", "img/city-old-town-aerial-paving.jpg", "Photo: Grad Tuzla"),
    "city-of-salt": ("A city of<br>salt", "Tuzla takes its name from tuz, the Turkish for salt.", "img/city-aerial-summer.jpg", "Photo: Grad Tuzla"),
    "seven-thousand-years": ("7,000<br>years", "Neolithic people boiled salt here, in houses on stilts.", "img/city-archaeological-park.jpg", "Photo: Grad Tuzla"),
    # The Tuesday Tuzla posts (wiki/org/outreach/drumbeat.md): the two statues facing each other, the Korzo behind.
    "mesa-and-ismet": ("Meet at Meša and Ismet", "The writer and the painter on the Korzo: Tuzla's meeting point.",
                       "img/korzo-mesa-and-ismet.jpg", "", ("50% 60%", "40% 50%")),
    # The drumbeat's week 6 post: the goat statue in front of Hotel Tuzla, the organiser's own photo, no credit.
    "why-a-goat": ("Why<br>a goat?", "The whole of Tuzla milked one goat.", "img/tuzla-goat-statue.jpg", "",
                   ("47% 50%", "50% 50%")),
}
# Photos taller than wide, whose subject a band across the square card would cut: on the square card they stand on
# the left at full height, as on the wide card.
UPRIGHT = {"why-a-goat"}


def photo_post(w: int, h: int, title: str, line: str, img: str, credit: str, square: bool,
               focus: tuple[str, str] = ("50% 50%", "50% 50%"), upright: bool = False) -> str:
    """A post with a photo: the photo as a sticker, on top (square) or on the left (wide, and square when
    `upright`), its credit on it if it has one, the words under or beside it."""
    _, _, first, second, ink, _, mark = CARD_TONES[THEME]
    src = (SITE / img).as_uri()
    cred = (f'<div style="position:absolute; left:18px; bottom:12px; font-size:20px; font-weight:700; color:#fff; '
            f'text-shadow:0 1px 4px rgb(0 0 0 / .8)">{esc(credit)}</div>') if credit else ""

    def pic(at: str) -> str:
        return f'<img src="{src}" style="display:block; width:100%; height:100%; object-fit:cover; object-position:{at}">{cred}'
    if square and upright:
        return card(w, h, f"""
{sticker(pic(focus[0]), 64, 58, 500, 760)}
<div style="position:absolute; left:626px; right:56px; top:64px; white-space:nowrap; text-align:right">{wordmark(44, mark)}</div>
<div style="position:absolute; left:626px; right:56px; top:210px">{title_lines(title, 150, first, second)}</div>
<div style="position:absolute; left:626px; right:56px; top:560px; color:{ink}"><div style="{SUB}; font-size:44px; line-height:1.15">{line}</div></div>
{band_square(URL)}""")
    if square:
        return card(w, h, f"""
<div style="position:absolute; left:72px; top:56px; white-space:nowrap">{wordmark(44, mark)}</div>
{sticker(pic(focus[0]), 72, 140, 918, 450)}
<div style="position:absolute; left:72px; right:72px; top:646px">
  <div class="disp fit" data-fit="60" style="font-size:150px">{title_line(title, first, second)}</div>
</div>
<div style="position:absolute; left:72px; right:72px; bottom:168px; color:{ink}"><div style="{SUB}; font-size:42px; line-height:1.15">{line}</div></div>
{band_square(URL)}""")
    band = 116
    # A title with set lines keeps them, fitted to the column; one without wraps into even lines.
    words = (title_lines(title, 120, first, second, 60) if "<br>" in title else
             f'<div class="disp" style="font-size:84px; text-wrap:balance">{title_line(title, first, second)}</div>')
    return card(w, h, f"""
{band_wide(URL, band)}
{sticker(pic(focus[1]), 50, 36, 520, h - band - 88, 16, 24, 7)}
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
<div style="position:absolute; left:640px; right:40px; top:120px">{words}</div>
<div style="position:absolute; left:640px; right:60px; bottom:{band + 40}px; color:{ink}"><div style="{SUB}; font-size:32px; line-height:1.15">{line}</div></div>""")


# The goat on a speaker's card may say a line (the organiser's "maybe",
# sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md). Picking is this one value:
# The organiser picked "See you in Tuzla" (sources/conversations/2026-11-22--org--organisers-own-page-and-see-you-in-tuzla.md);
# it carries the exclamation mark every line the goat says on the site carries (tools/frame.py SAYS_EVERY). The link
# previews (1200 x 630, shown small by the sites that unfurl a link) carry no bubble.
#   ""         it says nothing
#   a line     every speaker's goat says that line, for example "See you in Tuzla!"
#   "rotate"   each speaker's goat takes the next line of SAYS_CARD, in the speakers' order
#   "own"      each says the first line about its own work (tools/frame.py SAYS_SPEAKER), or the first of SAYS_CARD
# A record's own `card_says:` line wins over all of them. Every line here is already on the site or in the organiser's
# recorded words; the list with where each comes from is in DESIGN.md under "Share cards, light and dark".
SPEAKER_SAYS = "See you in Tuzla!"
SAYS_CARD = ("See you in Tuzla!", "Come to GoatConf!", "Free to attend!", "See you in June!")
SAYS_CANDIDATES = (*SAYS_CARD, "Tuzla, 3–5 June 2027!", "Baaa!", "Any programming language, any stack.")


def card_line(slug: str, meta, index: int = 0, mode: str | None = None) -> str:
    """What the goat says on this speaker's card: nothing unless a line is picked."""
    mode = SPEAKER_SAYS if mode is None else mode
    if meta.get("card_says"):
        return str(meta["card_says"])
    if mode == "rotate":
        return SAYS_CARD[index % len(SAYS_CARD)]
    if mode == "own":
        import frame
        return (frame.SAYS_SPEAKER.get(slug) or SAYS_CARD)[0]
    return mode


def bubble(line: str, right: float, bottom: float, px: int, room: int) -> str:
    """The goat's line in a bubble up and to the left of its head, its tail corner towards the goat: the site's own
    speech bubble, yellow with night lettering in both versions so it reads at the size a card is seen in a feed."""
    if not line:
        return ""
    return (f'<div class="says" style="position:absolute; right:{right:.0f}px; bottom:{bottom:.0f}px; max-width:{room}px; '
            f'padding:{px * .28:.0f}px {px * .62:.0f}px {px * .34:.0f}px; border-radius:{px * .8:.0f}px {px * .8:.0f}px {px * .16:.0f}px {px * .8:.0f}px; '
            f'background:{YELLOW}; color:{NIGHT}; font-family:\'Bricolage Grotesque\'; font-weight:800; font-stretch:85%; '
            f'font-size:{px}px; line-height:1.08; text-wrap:balance; text-align:center">{esc(line)}</div>')


def speaker_card(slug: str, meta, talks: list[str], square: bool, height: int = 675, announce: bool = False,
                 says: str = "", free: bool = True) -> str:
    """The speaker's own "I'm speaking" card, or with `announce` GoatConf's card announcing them. Both say the same,
    and little: the photo, the name, their role and session, their own goat, and a yellow band with when, where,
    that it is free, and their page's address. Only the tab on the photo differs. Without `free` the band stops
    before "Free", as the link preview's line does."""
    _, _, first_tone, last_tone, ink, talk_tone, mark = CARD_TONES[THEME]
    first, _, last = str(meta["name"]).partition(" ")
    name = (f'<span style="color:{first_tone}">{esc(first)}</span>'
            + (f' <span style="color:{last_tone}">{esc(last)}</span>' if last else ""))
    photo = (f'<img src="{(SITE / meta["photo"]).as_uri()}" style="display:block;width:100%;height:100%;object-fit:cover">'
             if meta.get("photo") else
             f'<img src="{(SITE / "brand" / "coin-yellow.svg").as_uri()}" style="width:70%;height:70%;margin:15%">')
    address = f"{URL}/{speakers.page_name(slug)[:-5]}"
    # Before the session has a slot, the record's own title stands in for it.
    talk = talks[0] if talks else f'{speakers.talk_format(meta)}: {esc(str(meta["talk"]))}' if meta.get("talk") else ""
    head = "Confirmed speaker" if announce else "I&#39;m speaking"
    pose = f"speaker-{slug}-sitting"
    shape = goat_atlas.manifest()[pose]["h"] / goat_atlas.manifest()[pose]["w"] if goat_atlas.has(pose) else 0
    tab_shadow = "box-shadow:0 6px 14px -6px rgb(5 29 71 / .6)"
    session_style = f"font-family:'Bricolage Grotesque'; font-weight:700; font-stretch:85%; color:{talk_tone}; text-wrap:balance"
    if square:
        w = h = 1080
        band, size, left, top = 124, 600, 72, 62
        foot = top + size + 18
        # Beside the photo the wordmark stands on the photo's foot line, and the goat sits on the wordmark.
        side = left + size + 32
        room = w - side - 40
        mid = side + room / 2
        goat = ""
        if shape:
            tall = 392
            wide = tall / shape
            up = foot - 62 - tall + 8
            goat = (f'<img src="{goat_src(pose)}" style="position:absolute; left:{mid - wide / 2 + 4:.0f}px; top:{up:.0f}px; width:{wide:.0f}px">'
                    + bubble(says, w - mid - 128, h - up + 4, 31, 300))
        session = f'<div style="{session_style}; font-size:32px; line-height:1.12; margin-top:8px">{talk}</div>' if talk else ""
        return card(w, h, f"""
{snapshot(photo, left, top, size, 18, 26, 8)}
<div style="position:absolute; left:{side}px; width:{room}px; top:{foot - 66}px; text-align:center; white-space:nowrap">{wordmark(46, mark)}</div>
{goat}
<div style="position:absolute; left:{left + 8}px; top:{top + size - 12}px; transform:rotate({CARD_TILT}deg); transform-origin:0 50%"><span class="tab" style="font-size:36px; {tab_shadow}">{head}</span></div>
<div style="position:absolute; left:{left}px; right:{left}px; top:{foot + 36}px; color:{ink}">
  <div class="disp fit" data-fit="70" style="font-size:{122 if talk else 146}px">{name}</div>
  <div style="font-size:{32 if talk else 36}px; font-weight:700; line-height:1.2; margin-top:{10 if talk else 16}px; text-wrap:balance">{esc(str(meta.get("role") or ""))}</div>
  {session}
</div>
{foot_band(left, band, address, free, 56, 22, 50, 16)}
{seal(100, f"right:64px; bottom:{(band - 100) // 2}px")}
""")
    w, h = 1200, height
    band = 116 if h >= 675 else 108
    left, top = 50, 36
    size = h - band - top - 52
    text = left + size + 70
    goat, wide = "", 0
    if shape:
        wide = 190 if h >= 675 else 172
        goat = (f'<img src="{goat_src(pose)}" style="position:absolute; right:36px; bottom:{band - 50}px; width:{wide}px">'
                + bubble(says, 36 + wide * .9, band - 50 + wide * shape * .56, 25, 250))
    session = f'<div style="{session_style}; font-size:27px; line-height:1.15; margin-top:8px">{talk}</div>' if talk else ""
    # The seal stands on the band before the line, the wordmark in the top corner, and the goat sits on the band.
    return card(w, h, f"""
{foot_band(left + 110, band, address, free, 52, 20, 48, 17)}
{snapshot(photo, left, top, size, 16, 24, 7)}
<div style="position:absolute; left:{left + 6}px; top:{top + size - 10}px; transform:rotate({CARD_TILT}deg); transform-origin:0 50%"><span class="tab" style="font-size:28px; {tab_shadow}">{head}</span></div>
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
<div style="position:absolute; left:{text}px; right:40px; top:112px; color:{ink}">
  <div class="disp fit" data-fit="50" style="font-size:112px">{name}</div>
  <div style="max-width:{w - text - 52 - wide}px">
    <div style="font-size:30px; font-weight:700; line-height:1.2; margin-top:16px; text-wrap:balance">{esc(str(meta.get("role") or ""))}</div>
    {session}
  </div>
</div>
{seal(88, f"left:{left}px; bottom:{(band - 88) // 2}px")}
{goat}
""")


def thanks(meta) -> str:
    """The card's last line: the record's own `thanks` line if it has one.
    Otherwise a funds line that starts with what the supporter does
    ("Funding and organising ...") is used as it stands; any other line
    names what they fund."""
    if meta.get("thanks"):
        return esc(str(meta["thanks"]))
    if meta.get("host") is True:
        return "for hosting GoatConf 2027."
    funds = str(meta["funds"])
    if funds.split()[0].lower().endswith("ing"):
        return f"for {esc(funds[0].lower() + funds[1:])}."
    # Lowercase only a leading article, never a name ("Christoph Lipautz's travel").
    first = funds.split()[0]
    if first in ("The", "A", "An"):
        funds = first.lower() + funds[len(first):]
    return f"for funding {esc(funds)}."


def logo_ground(meta) -> str:
    """What sits behind the logo on a card: night for a logo made for the dark, the supporter's own colour if given, else white."""
    return NIGHT if meta.get("logo_on") == "dark" else str(meta.get("logo_bg") or "#fff")


def support_card(slug: str, meta, square: bool, head: str, words: str) -> str:
    """A supporter's card: their logo on its own ground as the sticker, a tab saying whose voice the card is in,
    their name, and one line under it. On the square card the plain goat sits on the wordmark beside the logo, as a
    speaker's goat does; on the wide one it sits on the band."""
    _, _, first, second, ink, accent, mark = CARD_TONES[THEME]
    logo = (f'<div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; padding:9%">'
            f'<img src="{(SITE / meta["logo"]).as_uri()}" style="max-width:100%; max-height:100%; object-fit:contain"></div>')
    address = f"{URL}/{speakers.supporter_page_name(slug)[:-5]}"
    name = str(meta["name"])
    long_name = len(name) > 22  # a long name takes two lines; a short one is fitted to one
    if square:
        w = h = 1080
        left, top, wide, tall = 72, 62, 600, 440
        foot = top + tall + 18
        side = left + wide + 32
        room = w - side - 40
        goat, gw = card_goat(330, f"left:{{at}}px; top:{foot - 62 - 330 + 8}px")
        goat = goat.replace("{at}", f"{side + room / 2 - gw / 2 + 4:.0f}")
        lettering = ('<div class="disp" style="font-size:92px; text-wrap:balance">' if long_name
                     else '<div class="disp fit" data-fit="70" style="font-size:150px">')
        return card(w, h, f"""
{sticker(logo, left, top, wide, tall, ground=logo_ground(meta))}
<div style="position:absolute; left:{side}px; width:{room}px; top:{foot - 66}px; text-align:center; white-space:nowrap">{wordmark(46, mark)}</div>
{goat}
{label(head, 36, left + 8, top + tall - 12)}
<div style="position:absolute; left:{left}px; right:{left}px; top:{foot + 44}px; color:{ink}">
  {lettering}{two_tone(name, first, second)}</div>
  <div style="{SUB}; font-size:{36 if long_name else 42}px; line-height:1.15; margin-top:22px; color:{accent}">{words}</div>
</div>
{band_square(address)}""")
    w, h = 1200, 675
    band, left, top, wide = 116, 50, 36, 520
    tall = h - band - top - 52
    text = left + wide + 70
    goat, gw = card_goat(250, f"right:36px; bottom:{band - 6}px")
    lettering = ('<div class="disp" style="font-size:66px; text-wrap:balance">' if long_name
                 else '<div class="disp fit" data-fit="50" style="font-size:112px">')
    return card(w, h, f"""
{band_wide(address, band, left)}
{sticker(logo, left, top, wide, tall, 16, 24, 7, ground=logo_ground(meta))}
{label(head, 28, left + 6, top + tall - 10)}
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
<div style="position:absolute; left:{text}px; right:40px; top:120px; color:{ink}">
  {lettering}{two_tone(name, first, second)}</div>
  <div style="{SUB}; font-size:{28 if long_name else 32}px; line-height:1.15; margin-top:18px; color:{accent}; max-width:{w - text - 52 - gw:.0f}px">{words}</div>
</div>
{goat}""")


def supporter_card(slug: str, meta, square: bool) -> str:
    """GoatConf's thank-you to a supporter."""
    return support_card(slug, meta, square, "Thank you", thanks(meta))


def proud_card(slug: str, meta, square: bool) -> str:
    """For the supporter to post as their own: their logo, their name, and what they give."""
    return support_card(slug, meta, square, "Proud supporter", esc(str(meta["funds"])))


def event_card(meta, slug: str, square: bool, height: int = 675) -> str:
    """For the host and anyone going: the event, who organises it, that it is part of GoatConf 2027, and when and where."""
    _, _, first, _, ink, accent, mark = CARD_TONES[THEME]
    name = str(meta["name"])
    start = extensions.as_datetime(meta["start"])
    when = f'{start.strftime("%A")} {extensions.when(meta)}'
    address = f"{URL}/{extensions.page_name(slug)[:-5]}"
    if square:
        w = h = 1080
        # The square card has room for the name on two or three lines; the wide one keeps it to one or two.
        goat, wide = card_goat(340, "right:56px; bottom:118px")
        return card(w, h, f"""
<div style="position:absolute; left:72px; top:64px; white-space:nowrap">{wordmark(46, mark)}</div>
{label("Part of GoatConf 2027", 38, 72, 196, 0)}
<div style="position:absolute; left:72px; right:72px; top:256px; color:{ink}">
  <div class="disp" style="font-size:{142 if len(name) <= 30 else 112}px; color:{first}; text-wrap:balance">{esc(name)}</div>
  <div style="max-width:{w - 144 - wide - 20:.0f}px">
    <div style="font-size:38px; font-weight:700; line-height:1.2; text-wrap:balance; margin-top:44px">Organised by {esc(str(meta["host"]))}</div>
    <div style="{SUB}; font-size:40px; line-height:1.18; margin-top:22px; color:{accent}">{esc(when)}<br>{esc(str(meta["location"]))}</div>
  </div>
</div>
{goat}
{band_square(address)}""")
    w, h = 1200, height
    band = 116 if h >= 675 else 108
    goat, wide = card_goat(270 if h >= 675 else 240, f"right:40px; bottom:{band - 6}px")
    return card(w, h, f"""
<div style="position:absolute; right:40px; top:38px; white-space:nowrap">{wordmark(40, mark)}</div>
{label("Part of GoatConf 2027", 28, 60, 60, 0)}
<div style="position:absolute; left:60px; right:{40 + wide + 20:.0f}px; top:106px; color:{ink}">
  <div class="disp" style="font-size:{104 if len(name) <= 22 else 84}px; color:{first}; text-wrap:balance">{esc(name)}</div>
  <div style="font-size:28px; font-weight:700; line-height:1.2; margin-top:20px; text-wrap:balance">Organised by {esc(str(meta["host"]))}</div>
  <div style="{SUB}; font-size:29px; line-height:1.18; margin-top:12px; color:{accent}">{esc(when)} · {esc(str(meta["location"]))}</div>
</div>
{goat}
{band_wide(address, band, 60)}""")


def cards() -> dict[str, tuple[int, int, str]]:
    """Every still card, drawn in the colours last chosen with use()."""
    out = {
        "linkedin-banner.png": (1584, 396, brand_band(1584, 396, left=560, top=54, mark=124, tag=40, band=100, facts=46, small=20, goat=230, right=80)),
        "linkedin-page-cover.png": (4200, 700, page_cover()),
        "header-3x1.png": (1500, 500, brand_band(1500, 500, left=90, top=78, mark=170, tag=50, band=116, facts=52, small=22, goat=290, right=80, band_left=420)),
        "og.png": (1200, 630, brand_band(1200, 630, left=60, top=110, mark=132, tag=42, band=124, facts=58, small=24, goat=330, right=60)),
        "goatchi-preview.png": (1200, 630, goatchi_card()),
        "post-goatchi-square.png": (1080, 1080, goatchi_card(1080, 1080, True, "goatconf.com/goatchi")),
        "post-goatchi-wide.png": (1200, 675, goatchi_card(1200, 675, url="goatconf.com/goatchi")),
        "luma-cover.png": (1080, 1080, luma_cover()),
    }
    # The goats post's cards, still and animated, are tools/goats_post.py's: it lays the goats out on goats_post's
    # lettering and seal.
    for key, (title, line) in POSTS.items():
        out[f"post-{key}-square.png"] = (1080, 1080, post(1080, 1080, title, line, True))
        out[f"post-{key}-wide.png"] = (1200, 675, post(1200, 675, title, line, False))
    for key, (title, line, img, credit, *focus) in PHOTO_POSTS.items():
        out[f"post-{key}-square.png"] = (1080, 1080, photo_post(1080, 1080, title, line, img, credit, True, *focus,
                                                                upright=key in UPRIGHT))
        out[f"post-{key}-wide.png"] = (1200, 675, photo_post(1200, 675, title, line, img, credit, False, *focus))
    talks = speakers.sessions_by_speaker()
    for i, (slug, (meta, _)) in enumerate(speakers.speakers().items()):
        says = card_line(slug, meta, i)
        out[f"speaker-{slug}-square.png"] = (1080, 1080, speaker_card(slug, meta, talks.get(slug, []), True, says=says))
        out[f"speaker-{slug}-wide.png"] = (1200, 675, speaker_card(slug, meta, talks.get(slug, []), False, says=says))
        out[speakers.preview_name(slug)] = (1200, 630, speaker_card(slug, meta, talks.get(slug, []), False, 630, free=False))
        announce = speakers.announce_cards(slug)
        out[announce["square"]] = (1080, 1080, speaker_card(slug, meta, talks.get(slug, []), True, announce=True, says=says))
        out[announce["wide"]] = (1200, 675, speaker_card(slug, meta, talks.get(slug, []), False, announce=True, says=says))
    for slug, (meta, _) in speakers.supporters().items():
        out[f"supporter-{slug}-square.png"] = (1080, 1080, supporter_card(slug, meta, True))
        out[f"supporter-{slug}-wide.png"] = (1200, 675, supporter_card(slug, meta, False))
        proud = speakers.proud_cards(slug)
        out[proud["square"]] = (1080, 1080, proud_card(slug, meta, True))
        out[proud["wide"]] = (1200, 675, proud_card(slug, meta, False))
    for _, slug, meta, _ in extensions.accepted():
        names = extensions.cards(slug)
        out[names["square"]] = (1080, 1080, event_card(meta, slug, True))
        out[names["wide"]] = (1200, 675, event_card(meta, slug, False))
        out[names["preview"]] = (1200, 630, event_card(meta, slug, False, 630))
    return out


def jobs() -> dict[str, tuple[int, int, str]]:
    """Every still card twice: the light one under its own name, the dark one under the same name ending in -dark."""
    out = cards()
    use("dark")
    try:
        out.update({dark(name): job for name, job in cards().items()})
    finally:
        use("light")
    return out


def says_samples(out: Path) -> int:
    """The proposal to look at, nothing in site/share/ touched: four speakers' cards in light and dark, each goat
    saying a different line, and every candidate line on the same card."""
    out.mkdir(parents=True, exist_ok=True)
    people = speakers.speakers()
    talks = speakers.sessions_by_speaker()
    todo = {}
    picks = [(slug, line) for slug, line in zip(list(people)[:4], SAYS_CARD)]
    first = picks[0][0]
    for theme in ("light", "dark"):
        use(theme)
        for slug, line in picks:
            meta = people[slug][0]
            todo[f"sample-{slug}-square-{theme}.png"] = (1080, 1080, speaker_card(slug, meta, talks.get(slug, []), True, says=line))
            todo[f"sample-{slug}-wide-{theme}.png"] = (1200, 675, speaker_card(slug, meta, talks.get(slug, []), False, says=line))
        own = card_line(first, people[first][0], mode="own")
        for n, line in enumerate((*SAYS_CANDIDATES, own), start=1):
            todo[f"candidate-{n}-{theme}.png"] = (1080, 1080, speaker_card(first, people[first][0], talks.get(first, []), True, says=line))
    use("light")
    exe = brand.chrome()
    with tempfile.TemporaryDirectory() as tmp:
        for name, (w, h, doc) in todo.items():
            render(name, w, h, doc, Path(tmp), exe, out)
            print(f"rendered {out / name}")
    return 0


# The weight of the cards (sources/conversations/2026-11-22--org--anything-left-lets-iterate.md). A card of flat
# colour is saved with a palette of 256 colours when the palette reproduces the full-colour render at this peak
# signal to noise ratio or better, where the difference is not seen; every other card keeps full colour.
PALETTE_DB = 45.0


def photo_card(name: str) -> bool:
    """A post built around a photograph, which never takes a palette."""
    m = re.match(r"post-(.+)-(?:square|wide)(?:-dark)?\.png$", name)
    return bool(m) and m.group(1) in PHOTO_POSTS


def slim(path: Path, name: str) -> bool:
    """Save a rendered card with a palette of 256 colours when that reproduces it at PALETTE_DB or better, so a
    re-render stays small; the path and the size in pixels stay as they were. Says whether the palette was taken."""
    if photo_card(name):
        return False
    from PIL import Image, ImageChops, ImageStat  # only render needs Pillow
    with Image.open(path) as im:
        if im.mode == "P":
            return True
        full = im.convert("RGB")
    few = full.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    error = sum(ImageStat.Stat(ImageChops.difference(full, few.convert("RGB"))).sum2) / (full.width * full.height * 3)
    if error and 10 * math.log10(255 * 255 / error) < PALETTE_DB:
        return False
    packed = io.BytesIO()
    few.save(packed, format="PNG", optimize=True)
    if len(packed.getvalue()) >= path.stat().st_size:
        return False
    path.write_bytes(packed.getvalue())
    return True


def render(name: str, w: int, h: int, doc: str, tmp: Path, exe: str, out: Path | None = None) -> None:
    src = tmp / f"{name}.html"
    src.write_text(doc, encoding="utf-8")
    shot = tmp / name
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=4000",
                    f"--window-size={w},{h + 200}", f"--screenshot={shot}", src.as_uri()],
                   check=True, capture_output=True, timeout=120)
    brand.crop(shot, (out or OUT) / name, w, h)
    slim((out or OUT) / name, name)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("--only")
    sub.add_parser("list")
    sub.add_parser("slim", help="save the cards already rendered with a palette where it reproduces them, as render does")
    sm = sub.add_parser("says-samples", help="the proposal's samples of a goat that says a line, written to a folder outside the site")
    sm.add_argument("out")
    args = ap.parse_args(argv)
    if args.cmd == "says-samples":
        return says_samples(Path(args.out))
    todo = jobs()
    if args.cmd == "list":
        for name, (w, h, _) in todo.items():
            print(f"{name}  {w}x{h}")
        return 0
    if args.cmd == "slim":
        took = sum(slim(OUT / name, name) for name in todo if (OUT / name).exists())
        print(f"{took} of {sum((OUT / name).exists() for name in todo)} cards are saved with a palette")
        return 0
    OUT.mkdir(exist_ok=True)
    exe = brand.chrome()
    with tempfile.TemporaryDirectory() as tmp:
        for name, (w, h, doc) in todo.items():
            if args.only and args.only not in name:
                continue
            gone = missing(doc)
            if gone:
                print(f"skipped site/share/{name}: not on this machine: {', '.join(Path(g).name for g in gone)}")
                continue
            render(name, w, h, doc, Path(tmp), exe)
            print(f"rendered site/share/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
