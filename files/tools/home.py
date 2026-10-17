#!/usr/bin/env python3
"""The home page's generated parts, and the album's sticker numbers.

The home page is hand-written, with three parts filled from the records:

  <!-- home:days -->        the three days, from DAY_PLAN in tools/program.py
  <!-- home:speakers -->    the first speakers, from speakers/, in eight places
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
# The home page plans for eight speakers: two full rows of four on a wide screen,
# four rows of two on a phone. Places not yet taken invite a proposal.
SHOWN = 8
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


def speaker_sticker(i: int, slug: str, meta, sessions=()) -> str:
    role = f'<small class="sticker__role">{esc(meta["role"])}</small>' if meta.get("role") else ""
    # The session's title, as the speakers page shows it: the scheduled one
    # first, else the talk the record proposes while it has no slot.
    talk = (f'{sessions[0]["format"]}: {sessions[0]["title"]}' if sessions
            else f'Talk: {meta["talk"]}' if meta.get("talk") else "")
    role += f'<small class="sticker__talk">{esc(talk)}</small>' if talk else ""
    photo = (f'<img src="{esc(meta["photo"])}" alt="" loading="lazy">' if meta.get("photo")
             else '<span class="speaker__goat" aria-hidden="true"><svg viewBox="0 0 124 100"><use href="#goat"/></svg></span>')
    return (f'    <li><a class="sticker sticker--photo sticker--mini" href="speaker-{esc(slug)}.html" data-peel style="--tilt:{TILTS[i % 6]}deg">'
            f'<span class="num">0</span>{photo}<span class="sticker__name">{esc(meta["name"])}{role}</span></a></li>')


def open_place() -> str:
    return ('    <li><a class="slot slot--link slot--open" href="talk.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
            '<span class="num num--printed">0</span><strong>Your talk here?</strong><small>The call for proposals is open.</small>'
            '<span class="stamp">Yours?</span></a></li>')


def speakers_block() -> str:
    people = speakers.listed(speakers.speakers())
    if people:
        sessions = speakers.sessions_by_speaker(detail=True)
        cards = "\n".join([speaker_sticker(i, s, m, sessions.get(s, ())) for i, (s, (m, _)) in enumerate(people[:SHOWN])]
                          + [open_place() for _ in range(SHOWN - len(people[:SHOWN]))])
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
    known = speakers.listed_supporters(speakers.supporters())
    chips = [f'    <li><a class="supporter-chip{' supporter-chip--dark' if m.get('logo_on') == 'dark' else ''}" href="supporters.html#{esc(s)}"><img src="{esc(m["logo"])}" alt="{esc(m["name"])}" loading="lazy">'
             f'<small>{esc(m["funds"])}</small></a></li>' for s, (m, _) in known]
    # Until a company supports GoatConf (the host does not count), keep a place inviting one.
    if not any(m.get("host") is not True for _, (m, _b) in known):
        chips.append('    <li><a class="slot slot--link" href="supporters.html#h-become"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                     '<span class="num num--printed">0</span><strong>Your logo</strong><small>Support GoatConf online for 500 euro, and your logo and link go here.</small><span class="stamp">Yours?</span></a></li>')
    logos = "\n".join(chips)
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
