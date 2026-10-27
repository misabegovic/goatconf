#!/usr/bin/env python3
"""GoatConf's sticker packs: one set of stickers, three ways to take them.

Every sticker is drawn in code: the goats by tools/goats.py, the mark and the
words here. Rendered with a white die-cut edge, each becomes a 512-pixel
transparent PNG (a chat or a slide takes it as it is, and it meets
Telegram's rules for static stickers), and the drawn ones keep their SVG.
The pack gathers them in one zip, and an A4 sheet lays them out to print and
cut. The Stickers page shows them all, with the downloads.

  render          draw every sticker to site/stickers/, then the zip and the
                  print sheet (needs Chrome and Pillow)
  build [--check] write site/stickers.html; with --check, fail if it is not
                  current or the pack is missing a sticker

Usage: python3 tools/stickers.py <render|build> [--check]
(ADR wiki/org/adrs/sticker-packs.md)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand  # noqa: E402
import frame  # noqa: E402
import goats  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402
import program  # noqa: E402
import sitelib  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "stickers"
PAGE = SITE / "stickers.html"
ZIP = "goatconf-stickers.zip"
SHEET = "goatconf-sticker-sheet.pdf"
SIZE = 512
esc = program.esc
# A fixed date inside the zip, so the same stickers make the same file.
ZIP_DATE = (2027, 6, 3, 9, 0, 0)

GROUPS = {
    "goats": ("The goat's roles", "The GoatConf goat in its roles from the EuRuKo 2024 goat multiverse."),
    "words": ("The mark and words", "The seal, the coin, and a few words to stick on things."),
    "tuzla": ("Tuzla things", "The town of salt, its lakes, its coffee and its food, and the goat on its plinth."),
}

DISPLAY = "font-family:'Bricolage Grotesque'; font-weight:800; text-transform:uppercase; line-height:.9"
HOOF = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 36 30 30"><g fill="#0b3d91">'
        '<path d="M30 40c-5 0-7 6-7 11s3 8 6 8c2 0 2-2 2-3z"/><path d="M34 40c5 0 7 6 7 11s-3 8-6 8c-2 0-2-2-2-3z"/></g></svg>')


def _words() -> list[tuple[str, str, str]]:
    """The mark and words, as HTML for the renderer: (slug, label, body)."""
    brand_dir = (SITE / "brand").as_uri()
    return [
        ("seal", "The seal", f'<img src="{brand_dir}/seal.svg" style="width:440px">'),
        ("coin", "The coin", f'<img src="{brand_dir}/coin.svg" style="width:380px">'),
        ("yours", "Yours?", f'<div style="transform:rotate(-9deg); background:#fff; border:16px solid #e30613; border-radius:28px; '
                            f'padding:14px 34px 22px; color:#e30613; font-size:120px; {DISPLAY}; font-stretch:80%">Yours?</div>'),
        ("im-speaking", "I'm speaking", f'<div style="transform:rotate(-3deg); background:#ffd400; border-radius:999px; padding:44px 56px 40px; '
                                        f'text-align:center; color:#051d47"><div style="font-size:96px; {DISPLAY}; font-stretch:78%">I\'m speaking</div>'
                                        f'<div style="font-size:42px; {DISPLAY}; font-stretch:85%; margin-top:14px">GoatConf 2027</div></div>'),
        ("tuzla-june", "Tuzla, 3–5 June 2027", f'<div style="transform:rotate(2deg); background:#0b3d91; border-radius:36px; padding:42px 52px 46px; '
                                               f'text-align:center"><div style="color:#ffd400; font-size:150px; {DISPLAY}; font-stretch:75%">Tuzla</div>'
                                               f'<div style="color:#fff; font-size:56px; {DISPLAY}; font-stretch:85%; margin-top:16px">3–5 June 2027</div></div>'),
        ("feeds", "The one that feeds the community", f'<div style="transform:rotate(-2deg); background:#ffd400; border-radius:24px; padding:40px 44px; '
                                                      f'text-align:center; color:#0b3d91; font-size:76px; {DISPLAY}; font-stretch:78%; width:430px">'
                                                      'The one that feeds the community</div>'),
        ("hooves", "Hoof prints", f'<div style="display:grid; grid-template-columns:150px 150px; gap:20px 50px; transform:rotate(-14deg)">'
                                  f'<div>{HOOF}</div><div style="margin-top:110px">{HOOF}</div></div>'),
    ]


I = goats.INK
L = goats.LINE
_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'


def _statue() -> str:
    """The goat on a plinth, in bronze, as Tuzla's goat statue."""
    goat = goats.role("goat").replace(goats.COAT, "#c7a86a").replace(goats.HORN, "#8a6a32").replace(goats.BLUSH, "#b8945a")
    goat = goat.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 18 200 186">', '<svg x="34" y="6" width="132" height="122" viewBox="0 18 200 186">')
    return (_SVG + f'<path d="M48 128h104l8 22H40z" fill="#9aa3b2" {L}/><rect x="56" y="150" width="88" height="34" fill="#b7bfcc" {L}/>'
            f'<path d="M44 184h112v10H44z" fill="#9aa3b2" {L}/><path d="M78 164h44" stroke="{I}" stroke-width="3" stroke-linecap="round"/>' + goat + "</svg>")


