#!/usr/bin/env python3
"""The GoatConf brand kit: build every mark from one source.

The goat is the EuRuKo 2024 goat, traced once into site/brand/goat-outline.json.
This script smooths it into curves and builds, into site/brand/:

  goat.svg                 the goat alone
  coin.svg                 the small form: the goat in a disc (also the favicon)
  seal.svg                 the full seal: THE ONE THAT FEEDS THE COMMUNITY,
                           GOATCONF · 2027, and a band of hoof prints
  lockup-horizontal.svg    the coin with the wordmark beside it
  lockup-stacked.svg       the seal with the wordmark and the line below it

Seal and lockups carry their lettering as outlines of the site's display
face, so they need no font and render the same anywhere. The outlines, with
each letter's advance and kerning, live in assets/brand/lettering.json,
written once from the font by `lettering`; build lays them out from there.

  build [--check]   write the SVG files (and site/favicon.svg); with --check,
                    fail if a committed file is not current
  lettering         write assets/brand/lettering.json from the display face
                    (needs fontTools; run it when the lettering's words or the
                    font change)
  render            also export PNG and PDF files through headless Chrome
                    (not checked by CI: Chrome's raster output is not byte-stable)
  icons             only the raster favicons: site/favicon-96.png and
                    site/favicon.ico, for search engines and browsers that
                    skip the SVG (render writes them too)

Usage: python3 tools/brand.py <build|lettering|render|icons> [--check]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "brand"
# the full display face (tools/fonts.py publishes a trimmed copy in site/fonts/)
FONT = ROOT / "assets" / "fonts" / "bricolage-wdth-latin.woff2"
LETTERING = ROOT / "assets" / "brand" / "lettering.json"

BLUE, YELLOW, NIGHT, WHITE, INK = "#0b3d91", "#ffd400", "#051d47", "#ffffff", "#12204a"
TOP_LINE = "THE ONE THAT FEEDS THE COMMUNITY"
BOTTOM_LINE = "GOATCONF · 2027"
# Each run of lettering the marks carry: its words, and the display face's
# weight, width and optical size (a browser sets the optical size to the font
# size, which is what the marks used when they were drawn as text).
RUNS = {
    "top": (TOP_LINE, 800, 75, 24.5),
    "bottom": (BOTTOM_LINE, 800, 75, 18),
    "word": ("GOATCONF", 800, 75, 96),
    "line": ("The one that feeds the community.", 700, 85, 30),
}


def arc(x0: float, y0: float, x1: float, y1: float, sweep: int, cx: float = 150, cy: float = 150) -> tuple[float, float]:
    """An arc of the seal's lettering circle from one point to another, as (start angle, length), in degrees."""
    a0 = math.degrees(math.atan2(y0 - cy, x0 - cx))
    a1 = math.degrees(math.atan2(y1 - cy, x1 - cx))
    return a0, ((a1 - a0) if sweep else (a0 - a1)) % 360


ARC_TOP = arc(40.4, 173.3, 259.6, 173.3, 1)   # clockwise over the top
ARC_BOT = arc(47.7, 195.6, 252.3, 195.6, 0)   # anticlockwise under the bottom
# Where a hanging baseline sits, as a share of the em: the bottom line of the
# seal hangs from its arc, as dominant-baseline="hanging" set it in Chrome.
HANGING = 0.746
HOOF = "M3.4 1C1.2 4 1 9 3 12.6c2.2-.6 2.8-6.4.4-11.6zM8.6 1c2.2 3 2.4 8 .4 11.6-2.2-.6-2.8-6.4-.4-11.6z"


