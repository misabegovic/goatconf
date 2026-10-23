---
title: "Make it yours: one hub at /extend, built from event and venue records, with guides, filters, photos and the hours off"
kind: decision
status: accepted
updated: 2026-10-23
team: organiser
confidence: medium
depends_on:
  - org/prds/hosts-hub-guides-and-venues.md
  - org/adrs/extension-slots-and-the-record.md
sources:
  - sources/conversations/2026-10-23--org--make-it-yours-adr-approved.md
  - sources/conversations/2026-10-23--org--venues-approved.md
  - sources/conversations/2026-10-23--org--add-form-updated.md
  - sources/conversations/2026-10-23--org--hosts-hub-approved.md
  - sources/conversations/2026-10-23--org--hosts-hub-answers.md
  - sources/conversations/2026-10-23--org--extensions-page-search-guides-photos.md
  - sources/conversations/2026-10-23--org--reserved-venues-and-explore.md
  - sources/conversations/2026-10-23--org--host-guides-and-venues.md
  - sources/conversations/2026-10-23--org--extendable-and-each-edition.md
  - sources/conversations/2026-10-19--org--site-review-decisions.md
  - sources/conversations/2026-10-13--org--food-photos-one-by-one.md
  - sources/conversations/2026-10-12--org--friday-dzuma-schedule.md
  - sources/web/models/pycon-au-2024-birds-of-a-feather-2026-10-23.md
  - sources/web/models/london-tech-week-2020-fringe-event-toolkit-2026-10-23.md
  - sources/web/models/edfringe-finding-a-venue-2026-10-23.md
  - sources/web/models/edfringe-how-to-start-making-your-show-accessible-2026-10-23.md
  - sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md
---

# Make it yours: one hub at /extend, built from event and venue records, with guides, filters, photos and the hours off

Answers [Make it yours: the hosts' hub](../prds/hosts-hub-guides-and-venues.md),
approved by the organiser on 2026-10-23
(`sources/conversations/2026-10-23--org--hosts-hub-approved.md`). Accepted
the same day: "Approved, build it"
(`sources/conversations/2026-10-23--org--make-it-yours-adr-approved.md`).

## What

GoatConf gets one page for everything people add, "Make it yours", at
goatconf.com/extend. It replaces "Events people add" (`extensions.html`)
and "Propose an event" (`add.html`), which become short pages that send
the visitor on to /extend, so no shared link breaks; each accepted
event keeps its own page. The hub reads, in order: the line "Every
GoatConf is shaped by who joins it.", what people are adding (the
accepted events), the guides (how, what, where), the places in Tuzla
with filters and a search box, and the form. The home page carries the
same line, and its sticker 6, "Extendable", links to /extend. The top bar
gains "Make it yours" beside "Propose a session". Hosts may run short,
free, open events in the hours off on Thursday and Friday, never at the
same time as a session, and never in Friday's 12:30 hour; they propose
them through the same form, and the organiser accepts them like any other
event (`sources/conversations/2026-10-23--org--hosts-hub-answers.md`,
`sources/conversations/2026-10-23--org--hosts-hub-approved.md`).

## Why

The organiser counts extendability as GoatConf's special aspect and wants
it obvious (`sources/conversations/2026-10-23--org--extendable-and-each-edition.md`).
Today the invitation is spread over two pages that lead with rules, and
nothing tells a host how, what or where. One hub gives one address to
share, one place to read, and one door to propose through, which is what
the extension host persona asks for. Each edition is shaped by who joins
it and promises nothing beyond itself, so the line speaks of every
GoatConf, not of next year (`sources/conversations/2026-10-23--org--hosts-hub-answers.md`).

The hours off fit small events because IPI is in the centre and several
places are a few minutes away; PyCon AU runs the same kind of small
circles in its breaks (`sources/web/models/pycon-au-2024-birds-of-a-feather-2026-10-23.md`).
Keeping them out of session time protects the speakers' rooms, and Friday
12:30 is already held for Džuma and lunch
(`sources/conversations/2026-10-12--org--friday-dzuma-schedule.md`).
Using the same form keeps one record, one check and one acceptance for
everything, as the extension ADR set
([Extension slots and the record](extension-slots-and-the-record.md)).

