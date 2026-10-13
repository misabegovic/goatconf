---
title: "Online supporters pay the organiser's Austrian business; the budget becomes private"
kind: decision
status: proposed
updated: 2026-10-13
confidence: low
supersedes: org/adrs/budget-and-public-ledger.md
depends_on:
  - org/adrs/speakers-and-travel-supporters.md
  - org/adrs/supporters-and-hiring.md
sources:
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/web/legal/online-sponsorship-austria-bih-2026-10-13.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
---

# Online supporters pay the organiser's Austrian business; the budget becomes private

Proposed 2026-10-13 from the organiser's answers
(`sources/conversations/2026-10-13--org--online-supporters-through-the-business.md`).
Not accepted until the organiser approves this draft.

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
  included; anything still left carries to the next GoatConf. (The organiser's answer was given before
  travel grants were dropped; this reading needs confirming.)
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

## Related

- [Keep the public ledger as one CSV file here](../adrs/budget-and-public-ledger.md), superseded by this.
- [Speaker profiles and travel supporters](../adrs/speakers-and-travel-supporters.md)
- [Supporters and hiring](../adrs/supporters-and-hiring.md)
- `sources/conversations/2026-10-13--org--online-supporters-through-the-business.md`
- `sources/web/legal/online-sponsorship-austria-bih-2026-10-13.md`
