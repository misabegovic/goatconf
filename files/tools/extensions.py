#!/usr/bin/env python3
"""Extension records and the places to hold them: check them, and build the
site's Make it yours page.

An extension is one Markdown file with YAML frontmatter under extensions/
(ADR wiki/org/adrs/extension-slots-and-the-record.md). The frontmatter is
the record; the body is the host's own description. README.md and files
whose names start with "_" are not records. The places in Tuzla a host
could ask live in places/venues.yml (ADR wiki/org/adrs/make-it-yours-hub.md).

  check [files...]   check every record (or the named ones) and print one
                     summary per record, the text the agent posts on an
                     extension pull request, then check the venues. Exit 1
                     if any record or venue fails.
  build [--check] [--all]
                     write site/extend.html (Make it yours), a page for each
                     accepted event (site/event-<record>.html), and the two
                     old addresses (extensions.html, add.html) that send
                     visitors on to it; with --check, fail if a committed page
                     is not current. --all previews every venue, approved or
                     not, without changing what is approved.

Usage: python3 tools/extensions.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import math  # noqa: E402

import yaml  # noqa: E402

import meta  # noqa: E402
import nav  # noqa: E402
import images  # noqa: E402
import sitelib  # noqa: E402
import frame  # noqa: E402
import formlinks  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "extensions"
PAGE = ROOT / "site" / "extend.html"
VENUES = ROOT / "places" / "venues.yml"
PLACES = ROOT / "places" / "places.yml"
# The old addresses of the two pages Make it yours replaced, kept so shared links still land.
MOVED = {"extensions.html": "Events people add", "add.html": "Propose an event"}

KINDS = {
    "evening-event": "Evening event",
    "trip": "Community trip",
    "meetup": "Meetup",
    "podcast": "Live podcast",
    "hike": "Hike",
    "workshop": "Workshop",
    "hub": "Community hub",
    "activity": "Activity",
    "venue": "Another venue",
    "support": "Support",
    "karaoke": "Karaoke",
    "hackathon": "Hackathon",
    "other": "Something else",
}
FIELDS = ("name", "kind", "host", "location", "start", "end", "cost", "registration", "paid_by", "contact", "accepts")
# GoatConf runs 3–5 June 2027, and events people add run from 2 to 6 June
# (the organiser, 2026-10-19). Outside it, a record must say why.
WINDOW = (dt.date(2027, 6, 2), dt.date(2027, 6, 6))
NOT_OURS = re.compile(r"goatconf\s+(presents|proudly)", re.I)
FREE = re.compile(r"^\s*free\b", re.I)
# On the core days an added event may run only in an hour off, never beside a
# session, and never in Friday's 12:30 hour, kept for Džuma and lunch (the
# organiser, 2026-10-23, sources/conversations/2026-10-23--org--hosts-hub-answers.md).
KEPT_FREE = {(dt.date(2027, 6, 4), "12:30")}


def hour_after(hhmm: str, hours: int = 1) -> str:
    h, m = map(int, hhmm.split(":"))
    return f"{h + hours:02d}:{m:02d}"


def day_plan() -> dict:
    """The core days' times, from tools/program.py; imported late, since program.py imports this module."""
    import program
    return program.DAY_PLAN


def hours_off(day: dt.date) -> list[str]:
    """The hours off a host may use on a core day, as start times: the hour after each slot that has a break."""
    plan = day_plan().get(day)
    if not plan:
        return []
    return [hour_after(s) for s in plan["slots"] if s in plan["breaks"] and (day, hour_after(s)) not in KEPT_FREE]


def core_hours(day: dt.date):
    """From the welcome to the end of a core day, or None on any other day."""
    plan = day_plan().get(day)
    if not plan:
        return None
    t = lambda hhmm: dt.datetime.combine(day, dt.time(*map(int, hhmm.split(":"))))
    return t(plan["welcome"]), t(plan["end"])


def core_day_problem(meta, start, end):
    """Why an event on a core day does not fit, or None: it must sit inside one hour off and be free."""
    if start.time() == dt.time() and end.time() == dt.time():
        end = end + dt.timedelta(days=1)  # a record with dates only runs through its last day
    for day in (start.date() + dt.timedelta(days=i) for i in range((end.date() - start.date()).days + 1)):
        hours = core_hours(day)
        if hours and start < hours[1] and end > hours[0] and (start.date() != end.date() or day != start.date()):
            return "it runs through a core day's sessions: on Thursday and Friday an event fits only an hour off, or before or after the day"
    hours = core_hours(start.date())
    if not hours or end <= hours[0] or start >= hours[1]:
        return None
    if end.date() != start.date():
        return "it runs through a core day's sessions: on Thursday and Friday an event fits only an hour off, or before or after the day"
    day = start.date()
    for off in hours_off(day):
        lo = dt.datetime.combine(day, dt.time(*map(int, off.split(":"))))
        if lo <= start and end <= lo + dt.timedelta(hours=1):
            if not FREE.match(str(meta.get("cost", ""))):
                return "an event in an hour off is free: set cost to free"
            return None
    offs = ", ".join(hours_off(day))
    return (f"it overlaps the sessions on {day.strftime('%A %-d %B')}: an event that day fits inside one hour off "
            f"({offs}, one hour each), or before {core_hours(day)[0]:%H:%M} or after {core_hours(day)[1]:%H:%M}")


