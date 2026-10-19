---
title: "A design audit of the home page and the talk page"
date: 2026-10-19
kind: conversation
---

The impeccable design hook flagged 13 findings on site/index.html and
site/talk.html, attribution unknown. Asked whether to run an audit that
separates real problems from intentional ones, the organiser answered,
verbatim:

> Yes

The agent ran `impeccable detect` on both files and on the rendered pages
at 390 and 1280 pixels wide, and checked each finding against DESIGN.md
and screenshots.

Fixed:

- Running text in the prose card ran to about 98 characters a line on a
  wide screen; DESIGN.md holds running text to 62ch. Paragraphs and plain
  lists inside `.prose` now keep that measure; grids and maps in the same
  card (the brand files, the travel places) keep the full width.
- The session tags had 1.5 to 3 pixels of space around 11.8-pixel text;
  their padding is now 0.35em by 0.7em.

Sanctioned by DESIGN.md and recorded as file-scoped ignores in
`.impeccable/config.json`, each with its reason: the display line
heights on the home page (the lede at 1.2, sayings and buttons at 1.1),
its condensed uppercase labels, the stickers' printed bottom edge, and
the album wrappers that the static scan reads as flush although their
text is inset. Earlier ignores already covered stickers on pages (nested
cards) and the album pages' clipped corners.

Left standing: a low-contrast reading on the cover's second paragraph,
whose median contrast is 9.8:1 and which reads clearly on screen; the
detector samples the faint hoof pattern behind it. The home page's wide
copy runs to 74ch, as DESIGN.md sets.