TUZLA = [
    ("salt", "A salt crystal", _SVG + f'<path d="M100 22l58 34v68l-58 34-58-34V56z" fill="#f4f8ff" {L}/><path d="M100 22v68l58 34M100 90l-58 34" fill="none" stroke="#9cb6dc" stroke-width="3"/>'
     f'<path d="M100 22l58 34-58 34-58-34z" fill="#fff" {L}/><path d="M64 150l20-12 20 12v22l-20 12-20-12z" fill="#e8f0fc" {L}/><path d="M138 152l14-8 14 8v16l-14 8-14-8z" fill="#e8f0fc" {L}/>'
     f'<path d="M76 70l6 3M118 60l8 4" stroke="#9cb6dc" stroke-width="3" stroke-linecap="round"/></svg>'),
    ("pannonian-sea", "The Pannonian sea", _SVG + f'<path d="M14 150c10-60 60-110 120-96 34 8 50 38 40 62-8 18-30 22-44 10 16 0 24-14 16-26-12-18-48-12-64 20-12 24-12 44-4 56z" fill="#2f6fd6" {L}/>'
     f'<path d="M130 126c14 12 36 8 44-10 6 8 6 18 0 24" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'
     f'<path d="M10 150c20 10 40 10 60 0s40-10 60 0 40 10 60 0v40H10z" fill="#0b3d91" {L}/><path d="M24 172c14 6 26 6 40 0M96 174c14 6 26 6 40 0" fill="none" stroke="#9cc3ff" stroke-width="4" stroke-linecap="round"/>'
     f'<circle cx="60" cy="96" r="5" fill="#fff"/><circle cx="74" cy="80" r="4" fill="#fff"/><circle cx="88" cy="70" r="3" fill="#fff"/></svg>'),
    ("fildzan", "A fildžan of coffee", _SVG + f'<ellipse cx="100" cy="162" rx="72" ry="18" fill="#fff" {L}/><ellipse cx="100" cy="158" rx="46" ry="9" fill="#e6eefb"/>'
     f'<path d="M58 84h84l-8 58a14 14 0 0 1-14 12H80a14 14 0 0 1-14-12z" fill="#fff" {L}/><ellipse cx="100" cy="84" rx="42" ry="9" fill="#5a3a22" {L}/>'
     f'<path d="M66 108h68M70 128h60" stroke="#2f6fd6" stroke-width="5"/><path d="M82 116l6 6 6-6 6 6 6-6 6 6 6-6" fill="none" stroke="#d7263d" stroke-width="3" stroke-linejoin="round"/>'
     f'<path d="M84 64c-8-10 8-14 0-26M100 62c-8-10 8-14 0-26M116 64c-8-10 8-14 0-26" fill="none" stroke="#9aa9c7" stroke-width="4" stroke-linecap="round"/>'
     f'<rect x="150" y="128" width="20" height="20" rx="3" fill="#fff" {L}/></svg>'),
    ("cevapi", "Ćevapi", _SVG + f'<ellipse cx="100" cy="120" rx="86" ry="52" fill="#fff" {L}/><path d="M30 118c0-30 32-50 70-50s70 20 70 50c-20 14-44 20-70 20s-50-6-70-20z" fill="#e9c88f" {L}/>'
     + "".join(f'<rect x="{x}" y="{y}" width="56" height="17" rx="8.5" fill="#8a4e2c" {L} transform="rotate({r} {x + 28} {y + 8})"/>' for x, y, r in ((50, 88, -8), (66, 104, -4), (84, 92, 4), (96, 110, -6), (110, 96, 6)))
     + f'<path d="M48 140c6-6 14-6 18 0M128 144c6-6 14-6 18 0M90 150c6-6 14-6 18 0" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'
     f'<path d="M48 140c6-6 14-6 18 0M128 144c6-6 14-6 18 0M90 150c6-6 14-6 18 0" fill="none" stroke="#c9a0d8" stroke-width="2" stroke-linecap="round"/></svg>'),
    ("burek", "Burek", _SVG + f'<ellipse cx="100" cy="112" rx="88" ry="76" fill="#fff" {L}/><circle cx="100" cy="108" r="68" fill="#e0a54e" {L}/>'
     f'<path d="M100 108m0-6a6 6 0 1 1-6 6c0-14 12-22 24-18 16 6 20 26 8 40-16 18-46 14-56-6-12-24 4-52 30-58 32-8 60 16 60 46" fill="none" stroke="#9a5e1e" stroke-width="5" stroke-linecap="round"/>'
     f'<path d="M50 80l8 4M140 70l6-6M150 130l8 2" stroke="#fff3d6" stroke-width="4" stroke-linecap="round"/></svg>'),
    ("goat-statue", "The goat statue", _statue()),
    ("salt-lakes", "The salt lakes", _SVG + f'<defs><clipPath id="lake"><circle cx="100" cy="100" r="82"/></clipPath></defs><circle cx="100" cy="100" r="82" fill="#bfe3ff"/>'
     f'<g clip-path="url(#lake)"><circle cx="140" cy="62" r="18" fill="#ffd400"/><path d="M0 108c30-8 60-8 100 0s70 8 100 0v100H0z" fill="#2f9be0"/>'
     f'<path d="M0 150c40-14 80-14 120-4s60 8 80 0v60H0z" fill="#f2dca8"/><path d="M24 128c12 4 22 4 34 0M110 124c12 4 22 4 34 0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
     f'<path d="M66 172V116" stroke="{I}" stroke-width="4"/><path d="M36 122c8-20 52-20 60 0z" fill="#e30613" {L}/><path d="M50 122c4-10 28-10 32 0" fill="none" stroke="#fff" stroke-width="4"/></g>'
     f'<circle cx="100" cy="100" r="82" fill="none" {L}/></svg>'),
]


