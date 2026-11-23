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
    "light": {"BLUE": brand.BLUE, "SOFT": "#46557a", "PAPER": "#edf2fb", "INK": brand.INK, "RING": "#ffffff",
              "ACCENT": brand.BLUE, "HOOF": "0b3d91", "HOOF_A": ".13"},
    "dark": {"BLUE": "#f3f6ff", "SOFT": "#b6c5e8", "PAPER": "#051534", "INK": "#e8eefc", "RING": "#14387a",
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
    global THEME, BLUE, SOFT, PAPER, INK, RING, ACCENT, HOOVES
    t = THEMES[theme]
    THEME, BLUE, SOFT, PAPER, INK, RING, ACCENT = theme, t["BLUE"], t["SOFT"], t["PAPER"], t["INK"], t["RING"], t["ACCENT"]
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


def banner(w: int, h: int, word: int, sub: int, url: int, seal_size: int, left: int, right: int, top: int | None = None) -> str:
    """A wide band: the name, the facts and the address on the left, the whole seal on the right."""
    top_css = f"top:{top}px" if top is not None else "top:50%; transform:translateY(-50%)"
    return page(w, h, f"""
<div style="position:absolute; left:{left}px; {top_css}">
  <div class="word" style="font-size:{word}px">GoatConf 2027</div>
  <div class="sub" style="font-size:{sub}px; margin-top:{int(sub * .55)}px">{FACTS}</div>
  <div class="url" style="font-size:{url}px; margin-top:{int(sub * .7)}px">{URL}</div>
</div>
{seal(seal_size, f"right:{right}px; top:50%; transform:translateY(-50%)")}""")


def page_cover(w: int = 4200, h: int = 700) -> str:
    """The LinkedIn company page cover, at LinkedIn's 4200 x 700.

    LinkedIn lays the page's square logo over the bottom left of the cover and
    the phone app trims both sides, so the text starts past the logo's quarter
    and the seal sits well inside the right edge."""
    return page(w, h, f"""
<style>body {{ background-size: 600px 600px; }}</style>
<div style="position:absolute; left:1240px; top:50%; transform:translateY(-50%)">
  <div class="word" style="font-size:236px">GoatConf 2027</div>
  <div class="sub" style="font-size:100px; margin-top:52px">{FACTS}</div>
  <div style="font-size:70px; font-weight:700; margin-top:40px">Any programming language, any stack.<span class="url" style="margin-left:.9em">{URL}</span></div>
</div>
{seal(500, "right:360px; top:50%; transform:translateY(-50%)")}""")


def post(w: int, h: int, title: str, line: str, square: bool) -> str:
    if square:
        return page(w, h, f"""
<div style="position:absolute; left:84px; top:96px; right:84px">
  <div class="word" style="font-size:132px">{title}</div>
  <div class="rule" style="width:120px; margin:44px 0 36px"></div>
  <div class="sub" style="font-size:44px; line-height:1.15; max-width:24ch">{line}</div>
</div>
<div style="position:absolute; left:84px; bottom:92px">
  <div class="sub" style="font-size:34px; color:{INK}">{FACTS}</div>
  <div class="url" style="font-size:32px; margin-top:16px">{URL}</div>
</div>
{seal(300, "right:72px; bottom:72px")}""")
    return page(w, h, f"""
<div style="position:absolute; left:72px; top:72px; width:720px">
  <div class="word" style="font-size:104px">{title}</div>
  <div class="rule" style="width:100px; margin:34px 0 28px"></div>
  <div class="sub" style="font-size:36px; line-height:1.15">{line}</div>
</div>
<div style="position:absolute; left:72px; bottom:64px">
  <div class="sub" style="font-size:28px; color:{INK}">{FACTS}</div>
  <div class="url" style="font-size:26px; margin-top:12px">{URL}</div>
</div>
{seal(340, "right:72px; top:50%; transform:translateY(-50%)")}""")


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
    """Goatchi's link preview and its post: its name and what you do, beside the goat eating burek and the plain goat
    saying hello."""
    def g(pose, width, style):
        return f'<img src="{goat_src(pose)}" style="position:absolute; width:{width}px; {style}">'
    if square:
        return page(w, h, f"""
<div style="position:absolute; left:84px; top:96px; right:84px">
  <div class="word" style="font-size:150px">Goatchi</div>
  <div class="rule" style="width:120px; margin:40px 0 34px"></div>
  <div class="sub" style="font-size:46px; line-height:1.15; max-width:20ch">Keep a GoatConf goat. Feed it, play with it, let it sleep.</div>
</div>
<div style="position:absolute; left:84px; bottom:84px"><div class="url" style="font-size:32px">{url}</div></div>
{g("sticker-burek", 330, "left:84px; bottom:150px")}
{g("sitting", 380, "right:72px; bottom:72px")}
<div class="sub" style="position:absolute; right:300px; bottom:470px; padding:12px 28px 14px; border-radius:34px 34px 34px 6px; background:{YELLOW}; color:#0a1f4d; font-size:48px; font-weight:800">Baaa!</div>""")
    return page(w, h, f"""
<div style="position:absolute; left:72px; top:84px; width:500px">
  <div class="word" style="font-size:124px">Goatchi</div>
  <div class="rule" style="width:100px; margin:32px 0 28px"></div>
  <div class="sub" style="font-size:38px; line-height:1.15">Keep a GoatConf goat. Feed it, play with it, let it sleep.</div>
</div>
<div style="position:absolute; left:72px; bottom:62px"><div class="url" style="font-size:28px">{url}</div></div>
{g("sticker-burek", 255, "left:590px; bottom:44px")}
{g("sitting", 290, "right:56px; bottom:40px")}
<div class="sub" style="position:absolute; right:250px; top:128px; padding:10px 24px 12px; border-radius:30px 30px 30px 6px; background:{YELLOW}; color:#0a1f4d; font-size:40px; font-weight:800">Baaa!</div>""")


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
    """A post with a photo: the photo on top (square) or on the left (wide, and square when `upright`), its credit on
    it if it has one, the words beside. A title without set line breaks takes the card's full width and wraps into
    even lines."""
    src = (SITE / img).as_uri()
    cred = (f'<div style="position:absolute; left:18px; bottom:14px; font-size:20px; font-weight:700; '
            f'text-shadow:0 1px 4px rgb(0 0 0 / .8)">{esc(credit)}</div>') if credit else ""
    if square and upright:
        return page(w, h, f"""
<div style="position:absolute; left:0; top:0; width:580px; height:{h}px; overflow:hidden">
  <img src="{src}" style="width:100%; height:100%; object-fit:cover; object-position:{focus[0]}">{cred}</div>
<div class="rule" style="position:absolute; left:580px; top:0; width:8px; height:{h}px; border-radius:0"></div>
<div style="position:absolute; left:644px; top:84px; right:56px">
  <div class="word" style="font-size:104px; text-wrap:balance">{title}</div>
  <div class="sub" style="font-size:36px; line-height:1.15; margin-top:30px">{line}</div>
</div>
<div style="position:absolute; left:644px; bottom:290px; right:56px">
  <div class="sub" style="font-size:30px; line-height:1.3; color:{INK}">{FACTS.replace(" · ", "<br>")}</div>
  <div class="url" style="font-size:28px; margin-top:12px">{URL}</div>
</div>
{seal(200, "right:56px; bottom:64px")}""")
    if square:
        return page(w, h, f"""
<div style="position:absolute; left:0; top:0; width:{w}px; height:540px; overflow:hidden">
  <img src="{src}" style="width:100%; height:100%; object-fit:cover; object-position:{focus[0]}">{cred}</div>
<div class="rule" style="position:absolute; left:0; top:540px; width:{w}px; border-radius:0"></div>
<div style="position:absolute; left:84px; top:600px; right:84px">
  <div class="word" style="font-size:112px; text-wrap:balance">{title}</div>
  <div class="sub" style="font-size:38px; line-height:1.15; margin-top:30px; margin-right:246px">{line}</div>
</div>
<div style="position:absolute; left:84px; bottom:64px">
  <div class="sub" style="font-size:30px; color:{INK}">{FACTS}</div>
  <div class="url" style="font-size:28px; margin-top:10px">{URL}</div>
</div>
{seal(230, "right:64px; bottom:64px")}""")
    return page(w, h, f"""
<div style="position:absolute; left:0; top:0; width:560px; height:{h}px; overflow:hidden">
  <img src="{src}" style="width:100%; height:100%; object-fit:cover; object-position:{focus[1]}">{cred}</div>
<div class="rule" style="position:absolute; left:560px; top:0; width:6px; height:{h}px; border-radius:0"></div>
<div style="position:absolute; left:620px; top:64px; right:56px">
  <div class="word" style="font-size:{88 if "<br>" in title else 100}px; text-wrap:balance">{title}</div>
  <div class="sub" style="font-size:30px; line-height:1.15; margin-top:24px">{line}</div>
</div>
<div style="position:absolute; left:620px; bottom:56px; right:200px">
  <div class="sub" style="font-size:22px; color:{INK}">{FACTS}</div>
  <div class="url" style="font-size:22px; margin-top:8px">{URL}</div>
</div>
{seal(140, "right:48px; bottom:48px")}""")


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


# The speaker cards (sources/conversations/2026-11-23--org--speaker-cards-photo-first.md): the photo first, tilted
# like a sticker in the album, on a yellow block; the name on one line, as large as its room allows; a yellow band
# along the foot with the date, the town and "Free" in a dark pill. The light card is on paper, the dark one on the
# album's blue: per version the ground, its hoof marks, the first and last name, the text, the session and the
# wordmark.
SPEAKER_TONES = {
    "light": ("#edf2fb", ("0b3d91", ".13"), brand.INK, brand.BLUE, brand.INK, brand.BLUE, brand.BLUE),
    "dark": (brand.BLUE, ("ffffff", ".07"), "#ffffff", YELLOW, "#ffffff", YELLOW, "#ffffff"),
}
SPEAKER_TILT = -2.5
SPEAKER_WHEN = "3–5 June 2027 · Tuzla"
# A name is set at its largest size and stepped down until it fits its line: the script runs once the fonts are in.
FIT = """<script>
document.fonts.ready.then(() => {
  document.querySelectorAll('[data-fit]').forEach(el => {
    let s = parseFloat(getComputedStyle(el).fontSize);
    const min = parseFloat(el.dataset.fit) || 40;
    while (el.scrollWidth > el.clientWidth && s > min) { s -= 2; el.style.fontSize = s + 'px'; }
  });
});
</script>"""


def wordmark(px: int, colour: str) -> str:
    """GoatConf and the year in its yellow tab, on one line: the top bar's mark."""
    return (f'<span class="disp" style="font-size:{px}px; color:{colour}; vertical-align:middle">GoatConf</span>'
            f'<span class="tab" style="font-size:{px}px; margin-left:{px * .22:.0f}px; vertical-align:middle; font-stretch:75%">2027</span>')


def snapshot(photo: str, left: int, top: int, size: int, off: int, radius: int, ring: int) -> str:
    """The speaker's photo as a sticker: a rounded square with a white edge on a yellow block set down and to the
    right, the two tilted together about the photo's centre."""
    box = f"position:absolute; left:{left}px; top:{top}px; width:{size}px; height:{size}px; border-radius:{radius}px"
    return (f'<div style="position:absolute; left:0; top:0; width:0; height:0; transform-origin:{left + size / 2:.0f}px {top + size / 2:.0f}px; '
            f'transform:rotate({SPEAKER_TILT}deg)">'
            f'<div style="{box}; background:{YELLOW}; transform:translate({off}px,{off}px)"></div>'
            f'<div style="{box}; overflow:hidden; background:{YELLOW}; box-shadow:0 0 0 {ring}px #fff">{photo}</div></div>')


def foot_band(left: int, band: int, address: str, free: bool, px: int, small: int, lift: int, low: int) -> str:
    """The yellow band along the foot: when and where, "Free" in a dark pill, and the page's address under them."""
    pill = (f' · <span style="background:{NIGHT}; color:{YELLOW}; border-radius:.2em; padding:.03em .3em .06em; margin-left:.06em">Free</span>'
            if free else "")
    return (f'<div style="position:absolute; left:0; right:0; bottom:0; height:{band}px; background:{YELLOW}"></div>'
            f'<div class="disp" style="position:absolute; left:{left}px; bottom:{lift}px; font-size:{px}px; color:{NIGHT}; white-space:nowrap">{SPEAKER_WHEN}{pill}</div>'
            f'<div style="position:absolute; left:{left}px; bottom:{low}px; font-size:{small}px; font-weight:700; color:{NIGHT}">{address}</div>')


def speaker_card(slug: str, meta, talks: list[str], square: bool, height: int = 675, announce: bool = False,
                 says: str = "", free: bool = True) -> str:
    """The speaker's own "I'm speaking" card, or with `announce` GoatConf's card announcing them. Both say the same,
    and little: the photo, the name, their role and session, their own goat, and a yellow band with when, where,
    that it is free, and their page's address. Only the tab on the photo differs. Without `free` the band stops
    before "Free", as the link preview's line does."""
    ground, hoof, first_tone, last_tone, ink, talk_tone, mark = SPEAKER_TONES[THEME]
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
        return page(w, h, f"""
{snapshot(photo, left, top, size, 18, 26, 8)}
<div style="position:absolute; left:{side}px; width:{room}px; top:{foot - 66}px; text-align:center; white-space:nowrap">{wordmark(46, mark)}</div>
{goat}
<div style="position:absolute; left:{left + 8}px; top:{top + size - 12}px; transform:rotate({SPEAKER_TILT}deg); transform-origin:0 50%"><span class="tab" style="font-size:36px; {tab_shadow}">{head}</span></div>
<div style="position:absolute; left:{left}px; right:{left}px; top:{foot + 36}px; color:{ink}">
  <div class="disp fit" data-fit="70" style="font-size:{122 if talk else 146}px">{name}</div>
  <div style="font-size:{32 if talk else 36}px; font-weight:700; line-height:1.2; margin-top:{10 if talk else 16}px; text-wrap:balance">{esc(str(meta.get("role") or ""))}</div>
  {session}
</div>
{foot_band(left, band, address, free, 56, 22, 50, 16)}
{seal(100, f"right:64px; bottom:{(band - 100) // 2}px")}
{FIT}""", ground, hooves(*hoof), rule=False)
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
    return page(w, h, f"""
{foot_band(left + 110, band, address, free, 52, 20, 48, 17)}
{snapshot(photo, left, top, size, 16, 24, 7)}
<div style="position:absolute; left:{left + 6}px; top:{top + size - 10}px; transform:rotate({SPEAKER_TILT}deg); transform-origin:0 50%"><span class="tab" style="font-size:28px; {tab_shadow}">{head}</span></div>
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
{FIT}""", ground, hooves(*hoof), rule=False)


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


def logo_edge(meta) -> str:
    """On the dark card a logo drawn for the dark sits on a night tile on the night ground: a thin ring in the line
    blue keeps the tile's shape."""
    return "box-shadow:0 0 0 2px rgb(169 196 255 / .55); " if THEME == "dark" and logo_ground(meta) == NIGHT else ""


def supporter_card(slug: str, meta, square: bool) -> str:
    w, h = (1080, 1080) if square else (1200, 675)
    logo = (SITE / meta["logo"]).as_uri()
    address = f"{URL}/{speakers.supporter_page_name(slug)[:-5]}"
    # A long address shrinks on the square card so it stays clear of the seal.
    url_px = (32 if len(address) <= 36 else 26) if square else 26
    return page(w, h, f"""
<div style="position:absolute; left:{84 if square else 72}px; top:{96 if square else 72}px; right:{84 if square else 460}px">
  <div class="sub" style="font-size:{40 if square else 32}px; color:{INK}">Thank you,</div>
  <div class="word" style="font-size:{(120 if len(str(meta['name'])) <= 24 else 88) if square else 92}px; margin-top:16px">{esc(str(meta['name']))}</div>
  <div class="sub" style="font-size:{36 if square else 28}px; line-height:1.2; margin-top:28px">{thanks(meta)}</div>
</div>
<div style="position:absolute; {'left:84px; bottom:300px' if square else 'right:72px; top:72px'}; width:{420 if square else 340}px; height:{220 if square else 180}px; background:{logo_ground(meta)}; {logo_edge(meta)}border-radius:18px; display:grid; place-items:center; padding:28px">
  <img src="{logo}" style="max-width:100%; max-height:100%; object-fit:contain"></div>
<div class="url" style="position:absolute; left:{84 if square else 72}px; bottom:{84 if square else 64}px; font-size:{url_px}px">{address}</div>
{seal(240 if square else 220, "right:72px; bottom:72px")}""")


def proud_card(slug: str, meta, square: bool) -> str:
    """For the supporter to post as their own: their logo, what they give, when and where, and their profile."""
    w, h = (1080, 1080) if square else (1200, 675)
    logo = (SITE / meta["logo"]).as_uri()
    address = f"{URL}/{speakers.supporter_page_name(slug)[:-5]}"
    # A long address shrinks on the square card so it stays clear of the seal.
    url_px = (32 if len(address) <= 36 else 26) if square else 26
    return page(w, h, f"""
<div style="position:absolute; left:{84 if square else 72}px; top:{96 if square else 72}px; right:{84 if square else 72}px">
  <div class="sub" style="font-size:{40 if square else 32}px; color:{INK}">Proud supporter of</div>
  <div class="word" style="font-size:{120 if square else 92}px; margin-top:16px">GoatConf 2027</div>
</div>
<div style="position:absolute; left:{84 if square else 72}px; top:{400 if square else 290}px; width:{560 if square else 400}px; height:{280 if square else 200}px; background:{logo_ground(meta)}; {logo_edge(meta)}border-radius:18px; display:grid; place-items:center; padding:32px">
  <img src="{logo}" style="max-width:100%; max-height:100%; object-fit:contain"></div>
<div style="position:absolute; left:{84 if square else 520}px; top:{730 if square else 300}px; right:{360 if square else 72}px">
  <div class="sub" style="font-size:{34 if square else 28}px; line-height:1.2">{esc(str(meta["funds"]))}</div>
  <div style="font-size:{30 if square else 24}px; font-weight:700; line-height:1.2; margin-top:20px">{FACTS}</div>
</div>
<div class="url" style="position:absolute; left:{84 if square else 72}px; bottom:{84 if square else 64}px; font-size:{url_px}px">{address}</div>
{seal(240 if square else 160, "right:72px; bottom:72px" if square else "right:56px; bottom:48px")}""")


def event_card(meta, slug: str, square: bool, height: int = 675) -> str:
    """For the host and anyone going: the event, who organises it, that it is part of GoatConf 2027, and when and where."""
    w, h = (1080, 1080) if square else (1200, height)
    name = str(meta["name"])
    # The square card has room for the name on two or three lines; the wide one keeps it to one or two.
    name_px = (132 if len(name) <= 30 else 104) if square else (92 if len(name) <= 22 else 72)
    start = extensions.as_datetime(meta["start"])
    when = f'{start.strftime("%A")} {extensions.when(meta)}'
    return page(w, h, f"""
<div style="position:absolute; left:{84 if square else 72}px; top:{120 if square else 72}px; right:{84 if square else 320}px">
  <div class="sub" style="font-size:{46 if square else 30}px; color:{INK}">Part of GoatConf 2027</div>
  <div class="word" style="font-size:{name_px}px; margin-top:{24 if square else 16}px">{esc(name)}</div>
  <div style="font-size:{40 if square else 28}px; font-weight:700; line-height:1.2; margin-top:{36 if square else 24}px; text-wrap:balance">Organised by {esc(str(meta["host"]))}</div>
  <div class="sub" style="font-size:{40 if square else 28}px; line-height:1.2; margin-top:{28 if square else 20}px">{esc(when)}<br>{esc(str(meta["location"]))}</div>
</div>
<div class="url" style="position:absolute; left:{84 if square else 72}px; bottom:{84 if square else 64}px; font-size:{32 if square else 26}px">{URL}/{extensions.page_name(slug)[:-5]}</div>
{seal(240 if square else 220, "right:72px; bottom:72px")}""")


def cards() -> dict[str, tuple[int, int, str]]:
    """Every still card, drawn in the colours last chosen with use()."""
    out = {
        "linkedin-banner.png": (1584, 396, banner(1584, 396, 104, 36, 26, 320, 560, 90)),
        "linkedin-page-cover.png": (4200, 700, page_cover()),
        "header-3x1.png": (1500, 500, banner(1500, 500, 128, 40, 28, 400, 90, 96)),
        "og.png": (1200, 630, banner(1200, 630, 104, 34, 26, 400, 64, 56)),
        "goatchi-preview.png": (1200, 630, goatchi_card()),
        "post-goatchi-square.png": (1080, 1080, goatchi_card(1080, 1080, True, "goatconf.com/goatchi")),
        "post-goatchi-wide.png": (1200, 675, goatchi_card(1200, 675, url="goatconf.com/goatchi")),
        "luma-cover.png": (1080, 1080, page(1080, 1080, f"""
{seal(600, "left:240px; top:110px")}
<div style="position:absolute; left:0; right:0; bottom:110px; text-align:center">
  <div class="word" style="font-size:120px">GoatConf 2027</div>
  <div class="sub" style="font-size:42px; margin-top:24px">{FACTS}</div>
</div>""")),
    }
    # The goats post's cards, still and animated, are tools/goats_post.py's: it lays the goats out on goats_post's
    # lettering and seal.
    for key, (title, line) in POSTS.items():
        out[f"post-{key}-square.png"] = (1080, 1080, post(1080, 1080, title, line, True))
        out[f"post-{key}-wide.png"] = (1200, 675, post(1200, 675, title.replace("<br>", " "), line, False))
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
