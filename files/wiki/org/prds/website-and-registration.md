---
title: "Website and registration: goatconf.com and a free pass per core day"
kind: initiative
status: living
updated: 2026-10-12
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/website-and-registration.md
sources:
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/web/organiser/muhamed-at-about.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/tooling/pretix-hosted-pricing.md
  - sources/web/tooling/pretix-features.md
  - sources/web/tooling/tito-pricing.md
  - sources/web/tooling/luma-pricing.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/funding/fosdem-charter.md
---

# Website and registration: goatconf.com and a free pass per core day

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md).
It graduates the pitch
[A website of plain pages and a free registration with a cap](../pitches/website-and-registration.md),
bet on by the organiser on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`).

## Objective

**GoatConf has a site at muhamed.at/goatconf, written in this repository
and copied over when published, that says when, where, who and why, and
carries the code of conduct, travel basics, the program, the extension
list and the public budget; and, from the day IPI confirms the date, a
free registration capped at about 120 with a waiting list.**

## Background

The guide puts the site first: "As soon as you have a date and venue,
put up a simple website", saying when, where, who it is for and why
come, with the code of conduct, travel basics and accessibility added
early (`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Your website). It is also what supporters read to judge whether an
event is credible.

The organiser has decided where the site lives and how it is made: a
page on their own site, no new domain, with the page sources "in
goatconf, copied over", designed with impeccable here
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`), at
the path /goatconf
(`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
muhamed.at runs on a clone of pi-brain
(`sources/web/organiser/muhamed-at-about.md`), so the copied pages follow
that site's conventions. The public budget ledger is one of the site's
pages, written here and copied over like the rest
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).

Registration was "needed (if permitted, something like that)"
(`sources/conversations/2026-10-07--org--conference-vision.md`). The
organiser has since set its cap ("I would register per hall capacity",
about 120,
`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`)
and its timing: it opens as soon as IPI confirms the date in writing,
likely November 2026
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).

## Affected personas

- [Attendee](../../../.claude/personas/users/attendee.md). Today there is
  nothing to read and nowhere to sign up. With this shipped, an attendee
  finds the date, the place, the cost of the trip and the code of conduct
  on one site, registers for free with a name and an email, and reconfirms
  once in spring.
- [Speaker](../../../.claude/personas/users/speaker.md). Finds the call
  for talks and its terms (travel is theirs) on the site, and later their
  own talk on the program.
- [Extension host](../../../.claude/personas/users/extension-host.md).
  Sees their addition on the site's extension list, built from the record
  files in this repository.
- [Hiring partner](../../../.claude/personas/users/hiring-partner.md).
  Reads the supporters page and the charter, and reaches only attendees
  who chose to be seen.

## Now / Perceived / Target

- **Now (2026-10-07):** no site, no registration. The path,
  muhamed.at/goatconf, and the way pages are made (here, copied over) are
  decided. This repository is private and is to become public
  (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).
- **Perceived:** that a free event fills its room. A free place is easy
  to take and easy to forget, and the no-show rate for GoatConf is
  (unknown, needs source) until measured.
- **Target:** a first page live as soon as the date is confirmed, pages
  added as the event fills in, registration open from the confirmation
  with a cap of about 120 and a waiting list, and a check-in list on the
  day.

## Scope

**The site.** A handful of plain pages: home, program, travel and stay,
accessibility, code of conduct, extensions, supporters, the budget
ledger, contact. They are written and designed in this repository with
impeccable (see [Design with impeccable](design-with-impeccable.md)) and
copied into muhamed.at/goatconf when published; each publish is a public
act and the organiser's. Content follows the guide's order: first when,
where, who and why; then the code of conduct and travel basics; then the
call for talks, the supporters page and the program as they exist. The
trip is sold before the lineup: Tuzla, the lake, the low cost (guide,
§ What you are selling). The extension list is built here from the
extension record files and copied with the rest, since muhamed.at cannot
read this repository's files itself. Everything is in English
(`sources/conversations/2026-10-07--org--first-answers.md`, question 7).

**Registration.** Free, capped at about 120, with a waiting list. It
collects only what the event needs: a name for the badge, an email, and
optional questions (accessibility needs, and whether the attendee wants
hiring partners to see them), following FOSDEM's charter line that
"attendees are not required to submit personal information to attend
unless law or safety mandate it" (`sources/web/funding/fosdem-charter.md`).
It opens when IPI confirms the date. Because a free place is held for
about seven months, registrants reconfirm once in spring, unconfirmed
places go to the waiting list, and a last reminder goes out the week
before. On the day, a check-in list confirms who came.