def stickers() -> list[dict]:
    """The whole set, in order: group, slug, label, and an SVG (drawn) or HTML (lettered) body."""
    out = [{"group": "goats", "slug": f"goat-{r}", "label": goats.ROLE_NAMES[r], "svg": goats.role(r)} for r in goats.ROLE_NAMES]
    out += [{"group": "words", "slug": s, "label": label, "html": body} for s, label, body in _words()]
    out += [{"group": "tuzla", "slug": s, "label": label, "svg": body} for s, label, body in TUZLA]
    return out


def card(sticker: dict) -> str:
    """One sticker on a transparent 512-pixel square, with a white die-cut edge and a soft lift."""
    body = sticker.get("html") or f'<div style="width:400px">{sticker["svg"]}</div>'
    edge = " ".join(f"drop-shadow({x}px {y}px 0 #fff)" for x, y in ((7, 0), (-7, 0), (0, 7), (0, -7), (5, 5), (-5, 5), (5, -5), (-5, -5)))
    fonts = (SITE / "fonts").as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; }}
@font-face {{ font-family: "Bricolage Grotesque"; src: url("{fonts}/bricolage-wdth-latin-ext.woff2") format("woff2"); font-weight: 200 800; font-stretch: 75% 100%; unicode-range: U+0100-02BA; }}
* {{ margin: 0; box-sizing: border-box; }}
html, body {{ width: {SIZE}px; height: {SIZE}px; background: transparent; overflow: hidden; }}
body {{ display: grid; place-items: center; }}
.s {{ filter: {edge} drop-shadow(0 6px 6px rgb(0 0 0 / .22)); }}
svg {{ display: block; width: 100%; height: auto; }}
</style></head><body><div class="s">{body}</div></body></html>"""


def sheet_html(items: list[dict]) -> str:
    """An A4 sheet: every sticker at 45 mm, with room to cut around it."""
    cells = "".join(f'<figure><img src="{(OUT / (s["slug"] + ".png")).as_uri()}"><figcaption>{esc(s["label"])}</figcaption></figure>' for s in items)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 12mm; }}
body {{ margin: 0; font: 8pt sans-serif; color: #46557a; }}
h1 {{ font-size: 11pt; color: #0b3d91; margin: 0 0 6mm; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 45mm); gap: 4mm 1mm; justify-content: space-between; }}
figure {{ margin: 0; text-align: center; break-inside: avoid; }}
img {{ width: 45mm; height: 45mm; }}
</style></head><body><h1>GoatConf 2027 stickers · goatconf.com/stickers</h1><div class="grid">{cells}</div></body></html>"""


