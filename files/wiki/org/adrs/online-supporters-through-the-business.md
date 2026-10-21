---
title: "Online supporters pay the organiser's Austrian business; the budget becomes private"
kind: decision
status: accepted
updated: 2026-10-21
confidence: medium
supersedes: org/adrs/budget-and-public-ledger.md
depends_on:
  - org/adrs/speakers-and-travel-supporters.md
  - org/adrs/supporters-and-hiring.md
sources:
  - sources/conversations/2026-10-21--org--wroclove-rb-community-partner.md
  - sources/conversations/2026-10-19--org--site-review-decisions.md
  - sources/conversations/2026-10-18--org--speaker-travel-first-recording-main-hall-150.md
  - sources/conversations/2026-10-18--org--event-hosts-as-supporters.md
  - sources/conversations/2026-10-14--org--speakers-dinner.md
  - sources/conversations/2026-10-14--org--decisions-one-by-one.md
  - sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/web/legal/online-sponsorship-austria-bih-2026-10-13.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
---

# Online supporters pay the organiser's Austrian business; the budget becomes private

Accepted 2026-10-13 by the organiser ("Approve and roll out"), from their
answers in `sources/conversations/2026-10-13--org--online-supporters-through-the-business.md`.

## What

- **One online level, 500 EUR.** A company becomes an online supporter of
  GoatConf 2027 for 500 EUR plus VAT where it applies. Every online
  supporter gets the same: its logo and link on the site, one social post,
  and a mention in emails to registered attendees. Nothing at the venue:
  no booth, no banner, no tickets, no logo in the halls.
- **Paid to the organiser's Austrian business.** The business invoices
  the supporter under a short written agreement. This lifts the rule "No
  money goes though me" (`sources/conversations/2026-10-07--org--no-money-through-me.md`)
  for online supporters only.
- **The money pays event costs.** Whatever the event needs and nobody
  else covers. No supporter pays for a named speaker, and no speaker is
  credited to a supporter.
- **Speakers pay their own travel.** If the budget allows, the organiser
  may refund some or all of a speaker's travel afterwards. It is never
  promised or guaranteed, and the site says so.
- **A surplus** pays more of the event's costs, speakers' travel refunds
  included; anything still left carries to the next GoatConf. The
  organiser approved this reading of their answer.
- **The budget is private.** The budget page, `ledger.csv` and the home
  page's "Every euro in the open" section go. The site says nothing about
  the budget, and does not offer a summary.
- **Paying a supplier directly or giving in kind stays possible** for
  anyone who prefers it.

## Why

The organiser wants money that helps with costs nobody covers, and has a
business registered in Austria with a valid VAT ID that can be used for
event management (same source). Online-only perks keep the tax simple:
for business sponsors they are an advertising service taxed where the
sponsor is based, so the event being in Tuzla does not pull the
sponsorship into Bosnian VAT; venue perks could
(`sources/web/legal/online-sponsorship-austria-bih-2026-10-13.md`).
A single level treats every supporter alike.

## How

- **Invoices:** Austrian business supporters pay 20% Austrian VAT; EU
  business supporters are invoiced net under reverse charge and reported
  in the recapitulative statement; supporters outside the EU pay no
  Austrian VAT (same research source).
- **The agreement** lists the online perks and how long they run, says
  there is nothing at the venue, says the money pays event costs and is
  not a donation, gives a pro rata refund if the event is cancelled,
  licenses the logo for promotion only, and gives the supporter no say
  over the program. Austrian law applies.
- **Before the first invoice,** the organiser confirms with a tax
  adviser: the trade licence's scope, the small business status, the
  advertising classification, money received in 2026 for a 2027 event,
  how to document travel refunds to speakers, and the surplus.
- **The site:** the supporters page offers the online level and keeps the
  direct and in-kind routes; every sentence saying no money passes
  through the organiser, or pointing to the budget, is rewritten or
  removed (charter, supporters, speakers, talk, propose an event, home,
  footer links, `llms.txt`, README).

## Alternatives

