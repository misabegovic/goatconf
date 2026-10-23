#!/usr/bin/env python3
"""The program: check the session records, and build the site's program page.

A session is one Markdown file with YAML frontmatter under program/. The two
core days, Thursday 3rd and Friday 4th June 2027, run on one shared
timetable in every room at IPI Academy at once: four one-hour slots, each of
the first three followed by an hour off. DAY_PLAN holds each day's times
(why Friday starts earlier is in the comment on it), and every page that
gives them takes them from there: the program page, the day list on the
register page and the slot times on the talk page, which this script writes
too. Saturday 5th June is for the community. Events added around the talks come from extensions/.

  check [files...]   check every record (or the named ones). Exit 1 if any fails.
  build [--check]    write site/program.html and a page for each session
                     (site/session-<title>.html); with --check, fail if a
                     committed page is not current.

Usage: python3 tools/program.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extensions  # noqa: E402
import images  # noqa: E402
import sitelib  # noqa: E402
import frame  # noqa: E402
import blocks  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "program"
SPEAKER_RECORDS = ROOT / "speakers"
PAGE = ROOT / "site" / "program.html"

CORE_DAYS = {dt.date(2027, 6, 3): "Thursday 3rd June", dt.date(2027, 6, 4): "Friday 4th June"}
COMMUNITY_DAY = (dt.date(2027, 6, 5), "Saturday 5th June")
# Each core day's plan: when people are welcomed, the one-hour slots, what
# follows each slot, and when the day ends. Change a day here; the program
# page, the checks and the slot grid follow.
DAY_PLAN = {
    dt.date(2027, 6, 3): {
        "welcome": "09:45", "end": "17:00",
        "note": "Four one-hour slots in every room, an hour off after each.",
        "slots": ("10:00", "12:00", "14:00", "16:00"),
        "breaks": {"10:00": "Hour off, in the cafés on Freedom Square", "12:00": "Lunch in town, one hour",
                   "14:00": "Hour off, in the cafés on Freedom Square"},
    },
    # Friday starts half an hour earlier so the midday hour off covers Džuma
    # (podne in Tuzla is at 12:44 on 4 June 2027, per the Vaktija).
    dt.date(2027, 6, 4): {
        "welcome": "09:15", "end": "16:30",
        "note": "Four slots, starting half an hour earlier than Thursday.",
        "slots": ("09:30", "11:30", "13:30", "15:30"),
        "breaks": {"09:30": "Hour off, in the cafés on Freedom Square",
                   "11:30": "Lunch in town, one hour",
                   "13:30": "Hour off, in the cafés on Freedom Square"},
    },
}
ROOMS = {
    "hall-ground": ("Main hall", "ground floor, 150 seats"),
    "hall-first": ("First-floor hall", "100 seats"),
    "hall-second": ("Second-floor room", "34 seats"),
    "lab-1": ("Computer centre 1", "20 seats"),
    "lab-2": ("Computer centre 2", "26 seats"),
    "top-floor": ("Top-floor room", "24 seats"),
    "club": ("The old student club", "13 seats"),
}
# Cells held for confirmed speakers whose session has no slot yet, in the
# order they are held: as many as there are such speakers (published, not
# held, named in no program record), skipping a cell a session already takes.
# The organiser chose the main hall, three a day, on 2026-10-18, and a
# seventh at Thursday 16:00 on 2026-10-20 (sources/conversations/2026-10-20--org--roy-tomeij.md),
# and an eighth at Friday 15:30 on 2026-10-23 (sources/conversations/2026-10-23--org--predrag-radenkovic.md).
RESERVED = (
    (dt.date(2027, 6, 3), "10:00", "hall-ground"), (dt.date(2027, 6, 3), "12:00", "hall-ground"),
    (dt.date(2027, 6, 3), "14:00", "hall-ground"), (dt.date(2027, 6, 4), "09:30", "hall-ground"),
    (dt.date(2027, 6, 4), "11:30", "hall-ground"), (dt.date(2027, 6, 4), "13:30", "hall-ground"),
    (dt.date(2027, 6, 3), "16:00", "hall-ground"), (dt.date(2027, 6, 4), "15:30", "hall-ground"),
)
FORMATS = {"talk": "Talk", "panel": "Panel", "workshop": "Workshop", "other": "Session"}
# The areas the talk page names, as the proposal form's area question
# offers them (sources/conversations/2026-10-19--org--more-areas.md). They are
# meant to group into a few tracks later, if more venues join.
AREAS = {"engineering": "Engineering", "ai-ml": "AI/ML", "data": "Data", "ux-ui": "UX/UI", "product": "Product",
         "research": "Research", "business": "Business of software", "leadership": "Leadership"}
FOR_CHARS = 100
FORMAT_NAME_CHARS = 30
FIELDS = ("title", "speakers", "format", "day", "start", "room", "accepted")


def records(paths=None):
    return sitelib.records(RECORDS, paths)


def areas(value) -> list:
    """A session's areas: one key or a list of them, as the form's area question lets a speaker pick any number."""
    return [] if value is None else value if isinstance(value, list) else [value]


def flavor_problems(meta, area="area", audience="for") -> list:
    """A session's areas and who it is for: both optional; each area one of AREAS, who it is for one short line in the speaker's words."""
    problems = []
    picked = areas(meta.get(area))
    if meta.get(area) is not None and (not picked or any(a not in AREAS for a in picked) or len(set(picked)) < len(picked)):
        problems.append(f"{area} must be one of, or a list of different ones of: {', '.join(AREAS)}")
    v = meta.get(audience)
    if v is not None and (not isinstance(v, str) or not v.strip() or "\n" in v.strip() or len(v) > FOR_CHARS):
        problems.append(f"{audience} must be one line of at most {FOR_CHARS} characters: who the session is for, in the speaker's words")
    return problems


def format_name_problems(meta, fmt="format", name="format_name") -> list:
    """Something else may say what it is, for example Live coding: one short line, only with the format other."""
    v = meta.get(name)
    if v is None:
        return []
    problems = [] if meta.get(fmt) == "other" else [f"{name} needs {fmt}: other"]
    if not isinstance(v, str) or not v.strip() or "\n" in v.strip() or len(v) > FORMAT_NAME_CHARS:
        problems.append(f"{name} must be one line of at most {FORMAT_NAME_CHARS} characters, for example Live coding")
    return problems


def format_label(meta, fmt="format", name="format_name") -> str:
    """The session's format as people read it: what something else is called, if the record says; a talk if left out."""
    if meta.get(fmt) == "other" and meta.get(name):
        return str(meta[name]).strip()
    return FORMATS[meta.get(fmt) or "talk"]