def records(paths=None):
    return sitelib.records(RECORDS, paths)


parse = sitelib.parse


def as_datetime(value):
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time())
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(value.strip(), fmt)
            except ValueError:
                pass
    return None


def check_record(path: Path):
    meta, body, problems = parse(path)
    notes = []
    if meta is None:
        return problems, notes, None
    for field in FIELDS:
        if field not in meta or meta[field] in (None, ""):
            problems.append(f"missing field: {field}")
    kind = meta.get("kind")
    if kind and kind not in KINDS:
        problems.append(f"kind '{kind}' is not one of: {', '.join(KINDS)}")
    if meta.get("accepts") is not True:
        problems.append("accepts must be yes: the host accepts the charter and the code of conduct")
    start, end = as_datetime(meta.get("start")), as_datetime(meta.get("end"))
    if meta.get("start") and not start:
        problems.append("start is not a date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    if meta.get("end") and not end:
        problems.append("end is not a date (YYYY-MM-DD or YYYY-MM-DD HH:MM)")
    if start and end and end < start:
        problems.append("end comes before start")
    if start and end and not end < start:
        clash = core_day_problem(meta, start, end)
        if clash:
            problems.append(clash)
    if start and not (WINDOW[0] <= start.date() <= WINDOW[1]):
        if meta.get("outside_week_reason"):
            notes.append(f"outside the GoatConf week, with a reason: {meta['outside_week_reason']}")
        else:
            problems.append("dates fall outside the GoatConf week and no outside_week_reason is given")
    if kind == "support" and not meta.get("supplier"):
        problems.append("a support record names the supplier the supporter pays (field: supplier)")
    if not body:
        problems.append("no description below the frontmatter")
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", path.stem):
        problems.append("file name must be lowercase words joined by hyphens: it becomes the event's own address")
    name = str(meta.get("name", ""))
    if NOT_OURS.search(name) or NOT_OURS.search(body) or name.lower().startswith("goatconf"):
        problems.append('the name reads as if the organiser runs it; name it as "<name>, part of GoatConf 2027"')
    if not problems and meta.get("accepted") is not True:
        notes.append("not yet accepted by the organiser, so not listed: set accepted: yes once it is")
    return problems, notes, meta


def listed(meta) -> bool:
    """Only events the organiser accepted are part of GoatConf and shown to attendees."""
    return meta.get("accepted") is True


def cmd_check(args) -> int:
    paths = records(args.files)
    if not paths:
        print("extensions: no records yet")
        return report_venues()
    failed = 0
    for path in paths:
        problems, notes, meta = check_record(path)
        rel = path.relative_to(ROOT) if path.is_absolute() and ROOT in path.parents else path
        title = (meta or {}).get("name") or path.stem
        print(f"{rel}: {title}")
        if problems:
            failed += 1
            for p in problems:
                print(f"  needs a change: {p}")
        else:
            state = "accepted, listed" if listed(meta) else "waiting for the organiser's acceptance"
            print(f"  ok: {KINDS[meta['kind']].lower()}, hosted by {meta['host']}, accepts the charter and the code of conduct; {state}")
        for n in notes:
            print(f"  note: {n}")
    print(f"extensions: {len(paths)} record(s), {failed} need a change")
    return 1 if report_venues() or failed else 0


def report_venues() -> int:
    """Print what is wrong with the venues, and a one-line summary; 1 if any needs a change."""
    vp = check_venues()
    for vid, problem in vp:
        print(f"places/venues.yml: {vid}: needs a change: {problem}")
    data = venue_data().get("venues") or []
    if data:
        print(f"venues: {len(data)} place(s), {sum(1 for v in data if v.get('approved') is True)} approved, {len({v for v, _ in vp})} need a change")
    return 1 if vp else 0


def when(meta):
    start, end = as_datetime(meta["start"]), as_datetime(meta["end"])
    day = start.strftime("%-d %B %Y")
    if start.time() == dt.time() and end.time() == dt.time():
        return day if start.date() == end.date() else f"{day} to {end.strftime('%-d %B %Y')}"
    span = f"{start.strftime('%H:%M')} to {end.strftime('%H:%M')}"
    return f"{day}, {span}" if start.date() == end.date() else f"{day} {start.strftime('%H:%M')} to {end.strftime('%-d %B %H:%M')}"


def link(value):
    """A web address or an email as a link, shown without its scheme; anything else as text."""
    v = str(value)
    if re.match(r"^https?://", v):
        return f'<a href="{html.escape(v)}">{html.escape(re.sub(r"^https?://(www\.)?", "", v).rstrip("/"))}</a>'
    if re.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", v, re.I):
        return f'<a href="mailto:{html.escape(v)}">{html.escape(v)}</a>'
    return html.escape(v)


def page_name(slug: str) -> str:
    """Each accepted event's own page, next to the other pages so relative links keep working."""
    return f"event-{slug}.html"


def cards(slug: str) -> dict:
    """The event's shareable cards in site/share/, made by tools/shareables.py: to post, and the page's link preview."""
    return {"square": f"event-{slug}-square.png", "wide": f"event-{slug}-wide.png", "preview": f"event-{slug}-preview.png"}


def accepted():
    """The accepted events that pass the check, by start then name: (start, slug, meta, body)."""
    good = []
    for path in records():
        problems, _, meta = check_record(path)
        if not problems and listed(meta):
            _, body, _ = parse(path)
            good.append((as_datetime(meta["start"]), path.stem, meta, body))
    return sorted(good, key=lambda g: (g[0], str(g[2]["name"])))


def card(n: int, slug: str, meta) -> str:
    """An accepted event as a sticker that opens its page; the events page and the home page share it."""
    return (f'<li><a class="sticker sticker--fact sticker--example" href="{page_name(slug)}" style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">'
            f'<span class="num">{n}</span><small class="sticker__kind">{KINDS[meta["kind"]]}</small><strong>{html.escape(str(meta["name"]))}</strong>'
            f'<small>{when(meta)}. Run by {html.escape(str(meta["host"]))}.</small></a></li>')


OLD_TOWN = ("img/city-old-town-aerial-paving.jpg", 1375, 696, "The old town from above: tiled roofs and a street paved in a red and blue mosaic")
MORE = "More than one of each is welcome: a second meetup, another hike, a dinner every night."


def shell(name: str, title: str, description: str, photo, h1: str, lede: str, main: str, made_by: str, preview: str = "", photo_class: str = "") -> str:
    """A page of the site around its main part; the events page, each event's page and each session's page use it."""
    return frame.page(name[:-5], title, description, photo, h1, lede, main, made_by, preview, photo_class)


def host_profile(slug: str):
    """The supporter whose record lists this event under `events:`, as (profile page, name), or None.
    tools/speakers.py checks supporter records in full and builds the profile, supporter-<record>.html."""
    folder = ROOT / "supporters"
    for path in sorted(folder.glob("*.md")) if folder.is_dir() else []:
        if path.name == "README.md" or path.name.startswith("_"):
            continue
        rec, _, problems = parse(path)
        if rec and not problems and slug in (rec.get("events") or []):
            return f"supporter-{path.stem}.html", str(rec.get("name") or path.stem)
    return None


def event_page(slug: str, meta, body) -> str:
    e = lambda k: html.escape(str(meta[k]))
    profile = host_profile(slug)
    run_by = f'<a href="{profile[0]}">{e("host")}</a>' if profile else e("host")
    supporter = (f'\n      <p>{html.escape(profile[1])} is a supporter of GoatConf 2027. <a href="{profile[0]}">See their profile</a>: who they are and how to support them.</p>'
                 if profile else "")
    to_profile = f' <a class="go go--ink" href="{profile[0]}">{html.escape(profile[1])}</a>' if profile else ""
    start = as_datetime(meta["start"])
    # The program has a section per day from Thursday to Saturday; other days sit under "Around the talks".
    day = start.date().isoformat() if dt.date(2027, 6, 3) <= start.date() <= dt.date(2027, 6, 5) else "h-around"
    reg = str(meta["registration"])
    cta = (f'<p class="cta"><a class="button" href="{html.escape(reg)}">Register with the host</a></p>' if re.match(r"^https?://", reg)
           else f"<p><strong>How to join:</strong> {html.escape(reg)}</p>")
    about = "".join(f"<p>{html.escape(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    kind = f"{KINDS[meta['kind']]}, part of GoatConf 2027, run by {e('host')}"
    main = f"""<section class="album-page wrap" aria-labelledby="h-details">
  <h2 class="band" id="h-details">The details</h2>
  <div class="page-grid">
    <dl class="facts">
      <dt>When</dt><dd>{when(meta)}</dd>
      <dt>Where</dt><dd>{e('location')}</dd>
      <dt>Cost</dt><dd>{e('cost')}</dd>
      <dt>Register</dt><dd>{link(meta['registration'])}</dd>
      <dt>Run by</dt><dd>{run_by}</dd>
      <dt>Paid by</dt><dd>{e('paid_by')}</dd>
      <dt>Contact</dt><dd>{link(meta['contact'])}</dd>
    </dl>
    <div class="copy">
      {cta}
      <p>We accepted it as part of GoatConf 2027. {e('host')} runs it and pays for it, so questions about it go to the host. It follows the <a href="charter.html">charter</a> and the <a href="code-of-conduct.html">code of conduct</a>.</p>{supporter}
    </div>
  </div>
</section>
<section class="album-page wrap" aria-labelledby="h-about">
  <h2 class="band" id="h-about">In the host's words</h2>
  <div class="copy copy--wide">{about}</div>
  <p class="copy"><a class="go go--ink" href="extend.html">All events people add</a> <a class="go go--ink" href="program.html#{day}">The program for that day</a>{to_profile}</p>
</section>{share_section(cards(slug), f"The card for {e('name')}", "For the host and anyone going: post it wherever you like. It links back to this page.")}"""
    names = cards(slug)
    preview = names["preview"] if (PAGE.parent / "share" / names["preview"]).exists() else ""
    return shell(page_name(slug), f"{e('name')}: part of GoatConf 2027, Tuzla", f"{kind}: {when(meta)}, {e('location')}.",
                 OLD_TOWN, e("name"), f"{kind}. {when(meta)}.", main, "files/tools/extensions.py build from files/extensions/*.md", preview)


def share_section(names: dict, alt: str, note: str, heading: str = "Cards to share", site=None) -> str:
    """Both cards to look at, the square and the wide, each with its download; nothing until the cards are rendered."""
    if not all(((site or PAGE.parent) / "share" / names[k]).exists() for k in ("square", "wide")):
        return ""
    return f"""
<section class="album-page wrap" aria-labelledby="h-cards-{names['wide'][:-9]}">
  <h2 class="band" id="h-cards-{names['wide'][:-9]}">{heading}</h2>
  <p class="copy copy--wide">{note}</p>
  <div class="share-cards">
    <figure><img class="share-card" src="share/{names['square']}" width="1080" height="1080" alt="{alt}, the square card" loading="lazy">
      <figcaption><a class="go go--ink" href="share/{names['square']}" download>Download the square card</a></figcaption></figure>
    <figure><img class="share-card" src="share/{names['wide']}" width="1200" height="675" alt="{alt}, the wide card" loading="lazy">
      <figcaption><a class="go go--ink" href="share/{names['wide']}" download>Download the wide card</a></figcaption></figure>
  </div>
</section>"""


# Venues: the places in Tuzla a host could ask (places/venues.yml).
VENUE_KINDS = {"culture": "Cultural house", "bar": "Bar or pub", "cafe": "Café", "restaurant": "Restaurant",
               "hotel": "Hotel", "study": "Study or tech space", "outdoors": "Outdoors"}
SETTINGS = {"indoor": "Indoors", "outdoor": "Outdoors", "both": "Indoors and out"}
VENUE_FIELDS = ("id", "name", "kind", "address", "size", "setting", "suits", "about", "contact", "sources", "approved")
NEAR_M = 400      # under this, a short event fits an hour off, by the album's own reckoning of a five to eight minute walk
WALK_M = 1500     # under this, a walk from IPI Academy
SIZES = (("small", "Up to 40 people", 40), ("medium", "40 to 150 people", 150), ("large", "More than 150 people", None))


def venue_data() -> dict:
    return yaml.safe_load(VENUES.read_text(encoding="utf-8")) if VENUES.exists() else {"venues": []}


def ipi() -> tuple:
    data = yaml.safe_load(PLACES.read_text(encoding="utf-8"))
    return data["ipi"]["lat"], data["ipi"]["lon"]


def metres(a, b) -> float:
    """Straight-line distance, as tools/places.py measures it."""
    dy = (a[0] - b[0]) * 111_320
    dx = (a[1] - b[1]) * 111_320 * math.cos(math.radians(a[0]))
    return math.hypot(dx, dy)


def distance(v):
    """Metres from IPI Academy, or None when no source places it."""
    if v.get("lat") is not None and v.get("lon") is not None:
        return metres(ipi(), (v["lat"], v["lon"]))
    return float(v["metres"]) if v.get("metres") is not None else None


def check_venues(data=None) -> list:
    """What is wrong with each venue record, as (id, problem) pairs."""
    data = venue_data() if data is None else data
    problems, seen = [], set()
    for i, v in enumerate(data.get("venues") or []):
        vid = str(v.get("id") or f"venue {i + 1}")
        for field in VENUE_FIELDS:
            if field not in v or v[field] is None or (field != "contact" and v[field] in ("", [])):
                problems.append((vid, f"missing field: {field}"))
        if vid in seen:
            problems.append((vid, "two venues share this id"))
        seen.add(vid)
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", vid):
            problems.append((vid, "id must be lowercase words joined by hyphens: it becomes the place's anchor on the page"))
        if v.get("kind") and v["kind"] not in VENUE_KINDS:
            problems.append((vid, f"kind '{v['kind']}' is not one of: {', '.join(VENUE_KINDS)}"))
        if v.get("setting") and v["setting"] not in SETTINGS:
            problems.append((vid, f"setting '{v['setting']}' is not one of: {', '.join(SETTINGS)}"))
        for k in v.get("suits") or []:
            if k not in KINDS:
                problems.append((vid, f"suits '{k}', which is not a kind of event: {', '.join(KINDS)}"))
        if not isinstance(v.get("contact", []), list):
            problems.append((vid, "contact is a list of web addresses, emails and phone numbers"))
        for src in v.get("sources") or []:
            if not (ROOT / src).exists():
                problems.append((vid, f"source not found: {src}"))
        if v.get("approved") not in (True, False):
            problems.append((vid, "approved is yes or no, set by the organiser only"))
        if v.get("photo"):
            photo = ROOT / "site" / "img" / "venues" / v["photo"]
            record = ROOT / "assets" / "images" / "venues" / f"{v['photo']}.json"
            if not photo.exists():
                problems.append((vid, f"photo not found: site/img/venues/{v['photo']}"))
            if not record.exists():
                problems.append((vid, f"the photo has no record of where it came from: assets/images/venues/{v['photo']}.json"))
        if v.get("people") is not None and not isinstance(v["people"], int):
            problems.append((vid, "people is a whole number"))
    return problems


def venues(show_all=False) -> list:
    """The venues to show, nearest first, those with no distance last."""
    data = venue_data()
    shown = [dict(v) for v in data.get("venues") or [] if show_all or v.get("approved") is True]
    for v in shown:
        v["_m"] = distance(v)
    return sorted(shown, key=lambda v: (v["_m"] is None, v["_m"] or 0, str(v["name"])))


def far(m) -> str:
    if m is None:
        return "Distance from IPI Academy not measured"
    if m < 1000:
        return f"About {max(50, round(m / 50) * 50)} m from IPI Academy"
    return f"About {m / 1000:.1f} km from IPI Academy".replace(".0 km", " km")


def size_band(v) -> str:
    n = v.get("people")
    if n is None:
        return "unknown"
    for key, _, top in SIZES:
        if top is None or n <= top:
            return key
    return "unknown"


def contact_link(value) -> str:
    """A venue's contact as a link: a phone to call, an email, or a web address shown short."""
    v = str(value).strip()
    if re.match(r"^\+?[0-9][0-9 /-]{6,}$", v):
        return f'<a href="tel:{re.sub(r"[^0-9+]", "", v)}">{html.escape(v)}</a>'
    m = re.match(r"^https?://(?:www\.)?([^/]+)(/.*)?$", v)
    if m:
        shown = (m.group(1) + (m.group(2) or "")).rstrip("/")
        return f'<a href="{html.escape(v)}">{html.escape(shown if len(shown) <= 28 else m.group(1))}</a>'
    return link(v)


NUMBERS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
# The kinds of event in the plural, for "Good for meetups and karaoke."
PLURAL = {"evening-event": "evening events", "trip": "community trips", "meetup": "meetups", "podcast": "live podcasts",
          "hike": "hikes", "workshop": "workshops", "hackathon": "hackathons", "karaoke": "karaoke", "other": "something else"}


def kinds_text(suits) -> str:
    names = [PLURAL.get(k, KINDS[k].lower()) for k in suits]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def photo_record(name: str) -> dict:
    path = ROOT / "assets" / "images" / "venues" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def venue_card(n: int, v) -> str:
    e = lambda k: html.escape(str(v[k]))
    m = v["_m"]
    if v.get("photo"):
        rec = photo_record(v["photo"])
        alt = html.escape(str(rec.get("subject") or rec.get("title") or v["name"]))
        photo = f'<img src="img/venues/{html.escape(v["photo"])}" alt="{alt}" loading="lazy">'
    else:
        photo = f'<span class="speaker__goat venue__empty">{frame.sitting()}<small>No photo yet</small></span>'
    english = f'<span class="venue__english">{e("english")}</span>' if v.get("english") else ""
    where = f'{e("address")}. {far(m)}' + (", from the street" if v.get("point") == "street" and m is not None else "") + "."
    tags = [f'<span class="tag">{VENUE_KINDS[v["kind"]]}</span>'] + ([] if v["kind"] == "outdoors" else [f'<span class="tag">{SETTINGS[v["setting"]]}</span>'])
    if m is not None and m <= NEAR_M:
        tags.append('<span class="tag tag--near">Fits an hour off</span>')
    if v.get("check_first"):
        tags.append('<span class="tag tag--first">Ask GoatConf first</span>')
    first = ('<p class="venue__first">GoatConf may use this place for its own program. '
             '<a href="contact.html">Write to us</a> before you plan here.</p>') if v.get("check_first") else ""
    contacts = " ".join(contact_link(c) for c in v.get("contact") or [])
    if v.get("lat") is not None:
        contacts += f' <a href="https://www.openstreetmap.org/?mlat={v["lat"]}&amp;mlon={v["lon"]}#map=18/{v["lat"]}/{v["lon"]}">Map</a>'
    ask = f'<p class="venue__links">{contacts.strip()}</p>' if contacts.strip() else '<p class="venue__links">No public contact found: ask a local, or ask us.</p>'
    text = " ".join(str(v.get(k) or "") for k in ("name", "english", "address", "about", "size")) + " " + VENUE_KINDS[v["kind"]] + " " + kinds_text(v["suits"])
    attrs = (f' data-venue data-kinds="{" ".join(v["suits"])}" data-size="{size_band(v)}" data-near="{1 if m is not None and m <= NEAR_M else 0}"'
             f' data-walk="{1 if m is not None and m <= WALK_M else 0}" data-setting="{v["setting"]}" data-first="{1 if v.get("check_first") else 0}"'
             f' data-text="{html.escape(text.lower())}"')
    return f"""  <li class="sticker sticker--venue" id="venue-{e('id')}"{attrs} style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">
    <span class="num">{n}</span>
    <figure class="speaker__photo venue__photo">{photo}<figcaption>{e('name')}</figcaption></figure>
    <div class="venue__body">
      {english}<p class="venue__where">{where}</p>
      <p class="venue__tags">{" ".join(tags)}</p>
      <p>{e('about')}</p>
      <p class="venue__size">{e('size')}</p>
      <p class="venue__suits">Good for {kinds_text(v["suits"])}.</p>{first}
      {ask}
    </div>
  </li>"""


# What to run: the kinds on the form, in its order, each with what it needs and the kind of place that suits it.
WHAT = (
    ("evening-event", "A dinner, a party or a DJ night. Try a pub with a garden, a hotel restaurant or the youth centre."),
    ("trip", "Take a group out of Tuzla for a day: Lake Modrac, Konjuh or the fortress at Srebrenik. Meet on Freedom Square."),
    ("meetup", "For your community, your language or your stack, in a café or a room. A small one fits an hour off."),
    ("podcast", "Record an episode in front of the people who come. Podcasts are welcome in some of the rooms."),
    ("hike", "Ilinčica is a walk from the centre; Konjuh is a day out. Say how fit people need to be."),
    ("hackathon", "You organise all of it: the room, the theme, the judging and any prizes. No collecting attendees' data."),
    ("karaoke", "Book a café near Freedom Square, or a bar that takes private events, and bring the songs."),
    ("other", "A walk through the old town, a quiz, a run by the lakes, a corner for your community."),
)


def what_block(start: int) -> str:
    items = []
    for i, (kind, tip) in enumerate(WHAT):
        label = "Something else?" if kind == "other" else KINDS[kind]
        items.append(f'    <li><a class="slot slot--format slot--link" href="#where" data-pick-kind="{kind}">{frame.peek(kind)}'
                     f'<span class="num num--printed">{start + i}</span><strong>{label}</strong><small>{tip}</small><span class="stamp">Yours?</span></a></li>')
    return '  <ul class="slots slots--kinds slots--what" aria-label="Kinds of events you can run">\n' + "\n".join(items) + "\n  </ul>"


def hours_text() -> str:
    """The hours off a host may use, in words, from the day plan: "Thursday at 11:00, 13:00 and 15:00, and Friday at 10:30 and 14:30"."""
    parts = []
    for day in sorted(day_plan()):
        offs = hours_off(day)
        if offs:
            times = offs[0] if len(offs) == 1 else ", ".join(offs[:-1]) + " and " + offs[-1]
            parts.append(f"{day.strftime('%A')} at {times}")
    return ", and ".join(parts)


def finder() -> str:
    """The filters over the places; hidden until the script shows them, so the full list reads without it."""
    kinds = "".join(f'<option value="{k}">{"Something else" if k == "other" else KINDS[k]}</option>' for k, _ in WHAT)
    sizes = "".join(f'<option value="{k}">{label}</option>' for k, label, _ in SIZES)
    return f"""  <form class="finder" data-finder hidden role="search" aria-label="Find a place">
    <p class="finder__field finder__field--wide"><label for="f-text">Search the places</label><input id="f-text" name="text" type="search" placeholder="A name, a street, a kind of place"></p>
    <p class="finder__field"><label for="f-kind">What you want to run</label><select id="f-kind" name="kind"><option value="">Anything</option>{kinds}</select></p>
    <p class="finder__field"><label for="f-size">How many people</label><select id="f-size" name="size"><option value="">Any size</option>{sizes}</select></p>
    <p class="finder__field"><label for="f-far">How far from IPI Academy</label><select id="f-far" name="far"><option value="">Anywhere</option><option value="near">Fits an hour off (under 400 m)</option><option value="walk">A walk (under 1.5 km)</option></select></p>
    <p class="finder__field"><label for="f-setting">Indoors or out</label><select id="f-setting" name="setting"><option value="">Either</option><option value="indoor">Indoors</option><option value="outdoor">Outdoors</option></select></p>
    <p class="finder__field finder__field--check"><input id="f-first" name="first" type="checkbox"><label for="f-first">Leave out places to ask GoatConf about first</label></p>
    <p class="finder__count" data-count aria-live="polite"></p>
  </form>"""


def hub(show_all=False) -> str:
    good = accepted()
    n = 0
    if good:
        cards = "\n".join("  " + card(i + 1, s, m) for i, (_, s, m, _b) in enumerate(good))
        n = len(good) + 1
        cards += (f'\n  <li><a class="slot slot--link slot--open" href="#propose">{frame.peek("event")}'
                  f'<span class="num num--printed">{n}</span><strong>Yours next?</strong><small>{MORE}</small><span class="stamp">Yours?</span></a></li>')
        listings = f'<ul class="slots slots--events">\n{cards}\n</ul>'
    else:
        listings = """<div class="ledger-empty">
  <p><strong>No events yet.</strong> The first one could be yours: a workshop, a meetup, a dinner, a city walk, a hike, a corner for your community.</p>
</div>"""
    places = venues(show_all)
    firsts = sum(1 for v in places if v.get("check_first"))
    first_note = (f' {"One is" if firsts == 1 else NUMBERS.get(firsts, str(firsts)) + " are"} marked "Ask GoatConf first", because we may use '
                  f'{"it" if firsts == 1 else "them"} for our own program.') if firsts else ""
    if places:
        start = n + len(WHAT) + 1
        vcards = "\n".join(venue_card(start + i, v) for i, v in enumerate(places))
        checked = dt.date.fromisoformat(str(venue_data().get("checked")))
        where = f"""{finder()}
  <ul class="slots slots--venues" data-places>
{vcards}
  </ul>
  <p class="ledger-empty" data-none hidden>No place matches all of that. Try fewer filters, or pick any place you like: these are only ideas.</p>
  <p class="checked">Checked on {checked.day} {checked:%B %Y}. Places change hands and close: ask each one before you plan, and tell us if something here is wrong.</p>"""
    else:
        where = '<p class="ledger-empty">We are still checking the places in Tuzla where you could run something. The list will be here.</p>'
    main = f"""<section class="album-page wrap" aria-labelledby="h-adding">
  <h2 class="band" id="h-adding">What people are adding</h2>
  <p class="copy copy--wide">Every event here is part of GoatConf 2027: we accepted it, and it follows the <a href="charter.html">charter</a> and the <a href="code-of-conduct.html">code of conduct</a>. Each host runs their own event and pays for it directly. Open one to see when and where, and how to join.</p>
  {listings}
</section>
<section class="album-page wrap" aria-labelledby="h-how">
  <h2 class="band" id="h-how">How to host</h2>
  <div class="page-grid">
    <div class="howto">
      <ol class="steps">
        <li><strong>Pick what.</strong> A meetup, a party, a walk, a dinner, anything. Small is fine: ten people round a café table is an event.</li>
        <li><strong>Pick when.</strong> Any day from 2 to 6 June 2027. The evenings are free, and so is Saturday, the community's day. On Thursday and Friday you can also use an hour off between sessions: {hours_text()}. Friday at 12:30 stays free for Džuma and lunch.</li>
        <li><strong>Pick where.</strong> Any place you like: the ones below are ideas. Ask the place yourself, since GoatConf has arranged nothing with them.</li>
        <li><strong>Plan the people.</strong> Free events lose up to half of the people who sign up, so plan for that and keep a waiting list. Say clearly what is accessible and what is not.</li>
        <li><strong>Propose it.</strong> Fill in the short form. We read every proposal, may ask for changes, and write back either way. Once we accept it, it goes on this page and on the <a href="program.html">program</a>.</li>
        <li><strong>On the day,</strong> arrive early, put up a sign, and have a plan for rain: June is Tuzla's wettest month. Ask before you record anyone.</li>
      </ol>
      <p class="cta"><a class="button" data-form="add" href="#propose">Propose your event</a><span>Open now. It takes about ten minutes.</span></p>
    </div>
    <div class="copy">
      <h3 class="list-title">In an hour off</h3>
      <p>An event in an hour off is short, free and open to everyone who comes. It is near IPI Academy, so people can walk there and back, and it ends five minutes before the next session starts. Nothing runs at the same time as a session.</p>
      <h3 class="list-title">Before you book a place</h3>
      <ul class="checklist">
        <li>How many people does it hold, and is the room yours for the whole time?</li>
        <li>Is there step-free access and an accessible toilet?</li>
        <li>What does it have: chairs, tables, a screen, sound, power for laptops?</li>
        <li>What does it cost, and what happens if you cancel?</li>
        <li>Does it sell food and drink, or can people bring their own?</li>
        <li>Can you visit it before the day?</li>
      </ul>
      <h3 class="list-title">Tuzla's rules</h3>
      <p>An event inside a café, a hotel or a hall follows that place's rules. A free event for culture or fun is not reported to the police, unless its size calls for extra safety: then tell the local police station at least five days ahead. An event that charges for entry is reported at least seven days ahead. When in doubt, ask the place, or <a href="contact.html">ask us</a>.</p>
    </div>
  </div>
</section>
<section class="album-page wrap" aria-labelledby="h-what">
  <h2 class="band" id="h-what">What you could run</h2>
  <p class="copy copy--wide">{MORE} Pick one to see the places that suit it.</p>
{what_block(n + 1)}
</section>
<section class="album-page wrap" aria-labelledby="h-where" id="where">
  <h2 class="band" id="h-where">Where in Tuzla</h2>
  <p class="copy copy--wide">Places a host could ask, from cafés on Freedom Square to halls for a few hundred people. GoatConf has arranged nothing with them: you ask, you book and you pay.{first_note}</p>
{where}
</section>
<section class="album-page wrap" aria-labelledby="h-propose" id="propose">
  <h2 class="band" id="h-propose">Propose yours</h2>
  <div class="page-grid">
    <div class="howto">
      <p class="cta"><a class="button" data-form="add" href="#propose">Propose your event</a><span>Open now. It takes about ten minutes.</span></p>
      <h3 class="list-title">What happens next</h3>
      <ol class="steps">
        <li><strong>You fill in the form:</strong> the name, the kind, the host, where, when, the cost, how people join, who pays, a public contact and a short description.</li>
        <li><strong>We decide</strong> whether it becomes part of GoatConf, may ask for changes, and write back either way.</li>
        <li><strong>If accepted, it goes on this page</strong> and on the <a href="program.html">program</a>.</li>
      </ol>
    </div>
    <div class="copy">
      <h3 class="list-title">The rules</h3>
      <p>Not everything people propose becomes part of GoatConf. We accept what follows the <a href="code-of-conduct.html">code of conduct</a> and the <a href="charter.html">charter</a> and fits the program: its time, its place, who it is for and how it sits next to the talks. You run it and you pay for it, and its name says who runs it, for example "Rust night, part of GoatConf 2027". Anything not accepted may still happen, but not under GoatConf's name.</p>
      <p><strong>An event or a session?</strong> An event is something you run and pay for yourself. A talk, a panel or a workshop in one of the hour slots at IPI Academy on Thursday or Friday is a session, picked by us: <a href="talk.html">propose a session</a> instead.</p>
      <p>If you or your organisation fund and run it, you can also be listed as a <a href="supporters.html">supporter</a>. Want to support GoatConf with money or something in kind instead? See the <a href="supporters.html">supporters page</a>.</p>
    </div>
  </div>
</section>"""
    page = shell("extend.html", "Make it yours: GoatConf 2027",
                 "Every GoatConf is shaped by who joins it. Add a meetup, a party, a walk or a workshop to GoatConf 2027 in Tuzla: how to host, what to run, and places to ask.",
                 OLD_TOWN, "Make it yours",
                 "Every GoatConf is shaped by who joins it. Add a meetup, a party, a walk or a workshop: you run it, and once we accept it, it is part of GoatConf 2027.",
                 main, "files/tools/extensions.py build from files/extensions/*.md and files/places/venues.yml")
    page = page.replace('<script src="album.js" defer></script>', '<script src="album.js" defer></script>\n<script src="extend.js" defer></script>')
    return formlinks.rewrite(page, formlinks.forms())


def moved(name: str, label: str) -> str:
    """An old address that sends the visitor on to Make it yours, for links shared before the pages became one."""
    main = f"""<section class="album-page wrap" aria-labelledby="h-moved">
  <h2 class="band" id="h-moved">This page moved</h2>
  <p class="copy copy--wide">{label} is now part of Make it yours: the events people add, how to host, places in Tuzla, and the form, on one page.</p>
  <p class="copy"><a class="go go--ink" href="extend.html">Go to Make it yours</a></p>
</section>"""
    page = shell(name, f"{label}: now Make it yours, GoatConf 2027",
                 "This page is now part of Make it yours: the events people add to GoatConf 2027, how to host, and places in Tuzla.",
                 OLD_TOWN, label, "Now part of Make it yours.", main, "files/tools/extensions.py build")
    page = page.replace(f'<link rel="canonical" href="https://goatconf.com/{name[:-5]}">',
                        '<meta name="robots" content="noindex">\n<meta http-equiv="refresh" content="0; url=extend.html">\n<link rel="canonical" href="https://goatconf.com/extend">')
    return page


def all_pages(show_all=False) -> dict:
    out = {PAGE: nav.place(meta.tag(hub(show_all)), "extend.html")}
    for name, label in MOVED.items():
        out[PAGE.parent / name] = nav.place(meta.tag(moved(name, label)), nav.section(name))
    for _, slug, m, body in accepted():
        out[PAGE.parent / page_name(slug)] = nav.place(meta.tag(event_page(slug, m, body)), nav.section(page_name(slug)))
    return out


def cmd_build(args) -> int:
    pages = all_pages(getattr(args, "all", False))
    stale = 0
    if args.check:
        for _, slug, _, _ in accepted():
            for name in cards(slug).values():
                if not (PAGE.parent / "share" / name).exists():
                    print(f"site/share/{name} is missing: run python3 tools/shareables.py render --only event-{slug}")
                    stale += 1
    stale += sitelib.prune(PAGE.parent.glob("event-*.html"), pages, args.check, "tools/extensions.py build", "belongs to no accepted event")
    stale += sitelib.write_or_check(pages, args.check, "tools/extensions.py build")
    return 1 if stale else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("files", nargs="*")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    b.add_argument("--all", action="store_true")
    args = ap.parse_args(argv)
    return cmd_check(args) if args.cmd == "check" else cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
