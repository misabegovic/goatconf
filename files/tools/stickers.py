#!/usr/bin/env python3
"""GoatConf's sticker packs: one set of stickers, three ways to take them.

The goats are the painted goat (art/goat/, ADR goat-mascot): in its roles, out
in Tuzla, and as each speaker's own goat. The mark and the words are lettered
here. Rendered with a white die-cut edge, each becomes a 512-pixel
transparent PNG (a chat or a slide takes it as it is, and it meets
Telegram's rules for static stickers).
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
import goat_atlas  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402
import program  # noqa: E402
import sitelib  # noqa: E402
import speakers  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "stickers"
PAGE = SITE / "stickers.html"
ZIP = "goatconf-stickers.zip"
SPEAKER_ZIP = "goatconf-speaker-stickers.zip"
SHEET = "goatconf-sticker-sheet.pdf"
SIZE = 512
# The previews the Stickers page shows: about twice their size on screen, for sharp phones.
PREVIEW = 256
esc = program.esc
# A fixed date inside the zip, so the same stickers make the same file.
ZIP_DATE = (2027, 6, 3, 9, 0, 0)

GROUPS = {
    "goats": ("The goat's roles", "The GoatConf goat in its roles from the EuRuKo 2024 goat multiverse."),
    "words": ("The mark and words", "The seal, the coin, and a few words to stick on things."),
    "tuzla": ("Tuzla things", "The goat in the town of salt: in its lakes, at its coffee and its food, and on its plinth."),
    "speakers": ("The speakers' goats", "Each speaker's own goat, painted to look like them, in a pack of their own. They show real people: share them, and never use them to mock."),
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


# The goat's roles and its days in Tuzla, each a painted master in art/goat/ (sticker-<name>.webp).
ROLES = [("goat", "The goat"), ("speaker", "The speaker"), ("host", "The host"), ("coder", "The coder"),
         ("cook", "The cook"), ("pirate", "The Pannonian pirate"), ("hidden", "The hidden goat")]
TUZLA = [("salt-lakes", "A float in the salt lakes"), ("pannonian-sea", "A jump into the lake"), ("beach", "A day on the beach"),
         ("salt", "A lick of Tuzla salt"), ("cevapi", "Ćevapi"), ("burek", "Burek"), ("fildzan", "A fildžan of coffee"),
         ("hike", "A hike out of town"), ("goat-statue", "The goat statue")]


def _painted(pose: str) -> str:
    return f'<img src="{(goat_atlas.ART / (pose + ".webp")).as_uri()}" style="display:block; max-width:420px; max-height:440px">'


def stickers() -> list[dict]:
    """The whole set, in order: group, slug, label, and the HTML that shows it, painted or lettered."""
    out = [{"group": "goats", "slug": f"goat-{r}", "label": label, "html": _painted(f"sticker-{r}")} for r, label in ROLES]
    out += [{"group": "words", "slug": s, "label": label, "html": body} for s, label, body in _words()]
    out += [{"group": "tuzla", "slug": s, "label": label, "html": _painted(f"sticker-{s}")} for s, label in TUZLA]
    for slug, (meta_, _body) in speakers.listed(speakers.speakers()):
        if goat_atlas.has(f"speaker-{slug}-sitting"):
            name = esc(str(meta_["name"]))
            img = _painted(f"speaker-{slug}-sitting").replace("max-width:420px; max-height:440px", "max-width:330px; max-height:370px")
            out.append({"group": "speakers", "slug": f"speaker-{slug}", "label": str(meta_["name"]),
                        "html": f'<div style="width:400px; display:grid; justify-items:center">{img}<div style="margin-top:-14px; background:#0b3d91; color:#fff; '
                                f'border-radius:14px; padding:12px 22px 10px; font-size:44px; {DISPLAY}; font-stretch:78%; text-align:center; max-width:470px">{name}</div></div>'})
    return out


def card(sticker: dict) -> str:
    """One sticker on a transparent 512-pixel square, with a white die-cut edge and a soft lift."""
    body = sticker["html"]
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
    (OUT / "preview").mkdir(exist_ok=True)
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
                im = im.crop((0, 0, SIZE, SIZE))
                im.save(OUT / f"{s['slug']}.png", optimize=True)
                # The page shows a small WebP of each; the PNG is the download.
                im.resize((PREVIEW, PREVIEW), Image.LANCZOS).save(OUT / "preview" / f"{s['slug']}.webp", quality=80, method=6)
            print(f"rendered site/stickers/{s['slug']}.png")
        src = tmp / "sheet.html"
        src.write_text(sheet_html(items), encoding="utf-8")
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=3000",
                        f"--print-to-pdf={OUT / SHEET}", src.as_uri()], check=True, capture_output=True, timeout=120)
        print(f"rendered site/stickers/{SHEET}")
    for zip_name, folder, group in ((ZIP, "goatconf-stickers", "main"), (SPEAKER_ZIP, "goatconf-speaker-stickers", "speakers")):
        with zipfile.ZipFile(OUT / zip_name, "w", zipfile.ZIP_DEFLATED) as z:
            for name in pack_files(_pack(items, group)):
                info = zipfile.ZipInfo(f"{folder}/{name}", ZIP_DATE)
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, (OUT / name).read_bytes())
        print(f"wrote site/stickers/{zip_name}")
    return 0


def _pack(items: list[dict], which: str) -> list[dict]:
    """The main pack holds every sticker but the speakers' goats, which have a pack of their own."""
    return [s for s in items if (s["group"] == "speakers") == (which == "speakers")]


