---
kind: source
source_kind: doc
source_path: /home/muhamed/projects/tt/goatconf/files/PRODUCT.md
ingested_at: 2026-10-08
summary: goatconf product direction: what GoatConf is (one-day Ruby-flavoured conference in Tuzla, June 2027, IPI Academy, free, 120-300 people) and the product bets.
---

# PRODUCT.md

```
# Product

<!-- impeccable:product-schema 1 -->

This file summarises what the brain holds, for impeccable. The brain stays
the source of truth: [the facts page](wiki/org/goatconf-2027.md), [the
epic](wiki/org/epics/goatconf-2027.md), the PRDs and ADRs under
`wiki/org/`, and the personas under `.claude/personas/`.

## Platform

web

## Stack

Static HTML and CSS, no build step, kept in `site/` and copied as they are
into muhamed.at/goatconf (ADR `wiki/org/adrs/design-with-impeccable.md`).
The one generated part is the extension list, built from the records in
`extensions/` before a copy; the budget page shows `site/ledger.csv`.
Whether muhamed.at serves a plain HTML folder as it is is undecided.

## Users

First: **the would-be attendee**, deciding whether to come to Tuzla in June
2027 (organiser's answer, 2026-10-07). They are open and multi-discipline
(engineers, designers, product people, founders), English-speaking, and
need to know when, where, what the trip costs, and how to register.
Second, each with a clear door: speakers (an open call plus one or two
invited), extension hosts (anyone adding a workshop, meetup, hub or
activity), supporters (companies or people funding a named item),
volunteers.

## Product Purpose

GoatConf is a free conference in Tuzla, Bosnia and Herzegovina, in the
first or second week of June 2027, hosted by IPI Academy. The organiser's
goal: "get great minds together in an affordable environment, hang out,
spend time together, learn, share experiences". The website exists to make
a stranger decide to come, register, and know how to get there; success is
a full hall (about 120) and a waiting list.

## Positioning

A minimal core others extend, "like the Pi agent": one core day of three to
four talks in one room, with long breaks on Freedom Square, and everything
else (workshops, fringe events, the lake day, a town-wide goat hunt) added
by hosts. Named after Tuzla's goat: the man who hid his goat when
Austria-Hungary banned them, and the saying "The whole of Tuzla milked one
goat". No money passes through the organiser, and every euro is public.

## Operating Context

Pages are written in this repository and copied into muhamed.at/goatconf
by the organiser; each publish is the organiser's act. Registration and
the email list are on Luma; talks and extension submissions arrive through
Google Forms; extensions are also pull requests. Visitors arrive mostly on
phones from social posts and newsletters.

## Capabilities and Constraints

- Free to attend; registration capped at the hall, about 120, with a
  waiting list; opens when IPI confirms the date in writing.
- Dates undecided: six options in 1 to 13 June 2027 are with IPI. Until
  confirmed, the site says "June 2027" and must not announce a date.
- English only.
- Food and drink are never paid by the organiser: people pay their own or
  a supporter pays a café directly.
- Speakers pay their own travel; a grant exists only if a supporter funds
  it.
- No microphone or recording in the hall.
- Pages: home, program, travel and stay, accessibility, code of conduct,
  extensions, supporters, budget, contact. v1 needs only when, where, who,
  why, the code of conduct and the budget.

## Brand Commitments

- Name: GoatConf.
- The goat appears everywhere and is playful (organiser's choice,
  2026-10-07): mark, favicon, illustrations, badges, signs, social cards,
  slides. It never covers the facts, never replaces text a screen reader
  needs, and never makes the code of conduct or the budget read as a joke.
- Voice: plain language, one idea per sentence, common words; no em dashes.
- The pages sit inside muhamed.at, so they must not fight that site.

## Evidence on Hand

- The goat story: `sources/web/funding/euruko-2024-why-the-goat.md`.
- Tuzla facts and prices: `wiki/org/tuzla.md`; venue: `wiki/org/ipi-academy.md`.
- Code of conduct text: `sources/web/coc/rubyconf-austria-code-of-conduct.md`.
- No speakers, supporters, photos, testimonials, logos or past editions
  exist yet. None may be invented.

## Product Principles

- The trip is sold before the lineup: Tuzla, the lake, the low cost.
- Facts first: when, where, how to register, what it costs.
- Honest about what is undecided; nothing announced before it is true.
- Open doors: anyone can extend GoatConf, and the site shows how.
- Every euro in the open.

## Accessibility & Inclusion

The main hall and first floor are step-free; an accessible toilet is
unconfirmed. The site publishes what is known and says what is not. Pages
should meet WCAG 2.2 AA and work on slow mobile connections.

```
