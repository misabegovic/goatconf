---
title: "The organiser block moves below why a goat on the home page"
date: 2026-10-17
kind: conversation
---

The organiser wrote, verbatim:

> Let's move the who's organising section to be below why a goat?

Done on 2026-10-17:

- On `site/index.html`, the "Who's organising" section (the organiser,
  IPI Academy, the four fact stickers and the conferences run before,
  with their photos) moves from after the three days to after "Why a
  goat", before the code of conduct. Its content is unchanged.
- The album's sticker and slot numbers are renumbered in page order by
  `tools/home.py build`, so the RubyConf Austria photos now carry the
  numbers after the supporters.
- The home page now runs: the cover with the seal, the three days, who
  is speaking, give a talk, Tuzla, food, propose an event, the
  supporters, why a goat, who's organising, and the code of conduct.
