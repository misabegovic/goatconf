---
title: "A shared speaker profile shows that speaker's own card, not the generic banner"
date: 2026-10-14
kind: conversation
---

The organiser wrote, verbatim:

> Also, when I share a profile of a speaker, I don't want a generic banner shown, I want that speaker's banner to render

and then, of this and the home page's eight places (sources/conversations/2026-10-14--org--home-eight-places.md):

> Ok, deliver it

Done on 2026-10-14: every speaker has a third card, `site/share/speaker-<name>-preview.png`, 1200 by 630 pixels, in the design of their "I'm speaking" card (photo, name, role, and the session or the place and dates). Their page names it with `<link rel="image_src">`, and `tools/meta.py` then points the page's Open Graph and Twitter image at it, with the page title as its description. Every other page keeps the shared banner, `site/share/og.png`. `tools/speakers.py build --check`, which the local CI runs, fails while a published speaker has no preview card.

Sites that already fetched a speaker's link (LinkedIn, X, WhatsApp, Slack) keep their old preview until they fetch it again.
