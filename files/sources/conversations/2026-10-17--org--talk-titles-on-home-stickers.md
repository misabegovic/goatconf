---
title: "The home page's speaker stickers show the talk title, as the speakers page does"
date: 2026-10-17
kind: conversation
---

The organiser wrote, verbatim:

> I can't help but notice that we don't show talk titles the same way on speaker cards on the site. Let's make sure we do.

The speakers page showed "Talk: <title>" under the role for Dejan Menges
and Christoph Lipautz; the home page's "Who is speaking" stickers showed
only name and role, and the "I'm speaking" cards show the dates where a
scheduled session would go. Asked which to change, the organiser chose
"Home page stickers" only.

Done on 2026-10-17:

- `tools/home.py` adds the title under the role on each home page
  speaker sticker, in the same words as the speakers page: "Talk:
  <title>" from the record while the talk has no slot, and the
  session's format and title once a program record carries it.
- `site/goatconf.css` styles it a little smaller and lighter than the
  role; every page's stylesheet stamp is updated.
- A test in `tests/test_speakers.py` covers both cases.
- The "I'm speaking" cards are unchanged.
