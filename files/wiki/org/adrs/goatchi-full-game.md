---
title: "Goatchi as a full game: one image per pose from the atlas, a story to Tuzla, installable, with opt-in reminders made on the device"
kind: decision
status: accepted
updated: 2026-10-31
confidence: medium
affects:
  - org
sources:
  - wiki/org/prds/goatchi-full-game.md
  - sources/conversations/2026-10-31--org--goatchi-full-game-adr-approved.md
  - sources/conversations/2026-10-31--org--goatchi-full-game-built.md
  - site/goatchi-sw.js
  - site/goatchi.webmanifest
  - tests/test_goatchi_app.py
  - tests/browser/goatchi-reminders.mjs
  - sources/conversations/2026-10-31--org--goatchi-how-app-and-reminders.md
  - sources/conversations/2026-10-31--org--goatchi-full-game-bet.md
  - sources/conversations/2026-10-31--org--goatchi-full-game.md
  - sources/conversations/2026-10-28--org--goatchi-ship.md
  - sources/conversations/2026-10-27--org--mascot-watercolour.md
  - sources/conversations/2026-10-27--org--speaker-goats.md
  - sources/conversations/2026-10-27--org--goats-on-photos-and-spots.md
  - tools/goat_atlas.py
  - tools/goatchi.py
  - site/goatchi.js
  - site/album.js
---

# Goatchi as a full game: one image per pose from the atlas, a story to Tuzla, installable, with opt-in reminders made on the device

## Context

[The plan](../prds/goatchi-full-game.md), approved on 2026-10-31, makes
Goatchi a game played from the day a goat is picked to 3 June 2027 with the
same goat, then gives the site's other goats the same art
(source: sources/conversations/2026-10-31--org--goatchi-full-game-bet.md).
It asks how the art is made and named, how the game's state grows while
keeping today's goats, how moods are chosen and how the weight holds.

Today the painted masters stay on the organiser's computer and
`tools/goat_atlas.py` cuts them: the peeking goats into sprite sheets, and a
goat shown on its own into one image of about 30 KB. Goatchi uses those
single images: the seven goats to pick, three food scenes and the sleeping
goat, all of the plain goat except the seven picks
(source: tools/goat_atlas.py; sources/conversations/2026-10-28--org--goatchi-ship.md).
The goat is kept in the browser's local storage, written only once a goat is
picked (source: site/goatchi.js).

While this record was written the organiser chose how the art is served, and
added two things: Goatchi installable on its own, and reminders made on the
device only, which they turn on themselves
(source: sources/conversations/2026-10-31--org--goatchi-how-app-and-reminders.md).
The plan's no-go "no notifications" is amended to match.

## Decision

1. **One image per pose, from the atlas.** Each of the seven goat types (the
   goat, the host, the coder, the speaker, the cook, the pirate, the shy one)
   has eight poses: eating, sleeping, playing, hungry, sulking, happy, hiking
   and packing. Each is a master named for its type and pose, such as
   `pirate-eating`, and the atlas cuts each into one image, as it cuts
   Goatchi's goats today. The type's current painted goat stays its resting
   look and keeps its blink.
2. **The art, a sheet per type.** The agent writes one prompt per type; the
   organiser runs it in the generator in their Chrome. The plain goat's sheet
   comes first and is the reference given with every other sheet, beside the
   type's current picture. The agent cuts each sheet into masters on the
   organiser's computer, and a pose that drifts from its type is painted
   again or left out. The sheets and masters stay out of the repository, as
   now (source: sources/conversations/2026-10-27--org--mascot-watercolour.md).
3. **Moods from the needs.** Below a quarter on any need, the goat sulks; with
   food lowest and under about half, it looks hungry; with every need high,
   it looks happy; otherwise it rests. A bored or sleepy goat says so in its
   bubble rather than in a picture of its own.
4. **A story to Tuzla.** The kept goat counts days kept, never days in a row.
   At 7, 30 and 100 days it sends a postcard, from photos the site already
   has: the salt lakes, the fountain on Salt Square, and the Korzo. The
   postcards stay in a row under the goat. In the last seven days before
   3 June 2027 it shows packing; from that day it says it has arrived.
