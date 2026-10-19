#!/usr/bin/env python3
"""Files for search engines and AI agents, built from the same records as the pages.

  site/llms.txt             a plain-text guide to GoatConf and every page
  site/program.json         every day, room, session and event as data
  site/goatconf-2027.ics    the three days, for any calendar
  site/sitemap.xml          every page, for crawlers
  site/robots.txt           everyone may read; where the sitemap is
  site/index.html           schema.org Event data between <!-- event data --> markers

Nothing people see on the pages changes. Change a fact in the records,
tools/program.py or the constants below, then run build.

Usage: python3 tools/agents.py build [--check]
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
import extensions  # noqa: E402
import nav  # noqa: E402
import program  # noqa: E402
import speakers  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://goatconf.com/"
OFFSET = "+02:00"  # Central European Summer Time in June
LUMA = "https://luma.com/event/evt-dU4KbLhpIAm9Y9V"
STAMP = "20261012T000000Z"  # fixed, so the calendar file only changes when the days do

# The facts below are the ones the pages state, each cited in wiki/org/goatconf-2027.md
# and wiki/org/ipi-academy.md.
EVENT = {
    "name": "GoatConf 2027",
    "summary": "A free conference for people who build and sell software: engineers, designers, product people, founders, and the incurably curious dreamers and visionaries. Any programming language, any stack. An excuse to hang out with like-minded people and learn from folks sharing their current best. In Tuzla, Bosnia and Herzegovina, on 3–5 June 2027.",
    "venue": "IPI Academy (IPI Akademija Tuzla)",
    "street": "Kulina bana 2",
    "postcode": "75000",
    "city": "Tuzla",
    "country": "BA",
    "lat": 44.5404,
    "lon": 18.6738,
    "organiser": ("Muhamed Isabegović", "https://muhamed.at"),
    "email": "info@muhamed.at",
}
FACTS = [
    "Dates: Thursday 3rd and Friday 4th June 2027 are talk days; Saturday 5th June 2027 is the community day.",
    "Place: IPI Academy, Kulina bana 2, 75000 Tuzla, Bosnia and Herzegovina, next to Freedom Square (Trg slobode).",
    "Price: tickets are free. Registration asks only for a name and an email, on Luma.",
    "Format: one-hour talks, panels and workshops in all seven rooms of IPI Academy, with an hour off after each slot. Proposals for 30 minutes are welcome too, and may be paired into one hour. Closer to June, people with a ticket also register for the sessions they want, because each room has only so many seats; everyone with a ticket gets an email with how, and seats nobody registered for go to whoever is at the door.",
    "Friday starts half an hour earlier, at 09:30, and ends at 16:30.",
    "Saturday has no talks: it is the community's day, with the organiser's day at the Pannonian salt lakes and the goat hunt, plus events people add, such as walks and meetups.",
    "Talks: an open call; anyone may propose a session, first-time speakers welcome. The organiser reads every proposal.",
    "Supporters: companies can support GoatConf online for 500 EUR plus VAT where it applies (logo and link on the site, one social post, a mention in attendee emails; nothing at the venue), invoiced by the organiser's Austrian business, or pay a supplier directly. A host who funds and organises an accepted event is listed as a supporter too, if they agree. Speakers pay their own travel and stay; money from supporters that the event does not need goes first to refunding speakers who pay their own way, after the event, never promised.",
    "Recording: GoatConf aims to record the sessions in the two big halls of IPI Academy, the main hall and the first-floor hall; this is not promised yet, as it depends on the available budget. People may also bring a camera or a podcast, and a supporter may pay for a crew.",
]
# The pages an agent most likely needs first, in this order; the rest follow.
FIRST = ["index.html", "program.html", "register.html", "talk.html", "travel.html", "speakers.html",
         "add.html", "supporters.html", "extensions.html", "charter.html",
         "code-of-conduct.html", "access.html", "contact.html", "brand.html"]
START, END = "<!-- event data -->", "<!-- /event data -->"


def url(name: str) -> str:
    """The public address: pages without .html (GitHub Pages serves both), other files as they are."""
    if name == "index.html":
        return BASE
    return BASE + (name[:-5] if name.endswith(".html") else name)


def pages() -> list[Path]:
    found = {p.name: p for p in SITE.glob("*.html") if not p.name.startswith("_")}
    return [found[n] for n in FIRST if n in found] + sorted((p for n, p in found.items() if n not in FIRST), key=lambda p: p.name)


def head_text(page: Path) -> tuple[str, str]:
    text = page.read_text(encoding="utf-8")
    title = re.search(r"<title>(.*?)</title>", text, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
    return (html.unescape(title.group(1).strip()) if title else page.stem,
            html.unescape(desc.group(1).strip()) if desc else "")


def iso(day: dt.date, hhmm: str) -> str:
    return f"{day.isoformat()}T{hhmm}:00{OFFSET}"


def plus_hour(hhmm: str) -> str:
    h, m = map(int, hhmm.split(":"))
    return f"{h + 1:02d}:{m:02d}"


def session_list() -> list[dict]:
    table, _ = program.sessions()
    names = program.speaker_names()
    published = speakers.speakers()
    out = []
    for (day, start, room), (meta, body) in sorted(table.items(), key=lambda kv: (kv[0][0], kv[0][1], list(program.ROOMS).index(kv[0][2]))):
        people = [{"name": names[s], "page": url(speakers.page_name(s)), **({"role": published[s][0]["role"]} if published[s][0].get("role") else {})}
                  for s in meta.get("profiles") or [] if s in names and s in published]
        named = {p["name"] for p in people}
        for name in re.split(r"\s*,\s*", str(meta.get("speakers") or "")):
            if name and name not in named:
                people.append({"name": name})
        out.append({"day": day.isoformat(), "start": start, "end": plus_hour(start), "room": program.ROOMS[room][0],
                    "format": program.FORMATS[meta["format"]], "title": meta["title"], "page": url(program.page_name(meta)),
                    "about": body.split("\n\n")[0].strip(), "speakers": people,
                    **({"signup": meta["signup"]} if meta.get("signup") else {})})
    return out


def event_list() -> list[dict]:
    out = []
    for start, slug, meta, body in extensions.accepted():
        end = extensions.as_datetime(meta["end"])
        out.append({"name": meta["name"], "page": url(extensions.page_name(slug)), "kind": meta["kind"], "host": meta["host"], "where": meta["location"],
                    "start": start.strftime("%Y-%m-%dT%H:%M:00") + OFFSET, "end": end.strftime("%Y-%m-%dT%H:%M:00") + OFFSET,
                    "cost": meta["cost"], "registration": meta["registration"], "about": body.split("\n\n")[0].strip(),
                    "note": "Part of GoatConf 2027, accepted by the organiser and run by its host."})
    return sorted(out, key=lambda e: e["start"])


def days() -> list[dict]:
    out = []
    for day, plan in program.DAY_PLAN.items():
        out.append({"date": day.isoformat(), "name": program.CORE_DAYS[day], "welcome": plan["welcome"], "end": plan["end"],
                    "slots": list(plan["slots"]), "after_each_slot": {s: plan["breaks"][s] for s in plan["slots"] if s in plan["breaks"]},
                    "note": plan["note"]})
    out.append({"date": program.COMMUNITY_DAY[0].isoformat(), "name": program.COMMUNITY_DAY[1],
                "note": "No talks. The community's day: the organiser's lake day and goat hunt, plus events people add."})
    return out


def program_json() -> str:
    data = {
        "name": EVENT["name"], "url": BASE, "summary": EVENT["summary"], "timezone": "Europe/Sarajevo",
        "venue": {"name": EVENT["venue"], "address": f'{EVENT["street"]}, {EVENT["postcode"]} {EVENT["city"]}, Bosnia and Herzegovina',
                  "lat": EVENT["lat"], "lon": EVENT["lon"]},
        "register": LUMA, "propose_a_session": url("talk.html"),
        "days": days(),
        "rooms": [{"name": name, "seats": seats} for name, seats in program.ROOMS.values()],
        "sessions": session_list(),
        "events": event_list(),
    }
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def json_ld() -> str:
    first = min(program.DAY_PLAN)
    place = {"@type": "Place", "name": EVENT["venue"],
             "address": {"@type": "PostalAddress", "streetAddress": EVENT["street"], "postalCode": EVENT["postcode"],
                         "addressLocality": EVENT["city"], "addressCountry": EVENT["country"]},
             "geo": {"@type": "GeoCoordinates", "latitude": EVENT["lat"], "longitude": EVENT["lon"]}}
    data = {
        "@context": "https://schema.org", "@type": "Event", "name": EVENT["name"], "url": BASE,
        "description": EVENT["summary"] + " One-hour talks, panels and workshops in every room of IPI Academy, then a day for the community.",
        "startDate": iso(first, program.DAY_PLAN[first]["welcome"]),
        "endDate": program.COMMUNITY_DAY[0].isoformat(),
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "isAccessibleForFree": True,
        "image": ["https://goatconf.com/share/og.png"],
        "location": place,
        "organizer": {"@type": "Person", "name": EVENT["organiser"][0], "url": EVENT["organiser"][1], "email": EVENT["email"]},
        "offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "url": LUMA},
        "sameAs": [url for _, url, _ in nav.SOCIAL],
    }
    subs = [{"@type": "Event", "name": s["title"], "startDate": f'{s["day"]}T{s["start"]}:00{OFFSET}',
             "endDate": f'{s["day"]}T{s["end"]}:00{OFFSET}', "location": {"@type": "Place", "name": f'{s["room"]}, {EVENT["venue"]}'},
             **({"offers": {"@type": "Offer", "price": 0, "priceCurrency": "EUR", "url": s["signup"]}} if "signup" in s else {}),
             **({"performer": [{"@type": "Person", "name": p["name"], **({"url": p["page"]} if "page" in p else {}), **({"jobTitle": p["role"]} if "role" in p else {})} for p in s["speakers"]]}
                if s["speakers"] else {})} for s in session_list()]
    if subs:
        data["subEvent"] = subs
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'{START}\n<script type="application/ld+json">{body}</script>\n{END}\n'


def fold(line: str) -> str:
    raw, out = line.encode("utf-8"), []
    while len(raw) > 75:
        cut = 75 if not out else 74
        while (raw[cut] & 0xC0) == 0x80:
            cut -= 1
        out.append(raw[:cut].decode("utf-8"))
        raw = raw[cut:]
    out.append(raw.decode("utf-8"))
    return "\r\n ".join(out)


def ics_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def calendar() -> str:
    where = ics_text(f'{EVENT["venue"]}, {EVENT["street"]}, {EVENT["postcode"]} {EVENT["city"]}, Bosnia and Herzegovina')
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//GoatConf//goatconf.com//EN", "CALSCALE:GREGORIAN",
             "X-WR-CALNAME:GoatConf 2027",
             "BEGIN:VTIMEZONE", "TZID:Europe/Sarajevo",
             "BEGIN:DAYLIGHT", "TZOFFSETFROM:+0100", "TZOFFSETTO:+0200", "TZNAME:CEST", "DTSTART:19700329T020000",
             "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU", "END:DAYLIGHT",
             "BEGIN:STANDARD", "TZOFFSETFROM:+0200", "TZOFFSETTO:+0100", "TZNAME:CET", "DTSTART:19701025T030000",
             "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU", "END:STANDARD", "END:VTIMEZONE"]
    for day, plan in program.DAY_PLAN.items():
        stamp = day.strftime("%Y%m%d")
        lines += ["BEGIN:VEVENT", f"UID:{day.isoformat()}@goatconf.com", f"DTSTAMP:{STAMP}",
                  f"DTSTART;TZID=Europe/Sarajevo:{stamp}T{plan['welcome'].replace(':', '')}00",
                  f"DTEND;TZID=Europe/Sarajevo:{stamp}T{plan['end'].replace(':', '')}00",
                  f"SUMMARY:GoatConf 2027: {program.CORE_DAYS[day]}", f"LOCATION:{where}",
                  f"DESCRIPTION:{ics_text(plan['note'] + ' The program: ' + url('program.html'))}",
                  f"URL:{url('program.html')}", "END:VEVENT"]
    sat = program.COMMUNITY_DAY[0]
    lines += ["BEGIN:VEVENT", f"UID:{sat.isoformat()}@goatconf.com", f"DTSTAMP:{STAMP}",
              f"DTSTART;VALUE=DATE:{sat.strftime('%Y%m%d')}", f"DTEND;VALUE=DATE:{(sat + dt.timedelta(days=1)).strftime('%Y%m%d')}",
              "SUMMARY:GoatConf 2027: the community day", "LOCATION:Tuzla\\, Bosnia and Herzegovina",
              f"DESCRIPTION:{ics_text('No talks. The organiser\'s lake day and goat hunt, plus events people add, such as walks and meetups. ' + url('program.html') + '#' + sat.isoformat())}",
              f"URL:{url('program.html')}", "END:VEVENT", "END:VCALENDAR"]
    return "".join(fold(line) + "\r\n" for line in lines)


def llms() -> str:
    lines = [f"# {EVENT['name']}", "", f"> {EVENT['summary']} One-hour sessions in every room of IPI Academy, long breaks in town, and a day for the community.", ""]
    lines += [f"- {f}" for f in FACTS]
    lines += ["", f"Register: {LUMA}", f"Propose a session: {url('talk.html')}", f"Contact: {EVENT['email']}, or the form at {url('contact.html')}",
              "Follow GoatConf: " + ", ".join(f"{name} {link}" for name, link, _ in nav.SOCIAL), ""]
    people = speakers.listed(speakers.speakers())
    if people:
        lines += ["## Speakers", ""]
        lines += [f"- [{m['name']}]({url(speakers.page_name(s))})" + (f": {m['role']}" if m.get("role") else "") for s, (m, _) in people]
        lines.append("")
    backers = speakers.listed_supporters(speakers.supporters())
    if backers:
        lines += ["## Supporters", ""]
        lines += [f"- [{m['name']}]({url(speakers.supporter_page_name(s))}): {m['funds']}" for s, (m, _) in backers]
        lines.append("")
    table, _ = program.sessions()
    if table:
        lines += ["## Sessions", ""]
        lines += [f"- [{m['title']}]({url(program.page_name(m))}): {program.FORMATS[m['format']]} by {m['speakers']}, {program.CORE_DAYS[d]} at {t}, {program.ROOMS[r][0]}"
                  for (d, t, r), (m, _) in sorted(table.items(), key=lambda kv: (kv[0][0], kv[0][1], list(program.ROOMS).index(kv[0][2])))]
        lines.append("")
    events = extensions.accepted()
    if events:
        lines += ["## Events people add", ""]
        lines += [f"- [{m['name']}]({url(extensions.page_name(s))}): {extensions.KINDS[m['kind']]}, {extensions.when(m)}, run by {m['host']}" for _, s, m, _ in events]
        lines.append("")
    lines += ["## Pages", ""]
    for page in pages():
        if page.name.startswith(("speaker-", "supporter-", "event-", "session-")):
            continue
        title, desc = head_text(page)
        lines.append(f"- [{title}]({url(page.name)})" + (f": {desc}" if desc else ""))
    lines += ["", "## Data", "",
              f"- [The program as JSON]({url('program.json')}): every day, room, session and event, with times in Central European Summer Time.",
              f"- [The days for a calendar]({url('goatconf-2027.ics')}): Thursday, Friday and Saturday as calendar events.",
              "", "## Optional", "",
              f"- [Sitemap]({url('sitemap.xml')})",
              "- [The source and the records behind this site](https://github.com/misabegovic/goatconf)", ""]
    return "\n".join(lines)


def sitemap() -> str:
    rows = "".join(f"  <url><loc>{html.escape(url(p.name))}</loc></url>\n" for p in pages())
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n'


def robots() -> str:
    return f"# Everyone, people and agents, may read every page.\n# A short guide for AI agents: {url('llms.txt')}\nUser-agent: *\nAllow: /\n\nSitemap: {url('sitemap.xml')}\n"


def with_json_ld(text: str) -> str:
    block = json_ld()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text, count=1)
    return text.replace("</head>", block + "</head>", 1)


def outputs() -> dict[Path, str]:
    index = SITE / "index.html"
    return {SITE / "llms.txt": llms(), SITE / "program.json": program_json(), SITE / "goatconf-2027.ics": calendar(),
            SITE / "sitemap.xml": sitemap(), SITE / "robots.txt": robots(),
            index: with_json_ld(index.read_text(encoding="utf-8"))}


def cmd_build(args) -> int:
    stale = 0
    for path, want in outputs().items():
        have = path.read_bytes().decode("utf-8") if path.exists() else ""
        if args.check:
            if have != want:
                print(f"site/{path.name} is out of date: run python3 tools/agents.py build")
                stale += 1
            else:
                print(f"site/{path.name} is current")
        elif have != want:
            path.write_bytes(want.encode("utf-8"))
            print(f"wrote site/{path.name}")
    return 1 if stale else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="write the files, or check they are current")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    return cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