def tags(fmt, area) -> str:
    """The session's format and areas, as small tags; either may be left out."""
    inner = ((f'<span class="tag">{esc(fmt)}</span>' if fmt else "")
             + "".join(f'<span class="tag tag--area tag--{a}">{AREAS[a]}</span>' for a in areas(area) if a in AREAS))
    return f'<span class="tags">{inner}</span>' if inner else ""


def for_line(text, tag="p") -> str:
    """Who the session is for, in the speaker's words."""
    return f'<{tag} class="for-line"><b>For:</b> {esc(str(text).strip())}</{tag}>' if text else ""


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
    problems += flavor_problems(meta) + format_name_problems(meta)
    if meta.get("signup") and not str(meta["signup"]).startswith("https://"):
        problems.append("signup must be the session's own sign-up link, starting https://")
    if not body:
        problems.append("no description below the frontmatter")
    return problems, meta, body


def sessions():
    taken, pages, out, clashes = {}, {}, [], []
    for path in records():
        problems, meta, body = check_record(path)
        if problems:
            continue
        key = (meta["day"], str(meta["start"]), meta["room"])
        if key in taken:
            clashes.append(f"{path.name} and {taken[key]} share {meta['day']} {meta['start']} {meta['room']}")
            continue
        name = page_name(meta)
        if name in pages:
            clashes.append(f"{path.name} and {pages[name]} would share the page site/{name}: give one a different title")
            continue
        taken[key] = pages[name] = path.name
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
    table, clashes = sessions()
    for c in clashes:
        print(f"clash: {c}")
    waiting, free = len(waiting_speakers(table)), len([k for k in RESERVED if k not in table])
    if waiting > free:
        clashes.append(f"{waiting} confirmed speakers wait for a slot but RESERVED holds only {free} free cell(s): add one")
        print(f"clash: {clashes[-1]}")
    print(f"program: {len(paths)} record(s), {failed} need a change, {len(clashes)} clash(es)")
    return 1 if failed or clashes else 0


esc = sitelib.esc


