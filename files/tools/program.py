#!/usr/bin/env python3
"""The program: check the session records, and build the site's program page.

A session is one Markdown file with YAML frontmatter under program/. The two
core days, Thursday 3 and Friday 4 June 2027, run on one shared
timetable in every room at IPI Academy at once: four one-hour slots, each of
the first three followed by an hour off. Thursday runs 10:00 to 17:00; Friday
runs 09:30 to 16:30 (the reason is in the comment on DAY_PLAN). DAY_PLAN
holds each day's times. Saturday 5 June is
for the community. Events added around the talks come from extensions/.

  check [files...]   check every record (or the named ones). Exit 1 if any fails.
  build [--check]    write site/program.html; with --check, fail if the
                     committed page is not current.

Usage: python3 tools/program.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extensions  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "program"
SPEAKER_RECORDS = ROOT / "speakers"
PAGE = ROOT / "site" / "program.html"

CORE_DAYS = {dt.date(2027, 6, 3): "Thursday 3 June", dt.date(2027, 6, 4): "Friday 4 June"}
COMMUNITY_DAY = (dt.date(2027, 6, 5), "Saturday 5 June")
# Each core day's plan: when people are welcomed, the one-hour slots, what
# follows each slot, and when the day ends. Change a day here; the program
# page, the checks and the slot grid follow.
DAY_PLAN = {
    dt.date(2027, 6, 3): {
        "welcome": "09:45", "end": "17:00",
        "note": "Four one-hour slots in every room, an hour off after each. Welcome at 09:45.",
        "slots": ("10:00", "12:00", "14:00", "16:00"),
        "breaks": {"10:00": "Coffee on Freedom Square, one hour", "12:00": "Lunch in town, one hour",
                   "14:00": "Coffee on Freedom Square, one hour"},
    },
    # Friday starts half an hour earlier so the midday hour off covers Džuma
    # (podne in Tuzla is at 12:44 on 4 June 2027, per the Vaktija).
    dt.date(2027, 6, 4): {
        "welcome": "09:15", "end": "16:30",
        "note": "Four slots, starting half an hour earlier than Thursday. Welcome at 09:15.",
        "slots": ("09:30", "11:30", "13:30", "15:30"),
        "breaks": {"09:30": "Coffee on Freedom Square, one hour",
                   "11:30": "Lunch in town, one hour",
                   "13:30": "Coffee on Freedom Square, one hour"},
    },
}
ROOMS = {
    "hall-ground": ("Main hall", "ground floor, about 120 seats"),
    "hall-first": ("First-floor hall", "100 seats"),
    "hall-second": ("Second-floor room", "34 seats"),
    "lab-1": ("Computer centre 1", "20 seats"),
    "lab-2": ("Computer centre 2", "26 seats"),
    "top-floor": ("Top-floor room", "24 seats"),
    "club": ("The old student club", "13 seats"),
}
FORMATS = {"talk": "Talk", "panel": "Panel", "workshop": "Workshop", "other": "Session"}
FIELDS = ("title", "speakers", "format", "day", "start", "room", "accepted")


def records(paths=None):
    if paths:
        return [Path(p) for p in paths]
    if not RECORDS.is_dir():
        return []
    return sorted(p for p in RECORDS.glob("*.md") if p.name != "README.md" and not p.name.startswith("_"))


def check_record(path: Path):
    meta, body, problems = extensions.parse(path)
    if meta is None:
        return problems, None, body
    for f in FIELDS:
        if f not in meta or meta[f] in (None, ""):
            problems.append(f"missing field: {f}")
    if meta.get("format") and meta["format"] not in FORMATS:
        problems.append(f"format '{meta['format']}' is not one of: {', '.join(FORMATS)}")
    day = meta.get("day")
    if isinstance(day, str):
        try:
            day = dt.date.fromisoformat(day)
        except ValueError:
            day = None
    if meta.get("day") and day not in CORE_DAYS:
        problems.append("day must be 2027-06-03 or 2027-06-04, the two core days")
    meta["day"] = day
    if meta.get("start") and day in DAY_PLAN and str(meta["start"]) not in DAY_PLAN[day]["slots"]:
        problems.append(f"start on {CORE_DAYS[day]} must be one of {', '.join(DAY_PLAN[day]['slots'])}")
    if meta.get("room") and meta["room"] not in ROOMS:
        problems.append(f"room must be one of: {', '.join(ROOMS)}")
    if meta.get("accepted") is not True:
        problems.append("accepted must be yes")
    if meta.get("signup") and not str(meta["signup"]).startswith("https://"):
        problems.append("signup must be the session's sign-up link in the GoatConf app, starting https://")
    if not body:
        problems.append("no description below the frontmatter")
    return problems, meta, body


def sessions():
    taken, out, clashes = {}, [], []
    for path in records():
        problems, meta, body = check_record(path)
        if problems:
            continue
        key = (meta["day"], str(meta["start"]), meta["room"])
        if key in taken:
            clashes.append(f"{path.name} and {taken[key]} share {meta['day']} {meta['start']} {meta['room']}")
            continue
        taken[key] = path.name
        out.append((key, meta, body))
    return dict((k, (m, b)) for k, m, b in out), clashes


def cmd_check(args) -> int:
    paths = records(args.files)
    failed = 0
    for path in paths:
        problems, meta, _ = check_record(path)
        print(f"{path.name}: {(meta or {}).get('title') or path.stem}")
        for p in problems:
            print(f"  needs a change: {p}")
        failed += bool(problems)
    _, clashes = sessions()
    for c in clashes:
        print(f"clash: {c}")
    print(f"program: {len(paths)} record(s), {failed} need a change, {len(clashes)} clash(es)")
    return 1 if failed or clashes else 0


def esc(v) -> str:
    return html.escape(str(v))


def speaker_names() -> dict:
    """Published speaker profiles by slug; tools/speakers.py checks them in full."""
    out = {}
    for path in sorted(SPEAKER_RECORDS.glob("*.md")) if SPEAKER_RECORDS.is_dir() else []:
        if path.name == "README.md" or path.name.startswith("_"):
            continue
        meta, _, problems = extensions.parse(path)
        if meta and not problems and meta.get("publish") is True and meta.get("name"):
            out[path.stem] = str(meta["name"])
    return out


def who(meta) -> str:
    names = speaker_names()
    linked = [f'<a href="speaker-{esc(s)}.html">{esc(names[s])}</a>' for s in meta.get("profiles") or [] if s in names]
    return ", ".join(linked) if linked else esc(meta["speakers"])


def register(meta) -> str:
    """The session's own sign-up in the GoatConf app, once it exists."""
    if not meta.get("signup"):
        return ""
    return f'<a class="session__register" href="{esc(meta["signup"])}">Save a seat</a>'


