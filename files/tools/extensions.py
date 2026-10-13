#!/usr/bin/env python3
"""Extension records: check them, and build the site's extensions page.

An extension is one Markdown file with YAML frontmatter under extensions/
(ADR wiki/org/adrs/extension-slots-and-the-record.md). The frontmatter is
the record; the body is the host's own description. README.md and files
whose names start with "_" are not records.

  check [files...]   check every record (or the named ones) and print one
                     summary per record, the text the agent posts on an
                     extension pull request. Exit 1 if any record fails.
  build [--check]    write site/extensions.html from the records; with
                     --check, fail if the committed page is not current.

Usage: python3 tools/extensions.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import meta  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "extensions"
PAGE = ROOT / "site" / "extensions.html"
SHELL = ROOT / "site" / "contact.html"

KINDS = {
    "fringe-event": "Fringe event",
    "workshop": "Workshop",
    "hub": "Community hub",
    "activity": "Activity",
    "venue": "Another venue",
    "support": "Support",
    "hiring": "Hiring",
    "hackathon": "Hackathon",
}
FIELDS = ("name", "kind", "host", "location", "start", "end", "cost", "registration", "paid_by", "contact", "accepts")
# GoatConf runs 3–5 June 2027; the window leaves room for arrivals, trips
# and the weeks around it. Outside it, a record must say why.
WINDOW = (dt.date(2027, 5, 25), dt.date(2027, 6, 20))
NOT_OURS = re.compile(r"goatconf\s+(presents|proudly)", re.I)


def records(paths=None):
    if paths:
        return [Path(p) for p in paths]
    if not RECORDS.is_dir():
        return []
    return sorted(p for p in RECORDS.glob("*.md") if p.name != "README.md" and not p.name.startswith("_"))


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text, ["no frontmatter block"]
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as err:
        return None, m.group(2), [f"frontmatter is not valid YAML ({err.__class__.__name__})"]
    return meta, m.group(2).strip(), []


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
    if start and not (WINDOW[0] <= start.date() <= WINDOW[1]):
        if meta.get("outside_week_reason"):
            notes.append(f"outside the GoatConf week, with a reason: {meta['outside_week_reason']}")
        else:
            problems.append("dates fall outside the GoatConf week and no outside_week_reason is given")
    if kind == "support" and not meta.get("supplier"):
        problems.append("a support record names the supplier the supporter pays (field: supplier)")
    if not body:
        problems.append("no description below the frontmatter")
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
        return 0
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
    return 1 if failed else 0


def when(meta):
    start, end = as_datetime(meta["start"]), as_datetime(meta["end"])
    day = start.strftime("%-d %B %Y")
    if start.time() == dt.time() and end.time() == dt.time():
        return day if start.date() == end.date() else f"{day} to {end.strftime('%-d %B %Y')}"
    span = f"{start.strftime('%H:%M')} to {end.strftime('%H:%M')}"
    return f"{day}, {span}" if start.date() == end.date() else f"{day} {start.strftime('%H:%M')} to {end.strftime('%-d %B %H:%M')}"


def link(value):
    v = html.escape(str(value))
    return f'<a href="{v}">{v}</a>' if re.match(r"^https?://", str(value)) else v


def listing(meta, body):
    e = lambda k: html.escape(str(meta[k]))
    para = "".join(f"<p>{html.escape(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    return f"""  <li class="listing">
    <h2>{e('name')}</h2>
    <p class="listing__kind">{KINDS[meta['kind']]}, part of GoatConf 2027, run by {e('host')}</p>
    <dl class="facts">
      <dt>When</dt><dd>{when(meta)}</dd>
      <dt>Where</dt><dd>{e('location')}</dd>
      <dt>Cost</dt><dd>{e('cost')}</dd>
      <dt>Register</dt><dd>{link(meta['registration'])}</dd>
      <dt>Paid by</dt><dd>{e('paid_by')}</dd>
      <dt>Contact</dt><dd>{link(meta['contact'])}</dd>
    </dl>
    {para}
  </li>"""


def page() -> str:
    good = []
    for path in records():
        problems, _, meta = check_record(path)
        if not problems and listed(meta):
            _, body, _ = parse(path)
            good.append((as_datetime(meta["start"]), meta, body))
    good.sort(key=lambda g: (g[0], str(g[1]["name"])))
    if good:
        main = '<ol class="listings">\n' + "\n".join(listing(m, b) for _, m, b in good) + "\n</ol>"
    else:
        main = """<div class="ledger-empty">
  <p><strong>No events yet.</strong> The first one could be yours: a workshop, a meetup, a dinner, a city walk, a hike, a corner for your community.</p>
</div>"""
    shell = SHELL.read_text(encoding="utf-8")
    sprite = shell[shell.index('<svg width="0"'):shell.index("</svg>", shell.index('<svg width="0"')) + 6]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Events people add: GoatConf 2027</title>
<meta name="description" content="Workshops, meetups, hackathons, walks and more that the organiser has accepted as part of GoatConf 2027 in Tuzla, each run by its host.">
<meta name="theme-color" content="#0b3d91">
<link rel="canonical" href="https://goatconf.com/extensions">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="goatconf.css">
</head>
<body>
<!-- Generated by files/tools/extensions.py build from files/extensions/*.md. Edit the records, not this page. -->
{sprite}
<header class="page-head">
  <img class="page-head__photo" src="img/city-old-town-aerial-paving.jpg" width="1375" height="696" alt="The old town from above: tiled roofs and a street paved in a red and blue mosaic" decoding="async">
  <h1 class="sign">Added by the people who come</h1>
  <p class="lede">Workshops, meetups, hackathons and events around the talk days, accepted as part of GoatConf 2027 and run by their hosts.</p>
</header>
<main id="main" class="prose">
<p>Every event here is part of GoatConf 2027: the organiser accepted it, and it follows the <a href="charter.html">charter</a> and the <a href="code-of-conduct.html">code of conduct</a>. Each host runs their own event and pays for it directly. Not everything people propose is accepted, and events that are not accepted are not GoatConf's.</p>
{main}
<h2>Propose yours</h2>
<p>Propose it through the short form. The organiser decides whether it becomes part of GoatConf. <a href="add.html">Propose yours</a></p>
</main>
<footer class="footer">
  <p>GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3–5 June 2027. Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.</p>
  <p class="footer__links"><a href="index.html">Home</a> <a href="program.html">Program</a> <a href="speakers.html">Speakers</a> <a href="talk.html">Give a talk</a> <a href="add.html">Propose an event</a> <a href="register.html">Register</a> <a href="travel.html">Travel</a> <a href="supporters.html">Supporters</a> <a href="charter.html">Charter</a> <a href="code-of-conduct.html">Code of conduct</a> <a href="brand.html">Brand</a> <a href="access.html">Accessibility</a> <a href="contact.html">Contact</a></p>
</footer>
<script src="album.js" defer></script>
</body>
</html>
"""


def cmd_build(args) -> int:
    want = nav.place(meta.tag(page()), "extensions.html")
    if args.check:
        have = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        if have != want:
            print("site/extensions.html is out of date: run python3 tools/extensions.py build")
            return 1
        print("site/extensions.html is current")
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
