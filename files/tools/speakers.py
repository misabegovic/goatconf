#!/usr/bin/env python3
"""Speakers and supporters: check their records, and build the site's pages.

A speaker is one Markdown file with YAML frontmatter under speakers/, written
once their session is accepted and they agree to a public profile. A
supporter is one file under supporters/: a company that pays a named thing,
such as a speaker's travel, straight to the supplier. The body of each file is
their own words. README.md and files whose names start with "_" are not
records.

  check              check every speaker and supporter record. Exit 1 if any fails.
  build [--check]    write site/speakers.html and site/supporters.html; with
                     --check, fail if a committed page is not current.

Usage: python3 tools/speakers.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extensions  # noqa: E402
import program  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SPEAKERS = ROOT / "speakers"
SUPPORTERS = ROOT / "supporters"
PAGES = {"speakers": SITE / "speakers.html", "supporters": SITE / "supporters.html"}
URL = re.compile(r"^https?://\S+$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BIO_WORDS = 120
esc = program.esc


def records(folder: Path):
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if p.name != "README.md" and not p.name.startswith("_"))


def image_problem(value, folder: str, what: str):
    if not isinstance(value, str) or not value.startswith(f"img/{folder}/"):
        return f"{what} must be a path under site/img/{folder}/"
    if not (SITE / value).is_file():
        return f"{what} file not found: site/{value}"
    return None


def check_supporter(path: Path):
    meta, body, problems = extensions.parse(path)
    if meta is None:
        return problems, None, body
    if not SLUG.match(path.stem):
        problems.append("file name must be lowercase words joined by hyphens")
    for f in ("name", "logo", "url", "funds"):
        if not meta.get(f):
            problems.append(f"missing field: {f}")
    if meta.get("logo"):
        p = image_problem(meta["logo"], "supporters", "logo")
        if p:
            problems.append(p)
    if meta.get("url") and not URL.match(str(meta["url"])):
        problems.append("url must start with http:// or https://")
    return problems, meta, body


def supporters():
    out = {}
    for path in records(SUPPORTERS):
        problems, meta, body = check_supporter(path)
        if not problems:
            out[path.stem] = (meta, body)
    return out


def check_speaker(path: Path, known_supporters):
    meta, body, problems = extensions.parse(path)
    if meta is None:
        return problems, None, body
    if not SLUG.match(path.stem):
        problems.append("file name must be lowercase words joined by hyphens")
    if not meta.get("name"):
        problems.append("missing field: name")
    if meta.get("publish") is not True:
        problems.append("publish must be yes: the speaker agreed to this public profile")
    if not body:
        problems.append("no bio below the frontmatter")
    elif len(body.split()) > BIO_WORDS:
        problems.append(f"the bio is longer than {BIO_WORDS} words")
    if meta.get("photo"):
        p = image_problem(meta["photo"], "speakers", "photo")
        if p:
            problems.append(p)
    links = meta.get("links") or []
    if not isinstance(links, list) or any(not URL.match(str(u)) for u in links):
        problems.append("links must be a list of addresses starting with http:// or https://")
    funded = meta.get("travel_funded_by")
    if funded and funded not in known_supporters:
        problems.append(f"travel_funded_by '{funded}' is not a supporter record in supporters/")
    return problems, meta, body


def speakers():
    known = supporters()
    out = {}
    for path in records(SPEAKERS):
        problems, meta, body = check_speaker(path, known)
        if not problems:
            out[path.stem] = (meta, body)
    return out


def session_problems():
    """Program records that name a profile that is missing or not published."""
    known = speakers()
    problems = []
    for path in program.records():
        meta, _, _ = extensions.parse(path)
        for slug in (meta or {}).get("profiles") or []:
            if slug not in known:
                problems.append(f"{path.name}: profiles names '{slug}', which is not a published speaker record")
    return problems


def cmd_check(_args) -> int:
    known = supporters()
    failed = 0
    count = 0
    for path in records(SUPPORTERS):
        count += 1
        problems, meta, _ = check_supporter(path)
        print(f"supporters/{path.name}: {(meta or {}).get('name') or path.stem}")
        for p in problems:
            print(f"  needs a change: {p}")
        failed += bool(problems)
    for path in records(SPEAKERS):
        count += 1
        problems, meta, _ = check_speaker(path, known)
        print(f"speakers/{path.name}: {(meta or {}).get('name') or path.stem}")
        for p in problems:
            print(f"  needs a change: {p}")
        failed += bool(problems)
    linked = session_problems()
    for p in linked:
        print(f"program/{p}")
    print(f"speakers and supporters: {count} record(s), {failed} need a change, {len(linked)} broken profile link(s)")
    return 1 if failed or linked else 0


def page_name(slug: str) -> str:
    """Each speaker's own page, next to the other pages so relative links keep working."""
    return f"speaker-{slug}.html"


