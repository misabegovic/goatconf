---
title: "Tips for the hero on a phone: \"Ok, show me\""
date: 2026-11-22
kind: conversation
---

On 2026-11-22 the organiser sent a screenshot of the published home page
on their own phone (an Android phone in the dark theme, about 412 pixels
wide) and asked, verbatim:

> Ok. Any tips on how to improve the hero section?

The screenshot shows the top bar, then the cover: the seal beside
"GOATCONF 2027", the date line wrapped as "3–5 JUNE 2027 · TUZLA, BOSNIA"
over "AND HERZEGOVINA", the headline on three lines, the audience
paragraph on four, the "Register for free" button, and the links
"Propose a session" and "Host an event" each on a row of its own, with
the third link below the screen. No photo and no goat is on that screen.

The answer gave six tips:

1. The three links under the button each take a full row on a phone,
   about half a screen together. Put them on one row as compact links,
   each still 44 pixels tall to press, on two rows only where they cannot
   fit.
2. The grey audience paragraph repeats the headline over four lines. On a
   phone keep only "Any programming language, any stack."
3. The seal and "GOATCONF 2027" take about a quarter of the first screen
   directly under a top bar that already shows the mark and the name. On
   a phone make them much smaller: the seal about half its size beside a
   smaller name, on one line.
4. The date line wraps in the middle of the country's name. Break it
   after the dot: the date on one line, the place on the next.
5. Nothing real shows on the first phone screen, no photo and no goat.
   With the height saved, let the Tuzla photo from "What is decided" come
   into view at the foot of the first screen, and stand a goat on the
   hero where it covers neither the headline nor the button.
6. "What is decided" comes right after on a phone and repeats "Free",
   "3–5 June" and "Tuzla", which the cover has just said. On a phone keep
   the two photos and the stickers that add something new (where IPI
   Academy is, tech stack agnostic, extendable) and drop the repeats.

The organiser answered, verbatim:

> Ok, show me

Read as: the tips are built so that the organiser can judge them by eye,
as before and after images. It is not an approval of any tip. Nothing is
pushed, merged or published before the organiser approves it
(sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md).

Built as two local branches, so the organiser can take the layout without
the cuts:

- `site/phone-hero-layout-only`: tips 1, 3, 4 and 5. No word on the page
  is removed, added or changed.
- `site/phone-hero-layout-and-trim`: the first branch plus tips 2 and 6.
  Words are hidden on a phone only; the page's source, a wide screen and
  the files agents read keep every word.

Both change the page under 48rem only. From 48rem up the page is as
published.

Earlier words of the organiser that the tips touch, for the organiser to
weigh when choosing:

- Tip 1 undoes the tenth round's "the cover's three links one a row on a
  phone", which was the independent review's item 19 and was finished on
  the organiser's "Fix all"
  (sources/conversations/2026-11-22--org--fix-all.md). The review's fault
  was one link left alone on a second row; one a row was the builder's
  fix, not the organiser's wording.
- Tip 2 hides on a phone the words the organiser kept on 2026-10-26, when
  they chose "Ship it" over also trimming "and the incurably curious
  dreamers and visionaries"
  (sources/conversations/2026-10-26--org--hero-date-line.md).
- Tip 3 makes the seal smaller on a phone, where on 2026-10-12 the
  organiser asked "On mobile, the badge could be centered and bigger ?"
  (sources/conversations/2026-10-12--org--cover-seal-mobile.md). The seal
  has stood beside the title, not centred, since the organiser chose the
  photo column on 2026-10-20
  (sources/conversations/2026-10-20--org--hero-photo-column.md).
- Tip 5 is bounded by the order of "What is decided", which the organiser
  set: "feels weird to read 2-4-3-1, make it in order"
  (sources/conversations/2026-10-20--org--hero-photo-column.md) and, for
  phones, "Maybe order one by one?"
  (sources/conversations/2026-10-18--org--what-is-decided-one-by-one.md).
  With the order kept, sticker 1 stays above the Tuzla photo on the first
  branch.
- Tip 6 hides stickers on a phone, where the organiser asked for the
  hero redesign "without losing any context" and, for phones, "I want
  each card listed nicely the way we previously had"
  (sources/conversations/2026-10-20--org--hero-photo-column.md,
  sources/conversations/2026-10-20--org--hero-phone-list.md).

The sentence beginning "An excuse to" stays off the cover
(sources/conversations/2026-11-21--org--links-clickable-and-dark-mode-love.md),
and the hero has no control that closes it
(sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md).
