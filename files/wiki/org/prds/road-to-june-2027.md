---
title: "The road to June 2027: one calendar for every area"
kind: initiative
status: living
updated: 2026-10-14
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/the-road-to-june-2027.md
sources:
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--session-registration-later.md
  - sources/conversations/2026-10-12--org--approval-back-on.md
  - sources/conversations/2026-10-12--org--first-come-luma-only.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--date-options-for-ipi.md
  - sources/conversations/2026-10-07--org--weekday-lecture-days.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md
---

# The road to June 2027: one calendar for every area

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md),
graduated from the pitch
[The road to June 2027: one calendar for every area, starting this month](../pitches/the-road-to-june-2027.md),
on which the organiser bet on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`). This
PRD waits for the organiser's approval before its ADR is written.

## Objective

**One calendar, kept in this repository and reviewed at every call,
orders the work of every area from IPI's written confirmation of the
dates to the published final account, so that no step starts before the
step it depends on and no hard date from the guide is missed.**

## Background

Each area has its own timing, and they depend on each other: no
announcement before the venue and dates are confirmed, no CFP without a
website, no supporter menu without a date. The RubyEvents guide sets the
hard points: lock "Date, venue, rough budget" before announcing; sponsors
"allocate conference budgets in advance, sometimes by the previous
November"; "Open the CFP four to six months before the event"; "Most
tickets are sold in the last weeks before the conference"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`).
On 2026-10-07 about eight months remain, which the guide calls "doable
but stressful" (§ Give yourself a year).

The calendar cannot use fixed event dates yet. The organiser asked to
keep the dates flexible and prepare options for IPI Academy, whose
answer decides (`sources/conversations/2026-10-07--org--date-options-for-ipi.md`);
six options span Tuesday 1 June to Sunday 13 June 2027, with the core
day between Thursday 3 June and Saturday 12 June, including options where
every lecture day is a weekday
(`sources/conversations/2026-10-07--org--weekday-lecture-days.md`,
[the dates pitch](../pitches/dates-format-and-schedule.md)). Registration
opens as soon as IPI confirms in writing, likely November 2026
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
So the calendar hangs on two anchors: the day IPI confirms, and the core
day IPI picks.

## Affected personas

- [Speaker](../../../.claude/personas/users/speaker.md). They need a CFP
  that opens early enough to arrange their own travel, closes on the day
  it says, and answers them within two weeks. The calendar holds those
  dates.
- [Attendee](../../../.claude/personas/users/attendee.md). They need the
  date, the free registration and the travel facts early enough to plan
  a cheap trip, and a reminder to reconfirm so an early free place is not
  forgotten.
- [Hiring partner](../../../.claude/personas/users/hiring-partner.md).
  They need the supporter menu in November 2026, before their 2027
  budgets close.
- [Volunteer](../../../.claude/personas/users/volunteer.md). They need to
  know when the calls start and when their domain's work is due.
- [Extension host](../../../.claude/personas/users/extension-host.md).
  They need to know when extension slots open and the last day to submit.

## Now / Perceived / Target

- **Now (2026-10-07).** Every pitch is bet on and graduating into a PRD
  (`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`). No
  date is confirmed, nothing is announced, no site, registration or CFP
  exists. The organiser has visited IPI many times in 2026, so a first
  venue visit is not a pending step
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- **Perceived.** The October steps look small, but every later date
  hangs on IPI's written confirmation. If it slips past November 2026,
  the CFP and the supporter asks slip with it, and the November budget
  window closes. The pitch's table assumed the second week; until IPI
  answers, any fixed date in it is a guess.
- **Target.** A single calendar page under `wiki/org/` whose steps are
  dated from the two anchors, reviewed at every call, with each step
  marked done, late or moved, and the final account published within two
  weeks of the event.

## Scope

The calendar holds these steps, in this order. Months are the plan if IPI
confirms in October or November 2026; every step after the confirmation
moves with it.

