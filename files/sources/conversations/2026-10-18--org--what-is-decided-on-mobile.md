---
title: "On phones, the \"What is decided\" stickers are tighter"
date: 2026-10-18
kind: conversation
---

The organiser wrote, verbatim:

> Let's optimize the "What is decided" section for mobile?

The agent looked at the home page's "What is decided" section on phones
(320, 360 and 390 pixels wide). It kept two columns of six stickers. The
fact stickers had wide padding, so their text wrapped into narrow columns
(seven lines for "Free" at 360 pixels), and "Tech stack agnostic" took
three lines. The photos were tall (4:5), so each row was taller than its
words needed, and the section ran about 850 pixels.

Built as, on phones only (below 48rem):

- Less padding inside the fact stickers and slightly smaller body text,
  so it wraps in wider lines.
- "Tech stack agnostic" is set smaller, so it fits on two lines.
- The photos are square and fill the sticker's height, so no white strip
  is left under a photo when its neighbour is taller.
- The "Your session" slot has less padding and a smaller goat.

At 390 pixels the section is about 740 pixels tall, down from 850. Tablets
and desktops are unchanged. The words did not change.