5. **Today's goats carry over.** The stored goat gains a version and the
   postcards it has; a goat kept before the change is read as the same
   goat, with its needs, days kept and challenge mode, and receives any
   postcard its days have already earned.
6. **Weight.** Before a goat is picked the page loads what it loads today.
   After the pick, the kept type's eight images load once, about 240 KB, and
   the browser keeps them.
7. **Phones.** With a goat kept, the game comes first and the page's large
   goat steps back; the three buttons sit on one row.
8. **Installable, for Goatchi only.** A web manifest and a service worker
   whose scope is the Goatchi page alone let a visitor add Goatchi to their
   home screen, open it like an app and play offline. No other page
   registers a worker.
9. **Reminders, opt-in and made on the device.** Where the browser supports
   periodic background sync and Goatchi is installed, a "Tell me when my
   goat needs me" switch, off by default, asks for notification permission
   and registers a check about twice a day at most. While it is on, Goatchi
   copies the goat into the browser's IndexedDB, which the worker can read;
   the worker works out the needs and shows one notification when the goat
   is sulking, no more than once a day. Turning it off removes the check and
   the copy. Nothing is sent anywhere. Where the browser lacks it (iPhone,
   Firefox), the switch does not appear and the page says nothing about it.
10. **Tested before it ships.** Notifications are tested three ways: the
    check's decision (notify or not, from a goat's state and the last time it
    notified) as a unit test over hungry, sulking, already-told and turned-off
    goats; in headless Chromium, with notifications permitted, the periodic
    sync fired on purpose through the browser's developer protocol and the
    shown notifications read back from the worker; and by hand on the
    organiser's Android phone and on desktop Chrome, installed, firing the
    check from Chrome's developer tools.
11. **Then the site's other goats, on the same art.** The speakers' goats
    gain a wave, a jump and their own trick, named for each speaker and pose
    and loaded after the page as their turned heads are; every food and
    Tuzla photo on the home page gets its scene in the atlas's photo table;
    the companion in `site/album.js` uses them; Paul Campbell's goat is
    painted again in ginger under the same names, so nothing that places it
    changes (source: sources/conversations/2026-10-27--org--speaker-goats.md).

Scope check: every bullet of the plan's Scope is carried above, and the two
additions (installable, reminders) are the organiser's of 2026-10-31.

## Alternatives

- **One sheet per goat type.** One download instead of eight at about the
  same weight, like the companion's peeking sheets; but repainting one pose
  rebuilds the sheet, and scenes of different sizes pack poorly. Not chosen
  (source: sources/conversations/2026-10-31--org--goatchi-how-app-and-reminders.md).
- **Animate parts of fewer paintings.** Cutting each goat into head, ears and
  eyes and posing them in code needs fewer paintings, but the watercolour
  goats are not painted in layers, and goats posed in code look stiff. Not
  chosen.
- **Reminders through Web Push.** Reaches iPhone once installed, and times
  reminders exactly, but needs a server that keeps an identifier for each
  device, against the plan's no server and no tracking. Not chosen.
- **A browser extension.** Reminds on the device without a server, but runs
  on computers, not phones, needs a store listing and is a second codebase.
  Not chosen.
- **Do nothing.** Promote Goatchi as it is. Not chosen: the organiser wants
  it final before it is promoted.

## Consequences

- The art takes several generator sessions on the organiser's time and
  daily limit, and grows the illustrator's eventual redraw.
- A service worker is a new moving part: a stale worker can serve an old
  Goatchi. Its cache carries the same version stamp as the page's script,
  so a new build replaces it.
- Reminders reach only installed Goatchi on Chromium browsers, at times the
  browser picks; the page promises nothing more.
- The plan's no-go "no notifications" now reads: no notifications unless
  the player turns them on, and never from a server.
- Goatchi's post waits until the organiser calls the game final.

## Amendments

