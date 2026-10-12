---
title: "Program: every room open, with sessions posted as they are confirmed"
kind: decision
status: accepted
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/dates-and-the-core-day.md
  - org/prds/cfp-and-speakers.md
  - org/prds/extension-slots-and-the-record.md
sources:
  - sources/conversations/2026-10-12--org--first-come-luma-only.md
  - sources/web/tooling/rails-world-app-2026-10-12.md
  - sources/conversations/2026-10-12--org--agenda-in-rails-world-app.md
  - sources/conversations/2026-10-12--org--register-per-session.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-12--org--program-model-open-everything.md
  - sources/conversations/2026-10-12--org--headcount-and-open-rooms.md
  - sources/conversations/2026-10-12--org--open-room-confirmer.md
  - sources/conversations/2026-10-12--org--all-available-rooms.md
  - sources/conversations/2026-10-12--org--slots-filled-as-we-go.md
  - sources/conversations/2026-10-12--org--organiser-judges-no-strict-deadlines.md
  - sources/conversations/2026-10-12--org--extension-listings-judged.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
---

# Program: every room open, with sessions posted as they are confirmed

Accepted 2026-10-12 by the organiser
(`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`,
question 1).

## What

Every room at IPI Academy is open for sessions on both core days, and
the program changes as sessions are confirmed rather than being fixed in
advance (`sources/conversations/2026-10-12--org--program-model-open-everything.md`).
The organiser keeps the program open so that all rooms can be filled at
any moment (`sources/conversations/2026-10-12--org--headcount-and-open-rooms.md`).
Every slot in every room comes from the same call, judged by the
organiser ([the call](call-organiser-judges.md)). Events outside the core
days' rooms and timetable, before, after or on Saturday 5 June, are
additions: listed as extensions and run independently by their hosts.

## Why

The organiser expects a small crowd, so the limit is sessions to fill
the rooms, not seats (`sources/conversations/2026-10-12--org--headcount-and-open-rooms.md`).
IPI has several rooms free for workshops while talks run
(`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).

## How

The organiser confirms each session
(`sources/conversations/2026-10-12--org--open-room-confirmer.md`), and
the confirmation is a choice, since the organiser judges everything
(`sources/conversations/2026-10-12--org--organiser-judges-no-strict-deadlines.md`).
A confirmed session becomes a program record, and the program page on
goatconf.com is rebuilt and published; the page shows the date it was
last updated. Changes in the last week are also posted on a board at
the venue. People registered for a day hear about changes by email from
the registration sheet.

The labels follow from the room: a session in a core-day slot is part of
the GoatConf program; anything else is "<name>, a GoatConf fringe
event", as the extension rules say
(`wiki/org/prds/extension-slots-and-the-record.md`).

## Alternatives

- **A fixed core day with open rooms only around it.** Not adopted.
- **Keep one room and three to four talks.** Superseded by
  [parallel rooms](core-day-parallel-tracks.md).

## Consequences

- **Closes:** a fixed core day announced once; the 30 April
  announcement as a deadline (it becomes a target for a first program).
- **Opens:** rooms used at any time and a program that grows.
- **Costs:** the organiser's time on each session; people who travel
  need to check the program page and their email for changes.

## Amendments

- **2026-10-12.** IPI Academy has given GoatConf access to all seven rooms on both core days, so every room in this decision is available (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-12, a registration for every session.** Each accepted session gets its own free Luma event, so people register for the sessions they want (source: sources/conversations/2026-10-12--org--register-per-session.md). A session registration saves a seat up to the room's size, with no approval; when a session is full, Luma keeps a waiting list, and empty seats go to whoever is at the door when it starts. The main GoatConf registration, with the organiser's approval, stays as it is. When the organiser accepts a session, the agent creates its Luma event in the organiser's browser and records its link as `luma:` in the session's record; the program, the speaker's page and the agent files then link to it. This replaces "first come, first served at each room's door" wherever the site said it.
- **2026-10-12, session sign-ups move to an app, later.** This replaces the per-session Luma events of the amendment above (source: sources/conversations/2026-10-12--org--agenda-in-rails-world-app.md). The official GoatConf registration stays on Luma, with no limit. Closer to June, a copy of the Rails World conference app (TelosLabs/rails-world, GPL-3.0, Rails 8; sources/web/tooling/rails-world-app-2026-10-12.md) takes session sign-ups and personal agendas; its schedule and saved-session features exist, and a seat limit per session, which it lacks, is to be added. Ticket holders are sent its link. A session record's optional `signup:` link shows as "Save a seat" on the program and the speaker's page. Hosting, email and holding attendees' accounts are a decision of their own when the time comes, with any cost in the public budget.
- **2026-10-12, first come, first served, with Luma only.** This replaces the two amendments above about session sign-ups (source: sources/conversations/2026-10-12--org--first-come-luma-only.md). Registration is on Luma only, with no limit, and seats are first come, first served at each room's door. A sign-up for specific sessions may be introduced later; the Rails World app, a workshops-only sign-up and Tito were looked at and none is decided. The session record's optional `signup:` field stays in place, unused, for that case.

## Related

- [Core days: parallel rooms](core-day-parallel-tracks.md)
- [Dates: two core days](two-core-days-first-week.md)
- [The call: the organiser judges](call-organiser-judges.md)
- [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md)
- [Extension slots and the record](../prds/extension-slots-and-the-record.md)
- [IPI Academy](../ipi-academy.md)
