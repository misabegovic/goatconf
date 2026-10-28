---
title: "Goatchi, a page of its own: goatchi.html, built by a tool, with its own small script"
kind: decision
status: accepted
updated: 2026-10-28
confidence: medium
affects:
  - org
sources:
  - wiki/org/prds/goat-tamagotchi-on-the-site.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-how.md
  - sources/conversations/2026-10-28--org--goatchi-adr-approved.md
  - sources/conversations/2026-10-28--org--goatchi-ship.md
  - tools/goatchi.py
  - site/goatchi.js
  - tests/test_goatchi.py
  - sources/conversations/2026-10-28--org--goat-tamagotchi-bet.md
  - sources/conversations/2026-10-28--org--goat-tamagotchi-pitch.md
  - sources/conversations/2026-10-27--org--goat-tricks.md
  - sources/conversations/2026-10-28--org--goat-says.md
---

# Goatchi, a page of its own: goatchi.html, built by a tool, with its own small script

## Context

The organiser bet on a free tamagotchi of the painted goats and approved its
plan ([the PRD](../prds/goat-tamagotchi-on-the-site.md); sources:
sources/conversations/2026-10-28--org--goat-tamagotchi-bet.md,
sources/conversations/2026-10-28--org--goat-tamagotchi-how.md). The plan
asks the Tech Lead how it is built: inside the companion goat or beside it,
how the goat's state is kept, what the "Your goat" place is, and where each
speaker's agreement is recorded.

The site is plain HTML and CSS written by tools under `tools/`, each page
part between generated-part markers, and every page is checked by
`tools/site.py check`. The companion goat is one script, `site/album.js`,
loaded on every page with goats; the Host an event page already loads a
second script of its own, `site/extend.js`, so a page with its own script
is an established pattern. Pages the site generates, such as the Stickers
page, are written by a tool with `frame.page()` and checked by the same
tool with `--check`.

## Decision

On the organiser's choice, the game is **a page of its own, fully
separate** from the rest of the site
(source: sources/conversations/2026-10-28--org--goat-tamagotchi-how.md).

- **The name.** Goatchi: "Goatchi: keep a GoatConf goat". The page may
  describe it as a little game like a tamagotchi, but the name does not use
  "Tamagotchi", a registered trademark of Bandai
  (source: sources/conversations/2026-10-28--org--goat-tamagotchi-how.md).
- **The page.** `site/goatchi.html`, written and checked by a new tool,
  `tools/goatchi.py`, with `frame.page()`, and built and checked in
  `tools/site.py`'s order like the other generated pages. It lists the goats
  that can be adopted: the plain goat, the role goats, and each speaker's
  goat whose speaker has agreed.
- **Its script.** `site/goatchi.js`, loaded only on that page. It keeps the
  game's state and draws the goat, its needs and its moves. The companion in
  `site/album.js` is unchanged, and the game's goats use their own class so
  the companion does not treat them as its places.
- **The state.** One small record in the visitor's browser storage: which
  goat, when it was adopted, and for each need its value and when it was
  last set. A need's value now is worked out from the time passed whenever
  the page is opened, so nothing runs while the visitor is away. Needs
  drift from full to empty over about a day and a half. Below a quarter the
  goat sulks and says "Baaa…"; at empty it stays sulking; it never dies.
  Nothing is sent anywhere.
- **The needs.** Food, play and sleep. Feeding shows the painted goat with
  burek, ćevapi or coffee, from the scenes sheet already on the site;
  playing makes it do a trick; sleep shows the sleeping goat.
- **The cheers.** Links on the goat page itself: to its speaker's page (for
  a speaker's goat), to Register, and to the speaker's share card or the
  Stickers page. Following each one cheers the goat up once.
- **The countdown.** The page shows the days left to 3 June 2027, and the
  goat says so in its bubble.
- **Giving it up.** The page lets the visitor let their goat go or swap it
  for another, after a confirmation on the page itself.
- **Speakers' agreement.** A `goat_keep: yes` field in the speaker's own
  record under `speakers/`, set when the speaker agrees, with their yes kept
  as a source. `tools/speakers.py check` accepts it, and `tools/goatchi.py`
  offers only those speakers' goats.
- **The way in.** One link in every page's footer and the home page's back
  cover, "Goatchi", added when the page ships.

