---
title: "Accepted events break nicely on phones and show as examples on the home page"
date: 2026-10-18
kind: conversation
---

After the BH Professionals Meetup went live (PR #80), the organiser
wrote, verbatim:

> Ok, it landed, but doesn't break nicely on mobile. Maybe we should also list it on the homepage where we list examples

At 390 pixels wide the agent found three breaks: on the program page the
meetup's sticker sat in a half-width column on Saturday, so
"PROFESSIONALS" ran out of it; the day links at the top of the program
page did not wrap, so the whole page scrolled sideways (this was there
before the meetup); and the extensions page had no styles for a listing
at all, so its registration and contact links ran off the screen.

What changed:

- On phones an accepted event's sticker takes the full row on the
  program page, and the day links wrap inside their pills.
- A listing on the extensions page shows its facts in a light panel,
  labels beside values, with long links wrapping; each listing carries
  an anchor named after its record.
- The home page's "Propose an event" kinds are built from the records: a
  kind with an accepted event shows that event as its example, linking
  to its listing, and the other kinds stay open ("Yours?"). The Meetup
  place now shows the BH Professionals Meetup.
