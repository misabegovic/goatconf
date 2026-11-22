---
title: "Why are some speakers' goats on the left side and smaller?"
date: 2026-11-22
kind: conversation
---

On 2026-11-22, about the live site, after the section goats were published
at a size that reads
(sources/conversations/2026-11-22--org--ship-section-goats-right-size.md),
the organiser wrote, verbatim:

> Why are some speakers goats showing up on the left side and smaller?

Read as: every speaker's goat is to stand at the same end of its card and
at the same size on every card, at every width. It still covers no word,
link, stamp, number or tag.

The cause, in site/album.js: since the sections were made right in both
states
(sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md),
a goat that peeks over a slot's top edge and would cover something there
that is not the slot's own is moved to the slot's left end, then drawn at
62 percent of its size, then at 45 percent. On a speaker's card the goat
rises higher than the room kept above the card, so on some cards it
reaches the card above and takes one of those other seats; which cards
depends on each goat's own height and on what the card above ends with,
so the row looks random.

Measured on the published page the same day, "Who is speaking" open, each
card brought to the middle of the window:

- At 390 wide the goat is 119 to 120 pixels wide at the card's right end
  on five cards, and 74 pixels wide at the left end on Dejan Menges's.
- At 1440 wide it is 136 pixels wide at the right end on Roy Tomeij's
  card and 84 pixels wide at the left end on Cristian Planas's.

Not the organiser's words, and for the organiser to confirm: how much
room is kept above a row of speakers' cards, and what is done with every
other slot on the site where a goat stood at the left or smaller.

The same day, told the cause (the seat rule in site/album.js moving some
speakers' goats to the left end and drawing them smaller) and the fix (one
end and one size on every card, the room made in the layout, the same
check across every other kind of slot, never 45 percent), the organiser
said, verbatim:

> Ship when ready

Read as: the fix as described is published once it is built and the checks
pass, without being shown first.
