---
title: "Goatchi as a full game played with one goat, and more poses for every goat on the site"
kind: initiative
status: living
updated: 2026-10-31
appetite: big
confidence: medium
supersedes: org/pitches/goatchi-full-game.md
affects:
  - org
sources:
  - sources/conversations/2026-10-31--org--goatchi-how-app-and-reminders.md
  - sources/conversations/2026-10-31--org--goatchi-full-game-bet.md
  - sources/conversations/2026-10-31--org--goatchi-full-game.md
  - sources/conversations/2026-10-28--org--goatchi-ship.md
  - sources/conversations/2026-10-28--org--goatchi-challenge-mode.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-how.md
  - sources/conversations/2026-10-27--org--mascot-watercolour.md
  - sources/conversations/2026-10-27--org--speaker-goats.md
  - sources/conversations/2026-10-27--org--goats-on-photos-and-spots.md
  - sources/conversations/2026-10-24--org--tuesday-and-saturday-posts.md
---

# Goatchi as a full game played with one goat, and more poses for every goat on the site

## Objective

A visitor picks a goat on Goatchi and plays it from that day to 3 June 2027
as the same goat: it eats, sleeps, plays its own trick and shows its mood in
its own look, reaches milestones that bring postcards from Tuzla, packs in
the last week and arrives at GoatConf. On the same art, the site's other
goats (the speakers' goats, the goats on the food and Tuzla photos) gain
poses and moves, and Paul Campbell's goat is painted again in ginger.

## Background

Goatchi shipped on 2026-10-28 as a small bet on a page of its own
(sources: sources/conversations/2026-10-28--org--goat-tamagotchi-how.md,
sources/conversations/2026-10-28--org--goatchi-ship.md). An audit on
2026-10-31 found no console errors and no sideways scrolling, but a thin
game: a role goat turns into the plain goat while it eats or sleeps, the goat
smiles with a need nearly empty, play is one hop, nothing changes over weeks,
and on phones the game starts below the first screen
(source: sources/conversations/2026-10-31--org--goatchi-full-game.md).

The organiser asked for "a full game. Played end to end with the same goat
type", added the home page's goats ("Speaker goats for example... Goats on
food section... Tuzla images") and Paul Campbell's goat, which was painted
from a black and white photo and recoloured by hand, and held the Saturday
post of 31 October 2026 for Goatchi until it is final
(source: sources/conversations/2026-10-31--org--goatchi-full-game.md). They
bet on [the pitch](../pitches/goatchi-full-game.md) the same day
(source: sources/conversations/2026-10-31--org--goatchi-full-game-bet.md).
It stands on its own, as Goatchi does, not under the GoatConf 2027 epic.

The goats are painted in an image generator in the organiser's Chrome, a
sheet at a time; the sheets stay on the organiser's computer and the site's
tools cut the pictures it shows. The plan is still for an illustrator to
draw the final goat (source: sources/conversations/2026-10-27--org--mascot-watercolour.md).
On 2026-10-27 only five photos on the home page had a matching painted
scene (source: sources/conversations/2026-10-27--org--goats-on-photos-and-spots.md).

## Affected personas

- [Attendee](../../../.claude/personas/users/attendee.md), owning the need:
  someone deciding whether to come, or registered and waiting for June. A
  game they can play with one goat for seven months is a reason to come
  back, and its story ends where GoatConf begins.
- [Speaker](../../../.claude/personas/users/speaker.md), affected: their goat
  is a painting of them and gains poses on the site, published with a change
  on request (source: sources/conversations/2026-10-27--org--speaker-goats.md).
  It can be kept in Goatchi only once they agree.

## Now / Perceived / Target

- **Now.** Goatchi offers the plain goat and six role goats. Feeding shows
  the plain goat with burek, ćevapi or coffee, sleep the plain goat asleep,
  play a hop; the needs drift over a day and a half, the goat sulks below a
  quarter, and in challenge mode it wanders off after three days with every
  need empty. It counts the days to Tuzla and has no end
  (sources: sources/conversations/2026-10-28--org--goatchi-ship.md,
  sources/conversations/2026-10-28--org--goatchi-challenge-mode.md,
  sources/conversations/2026-10-31--org--goatchi-full-game.md). The speakers'
  goats peek, blink, turn and sit; five photos have a goat scene.
- **Perceived.** Goatchi is read as finished and ready to promote; the
  organiser now sees it as a first version.
- **Target.** Every act and mood shows the kept goat's own type. The goat
  has a story across the months to June, with milestones and postcards, and
  an ending on 3 June 2027. On phones the game is the first thing on the
  page. Every food and Tuzla photo has its goat, the speakers' goats have
  more than a peek and a sit, and Paul Campbell's goat is ginger in paint.

## Scope

- Eight poses for each of the seven goat types: eating, sleeping, playing
  its own trick, hungry, sulking, happy, hiking and packing for Tuzla.
- Moods chosen from the needs, shown in the goat's own look.
- Animations at rest (breathing, blinking, an ear) and for each act.
- Milestones at 7, 30 and 100 days kept, each unlocking a postcard from
  Tuzla; packing in the last week; arriving at GoatConf on 3 June 2027.
- Goats kept before this change keep their type, needs and days kept.
- On phones, with a goat kept, the game first and the three buttons on one
  row.
- Then, on the same art: more poses for the speakers' goats, a goat for
  every food and Tuzla photo on the home page, the companion using them, and
  Paul Campbell's goat painted again in ginger.
- Goatchi's post goes out only when the organiser calls the game final.

## No-gos

- Nothing to buy, no accounts, no tracking, no server, no notifications.
- The goat never dies; only a goat in challenge mode wanders off.
- No speaker's goat kept in Goatchi without that speaker's agreement.
- No streaks: milestones count days kept, never days in a row.
- No minigames: a trick is a picture and a move.
- The generators' sheets stay out of this repository.

## Rabbit holes

- **Drift between poses.** A generator can paint a different goat from one
  pose to the next; each type's sheet is checked against its reference, and
  a pose that drifts is redone or dropped.
- **The generator's daily limit** can make the art slower than the build.
- **The illustrator's redraw** grows with every pose added.
- **Weight.** Only the kept goat's pictures load on Goatchi, after it is
  picked; on the home page, new poses load no earlier than today's.

## Appetite

Big: about three to four weeks, most of it art, in two parts on the same
art: Goatchi first, then promoted; the home page's goats after
(source: sources/conversations/2026-10-31--org--goatchi-full-game.md).

## Success metrics

There is no tracking, so nothing counts players. The work is done when:

- For each of the seven goat types, every act and mood shows that type,
  never the plain goat in its place.
- A goat kept before the change is still the same goat after it, with its
  needs and days kept.
- Setting a goat's days kept to 7, 30 and 100 in the scripted audit unlocks
  each postcard once; setting the date to the last week shows it packing,
  and to 3 June 2027 shows it arriving.
- Goatchi before a goat is picked weighs no more than on 2026-10-31 (about
  531 KB), and picking adds no more than about 300 KB.
- The scripted goat audit (every page, at 360, 412, 768 and 1300 pixels)
  shows no console errors and no goat cut off.
- The organiser plays it end to end on their phone with one goat and calls
  it final; then Goatchi's post goes.
- The organiser approves Paul Campbell's goat in ginger, and every food and
  Tuzla photo on the home page has its goat.

## Dependencies

- The organiser's time in their Chrome for the generator sessions; the
  agent writes the prompts and cuts the sheets.
- `site/goatchi.js`, `tools/goatchi.py`, the companion in `site/album.js`
  and the cutting in `tools/goat_atlas.py`.

## Open questions

- Which generator paints best for this set: ChatGPT, used for the
  watercolour sheet, or Gemini, used for the photo scenes
  (sources: sources/conversations/2026-10-27--org--mascot-watercolour.md,
  sources/conversations/2026-10-27--org--goats-on-photos-and-spots.md).
- Whether the illustrator, once engaged, draws the whole set or only the
  base goat.

## Decision needed

The Tech Lead is asked to decide how the art is made and named (a sheet per
type, its reference, which poses get blink frames), how Goatchi's state
grows to carry milestones and postcards while keeping today's goats, how
moods are chosen from the needs, how the pictures load so the weight holds,
and how the companion and the home page take up the new poses after Goatchi
ships.

## Decision

The Tech Lead's answer is [the decision record](../adrs/goatchi-full-game.md):
one image per pose cut by the atlas, a sheet per type with the plain goat's
as the reference, moods from the needs, postcards from photos the site has,
today's goats carried over, and Goatchi installable, with reminders the
player turns on, made on the device.

## Amendments

- **2026-10-31, installable, with opt-in reminders.** While the decision
  record was written, the organiser added Goatchi installable on its own,
  and reminders made on the device that the player turns on, where the
  browser supports them. The no-go "no notifications" now reads: no
  notifications unless the player turns them on, and never from a server.
  The organiser asked that the notifications be properly tested, so the work
  is also done when the notification check passes a unit test, fires in
  headless Chromium with the shown notification read back, and works by hand
  on the organiser's Android phone and on desktop Chrome, installed
  (source: sources/conversations/2026-10-31--org--goatchi-how-app-and-reminders.md).
