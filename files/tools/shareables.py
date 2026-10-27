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
BLUE, YELLOW, NIGHT, SOFT = brand.BLUE, brand.YELLOW, brand.NIGHT, "#c9d7f5"
FACTS = "Tuzla · 3–5 June 2027 · Free to attend"
URL = "goatconf.com"
esc = html.escape

HOOVES = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E"
          "%3Cg fill='white' fill-opacity='.06'%3E%3Cpath d='M30 40c-5 0-7 6-7 11s3 8 6 8c2 0 2-2 2-3z'/%3E"
          "%3Cpath d='M34 40c5 0 7 6 7 11s-3 8-6 8c-2 0-2-2-2-3z'/%3E%3Cpath d='M112 104c-5 0-7 6-7 11s3 8 6 8c2 0 2-2 2-3z'/%3E"
          "%3Cpath d='M116 104c5 0 7 6 7 11s-3 8-6 8c-2 0-2-2-2-3z'/%3E%3C/g%3E%3C/svg%3E\")")


def page(w: int, h: int, body: str, bg: str = BLUE) -> str:
    fonts = (SITE / "fonts").as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; }}
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin-ext.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; unicode-range: U+0100-02BA; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{fonts}/atkinson-latin.woff2") format("woff2"); font-weight: 200 800; }}
@font-face {{ font-family: "Atkinson Hyperlegible Next"; src: url("{fonts}/atkinson-latin-ext.woff2") format("woff2"); font-weight: 200 800; unicode-range: U+0100-02BA; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{ background: {bg} {HOOVES}; color: #fff; font-family: "Atkinson Hyperlegible Next", sans-serif; position: relative; }}
.word {{ font-family: "Bricolage Grotesque"; font-weight: 800; font-stretch: 75%; line-height: .86; letter-spacing: .005em; text-transform: uppercase; }}
.sub {{ font-family: "Bricolage Grotesque"; font-weight: 700; font-stretch: 85%; color: {YELLOW}; }}
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
  <div class="sub" style="font-size:34px; color:#fff">{FACTS}</div>
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
  <div class="sub" style="font-size:28px; color:#fff">{FACTS}</div>
  <div class="url" style="font-size:26px; margin-top:12px">{URL}</div>
</div>
{seal(340, "right:72px; top:50%; transform:translateY(-50%)")}""")


POSTS = {
    "save-the-date": ("Save<br>the date", "Two days of talks in every room of IPI Academy, then a day for the community."),
    "run-a-session": ("Run a<br>session", "A talk, a panel, a workshop or something else. One hour, one room."),
    "register": ("Get your<br>free ticket", "Thursday and Friday for the talks, Saturday for the community."),
    "add-something": ("Propose<br>an event", "A workshop, a meetup, a dinner, a hike: run it around GoatConf."),
    "first-speakers": ("The first<br>speakers<br>are here", "Eight speakers so far, each with an hour at IPI Academy on 3 or 4 June."),
    # The drumbeat to June 2027 (wiki/org/outreach/drumbeat.md)
    "why-a-goat": ("Why<br>a goat?", "The whole of Tuzla milked one goat."),
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
    "community-day": ("The<br>community's<br>day", "The salt lakes, the goat hunt, and the evening meetup."),
    "thank-you": ("Thank<br>you", "To everyone who spoke, supported, hosted, volunteered and came."),
    # The Tuesday Tuzla posts (wiki/org/outreach/drumbeat.md)
    "mesa-and-ismet": ("Meet at<br>Meša and<br>Ismet", "The writer and the painter on the Korzo: Tuzla's meeting point."),
    "where-to-run-it": ("58 places<br>to run<br>yours", "From cafés on Freedom Square to halls for a few hundred people."),
    "salt-square": ("Salt<br>Square", "An Ottoman salt well from 1476, now an open-air museum."),
}

# Posts with a photo given for GoatConf, each with the credit line its giver asked for
# (wiki/org/tuzla-images.md). The food photos are not freely licensed, so none is here.
PHOTO_POSTS = {
    "getting-to-tuzla": ("Getting<br>to Tuzla", "Fly to Tuzla or Sarajevo, or come by bus.", "img/city-square-mosque-summer.jpg", "Photo: Grad Tuzla"),
    "an-hour-off": ("An hour<br>off", "After every session: Freedom Square, five minutes away.", "img/city-square-fountain-summer.jpg", "Photo: Grad Tuzla"),
    "where-to-stay": ("Where<br>to stay", "Hotels and guest houses a short walk from IPI Academy.", "img/city-korzo-clock.jpg", "Photo: Grad Tuzla"),
    "saturday": ("Saturday<br>at the lakes", "The salt lakes, the goat hunt, and what people add.", "img/city-lakes-aerial-summer.jpg", "Photo: Grad Tuzla"),
    "next-week": ("Next week<br>in Tuzla", "The salt lakes open for the season on 1 June.", "img/city-old-town-aerial-paving.jpg", "Photo: Grad Tuzla"),
    "city-of-salt": ("A city of<br>salt", "Tuzla takes its name from tuz, the Turkish for salt.", "img/city-aerial-summer.jpg", "Photo: Grad Tuzla"),
    "seven-thousand-years": ("7,000<br>years", "Neolithic people boiled salt here, in houses on stilts.", "img/city-archaeological-park.jpg", "Photo: Grad Tuzla"),
}


def photo_post(w: int, h: int, title: str, line: str, img: str, credit: str, square: bool) -> str:
    """A post with a photo: the photo on top (square) or on the left (wide), its credit on it, the words beside."""
    src = (SITE / img).as_uri()
    cred = (f'<div style="position:absolute; left:18px; bottom:14px; font-size:20px; font-weight:700; '
            f'text-shadow:0 1px 4px rgb(0 0 0 / .8)">{esc(credit)}</div>')
    if square:
        return page(w, h, f"""
<div style="position:absolute; left:0; top:0; width:{w}px; height:540px; overflow:hidden">
  <img src="{src}" style="width:100%; height:100%; object-fit:cover">{cred}</div>
<div class="rule" style="position:absolute; left:0; top:540px; width:{w}px; border-radius:0"></div>
<div style="position:absolute; left:84px; top:600px; right:330px">
  <div class="word" style="font-size:112px">{title}</div>
  <div class="sub" style="font-size:38px; line-height:1.15; margin-top:30px">{line}</div>
</div>
<div style="position:absolute; left:84px; bottom:64px">
  <div class="sub" style="font-size:30px; color:#fff">{FACTS}</div>
  <div class="url" style="font-size:28px; margin-top:10px">{URL}</div>
</div>
{seal(230, "right:64px; bottom:64px")}""")
    return page(w, h, f"""
<div style="position:absolute; left:0; top:0; width:560px; height:{h}px; overflow:hidden">
  <img src="{src}" style="width:100%; height:100%; object-fit:cover">{cred}</div>
<div class="rule" style="position:absolute; left:560px; top:0; width:6px; height:{h}px; border-radius:0"></div>
<div style="position:absolute; left:620px; top:64px; right:56px">
  <div class="word" style="font-size:88px">{title}</div>
  <div class="sub" style="font-size:30px; line-height:1.15; margin-top:24px">{line}</div>
</div>
<div style="position:absolute; left:620px; bottom:56px; right:200px">
  <div class="sub" style="font-size:22px; color:#fff">{FACTS}</div>
  <div class="url" style="font-size:22px; margin-top:8px">{URL}</div>
</div>
{seal(140, "right:48px; bottom:48px")}""")


# Where the speaker's goat sits on their cards: "corner", whole, in the bottom corner (the organiser's choice,
# 2026-10-27), or "ring", small against the photo's ring.
SPEAKER_GOAT = "corner"


def speaker_card(slug: str, meta, talks: list[str], square: bool, height: int = 675, announce: bool = False) -> str:
    """The speaker's own "I'm speaking" card, or with `announce` GoatConf's card announcing them. Both say the same,
    and little: the name and photo, their role and session, one quiet line of when, where and their page's address,
    and their own goat. Only the headline differs."""
    name = esc(str(meta["name"]))
    photo = (f'<img src="{(SITE / meta["photo"]).as_uri()}" style="width:100%;height:100%;object-fit:cover">'
             if meta.get("photo") else
             f'<img src="{(SITE / "brand" / "coin-yellow.svg").as_uri()}" style="width:70%;height:70%;margin:15%">')
    address = f"{URL}/{speakers.page_name(slug)[:-5]}"
    # Before the session has a slot, the record's own title stands in for it.
    talk = talks[0] if talks else f'{speakers.talk_format(meta)}: {esc(str(meta["talk"]))}' if meta.get("talk") else ""
    w, h = (1080, 1080) if square else (1200, height)
    size = 330 if square else min(330, h - 150)
    long_name = len(str(meta["name"])) > 14
    name_px = (84 if long_name else 110) if square else (70 if long_name else 92)
    top = 72 if square else (h - size) // 2
    frame = (f'<div style="position:absolute; left:{84 if square else 64}px; top:{top}px; width:{size}px; height:{size}px; border-radius:50%; '
             f'overflow:hidden; background:{YELLOW}; box-shadow:0 0 0 10px #fff">{photo}</div>')
    # The speaker's own painted goat, whole, sitting in the bottom corner (ADR goat-mascot), or small against
    # the photo's ring.
    corner = SPEAKER_GOAT == "corner"
    pose = f"speaker-{slug}-sitting"
    if not goat_atlas.has(pose):
        goat = ""
    elif corner:
        gw = 170 if square else min(160, h * 0.25)
        goat = (f'<img src="{(goat_atlas.ART / (pose + ".webp")).as_uri()}" style="position:absolute; right:{72 if square else 56}px; '
                f'bottom:{40 if square else 28}px; width:{gw:.0f}px">')
    else:
        gw = 140 if square else 112
        left = (84 + size - gw * 0.55) if square else (64 + size - gw * 0.55)
        goat = (f'<img src="{(goat_atlas.ART / (pose + ".webp")).as_uri()}" style="position:absolute; left:{left:.0f}px; '
                f'top:{top + size - gw * 1.05:.0f}px; width:{gw}px">')
    head = f'<div class="sub" style="font-size:{44 if square else 30}px; color:#fff">{"Confirmed speaker at GoatConf 2027" if announce else "I&#39;m speaking at GoatConf 2027"}</div>'
    who = f'<div class="word" style="font-size:{name_px}px; margin-top:18px">{name}</div>'
    role = (f'<div style="font-size:{36 if square else 30}px; font-weight:700; line-height:1.25; margin-top:20px; text-wrap:balance">{esc(str(meta["role"]))}</div>'
            if meta.get("role") else "")
    session = (f'<div class="sub" style="font-size:{40 if square else 32}px; line-height:1.2; margin-top:24px; text-wrap:balance">{talk}</div>'
               if talk else "")
    # The quiet line of when, where and the page's address follows the text, so the two never meet.
    foot = (f'<div class="url" style="font-size:{26 if square else 22}px; line-height:1.3; text-wrap:balance">'
            f'Tuzla · 3–5 June 2027 · {address}</div>')
    clear = (270 if square else 270) if corner else (84 if square else 72)
    if square:
        # The text has the card's width above the goat; only the quiet line beside it steps around it.
        return page(w, h, f"""
{frame}{goat}{seal(210, "right:84px; top:84px")}
<div style="position:absolute; left:84px; right:84px; bottom:{290 if corner else 150}px">
  {head}{who}{role}{session}
</div>
<div style="position:absolute; left:84px; right:{clear}px; bottom:80px">{foot}</div>""")
    # The seal stands small in the top corner, above the end of the longest name.
    return page(w, h, f"""
{frame}{goat}{seal(112, "right:44px; top:32px")}
<div style="position:absolute; left:{64 + size + 64}px; right:72px; top:{56 if h < 675 else 72}px">
  {head}{who}{role}{session}
</div>
<div style="position:absolute; left:{64 + size + 64}px; right:{clear}px; bottom:{48 if h < 675 else 60}px">{foot}</div>""")


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


def supporter_card(slug: str, meta, square: bool) -> str:
    w, h = (1080, 1080) if square else (1200, 675)
    logo = (SITE / meta["logo"]).as_uri()
    address = f"{URL}/{speakers.supporter_page_name(slug)[:-5]}"
    # A long address shrinks on the square card so it stays clear of the seal.
    url_px = (32 if len(address) <= 36 else 26) if square else 26
    return page(w, h, f"""
<div style="position:absolute; left:{84 if square else 72}px; top:{96 if square else 72}px; right:{84 if square else 460}px">
  <div class="sub" style="font-size:{40 if square else 32}px; color:#fff">Thank you,</div>
  <div class="word" style="font-size:{(120 if len(str(meta['name'])) <= 24 else 88) if square else 92}px; margin-top:16px">{esc(str(meta['name']))}</div>
  <div class="sub" style="font-size:{36 if square else 28}px; line-height:1.2; margin-top:28px">{thanks(meta)}</div>
</div>
<div style="position:absolute; {'left:84px; bottom:300px' if square else 'right:72px; top:72px'}; width:{420 if square else 340}px; height:{220 if square else 180}px; background:{logo_ground(meta)}; border-radius:18px; display:grid; place-items:center; padding:28px">
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
  <div class="sub" style="font-size:{40 if square else 32}px; color:#fff">Proud supporter of</div>
  <div class="word" style="font-size:{120 if square else 92}px; margin-top:16px">GoatConf 2027</div>
</div>
<div style="position:absolute; left:{84 if square else 72}px; top:{400 if square else 290}px; width:{560 if square else 400}px; height:{280 if square else 200}px; background:{logo_ground(meta)}; border-radius:18px; display:grid; place-items:center; padding:32px">
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
  <div class="sub" style="font-size:{46 if square else 30}px; color:#fff">Part of GoatConf 2027</div>
  <div class="word" style="font-size:{name_px}px; margin-top:{24 if square else 16}px">{esc(name)}</div>
  <div style="font-size:{40 if square else 28}px; font-weight:700; line-height:1.2; margin-top:{36 if square else 24}px; text-wrap:balance">Organised by {esc(str(meta["host"]))}</div>
  <div class="sub" style="font-size:{40 if square else 28}px; line-height:1.2; margin-top:{28 if square else 20}px">{esc(when)}<br>{esc(str(meta["location"]))}</div>
</div>
<div class="url" style="position:absolute; left:{84 if square else 72}px; bottom:{84 if square else 64}px; font-size:{32 if square else 26}px">{URL}/{extensions.page_name(slug)[:-5]}</div>
{seal(240 if square else 220, "right:72px; bottom:72px")}""")


def jobs() -> dict[str, tuple[int, int, str]]:
    out = {
        "linkedin-banner.png": (1584, 396, banner(1584, 396, 104, 36, 26, 320, 560, 90)),
        "linkedin-page-cover.png": (4200, 700, page_cover()),
        "header-3x1.png": (1500, 500, banner(1500, 500, 128, 40, 28, 400, 90, 96)),
        "og.png": (1200, 630, banner(1200, 630, 104, 34, 26, 400, 64, 56)),
        "luma-cover.png": (1080, 1080, page(1080, 1080, f"""
{seal(600, "left:240px; top:110px")}
<div style="position:absolute; left:0; right:0; bottom:110px; text-align:center">
  <div class="word" style="font-size:120px">GoatConf 2027</div>
  <div class="sub" style="font-size:42px; margin-top:24px">{FACTS}</div>
</div>""")),
    }
    for key, (title, line) in POSTS.items():
        out[f"post-{key}-square.png"] = (1080, 1080, post(1080, 1080, title, line, True))
        out[f"post-{key}-wide.png"] = (1200, 675, post(1200, 675, title.replace("<br>", " "), line, False))
    for key, (title, line, img, credit) in PHOTO_POSTS.items():
        out[f"post-{key}-square.png"] = (1080, 1080, photo_post(1080, 1080, title, line, img, credit, True))
        out[f"post-{key}-wide.png"] = (1200, 675, photo_post(1200, 675, title, line, img, credit, False))
    talks = speakers.sessions_by_speaker()
    for slug, (meta, _) in speakers.speakers().items():
        out[f"speaker-{slug}-square.png"] = (1080, 1080, speaker_card(slug, meta, talks.get(slug, []), True))
        out[f"speaker-{slug}-wide.png"] = (1200, 675, speaker_card(slug, meta, talks.get(slug, []), False))
        out[speakers.preview_name(slug)] = (1200, 630, speaker_card(slug, meta, talks.get(slug, []), False, 630))
        announce = speakers.announce_cards(slug)
        out[announce["square"]] = (1080, 1080, speaker_card(slug, meta, talks.get(slug, []), True, announce=True))
        out[announce["wide"]] = (1200, 675, speaker_card(slug, meta, talks.get(slug, []), False, announce=True))
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


def render(name: str, w: int, h: int, doc: str, tmp: Path, exe: str) -> None:
    src = tmp / f"{name}.html"
    src.write_text(doc, encoding="utf-8")
    shot = tmp / name
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=4000",
                    f"--window-size={w},{h + 200}", f"--screenshot={shot}", src.as_uri()],
                   check=True, capture_output=True, timeout=120)
    brand.crop(shot, OUT / name, w, h)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("--only")
    sub.add_parser("list")
    args = ap.parse_args(argv)
    todo = jobs()
    if args.cmd == "list":
        for name, (w, h, _) in todo.items():
            print(f"{name}  {w}x{h}")
        return 0
    OUT.mkdir(exist_ok=True)
    exe = brand.chrome()
    with tempfile.TemporaryDirectory() as tmp:
        for name, (w, h, doc) in todo.items():
            if args.only and args.only not in name:
                continue
            render(name, w, h, doc, Path(tmp), exe)
            print(f"rendered site/share/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