def sessions_by_speaker(detail=False):
    table, _ = program.sessions()
    out = {}
    for (day, start, room), (meta, body) in sorted(table.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        for slug in meta.get("profiles") or []:
            if detail:
                out.setdefault(slug, []).append({"day": day, "start": start, "room": program.ROOMS[room][0], "format": program.FORMATS[meta["format"]],
                                                 "title": meta["title"], "about": body.split("\n\n")[0].strip(), "luma": meta.get("luma")})
            else:
                out.setdefault(slug, []).append(f"{program.FORMATS[meta['format']]}, {program.CORE_DAYS[day]} at {start}, {program.ROOMS[room][0]}: {esc(meta['title'])}")
    return out


def goat_photo() -> str:
    return '<span class="speaker__goat" aria-hidden="true"><svg viewBox="0 0 124 100"><use href="#goat"/></svg></span>'


def speaker_card(n: int, slug: str, meta, body, sessions, known) -> str:
    photo = f'<img src="{esc(meta["photo"])}" alt="" loading="lazy">' if meta.get("photo") else goat_photo()
    first = f'<span class="speaker__first">{sessions[0]}</span>' if sessions else ""
    more = f'<span class="speaker__more">and {len(sessions) - 1} more</span>' if len(sessions) > 1 else ""
    travel = ""
    if meta.get("travel_funded_by"):
        s_meta, _ = known[meta["travel_funded_by"]]
        travel = f'<span class="speaker__travel"><img src="{esc(s_meta["logo"])}" alt=""><span>Travel funded by {esc(s_meta["name"])}</span></span>'
    return f"""  <li class="sticker sticker--speaker" id="{esc(slug)}" data-peel style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">
    <a class="speaker__link" href="{page_name(slug)}">
    <span class="num">{n}</span>
    <figure class="speaker__photo">{photo}<figcaption>{esc(meta['name'])}</figcaption></figure>
    <span class="speaker__body">{first}{more}{travel}</span>
    </a>
  </li>"""


def speaker_page(slug: str, meta, body, sessions, known) -> str:
    name = esc(meta["name"])
    bio = "".join(f"<p>{esc(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    talks = "\n".join(
        f'<li class="talk"><span class="talk__when"><a href="program.html#{s["day"].isoformat()}">{program.CORE_DAYS[s["day"]]}, {s["start"]}</a>'
        f'<span>{esc(s["format"])}, {esc(s["room"])}</span></span><strong>{esc(s["title"])}</strong><p>{esc(s["about"])}</p>'
        + (f'<a class="session__register" href="{esc(s["luma"])}">Register for this session</a>' if s.get("luma") else "") + '</li>' for s in sessions)
    links = "".join(f'<li><a href="{esc(u)}">{esc(re.sub(r"^https?://(www\.)?", "", str(u)).rstrip("/"))}</a></li>' for u in meta.get("links") or [])
    travel = ""
    if meta.get("travel_funded_by"):
        s_slug = meta["travel_funded_by"]
        s_meta, _ = known[s_slug]
        travel = (f'<p class="speaker-page__travel"><a href="supporters.html#{esc(s_slug)}"><img src="{esc(s_meta["logo"])}" alt="">'
                  f'<span>{name.split()[0]}\'s travel is funded by {esc(s_meta["name"])}.</span></a></p>')
    card = SITE / "share" / f"speaker-{slug}-square.png"
    share = (f'<p><a class="go go--ink" href="share/speaker-{esc(slug)}-square.png" download>Download the "I\'m speaking" card</a></p>'
             if card.exists() else "")
    photo = (esc(meta["photo"]), 800, 800, meta["name"]) if meta.get("photo") else ("brand/coin.svg", 300, 300, "")
    first = sessions[0] if sessions else None
    lede = (f'{esc(first["format"])} on {program.CORE_DAYS[first["day"]]} at {first["start"]}, {esc(first["room"])}.' if first
            else "Speaking at GoatConf 2027 in Tuzla.")
    main = f"""<section class="album-page wrap speaker-page" aria-labelledby="h-about">
  <h2 class="band" id="h-about">About {name.split()[0]}</h2>
  <div class="copy copy--wide">{bio}</div>
  {f'<ul class="speaker-page__links">{links}</ul>' if links else ''}
  {travel}
</section>
<section class="album-page wrap" aria-labelledby="h-talks">
  <h2 class="band" id="h-talks">{"Sessions" if len(sessions) > 1 else "Session"}</h2>
  {f'<ul class="talks">{talks}</ul>' if talks else '<p class="copy">The session will be on the program soon.</p>'}
  <p class="copy"><a class="go go--ink" href="program.html">See the whole program</a> <a class="go go--ink" href="speakers.html">All speakers</a></p>
  {share}
</section>"""
    title = f"{meta['name']}: speaking at GoatConf 2027, Tuzla"
    desc = f"{meta['name']} speaks at GoatConf 2027 in Tuzla, 3 to 5 June 2027: " + (esc(first["title"]) if first else "a session at IPI Academy") + "."
    return shell(page_name(slug)[:-5], esc(title), desc, photo, name, lede, main)


def supporter_card(n: int, slug: str, meta, body, funded_speakers) -> str:
    words = "".join(f"<p>{esc(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    names = ", ".join(f'<a href="{page_name(s)}">{esc(m["name"])}</a>' for s, m in funded_speakers)
    return f"""  <li class="sticker sticker--supporter" id="{esc(slug)}" data-peel style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">
    <span class="num">{n}</span>
    <a class="supporter__logo" href="{esc(meta['url'])}"><img src="{esc(meta['logo'])}" alt="{esc(meta['name'])}" loading="lazy"></a>
    <strong>{esc(meta['name'])}</strong>
    <p class="supporter__funds">Funds: {esc(meta['funds'])}</p>{f'<p class="supporter__funds">Travel for {names}.</p>' if names else ''}{words}
  </li>"""


def shell(slug: str, title: str, description: str, photo: str, h1: str, lede: str, main: str) -> str:
    sprite = extensions.SHELL.read_text(encoding="utf-8")
    sprite = sprite[sprite.index('<svg width="0"'):sprite.index("</svg>", sprite.index('<svg width="0"')) + 6]
    src, width, height, alt = photo
    mark = " page-head__photo--mark" if src.startswith("brand/") else (" page-head__photo--portrait" if src.startswith("img/speakers/") else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0b3d91">
<link rel="canonical" href="https://goatconf.com/{slug}.html">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="goatconf.css">
<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver"in window)document.documentElement.classList.add("js-peel")</script>
</head>
<body>
<!-- Generated by files/tools/speakers.py build from files/speakers/*.md and files/supporters/*.md. Edit the records, not this page. -->
{sprite}
<header class="page-head">
  <img class="page-head__photo{mark}" src="{src}" width="{width}" height="{height}" alt="{alt}" decoding="async">
  <h1 class="sign">{h1}</h1>
  <p class="lede">{lede}</p>
</header>
<main id="main">
{main}
</main>
<footer class="footer">
  <p>GoatConf 2027, a free conference in Tuzla, Bosnia and Herzegovina, 3 to 5 June 2027. Organised by <a href="https://muhamed.at">Muhamed Isabegović</a>, with IPI Academy as host and partner.</p>
  <p class="footer__links">{FOOTER_LINKS}</p>
</footer>
<script src="album.js" defer></script>
</body>
</html>
"""


FOOTER_LINKS = ('<a href="index.html">Home</a> <a href="program.html">Program</a> <a href="speakers.html">Speakers</a> '
                '<a href="talk.html">Give a talk</a> <a href="add.html">Add something</a> <a href="register.html">Register</a> '
                '<a href="travel.html">Travel</a> <a href="supporters.html">Supporters</a> <a href="budget.html">Budget</a> '
                '<a href="charter.html">Charter</a> <a href="code-of-conduct.html">Code of conduct</a> <a href="brand.html">Brand</a> <a href="contact.html">Contact</a>')


def speakers_page() -> str:
    known = supporters()
    people = speakers()
    talks = sessions_by_speaker()
    order = sorted(people.items(), key=lambda kv: str(kv[1][0]["name"]).lower())
    if order:
        cards = '<ul class="slots slots--speakers">\n' + "\n".join(
            speaker_card(i + 1, slug, m, b, talks.get(slug, []), known) for i, (slug, (m, b)) in enumerate(order)) + "\n</ul>"
    else:
        cards = """<ul class="slots slots--speakers">
  <li><a class="slot slot--link" href="talk.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg><span class="num num--printed">1</span><strong>The first speaker</strong><small>No speakers yet: the call is open and every one-hour slot is waiting. Propose a session.</small><span class="stamp">Yours?</span></a></li>
</ul>"""
    main = f"""<section class="album-page wrap" aria-labelledby="h-speakers">
  <h2 class="band" id="h-speakers">Who is speaking</h2>
  <p class="copy copy--wide">Each speaker here has a session on Thursday 3 or Friday 4 June 2027. They chose to have a profile, and wrote it themselves. Each session is on the <a href="program.html">program</a> with its day, time and room.</p>
  {cards}
</section>
<section class="album-page wrap" aria-labelledby="h-travel">
  <h2 class="band" id="h-travel">Getting speakers here</h2>
  <p class="copy copy--wide">Speakers pay their own travel unless a supporter covers it. A supporter pays the airline or hotel directly. The speaker's profile then says who paid, and the payment is listed in the <a href="budget.html">public budget</a>. See the <a href="supporters.html">supporters</a>, or <a class="go go--ink" href="add.html">fund a speaker's travel</a>.</p>
</section>"""
    return shell("speakers", "Speakers: GoatConf 2027, 3 to 5 June, Tuzla",
                 "The speakers at GoatConf 2027 in Tuzla: their sessions, in their own words, and who funded their travel.",
                 ("img/ipi-lecture-hall.jpg", 1024, 768, "A talk in IPI Academy's lecture hall, students' faces blurred"),
                 "The speakers", "The people giving the talks, panels and workshops, in their own words.", main)


def supporters_page() -> str:
    known = supporters()
    people = speakers()
    order = sorted(known.items(), key=lambda kv: str(kv[1][0]["name"]).lower())
    if order:
        cards = '<ul class="slots slots--supporters">\n' + "\n".join(
            supporter_card(i + 1, slug, m, b, sorted(((s, pm) for s, (pm, _) in people.items() if pm.get("travel_funded_by") == slug), key=lambda x: str(x[1]["name"]).lower()))
            for i, (slug, (m, b)) in enumerate(order)) + "\n</ul>"
    else:
        cards = """<ul class="slots slots--supporters">
  <li><a class="slot slot--link" href="add.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg><span class="num num--printed">1</span><strong>Your logo</strong><small>No supporters yet. Fund a speaker's travel and your logo goes here and on their profile.</small><span class="stamp">Yours?</span></a></li>
</ul>"""
    main = f"""<section class="album-page wrap" aria-labelledby="h-supporters">
  <h2 class="band" id="h-supporters">Who makes it possible</h2>
  <p class="copy copy--wide">GoatConf is free, and no money passes through the organiser. A supporter pays the supplier directly for one named thing: a speaker's flight or room, a round of coffee, the printing. We thank each supporter for exactly what they paid for. Every payment is listed in the <a href="budget.html">public budget</a>. Supporters cannot buy talks, stage time or the attendee list. See <a href="charter.html">the charter</a>.</p>
  {cards}
</section>
<section class="album-page wrap" aria-labelledby="h-become">
  <h2 class="band" id="h-become">Fund a speaker's travel</h2>
  <p class="copy copy--wide">Pick a speaker, or fund travel grants: tickets or rooms for speakers who ask for help. You pay the airline or hotel directly. Asking never affects whether a session is picked. Your logo shows on this page and on the profile of every speaker whose travel you covered. Tell us through the <a href="add.html">add-something form</a>. Choose Support.</p>
</section>"""
    return shell("supporters", "Supporters: GoatConf 2027, 3 to 5 June, Tuzla",
                 "The companies and people who make GoatConf 2027 possible, each thanked for exactly what they paid for, starting with speakers' travel.",
                 ("img/city-korzo-clock.jpg", 1160, 773, "The Korzo on a sunny day: the street clock, a pink corner house, café umbrellas and people walking"),
                 "The supporters", "Companies and people who pay a supplier directly for one named thing, such as a speaker's travel.", main)


def all_pages() -> dict:
    out = {PAGES["speakers"]: nav.place(meta.tag(speakers_page()), "speakers.html"),
           PAGES["supporters"]: nav.place(meta.tag(supporters_page()), "supporters.html")}
    known = supporters()
    detail = sessions_by_speaker(detail=True)
    for slug, (m, b) in speakers().items():
        name = page_name(slug)
        out[SITE / name] = nav.place(meta.tag(speaker_page(slug, m, b, detail.get(slug, []), known)), "speakers.html")
    return out


def cmd_build(args) -> int:
    pages = all_pages()
    stale = 0
    for old in SITE.glob("speaker-*.html"):
        if old not in pages:
            if args.check:
                print(f"site/{old.name} belongs to no speaker record: run python3 tools/speakers.py build")
                stale += 1
            else:
                old.unlink()
                print(f"removed site/{old.name}")
    for path, want in pages.items():
        if args.check:
            have = path.read_text(encoding="utf-8") if path.exists() else ""
            if have != want:
                print(f"site/{path.name} is out of date: run python3 tools/speakers.py build")
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
    sub.add_parser("check")
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    return cmd_check(args) if args.cmd == "check" else cmd_build(args)


if __name__ == "__main__":
    sys.exit(main())