def cell(n: int, found, room: str) -> str:
    where = f'<span class="room-name">{ROOMS[room][0]}</span>'
    if found:
        meta, body = found
        first = body.split("\n\n")[0].strip()
        return f"""<li class="sticker sticker--session" data-peel style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg"><span class="num">{n}</span><span class="session__format">{FORMATS[meta['format']]}, {ROOMS[room][0]}</span><strong>{esc(meta['title'])}</strong><small>{who(meta)}</small><p>{esc(first)}</p>{register(meta)}</li>"""
    return f"""<li class="slot slot--session"><span class="num num--printed">{n}</span>{where}<strong>Open</strong><small>Waiting for a talk, a panel or a workshop.</small><span class="stamp">Yours?</span></li>"""


def day_block(day, label, table, start_n) -> tuple[str, int]:
    n = start_n
    rows = []
    plan = DAY_PLAN[day]
    for t in plan["slots"]:
        cells = []
        for room in ROOMS:
            cells.append(cell(n, table.get((day, t, room)), room))
            n += 1
        filled = sum(1 for room in ROOMS if (day, t, room) in table)
        open_rooms = len(ROOMS) - filled
        open_line = (f'\n    <p class="timeslot__open">{open_rooms} of {len(ROOMS)} rooms still open. <a href="talk.html">Propose a session</a></p>'
                     if open_rooms else "")
        rows.append(f"""<li class="timeslot">
    <h3 class="timeslot__time">{t}<span>{filled} of {len(ROOMS)} rooms taken</span></h3>{open_line}
    <ul class="rooms">
      {chr(10).join('      ' + c if i else c for i, c in enumerate(cells))}
    </ul>
  </li>""")
        if t in plan["breaks"]:
            rows.append(f'<li class="breakrow"><span class="breakrow__time">{int(t[:2]) + 1:02d}{t[2:]}</span>{plan["breaks"][t]}</li>')
    rows.insert(0, f'<li class="breakrow breakrow--welcome"><span class="breakrow__time">{plan["welcome"]}</span>Welcome, in the main hall</li>')
    rows.append(f'<li class="breakrow"><span class="breakrow__time">{plan["end"]}</span>The day ends. The evening is yours, or one of the events people add.</li>')
    return f"""<section class="album-page wrap day" id="{day.isoformat()}" aria-labelledby="h-{day.isoformat()}">
  <h2 class="band" id="h-{day.isoformat()}">{label}<span class="band__sub">Core day, {plan['slots'][0]} to {plan['end']}</span></h2>
  <ol class="timetable">
  {chr(10).join(rows)}
  </ol>
</section>""", n


