#!/usr/bin/env python3
"""The home page's generated parts, and the album's sticker numbers.

The home page is hand-written, with four parts filled from the records:

  <!-- home:days -->        the three days, from DAY_PLAN in tools/program.py
  <!-- home:speakers -->    the first speakers, from speakers/, in eight places
  <!-- home:supporters -->  the supporters' logos, from supporters/
  <!-- home:kinds -->       every accepted event, from extensions/, then the
                            kinds of event to propose, all still open

Then every sticker and slot number on the page is renumbered in order, so
the album keeps one sequence however the sections move.

  build [--check]   write site/index.html; with --check, fail if it is not current

Usage: python3 tools/home.py build [--check]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extensions  # noqa: E402
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


# Events people add may run on any day of the GoatConf week; the ones the
# organiser accepts show under their day, the rest of the week under the slot
# that invites more.
WEEK = (dt.date(2027, 6, 2), dt.date(2027, 6, 6))
EVENING = "Evening: open for whatever people add."


def hours_off(plan) -> str:
    kinds = []
    for what in plan["breaks"].values():
        what = what.removeprefix("Hour off, in ").split(",")[0]
        what = what[0].lower() + what[1:]
        if what not in kinds:
            kinds.append(what)
    return "Hours off: " + " and ".join(kinds) + "."


def added(events) -> str:
    return "".join(f'<small class="day__added">Added: {esc(m["name"])}'
                   + (f', {start.strftime("%H:%M")}' if start.time() != dt.time() else "") + "</small>"
                   for start, _, m, _ in sorted(events, key=lambda e: e[0]))


def day_sticker(i: int, day, label: str, hours: str, lines: str) -> str:
    return (f'    <li><a class="sticker sticker--fact sticker--day" href="program.html#{day.isoformat()}" data-peel style="--tilt:{TILTS[i]}deg">'
            f'<span class="num">0</span><strong>{label}</strong><span class="day__hours">{hours}</span>{lines}</a></li>')


def days() -> str:
    ext = program.extension_days()
    items = []
    for i, (day, plan) in enumerate(program.DAY_PLAN.items()):
        lines = (f'<small>{plan["note"]}</small><small class="day__off">{hours_off(plan)}</small>'
                 f'<small class="day__evening">{EVENING}</small>{added(ext.get(day, []))}')
        items.append(day_sticker(i, day, program.CORE_DAYS[day], f'{plan["slots"][0]} to {plan["end"]}', lines))
    sat, label = program.COMMUNITY_DAY
    items.append(day_sticker(len(items), sat, label, "The community\'s day",
                             '<small>A day at the lakes and the goat hunt, planned by us, plus what people add.</small>'
                             + added(ext.get(sat, []))))
    outside = [e for d, evs in ext.items() if d not in program.DAY_PLAN and d != sat and WEEK[0] <= d <= WEEK[1] for e in evs]
    items.append('    <li class="slots__wide"><a class="slot slot--link slot--open" href="add.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                 '<span class="num num--printed">0</span><strong>Your event, any day from 2 to 6 June</strong>'
                 '<small>Anything you would like to run for the people who come. You run it, and once we accept it, it is on the program.</small>'
                 + added(outside) + '<span class="stamp">Yours?</span></a></li>')
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
            '<span class="num num--printed">0</span><strong>Your session here?</strong><small>A talk, a panel, a workshop or something else. The call is open.</small>'
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
    chips = [f'    <li><a class="supporter-chip{' supporter-chip--dark' if m.get('logo_on') == 'dark' else ''}" href="{speakers.supporter_page_name(s)}"><img src="{esc(m["logo"])}" alt="{esc(m["name"])}" loading="lazy">'
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


# The kinds of event the home page invites, in the form's order. They stay open
# however many are accepted: more than one of each is welcome.
HOME_KINDS = ("evening-event", "trip", "meetup", "podcast", "hike", "hackathon", "karaoke", "other")


def kinds_block() -> str:
    """Every accepted event, any kind, then the kinds to propose, all still open."""
    good = extensions.accepted()
    accepted = ""
    if good:
        cards = "\n".join("    " + extensions.card(i + 1, slug, m) for i, (_, slug, m, _b) in enumerate(good))
        accepted = f'  <h3 class="list-title">Accepted so far</h3>\n  <ul class="slots slots--events">\n{cards}\n  </ul>\n'
    kinds = []
    for kind in HOME_KINDS:
        label = "Something else?" if kind == "other" else extensions.KINDS[kind]
        kinds.append(f'    <li><a class="slot slot--kind slot--link" href="add.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                     f'<span class="num num--printed">0</span><strong>{label}</strong><span class="nameline" aria-hidden="true"></span><span class="stamp">Yours?</span></a></li>')
    return (accepted + f'  <p class="copy">{extensions.MORE}</p>\n'
            '  <ul class="slots slots--kinds" aria-label="Kinds of events you can propose">\n' + "\n".join(kinds) + "\n  </ul>")


def renumber(text: str) -> str:
    n = 0

    def nxt(m):
        nonlocal n
        n += 1
        return f'{m.group(1)}{n}</span>'
    return re.sub(r'(<span class="num(?: num--printed)?">)\d+</span>', nxt, text)


def page() -> str:
    text = PAGE.read_text(encoding="utf-8")
    for name, html in (("days", days()), ("speakers", speakers_block()), ("supporters", supporters_block()), ("kinds", kinds_block())):
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
