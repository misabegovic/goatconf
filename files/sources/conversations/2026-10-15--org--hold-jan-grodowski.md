---
title: "Jan Grodowski held from the site while his employer clears the engagement"
date: 2026-10-15
kind: conversation
---

The organiser wrote, verbatim:

> cool. we need to hide Jan Grodowski for now, he needs to confirm with his
> company first since all talking engagements need to be cleared by Shopify
> for him. don't delete him, just hide from rendering on the site, so we can
> add him back easily later

Done on 2026-10-15:

- Speaker records gain an optional `hold` line: a short reason that keeps
  the record, its checks and its `order`, while nothing on the site shows
  the speaker. `speakers.py check` passes with a note (held from the
  site, so not listed), the speaker leaves the speakers page, the home
  page and the files for agents, and their own page is removed from
  `site/` on the next build. Removing the line puts them back.
  Documented in `speakers/README.md`, tested in `tests/test_speakers.py`.
- A held speaker still counts in the no-two-share order check, and a
  session on the program that names a held speaker still fails the check
  ("not a published speaker record"), so hiding someone never half-hides
  them.
- His record carries
  `hold: waiting for his employer's approval before any announcement`;
  his photo, links, bio and `order` 4 stay untouched.
- The site was rebuilt without him: `site/speaker-jan-grodowski.html` is
  gone, and he left `speakers.html`, the home page, `llms.txt` and the
  sitemap. His "I'm speaking" cards stay under `site/share/` (nothing
  links to them while he is held), so adding him back is removing the
  `hold` line and rebuilding.
