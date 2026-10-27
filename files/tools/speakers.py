#!/usr/bin/env python3
"""Speakers and supporters: check their records, and build the site's pages.

A speaker is one Markdown file with YAML frontmatter under speakers/, written
once they are confirmed and agree to a public profile, with or without a
session on the program yet. A supporter is one file under supporters/: a
company that pays a named thing, such as a speaker's travel, straight to the
supplier. The body of each file is their own words. README.md and files whose names start with "_" are not
records.

  check              check every speaker and supporter record. Exit 1 if any fails.
  build [--check]    write site/speakers.html, site/supporters.html, each
                     speaker's page (site/speaker-<record>.html) and each
                     supporter's profile (site/supporter-<record>.html), where
                     they download their cards; with --check, fail if a
                     committed page is not current or a card is missing.

Usage: python3 tools/speakers.py <check|build> [...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extensions  # noqa: E402
import images  # noqa: E402
import frame  # noqa: E402
import sitelib  # noqa: E402
import program  # noqa: E402
import meta  # noqa: E402
import nav  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SPEAKERS = ROOT / "speakers"
SUPPORTERS = ROOT / "supporters"
PAGES = {"speakers": SITE / "speakers.html", "supporters": SITE / "supporters.html"}
URL = re.compile(r"^https?://\S+$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BIO_WORDS = 120
ROLE_CHARS = 80
TALK_CHARS = 80
TALK_WORDS = 300
HOLD_CHARS = 80
# The session's format, area and who it is for, while it has no slot; the
# program record carries them as format, area and for once it has one.
TALK_EXTRAS = ("talk_format", "talk_format_name", "talk_area", "talk_for")
esc = program.esc


def records(folder: Path):
    return sitelib.records(folder)


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
    if "host" in meta and meta["host"] is not True:
        problems.append("host must be yes, or left out")
    if meta.get("logo_on", "light") not in ("light", "dark"):
        problems.append("logo_on must be light or dark: the background the logo is made for")
    if "logo_bg" in meta and not (isinstance(meta["logo_bg"], str) and HEX.match(meta["logo_bg"])):
        problems.append("logo_bg must be a colour written #RRGGBB, for example \"#E0FF6E\"")
    if "logo_bg" in meta and meta.get("logo_on") == "dark":
        problems.append("logo_bg and logo_on: dark both set the logo's background: keep one")
    problems += support_problems(meta)
    events = meta.get("events")
    if events is not None:
        known = {slug for _, slug, _, _ in extensions.accepted()}
        if not isinstance(events, list) or any(str(e) not in known for e in events):
            problems.append(f"events must list accepted events it hosts by their record names, from: {', '.join(sorted(known)) or 'none yet'}")
    return problems, meta, body


def supporters():
    out = {}
    for path in records(SUPPORTERS):
        problems, meta, body = check_supporter(path)
        if not problems:
            out[path.stem] = (meta, body)
    return out


def listed_supporters(known: dict) -> list:
    """The host and partner first, then every other supporter by name."""
    return sorted(known.items(), key=lambda kv: (kv[1][0].get("host") is not True, str(kv[1][0]["name"]).lower()))


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
    if "role" in meta and (not isinstance(meta["role"], str) or not meta["role"].strip() or "\n" in meta["role"] or len(meta["role"]) > ROLE_CHARS):
        problems.append(f"role must be one line of at most {ROLE_CHARS} characters, for example: Staff Engineer at Vinted")
    if "talk" in meta and (not isinstance(meta["talk"], str) or not meta["talk"].strip() or "\n" in meta["talk"] or len(meta["talk"]) > TALK_CHARS):
        problems.append(f"talk must be one line of at most {TALK_CHARS} characters: the proposed session's title")
    about = meta.get("talk_about")
    if about is not None:
        if not meta.get("talk"):
            problems.append("talk_about needs talk: the title of the session it describes")
        if not isinstance(about, str) or not about.strip():
            problems.append("talk_about must be the speaker's own words on the session")
        elif len(about.split()) > TALK_WORDS:
            problems.append(f"talk_about is longer than {TALK_WORDS} words")
    if meta.get("talk_format") is not None and meta["talk_format"] not in program.FORMATS:
        problems.append(f"talk_format must be one of: {', '.join(program.FORMATS)}")
    problems += program.flavor_problems(meta, "talk_area", "talk_for") + program.format_name_problems(meta, "talk_format", "talk_format_name")
    if not meta.get("talk") and any(meta.get(k) is not None for k in TALK_EXTRAS):
        problems.append(f"{', '.join(k for k in TALK_EXTRAS if meta.get(k) is not None)} need talk: the title of the session they describe")
    if "hold" in meta and (not isinstance(meta["hold"], str) or not meta["hold"].strip() or "\n" in meta["hold"] or len(meta["hold"]) > HOLD_CHARS):
        problems.append(f"hold must be one line of at most {HOLD_CHARS} characters: why the speaker stays off the site for now")
    problems += support_problems(meta)
    if meta.get("photo"):
        p = image_problem(meta["photo"], "speakers", "photo")
        if p:
            problems.append(p)
    links = meta.get("links") or []
    if not isinstance(links, list) or any(not URL.match(str(u)) for u in links):
        problems.append("links must be a list of addresses starting with http:// or https://")
    if "order" in meta and (type(meta["order"]) is not int or meta["order"] < 1):
        problems.append("order must be a whole number from 1, where 1 is listed first")
    if "travel_funded_by" in meta:
        problems.append("travel_funded_by is retired: no supporter pays for a named speaker's travel; remove it")
    return problems, meta, body


def speakers(include_held=False):
    """Valid records; a held one (a `hold` line) only when asked for: it is kept, but not listed."""
    known = supporters()
    out = {}
    for path in records(SPEAKERS):
        problems, meta, body = check_speaker(path, known)
        if problems or (meta.get("hold") and not include_held):
            continue
        out[path.stem] = (meta, body)
    return out


def listed(people: dict) -> list:
    """Speakers in the organiser's order: by `order` (1 first), then those without one, by name."""
    return sorted(people.items(), key=lambda kv: (kv[1][0].get("order") or float("inf"), str(kv[1][0]["name"]).lower()))


