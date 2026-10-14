---
title: "A speaker's role and employer show wherever their name does, as text"
date: 2026-10-14
kind: conversation
---

The organiser wrote, verbatim:

> Do we also show where the speaker works at which role on their promo stuff? And on our site?

They did not: a speaker record had only a name, photo, links and bio. Asked four questions, the organiser chose:

- **Where it shows:** "Promo cards", "Their own page", "Speakers grid + home" and "Search/AI files": all four.
- **How it is written:** "One free-text line (Recommended)", for example `role: Staff Engineer at Vinted`, so it also fits "Independent consultant" or "Founder, Acme".
- **Where it comes from:** "I research it". The agent finds it on the speaker's own site or a past conference and records the source; the talk form gains no question.
- **A company logo:** "No, text only (Recommended)". An employer's logo never appears beside a speaker, so an employer cannot read as a supporter.

Done on 2026-10-14:

- Speaker records take an optional `role`, one line of at most 80 characters; the check refuses a longer or empty one.
- It shows under the name on the speaker's own page (and in its search and link-preview description), on the speakers page cards, on the home page stickers, on the "I'm speaking" cards, in `llms.txt`, and as `jobTitle` for the speaker in the event data once they have a session.
- Dejan Menges's record reads `role: Staff Engineer at Vinted`, from "Staff Engineer at Vinted" on https://menges.dev/ and https://menges.dev/speaking/ (sources/web/speakers/menges-dev-2026-10-14.md).
