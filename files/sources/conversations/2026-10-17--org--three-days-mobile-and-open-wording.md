---
title: "The three days: one column on phones, and wording that names no kinds of event"
date: 2026-10-17
kind: conversation
---

The organiser wrote, verbatim:

> Breaks weird on mobile. Also don't restrict to certain types, be accepting.

On a phone, a general rule put the day stickers into two narrow
columns, and Saturday lost the full width it used to take as the last
item, now that the "Your event" slot follows it. At tablet width the
full-width stickers' tilt made them overlap the heading and each other.

Done on 2026-10-17:

- `site/goatconf.css`: on phones the day stickers are one column; in
  the one-column layout they tilt only half a degree; the hours line
  keeps a tight line height. Every page's stylesheet stamp is updated.
- `tools/home.py`: Thursday's and Friday's evening line reads
  "Evening: open for whatever people add."; the "Your event" slot reads
  "Anything you would like to run for the people who come. You run it,
  and once the organiser accepts it, it is on the program." No kind of
  event is named.