def goat_path() -> str:
    """The traced outline as smooth cubic curves; turns sharper than 40 degrees stay corners."""
    data = json.loads((OUT / "goat-outline.json").read_text(encoding="utf-8"))
    parts = []
    for pts in data["loops"]:
        n = len(pts)

        def corner(i):
            (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[(i + 1) % n]
            a1, a2 = math.atan2(by - ay, bx - ax), math.atan2(cy - by, cx - bx)
            turn = abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi)
            return turn > math.radians(40)

        sharp = [corner(i) for i in range(n)]
        out = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
        for i in range(n):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            if sharp[i] or sharp[(i + 1) % n]:
                # keep at least one end crisp: tangent collapses to the point itself
                t1 = p1 if sharp[i] else ((p1[0] + (p2[0] - p0[0]) / 6), (p1[1] + (p2[1] - p0[1]) / 6))
                t2 = p2 if sharp[(i + 1) % n] else ((p2[0] - (p3[0] - p1[0]) / 6), (p2[1] - (p3[1] - p1[1]) / 6))
            else:
                t1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
                t2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            out.append(f"C{t1[0]:.1f} {t1[1]:.1f} {t2[0]:.1f} {t2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
        parts.append(" ".join(out) + "Z")
    return " ".join(parts)


_lettering = None


def lettering() -> dict:
    global _lettering
    if _lettering is None:
        _lettering = json.loads(LETTERING.read_text(encoding="utf-8"))
    return _lettering


def glyphs(run: str, first: int = 0, last: int | None = None) -> list[dict]:
    """A run's letters, or a slice of them; the last letter keeps no kerning to a letter that is not there."""
    gs = lettering()["runs"][run]["glyphs"][first:last]
    return gs[:-1] + [dict(gs[-1], kern=0)] if gs else gs


def advances(gs: list[dict], size: float, spacing: float) -> list[float]:
    k = size / 1000
    return [(g["adv"] + g["kern"]) * k + spacing for g in gs]


# Each letter's outline, drawn once per file in <defs> and placed with <use>.
SHAPES: dict[str, str] = {}


def glyph(run: str, g: dict, transform: str) -> str:
    if not g["d"]:
        return ""
    gid = f"{run}-{ord(g['char'])}"
    SHAPES[gid] = g["d"]
    return f'<use href="#{gid}" transform="{transform}"/>'


def straight(run: str, x: float, y: float, size: float, spacing: float, first: int = 0, last: int | None = None) -> str:
    """Letters along a baseline from (x, y), as <text x y> set them."""
    gs, k, out = glyphs(run, first, last), size / 1000, []
    for g, adv in zip(gs, advances(gs, size, spacing)):
        out.append(glyph(run, g, f"translate({x:.2f} {y:.2f}) scale({k:.5f} {-k:.5f})"))
        x += adv
    return "".join(out)


def on_arc(run: str, size: float, spacing: float, start_deg: float, sweep: int, hanging: bool = False,
           cx: float = 150, cy: float = 150, r: float = 112, length_deg: float = 0) -> str:
    """Letters centred along a circular arc, each standing on it at its own midpoint,
    as <textPath startOffset="50%" text-anchor="middle"> set them."""
    gs, k = glyphs(run), size / 1000
    adv = advances(gs, size, spacing)
    turn = 1 if sweep else -1
    s = r * math.radians(length_deg) / 2 - sum(adv) / 2
    drop = HANGING * size if hanging else 0
    out = []
    for g, a in zip(gs, adv):
        w = (g["adv"] + g["kern"]) * k
        theta = math.radians(start_deg) + turn * (s + w / 2) / r
        x, y = cx + r * math.cos(theta), cy + r * math.sin(theta)
        rot = math.degrees(theta) + turn * 90
        out.append(glyph(run, g, f"translate({x:.2f} {y:.2f}) rotate({rot:.2f}) translate({-w / 2:.2f} {drop:.2f}) scale({k:.5f} {-k:.5f})"))
        s += a
    return "".join(out)


def hoof_band(fg: str, r0=78, n=20, size=10.5) -> str:
    out = []
    for i in range(n):
        a = i / n * 2 * math.pi
        r = r0 + (2.4 if i % 2 else -2.4)
        x, y = 150 + r * math.cos(a), 150 + r * math.sin(a)
        deg = math.degrees(a) + 180
        s = size / 12
        out.append(f'<path transform="translate({x:.2f} {y:.2f}) rotate({deg:.1f}) scale({s:.4f}) translate(-6 -7)" d="{HOOF}"/>')
    return f'<g fill="{fg}">{"".join(out)}</g>'


def goat_in(fg: str, x: float, y: float, w: float, clip_r: float, cid: str) -> str:
    """The goat placed as a bust inside a circle of radius clip_r around (150, 150)."""
    s = w / 394
    return (f'<clipPath id="{cid}"><circle cx="150" cy="150" r="{clip_r}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><path fill="{fg}" fill-rule="evenodd" '
            f'transform="translate({x} {y}) scale({s:.5f})" d="{goat_path()}"/></g>')


def seal_body(fg: str, bg: str, cid: str = "seal-coin") -> str:
    return (
        f'<circle cx="150" cy="150" r="146" fill="{bg}"/>'
        f'<circle cx="150" cy="150" r="138" fill="none" stroke="{fg}" stroke-width="4"/>'
        f'<circle cx="150" cy="150" r="88" fill="none" stroke="{fg}" stroke-width="4"/>'
        f'<circle cx="150" cy="150" r="68" fill="none" stroke="{fg}" stroke-width="3"/>'
        f'<g fill="{fg}">'
        # the top line runs clockwise over the top, from (40.4, 173.3) to (259.6, 173.3);
        # the bottom line anticlockwise under it, from (47.7, 195.6) to (252.3, 195.6)
        + on_arc("top", 24.5, 1.1, ARC_TOP[0], 1, length_deg=ARC_TOP[1])
        + on_arc("bottom", 18, 1.3, ARC_BOT[0], 0, hanging=True, length_deg=ARC_BOT[1])
        + '<path d="M33 190 l5 -5 l5 5 l-5 5 Z"/><path d="M257 190 l5 -5 l5 5 l-5 5 Z"/></g>'
        + hoof_band(fg)
        + goat_in(fg, 86, 86, 130, 66, cid)
    )


def coin_body(fg: str, bg: str, cid: str = "coin") -> str:
    return (f'<circle cx="150" cy="150" r="146" fill="{bg}"/>'
            f'<circle cx="150" cy="150" r="128" fill="none" stroke="{fg}" stroke-width="12"/>'
            + goat_in(fg, 52, 40, 212, 122, cid))


def svg(view: str, body: str, title: str) -> str:
    used = sorted(set(re.findall(r'<use href="#([a-z]+-[0-9]+)"', body)))
    defs = f'<defs>{"".join(f"<path id={chr(34)}{i}{chr(34)} d={chr(34)}{SHAPES[i]}{chr(34)}/>" for i in used)}</defs>' if used else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{defs}{body}</svg>\n')


def word(fill: str, x: float, y: float, size: float, first: int = 0, last: int | None = None) -> str:
    """GOATCONF (or a slice of it) in the display face, letter-spaced 0.5."""
    return f'<g fill="{fill}">{straight("word", x, y, size, 0.5, first, last)}</g>'


def files() -> dict[str, str]:
    goat = goat_path()
    return {
        "goat.svg": svg("0 0 394 449", f'<path fill="{BLUE}" fill-rule="evenodd" d="{goat}"/>', "The GoatConf goat"),
        "coin.svg": svg("0 0 300 300", coin_body(YELLOW, BLUE), "GoatConf"),
        "coin-yellow.svg": svg("0 0 300 300", coin_body(BLUE, YELLOW), "GoatConf"),
        "seal.svg": svg("0 0 300 300", seal_body(BLUE, YELLOW), "GoatConf: the one that feeds the community"),
        "seal-blue.svg": svg("0 0 300 300", seal_body(YELLOW, BLUE), "GoatConf: the one that feeds the community"),
        "seal-black.svg": svg("0 0 300 300", seal_body("#111111", WHITE), "GoatConf: the one that feeds the community"),
        "lockup-horizontal.svg": svg("0 0 1000 300",
            f'<g>{coin_body(YELLOW, BLUE)}</g>' + word(BLUE, 330, 212, 170),
            "GoatConf"),
        "lockup-stacked.svg": svg("0 0 900 360",
            f'<g transform="translate(20 20) scale(1.066)">{seal_body(BLUE, YELLOW)}</g>'
            + word(BLUE, 370, 150, 118, 0, 4) + word(BLUE, 370, 250, 118, 4)
            + f'<g fill="{BLUE}">{straight("line", 372, 310, 30, 0)}</g>',
            "GoatConf: the one that feeds the community"),
    }


def cmd_build(args) -> int:
    want = files()
    want_favicon = want["coin.svg"]
    stale = 0
    for name, text in list(want.items()) + [("../favicon.svg", want_favicon)]:
        path = (OUT / name).resolve()
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                print(f"site/{path.relative_to(SITE)} is out of date: run python3 tools/brand.py build")
                stale += 1
        else:
            path.write_text(text, encoding="utf-8")
            print(f"wrote site/{path.relative_to(SITE)}")
    if args.check and not stale:
        print("brand files are current")
    return 1 if stale else 0


def kerning(font):
    """The kerning between two glyphs, as the font's pair-positioning lookups give it."""
    gpos = font["GPOS"].table
    wanted = {i for fr in gpos.FeatureList.FeatureRecord if fr.FeatureTag == "kern" for i in fr.Feature.LookupListIndex}
    subtables = []
    for i in sorted(wanted):
        lookup = gpos.LookupList.Lookup[i]
        for st in lookup.SubTable:
            st = st.ExtSubTable if lookup.LookupType == 9 else st
            if getattr(st, "LookupType", lookup.LookupType) == 2:
                subtables.append(st)

    def x_advance(value) -> int:
        return getattr(value, "XAdvance", 0) or 0 if value is not None else 0

    def pair(a: str, b: str) -> int:
        for st in subtables:
            if a not in st.Coverage.glyphs:
                continue
            if st.Format == 1:
                for rec in st.PairSet[st.Coverage.glyphs.index(a)].PairValueRecord:
                    if rec.SecondGlyph == b:
                        return x_advance(rec.Value1)
            else:
                c1 = st.ClassDef1.classDefs.get(a, 0)
                c2 = st.ClassDef2.classDefs.get(b, 0)
                return x_advance(st.Class1Record[c1].Class2Record[c2].Value1)
        return 0
    return pair


def cmd_lettering(_args) -> int:
    from fontTools.pens.svgPathPen import SVGPathPen  # only lettering needs fontTools
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer

    out = {"font": f"assets/fonts/{FONT.name}", "runs": {}}
    for name, (text, wght, wdth, opsz) in RUNS.items():
        font = instancer.instantiateVariableFont(TTFont(FONT), {"wght": wght, "wdth": wdth, "opsz": opsz})
        assert font["head"].unitsPerEm == 1000
        cmap, gs, hmtx, pair = font.getBestCmap(), font.getGlyphSet(), font["hmtx"], kerning(font)
        names = [cmap[ord(ch)] for ch in text]
        letters = []
        for i, (ch, g) in enumerate(zip(text, names)):
            pen = SVGPathPen(gs)
            gs[g].draw(pen)
            # whole font units: a thousandth of the letter's height, far below a pixel at any size the marks are used
            d = re.sub(r"-?\d+\.\d+", lambda m: str(round(float(m.group()))), pen.getCommands())
            letters.append({"char": ch, "adv": hmtx[g][0], "kern": pair(g, names[i + 1]) if i + 1 < len(names) else 0, "d": d})
        out["runs"][name] = {"text": text, "weight": wght, "width": wdth, "optical_size": opsz, "glyphs": letters}
    LETTERING.parent.mkdir(parents=True, exist_ok=True)
    LETTERING.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {LETTERING.relative_to(ROOT)}")
    return 0


def chrome() -> str:
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(name):
            return name
    sys.exit("render needs Chrome or Chromium on PATH")


def crop(src: Path, dst: Path, w: int, h: int) -> None:
    from PIL import Image  # only render needs Pillow
    with Image.open(src) as im:
        im.crop((0, 0, w, h)).save(dst, optimize=True)


def cmd_icons(_args) -> int:
    """The raster favicons: Google Search wants a square icon in a multiple of 48 pixels, and some crawlers ask for /favicon.ico."""
    from PIL import Image  # only the raster exports need Pillow
    exe = chrome()
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "icon.html"
        page.write_text(f'<html><body style="margin:0;background:transparent"><img src="{(OUT / "coin.svg").as_uri()}" '
                        'style="width:192px;height:192px;display:block"></body></html>', encoding="utf-8")
        shot = Path(tmp) / "icon.png"
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        "--window-size=192,392", f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True, timeout=120)
        with Image.open(shot) as im:
            icon = im.crop((0, 0, 192, 192)).convert("RGBA")
        icon.resize((96, 96), Image.LANCZOS).save(SITE / "favicon-96.png", optimize=True)
        print("rendered site/favicon-96.png")
        icon.save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        print("rendered site/favicon.ico")
    return 0


