---
title: "Keep a goat: a free tamagotchi of the painted goats on goatconf.com"
kind: pitch
status: superseded
superseded_by: org/prds/goat-tamagotchi-on-the-site.md
updated: 2026-10-28
appetite: small
confidence: low
affects:
  - org
sources:
  - sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-bet.md
  - sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md
  - sources/conversations/2026-10-27--org--goat-tricks.md
  - sources/conversations/2026-10-28--org--goat-says.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-24--org--foss-values-and-mit-licence.md
---

# Keep a goat: a free tamagotchi of the painted goats on goatconf.com

## Problem

Between now and 3 June 2027 the site gives a visitor few reasons to come
back: the program fills slowly, and a speaker is a name and a photo until
their session has a slot. The organiser left an idea for this on
2026-10-27: "tamagochi game as part of the conference, for each speaker.
folks can play and keep alive their favorite speaker"
(source: sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md;
[the idea page](../ideas/speaker-goat-tamagotchi.md)).

The pieces are already on the site. Every speaker has a painted goat; the
companion goat blinks, turns its head, hops, ducks and pops up, and since
2026-10-27 plays a trick when tapped and says a line in a bubble, a
speaker's goat something about their own work
(sources: sources/conversations/2026-10-27--org--goat-tricks.md,
sources/conversations/2026-10-28--org--goat-says.md). The painted scenes
include the goat eating burek, ćevapi and coffee, and a sleeping goat.

On 2026-10-28 the organiser asked whether this should be a separate phone
game sold for 0.99 euro to support the conference. The answer shaped here
is no, for four reasons (source: sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md):

- **The money does not add up.** Apple charges about 99 US dollars a year
  to publish and Google about 25 once; the stores keep about 15% of a sale
  and VAT comes off, leaving about 0.65 euro, so about 150 sales a year
  only cover Apple's fee, before any work.
- **The charter says no.** GoatConf's "content is never for sale" (the
  charter, as written on 2026-10-24; source: sources/conversations/2026-10-24--org--foss-values-and-mit-licence.md).
- **The speakers' goats depict real people**, who would have to agree to
  being in something sold.
- **Money to the organiser's business** is for its adviser to place: today
  only companies pay it, as online supporters, under a written agreement
  (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).

## Appetite

**Small**: about a week of work, mostly the agent's, with the organiser
reviewing it in the browser before it ships, as every goat change has
been (source: sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md).
The QR treats at the event and a support link are a second bet, in spring,
once this one has been played.

## Solution

Fat-marker, for a bet; the details are for a decision record after one.

- **Adopting.** A goat can be adopted where it already lives: tapping a
  goat offers "Keep me", and the plain and role goats can be adopted from
  the Stickers page. A speaker's goat can be adopted once that speaker has
  agreed. The adopted goat is the visitor's companion from then on: the
  goat that follows them down every page is theirs.
- **Its needs.** Three, shown in a small "Your goat" place reached from
  the goat itself: food, play and sleep. Feeding offers the painted Bosnian
  food, playing is the tricks it already has, and sleep is the sleeping
  goat. The needs drift slowly in real time, over a day, not an hour.
- **It never dies.** A neglected goat sits sulking, says "Baaa…" in its
  bubble and perks up when fed. Nothing is lost by being away.
- **The conference feeds it.** Reading its speaker's page, registering
  and sharing a card each cheer it up once. Its trip to Tuzla counts down
  to 3 June: as the day nears, it packs.
- **Where it lives.** In the visitor's own browser only, saved on their
  device, with no account and nothing sent anywhere. On Save-Data or a 2G
  connection, where the site shows no goat today, the game is not offered.

## Rabbit holes

- **Payments from individuals.** A "buy your goat a burek" link would be
  money from people, not companies, to the organiser's Austrian business.
  How that is invoiced and taxed is for the adviser, before any link.
- **Weight on a slow connection.** The game must load nothing until a
  visitor adopts, and reuse the sprite sheets the companion already loads.
- **Guilt.** A tamagotchi can nag. The needs drift slowly, the goat never
  dies, and nothing pings the visitor.
- **Speakers' consent.** Asking every speaker takes time; the game ships
  with the plain and role goats and adds a speaker's goat when they agree.
- **Clearing the browser** loses the goat. That is accepted, and said.

## No-gos

- No paid app, and nothing to buy inside the game.
- No accounts, no tracking, no server: everything stays in the visitor's
  browser.
- The goat never dies, and there are no notifications.
- No speaker's goat without that speaker's agreement.
- Nothing on the site promises the game before it is built.

## Related

- [The tamagotchi idea](../ideas/speaker-goat-tamagotchi.md): the idea this
  pitch shapes.
- [The goat mascot](../adrs/goat-mascot.md): the painted goats, the
  companion, its tricks and what it says.
- [Online supporters through the business](../adrs/online-supporters-through-the-business.md):
  the only way money reaches the organiser's business today.
