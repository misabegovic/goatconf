---
title: "A compact phone menu: Menu and Register, pinned at the top"
date: 2026-10-23
kind: conversation
---

The organiser asked, verbatim:

> Do you think we should update the navbar? So we have a mobile friendly menu?

The agent measured the top bar on phones on 2026-10-23: 149 px of a 760 px
screen at 390 and 430 px wide, 190 px at 320 and 360 px, where the buttons
wrap onto extra rows; it is not pinned on phones, so after scrolling there
is no menu until the footer; and DESIGN.md describes a single sideways
scrolling row the CSS does not follow. Asked one question at a time, the
organiser chose:

1. **How the bar works on phones:** "Menu button (Recommended)": a compact
   bar with the GoatConf mark, a Register button and a Menu button that
   opens a panel with Program, Speakers, Travel, Supporters, Make it yours
   and Propose a session, about 56 px tall.
2. **Pinned:** "Yes, pinned (Recommended)": the compact bar stays at the
   top as people scroll.
3. **What stays visible besides Menu:** "Register only (Recommended)".

Wider screens keep today's bar.

The agent then put the change to the organiser to approve before building:
under 768 px, a pinned bar about 56 px tall with the GoatConf mark, a
yellow Register button and a Menu button; Menu opens a panel under the bar
with Program, Speakers, Travel, Supporters, Make it yours and Propose a
session as large tap targets, the current page marked; it works without
JavaScript and closes on Escape, on tapping Menu again, or on following a
link; wider screens keep today's bar; every page gets it from
`tools/nav.py`, with tests. The organiser chose "Approve, build it
(Recommended)".

After seeing the screenshots and PR #159, the organiser wrote, verbatim:

> Let's remoce register button then, make it part od menu
> Return year

Read as: no Register button beside Menu; Register moves into the menu; and
the mark keeps its year on every phone (the build had dropped "2027" under
about 376 px so the two buttons fit). The phone bar is now the mark with
its year and Menu; the menu lists Program, Speakers, Travel, Supporters,
Make it yours, Propose a session, and Register last, as a yellow button.