def order_problems():
    """Two speakers with the same order would leave the list's order to chance; a held speaker keeps their number."""
    seen = {}
    for slug, (meta, _) in speakers(include_held=True).items():
        if meta.get("order"):
            seen.setdefault(meta["order"], []).append(slug)
    return [f"order {n} is given to more than one speaker: {', '.join(slugs)}" for n, slugs in sorted(seen.items()) if len(slugs) > 1]


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


def talk_problems():
    """A speaker whose session reached the program keeps no copy of the talk: the program record is the source."""
    known = speakers()
    on_program = set()
    for path in program.records():
        meta, _, _ = extensions.parse(path)
        on_program.update((meta or {}).get("profiles") or [])
    return [f"{slug}: the session is on the program now, so remove talk, talk_about and the other talk_ fields from the speaker record"
            for slug in sorted(known) if slug in on_program and any(known[slug][0].get(k) for k in ("talk", "talk_about") + TALK_EXTRAS)]


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
        if not problems and (meta or {}).get("hold"):
            print(f"  note: held from the site, so not listed: {meta['hold']}")
        failed += bool(problems)
    linked = session_problems()
    for p in linked:
        print(f"program/{p}")
    clashes = order_problems()
    for p in clashes:
        print(f"speakers: {p}")
        failed += 1
    spent = talk_problems()
    for p in spent:
        print(f"speakers: {p}")
        failed += 1
    print(f"speakers and supporters: {count} record(s), {failed} need a change, {len(linked)} broken profile link(s)")
    return 1 if failed or linked else 0


def announce_cards(slug: str) -> dict:
    """GoatConf's "Confirmed speaker" cards announcing the speaker, made by tools/shareables.py."""
    return {"square": f"speaker-{slug}-announce-square.png", "wide": f"speaker-{slug}-announce-wide.png"}


def preview_name(slug: str) -> str:
    """The speaker's own link-preview card in site/share/, made by tools/shareables.py."""
    return f"speaker-{slug}-preview.png"


