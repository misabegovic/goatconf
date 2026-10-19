#!/usr/bin/env python3
"""The display face, cut down to what the site uses.

Bricolage Grotesque comes as a variable font with weights 200 to 800 and
widths 75% to 100%. The site sets it only at weights 650 to 800 and widths
75% to 90% (measured across every page on 2026-10-19), so the published
files keep just that range of those two axes, and the optical size axis
whole. The full files stay in assets/fonts/, which is not published.

  build     write site/fonts/bricolage-*.woff2 from assets/fonts/ (needs
            fontTools and brotli)

When the stylesheet starts using a weight or width outside the range, widen
AXES, run build, and update the @font-face rules in goatconf.css to match.

Usage: python3 tools/fonts.py build
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "fonts"
OUT = ROOT / "site" / "fonts"
FILES = ("bricolage-wdth-latin.woff2", "bricolage-wdth-latin-ext.woff2")
AXES = {"wght": (650, 800), "wdth": (75, 90)}


def cmd_build(_args) -> int:
    from fontTools.ttLib import TTFont  # only build needs fontTools
    from fontTools.varLib import instancer

    for name in FILES:
        font = instancer.instantiateVariableFont(TTFont(SRC / name), AXES)
        font.flavor = "woff2"
        font.save(OUT / name)
        print(f"wrote site/fonts/{name}: {(SRC / name).stat().st_size // 1024} KB to {(OUT / name).stat().st_size // 1024} KB")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    args = ap.parse_args(argv)
    return cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
