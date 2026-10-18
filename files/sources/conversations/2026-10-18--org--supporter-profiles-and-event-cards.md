---
title: "Supporter profiles with their cards, and a card for every accepted event"
date: 2026-10-18
kind: conversation
---

The organiser asked, verbatim:

> Question: how can supporters download their thank you card and the I am or We are organising this event as part of GoatConf ?
> Ok, deliver but let's not deliver fake example data to the production

"Deliver" was PR #82, merged after the agent checked that no sample
record, page or card was in `files/site/` (the sample session used to
check the session page lived only in the agent's scratch folder and in
the tests, which are not published).

The agent answered that thank-you cards were online but linked from
nowhere, and that no card existed for an event's host. Asked how to
offer them, the organiser answered, verbatim:

> We should have a supporter profiles, same way we have for speakers and let them download their cards there. Thank you and I am organising or part of official program cards.

and chose:

- **The event card's wording:** "Neutral wording": "<event>, organised
  by <host>, part of GoatConf 2027", which suits a person or an
  organisation without a new field.
- **Where it shows, and what it carries:** "Download on event page",
  "Link preview" and "Date and place on it".

What was built:

- Every supporter has a profile, `supporter-<record>.html`, linked from
  the supporters page and the home page: their logo, their line, their
  website, the events they host, and their cards to download (the
  thank-you card, square and wide, and each hosted event's card). A
  supporter record's optional `events:` names the accepted events it
  hosts; the foundation's names the BH Professionals Meetup.
- Every accepted event has a card, square, wide and a 1200 by 630
  preview: "Part of GoatConf 2027", the name, "Organised by <host>",
  the day, time and place, and the event's address. The event's page
  offers both sizes and uses the preview when its link is shared.
- Thank-you cards now name the supporter's profile address. The local
  CI fails while an accepted event's or a supporter's cards are missing.
