---
title: "GoatConf 2027: a minimal core others extend"
kind: epic
status: draft
updated: 2026-10-14
confidence: medium
supersedes: org/pitches/one-goat-minimal-core-and-extensions.md
sources:
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--approval-back-on.md
  - sources/conversations/2026-10-12--org--first-come-luma-only.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--prds-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/web/funding/euruko-2024-why-the-goat.md
  - sources/web/models/fosdem-2026-fringe.md
  - sources/web/funding/fosdem-charter.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
---

# GoatConf 2027: a minimal core others extend

The umbrella for GoatConf 2027. It graduates the pitch
[One goat feeds the town](../pitches/one-goat-minimal-core-and-extensions.md),
on which the organiser bet on 2026-10-07 together with every area pitch
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`). Each
child PRD carries one area; this page carries what holds them together.
Epics have no ADR of their own: the decisions live in the children.

## Objective

**A free GoatConf in Tuzla in June 2027 that the organiser can promise
in full: one core day of three to four talks at IPI Academy, with long
breaks in town, wrapped in days that others fill.**

The organiser asked for an event "minimalistic and extendable... Like the
Pi agent": "I will provide the minimum needed for a conference and folks
can extend" (`sources/conversations/2026-10-07--org--conference-vision.md`).
The name already says it: "The whole of Tuzla milked one goat", the
saying behind EuRuKo 2024's G.O.A.T. edition, which the organiser founded
(`sources/web/funding/euruko-2024-why-the-goat.md`). One small, reliable
core; everyone draws on it and adds to it.

## Background

As of 2026-10-07 GoatConf has an organiser, Muhamed Isabegovic, who
organised EuRuKo 2024 and RubyConf Austria and runs it from Vienna; a
host and venue, IPI Academy in Tuzla, his own school, with a hall of
about 120 seats, several other rooms, a projector, sound and Wi-Fi but
no microphone or recording; a window, the first or second week of June
2027, with six date options to put to IPI; and a set of rules the
organiser stated one by one ([what is known](../goatconf-2027.md)).

Those rules shape every child:

- **Free to attend**, registration capped at the hall, about 120.
- **No money passes through the organiser.** Supporters pay suppliers
  directly or give in kind; **the budget is public**, line by line
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- **The organiser's own money is a fallback only**, at most 1,000 EUR,
  and **never spent on food or drink** for anyone
  (`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
- **Space to hang out**: few talks, coffee and lunch on Freedom Square,
  one to two hours each (`sources/conversations/2026-10-07--org--space-to-hang-out.md`).
