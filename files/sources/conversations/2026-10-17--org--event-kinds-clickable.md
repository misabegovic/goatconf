---
title: "Every event kind on the home page links to proposing one"
date: 2026-10-17
kind: conversation
---

The organiser wrote, verbatim:

> In the propose an event section, all options should be clickable

Done on 2026-10-17:

- On `site/index.html`, each of the eight kinds in "Propose an event"
  (evening event, community trip, meetup, live podcast, hike, hackathon,
  karaoke, something else) becomes a link to `add.html`, the same page
  "Propose yours" opens, in the same style as the "Your talk" slots that
  link to `talk.html`: a lighter blue on hover and a tilting "Yours?"
  stamp.
- `site/goatconf.css` lets each linked slot fill its grid cell and keeps
  the list free of bullets; every page's stylesheet version stamp is
  updated by `tools/meta.py apply`.
