#!/usr/bin/env python3
"""Smaller photos for the site: WebP copies at a few widths, picked by the browser.

Every JPG a page shows from site/img/ gets WebP copies beside it, at 480, 800
and 1200 pixels wide (never wider than the original): img/city-kapija.jpg
gets img/city-kapija-480.webp and so on. Each <img> of such a JPG is wrapped
in a <picture> whose WebP <source> lists the copies, so a browser downloads
the one that fits; the JPG stays as the fallback. `picture { display:
contents }` in the stylesheet keeps the layout as if the <img> stood alone.

The generators call wrap() on the pages they write, and `apply` wraps the
hand-written ones, so every page is wrapped the same way.

  build     write the missing WebP copies (needs Pillow), then apply
  apply     wrap every <img> of a JPG that has copies, on every page
  check     fail if a shown JPG has no copies or a page is not wrapped

Usage: python3 tools/images.py <build|apply|check>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
WIDTHS = (480, 800, 1200)
QUALITY = 75
# How wide the photo shows: a page's header photo, or a sticker.
SIZES = {"page-head__photo": "(max-width: 47.99rem) 92vw, 34rem"}
DEFAULT_SIZES = "(max-width: 47.99rem) 92vw, 22rem"

IMG = re.compile(r'<img\b[^>]*\bsrc="(img/[^"]+\.jpg)"[^>]*>')
WRAPPED = re.compile(r'<picture><source type="image/webp"[^>]*>(<img\b[^>]*>)</picture>')


def copies(src: str) -> list[tuple[int, str]]:
    """The WebP copies a JPG has on disk, as (width, path), narrowest first."""
    jpg = SITE / src
    found = []
    for p in jpg.parent.glob(f"{jpg.stem}-*.webp"):
        width = p.stem.rsplit("-", 1)[1]
        if width.isdigit():
            found.append((int(width), str(p.relative_to(SITE))))
    return sorted(found)


def picture(img: str, src: str) -> str:
    have = copies(src)
    if not have:
        return img
    sizes = next((s for cls, s in SIZES.items() if cls in img), DEFAULT_SIZES)
    srcset = ", ".join(f"{path} {w}w" for w, path in have)
    return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{img}</picture>'


def wrap(text: str) -> str:
    """Every <img> of a JPG with copies, in a <picture>; already wrapped ones are rebuilt, so the list stays current."""
    text = WRAPPED.sub(lambda m: m.group(1), text)
    return IMG.sub(lambda m: picture(m.group(0), m.group(1)), text)


def pages() -> list[Path]:
    return sorted(SITE.glob("*.html"))


def shown() -> set[str]:
    """Every JPG under img/ that a page shows."""
    return {m.group(1) for p in pages() for m in IMG.finditer(p.read_text(encoding="utf-8"))}


def cmd_build() -> int:
    from PIL import Image  # only build needs Pillow

    for src in sorted(shown()):
        jpg = SITE / src
        with Image.open(jpg) as im:
            im = im.convert("RGB")
            for width in sorted({min(w, im.width) for w in WIDTHS}):
                out = jpg.with_name(f"{jpg.stem}-{width}.webp")
                if out.exists() and out.stat().st_mtime >= jpg.stat().st_mtime:
                    continue
                height = round(im.height * width / im.width)
                im.resize((width, height), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
                print(f"wrote site/{out.relative_to(SITE)}")
    return cmd_apply()


def cmd_apply() -> int:
    for p in pages():
        old = p.read_text(encoding="utf-8")
        new = wrap(old)
        if new != old:
            p.write_text(new, encoding="utf-8")
            print(f"wrapped the photos on site/{p.name}")
    return 0


def cmd_check() -> int:
    bad = 0
    for src in sorted(shown()):
        if not copies(src):
            print(f"site/{src} has no WebP copies: run python3 tools/images.py build")
            bad += 1
    for p in pages():
        text = p.read_text(encoding="utf-8")
        if wrap(text) != text:
            print(f"site/{p.name} has photos not wrapped for WebP: run python3 tools/images.py apply")
            bad += 1
    if not bad:
        print("every photo has its WebP copies, and every page uses them")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "apply", "check"])
    args = ap.parse_args(argv)
    return {"build": cmd_build, "apply": cmd_apply, "check": cmd_check}[args.cmd]()


if __name__ == "__main__":
    sys.exit(main())