def extension_days():
    by_day = {}
    for path in extensions.records():
        problems, _, meta = extensions.check_record(path)
        if problems or not extensions.listed(meta):
            continue
        _, body, _ = extensions.parse(path)
        start = extensions.as_datetime(meta["start"])
        by_day.setdefault(start.date(), []).append((start, meta, body))
    return by_day


def ext_item(meta) -> str:
    return f"""<li class="sticker sticker--fact sticker--ext" data-peel style="--tilt:-1deg"><strong>{esc(meta['name'])}</strong><small>{extensions.KINDS[meta['kind']]}, part of GoatConf 2027, run by {esc(meta['host'])}. {extensions.when(meta)}, {esc(meta['location'])}.</small></li>"""


def page() -> str:
    table, _ = sessions()
    ext = extension_days()
    n = 1
    days = []
    for day, label in CORE_DAYS.items():
        block, n = day_block(day, label, table, n)
        days.append(block)
    sat, sat_label = COMMUNITY_DAY
    sat_items = "\n".join(ext_item(m) for _, m, _ in sorted(ext.get(sat, []), key=lambda e: e[0]))
    sat_open = "\n".join(f'<li class="slot"><span class="num num--printed">{n + i}</span><strong>{name}</strong><small>{what}</small><span class="stamp">Yours?</span></li>'
                         for i, (name, what) in enumerate([("A day at the lakes", "Swimming, the salt waterfalls and the beach at the Pannonian Lakes."),
                                                           ("The goat hunt", "Clues through town for teams of people who just met, ending at the goat statue."),
                                                           ("A walk or a hike", "The old town, the salt story, the hills above Tuzla."),
                                                           ("Something else?", "A meetup, a dinner, a corner for your community.")]))
    around = []
    for day in sorted(d for d in ext if d not in CORE_DAYS and d != sat):
        around.extend(ext_item(m) for _, m, _ in sorted(ext[day], key=lambda e: e[0]))
    for day in CORE_DAYS:
        around.extend(ext_item(m) for _, m, _ in sorted(ext.get(day, []), key=lambda e: e[0]))
    around_html = ('<ul class="slots ext-list">\n' + "\n".join(around) + "\n</ul>") if around else '<p class="ledger-empty">No evening events or workshops yet. Want to run a workshop the evening before, or a dinner after the talks? <a href="add.html">Propose yours</a>.</p>'
    sprite = extensions.SHELL.read_text(encoding="utf-8")
    sprite = sprite[sprite.index('<svg width="0"'):sprite.index("</svg>", sprite.index('<svg width="0"')) + 6]
    room_list = "\n".join(f"    <li><strong>{name}</strong>, {seats}</li>" for name, seats in ROOMS.values())
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Program: GoatConf 2027, 3 to 5 June, Tuzla</title>
<meta name="description" content="The GoatConf 2027 program: two core days, Thursday 3 and Friday 4 June, in every room of IPI Academy, Tuzla, and Saturday 5 June for the community.">
<meta name="theme-color" content="#0b3d91">
<link rel="canonical" href="https://goatconf.com/program">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="goatconf.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver"in window)document.documentElement.classList.add("js-peel")</script>
</head>
<body>
<!-- Generated by files/tools/program.py build from files/program/*.md and files/extensions/*.md. Edit the records, not this page. -->
{sprite}
<header class="page-head">
  <img class="page-head__photo" src="img/ipi-lecture-hall.jpg" width="1024" height="768" alt="A talk in IPI Academy's lecture hall, students' faces blurred" decoding="async">
  <h1 class="sign">The program</h1>
  <p class="lede">Two days of talks in every room of IPI Academy, then a community day on Saturday. Every empty slot is waiting for someone.</p>
</header>
<main id="main">
<section class="album-page wrap" aria-labelledby="h-how">
  <h2 class="band" id="h-how">How a day runs</h2>
  <div class="page-grid">
    <div class="copy">
      <p>Thursday 3 and Friday 4 June 2027 are the core days, at IPI Academy, Kulina bana 2, Tuzla. Each day runs on one timetable for every room, so you can change rooms at every break.</p>
      <p>Every slot is one hour: a talk with time for questions, a panel, or a workshop. After each slot comes a full hour off, in the cafés on Freedom Square under five minutes away. That is when you talk to the person you just heard.</p>
      <p>Thursday runs from 10:00 to 17:00. Friday runs from 09:30 to 16:30.</p>
      <p>GoatConf does not record the talks. You may bring a camera or a podcast and record, and podcasts are welcome in some of the rooms.</p>
      <p>The slots fill as proposals come in and are accepted. <a href="talk.html">Propose a session</a>, or <a href="register.html">register for free</a> to come and listen.</p>
    </div>
    <div>
      <h3 class="list-title">The rooms</h3>
      <ul class="rooms-list">
{room_list}
      </ul>
      <p class="checked">Closer to June, you will also register for the sessions you want, because each room has only so many seats. Everyone with a ticket gets an email with how. Seats nobody registered for go to whoever is at the door when a session starts.</p>
      <p><a class="go go--ink" href="goatconf-2027.ics" download>Add the three days to your calendar</a></p>
    </div>
  </div>
</section>
<nav class="daynav wrap" aria-label="Days">
  {"".join(f'<a href="#{d.isoformat()}">{lbl}</a>' for d, lbl in [(d, CORE_DAYS[d]) for d in CORE_DAYS] + [(COMMUNITY_DAY[0], COMMUNITY_DAY[1])])}
</nav>
{chr(10).join(days)}
<section class="album-page wrap day" id="{sat.isoformat()}" aria-labelledby="h-sat">
  <h2 class="band" id="h-sat">{sat_label}<span class="band__sub">The community's day</span></h2>
  <p class="copy copy--wide">No talks on Saturday. The day is for events people add: the lakes, the goat hunt, walks and meetups. Each host runs their own event and says how to join.</p>
  <ul class="slots slots--kinds">
{sat_items}
{sat_open}
  </ul>
  <p class="copy"><a class="go go--ink" href="add.html">Propose something for Saturday</a></p>
</section>
<section class="album-page wrap" aria-labelledby="h-around">
  <h2 class="band" id="h-around">Around the talks</h2>
  {around_html}
</section>
</main>
<footer class="footer">
  <p>GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3 to 5 June 2027. Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.</p>
  <p class="footer__links"><a href="index.html">Home</a> <a href="program.html">Program</a> <a href="speakers.html">Speakers</a> <a href="talk.html">Give a talk</a> <a href="add.html">Propose an event</a> <a href="register.html">Register</a> <a href="travel.html">Travel</a> <a href="supporters.html">Supporters</a> <a href="charter.html">Charter</a> <a href="code-of-conduct.html">Code of conduct</a> <a href="brand.html">Brand</a> <a href="access.html">Accessibility</a> <a href="contact.html">Contact</a></p>
</footer>
<script src="album.js" defer></script>
</body>
</html>
"""


def cmd_build(args) -> int:
    want = nav.place(meta.tag(page()), "program.html")
    if args.check:
        have = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        if have != want:
            print("site/program.html is out of date: run python3 tools/program.py build")
            return 1
        print("site/program.html is current")
        return 0
    PAGE.write_text(want, encoding="utf-8")
    print(f"wrote {PAGE.relative_to(ROOT)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("files", nargs="*")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    return cmd_check(args) if args.cmd == "check" else cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