def page_name(slug: str) -> str:
    """Each speaker's own page, next to the other pages so relative links keep working."""
    return f"speaker-{slug}.html"


def sessions_by_speaker(detail=False):
    table, _ = program.sessions()
    out = {}
    for (day, start, room), (meta, body) in sorted(table.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        for slug in meta.get("profiles") or []:
            if detail:
                out.setdefault(slug, []).append({"day": day, "start": start, "room": program.ROOMS[room][0], "format": program.format_label(meta),
                                                 "title": meta["title"], "about": body.split("\n\n")[0].strip(), "signup": meta.get("signup"),
                                                 "area": meta.get("area"), "for": meta.get("for"),
                                                 "page": program.page_name(meta)})
            else:
                out.setdefault(slug, []).append(f"{esc(program.format_label(meta))}, {program.CORE_DAYS[day]} at {start}, {program.ROOMS[room][0]}: {esc(meta['title'])}")
    return out


def talk_format(meta) -> str:
    """The proposed session's format, a talk unless the record says otherwise, ready for the page."""
    return esc(program.format_label(meta, "talk_format", "talk_format_name"))


def goat_photo() -> str:
    return '<span class="speaker__goat" aria-hidden="true"><svg viewBox="0 0 124 100"><use href="#goat"/></svg></span>'


def speaker_card(n: int, slug: str, meta, body, sessions, known, scheduled=None, anchor=True) -> str:
    """One speaker's card, the same on the speakers page and the home page. `scheduled` is the first
    session on the program, with its area and who it is for; `anchor` gives the card the id the speakers page links to."""
    photo = f'<img src="{esc(meta["photo"])}" alt="" loading="lazy">' if meta.get("photo") else goat_photo()
    role = f'<span class="speaker__role">{esc(meta["role"])}</span>' if meta.get("role") else ""
    first = (f'<span class="speaker__first">{sessions[0]}</span>' if sessions
             else f'<span class="speaker__first">{talk_format(meta)}: {esc(meta["talk"])}</span>' if meta.get("talk")
             else '<span class="speaker__first speaker__first--tba">Session to be announced</span>')
    flavor = scheduled or ({"area": meta.get("talk_area"), "for": meta.get("talk_for")} if meta.get("talk") else {})
    first += program.tags(None, flavor.get("area")) + program.for_line(flavor.get("for"), "span")
    more = f'<span class="speaker__more">and {len(sessions) - 1} more</span>' if len(sessions) > 1 else ""
    return f"""  <li class="sticker sticker--speaker"{f' id="{esc(slug)}"' if anchor else ''} style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">
    <a class="speaker__link" href="{page_name(slug)}">
    <span class="num">{n}</span>
    <figure class="speaker__photo">{photo}<figcaption>{esc(meta['name'])}</figcaption></figure>
    <span class="speaker__body">{role}{first}{more}</span>
    </a>
  </li>"""


def speaker_page(slug: str, meta, body, sessions, known) -> str:
    name = esc(meta["name"])
    bio = "".join(f"<p>{esc(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    if sessions:
        talks = "\n".join(
            f'<li class="talk"><span class="talk__when"><a href="program.html#{s["day"].isoformat()}">{program.CORE_DAYS[s["day"]]}, {s["start"]}</a>'
            f'<span>{esc(s["format"])}, {esc(s["room"])}</span></span>{program.tags(None, s.get("area"))}<strong><a href="{esc(s["page"])}">{esc(s["title"])}</a></strong>'
            f'{program.for_line(s.get("for"))}<p>{esc(s["about"])}</p>'
            + (f'<a class="session__register" href="{esc(s["signup"])}">Save a seat</a>' if s.get("signup") else "") + '</li>' for s in sessions)
    elif meta.get("talk"):
        about = "".join(f"<p>{esc(p.strip())}</p>" for p in str(meta.get("talk_about") or "").split("\n\n") if p.strip())
        talks = (f'<li class="talk"><span class="talk__when"><span>{talk_format(meta)}</span><span>Day and time to be announced</span></span>'
                 f'{program.tags(None, meta.get("talk_area"))}<strong>{esc(meta["talk"])}</strong>{program.for_line(meta.get("talk_for"))}{about}</li>')
    else:
        talks = ""
    links = "".join(f'<li><a href="{esc(u)}">{esc(re.sub(r"^https?://(www\.)?", "", str(u)).rstrip("/"))}</a></li>' for u in meta.get("links") or [])
    # The "I'm speaking" card shown as supporters' cards are, with both sizes to download.
    share = extensions.share_section({"square": f"speaker-{slug}-square.png", "wide": f"speaker-{slug}-wide.png"},
                                     f"{name}, speaking at GoatConf 2027",
                                     "Your card, to post as your own: speaking at GoatConf 2027. It links back to the speakers page.",
                                     "Your card: I'm speaking", SITE)
    share += extensions.share_section(announce_cards(slug), f"Confirmed speaker at GoatConf 2027: {name}",
                                      "GoatConf 2027's card announcing you, for anyone to post. It links to this page.",
                                      "The announcement card", SITE)
    photo = (esc(meta["photo"]), 800, 800, meta["name"]) if meta.get("photo") else ("brand/coin.svg", 300, 300, "")
    first = sessions[0] if sessions else None
    lede = (f'{esc(first["format"])} on {program.CORE_DAYS[first["day"]]} at {first["start"]}, {esc(first["room"])}.' if first
            else "Speaking at GoatConf 2027 in Tuzla.")
    if meta.get("role"):
        lede = f'<span class="lede__role">{esc(meta["role"])}</span>{lede}'
    main = f"""<section class="album-page wrap speaker-page" aria-labelledby="h-about">
  <h2 class="band" id="h-about">Who they are</h2>
  <div class="copy copy--wide">{bio}</div>
  {f'<ul class="speaker-page__links">{links}</ul>' if links else ''}
</section>
<section class="album-page wrap" aria-labelledby="h-talks">
  <h2 class="band" id="h-talks">{"Sessions" if len(sessions) > 1 else "Session"}</h2>
  {f'<ul class="talks">{talks}</ul>' if talks else '<p class="copy">The session will be on the program soon.</p>'}
  <p class="copy"><a class="go go--ink" href="program.html">See the whole program</a> <a class="go go--ink" href="speakers.html">All speakers</a></p>
</section>{support_section(meta)}{share}"""
    title = f"{meta['name']}: speaking at GoatConf 2027, Tuzla"
    who = f"{meta['name']} ({meta['role']})" if meta.get("role") else meta["name"]
    if first:
        subject = esc(first["title"])
    elif meta.get("talk"):
        subject = esc(meta["talk"])
    else:
        subject = "a session at IPI Academy"
    desc = f"{esc(who)} speaks at GoatConf 2027 in Tuzla, 3–5 June 2027: {subject}."
    preview = preview_name(slug) if (SITE / "share" / preview_name(slug)).exists() else ""
    return shell(page_name(slug)[:-5], esc(title), desc, photo, name, lede, main, preview)


def support_problems(meta) -> list:
    """`support_them`, on a speaker or a supporter: each way a short line of text and an https link."""
    ways = meta.get("support_them")
    if ways is not None and (not isinstance(ways, list) or not ways or any(
            not isinstance(w, dict) or not str(w.get("text") or "").strip() or "\n" in str(w.get("text")) or len(str(w.get("text"))) > 90
            or not str(w.get("url") or "").startswith("https://") for w in ways)):
        return ["support_them must list ways to support them, each a text of one short line and a url starting https://"]
    return []


def support_section(meta) -> str:
    """How people can support a speaker or a supporter, from their record's `support_them`; nothing without it."""
    ways = "".join(f'<li><a href="{esc(w["url"])}">{esc(w["text"])}</a></li>' for w in meta.get("support_them") or [])
    return (f"""
<section class="album-page wrap" aria-labelledby="h-support-them">
  <h2 class="band" id="h-support-them">How to support them</h2>
  <ul class="copy copy--wide support-them">{ways}</ul>
</section>""" if ways else "")


def supporter_page_name(slug: str) -> str:
    """Each supporter's own profile, where they download their cards."""
    return f"supporter-{slug}.html"


def supporter_cards(slug: str) -> dict:
    """The supporter's thank-you cards in site/share/, made by tools/shareables.py."""
    return {"square": f"supporter-{slug}-square.png", "wide": f"supporter-{slug}-wide.png"}


def proud_cards(slug: str) -> dict:
    """The supporter's own "Proud supporter of GoatConf 2027" cards, for them to post."""
    return {"square": f"supporter-{slug}-proud-square.png", "wide": f"supporter-{slug}-proud-wide.png"}


def supporter_page(slug: str, meta, body) -> str:
    name = esc(meta["name"])
    words = "".join(f"<p>{esc(p.strip())}</p>" for p in body.split("\n\n") if p.strip())
    site = esc(re.sub(r"^https?://(www\.)?", "", str(meta["url"])).rstrip("/"))
    hosted = {s: (m, b) for _, s, m, b in extensions.accepted() if s in (meta.get("events") or [])}
    events = ""
    if hosted:
        cards = "\n".join("  " + extensions.card(i + 1, s, m) for i, (s, (m, _)) in enumerate(hosted.items()))
        events = f"""
<section class="album-page wrap" aria-labelledby="h-events">
  <h2 class="band" id="h-events">{"Their events" if len(hosted) > 1 else "Their event"}</h2>
  <p class="copy copy--wide">Part of GoatConf 2027: accepted by us, and organised and paid for by {name}.</p>
  <ul class="slots slots--events">
{cards}
  </ul>
</section>"""
    proud = extensions.share_section(proud_cards(slug), f"{name}, proud supporter of GoatConf 2027",
                                     "Your card, to post as your own: proud supporter of GoatConf 2027. It links back to this page.",
                                     "Your card: proud supporter", SITE)
    thanks = extensions.share_section(supporter_cards(slug), f"Thank you, {name}", "A thank-you from GoatConf 2027 to post wherever you like. It links back to this page.",
                                      "The thank-you card", SITE)
    event_cards = "".join(extensions.share_section(extensions.cards(s), f"The card for {esc(m['name'])}",
                                                   f"{esc(m['name'])}, organised by {name}, part of GoatConf 2027: for you and anyone going to post. It links to the event's page.",
                                                   f"The card for {esc(m['name'])}", SITE) for s, (m, _) in hosted.items())
    support = support_section(meta)
    main = f"""<section class="album-page wrap" aria-labelledby="h-support">
  <h2 class="band" id="h-support">{"Who they are" if words else "Host and partner" if meta.get("host") is True else "Their support"}</h2>
  {f'<div class="copy copy--wide">{words}</div>' if words else ""}
  <p class="copy"><a class="go go--ink" href="{esc(meta["url"])}">{site}</a> <a class="go go--ink" href="supporters.html">All supporters</a></p>
</section>{support}{events}{proud}{thanks}{event_cards}"""
    # A link to the profile shows the card of the first event they host, else their thank-you card.
    previews = [extensions.cards(s)["preview"] for s in hosted] + [supporter_cards(slug)["wide"]]
    preview = next((name for name in previews if (SITE / "share" / name).exists()), "")
    dark = " page-head__photo--logo" + {"dark": " page-head__photo--logo-dark", "tinted": " page-head__photo--logo-tinted"}.get(logo_class(meta, "")[2:], "")
    return shell(supporter_page_name(slug)[:-5], f"{name}: supporting GoatConf 2027, Tuzla", f"{name} supports GoatConf 2027 in Tuzla: {esc(meta['funds'])}.",
                 (esc(meta["logo"]), 600, 300, name), name, esc(meta["funds"]), main, preview, dark, logo_style(meta))


def supporter_card(n: int, slug: str, meta, body) -> str:
    """The supporter on the wall: logo, name and their line; who they are is on their profile."""
    return f"""  <li class="sticker sticker--supporter" id="{esc(slug)}" style="--tilt:{(-1, 1, -0.5, 0.5)[n % 4]}deg">
    <span class="num">{n}</span>
    <a class="supporter__logo{logo_class(meta, ' supporter__logo')}"{logo_style(meta)} href="{supporter_page_name(slug)}"><img src="{esc(meta['logo'])}" alt="{esc(meta['name'])}" loading="lazy"></a>
    <strong><a href="{supporter_page_name(slug)}">{esc(meta['name'])}</a></strong>
    <p class="supporter__funds">{esc(meta['funds'])}</p>
  </li>"""


def logo_class(meta, base: str) -> str:
    """The modifier for a logo's background: dark for a logo made for one, tinted for one in the supporter's own colour."""
    return f"{base}--dark" if meta.get("logo_on") == "dark" else f"{base}--tinted" if meta.get("logo_bg") else ""


def logo_style(meta) -> str:
    """The supporter's own colour behind their logo, if their record gives one (logo_bg)."""
    return f' style="--logo-bg:{esc(meta["logo_bg"])}"' if meta.get("logo_bg") else ""


def shell(slug: str, title: str, description: str, photo, h1: str, lede: str, main: str, preview: str = "", photo_class: str = "",
          photo_style: str = "") -> str:
    src = photo[0]
    mark = photo_class or (" page-head__photo--mark" if src.startswith("brand/") else (" page-head__photo--portrait" if src.startswith("img/speakers/") else ""))
    return frame.page(slug, title, description, photo, h1, lede, main,
                      "files/tools/speakers.py build from files/speakers/*.md and files/supporters/*.md", preview, mark, photo_style)



def speakers_page() -> str:
    known = supporters()
    people = speakers()
    talks = sessions_by_speaker()
    detail = sessions_by_speaker(detail=True)
    order = listed(people)
    if order:
        cards = '<ul class="slots slots--speakers">\n' + "\n".join(
            speaker_card(i + 1, slug, m, b, talks.get(slug, []), known, (detail.get(slug) or [None])[0]) for i, (slug, (m, b)) in enumerate(order)) + "\n</ul>"
    else:
        cards = """<ul class="slots slots--speakers">
  <li class="slots__wide"><a class="slot slot--link slot--wait" href="talk.html"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg><span class="num num--printed">1</span><strong>The first speaker could be you</strong><small>No one is announced yet. Speakers appear here as their sessions are accepted, and the call for proposals is open now.</small><span class="stamp">Yours?</span></a></li>
</ul>"""
    main = f"""<section class="album-page wrap" aria-labelledby="h-speakers">
  <h2 class="band" id="h-speakers">Who is speaking</h2>
  <p class="copy copy--wide">Each speaker here has a session on Thursday 3rd or Friday 4th June 2027, or will have one soon: some are confirmed before their session has a time and room. They wrote their profiles themselves. Days, times and rooms are set closer to the event; the <a href="program.html">program</a> shows each session once it has its slot.</p>
  {cards}
</section>"""
    return shell("speakers", "Speakers: GoatConf 2027, 3–5 June, Tuzla",
                 "The speakers at GoatConf 2027 in Tuzla: their sessions, in their own words.",
                 ("img/ipi-lecture-hall.jpg", 1024, 768, "A talk in IPI Academy's lecture hall, students' faces blurred"),
                 "The speakers", "The people giving the talks, panels and workshops, in their own words.", main)


def supporters_page() -> str:
    known = supporters()
    people = speakers()
    order = listed_supporters(known)
    # Until a company supports GoatConf (the host does not count), the wall keeps a place inviting one.
    invite = ("" if any(m.get("host") is not True for _, (m, _b) in order) else
              f'  <li><a class="slot slot--link" href="#h-become"><svg class="ghost" aria-hidden="true" viewBox="0 0 124 100"><use href="#goat"/></svg><span class="num num--printed">{len(order) + 1}</span>'
              f'<strong>Your logo</strong><small>{"Be the first supporter." if order else "No supporters yet."} Support GoatConf online and your logo and link go here.</small><span class="stamp">Yours?</span></a></li>')
    cards = '<ul class="slots slots--supporters">\n' + "\n".join(
        [supporter_card(i + 1, slug, m, b) for i, (slug, (m, b)) in enumerate(order)] + ([invite] if invite else [])) + "\n</ul>"
    main = f"""<section class="album-page wrap" aria-labelledby="h-supporters">
  <h2 class="band" id="h-supporters">Who makes it possible</h2>
  <p class="copy copy--wide">GoatConf is free to attend. Companies and communities help keep it that way. Supporters cannot buy talks, stage time or the attendee list, and who speaks is never decided by who supports. See <a href="charter.html">the charter</a>.</p>
  {cards}
</section>
<section class="album-page wrap" aria-labelledby="h-become">
  <h2 class="band" id="h-become">Support GoatConf online</h2>
  <p class="copy copy--wide">Reach the 120 to 300 engineers, designers, product people and founders who come to Tuzla. One level, the same for every supporter: 500 euro, plus VAT where it applies.</p>
  <ul class="copy copy--wide">
    <li>Your logo and a link on this page and on the home page.</li>
    <li>One post about you on GoatConf's social channels.</li>
    <li>A mention in the emails to everyone registered.</li>
  </ul>
  <p class="copy copy--wide">It is online only: no booth, no banner and nothing at the venue. The money pays the event's costs.</p>
  <p class="copy copy--wide">You can also pay a supplier directly for one named thing, such as the printing or a round of coffee, or give something in kind.</p>
  <p class="copy copy--wide">If you speak at GoatConf and your company covers your travel, your company is listed here as a supporter too, with its logo and link, the same as online supporters.</p>
  <p class="copy copy--wide">If you or your organisation fund and organise an event we accept as part of GoatConf 2027, you are listed here as a supporter too, if you agree, with your logo and link, the same as online supporters.</p>
  <p class="copy copy--wide">To support GoatConf, reach Muhamed, the organiser, through the contact form or at <a href="mailto:info@muhamed.at">info@muhamed.at</a>.</p>
  <p class="cta"><a class="button" href="contact.html">Become a supporter</a></p>
</section>"""
    return shell("supporters", "Supporters: GoatConf 2027, 3–5 June, Tuzla",
                 "The companies and communities that make GoatConf 2027 possible, and how to support it online: one level, 500 euro, nothing at the venue.",
                 ("img/city-korzo-clock.jpg", 1160, 773, "The Korzo on a sunny day: the street clock, a pink corner house, café umbrellas and people walking"),
                 "The supporters", "The companies and communities that help keep GoatConf free, and how to join them.", main)


def all_pages() -> dict:
    out = {PAGES["speakers"]: nav.place(meta.tag(speakers_page()), "speakers.html"),
           PAGES["supporters"]: nav.place(meta.tag(supporters_page()), "supporters.html")}
    known = supporters()
    detail = sessions_by_speaker(detail=True)
    for slug, (m, b) in speakers().items():
        name = page_name(slug)
        out[SITE / name] = nav.place(meta.tag(speaker_page(slug, m, b, detail.get(slug, []), known)), nav.section(name))
    for slug, (m, b) in known.items():
        name = supporter_page_name(slug)
        out[SITE / name] = nav.place(meta.tag(supporter_page(slug, m, b)), nav.section(name))
    return out


def cmd_build(args) -> int:
    pages = all_pages()
    stale = 0
    stale += sitelib.prune([*SITE.glob("speaker-*.html"), *SITE.glob("supporter-*.html")], pages, args.check, "tools/speakers.py build", "belongs to no record")
    if args.check:
        for slug in speakers():
            if not (SITE / "share" / preview_name(slug)).exists():
                print(f"site/share/{preview_name(slug)} is missing, so the page would share the generic banner: "
                      f"run python3 tools/shareables.py render --only {preview_name(slug)}")
                stale += 1
            for card in announce_cards(slug).values():
                if not (SITE / "share" / card).exists():
                    print(f"site/share/{card} is missing, so the speaker has no card announcing them: "
                          f"run python3 tools/shareables.py render --only {card}")
                    stale += 1
        for slug in supporters():
            for card in [*supporter_cards(slug).values(), *proud_cards(slug).values()]:
                if not (SITE / "share" / card).exists():
                    print(f"site/share/{card} is missing, so the supporter's profile has no card to download: "
                          f"run python3 tools/shareables.py render --only supporter-{slug}")
                    stale += 1
    stale += sitelib.write_or_check(pages, args.check, "tools/speakers.py build")
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
