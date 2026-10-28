---
title: "Keep a goat: a free tamagotchi of the painted goats on goatconf.com"
kind: initiative
status: living
updated: 2026-10-28
appetite: small
confidence: medium
supersedes: org/pitches/goat-tamagotchi-on-the-site.md
affects:
  - org
sources:
  - sources/conversations/2026-10-28--org--goat-tamagotchi-bet.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-how.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md
  - sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md
  - sources/conversations/2026-10-27--org--goat-tricks.md
  - sources/conversations/2026-10-28--org--goat-says.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
---

# Keep a goat: a free tamagotchi of the painted goats on goatconf.com

## Objective

A visitor can adopt one of GoatConf's painted goats on the site and keep it
in their own browser, feeding it, playing with it and letting it sleep, so
that they have a light, friendly reason to come back before 3 June 2027.

## Background

The organiser left the idea on 2026-10-27, "tamagochi game as part of the
conference, for each speaker. folks can play and keep alive their favorite
speaker" (source: sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md),
asked on 2026-10-28 whether it should be a paid phone game, chose a free
game on the site instead, shaped it as a small pitch, and bet on it the same
day, on its own rather than under the GoatConf 2027 epic
(sources: sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md,
sources/conversations/2026-10-28--org--goat-tamagotchi-bet.md;
[the pitch](../pitches/goat-tamagotchi-on-the-site.md)).

The reasons against a paid app are in the pitch: the store costs outweigh
0.99 euro sales, the charter says GoatConf's content is never for sale, the
speakers' goats depict real people, and money from individuals to the
organiser's business is for its adviser to place
(source: sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md).

## Affected personas

- [Attendee](../../../.claude/personas/users/attendee.md): someone deciding
  whether to come, or already registered and waiting for June. Today the
  site gives them little to come back for until the program fills. With
  this, they keep a goat that is glad to see them, cheers up when they read
  a speaker's session, and packs for Tuzla as the day nears.
- [Speaker](../../../.claude/personas/users/speaker.md), affected: their
  goat is a painting of them. It can be adopted only once they agree.

## Now / Perceived / Target

- **Now.** One companion goat moves between the goats' places on every page,
  in the role of the place or as a speaker's own goat. It blinks, turns its
  head, hops, ducks and pops up; tapped, it plays a trick and says a line in
  a bubble, and a speaker's goat also says something about their own work.
  It is not offered on Save-Data or a 2G connection, and with reduced motion
  it only appears and speaks
  (sources: sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md,
  sources/conversations/2026-10-27--org--goat-tricks.md,
  sources/conversations/2026-10-28--org--goat-says.md). Painted scenes show
  the goat with burek, ćevapi and coffee, and a sleeping goat exists. Nothing
  about the goat is kept between visits.
- **Perceived.** The goat is read as a fun mascot that does tricks; nobody
  expects it to remember them.
- **Target.** A visitor taps a goat, chooses "Keep me", and from then on the
  companion on every page is their goat. A small "Your goat" place, opened
  from the goat, shows how fed, played with and rested it is, and lets them
  feed it, play and put it to sleep. Its needs drift slowly over a day; left
  alone it sulks and says "Baaa…", and never dies. Reading its speaker's
  page, following the link to register and downloading or sharing a card
  each cheer it up once. As 3 June 2027 nears, it packs for Tuzla. All of it
  is saved in the visitor's browser only.

## Scope

- Adopting a goat from the companion ("Keep me"), and from the Stickers page
  for the plain and role goats.
- The adopted goat becomes the visitor's companion on every page, in its own
  look rather than each place's role.
- A "Your goat" place with three needs (food, play, sleep), feeding from the
  painted food, playing with the tricks it has, and sleep with the sleeping
  goat.
- Needs that drift slowly in real time; a sulking state; no death.
- One-time cheers for reading its speaker's page, following the register
  link, and downloading or sharing a card; a countdown to 3 June 2027.
- Letting a visitor give their goat up or swap it for another.
- Speakers' goats adoptable only once each speaker has agreed, the agreement
  recorded in the brain.

## No-gos

- No paid app, and nothing to buy inside the game.
- No accounts, no tracking, no server: nothing about a visitor's goat leaves
  their browser.
- The goat never dies, and there are no notifications.
- No speaker's goat without that speaker's agreement.
- No QR treats at the event and no support link in this bet: those are a
  second bet in spring.
- Nothing on the site promises the game before it ships.

## Rabbit holes

- **Payments from individuals.** Any "buy your goat a burek" link waits for
  the organiser's adviser.
- **Weight.** If the game needs more than the sheets the companion already
  loads, plus a small script fetched only on adoption, stop and re-pitch.
- **Guilt.** If tuning the needs turns into a balancing exercise, keep them
  slow and forgiving and stop.
- **Knowing what a visitor did elsewhere.** The site cannot see a Luma
  registration or a post on another site; following the link counts, and
  nothing more is attempted.

## Appetite

Small: about a week of work, mostly the agent's, with the organiser
reviewing it in the browser before it ships
(source: sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md).

## Success metrics

There is no tracking, so nothing counts players. The work is done when:

- A visitor who never adopts a goat downloads nothing more than today.
- An adopted goat is still theirs, with its needs where they left them,
  after closing the browser and coming back.
- A goat left alone for a week is sulking, not gone, and cheers up when fed.
- The scripted goat audit (every page, at 360, 412, 768 and 1300 pixels)
  shows no console errors and no goat cut off, with and without an adopted
  goat.
- The organiser plays it on their phone and approves it.

## Dependencies

- The organiser asks each speaker whether their goat may be adopted; that
  message is the organiser's to send, and the agent drafts it.
- The companion goat in `site/album.js` and the sheets built by
  `tools/goat_atlas.py`.

## Open questions

- Which speakers agree, and when; until then only the plain and role goats
  can be adopted.
- Whether the companion keeps changing role at each place once a goat is
  adopted, or is always the adopted goat.

## Decision needed

The Tech Lead is asked to decide how the game is built: whether it extends
the companion in `site/album.js` or loads as its own small script on
adoption; how the goat's state is kept in the browser and how its needs
drift; what the "Your goat" place is (a panel over the page or a page of its
own); and where each speaker's agreement is recorded.

## Decision

The organiser approved this plan on 2026-10-28 and chose to build it as a
page of its own, fully separate from the rest of the site: adoption, the
needs and the cheers all happen on `goatchi.html`, named Goatchi, and the companion goat is
unchanged, so two Scope bullets (adopting from the companion and the
Stickers page, and the adopted goat following the visitor) are dropped
([the ADR](../adrs/goat-tamagotchi-on-the-site.md); source: sources/conversations/2026-10-28--org--goat-tamagotchi-how.md).
