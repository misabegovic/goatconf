#!/usr/bin/env python3
"""Goatchi: keep a GoatConf goat, a little game like a tamagotchi, on a page of its own.

A visitor picks a goat (the plain goat, a role goat, or a speaker's goat once that speaker said yes), and keeps
it in their own browser: they feed it, play with it and let it sleep, and it sulks when left alone but never
dies. The page is written here; the game is site/goatchi.js, loaded on this page only, and the rest of the site
is unchanged apart from a link in the footer.

Goatchi can be installed on its own (ADR wiki/org/adrs/goatchi-full-game.md): this tool also writes its web manifest
and its home-screen icons, cut from the sitting goat on the album's blue; site/goatchi-sw.js is its service worker,
registered by goatchi.js for the Goatchi page only, once a goat is kept.

  build [--check]  write site/goatchi.html, its manifest and icons; with --check, fail if any is not current

Usage: python3 tools/goatchi.py build [--check]
(ADR wiki/org/adrs/goat-tamagotchi-on-the-site.md)
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from html import escape as esc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame  # noqa: E402
import goat_atlas  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402
import sitelib  # noqa: E402
import speakers  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "goatchi.html"
MANIFEST = ROOT / "site" / "goatchi.webmanifest"
# The home-screen icons: name, size, and how much of the square the goat fills (less for the maskable one, which a
# phone may crop to a circle).
ICONS = (("img/goatchi-icon-192.png", 192, 0.82, ""), ("img/goatchi-icon-512.png", 512, 0.82, ""),
         ("img/goatchi-icon-maskable-512.png", 512, 0.62, "maskable"))
BLUE = (11, 61, 145)
# The goats anyone can keep, in order, with their names.
NAMES = {"sitting": "The goat", "sticker-host": "The host", "sticker-coder": "The coder", "sticker-speaker": "The speaker",
         "sticker-cook": "The cook", "sticker-pirate": "The pirate", "sticker-hidden": "The shy one"}
FOOD = goat_atlas.GOATCHI_FOOD
# The first day of GoatConf 2027, which the goat counts down to.
DAY_ONE = "2027-06-03"
# The postcards a kept goat sends from Tuzla, at so many days kept (ADR goatchi-full-game): photos the site already
# shows, each with the credit its giver asked for.
POSTCARDS = ((7, "city-lakes-aerial-summer", "The salt lakes"), (30, "city-square-fountain-summer", "Freedom Square"),
             (100, "city-korzo-clock", "The Korzo"))


def postcards() -> list:
    out = []
    for day, photo, place in POSTCARDS:
        info = json.loads((ROOT / "assets" / "images" / "city" / f"{photo}.jpg.json").read_text(encoding="utf-8"))
        w, h = goat_atlas.webp_size(ROOT / "site" / "img" / f"{photo}-480.webp")
        out.append({"day": day, "src": f"img/{photo}-480.webp", "w": w, "h": h, "place": place, "alt": info["title"],
                    "credit": info["required_credit_line"]})
    return out


def poses(goat: str) -> dict:
    """The goat's own poses on the site, each as the pictures it may show."""
    return {pose: [goat_atlas.single(n)[0] for n in names] for pose, names in goat_atlas.goatchi_poses(goat).items()}


def goats(people) -> list:
    """The goats a visitor can keep: the plain and role goats, then each speaker's goat whose speaker said yes
    (`goat_keep: yes` in their record), in the organiser's order."""
    out = [{"pose": p, "name": NAMES[p], "speaker": ""} for p in goat_atlas.GOATCHI_GOATS]
    for slug, m in people:
        pose = f"speaker-{slug}-sitting"
        if m.get("goat_keep") is True and goat_atlas.has(pose):
            out.append({"pose": pose, "name": f"{m['name']}'s goat", "speaker": speakers.page_name(slug)})
    return out


def _img(pose: str, cls: str, alt: str = "", lazy: bool = True) -> str:
    src, w, h = goat_atlas.single(pose)
    return f'<img class="{cls}" src="{src}" width="{w}" height="{h}" alt="{esc(alt)}"{" loading=\"lazy\"" if lazy else ""} decoding="async">'