- **Speakers pay their own travel.**
- **This repository is to be public**, and extension hosts contribute to
  it (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

The calendar is tight. The RubyEvents guide puts a first conference at
about a year and sponsor budgets as closing around the previous November
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`);
GoatConf has about eight months.

## Affected personas

- **[Attendee](../../../.claude/personas/users/attendee.md).** *Now:* no
  date, no site, no way to register. *Target:* a free place on a dated
  day, the trip's real cost known in advance, and most of the day spent
  with people.
- **[Speaker](../../../.claude/personas/users/speaker.md).** *Now:* no
  call. *Target:* an honest call that says travel is theirs, three to four
  main-day slots, and real homes for the proposals that do not fit.
- **[Extension host](../../../.claude/personas/users/extension-host.md).**
  *Now:* nothing to extend. *Target:* one short record, submitted by pull
  request or form, listed under clear terms.
- **[Hiring partner](../../../.claude/personas/users/hiring-partner.md).**
  *Now:* no way in. *Target:* a named item to fund, a job board, and
  attendees who opted in.
- **[Volunteer](../../../.claude/personas/users/volunteer.md).** *Now:*
  none recruited. *Target:* one owned domain each, from IPI's students or
  the community.

## Scope

**In:** the core the organiser guarantees (the date and room, one program,
free capped registration, the website at muhamed.at/goatconf, the code of
conduct, the breaks in town, the one-page charter), the extension
mechanism others use to add to it, the public ledger and the supporters'
menu, and the work that gets all of it ready by June 2027.

**Out:** anything an extension host runs (fringe events, workshops beyond
the program, hubs, activities, extra venues) except the rules and listing
for them; a second edition; the reusable kit, which is extracted only
after the 2027 event.

## No-gos

- No paid tickets.
- No money through the organiser; no spending off the public ledger.
- No food or drink from the organiser's money.
- No more than one core day, and no parallel talks in it.
- No attendee data sold, shared or kept beyond the follow-up.
- No kit extraction before the 2027 event.
- CI stays local; one GitHub Actions workflow only publishes the site (amended 2026-10-12, sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md).

## Children

Each child is a PRD under `wiki/org/prds/`, graduated from the area pitch
named beside it. The organiser approved every PRD on 2026-10-07
(`sources/conversations/2026-10-07--org--prds-approved.md`); each has a
accepted ADR under `wiki/org/adrs/` with the same name, written from the
organiser's answers (`sources/conversations/2026-10-07--org--adr-answers.md`)
and approved on 2026-10-07
(`sources/conversations/2026-10-07--org--adrs-approved.md`).

- [Extension slots and the record](../prds/extension-slots-and-the-record.md):
  the seven kinds of slot, the shared record, pull request or form, an
  agent's check and the organiser's merge (from the umbrella pitch).
- [Dates and the core day](../prds/dates-and-the-core-day.md): six date
  options for IPI, one core day of three to four talks, breaks on Freedom
  Square (from [the dates pitch](../pitches/dates-format-and-schedule.md)).
- [Website and registration](../prds/website-and-registration.md):
  muhamed.at/goatconf written here, registration with the date, a cap of
  about 120 (from [the website pitch](../pitches/website-and-registration.md)).
- [Design with impeccable](../prds/design-with-impeccable.md) (from
  [the design pitch](../pitches/design-with-impeccable.md)).
- [Social drumbeat](../prds/social-drumbeat.md) (from
  [the social pitch](../pitches/social-presence-and-drumbeat.md)).
- [CFP and speakers](../prds/cfp-and-speakers.md): one or two invited
  speakers, an open call by form (from
  [the CFP pitch](../pitches/cfp-and-speakers.md)).
- [Supporters and hiring](../prds/supporters-and-hiring.md) (from
  [the partners pitch](../pitches/partners-sponsors-and-hiring.md)).
- [Budget and the public ledger](../prds/budget-and-public-ledger.md) (from
  [the budget pitch](../pitches/budget-a-goat-and-a-menu.md)).
- [Activities: the lake and the town](../prds/activities-lake-and-town.md)
  (from [the activities pitch](../pitches/activities-the-lake-and-the-town.md)).
- [Operations and the day](../prds/operations-and-the-day.md) (from
  [the operations pitch](../pitches/operations-people-rules-and-the-day.md)).
- [The road to June 2027](../prds/road-to-june-2027.md) (from
  [the road pitch](../pitches/the-road-to-june-2027.md)).

## Success metrics

- **IPI confirms a date and rooms in writing by 30 November 2026.**
  Observed as a source snapshot of the confirmation under
  `sources/conversations/` or `sources/venue/`.
- **The core day runs with its hall full or nearly so:** registrations
  checked in on the day at 90 or more of about 120 places. Observed from
  the registration tool's check-in export, counted the day after.
- **The organiser's fallback money spent: 0 EUR, or every euro of it on
  the public ledger.** Observed from the ledger page's final account,
  published within two weeks of the event.
- **At least five extensions listed** by the week before the event, none
  run by the organiser. Observed as a count of extension records in this
  repository.

## Open questions

- Which of the six date options IPI can host.
- Which IPI staff member is the second code-of-conduct contact.
- Who the one or two invited speakers are.
- Whether supporters can be found for any item on the menu before the
  November budget window closes.
- When the organiser flips this repository to public, and makes the clean
  first commit with it.

## Amendments

- **2026-10-12.** The epic's one-core-day shape is superseded: two core days, Thursday 3 and Friday 4 June 2027, with Saturday 5 June free for the community; every available room in parallel; the organiser judges every proposal with no strict deadline; and the site moves to goatconf.com on GitHub Pages with every intake through Google Forms. The no-go "no more than one core day, and no parallel talks in it" no longer applies. See [Dates: two core days](../adrs/two-core-days-first-week.md), [Core days: parallel rooms](../adrs/core-day-parallel-tracks.md), [Program: every room open](../adrs/open-program-every-room.md), [The call](../adrs/call-organiser-judges.md) and [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. The epic's IPI-confirmation milestone is met as reported (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-14, read with the later decisions.** Registration is on the organiser's Luma event with no limit and the organiser's approval, not capped at about 120; seats in each room are first come, first served at the door (sources: sources/conversations/2026-10-12--org--registration-on-luma.md, sources/conversations/2026-10-12--org--first-come-luma-only.md, sources/conversations/2026-10-12--org--approval-back-on.md). The background rule "no money passes through the organiser" and "the budget is public" no longer hold: online supporters pay the organiser's Austrian business 500 EUR for online perks only, the budget is private with no budget page, and speakers pay their own travel, refunded only if the budget allows, never promised (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md). So the no-go "no money through the organiser; no spending off the public ledger" no longer applies, and the success metric on the fallback money is observed from the private budget rather than a public final account. The check-in metric's "90 or more of about 120 places" has no single cap behind it any more; a new target is (unknown, needs source).
