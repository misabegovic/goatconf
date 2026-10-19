#!/usr/bin/env python3
"""Build or check the whole site, every generator in the order they depend on.

  build     check the records, then write every generated page and part:
            the program, the events people add, the speakers and supporters,
            the travel page's places, the home page, the files for agents,
            the photos' WebP copies (needs Pillow), the page frame, the top
            bar and the link previews
  check     the same, writing nothing: fail if a record is invalid, any page
            or part is not current, or a page's HTML is broken
            (tools/site_lint.py)

The share cards and the brand files are not part of it: they need Chrome
(tools/shareables.py, tools/brand.py).

Usage: python3 tools/site.py <build|check>
(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

RECORDS = [["extensions.py", "check"], ["program.py", "check"], ["speakers.py", "check"]]
BUILD = [["program.py", "build"], ["extensions.py", "build"], ["speakers.py", "build"], ["places.py", "build"],
         ["home.py", "build"], ["agents.py", "build"], ["images.py", "build"], ["frame.py", "apply"],
         ["nav.py", "apply"], ["meta.py", "apply"]]
CHECK = [["program.py", "build", "--check"], ["extensions.py", "build", "--check"], ["speakers.py", "build", "--check"],
         ["places.py", "build", "--check"], ["home.py", "build", "--check"], ["agents.py", "build", "--check"],
         ["images.py", "check"], ["frame.py", "check"], ["nav.py", "check"], ["meta.py", "check"],
         ["site_lint.py", "check"]]


def run(steps) -> int:
    failed = []
    for step in steps:
        print(f"site ▶ {' '.join(step)}", flush=True)
        if subprocess.run([sys.executable, str(TOOLS / step[0]), *step[1:]], cwd=TOOLS.parent).returncode:
            failed.append(" ".join(step))
    for f in failed:
        print(f"site ✗ {f}")
    return 1 if failed else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "check"])
    args = ap.parse_args(argv)
    if run(RECORDS):
        return 1
    return run(BUILD) or run(CHECK) if args.cmd == "build" else run(CHECK)


if __name__ == "__main__":
    sys.exit(main())
