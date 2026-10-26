---
title: "Make it yours: one hub with guides on how, what and where, a searchable list of Tuzla venues, and events in the hours off"
kind: initiative
status: living
parent_epic: goatconf-2027
updated: 2026-10-23
team: organiser
repos:
  - org
appetite: medium
confidence: medium
depends_on:
  - org/tuzla/venues-for-hosts.md
  - org/adrs/extension-slots-and-the-record.md
sources:
  - sources/conversations/2026-10-23--org--extendable-and-each-edition.md
  - sources/conversations/2026-10-23--org--host-guides-and-venues.md
  - sources/conversations/2026-10-23--org--reserved-venues-and-explore.md
  - sources/conversations/2026-10-23--org--extensions-page-search-guides-photos.md
  - sources/conversations/2026-10-23--org--hosts-hub-answers.md
  - sources/conversations/2026-10-23--org--hosts-hub-approved.md
  - sources/conversations/2026-10-13--org--food-photos-one-by-one.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-20--org--hero-extendable.md
  - sources/conversations/2026-10-19--org--site-review-decisions.md
  - sources/conversations/2026-10-12--org--accepted-events-and-hackathons.md
  - sources/web/models/pycon-au-2024-birds-of-a-feather-2026-10-23.md
  - sources/web/models/pycon-us-2025-open-spaces-2026-10-23.md
  - sources/web/models/europython-2025-open-spaces-2026-10-23.md
  - sources/web/models/europython-2025-sprints-2026-10-23.md
  - sources/web/models/ietf-side-meetings-and-private-meetings-2026-10-23.md
  - sources/web/models/sxsw-2027-affiliate-activity-inquiry-form-2026-10-23.md
  - sources/web/models/techcrunch-early-stage-2024-host-your-side-event-2026-10-23.md
  - sources/web/models/devconnect-istanbul-host-an-event-notion-2026-10-23.md
  - sources/web/models/devconnect-amsterdam-host-an-event-notion-2026-10-23.md
  - sources/web/models/london-tech-week-2020-fringe-event-toolkit-2026-10-23.md
  - sources/web/models/edfringe-finding-a-venue-2026-10-23.md
  - sources/web/models/edfringe-how-to-start-making-your-show-accessible-2026-10-23.md
  - sources/web/models/woocommerce-meetup-organizer-handbook-2026-10-23.md
  - sources/web/models/fosdem-2026-fringe.md
  - sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md
---

# Make it yours: one hub with guides on how, what and where, a searchable list of Tuzla venues, and events in the hours off

Approved by the organiser on 2026-10-23 (`sources/conversations/2026-10-23--org--hosts-hub-approved.md`), after seven answers (`sources/conversations/2026-10-23--org--hosts-hub-answers.md`). Agent-drafted from the organiser's asks and answers; the decision record is [Make it yours: one hub at /extend](../adrs/make-it-yours-hub.md).

## Background

On 2026-10-23 the organiser asked how obvious it is that people can
extend GoatConf and make it their own, called that "one of the special
aspects of GoatConf", and added that "each year the edition might change
depending on folks joining"
(`sources/conversations/2026-10-23--org--extendable-and-each-edition.md`).
The organiser then floated guides on how to add something and a list of
venues "where they could do their magic", including events between
sessions (`sources/conversations/2026-10-23--org--host-guides-and-venues.md`);
asked that the National Theatre and the "church in glass" be marked
"check with us first", since GoatConf may use them itself
(`sources/conversations/2026-10-23--org--reserved-venues-and-explore.md`);
and asked that the page for extending the event grow search, filtering,
guides for "how and maybe what, where", contacts and photos
(`sources/conversations/2026-10-23--org--extensions-page-search-guides-photos.md`).
The research behind the venues is
[Places in Tuzla where hosts could run an event](../tuzla/venues-for-hosts.md).

The shape is the organiser's from the first day: a minimal core that
others extend, "like the Pi agent", with "a framework for others to
build on" (`sources/conversations/2026-10-07--org--conference-vision.md`).
Today the framework is the record and the rules
([Extension slots and the record](../adrs/extension-slots-and-the-record.md));
what a would-be host lacks is the help to get from an idea to an event.

## Objective

If GoatConf publishes one hosts' hub (how to host, what to run, where in
Tuzla, with photos and contacts, searchable and filterable, next to the
events already accepted), it turns "make it your own" from a sticker
into something a stranger can act on in an evening, and it makes
plain that GoatConf's shape comes from the people who join.

## Affected personas