## How

**Venue records.** Each place becomes an entry in a new venues list kept
beside the places to eat and stay, in `places/`, in the same way that
list drives the travel page today: name, kind of place, address, a map
point, distance from IPI, whether it fits an hour off, size where known,
indoor or outdoor, the kinds of event it suits, what it already hosts,
the public contact, whether to check with GoatConf first, a photo, the
sources, the date it was checked, and an approval flag only the
organiser sets. The first entries come from
[Places in Tuzla where hosts could run an event](../tuzla/venues-for-hosts.md).
The National Theatre and HKC "Sveti Franjo" carry "check with GoatConf
first" (`sources/conversations/2026-10-23--org--reserved-venues-and-explore.md`,
`sources/conversations/2026-10-23--org--hosts-hub-answers.md`). Every
listing says it is a place to ask, not an arrangement.

**The hub is generated.** The tool that writes the events page today
writes /extend instead, from the event records and the venue records,
and keeps writing each event's own page. The guides are written by hand
in plain language between the generated parts, with the rest of the
site's frame, top bar and link previews applied by the existing tools.
The two old addresses become small pages that point to /extend, written
and checked by the same build.

**Guides.** Three short parts. How: the deal (you run it and pay for it;
GoatConf accepts and lists it), the GoatConf week and the hours off, a
venue checklist (size, step-free access and toilets, equipment, licence,
costs, cancellation, a visit beforehand, after Edinburgh Fringe and its
access guide), sign-ups and the no-shows a free event expects (up to half,
after London Tech Week), the code of conduct and consent before
recording, and Tuzla Canton's notice rules in plain words with a pointer
to the law (`sources/web/models/edfringe-finding-a-venue-2026-10-23.md`,
`sources/web/models/edfringe-how-to-start-making-your-show-accessible-2026-10-23.md`,
`sources/web/models/london-tech-week-2020-fringe-event-toolkit-2026-10-23.md`,
`sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md`). What: one card
per kind on the form, with what it needs and the kind of place that
suits it, karaoke pointing to the cafés on and around Freedom Square.
Where: the places.

**Filters and search** are a small script over the venue cards already in
the page, filtering by kind of event, size, distance, fits an hour off,
indoor or outdoor and check with GoatConf first, with a text box over
places and events. Without the script the full list reads as it is; no
library and no build step are added.

**Photos.** Each venue shows the best photo found, freely licensed or the
venue's own, picked one by one and stored with a record of where it came
from, as the site's photos are; a photo comes down if its owner asks, as
the food photos do (`sources/conversations/2026-10-13--org--food-photos-one-by-one.md`,
`sources/conversations/2026-10-23--org--hosts-hub-answers.md`). A venue
without a good photo shows the album's printed empty slot.

**The hours off in the check.** The record check accepts an event on
Thursday 3 or Friday 4 June during core-day hours only when it sits
inside one hour off (Thursday 11:00, 13:00 or 15:00; Friday 10:30 or
14:30) and is free; anything else in core-day hours fails the check with
a plain message. The propose an event form's wording on times changes to
say so, which is the organiser's edit, since the form is public
(`sources/conversations/2026-10-19--org--site-review-decisions.md`).

**Links.** The footer's "Events people add" and "Propose an event" become
"Make it yours"; the program's Saturday link, the charter's links, the
home page's event section, the files for agents and the sitemap all
point to /extend.

## Alternatives

- **Keep the two pages and add a guides page.** Least change, but three
  pages to find and share; the organiser chose one hub.
- **Venues as one Markdown file each, like events.** Lets a venue or a
  host propose a place by pull request, but adds approval work for
  places GoatConf never arranges; the list beside the places to eat and
  stay matches how the travel page already works. A venue file per place
  stays possible later.
- **Venues written straight into the page.** No records to keep, but no
  checks, no approval flag and no reuse on the travel page or in the
  files for agents.
- **A board for the hours off, closer to the day,** like PyCon US's open
  spaces: lighter for spontaneous circles, but a second door and a second
  kind of listing; the organiser chose the same form.
- **Only freely licensed photos.** Safer on rights, but most venues would
  show an empty slot; the organiser chose all good photos.