- **Keep "no money through the organiser".** Rejected by the organiser.
- **Travel grants for named speakers.** Dropped by the organiser.
- **Two or three levels.** The organiser chose one.
- **A public budget, in full or as totals.** The organiser chose private.
- **A fiscal host or association.** Slower to set up, a fee, and no
  advantage for online-only perks.

## Consequences

- The organiser's business carries the money, the paperwork and the tax.
- Speakers still pay their own travel; a refund depends on the budget and
  is never promised.
- A private budget removes a promise the site made from the start
  ("Every euro in the open"); the site stops making it rather than
  keeping it quietly.
- Supporters can deduct the cost as advertising when the agreement is
  written in advance and the perks are visible and documented.

## Amendments

- **2026-10-13, a speaker's company that covers their travel.** A company that pays its own speaker's travel is listed on the site as a supporter, the same as online supporters, with its logo and link. No money goes through the organiser for it, so there is nothing to invoice. This is the speaker's own employer paying for its own person; a supporter still never pays for another company's or a named outside speaker's travel (source: sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md).
- **2026-10-14, the surplus, confirmed.** Leftover money pays more of this year's event costs, speaker travel refunds included where the organiser decides, and anything still left carries to the next GoatConf. The organiser confirmed this reading of their earlier answer (source: sources/conversations/2026-10-14--org--decisions-one-by-one.md).
- **2026-10-14, the speakers dinner is an event cost.** The money may pay for the speakers dinner for accepted speakers, if the budget allows (source: sources/conversations/2026-10-14--org--speakers-dinner.md).
- **2026-10-18, the speakers dinner is no longer paid from this money.** The organiser pays for the speakers dinner, whatever the budget, so the 2026-10-14 amendment above no longer holds (source: sources/conversations/2026-10-18--org--organiser-pays-speakers-dinner.md).
- **2026-10-18, a host that funds and organises an accepted event.** A host, whether a person, a group or a company, that funds and organises an event the organiser accepted as part of GoatConf 2027 is listed on the site as a supporter, the same as online supporters, with its logo and link, if it agrees. No money goes through the organiser, so there is nothing to invoice. Its line names the event. Being listed buys nothing: no talk, no stage time, no say over the program and nothing at GoatConf's venue. The first is the Bosnia & Herzegovina Futures Foundation, for the BH Professionals Meetup on Saturday 5 June 2027 (source: sources/conversations/2026-10-18--org--event-hosts-as-supporters.md).
- **2026-10-18, self-funded speakers' travel comes first.** Of the surplus, refunds to speakers who pay their own travel come first, before other costs it may pay; still never promised (source: sources/conversations/2026-10-18--org--speaker-travel-first-recording-main-hall-150.md).
- **2026-10-19, the site no longer names the Austrian business.** Online supporters still pay the organiser's Austrian business, but the supporters page, the charter and llms.txt no longer say so: the supporters page says whom a supporter reaches (the 120 to 300 engineers, designers, product people and founders who come), that supporters reach Muhamed, the organiser, through the contact form or by email, and carries a "Become a supporter" button to the contact form (source: sources/conversations/2026-10-19--org--site-review-decisions.md).
- **2026-10-21, a community partner that gives in kind.** A community partner that supports GoatConf in kind, such as by sharing it on its social media, is listed on the site as a supporter, the same as online supporters, with its logo and link, in the same list. No money goes through the organiser, so there is nothing to invoice. Being listed buys nothing: no talk, no stage time, no say over the program and nothing at GoatConf's venue. The first is wroclove.rb, the Ruby conference in Wrocław, for "Community partner: social media" (source: sources/conversations/2026-10-21--org--wroclove-rb-community-partner.md).


## Related

- [Keep the public ledger as one CSV file here](budget-and-public-ledger.md), superseded by this.
- [Speaker profiles and travel supporters](speakers-and-travel-supporters.md)
- [Supporters and hiring](supporters-and-hiring.md)
- `sources/conversations/2026-10-13--org--online-supporters-through-the-business.md`
- `sources/web/legal/online-sponsorship-austria-bih-2026-10-13.md`
