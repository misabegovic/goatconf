---
title: "The home page: the attendee's story first, a Register band in the middle, shorter on phones"
date: 2026-11-07
kind: conversation
---

After the speakers page's change, the organiser asked, verbatim:

> What do you think of the home page?

The agent's view: the opening spread is the album at its best, and each
section is honest and specific, but the page ran about 13,800 px on a
desktop and 29,300 px on a phone; the order broke the attendee's story,
with "Propose a session" between the speakers and Tuzla, and Tuzla and
the food fifth; the two Register buttons sat at the top and at the very
end, about 28,000 px apart on a phone; the hallway track showed only in
the days' small print; and "120 to 300 people" was said twice side by
side.

Asked, the organiser chose:

- **Order:** the attendee first, the doors later: days, speakers, Tuzla,
  food, a Register band, then propose a session, make it yours and
  support, then why a goat, the organiser, the code of conduct, Goatchi
  and "See you in Tuzla".
- **A Register band in the middle:** after the food.
- **The "What is decided" stickers:** left as they are.
- **Shorter on phones:** no preference; the agent took the two it
  recommended, the speakers as the faces strip and the food folded to
  four dishes, desktop unchanged for both.

Built as, on index.html:

- "Propose a session" moves from after the speakers to after the food,
  behind a new "Get your free ticket" band: "Two days of sessions in
  every room of IPI Academy, the hallway track after each one, and a
  Saturday at the lakes. Free to attend, for everyone.", with "Register
  for free" to the register page.
- On a phone the speakers show as the faces strip from tools/speakers.py
  (written beside the cards by tools/home.py), and the food shows four
  dishes and "Show all dishes", a toggle that needs no script.
- The page is about 23,100 px on a phone, from 29,300.
