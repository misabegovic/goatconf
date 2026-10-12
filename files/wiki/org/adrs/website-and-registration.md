---
title: "Register on Luma, capped at the hall, with pages copied into muhamed.at/goatconf"
kind: decision
status: superseded
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/website-and-registration.md
sources:
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/web/tooling/luma-pricing.md
  - sources/web/tooling/luma-help-center.md
  - sources/web/tooling/luma-privacy-policy.md
  - sources/web/tooling/pretix-hosted-pricing.md
  - sources/web/tooling/tito-pricing.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md
  - sources/web/funding/fosdem-charter.md
superseded_by: org/adrs/goatconf-ba-and-google-forms.md
---

# Register on Luma, capped at the hall, with pages copied into muhamed.at/goatconf

> **Superseded 2026-10-12** by [goatconf ba and google forms](goatconf-ba-and-google-forms.md), on the organiser's approval (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`). Kept as the record of the earlier decision.

Answers the "Decision needed" of
[Website and registration](../prds/website-and-registration.md).
Accepted 2026-10-07 from the organiser's answers
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 1), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

GoatConf 2027 registers people on Luma. One Luma event covers the core
day, capped at the hall's about 120 seats with Luma's waiting list
switched on, and asks only for a name, an email address and two optional
questions: accessibility needs, and whether the person wants hiring
partners to see them (see
[Supporters and hiring](supporters-and-hiring.md)). The website's pages
are written in this repository and copied into muhamed.at/goatconf by the
organiser at each publish; the extension list is built here from the
extension records before the copy.

## Why

The organiser asked for registration per hall capacity ("I would register
per hall capacity",
`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`)
and picked Luma among the four tools the PRD weighed. Luma's free plan
offers "Unlimited number of guests per event", check-in at the door,
"Require approval or token gating for registration", CSV export and email
blasts to guests (`sources/web/tooling/luma-pricing.md`), and its help
centre documents a waiting list "when your event reaches capacity" and a
guest-list CSV download "for analysis, printing badges"
(`sources/web/tooling/luma-help-center.md`). For a free event the 5%
platform fee never applies. The same tool then carries the email list
([Social drumbeat](social-drumbeat.md)) and the open-to-work question, so
attendees meet one tool rather than three.

## How

The registration page links from the site's home and program pages. The
form opens when IPI confirms the date in writing, as the organiser chose
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
In spring, registrants are asked to reconfirm, and places not reconfirmed
go to the waiting list; a reminder goes out in the week before. On the
day, the door volunteer checks people in on Luma, with a printed list
from the CSV export as the fallback when the venue's Wi-Fi fails.

The form carries the notice Bosnia and Herzegovina's personal data law
asks for: who holds the data, why, on what basis, for how long, and what
rights people have
(`sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md`). The
list is kept until the feedback survey is sent, then deleted from Luma,
and is never shared, after FOSDEM's charter
(`sources/web/funding/fosdem-charter.md`). Nothing from the guest list
enters this public repository.

## Alternatives

- **Luma** *(chosen)*: free for free events, waiting list, check-in, email
  to guests, and a subscription audience in one place.
- **Hosted pretix:** "500 free tickets per year" and the strongest
  check-in (`sources/web/tooling/pretix-hosted-pricing.md`); it was the
  pitch's recommendation, and loses on having no built-in way to write to
  followers before registration opens.
- **Tito:** a polished ticketing tool whose pricing is built around paid
  tickets (`sources/web/tooling/tito-pricing.md`).
- **A plain form** in the CFP's form tool: no waiting list, no check-in,
  all of it by hand.

## Consequences

- **Opens:** one tool for registration, reminders, the email list and the
  open-to-work opt-in; a ready check-in at the door.
- **Costs:** Luma Labs, Inc. is a US company, and its privacy policy says
  registrants' data is shared with the event host and retained "for the
  period necessary to fulfill obligations to the law", but does not say
  where the data is stored (`sources/web/tooling/luma-privacy-policy.md`).
  Where it is stored, and whether the organiser or IPI is the controller
  named in the notice, are (unknown, needs source) and must be settled
  before the form opens.
- **Costs:** the free plan sends "up to 500 invites or newsletters per
  week" (`sources/web/tooling/luma-pricing.md`). Messages to an event's
  own guests are not capped ("You can always send unlimited blasts to
  event guests", same source), so the limit binds only the followers who
  have not registered.
- **Closes:** a self-hosted registration whose data never leaves Europe,
  unless this ADR is superseded.

## Linked PRD

[Website and registration](../prds/website-and-registration.md).

## Build notes

*(empty until the work ships)*