- **2026-10-31, the reminder names the need, and says when a goat leaves.**
  The one reminder names the need the goat lacks most ("The pirate is
  hungry", "wants to play", "is sleepy"), still at most once a day, and a
  challenge goat that wanders off is reported once, with how long it was
  kept. The story moments (postcards, packing, GoatConf day) bring no
  notification (source: sources/conversations/2026-10-31--org--goatchi-full-game-built.md).
- **2026-10-31, each need at its own speed.** Food empties over a day, play
  over a day and a half and sleep over two days, in the page and the worker
  alike, so a player who comes once a day keeps the goat happy
  (source: sources/conversations/2026-10-31--org--goatchi-full-game-built.md).
- **2026-10-31, a Goatchi section on the home page.** The first Goatchi
  decision kept the game on its own page with a footer link only; the
  organiser chose a section near the bottom of the home page, live with this
  release (source: sources/conversations/2026-10-31--org--goatchi-full-game-built.md).

## Linked PRD

[Goatchi as a full game played with one goat, and more poses for every goat on the site](../prds/goatchi-full-game.md)

## Build notes

Built on 2026-10-31 and shipped in two pull requests: Goatchi installable with
its reminders, then the game (source: sources/conversations/2026-10-31--org--goatchi-full-game-built.md).

- **The art.** Fourteen 2 by 2 sheets in ChatGPT, two per type rather than one
  of eight, so each pose is painted large enough to stay sharp on a phone; the
  Free plan stopped at three a day and the organiser started a Plus trial for
  the rest. The plain goat needed four new poses: its eating, sleeping, happy
  and hiking poses are the burek, ćevapi and coffee scenes, the sleeping goat,
  the jumping goat and the hike painted before. Each sheet is cut by figure,
  not by grid: the background is removed from the whole sheet and each half
  splits at the emptiest row or column near its middle, so a horn reaching
  over the middle stays on its goat; two sheets needed a one-line override.
  A fruit logo on the coder's laptop was painted out, and every later prompt
  asked for no logos. Fifty-two masters, about 30 KB each on the site.
- **The postcards** are the salt lakes, the fountain on Freedom Square (the
  photo is of Freedom Square, not Salt Square as written above) and the
  Korzo, each with "Photo: Grad Tuzla".
- **The service worker** fetches the network first and keeps the last copy for
  offline, instead of a cache stamped with the script's version: Goatchi is
  always the newest build when online, and a stale worker cannot hold an old
  one.
- **No blink yet.** Goatchi's poses have no closed-eye frames; petting,
  blinking and more moves are left for the next animation pitch, on the
  organiser's choice.
- **Not done in this build:** the speakers' goats, the food and Tuzla photo
  goats, and Paul Campbell's goat in ginger, which come next on the same art.

### Success metrics, checked

- "For each of the seven goat types, every act and mood shows that type, never the plain goat in its place." **met**: every pick on site/goatchi.html carries eight poses of its own type (counted on the built page), and the scripted game audit of the host showed its own picture resting, happy, hungry, sulking, eating, playing, asleep, packing and hiking (2026-10-31).
- "A goat kept before the change is still the same goat after it, with its needs and days kept." **met**: a stored goat without postcards loads as the same goat with its needs and days, and earns the postcards its days have at once (scripted game audit, 2026-10-31).
- "Setting a goat's days kept to 7, 30 and 100 in the scripted audit unlocks each postcard once; setting the date to the last week shows it packing, and to 3 June 2027 shows it arriving." **met**: 31 days kept showed two postcards, the browser clock at 30 May 2027 showed the packing pose and at 3 June 2027 the happy pose saying it is GoatConf (2026-10-31).
- "Goatchi before a goat is picked weighs no more than on 2026-10-31 (about 531 KB), and picking adds no more than about 300 KB." **met**: no pose loads before a pick (the requests show none); picking a role goat loads its eight poses, 280 to 308 KB, the host's a little over; the plain goat's four new poses are 150 KB (2026-10-31).
- "The scripted goat audit (every page, at 360, 412, 768 and 1300 pixels) shows no console errors and no goat cut off." **not checked**: Goatchi was audited at 390 and 1300 pixels with no console errors and no sideways scrolling; the audit of every page at four widths runs with the site's other goats, next.
- "The organiser plays it end to end on their phone with one goat and calls it final; then Goatchi's post goes." **not checked**: due once this is live, with the hands-on test of installing and reminders on the organiser's Android phone.
- "The organiser approves Paul Campbell's goat in ginger, and every food and Tuzla photo on the home page has its goat." **not checked**: the second part of this work, next.