def pack_files(items: list[dict]) -> list[str]:
    """What the zip holds: every sticker's PNG."""
    return [f"{s['slug']}.png" for s in items]


def pack_problems() -> list[str]:
    """The pack matches the set: every PNG is there, and the zip holds exactly them."""
    items = stickers()
    previews = [f"preview/{s['slug']}.webp" for s in items]
    out = [f"site/stickers/{n} is missing: run python3 tools/stickers.py render" for n in pack_files(items) + previews + [ZIP, SPEAKER_ZIP, SHEET]
           if not (OUT / n).exists()]
    for zip_name, folder, group in ((ZIP, "goatconf-stickers", "main"), (SPEAKER_ZIP, "goatconf-speaker-stickers", "speakers")):
        if (OUT / zip_name).exists():
            with zipfile.ZipFile(OUT / zip_name) as z:
                if sorted(z.namelist()) != sorted(f"{folder}/{n}" for n in pack_files(_pack(items, group))):
                    out.append(f"site/stickers/{zip_name} does not hold the current set: run python3 tools/stickers.py render")
    return out


def page() -> str:
    items = stickers()
    sections = []
    for group, (title, note) in GROUPS.items():
        cells = "\n".join(f'    <li class="sticker-dl"><a href="stickers/{s["slug"]}.png" download><img src="stickers/preview/{s["slug"]}.webp" width="{PREVIEW}" height="{PREVIEW}" '
                          f'alt="{esc(s["label"])}" loading="lazy"><span>{esc(s["label"])}</span></a></li>' for s in items if s["group"] == group)
        sections.append(f"""<section class="album-page wrap" aria-labelledby="h-{group}">
  <h2 class="band" id="h-{group}">{title}</h2>
  <p class="copy copy--wide">{note} Tap one to save it.</p>
  <ul class="sticker-grid">
{cells}
  </ul>{f"""
  <p class="copy"><a class="go go--ink" href="stickers/{SPEAKER_ZIP}" download>Download the speakers' pack</a></p>""" if group == "speakers" else ""}
</section>""")
    main = f"""<section class="album-page wrap" aria-labelledby="h-take">
  <h2 class="band" id="h-take">Take them all</h2>
  <div class="copy copy--wide">
    <p>Every sticker as a transparent image, ready for chats, slides and posts, or a sheet to print at home or at a print shop, and cut out.</p>
    <p class="cta"><a class="button" href="stickers/{ZIP}" download>Download the pack</a></p>
    <p>The speakers' goats have a pack of their own, below.</p>
    <p><a class="go go--ink" href="stickers/{SHEET}" download>The print sheet (A4, PDF)</a></p>
    <p>The stickers are free to use for sharing GoatConf: on your laptop, in your slides, in your chats.</p>
  </div>
</section>
{chr(10).join(sections)}"""
    return frame.page("stickers", "Stickers: GoatConf 2027, 3–5 June, Tuzla",
                      "GoatConf 2027 stickers to download: the goat in its roles and out in Tuzla, the seal and a few words, as images or a sheet to print.",
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
