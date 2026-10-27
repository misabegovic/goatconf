---
title: "The stickers stop peeling: no entrance animation on the cards"
date: 2026-10-27
kind: conversation
---

The organiser said, of the stickers that lifted and settled into place as they scrolled into view:

> I don't want the cards on the site to have that animation, becomes annoying

The peel and settle (each sticker starting rotated, shifted and raised, then settling into its slot over 900ms, staggered) is removed: the head script that set the peeled start, the observer in `album.js`, the CSS and the `data-peel` attributes. Stickers keep their tilt and sit still. The goat's hover wiggle and the button hover are not card animations and stay.
