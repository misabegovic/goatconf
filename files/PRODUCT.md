# Product

<!-- impeccable:product-schema 1 -->

This file summarises what the brain holds, for impeccable. The brain stays
the source of truth: [the facts page](wiki/org/goatconf-2027.md), [the
epic](wiki/org/epics/goatconf-2027.md), the PRDs and ADRs under
`wiki/org/` (read each with its amendments), and the personas under
`.claude/personas/`. Brought up to date on 2026-10-14.

## Platform

web

## Stack

Static HTML and CSS, no build step, kept in `site/` and published at
goatconf.com on GitHub Pages by one Actions workflow on every merge to
`main` (ADR `wiki/org/adrs/goatconf-ba-and-google-forms.md`). Some parts
are generated from records by the scripts in `tools/` and checked by the
local CI: the program, the speakers and supporters pages, the extensions
page, the places on the travel page, the top bar, the link previews and
the files for agents.

## Users

First: **the would-be attendee**, deciding whether to come to Tuzla in June
2027. They are open and multi-discipline (engineers, designers, product
people, founders: people who build and sell software), not tied to any
language or stack, English-speaking, and need to know when, where, what
the trip costs, and how to register.
Second, each with a clear door: speakers (an open call the organiser
judges), event hosts (anyone proposing an evening event, meetup, trip,
hike, hackathon or other event around the conference), supporters
(companies supporting GoatConf online), volunteers.

## Product Purpose

GoatConf is a free conference in Tuzla, Bosnia and Herzegovina, on 3 to 5
June 2027, hosted by IPI Academy. The organiser's goal: "get great minds
together in an affordable environment, hang out, spend time together,
learn, share experiences". The website exists to make a stranger decide to
come, register, and know how to get there. The first edition expects 120
to 300 people.

## Positioning

A minimal core others extend, "like the Pi agent". Two core days,
Thursday 3 and Friday 4 June, run one-hour sessions in all seven IPI
rooms at once, with an hour off after each session on Freedom Square.
Saturday 5 June is the community day: the lake day and the goat hunt the
organiser plans, and the events hosts add. Named after Tuzla's goat: the
man who hid his goat when Austria-Hungary banned them, and the saying "The
whole of Tuzla milked one goat".

## Operating Context

Pages are written in this repository; every merge to `main` publishes the
site, and each merge is the organiser's act. Registration is on Luma.
Talk proposals, proposed events and contact (including code-of-conduct
reports) arrive through Google Forms; events can also come as pull
requests. Visitors arrive mostly on phones from social posts and
newsletters.

## Capabilities and Constraints

- Free to attend. Registration on Luma has no limit, and the organiser
  approves each one, usually within a few days. Seats in each room are
  first come, first served at the door; registering for single sessions
  comes later, with the tool not decided.
- Thursday runs 10:00 to 17:00. Friday runs 09:30 to 16:30, so the break
  at 12:30 covers Friday prayer and lunch.
- English only.
- Food and drink are never paid by the organiser: people pay their own.
- Speakers pay their own travel; the organiser may refund some or all of
  it if the budget allows, never promised. Every accepted speaker's
  profile is published and promoted; this is not optional.
- Supporters are online only: one level, 500 EUR, invoiced by the
  organiser's Austrian business, nothing at the venue, and they never buy
  content. A speaker's company that covers their travel is listed the
  same way.
- The budget is private: no budget page, and the site never mentions it.
- GoatConf does not record the talks; people who come may record or
  podcast.
- Pages: home, program, register, propose a talk, travel and stay,
  speakers, propose an event, supporters, extensions, charter, code of
  conduct, accessibility, contact, brand.

## Brand Commitments

- Name: GoatConf. The mark is a seal with the EuRuKo 2024 goat: "the one
  that feeds the community".
- The design is the sticker album in `DESIGN.md`: a decided fact is a
  sticker, anything undecided an empty printed slot.
- The goat appears everywhere and is playful. It never covers the facts,
  never replaces text a screen reader needs, and never makes the code of
  conduct read as a joke.
- Voice: plain language, one idea per sentence, common words; no em
  dashes. Dates read "3–5 June 2027" and "Thursday 3rd June".
- No photo credits on the site.

## Evidence on Hand

- The goat story: `sources/web/funding/euruko-2024-why-the-goat.md`.
- Tuzla facts and prices: `wiki/org/tuzla.md`; places to eat and stay:
  `places/places.yml`; venue: `wiki/org/ipi-academy.md`.
- Code of conduct text: `sources/web/coc/rubyconf-austria-code-of-conduct.md`.
- Photos of the city, the food, IPI's lecture hall and the organiser's past
  conferences, under `site/img/`. The food photos are not freely licensed
  and come down if an owner asks.
- No speakers, supporters, sessions or extensions exist yet. None may be
  invented.

## Product Principles

- The trip is sold before the lineup: Tuzla, the lakes, the food, the low
  cost.
- Facts first: when, where, how to register, what it costs.
- Honest about what is undecided; nothing announced before it is true.
- Open doors: anyone can propose a talk or an event, and the site shows
  how.

## Accessibility & Inclusion

The ground floor and first floor are step-free, and computer centre 1 on
the first floor is reached by the lift. Computer centre 2 and the rooms
above the first floor are not step-free. Guide dogs cannot come in.
Accessible toilets probably exist but are not verified. The site
publishes what is known and says what is not. Pages should meet WCAG 2.2
AA and work on slow mobile connections.
