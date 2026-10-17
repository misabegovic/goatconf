---
title: "The home page's three days: evenings open, events listed under their day, an invitation for any day of the week"
date: 2026-10-17
kind: conversation
---

The organiser wrote, verbatim:

> For "Three days in June" section. The events folks add can apply for either of the days. I am curious, how can we improve this entire section?

The agent noted that only Saturday's sticker mentioned events people
add, while the propose page says an accepted event between 2 and 6 June
goes on the program, and proposed: open the Thursday and Friday
evenings on their stickers; add an empty "Yours?" slot for an event on
any day; make Saturday's line general; list accepted events under
their day; link each day to the program; say what the hours off are;
and write day names without ordinals. The organiser wrote, verbatim:

> Do all.

The ordinals stay: `PRODUCT.md` sets "Thursday 3rd June" as the site's
style for day names, so the agent left them and said so.

Done on 2026-10-17, in `tools/home.py`:

- Each day sticker links to its day on the program page.
- Thursday and Friday add "Hours off: coffee on Freedom Square and
  lunch in town." (from the day plan's breaks) and "Evening: open for
  the meetups, dinners and karaoke people add."
- Saturday reads "A day at the lakes and the goat hunt, planned by the
  organiser, plus what people add."
- A wide "Yours?" slot follows the three days: "Your event, any day
  from 2 to 6 June", linking to the propose page.
- Accepted events show under their day as "Added: <name>, <time>";
  those on 2 or 6 June show in the "Your event" slot. None is accepted
  yet, so a test in `tests/test_home_and_nav.py` covers it.
- `site/goatconf.css` styles the linked stickers and the "Added" lines;
  every page's stylesheet stamp is updated. The album's numbers after
  the section move up by one.
