---
title: "No icon beside GoatConf in Google's search results"
date: 2026-10-19
kind: conversation
---

The organiser wrote, verbatim:

> When googling goatconf I don't see an icon load on the search results

Checked on 2026-10-19: every page linked only `favicon.svg` (the coin,
served as image/svg+xml, 200), `/favicon.ico` answered 404, and
robots.txt allows everything. Google's favicon service
(`https://www.google.com/s2/favicons?domain=goatconf.com&sz=64`) already
returned the goat coin as a 64 by 64 PNG, so Google had fetched the icon;
search results pick up a site's icon on their own schedule, often days to
weeks for a new site.

The agent added raster fallbacks, rendered from the same coin:
`favicon-96.png` (96 pixels, a multiple of 48 as Google asks), linked
from every page next to the SVG, and `/favicon.ico` (16, 32 and 48
pixels). Requesting a recrawl of the home page in Google Search Console
can speed it up; that is the organiser's to do.