- [The extension host](../../../../.claude/personas/users/extension-host.md):
  the persona's own hypothesis is "one page that says what they may add,
  by when, and on what terms" and "a slot or a place in the shared
  calendar". The hub is that page, plus the places.
- [The attendee](../../../../.claude/personas/users/attendee.md): finds
  what to do in the evenings and the hours off, and learns early that
  they can add something themselves.

## The organiser's answers (2026-10-23)

The seven open questions were put to the organiser one at a time
(`sources/conversations/2026-10-23--org--hosts-hub-answers.md`):

1. **Hours off only.** Hosts may run short, free, open events near IPI
   in the hours off on Thursday and Friday, never at the same time as a
   session; Friday 12:30 stays free for Džuma and lunch.
2. **The church in glass is HKC "Sveti Franjo",** and it is "check with
   GoatConf first" with the National Theatre.
3. **Each edition is its own.** "It only shapes the current edition,
   every edition could be different based on who joins." The site says
   that what people add shapes this year's GoatConf, and that the next
   edition may look different because different people join; it promises
   nothing carried over.
4. **One hub,** with the old addresses redirected.
5. **List only for now.** Every venue reads "a place you could ask"; the
   agent may draft emails the organiser could send later.
6. **Use all good photos,** licensed or not ("Use all photos that are
   good, disregard that"), as with the food photos, which come down if an
   owner asks (`sources/conversations/2026-10-13--org--food-photos-one-by-one.md`).
7. **Karaoke in cafés nearby,** "like on the square"; the hub points a
   karaoke host at the cafés on and around Freedom Square.

## Now / Perceived / Target

- **Now.** The home page says "Extendable: a minimal core, make it your
  own" (`sources/conversations/2026-10-20--org--hero-extendable.md`) and
  shows eight "Yours?" kind slots. `site/add.html` explains the rules and
  links the form; `site/extensions.html` lists one accepted event. No page
  says how to run an event, where in Tuzla, or that a host may use the
  hours off. "Propose an event" is not in the top bar. An event is
  anything a host runs from 2 to 6 June, and a slot at IPI is a session
  (`sources/conversations/2026-10-19--org--site-review-decisions.md`).
  Nothing says one edition shapes the next.
- **Perceived.** The organiser reads extendability as GoatConf's special
  aspect and wants it obvious (`sources/conversations/2026-10-23--org--extendable-and-each-edition.md`).
- **Target.** A visitor lands on one hub, sees what people
  are adding, filters places by what they want to run, reads a short
  guide, and proposes. Two venues say "check with GoatConf first". The
  hub says, in one line, that the people who join shape this edition and
  that every edition can be different.

## Scope

- **One hub page, "Make it yours" at goatconf.com/extend,** that replaces today's two pages: what people are
  adding (the accepted events, as now), then the guides, then the places,
  then the proposal form. `extensions.html` and `add.html` redirect to it,
  so every existing link keeps working.
- **Guides, short and plain, in three parts**, built from the prior art
  (sources listed above):
  - **How:** the deal (you run it and pay for it; GoatConf accepts and
    lists it), timing and the GoatConf week, picking and booking a venue
    with a checklist (capacity, step-free access and toilets, equipment,
    licence, costs, cancellation, a visit beforehand), registration and
    no-shows (free events lose up to half their sign-ups, per London Tech
    Week), accessibility (Edinburgh Fringe), the code of conduct and
    consent before recording, Tuzla's notice rules in the agent's plain
    reading, and the day itself.
  - **What:** one short card per kind already on the form (evening
    event, community trip, meetup, live podcast, hike, hackathon,
    karaoke, something else) with what it needs, a good size and the kind
    of place that suits it; plus small formats for the hours off, like a
    birds-of-a-feather circle (PyCon AU) or a walk.
  - **Where:** the places list, below.
- **Places, as records.** Each venue becomes a short record (name, kind,
  address, distance from IPI, fits an hour off, size, indoor or outdoor,
  what it already hosts, how to ask, check with GoatConf first, a photo
  with its licence), the way `places/places.yml` already drives the
  travel page. The organiser approves each before it shows, as with
  places to eat. The research page is the starting set.
- **Search and filters** on the hub: by kind of event, size, distance,
  fits an hour off, indoor or outdoor, and "check with us first", plus a
  text search over places and accepted events. The site is static with no
  build step (`PRODUCT.md`), so this is a small script over data already
  in the page, and the full list still reads without it.
- **Photos.** Every good photo of a place, freely licensed or the
  venue's own, picked one by one like the food photos, each with a record
  of where it came from; a photo comes down if its owner asks. Where no
  good photo exists, the record shows a printed empty slot, as the sticker
  album does for anything undecided (`DESIGN.md`).
- **Check with GoatConf first** on the National Theatre and the church in
  glass (HKC "Sveti Franjo" if the organiser confirms the match), and on
  any IPI room, in the way SXSW and IETF mark spaces the organiser
  controls (`sources/web/models/sxsw-2027-affiliate-activity-inquiry-form-2026-10-23.md`,
  `sources/web/models/ietf-side-meetings-and-private-meetings-2026-10-23.md`).
- **Events in the hours off,** as the organiser decided: short, free,
  open events near IPI during the hours off on Thursday and Friday, never
  at the same time as a session, listed like any other event; Friday
  12:30 stays free. The hub marks the places that fit an hour off.
  PyCon AU's birds-of-a-feather and PyCon US's open spaces are the
  models; TechCrunch's "after 17:00 on the main day" is the choice not
  taken (`sources/web/models/pycon-au-2024-birds-of-a-feather-2026-10-23.md`,
  `sources/web/models/pycon-us-2025-open-spaces-2026-10-23.md`,
  `sources/web/models/techcrunch-early-stage-2024-host-your-side-event-2026-10-23.md`).
- **The line about editions,** "Every GoatConf is shaped by who joins
  it.", on the hub and on the home page.
- **"Propose an event" in the top bar,** next to "Propose a session".

## No-gos

- No venue is listed as arranged, partnered or reserved for hosts unless
  the organiser has arranged it; the default wording is "a place you
  could ask".
- No photo without a record of where it came from.
- No places of worship in the list, except the church in glass the
  organiser named.
- GoatConf never pays for, books or guarantees a host's venue; the
  charter's four rules stay as they are.
- No added event at the same time as a session on Thursday or Friday,
  and none in Friday's 12:30 hour.
- No private persons' contact details; only what a venue publishes.

## Rabbit holes

- **Capacities.** Most cultural houses publish no seat counts. Ask the
  venues, or show "size unknown, ask the venue", rather than guess.
- **Photo picking.** Commons has photos of only a few venues, and the
  venues' own photos vary; picking a good one per place, as with the
  food, takes time. Start with the places most hosts will want.
- **The law.** The notice rules depend on whether an event aims at
  income and on draft laws whose fate is unknown. The guide should say
  "ask the venue, and when in doubt tell the police five to seven days
  ahead", and point to the law, not interpret edge cases.
- **Search without a build step.** Keep it to filters over a list already
  in the page; anything heavier pulls toward a framework the site does
  not have.
- **Keeping it current.** Bars change hands and websites lapse (Old Story
  Pub's old site now shows gambling content). Each record needs a
  checked date, and the hub should say when it was last checked.

## Appetite

Medium: the records and the hub page build on tools that already exist
for places and extensions; the guides are writing; the decisions (hours
off, wording on editions, which venues to arrange) are the organiser's.

## Success metrics

- The number of events people propose, and how many are accepted, by the
  end of April 2027, compared with today's one.
- How many proposals name a venue from the hub.
- Whether people asked at the event say they knew they could add
  something (a question in the feedback survey).

## Decision needed

Answered by [Make it yours: one hub at /extend](../adrs/make-it-yours-hub.md), accepted and built on 2026-10-23. The three questions this PRD left were answered on 2026-10-23
(`sources/conversations/2026-10-23--org--hosts-hub-approved.md`):

1. **The editions line** reads "Every GoatConf is shaped by who joins
   it.", on the hub and on the home page.
2. **The hub** is "Make it yours" at goatconf.com/extend; /extensions and
   /add redirect to it.
3. **An hour off is claimed through the same form** as any event, with
   the hour off as its time; the organiser accepts it like any other, and
   it shows on the hub and the program.

## Next step

The ADR, [Make it yours: one hub at /extend](../adrs/make-it-yours-hub.md),
records how; once the organiser approves it, the agent builds the venue
records, the hub, the guides, the redirects and the editions line.

## Sources

The organiser's four messages of 2026-10-23, the vision of 2026-10-07,
the extension ADR and its amendments, the venues research page and its
sources, and the prior art under `sources/web/models/` dated 2026-10-23,
as listed in the frontmatter.

## Related

- [Places in Tuzla where hosts could run an event](../tuzla/venues-for-hosts.md)
- [Extension slots and the record](extension-slots-and-the-record.md)
- [Activities: the lake and the town](activities-lake-and-town.md)
