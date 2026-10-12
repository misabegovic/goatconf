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

Seal and lockups carry their lettering in the site's display face, embedded,
so they render the same anywhere a browser renders them.

  build [--check]   write the SVG files (and site/favicon.svg); with --check,
                    fail if a committed file is not current
  render            also export PNG and PDF files through headless Chrome
                    (not checked by CI: Chrome's raster output is not byte-stable)

Usage: python3 tools/brand.py <build|render> [--check]
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = SITE / "brand"
FONT = SITE / "fonts" / "bricolage-wdth-latin.woff2"

BLUE, YELLOW, NIGHT, WHITE, INK = "#0b3d91", "#ffd400", "#051d47", "#ffffff", "#12204a"
TOP_LINE = "THE ONE THAT FEEDS THE COMMUNITY"
BOTTOM_LINE = "GOATCONF · 2027"
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


def font_face() -> str:
    data = base64.b64encode(FONT.read_bytes()).decode("ascii")
    return ('<style>@font-face{font-family:"GoatConf Display";font-weight:200 800;font-stretch:75% 100%;'
            f'src:url(data:font/woff2;base64,{data}) format("woff2")}}</style>')


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
        '<path id="arc-top" fill="none" d="M 40.4 173.3 A 112 112 0 1 1 259.6 173.3"/>'
        '<path id="arc-bot" fill="none" d="M 47.7 195.6 A 112 112 0 0 0 252.3 195.6"/>'
        f'<g fill="{fg}" font-family="GoatConf Display, Bricolage Grotesque, sans-serif" font-weight="800" font-stretch="75%">'
        f'<text font-size="24.5" letter-spacing="1.1" text-anchor="middle"><textPath href="#arc-top" startOffset="50%">{TOP_LINE}</textPath></text>'
        f'<text font-size="18" letter-spacing="1.3" text-anchor="middle" dominant-baseline="hanging"><textPath href="#arc-bot" startOffset="50%">{BOTTOM_LINE}</textPath></text>'
        '<path d="M33 190 l5 -5 l5 5 l-5 5 Z"/><path d="M257 190 l5 -5 l5 5 l-5 5 Z"/></g>'
        + hoof_band(fg)
        + goat_in(fg, 86, 86, 130, 66, cid)
    )


def coin_body(fg: str, bg: str, cid: str = "coin") -> str:
    return (f'<circle cx="150" cy="150" r="146" fill="{bg}"/>'
            f'<circle cx="150" cy="150" r="128" fill="none" stroke="{fg}" stroke-width="12"/>'
            + goat_in(fg, 52, 40, 212, 122, cid))


def svg(view: str, body: str, title: str, font=False) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{font_face() if font else ""}{body}</svg>\n')


WORD = ('<text font-family="GoatConf Display, Bricolage Grotesque, sans-serif" font-weight="800" '
        'font-stretch="75%" letter-spacing="0.5" fill="{fill}" x="{x}" y="{y}" font-size="{size}">GOATCONF</text>')


def files() -> dict[str, str]:
    goat = goat_path()
    return {
        "goat.svg": svg("0 0 394 449", f'<path fill="{BLUE}" fill-rule="evenodd" d="{goat}"/>', "The GoatConf goat"),
        "coin.svg": svg("0 0 300 300", coin_body(YELLOW, BLUE), "GoatConf"),
        "coin-yellow.svg": svg("0 0 300 300", coin_body(BLUE, YELLOW), "GoatConf"),
        "seal.svg": svg("0 0 300 300", seal_body(BLUE, YELLOW), "GoatConf: the one that feeds the community", font=True),
        "seal-blue.svg": svg("0 0 300 300", seal_body(YELLOW, BLUE), "GoatConf: the one that feeds the community", font=True),
        "seal-black.svg": svg("0 0 300 300", seal_body("#111111", WHITE), "GoatConf: the one that feeds the community", font=True),
        "lockup-horizontal.svg": svg("0 0 1000 300",
            f'<g>{coin_body(YELLOW, BLUE)}</g>' + WORD.format(fill=BLUE, x=330, y=212, size=170),
            "GoatConf", font=True),
        "lockup-stacked.svg": svg("0 0 900 360",
            f'<g transform="translate(20 20) scale(1.066)">{seal_body(BLUE, YELLOW)}</g>'
            + WORD.format(fill=BLUE, x=370, y=150, size=118).replace(">GOATCONF<", ">GOAT<")
            + WORD.format(fill=BLUE, x=370, y=250, size=118).replace(">GOATCONF<", ">CONF<")
            + f'<text font-family="GoatConf Display, Bricolage Grotesque, sans-serif" font-weight="700" font-stretch="85%" fill="{BLUE}" x="372" y="310" font-size="30">The one that feeds the community.</text>',
            "GoatConf: the one that feeds the community", font=True),
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


def chrome() -> str:
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(name):
            return name
    sys.exit("render needs Chrome or Chromium on PATH")


def crop(src: Path, dst: Path, w: int, h: int) -> None:
    from PIL import Image  # only render needs Pillow
    with Image.open(src) as im:
        im.crop((0, 0, w, h)).save(dst, optimize=True)


def cmd_render(_args) -> int:
    cmd_build(argparse.Namespace(check=False))
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
    sub.add_parser("render")
    args = ap.parse_args(argv)
    return cmd_build(args) if args.cmd == "build" else cmd_render(args)


if __name__ == "__main__":
    sys.exit(main())