The pitch recommended hosted pretix, whose plan includes "500 free
tickets per year" and has a waiting list and check-in
(`sources/web/tooling/pretix-hosted-pricing.md`,
`sources/web/tooling/pretix-features.md`), with Tito
(`sources/web/tooling/tito-pricing.md`), Luma
(`sources/web/tooling/luma-pricing.md`) and a plain Tally form
(`sources/web/tooling/tally-pricing.md`) as fallbacks. That choice is the
ADR's to make.

## No-gos

- No paid tickets, and no "supporter" upsell in registration.
- No data collected that the event does not use; nothing sold or shared.
- No login or account system on the site.
- No new domain for 2027.
- No custom-built site generator or registration system.
- No registration before IPI confirms the date in writing.
- No payment taken through the site; no money passes through the
  organiser
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- No publishing without the organiser.

## Rabbit holes

- **Building a custom site or registration system.** Tempting for a
  technical organiser; it costs the evenings the program needs. Stop and
  use a hosted tool.
- **Fighting the host site's conventions.** muhamed.at is a pi-brain
  clone; if the copied pages need that site changed in more than small
  ways, stop and re-pitch.
- **No-shows.** Reminders and releasing unconfirmed places matter more
  than the tool. An overbooking margin is (unknown, needs source) until
  measured; do not guess one larger than the waiting list can absorb.
- **Data protection.** Names and emails are personal data under Bosnian
  and EU rules; how the law applies is for operations (unknown, needs
  source).
- **The list builder.** Rendering the extension list must stay a small
  step; if it grows into a site generator, stop.

## Appetite

**Small.** A few evenings for a first page and the registration set-up,
then steady additions as the event fills in. The site grows from one
page; registration is configured once and opened on the confirmation.

## Success metrics

- **The first page is live at muhamed.at/goatconf within two weeks of
  IPI's written confirmation.** Observed from the page's first publish
  date against the confirmation's date in `sources/`.
- **Registration opens within a week of IPI's written confirmation.**
  Observed from the registration tool's opening date.
- **90 or more of about 120 registrants check in on the day.** Observed
  from the registration tool's check-in export, counted the day after.
- **No registration question beyond name, email and the optional ones
  named here.** Observed from the registration form's own export of its
  questions at opening.

## Dependencies

- [Dates and the core day](dates-and-the-core-day.md): the confirmed date
  opens registration and the cap comes from the hall.
- [Design with impeccable](design-with-impeccable.md): the look the pages
  are built on.
- [Extension slots and the record](extension-slots-and-the-record.md):
  the record files the extension list is built from, and the charter
  page.
- [Budget and the public ledger](budget-and-public-ledger.md): the ledger
  is a page on this site.
- [CFP and speakers](cfp-and-speakers.md): the call is linked from the
  site, and the program comes from it.
- [Operations and the day](operations-and-the-day.md): the code of
  conduct, the data-protection question and check-in on the day.

## Decisions already made by the organiser

- **The site is a page on muhamed.at, no new domain.**
  `sources/conversations/2026-10-07--org--talks-team-and-site.md`.
- **Pages are written and designed in this repository and copied over
  when published.** Same source.
- **The path is /goatconf.**
  `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **The public budget ledger is a page on muhamed.at/goatconf.**
  `sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`.
- **Registration opens when the date is confirmed in writing.** Same
  source.
- **The call for talks uses a simple form.** Same source.
- **Registration is capped at the hall, about 120.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`.
- **This repository will be public.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.
- **English.** `sources/conversations/2026-10-07--org--first-answers.md`,
  question 7.

## Open questions

- Is registration legally or practically required, and what does the law
  ask of the list it keeps? (unknown, needs source)
- How the copied pages fit muhamed.at's own layout and navigation.
- What overbooking margin, if any, the waiting list allows.

## Decision needed

Which registration tool GoatConf uses: hosted pretix (free quota,
waiting list, check-in), Tito, Luma, or a plain form in the same tool as
the call for talks. The ADR also records how the pages are copied into
muhamed.at/goatconf and how the extension list is built before the copy.

**Answered by the ADR** [Register on Luma, capped at the hall, with pages copied into muhamed.at/goatconf](../adrs/website-and-registration.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** The site's home is goatconf.com, published on GitHub Pages from this repository; muhamed.at/goatconf is superseded. Registration is a Google Form, one free pass per core day, replacing Luma; the cap is per room at the door. Talk proposals, add-something submissions and contact (including code-of-conduct reports) are Google Forms too, created by the script in the repository. See [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md), [Dates: two core days](../adrs/two-core-days-first-week.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. Nothing on the site or the registration form waits on IPI any longer (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