def page_name(meta) -> str:
    """Each session's own page, named after its title: "Salt, goats and servers" is session-salt-goats-and-servers.html."""
    plain = unicodedata.normalize("NFKD", str(meta["title"])).encode("ascii", "ignore").decode()
    return "session-" + (re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-") or "untitled") + ".html"


def ends(start: str) -> str:
    h, m = map(int, str(start).split(":"))
    return f"{h + 1:02d}:{m:02d}"


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


def waiting_speakers(table) -> list:
    """Published speakers, not held, that no program record names yet."""
    named = {s for m, _ in table.values() for s in m.get("profiles") or []}
    out = []
    for path in sorted(SPEAKER_RECORDS.glob("*.md")) if SPEAKER_RECORDS.is_dir() else []:
        if path.name == "README.md" or path.name.startswith("_"):
            continue
        meta, _, problems = extensions.parse(path)
        if meta and not problems and meta.get("publish") is True and not meta.get("hold") and path.stem not in named:
            out.append(path.stem)
    return out


def reserved_cells(table) -> set:
    free = [key for key in RESERVED if key not in table]
    return set(free[:len(waiting_speakers(table))])


def who(meta) -> str:
    names = speaker_names()
    linked = [f'<a href="speaker-{esc(s)}.html">{esc(names[s])}</a>' for s in meta.get("profiles") or [] if s in names]
    return ", ".join(linked) if linked else esc(meta["speakers"])


def register(meta) -> str:
    """The session's own sign-up link, if session registration is introduced later."""
    if not meta.get("signup"):
        return ""
    return f'<a class="session__register" href="{esc(meta["signup"])}">Save a seat</a>'


def cell(n: int, found, room: str, reserved=False) -> str:
    where = f'<span class="room-name">{ROOMS[room][0]}</span>'
    if reserved and not found:
        return f"""<li class="slot slot--session slot--reserved"><span class="num num--printed">{n}</span>{where}<strong>Reserved</strong><small>For a <a href="speakers.html">confirmed speaker</a>, session to come.</small><span class="stamp stamp--planned">Reserved</span></li>"""
    if found:
        meta, body = found
        first = body.split("\n\n")[0].strip()
        return f"""<li class="sticker sticker--session" data-peel style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg"><span class="num">{n}</span><span class="session__format">{esc(format_label(meta))}, {ROOMS[room][0]}</span>{tags(None, meta.get('area'))}<strong><a class="sticker__open sticker__open--stretch" href="{page_name(meta)}">{esc(meta['title'])}</a></strong><small>{who(meta)}</small>{for_line(meta.get('for'))}<p>{esc(first)}</p>{register(meta)}</li>"""
    return f"""<li class="slot slot--session"><span class="num num--printed">{n}</span>{where}<strong>Open</strong><small>Waiting for a talk, a panel or a workshop.</small><span class="stamp">Yours?</span></li>"""


def day_block(day, label, table, start_n) -> tuple[str, int]:
    n = start_n
    rows = []
    plan = DAY_PLAN[day]
    held = reserved_cells(table)
    for t in plan["slots"]:
        cells = []
        for room in ROOMS:
            cells.append(cell(n, table.get((day, t, room)), room, (day, t, room) in held))
            n += 1
        filled = sum(1 for room in ROOMS if (day, t, room) in table or (day, t, room) in held)
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
    rows.append(f'<li class="breakrow"><span class="breakrow__time">{plan["end"]}</span>The day ends. Many people head to the salt lakes around 17:00 or 18:00; come along, or join one of the events people add.</li>')
    return f"""<section class="album-page wrap day" id="{day.isoformat()}" aria-labelledby="h-{day.isoformat()}">
  <h2 class="band" id="h-{day.isoformat()}">{label}<span class="band__sub">Core day, {plan['slots'][0]} to {plan['end']}</span></h2>
  <ol class="timetable">
  {chr(10).join(rows)}
  </ol>
</section>""", n


def extension_days():
    """The accepted events by day, each (start, slug, meta, body), in order."""
    by_day = {}
    for start, slug, meta, body in extensions.accepted():
        by_day.setdefault(start.date(), []).append((start, slug, meta, body))
    return by_day


def ext_item(slug, meta) -> str:
    return f"""<li class="sticker sticker--fact sticker--ext" data-peel style="--tilt:-1deg"><a class="sticker__open" href="{extensions.page_name(slug)}"><strong>{esc(meta['name'])}</strong><small>{extensions.KINDS[meta['kind']]}, part of GoatConf 2027, run by {esc(meta['host'])}. {extensions.when(meta)}, {esc(meta['location'])}.</small></a></li>"""


def page() -> str:
    table, _ = sessions()
    ext = extension_days()
    n = 1
    days = []
    for day, label in CORE_DAYS.items():
        block, n = day_block(day, label, table, n)
        days.append(block)
    sat, sat_label = COMMUNITY_DAY
    sat_items = "\n".join(ext_item(s, m) for _, s, m, _ in ext.get(sat, []))
    sat_open = "\n".join(f'<li class="slot"><span class="num num--printed">{n + i}</span><strong>{name}</strong><small>{what}</small><span class="stamp{" stamp--planned" if planned else ""}">{"Planned" if planned else "Yours?"}</span></li>'
                         for i, (name, what, planned) in enumerate([("A day at the lakes", "Swimming, the salt waterfalls and the beach at the Pannonian Lakes.", True),
                                                           ("The goat hunt", "Clues through town for teams of people who just met, ending at the goat statue.", True),
                                                           ("A walk or a hike", "The old town, the salt story, the hills above Tuzla.", False),
                                                           ("Something else?", "A meetup, a dinner, a corner for your community.", False)]))
    around = []
    for day in sorted(d for d in ext if d not in CORE_DAYS and d != sat):
        around.extend(ext_item(s, m) for _, s, m, _ in ext[day])
    for day in CORE_DAYS:
        around.extend(ext_item(s, m) for _, s, m, _ in ext.get(day, []))
    around_html = ('<section class="album-page wrap" aria-labelledby="h-around">\n'
                   '  <h2 class="band" id="h-around">Around the talks</h2>\n'
                   '  <ul class="slots ext-list">\n' + "\n".join(around) + "\n</ul>\n</section>") if around else ""
    room_list = "\n".join(f"    <li><strong>{name}</strong>, {seats}</li>" for name, seats in ROOMS.values())
    return frame.page("program", "Program: GoatConf 2027, 3–5 June, Tuzla",
        "The GoatConf 2027 program: two core days, Thursday 3rd and Friday 4th June, in every room of IPI Academy, Tuzla, and Saturday 5th June for the community.",
        ("img/ipi-lecture-hall.jpg", 1024, 768, "A talk in IPI Academy's lecture hall, students' faces blurred"),
        "The program",
        "Two days of talks in every room of IPI Academy, then a community day on Saturday. Every empty slot is waiting for someone.",
        f"""<section class="album-page wrap" aria-labelledby="h-how">
  <h2 class="band" id="h-how">How a day runs</h2>
  <div class="page-grid">
    <div class="copy">
      <p>Thursday 3rd and Friday 4th June 2027 are the core days, at IPI Academy, Kulina bana 2, Tuzla. Each day runs on one timetable for every room, so you can change rooms at every break.</p>
      <p>Every slot is one hour: a talk with time for questions, a panel, a workshop or something else. Two half-hour sessions can share a slot, and a workshop in a computer centre can run longer. At a workshop, everyone works on the laptop they bring. After each slot comes a full hour off, in the cafés on Freedom Square under five minutes away. That is when you talk to the person you just heard.</p>
      <p>{' '.join(f'{CORE_DAYS[d].split()[0]} runs from {day_hours(d)}.' for d in CORE_DAYS)}</p>
      <p>GoatConf aims to record the sessions in the two big halls, the main hall and the first-floor hall. This is not promised yet, as it depends on the available budget. You may also bring a camera or a podcast and record, and podcasts are welcome in some of the rooms.</p>
      <p>The slots fill as proposals come in and are accepted. Days, times and rooms are final only once the program is finalised, closer to the event. Until then a session's place on this page can still move. <a href="talk.html">Propose a session</a>, or <a href="register.html">register for free</a> to come and listen.</p>
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
  <p class="copy copy--wide">No talks on Saturday. We plan a day at the lakes and run the goat hunt. Walks, meetups and anything else are events people add; each host runs their own and says how to join.</p>
  <ul class="slots slots--kinds">
{sat_items}
{sat_open}
  </ul>
  <p class="copy"><a class="go go--ink" href="add.html">Propose something for Saturday</a></p>
</section>
{around_html}""",
        "files/tools/program.py build from files/program/*.md and files/extensions/*.md")


def session_page(key, meta, body) -> str:
    day, start, room = key
    fmt = esc(format_label(meta))
    about = "".join(f"<p>{esc(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    picked = areas(meta.get("area"))
    flavor = ((f'<dt>{"Areas" if len(picked) > 1 else "Area"}</dt><dd>{", ".join(AREAS[a] for a in picked)}</dd>' if picked else "")
              + (f'<dt>For</dt><dd>{esc(meta["for"])}</dd>' if meta.get("for") else ""))
    seat = (f'<p class="cta"><a class="button" href="{esc(meta["signup"])}">Save a seat</a></p>' if meta.get("signup") else
            '<p>Free with a GoatConf ticket: <a href="register.html">register for free</a>. Closer to June, everyone with a ticket also registers for the sessions they want, because each room has only so many seats.</p>')
    main = f"""<section class="album-page wrap" aria-labelledby="h-details">
  <h2 class="band" id="h-details">The details</h2>
  <div class="page-grid">
    <dl class="facts">
      <dt>When</dt><dd>{CORE_DAYS[day]} 2027, {start} to {ends(start)}</dd>
      <dt>Where</dt><dd>{ROOMS[room][0]} ({ROOMS[room][1]}), IPI Academy, Kulina bana 2, Tuzla</dd>
      <dt>Format</dt><dd>{fmt}</dd>{flavor}
      <dt>{"Speakers" if "," in str(meta["speakers"]) or " and " in str(meta["speakers"]) else "Speaker"}</dt><dd>{who(meta)}</dd>
    </dl>
    <div class="copy">
      {seat}
      <p>After the session comes a full hour off, in the cafés on Freedom Square: the time to talk to the people you just heard.</p>
    </div>
  </div>
</section>
<section class="album-page wrap" aria-labelledby="h-about">
  <h2 class="band" id="h-about">About the session</h2>
  <div class="copy copy--wide">{about}</div>
  <p class="copy"><a class="go go--ink" href="program.html#{day.isoformat()}">The program for {CORE_DAYS[day]}</a> <a class="go go--ink" href="speakers.html">All speakers</a></p>
</section>"""
    return extensions.shell(page_name(meta), f"{esc(meta['title'])}: GoatConf 2027, Tuzla",
                            f"{fmt} by {esc(meta['speakers'])} at GoatConf 2027 in Tuzla, {CORE_DAYS[day]} at {start}, {ROOMS[room][0]}.",
                            ("img/ipi-lecture-hall.jpg", 1024, 768, "A talk in IPI Academy's lecture hall, students' faces blurred"),
                            esc(meta["title"]), f"{fmt} by {who(meta)}. {CORE_DAYS[day]} at {start}, {ROOMS[room][0]}.", main,
                            "files/tools/program.py build from files/program/*.md")


def day_hours(day) -> str:
    """A core day's hours, from its first slot to its end: "10:00 to 17:00"."""
    plan = DAY_PLAN[day]
    return f"{plan['slots'][0]} to {plan['end']}"


def day_note(plan) -> str:
    return f"{plan['note']} Welcome at {plan['welcome']}."


def register_days() -> str:
    """The days on the register page."""
    rows = []
    for i, (day, label) in enumerate(CORE_DAYS.items()):
        where = ", IPI Academy, Kulina bana 2, Tuzla" if i == 0 else ""
        rows.append(f"<li><strong>{label} 2027:</strong> talks, {day_hours(day)}{where}. Welcome at {DAY_PLAN[day]['welcome']}.</li>")
    rows.append(f'<li><strong>{COMMUNITY_DAY[1]} 2027:</strong> the community day. Each event there is run by its host, '
                'who says how to join. See the <a href="program.html">program</a>.</li>')
    return "\n".join(rows)


def slot_times() -> str:
    """Each core day's slot times, for the talk page."""
    return "<br>".join(f"{label} 2027: {', '.join(DAY_PLAN[d]['slots'][:-1])} or {DAY_PLAN[d]['slots'][-1]}."
                       for d, label in CORE_DAYS.items())


def room_sizes() -> str:
    """The rooms and their seats, for the talk page."""
    return "; ".join(f"{name} ({seats})" for name, seats in ROOMS.values()) + "."


# Hand-written pages that carry a part of the day plan, and the part.
DAY_PARTS = [("register.html", "register-days", register_days), ("talk.html", "slot-times", slot_times),
             ("talk.html", "room-sizes", room_sizes)]


def all_pages() -> dict:
    out = {PAGE: nav.place(meta.tag(page()), "program.html")}
    for name, part, make in DAY_PARTS:
        path = PAGE.parent / name
        if not path.exists():  # a scratch site in the tests has only the program
            continue
        text = out[path] if path in out else path.read_text(encoding="utf-8")
        out[path] = blocks.fill(text, part, "tools/program.py", make(), f"site/{name}")
    table, _ = sessions()
    for key, (m, body) in table.items():
        out[PAGE.parent / page_name(m)] = nav.place(meta.tag(session_page(key, m, body)), nav.section(page_name(m)))
    return out


def cmd_build(args) -> int:
    pages = all_pages()
    stale = 0
    stale += sitelib.prune(PAGE.parent.glob("session-*.html"), pages, args.check, "tools/program.py build", "belongs to no session on the program")
    stale += sitelib.write_or_check(pages, args.check, "tools/program.py build")
    return 1 if stale else 0


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
