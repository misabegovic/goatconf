#!/usr/bin/env python3
"""The home page's generated parts, and the album's sticker numbers.

The home page is hand-written, with three parts filled from the records:

  <!-- home:days -->        the three days, from DAY_PLAN in tools/program.py
  <!-- home:speakers -->    the first speakers, from speakers/
  <!-- home:supporters -->  the supporters' logos, from supporters/

Then every sticker and slot number on the page is renumbered in order, so
the album keeps one sequence however the sections move.

  build [--check]   write site/index.html; with --check, fail if it is not current

Usage: python3 tools/home.py build [--check]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import program  # noqa: E402
import speakers  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "site" / "index.html"
SHOWN = 6
esc = program.esc
TILTS = (-1.5, 1, -1, 1.5, -0.5, 0.5)


def block(name: str, html: str) -> tuple[re.Pattern, str]:
    start, end = f"<!-- home:{name} -->", f"<!-- /home:{name} -->"
    return re.compile(re.escape(start) + r".*?" + re.escape(end), re.S), f"{start}\n{html}\n{end}"


def days() -> str:
    items = []
    for i, (day, plan) in enumerate(program.DAY_PLAN.items()):
        items.append(f'    <li class="sticker sticker--fact sticker--day" data-peel style="--tilt:{TILTS[i]}deg"><span class="num">0</span>'
                     f'<strong>{program.CORE_DAYS[day]}</strong><span class="day__hours">{plan["slots"][0]} to {plan["end"]}</span>'
                     f'<small>{plan["note"]}</small></li>')
    sat, label = program.COMMUNITY_DAY
    items.append(f'    <li class="sticker sticker--fact sticker--day" data-peel style="--tilt:1deg"><span class="num">0</span>'
                 f'<strong>{label}</strong><span class="day__hours">The community\'s day</span>'
                 f'<small>A day at the lakes and the goat hunt, planned by the organiser, plus walks and meetups people add.</small></li>')
    return f"""<section class="album-page wrap" id="days" aria-labelledby="days-title">
  <h2 class="band" id="days-title">Three days in June</h2>
  <ul class="slots slots--days">
{chr(10).join(items)}
  </ul>
  <p class="copy"><a class="go go--ink" href="program.html">See the program, room by room</a></p>
</section>"""


def speaker_sticker(i: int, slug: str, meta) -> str:
    photo = (f'<img src="{esc(meta["photo"])}" alt="" loading="lazy">' if meta.get("photo")
             else '<span class="speaker__goat" aria-hidden="true"><svg viewBox="0 0 124 100"><use href="#goat"/></svg></span>')
    return (f'    <li><a class="sticker sticker--photo sticker--mini" href="speaker-{esc(slug)}.html" data-peel style="--tilt:{TILTS[i % 6]}deg">'
            f'<span class="num">0</span>{photo}<span class="sticker__name">{esc(meta["name"])}</span></a></li>')


def speakers_block() -> str:
    people = sorted(speakers.speakers().items(), key=lambda kv: str(kv[1][0]["name"]).lower())
    if people:
        cards = "\n".join(speaker_sticker(i, s, m) for i, (s, (m, _)) in enumerate(people[:SHOWN]))
        more = f'<a class="go go--ink" href="speakers.html">All {len(people)} speakers</a>' if len(people) > SHOWN else '<a class="go go--ink" href="speakers.html">Meet the speakers</a>'
        intro = "The people giving the talks, panels and workshops so far. More are added as proposals are accepted."
    else:
        cards = ('    <li class="slots__wide"><a class="slot slot--link slot--wait" href="talk.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                 '<span class="num num--printed">0</span><strong>The first speaker could be you</strong>'
                 '<small>No one is announced yet. Speakers appear here as their sessions are accepted, and the call for proposals is open now.</small>'
                 '<span class="stamp">Yours?</span></a></li>')
        more = '<a class="go go--ink" href="talk.html">Propose a session</a>'
        intro = ""
    intro_html = f'\n  <p class="copy copy--wide">{intro}</p>' if intro else ""
    return f"""<section class="album-page wrap" id="speakers" aria-labelledby="speakers-title">
  <h2 class="band" id="speakers-title">Who is speaking</h2>{intro_html}
  <ul class="slots slots--mini">
{cards}
  </ul>
  <p class="copy">{more}</p>
</section>"""


def supporters_block() -> str:
    known = sorted(speakers.supporters().items(), key=lambda kv: str(kv[1][0]["name"]).lower())
    if known:
        logos = "\n".join(
            f'    <li><a class="supporter-chip" href="supporters.html#{esc(s)}"><img src="{esc(m["logo"])}" alt="{esc(m["name"])}" loading="lazy">'
            f'<small>{esc(m["funds"])}</small></a></li>' for s, (m, _) in known)
    else:
        logos = ('    <li><a class="slot slot--link" href="supporters.html#h-become"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                 '<span class="num num--printed">0</span><strong>Your logo</strong><small>Support GoatConf online for 500 euro, and your logo and link go here.</small><span class="stamp">Yours?</span></a></li>')
    return f"""<h3 class="list-title">Who makes it possible</h3>
    <ul class="slots slots--supporters-home">
{logos}
    </ul>
    <p class="copy"><a class="go go--ink" href="supporters.html">The supporters</a></p>"""


def renumber(text: str) -> str:
    n = 0

    def nxt(m):
        nonlocal n
        n += 1
        return f'{m.group(1)}{n}</span>'
    return re.sub(r'(<span class="num(?: num--printed)?">)\d+</span>', nxt, text)


def page() -> str:
    text = PAGE.read_text(encoding="utf-8")
    for name, html in (("days", days()), ("speakers", speakers_block()), ("supporters", supporters_block())):
        pattern, filled = block(name, html)
        if not pattern.search(text):
            raise SystemExit(f"site/index.html has no <!-- home:{name} --> block")
        text = pattern.sub(lambda _m: filled, text, count=1)
    return renumber(text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    want = page()
    have = PAGE.read_text(encoding="utf-8")
    if args.check:
        if want != have:
            print("site/index.html is out of date: run python3 tools/home.py build")
            return 1
        print("site/index.html is current")
        return 0
    PAGE.write_text(want, encoding="utf-8")
    print("wrote site/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