Scope check against the PRD's seven Scope bullets: four carried (the Goatchi
page and its three needs; drift, sulking and no death; give up or
swap; speakers only with agreement), one carried in a changed form (the
cheers and the countdown, as links and a counter on the goat page), and two
dropped on the organiser's choice of a fully separate page: adopting from
the companion and from the Stickers page (adoption happens on the goat page
only), and the adopted goat becoming the companion on every page.

## Alternatives

- **A small extra script beside the companion**, the agent's recommendation:
  album.js offers "Keep me" when a goat is tapped, the game loads only on
  adoption, and the adopted goat follows the visitor on every page. It kept
  the plan's heart, a goat that follows you, but touches every page; the
  organiser chose a page of its own.
- **All of it in album.js.** The least code, but every visitor would
  download the game, against the plan's first success metric.
- **A page of its own, connected**: album.js notes a speaker's page read, a
  register link followed or a card shared, and tapping a goat links to the
  page. The organiser chose fully separate instead.
- **Do nothing.** The plan stays on the shelf; the pitch and the reasons
  against a paid app stay recorded.

## Consequences

- Pages other than the goat page download nothing new; only the footer
  gains a link. The plan's first success metric holds by construction.
- The goat does not follow the visitor; they come back to the goat page to
  see it. That is the trade the organiser made for a separate page.
- The game's moves are its own small set in `site/goatchi.js`, a little like
  the companion's, rather than shared with album.js.
- The speaker records gain an optional field, set only from a speaker's
  yes; the agent drafts the message asking for it, and the organiser sends
  it.
- Clearing the browser loses the goat; the page says so.
- No new painted art is needed: the goats, the food scenes and the sleeping
  goat exist.

## Linked PRD

[Keep a goat: a free tamagotchi of the painted goats on goatconf.com](../prds/goat-tamagotchi-on-the-site.md)

## Build notes

Built and shipped on 2026-10-28 (source: sources/conversations/2026-10-28--org--goatchi-ship.md).

- `tools/goatchi.py` writes `site/goatchi.html` with `frame.page()`, built
  and checked in `tools/site.py`'s order after the Stickers page; the page
  loads `site/goatchi.js`, stamped like the other scripts in `tools/meta.py`.
- The goats are single images built by `tools/goat_atlas.py` from the
  painted masters: the plain sitting goat, six role goats (the host, the
  coder, the speaker, the cook, the pirate and the shy one in a basket), the
  burek, ćevapi and coffee scenes for feeding, and the sleeping goat, each
  about 30 KB.
- The needs show as bars in the site's yellow, red when low, with the ARIA
  meter role, instead of the browser's own meters.
- Nothing is written to the browser until a goat is picked; the page only
  reads whether one is kept. The organiser asked whether the site uses
  cookies: it uses none, and Goatchi's local storage is the only thing the
  site stores.
- `tools/speakers.py check` accepts `goat_keep: yes` and fails any other
  value; no speaker has it yet, so only the plain and role goats are offered.
- The footer and the home page's back cover link "Goatchi".

### Success metrics, checked

- "A visitor who never adopts a goat downloads nothing more than today." **met**: `site/goatchi.js` is loaded by `site/goatchi.html` only (grep on 2026-10-28: 0 in `site/index.html` and `site/speakers.html`); other pages gain only the footer link, 2026-10-28.
- "An adopted goat is still theirs, with its needs where they left them, after closing the browser and coming back." **met**: in the browser, a goat was picked, the page closed and opened again, and the goat and its needs were as left, 2026-10-28.
- "A goat left alone for a week is sulking, not gone, and cheers up when fed." **met**: with its needs set seven days back, the goat was still kept, every bar was empty and red and it said "Baaa…"; fed, its food bar filled, 2026-10-28.
- "The scripted goat audit (every page, at 360, 412, 768 and 1300 pixels) shows no console errors and no goat cut off, with and without an adopted goat." **not checked**: the companion goat and the other pages are unchanged apart from a footer link, and an adopted goat lives on the Goatchi page only; that page was checked at 390 and 900 pixels with no console errors, 2026-10-28.
- "The organiser plays it on their phone and approves it." **not checked**: checkable once it is live on goatconf.com, after this merge.
