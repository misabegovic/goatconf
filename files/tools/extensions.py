#!/usr/bin/env python3
"""Extension records: check them, and build the site's extensions page.

An extension is one Markdown file with YAML frontmatter under extensions/
(ADR wiki/org/adrs/extension-slots-and-the-record.md). The frontmatter is
the record; the body is the host's own description. README.md and files
whose names start with "_" are not records.

  check [files...]   check every record (or the named ones) and print one
                     summary per record, the text the agent posts on an
                     extension pull request. Exit 1 if any record fails.
  build [--check]    write site/extensions.html and a page for each accepted
                     event (site/event-<record>.html) from the records; with
                     --check, fail if a committed page is not current.

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
import images  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "extensions"
PAGE = ROOT / "site" / "extensions.html"
SHELL = ROOT / "site" / "contact.html"

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
    return (f'<li><a class="sticker sticker--fact sticker--example" href="{page_name(slug)}" data-peel style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">'
            f'<span class="num">{n}</span><small class="sticker__kind">{KINDS[meta["kind"]]}</small><strong>{html.escape(str(meta["name"]))}</strong>'
            f'<small>{when(meta)}. Run by {html.escape(str(meta["host"]))}.</small></a></li>')


FOOTER = """<footer class="footer">
  <p>GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3–5 June 2027. Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.</p>
  <p class="footer__links"><a href="index.html">Home</a> <a href="program.html">Program</a> <a href="speakers.html">Speakers</a> <a href="talk.html">Propose a session</a> <a href="add.html">Propose an event</a> <a href="extensions.html">Events people add</a> <a href="register.html">Register</a> <a href="travel.html">Travel</a> <a href="supporters.html">Supporters</a> <a href="charter.html">Charter</a> <a href="code-of-conduct.html">Code of conduct</a> <a href="brand.html">Brand</a> <a href="access.html">Accessibility</a> <a href="contact.html">Contact</a></p>
</footer>"""
OLD_TOWN = ("img/city-old-town-aerial-paving.jpg", 1375, 696, "The old town from above: tiled roofs and a street paved in a red and blue mosaic")
MORE = "More than one of each is welcome: a second meetup, another hike, a dinner every night."


def shell(name: str, title: str, description: str, photo, h1: str, lede: str, main: str, made_by: str, preview: str = "", photo_class: str = "") -> str:
    """A page of the site around its main part; the events page, each event's page and each session's page use it."""
    sprite = SHELL.read_text(encoding="utf-8")
    sprite = sprite[sprite.index('<svg width="0"'):sprite.index("</svg>", sprite.index('<svg width="0"')) + 6]
    src, width, height, alt = photo
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0b3d91">
<link rel="canonical" href="https://goatconf.com/{name[:-5]}">{f"""
<link rel="image_src" href="https://goatconf.com/share/{preview}">""" if preview else ""}
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="goatconf.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver"in window)document.documentElement.classList.add("js-peel")</script>
</head>
<body>
<!-- Generated by {made_by}. Edit the records, not this page. -->
{sprite}
<main id="main">
<div class="page-head">
  <img class="page-head__photo{photo_class}" src="{src}" width="{width}" height="{height}" alt="{alt}" decoding="async">
  <h1 class="sign">{h1}</h1>
  <p class="lede">{lede}</p>
</div>
{main}
</main>
{FOOTER}
<script src="album.js" defer></script>
</body>
</html>
"""


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
  <p class="copy"><a class="go go--ink" href="extensions.html">All events people add</a> <a class="go go--ink" href="program.html#{day}">The program for that day</a>{to_profile}</p>
</section>{share_section(cards(slug), f"The card for {e('name')}", "For the host and anyone going: post it wherever you like. It links back to this page.")}"""
    names = cards(slug)
    preview = names["preview"] if (PAGE.parent / "share" / names["preview"]).exists() else ""
    return shell(page_name(slug), f"{e('name')}: part of GoatConf 2027, Tuzla", f"{kind}: {when(meta)}, {e('location')}.",
                 OLD_TOWN, e("name"), f"{kind}. {when(meta)}.", main, "files/tools/extensions.py build from files/extensions/*.md", preview)


def share_section(names: dict, alt: str, note: str, heading: str = "Cards to share", site=None) -> str:
    """The wide card to look at, with both sizes to download; nothing until the cards are rendered."""
    if not all(((site or PAGE.parent) / "share" / names[k]).exists() for k in ("square", "wide")):
        return ""
    return f"""
