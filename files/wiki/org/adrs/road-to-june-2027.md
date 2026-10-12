---
title: "Anchor the road calendar to IPI's confirmation and the core day, not to fixed dates"
kind: decision
status: accepted
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/road-to-june-2027.md
sources:
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md
---

# Anchor the road calendar to IPI's confirmation and the core day, not to fixed dates

Answers the "Decision needed" of
[The road to June 2027](../prds/road-to-june-2027.md). Accepted 2026-10-07 from the organiser's answer
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 14), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

The road calendar is written as steps anchored to two dates: the day IPI
confirms the dates and rooms in writing, and the core day. Each step says
how far it sits from its anchor. Calendar dates are filled in only when
the anchors are known, and every step moves with its anchor if IPI's
answer comes late or picks a different week. The calendar becomes a
reference page in this brain, `wiki/org/road-calendar.md`, created on
IPI's confirmation and reviewed at every call every two weeks.

## Why

The organiser chose anchored steps over fixed dates. Nothing can be
announced before the venue is confirmed (the guide's first rule, and the
PRD's no-go), so the whole calendar already hangs on IPI's answer; fixed
dates written now would be wrong the day IPI picks the first week
instead of the second, or answers in December instead of November.

## How

Anchored to IPI's confirmation: website v1, registration and the email
list open, and the date announced, on the confirmation itself (the
organiser's choice for registration,
`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`);
the supporter menu and the personal asks within two weeks; the invited
speakers confirmed within six weeks.

Anchored to the core day: the call for talks opens about six months
before it, the guide's "four to six months before the event" at its
early end (`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`),
and closes about four and a half months before it, never extended once
published; review takes two weeks after the close; speakers are
announced from about three months out; the full schedule at two months;
the run sheet and reminders at one month; a courtesy police notice, if
the organiser or IPI sends one, at least five days before
(`sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md`, Article 36);
the feedback survey within a week after; the final account within two
weeks after.

If the confirmation comes so late that the call would open less than
four months before the core day, the call shortens and that is said on
the calendar page, rather than the review or the announcements being
squeezed silently. Each step on the page is marked done, late or moved,
with the date and the reason.

## Alternatives

- **Anchored steps** *(chosen)*: true however IPI answers.
- **Fixed dates now, assuming the second week:** readable today, and
  wrong in part the moment IPI answers differently.

## Consequences

- **Opens:** a calendar that never needs rewriting, only filling in.
- **Costs:** until IPI answers, nobody can say on which date the call
  opens; the PRD's month table stays the working guess.
- **Costs:** a late answer from IPI pushes everything; the October
  approach to IPI is the step that matters most.

## Linked PRD

[The road to June 2027](../prds/road-to-june-2027.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-12.** Read every mention of the core day as the two core days, Thursday 3 and Friday 4 June 2027. The call opens earlier and has no strict deadline, so its rows are targets. See [Dates: two core days](two-core-days-first-week.md), [The call: the organiser judges](call-organiser-judges.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** The first anchor is reached. IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. The steps anchored to IPI's confirmation (website, registration, the call and the announcement) are due now (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