def cmd_render(_args) -> int:
    cmd_build(argparse.Namespace(check=False))
    cmd_icons(_args)
    exe = chrome()
    jobs = [  # (output, source svg, width, height)
        ("seal-1024.png", "seal.svg", 1024, 1024),
        ("seal-blue-1024.png", "seal-blue.svg", 1024, 1024),
        ("coin-400.png", "coin.svg", 400, 400),
        ("coin-yellow-400.png", "coin-yellow.svg", 400, 400),
        ("lockup-horizontal.png", "lockup-horizontal.svg", 2000, 600),
        ("lockup-stacked.png", "lockup-stacked.svg", 1800, 720),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        for out, src, w, h in jobs:
            page = Path(tmp) / f"{out}.html"
            page.write_text(f'<html><body style="margin:0;background:transparent"><img src="{(OUT / src).as_uri()}" '
                            f'style="width:{w}px;height:{h}px;display:block"></body></html>', encoding="utf-8")
            shot = Path(tmp) / out
            # headless Chrome's viewport is shorter than the window: render taller, then crop exactly
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                            f"--window-size={w},{h + 200}", f"--screenshot={shot}", page.as_uri()],
                           check=True, capture_output=True, timeout=120)
            crop(shot, OUT / out, w, h)
            print(f"rendered site/brand/{out}")
        # the home-screen icon: iOS fills transparent corners with black, so it sits on a blue square
        page = Path(tmp) / "touch.html"
        page.write_text(f'<html><body style="margin:0;background:{BLUE}"><img src="{(OUT / "coin.svg").as_uri()}" '
                        'style="width:164px;height:164px;margin:8px;display:block"></body></html>', encoding="utf-8")
        shot = Path(tmp) / "touch.png"
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=180,380",
                        f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True, timeout=120)
        crop(shot, SITE / "apple-touch-icon.png", 180, 180)
        print("rendered site/apple-touch-icon.png")
        page = Path(tmp) / "seal-print.html"
        page.write_text('<html><head><style>@page{size:300mm 300mm;margin:0}body{margin:0}</style></head><body>'
                        f'<img src="{(OUT / "seal.svg").as_uri()}" style="width:300mm;height:300mm;display:block"></body></html>',
                        encoding="utf-8")
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT / 'seal-print.pdf'}", page.as_uri()],
                       check=True, capture_output=True, timeout=120)
        print("rendered site/brand/seal-print.pdf")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    sub.add_parser("lettering")
    sub.add_parser("render")
    sub.add_parser("icons")
    args = ap.parse_args(argv)
    return {"build": cmd_build, "lettering": cmd_lettering, "render": cmd_render, "icons": cmd_icons}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