<section class="album-page wrap" aria-labelledby="h-cards-{names['wide'][:-9]}">
  <h2 class="band" id="h-cards-{names['wide'][:-9]}">{heading}</h2>
  <p class="copy copy--wide">{note}</p>
  <img class="share-card" src="share/{names['wide']}" width="1200" height="675" alt="{alt}" loading="lazy">
  <p class="copy"><a class="go go--ink" href="share/{names['square']}" download>Download the square card</a> <a class="go go--ink" href="share/{names['wide']}" download>Download the wide card</a></p>
</section>"""


def page() -> str:
    good = accepted()
    if good:
        cards = "\n".join("  " + card(i + 1, s, m) for i, (_, s, m, _b) in enumerate(good))
        cards += (f'\n  <li><a class="slot slot--link slot--open" href="add.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg>'
                  f'<span class="num num--printed">{len(good) + 1}</span><strong>Yours next?</strong><small>{MORE}</small><span class="stamp">Yours?</span></a></li>')
        listings = f'<ul class="slots slots--events">\n{cards}\n</ul>'
    else:
        listings = """<div class="ledger-empty">
  <p><strong>No events yet.</strong> The first one could be yours: a workshop, a meetup, a dinner, a city walk, a hike, a corner for your community.</p>
</div>"""
    main = f"""<section class="album-page wrap" aria-labelledby="h-events">
  <h2 class="band" id="h-events">Accepted so far</h2>
  <p class="copy copy--wide">Every event here is part of GoatConf 2027: we accepted it, and it follows the <a href="charter.html">charter</a> and the <a href="code-of-conduct.html">code of conduct</a>. Each host runs their own event and pays for it directly. Open one to see when and where, and how to join. Not everything people propose is accepted, and events that are not accepted are not GoatConf's.</p>
  {listings}
</section>
<section class="album-page wrap" aria-labelledby="h-yours">
  <h2 class="band" id="h-yours">Propose yours</h2>
  <p class="copy copy--wide">{MORE} Propose it through the short form, and we decide whether it becomes part of GoatConf.</p>
  <p class="copy"><a class="go go--ink" href="add.html">Propose an event</a></p>
</section>"""
    return shell("extensions.html", "Events people add: GoatConf 2027",
                 "Workshops, meetups, hackathons, walks and more that the organiser has accepted as part of GoatConf 2027 in Tuzla, each run by its host.",
                 OLD_TOWN, "Events people add",
                 "Workshops, meetups, hackathons and events around the talk days, accepted as part of GoatConf 2027 and run by their hosts.",
                 main, "files/tools/extensions.py build from files/extensions/*.md")


def all_pages() -> dict:
    out = {PAGE: nav.place(meta.tag(page()), "extensions.html")}
    for _, slug, m, body in accepted():
        out[PAGE.parent / page_name(slug)] = nav.place(meta.tag(event_page(slug, m, body)), nav.section(page_name(slug)))
    return out


def cmd_build(args) -> int:
    pages = all_pages()
    stale = 0
    if args.check:
        for _, slug, _, _ in accepted():
            for name in cards(slug).values():
                if not (PAGE.parent / "share" / name).exists():
                    print(f"site/share/{name} is missing: run python3 tools/shareables.py render --only event-{slug}")
                    stale += 1
    for old in PAGE.parent.glob("event-*.html"):
        if old not in pages:
            if args.check:
                print(f"site/{old.name} belongs to no accepted event: run python3 tools/extensions.py build")
                stale += 1
            else:
                old.unlink()
                print(f"removed site/{old.name}")
    for path, want in pages.items():
        want = images.wrap(want)
        if args.check:
            have = path.read_text(encoding="utf-8") if path.exists() else ""
            if have != want:
                print(f"site/{path.name} is out of date: run python3 tools/extensions.py build")
                stale += 1
            else:
                print(f"site/{path.name} is current")
        else:
            path.write_text(want, encoding="utf-8")
            print(f"wrote site/{path.name}")
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