def page() -> str:
    people = [(slug, m) for slug, (m, _body) in speakers.listed(speakers.speakers())]
    picks = "\n".join(
        f'    <li><button type="button" class="goatchi__pick-goat" data-pose="{g["pose"]}" data-name="{esc(g["name"])}" '
        f'data-src="{goat_atlas.single(g["pose"])[0]}" data-speaker="{g["speaker"]}" '
        f'data-poses="{esc(json.dumps(poses(g["pose"]), separators=(",", ":")))}">{_img(g["pose"], "goatchi__thumb")}'
        f'<span>{esc(g["name"])}</span></button></li>' for g in goats(people))
    cards = "\n".join(
        f'          <li class="goatchi__card" data-day="{c["day"]}"><span class="goatchi__card-lock">At {c["day"]} days</span>'
        f'<figure hidden><img src="{c["src"]}" width="{c["w"]}" height="{c["h"]}" alt="{esc(c["alt"])}" loading="lazy" decoding="async">'
        f'<figcaption>{esc(c["place"])} <small>{esc(c["credit"])}</small></figcaption></figure></li>' for c in postcards())
    food = "|".join(goat_atlas.single(p)[0] for p in FOOD)
    main = f"""<section class="album-page wrap" id="goatchi" aria-labelledby="h-goat" data-food="{food}" data-sleep="{goat_atlas.single("asleep")[0]}" data-day="{DAY_ONE}">
  <h2 class="band" id="h-goat">Your goat</h2>
  <div class="goatchi__play" hidden>
    <figure class="goatchi__stage">
      <b class="goatchi__say" aria-live="polite"></b>
      <img class="goatchi__goat" src="{goat_atlas.single("sitting")[0]}" alt="">
      <figcaption><span class="goatchi__name"></span> <span class="goatchi__kept"></span></figcaption>
    </figure>
    <div class="goatchi__care">
      <ul class="goatchi__needs">
        <li><span id="need-food">Food</span> <span class="goatchi__bar" role="meter" aria-labelledby="need-food" aria-valuemin="0" aria-valuemax="100" data-need="food"></span> <span class="goatchi__pct" data-pct="food"></span></li>
        <li><span id="need-play">Play</span> <span class="goatchi__bar" role="meter" aria-labelledby="need-play" aria-valuemin="0" aria-valuemax="100" data-need="play"></span> <span class="goatchi__pct" data-pct="play"></span></li>
        <li><span id="need-sleep">Sleep</span> <span class="goatchi__bar" role="meter" aria-labelledby="need-sleep" aria-valuemin="0" aria-valuemax="100" data-need="sleep"></span> <span class="goatchi__pct" data-pct="sleep"></span></li>
      </ul>
      <p class="goatchi__lasts"></p>
      <p class="goatchi__acts"><button type="button" class="button" data-act="feed">Feed</button> <button type="button" class="button" data-act="play">Play</button> <button type="button" class="button" data-act="sleep">Sleep</button></p>
      <p class="goatchi__trip"></p>
      <div class="goatchi__mail">
        <p class="goatchi__mail-intro">Postcards from Tuzla, the longer you keep your goat:</p>
        <ul class="goatchi__cards">
{cards}
        </ul>
      </div>
      <p class="goatchi__cheers-intro">Your goat cheers up the first time you:</p>
      <ul class="goatchi__cheers">
        <li><a data-cheer="speaker" href="speakers.html">See who is speaking</a></li>
        <li><a data-cheer="register" href="register.html">Register for free</a></li>
        <li><a data-cheer="share" href="stickers.html">Share a sticker</a></li>
      </ul>
      <p class="goatchi__confirm" hidden><span></span> <button type="button" class="goatchi__link" data-act="yes">Yes</button> <button type="button" class="goatchi__link" data-act="no">No</button></p>
      <p><button type="button" class="goatchi__link" data-act="let-go">Let your goat go</button></p>
      <p class="goatchi__install" hidden><button type="button" class="button">Add Goatchi to your home screen</button></p>
      <p class="goatchi__remind goatchi__mode" hidden><label><input type="checkbox"> Tell me when my goat needs me</label> <span class="goatchi__remind-note" aria-live="polite"></span></p>
    </div>
  </div>
  <div class="goatchi__empty copy copy--wide">
    <p>Pick a goat below and keep it: feed it, play with it, and let it sleep. It counts the days to Tuzla with you.</p>
  </div>
  <div class="goatchi__gone copy copy--wide" hidden>
    {_img(goat_atlas.GOATCHI_GONE, "goatchi__hike", "The goat hiking in the hills above Tuzla")}
    <p class="goatchi__gone-line"></p>
    <p>Pick a goat below to keep another.</p>
  </div>
  <noscript><p class="copy copy--wide">Goatchi needs JavaScript to keep your goat.</p></noscript>
</section>

<section class="album-page wrap" aria-labelledby="h-pick">
  <h2 class="band" id="h-pick">Pick a goat</h2>
  <p class="copy copy--wide">Your goat lives in this browser only: nothing about it is sent anywhere, and clearing your browser's data lets it go. You can swap it for another at any time.</p>
  <p class="copy copy--wide goatchi__mode"><label><input type="checkbox" class="goatchi__challenge"> Challenge mode: left with every need empty for three days, your goat wanders off to explore the hills above Tuzla.</label></p>
  <ul class="sticker-grid goatchi__pick">
{picks}
  </ul>
</section>

<section class="album-page wrap" aria-labelledby="h-how">
  <h2 class="band" id="h-how">How it works</h2>
  <div class="copy copy--wide">
    <p>Goatchi is a little game like a tamagotchi. Your goat gets hungry, bored and sleepy over about a day and a half. Left alone it sulks and says so, but it never dies: feed it, play with it or let it sleep, and it is glad you came back.</p>
    <p>In challenge mode, which you choose when you pick a goat, a goat left with every need empty for three days wanders off to explore the hills above Tuzla, and the page tells you how many days you kept it.</p>
    <p>A speaker's goat can be kept once that speaker has said yes. The goats, the name GoatConf and Goatchi are <a href="brand.html#use">all rights reserved</a>.</p>
  </div>
</section>"""
    src, w, h = goat_atlas.single("sitting")
    html = frame.page("goatchi", "Goatchi: keep a GoatConf goat",
                      "Goatchi: keep a GoatConf goat in your browser. Feed it, play with it and let it sleep; it counts the days to GoatConf in Tuzla.",
                      (src, w, h, ""), "Goatchi", "Keep a GoatConf goat: feed it, play with it, and let it sleep. It lives in your browser and never dies.",
                      main, "files/tools/goatchi.py build", preview="goatchi-preview.png", photo_class=" page-head__photo--mark")
    # A kept goat's game comes first on phones: known before the page paints, so nothing jumps once it has.
    html = html.replace('<link rel="stylesheet" href="goatconf.css">',
                        '<script>try{localStorage.getItem("goatconf-goatchi")&&document.documentElement.classList.add("goatchi-kept")}catch(e){}</script>\n'
                        '<link rel="stylesheet" href="goatconf.css">', 1)
    html = html.replace('<link rel="apple-touch-icon" href="apple-touch-icon.png">',
                        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="manifest" href="goatchi.webmanifest">', 1)
    return html.replace('<script src="album.js" defer></script>', '<script src="album.js" defer></script>\n<script src="goatchi.js" defer></script>')


def manifest() -> str:
    """Goatchi as an app of its own: it starts at goatchi.html, and its scope is the Goatchi page only."""
    icons = [{"src": src, "sizes": f"{n}x{n}", "type": "image/png", **({"purpose": purpose} if purpose else {})}
             for src, n, _fill, purpose in ICONS]
    return json.dumps({
        "id": "goatchi.html", "name": "Goatchi: keep a GoatConf goat", "short_name": "Goatchi",
        "description": "Keep a GoatConf goat: feed it, play with it and let it sleep. It counts the days to GoatConf in Tuzla.",
        "start_url": "goatchi.html", "scope": "goatchi", "display": "standalone",
        "background_color": "#0b3d91", "theme_color": "#0b3d91", "icons": icons,
    }, indent=1, ensure_ascii=False) + "\n"


def icon(n: int, fill: float) -> bytes:
    """The sitting goat, centred on the album's blue, as a PNG."""
    from PIL import Image
    goat = Image.open(ROOT / "site" / goat_atlas.single("sitting")[0].split("?")[0]).convert("RGBA")
    k = n * fill / max(goat.size)
    goat = goat.resize((round(goat.width * k), round(goat.height * k)), Image.LANCZOS)
    out = Image.new("RGBA", (n, n), BLUE + (255,))
    out.alpha_composite(goat, ((n - goat.width) // 2, (n - goat.height) // 2))
    buf = io.BytesIO()
    out.convert("RGB").save(buf, "PNG", optimize=True)
    return buf.getvalue()


def write_app(check: bool) -> int:
    """The manifest and the icons; the icons are only checked to exist, since they need Pillow to draw."""
    stale = 0
    have = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else ""
    if have != manifest():
        if check:
            print(f"site/{MANIFEST.name} is out of date: run python3 tools/goatchi.py build")
            stale += 1
        else:
            MANIFEST.write_text(manifest(), encoding="utf-8")
            print(f"wrote site/{MANIFEST.name}")
    for src, n, fill, _purpose in ICONS:
        path = ROOT / "site" / src
        if check:
            if not path.exists():
                print(f"site/{src} is missing: run python3 tools/goatchi.py build")
                stale += 1
        else:
            path.write_bytes(icon(n, fill))
            print(f"wrote site/{src}")
    return stale


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    pages = {PAGE: nav.place(meta.tag(page()), nav.section(PAGE.name))}
    stale = sitelib.write_or_check(pages, args.check, "tools/goatchi.py build") + write_app(args.check)
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