def render() -> int:
    from PIL import Image  # only render needs Pillow
    OUT.mkdir(exist_ok=True)
    (OUT / "svg").mkdir(exist_ok=True)
    exe = brand.chrome()
    items = stickers()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for s in items:
            src = tmp / f"{s['slug']}.html"
            src.write_text(card(s), encoding="utf-8")
            shot = tmp / f"{s['slug']}.png"
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=3000",
                            "--default-background-color=00000000", f"--window-size={SIZE},{SIZE + 200}", f"--screenshot={shot}", src.as_uri()],
                           check=True, capture_output=True, timeout=120)
            with Image.open(shot) as im:
                im.crop((0, 0, SIZE, SIZE)).save(OUT / f"{s['slug']}.png", optimize=True)
            if s.get("svg"):
                (OUT / "svg" / f"{s['slug']}.svg").write_text(s["svg"] + "\n", encoding="utf-8")
            print(f"rendered site/stickers/{s['slug']}.png")
        src = tmp / "sheet.html"
        src.write_text(sheet_html(items), encoding="utf-8")
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=3000",
                        f"--print-to-pdf={OUT / SHEET}", src.as_uri()], check=True, capture_output=True, timeout=120)
        print(f"rendered site/stickers/{SHEET}")
    with zipfile.ZipFile(OUT / ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for name in pack_files(items):
            info = zipfile.ZipInfo(f"goatconf-stickers/{name}", ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (OUT / name).read_bytes())
    print(f"wrote site/stickers/{ZIP}")
    return 0


def pack_files(items: list[dict]) -> list[str]:
    """What the zip holds: every sticker's PNG, and the SVG of every drawn one."""
    return [f"{s['slug']}.png" for s in items] + [f"svg/{s['slug']}.svg" for s in items if s.get("svg")]


def pack_problems() -> list[str]:
    """The pack matches the set: every PNG and SVG is there and current, and the zip holds exactly them."""
    items = stickers()
    out = [f"site/stickers/{n} is missing: run python3 tools/stickers.py render" for n in pack_files(items) + [ZIP, SHEET]
           if not (OUT / n).exists()]
    for s in items:
        p = OUT / "svg" / f"{s['slug']}.svg"
        if s.get("svg") and p.exists() and p.read_text(encoding="utf-8") != s["svg"] + "\n":
            out.append(f"site/stickers/svg/{s['slug']}.svg is out of date: run python3 tools/stickers.py render")
    if (OUT / ZIP).exists():
        with zipfile.ZipFile(OUT / ZIP) as z:
            if sorted(z.namelist()) != sorted(f"goatconf-stickers/{n}" for n in pack_files(items)):
                out.append(f"site/stickers/{ZIP} does not hold the current set: run python3 tools/stickers.py render")
    return out


def page() -> str:
    items = stickers()
    sections = []
    for group, (title, note) in GROUPS.items():
        cells = "\n".join(f'    <li class="sticker-dl"><a href="stickers/{s["slug"]}.png" download><img src="stickers/{s["slug"]}.png" width="512" height="512" '
                          f'alt="{esc(s["label"])}" loading="lazy"><span>{esc(s["label"])}</span></a></li>' for s in items if s["group"] == group)
        sections.append(f"""<section class="album-page wrap" aria-labelledby="h-{group}">
  <h2 class="band" id="h-{group}">{title}</h2>
  <p class="copy copy--wide">{note} Tap one to save it.</p>
  <ul class="sticker-grid">
{cells}
  </ul>
</section>""")
    main = f"""<section class="album-page wrap" aria-labelledby="h-take">
  <h2 class="band" id="h-take">Take them all</h2>
  <div class="copy copy--wide">
    <p>Every sticker as a transparent image, ready for chats, slides and posts, with the drawn ones also as SVG; or a sheet to print at home or at a print shop, and cut out.</p>
    <p class="cta"><a class="button" href="stickers/{ZIP}" download>Download the pack</a></p>
    <p><a class="go go--ink" href="stickers/{SHEET}" download>The print sheet (A4, PDF)</a></p>
    <p>The stickers are free to use for sharing GoatConf: on your laptop, in your slides, in your chats.</p>
  </div>
</section>
{chr(10).join(sections)}"""
    return frame.page("stickers", "Stickers: GoatConf 2027, 3–5 June, Tuzla",
                      "GoatConf 2027 stickers to download: the goat in its roles, the seal and a few words, as images or a sheet to print.",
                      ("brand/coin.svg", 300, 300, ""), "Stickers", "The goat, the seal and a few words, to stick on your laptop, your slides and your chats.",
                      main, "files/tools/stickers.py build", photo_class=" page-head__photo--mark")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("render")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if args.cmd == "render":
        return render()
    pages = {PAGE: nav.place(meta.tag(page()), nav.section(PAGE.name))}
    problems = pack_problems() if args.check else []
    for p in problems:
        print(p)
    return 1 if sitelib.write_or_check(pages, args.check, "tools/stickers.py build") or problems else 0

if __name__ == "__main__":
    sys.exit(main())
