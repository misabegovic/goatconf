---
title: "The program page: the lineup first, open rooms folded, a tighter intro"
date: 2026-11-07
kind: conversation
---

After the register page's refresh, the organiser asked, verbatim:

> What do you think of the program page?

The agent's view: on a phone it works, folding each slot's open rooms
into one line; on a desktop it hid the lineup and showed mostly empty
cards. Eight speakers were confirmed, some with talk titles, but the page
showed eight "Reserved: for a confirmed speaker" cells and 48 "Open"
cells; seven rooms sat in a six-across grid, so the seventh wrapped alone
in every slot; the intro ran five paragraphs, with the seats note now on
the register page; the lede ("Every empty slot is waiting for someone")
spoke to speakers; and Saturday's event sticker had no number.

Asked, the organiser chose:

- **The lineup:** a "Confirmed so far" strip of the confirmed speakers'
  photos and names before the timetable, with their sessions, days and
  times still to come; reserved cells stay unnamed, since their slot is
  not decided.
- **Open rooms on desktop:** folded like on phones: reserved rooms and
  sessions as cards, the open ones as one line per slot ("6 of 7 rooms
  still open. Propose a session").
- **The intro:** tightened, attendee-facing, nothing decided dropped.

Built as:

- tools/speakers.py holds the faces strip, now shared by the register
  page and the program page.
- program.html opens on "Confirmed so far": "These speakers are
  confirmed. Their sessions, days and times are still to come; each
  main-hall cell marked Reserved below is held for one of them."
- The lede: "Two days of sessions in every room of IPI Academy, an hour
  off after each for the hallway track, then a community day on
  Saturday."
- "How a day runs" in four paragraphs: the days and their hours, the
  slot and the hallway track (with half-hour sessions and longer
  workshops), recording in one line, and when things are final; the seats
  note points to the register page.
- On wide screens, the open rooms fold into one dashed line beside the
  slot's cards, as on phones; the "rooms taken" count hides when that
  line shows.
- Saturday's added events carry their number, before the open slots.
