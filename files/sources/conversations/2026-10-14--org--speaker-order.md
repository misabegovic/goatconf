---
title: "Speakers are listed by the organiser's order of standing, not alphabetically"
date: 2026-10-14
kind: conversation
---

The organiser wrote, verbatim:

> Let's put Paul first, Dejan second, Amar third when we list them. Dont list alphabetically, list in order of magnitude of speaker

Done on 2026-10-14:

- Speaker records take an optional `order`, a whole number from 1, set by the organiser. The speakers page, the home page's "Who is speaking" stickers and `llms.txt` list speakers by it, 1 first; speakers without one come after, by name. The check refuses two speakers with the same number, and an order that is not a whole number from 1.
- Paul Campbell is `order: 1`, Dejan Menges `order: 2`, Amar Mahmutbegović `order: 3`.