- **Do nothing.** The sticker says "make it your own" and the pages
  still lead with rules.

## Consequences

- **Gains:** one address to share, guides a stranger can act on, the
  places in one list with contacts, and the hours off open to small
  events.
- **Gains:** the venue list is reusable: the travel page and the files
  for agents can read it.
- **Costs:** the records need upkeep; bars change hands and sites lapse,
  so each entry shows the date it was checked.
- **Costs:** photos that are not freely licensed carry a takedown risk,
  accepted by the organiser.
- **Costs:** the form's wording changes, an organiser's act.
- **Risk:** an hour-off event that runs over pulls people from the next
  session; the guide asks hosts to end five minutes before the hour.
- **Unchanged:** the charter's four rules, the record's fields, the
  acceptance by the organiser, and each event's own page.

## Linked PRD

[Make it yours: the hosts' hub](../prds/hosts-hub-guides-and-venues.md).

## Build notes

**2026-10-23.** Built as decided, on the branch for review before any
merge, since every merge to `main` publishes the site.

- **The hub** is `site/extend.html`, written by `tools/extensions.py build`
  from `extensions/*.md` and `places/venues.yml`; `extensions.html` and
  `add.html` are written by the same build as small pages with a refresh to
  /extend, a canonical link to it and `noindex`, and `tools/agents.py`
  leaves them out of llms.txt and the sitemap. Each event's page links back
  to the hub.
- **Venue records** are `places/venues.yml`: 33 places from
  [the research](../tuzla/venues-for-hosts.md), each with its sources, a
  map point or a sourced distance, the kinds of event it suits, its
  public contact and an `approved` flag. All 33 start unapproved, since only
  the organiser sets the flag; the hub says the list is being checked until
  they do, and `build --all` previews every place. The check fails a record
  with a missing field, an unknown kind, a missing source or a photo without
  its record.
- **Photos:** 24 places have one, in `site/img/venues/` with WebP copies;
  the originals and their records are in `assets/images/venues/`, and
  `sources/web/images/venue-photos-2026-10-23.md` lists each one's author,
  licence or "not freely licensed", page and image address. Eight are
  freely licensed, from Wikimedia Commons; one is the city's photo of the
  lakes, given for GoatConf and already on the site; fifteen are venues' or
  publishers' own. The other nine places show the printed empty slot.
- **Filters** are `site/extend.js`, stamped like the other assets by
  `tools/meta.py`. The text box searches the places, not the events, since
  one event is listed today; filtering events can follow when there are
  more.
- **The hours off** come from `DAY_PLAN` in `tools/program.py`: the hour
  after each slot with a break, less Friday's 12:30. The record check fails
  an event on 3 or 4 June that overlaps the day's sessions unless it sits
  inside one hour off and is free, and fails a whole-day record on a core
  day; the guide says so in words built from the same plan.
- **Links:** "Make it yours" is in the top bar beside "Propose a session"
  and in every footer in place of "Propose an event" and "Events people
  add"; the home page's section is now "Make it yours" and opens with the
  editions line, its kind slots open the hub with that kind already picked,
  and the program, charter, contact and talk pages point to /extend.
- **The form's wording** was drafted in `tools/google-forms/README.md`, and
  the organiser put it into the public form the same day
  (`sources/conversations/2026-10-23--org--add-form-updated.md`).
- **Tests:** `tests/test_extensions.py` covers the hours off, whole core
  days, venue records and their check, the preview, and the old addresses.

**2026-10-23, the places approved.** The organiser approved all 33 places
("Approve all 33", `sources/conversations/2026-10-23--org--venues-approved.md`),
so every one shows on the hub. Checked in a browser: the filters narrow the
list (karaoke to 6 places, "fits an hour off" to 8), the "no match" note
shows when nothing fits, a kind in the address (`?kind=karaoke`) picks the
filter, and /add forwards to /extend.

**2026-10-23, live.** Merged as PR #158 and published: goatconf.com/extend
answers, and /add forwards to it. The organiser updated the "add something"
form with the new wording on the hours off and the link to /extend
(`sources/conversations/2026-10-23--org--add-form-updated.md`).