| When | What | Area |
|------|------|------|
| October 2026 | Propose the six date options to IPI and ask for written confirmation of dates and rooms; ask IPI's student club about volunteering; open the public budget ledger | Dates, Operations, Budget |
| On IPI's written confirmation (aimed for November 2026) | Website v1 at muhamed.at/goatconf, written here and copied over (when, where, who, why, code of conduct, the budget ledger); registration and the email list open; the date announced | Website, Design, Social, Operations |
| November 2026 | Supporter menu published and personal asks begin, before 2027 budgets close | Supporters |
| November to December 2026 | The one or two invited speakers confirmed | CFP |
| About six months before the core day (mid-December 2026) | CFP opens by simple form, with the invited names; extension slots open | CFP, Extensions |
| Late January 2027 | CFP closes, on the day it said | CFP |
| February 2027 | Review in two weeks; accepted speakers told first, declined promptly; volunteer calls every two weeks begin | CFP, Operations |
| March 2027 | Registrants asked to reconfirm; speakers announced; prices and travel page live | Website, Social, Activities |
| April 2027 | Full schedule; extension listings filling; the goat hunt's clues written | Dates, Extensions, Activities |
| May 2027 | Run sheet with an owner per domain; reminders and waiting-list releases | Operations, Website |
| Five or more days before the event | A courtesy notice to the police, only if the organiser or IPI chooses to send one (Article 36's period, `sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md`) | Operations |
| The days IPI picks, first or second week of June 2027 | Arrivals and fringe, workshops, the core day, the lake day | All |
| Within a week of the core day | Feedback survey sent | Operations |
| Within two weeks of the core day | Final account published from the public ledger | Budget |
| Summer 2027 | What worked becomes the reusable kit | Epic |

The social drumbeat runs under all of it.

## No-gos

- No public announcement before IPI confirms the dates and rooms in
  writing.
- No CFP closing date extended after it is published.
- No fixed event date written into the calendar before IPI picks one.
- No step that spends money through the organiser or pays for food or
  drink from the organiser's money.
- No public act (an announcement, a message to IPI, a post) made by an
  agent; the agent drafts the step, the organiser takes it.

## Rabbit holes

- **Turning the calendar into project management software.** It is one
  page in this repository. If it needs a tool, an integration or a
  dashboard, stop and re-pitch.
- **Slipping the October steps.** Every later date hangs on IPI's written
  confirmation; when it slips, move the whole calendar at the next call
  rather than squeezing the CFP.
- **Announcing before signing,** against the guide's first rule.

## Appetite

**Small.** One page, written once and adjusted at each call every two
weeks. The work it orders belongs to the other PRDs; this PRD only keeps
their order and dates honest.

## Success metrics

- **IPI confirms dates and rooms in writing by 30 November 2026.**
  Observed as a snapshot of the confirmation under `sources/`, dated.
- **The CFP opens at least five months before the core day and closes on
  its published date.** Observed from the commit dates of the CFP page's
  opening and closing notes on the site's source in this repository.
- **No step on the calendar is more than four weeks late at any call from
  February 2027.** Observed from the calendar page's done, late or moved
  marks in its git history.
- **The final account is published within two weeks of the core day.**
  Observed as the ledger page's final-account commit date against the
  core day's date.

## Dependencies

- [Dates and the core day](./dates-and-the-core-day.md): the second
  anchor, the core day IPI picks.
- [Website and registration](./website-and-registration.md): site v1 and
  registration, on the first anchor.
- [CFP and speakers](./cfp-and-speakers.md): the CFP window and review.
- [Supporters and hiring](./supporters-and-hiring.md): the November menu.
- [Budget and the public ledger](./budget-and-public-ledger.md): the
  ledger opens in October and closes with the final account.
- [Social drumbeat](./social-drumbeat.md): the weekly rhythm under it.
- [Design with impeccable](./design-with-impeccable.md): the site's
  design, due with v1.
- [Extension slots and the record](./extension-slots-and-the-record.md):
  when extension slots open and close.
- [Activities: the lake and the town](./activities-lake-and-town.md): the
  prices page and the goat hunt's clues.
- [Operations and the day](./operations-and-the-day.md): volunteers, the
  calls, the run sheet, the survey.

## Decisions already made by the organiser

- The conference is in Tuzla in the first or second week of June 2027
  (`sources/conversations/2026-10-07--org--conference-vision.md`); the
  dates are options for IPI, not fixed
  (`sources/conversations/2026-10-07--org--date-options-for-ipi.md`),
  including weekday-only lecture days
  (`sources/conversations/2026-10-07--org--weekday-lecture-days.md`).
- Registration opens when IPI confirms the date in writing; the CFP is a
  simple form; the budget ledger lives on muhamed.at/goatconf
  (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
- One or two invited speakers from the organiser's network, the rest from
  an open call; the site is under muhamed.at, written here and copied over
  (`sources/conversations/2026-10-07--org--talks-team-and-site.md`), at
  the path /goatconf
  (`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
- No money passes through the organiser; the budget is public; IPI is
  already visited
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- This repository will be public, and extensions come in by pull request
  or the CFP's form tool
  (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

## Open questions

- Can IPI confirm in writing in October or November 2026?
- Is mid-December too close to the holidays for opening a CFP, or a help
  (people have time to write)?
- When the organiser flips this repository to public, and whether the
  calendar should say so as a step.
- The last day an extension can be submitted and still be listed
  (unknown, needs source).

## Decision needed

**Is the calendar kept as fixed calendar dates, or as steps anchored to
IPI's written confirmation and the core day, and where does it live?**
The ADR records the chosen shape of the calendar page (its anchors, its
done, late or moved marks, and its review at each call every two weeks)
and the CFP window it implies.

**Answered by the ADR** [Anchor the road calendar to IPI's confirmation and the core day, not to fixed dates](../adrs/road-to-june-2027.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** The calendar's dates move with the decisions of 2026-10-12: the core days are Thursday 3 and Friday 4 June 2027 and Saturday 5 June is the community day; the call opens with the site on goatconf.com and has no strict deadline, so the call and schedule dates are targets; registration is a Google Form; the site is goatconf.com, not muhamed.at/goatconf. See [Dates: two core days](../adrs/two-core-days-first-week.md), [The call: the organiser judges](../adrs/call-organiser-judges.md), [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** The first anchor is reached. IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. The October and November steps that waited on IPI's confirmation are due now, and the metric "IPI confirms dates and rooms in writing by 30 November 2026" is met as reported, though no written snapshot is under `sources/` (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-14, read with the later decisions.** The first amendment above no longer holds on registration: registration is on the organiser's Luma event, not a Google Form, with no limit; the organiser approves each registration, seats are first come, first served at each room's door, and ticket holders register for sessions later, with the tool not decided yet (sources: sources/conversations/2026-10-12--org--registration-on-luma.md, sources/conversations/2026-10-12--org--first-come-luma-only.md, sources/conversations/2026-10-12--org--approval-back-on.md, sources/conversations/2026-10-12--org--session-registration-later.md). The calendar's ledger steps (open the public ledger in October, publish a final account after the event) are dropped: the budget is private, with no budget page and no public ledger; online supporters pay the organiser's Austrian business 500 EUR for online perks only, and speakers' travel is refunded only if the budget allows, never promised (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md). The calendar page this plan names, `wiki/org/road-calendar.md`, does not exist yet.
