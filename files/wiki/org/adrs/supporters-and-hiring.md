---
title: "Ask about open to work as an unticked Luma question, shared only for those who tick it"
kind: decision
status: accepted
updated: 2026-10-14
confidence: medium
depends_on:
  - org/prds/supporters-and-hiring.md
sources:
  - sources/conversations/2026-10-13--org--evening-event-karaoke-hackathon.md
  - sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/web/tooling/luma-help-center.md
  - sources/web/hiring/strangeloop-privacy-policy.md
  - sources/web/hiring/leaddev-london-terms.md
  - sources/web/funding/writethedocs-portland-2026-prospectus.md
  - sources/web/funding/fosdem-charter.md
---

# Ask about open to work as an unticked Luma question, shared only for those who tick it

Answers the "Decision needed" of
[Supporters and hiring](../prds/supporters-and-hiring.md). Accepted 2026-10-07 from the organiser's answer
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 9), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

Luma's registration form carries one optional, unticked question: "Would
you like hiring partners at GoatConf to see your name and a link you
choose?", with a field for the link. Only people who tick it are shared,
and only their name and that link, with the hiring partners listed on the
site. Nobody else's data is shared with anyone. A supporter is recorded
as an extension record of the kind "support", like any other extension.

## Why

The organiser picked the opt-in question over a badge mark, both, or no
signal. It lives where people already register, so there is no extra
form, and it shares the least that makes an introduction possible. It
keeps the line every source the PRD cited draws: "We do not share any
attendee information with sponsors"
(`sources/web/funding/writethedocs-portland-2026-prospectus.md`), Strange
Loop's never share or sell
(`sources/web/hiring/strangeloop-privacy-policy.md`), and LeadDev's
"Choosing not to have your badge scanned will not affect your
participation in the event" (`sources/web/hiring/leaddev-london-terms.md`).

## How

The organiser exports the ticked rows from Luma's guest list
(`sources/web/tooling/luma-help-center.md`), keeps only the name and
link, and sends that short list to each hiring partner a fortnight before
the event and again on the day. The list never enters this public
repository. Hiring partners agree, when they join, to delete it within
two weeks of the event and not to pass it on; the organiser deletes the
export at the same time. Ticking or not changes nothing else about a
person's place.

A supporter's record carries the item funded, the supplier the supporter
pays or the gift in kind, and how the supporter wants to be named, or "an
anonymous supporter"; the money never passes through the organiser
(`sources/conversations/2026-10-07--org--no-money-through-me.md`), and the
same line appears on the public ledger
([Budget and the public ledger](budget-and-public-ledger.md)).

## Alternatives

- **An opt-in Luma question** *(chosen)*: no extra form, least data
  shared, consent recorded at registration.
- **A badge mark only:** nothing shared in advance; companies cannot
  prepare.
- **Both:** more reach, and a second thing to explain and print.
- **Neither:** the job board and hiring corner alone; the attendee who
  wants an introduction has no way to say so.

## Consequences

- **Opens:** introductions that start from the attendee's choice.
- **Costs:** the partners' promise to delete is a promise; GoatConf has
  no way to enforce it beyond not inviting them again.
- **Closes:** any sale or wider sharing of the attendee list, in line
  with the charter (`sources/web/funding/fosdem-charter.md`).

## Linked PRD

[Supporters and hiring](../prds/supporters-and-hiring.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-12.** Luma is no longer used. The same optional, unticked open-to-work question sits on the registration Google Form, and the organiser exports the ticked rows from its response sheet. See [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-13, money through the organiser's business.** "The money never passes through the organiser" no longer holds for online supporters, who pay the organiser's Austrian business 500 EUR for online perks only ([Online supporters pay the organiser's Austrian business](online-supporters-through-the-business.md); source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
- **2026-10-14, registration is back on Luma.** On 2026-10-12 registration moved to the organiser's Luma event, so the registration Google Form in the first amendment does not exist (source: sources/conversations/2026-10-12--org--registration-on-luma.md). The Luma event asks one optional question, why the person wants to come, and not the open-to-work question (source: sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md). Whether and where the open-to-work question returns is (unknown, needs source). "Support" is no longer a kind on the propose-an-event form; the add page points people who want to support GoatConf to the supporters page, and the older `support` kind stays accepted in the records (source: sources/conversations/2026-10-13--org--evening-event-karaoke-hackathon.md).
