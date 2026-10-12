---
title: "A base budget others cover, a menu of stretch goals, and every line public"
kind: initiative
status: living
updated: 2026-10-12
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/budget-a-goat-and-a-menu.md
sources:
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/tooling/pretix-hosted-pricing.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/tooling/obs-project.md
  - sources/web/tooling/videographer-rates-2026-ruah.md
  - sources/web/tuzla/numbeo-cost-of-living-tuzla.md
  - sources/web/tuzla/easybalkan-bosnia-costs-2026.md
  - sources/web/tuzla/slana-jezera-cijene-kurir-2026-08.md
  - sources/web/tuzla/cbbh-exchange-rate-2026-10-07.md
  - sources/web/funding/balkanruby-sponsorship.md
  - sources/web/funding/euruko-2024-sponsoring.md
  - sources/web/funding/fosdem-charter.md
---

# A base budget others cover, a menu of stretch goals, and every line public

Product requirements for GoatConf 2027's money. It graduates the pitch
[The budget: a base under 1,000 EUR and a menu](../pitches/budget-a-goat-and-a-menu.md),
on which the organiser bet on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`), and sits
under the epic [GoatConf 2027](../epics/goatconf-2027.md).

## Objective

**A public ledger on muhamed.at/goatconf, kept current from the first line,
that shows what GoatConf 2027 costs, who covered each item (a supporter
paying a supplier, a gift in kind, or the organiser's fallback), and which
stretch goals are funded, so that the event runs with no money passing
through the organiser and anyone can check every euro.**

## Background

GoatConf is free to attend, so there is no ticket income
(`sources/conversations/2026-10-07--org--conference-vision.md`). The
organiser set a ceiling of "Up to 1,000 EUR" of their own money, "truly
minimal: the venue is the partner's, everything else volunteer or
sponsored" (`sources/conversations/2026-10-07--org--first-answers.md`,
question 8), and then narrowed it to a fallback: "Just in case there are
any expenses I need to cover. Normally, I pay for nothing also"
(`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`,
question 1). It never pays for food or drink: "I am not paying for food or
drinks... Nothing. Just leaving space either for others to cover or for
folks to pay themselves"
(`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).

Two further decisions set the shape: "Sponsors can provide no money
directly to me. No money goes though me", and "We also need to be
transparent about the budget"
(`sources/conversations/2026-10-07--org--no-money-through-me.md`). The
ledger's home is a budget page on the site, written in this repository and
copied over like the rest
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`,
question 2).

The guide's method fits with one change of trigger: a base budget, "the
minimum required to run the event", plus stretch goals that unlock only
when money arrives
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Base budget and stretch goals). At GoatConf a stretch goal unlocks when a
supporter funds it, not when tickets sell. The guide also warns that a
first conference is "likely to lose money... or barely break even" (guide,
§ Money); by design, the most the organiser can lose here is the fallback.

## Affected personas

- **[Attendee](../../../.claude/personas/users/attendee.md).** *Now:* no
  idea what GoatConf costs or who pays. *Target:* can read what the free
  event costs, who covered it, and knows in advance that coffee and lunch
  are on them unless a supporter's line says otherwise.
- **[Hiring partner](../../../.claude/personas/users/hiring-partner.md).**
  *Now:* no priced way to help. *Target:* a menu of items with estimated
  amounts and named suppliers, and their own line visible on the ledger
  before they are thanked.

Secondary:

- **[Extension host](../../../.claude/personas/users/extension-host.md)**:
  an extension funded by its host or a supporter that uses GoatConf's name
  appears on the ledger like any other line.
- **[Speaker](../../../.claude/personas/users/speaker.md)**: sees plainly
  that travel is theirs, and whether a supporter-funded grant exists.
- **[Volunteer](../../../.claude/personas/users/volunteer.md)**: knows
  their lunch is paid only if a supporter funds it, never from the
  organiser's money.

## Now / Perceived / Target

- **Now (2026-10-07):** no line spent, no supporter, no ledger. The pitch
  holds a first base and menu, as allocations and estimates rather than
  quotes. IPI Academy provides the hall and rooms; the terms are (unknown,
  needs source).
- **Perceived:** a conference budget is usually read as money an organiser
  holds and spends (the guide's "a clean entity for sponsors to pay",
  § Legal structure and insurance). At GoatConf nobody holds money, so the
  risk is supporters, suppliers or attendees expecting an invoice or a
  refund from GoatConf that cannot exist.
- **Target:** the budget page live with the site; every line added when it
  happens; the menu showing funded and unfunded items; the organiser's
  fallback at 0 EUR or every euro of it on the ledger; a final account
  published within two weeks of the event, as the guide advises (§ Settle
  the finances).

## Scope

The base is what the core needs and somebody has to cover, first by a
supporter or in kind, and only then by the organiser's fallback. Items that
cost nothing are recorded too: the hall and rooms in kind from IPI Academy,
registration on a free tier (pretix hosted gives 500 free tickets a year,
`sources/web/tooling/pretix-hosted-pricing.md`), a CFP on a simple free
form (`sources/web/tooling/tally-pricing.md`), and the site under
muhamed.at with no domain to buy
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`,
question 5). The pitch's fallback allocations are carried as ceilings, not
prices: printing (badges, signs, the code-of-conduct poster) 250 EUR, small
supplies 50 EUR, tools 50 EUR, a reserve of 500 EUR for emergencies (guide,
§ Emergencies), and food and drink at 0 EUR, always. That is 850 EUR
allocated, 1,000 EUR at most, and 0 EUR if everything is covered. An
unspent reserve stays unspent; it is never collected or carried as money by
GoatConf.

The menu lists the stretch goals a supporter can fund, each with what it
buys, its supplier and an estimate from cited Tuzla prices at 1.95583 KM to
the euro (`sources/web/tuzla/cbbh-exchange-rate-2026-10-07.md`):

- a round of lunch, about 552 EUR for about 120 people at 9 KM a meal
  (`sources/web/tuzla/numbeo-cost-of-living-tuzla.md`), optional because
  breaks are in town and people pay their own
  (`sources/conversations/2026-10-07--org--space-to-hang-out.md`);
- volunteers' lunch, about 92 EUR for about 20 meals (same source);
- a round of coffee, about 199 EUR for about 120 cappuccinos at 3.25 KM
  (same source);
- a speaker grant pool, about 1,000 EUR for ten speakers at the 100 EUR the
  organiser once floated ([CFP and speakers](cfp-and-speakers.md));
- a speaker dinner, about 120 to 190 EUR for twelve
  (`sources/web/tuzla/easybalkan-bosnia-costs-2026.md`);
- the salt lake for everyone, about 552 EUR for the core day's cap of
  about 120 weekend tickets at 9 KM (`sources/web/tuzla/slana-jezera-cijene-kurir-2026-08.md`);
- video, volunteer-run with free OBS (`sources/web/tooling/obs-project.md`)
  at an equipment cost that is (unknown, needs source), or a hired crew at
  about 1,500 to 4,000 USD a day at US rates
  (`sources/web/tooling/videographer-rates-2026-ruah.md`);
- the after-party, shirts and lanyards, priced when a supporter asks.

For scale, Balkan Ruby's entry tier is 500 EUR and its Food and Coffee items
1,500 EUR each (`sources/web/funding/balkanruby-sponsorship.md`), and
EuRuKo 2024 took "Anonymous support" from 500 EUR
(`sources/web/funding/euruko-2024-sponsoring.md`).

The ledger is one list, kept in this repository as the source of the budget
page. Each line says what the item is, who covered it (the organiser, a
named supporter, "an anonymous supporter", or in kind from whom), the
amount or an in-kind estimate, the supplier, the date, and whether the
supplier's receipt is in hand. Lines are added as things happen, not at the
end. With no money to receive, GoatConf 2027 needs no company, association
or bank account.

## No-gos

- No money from anyone to the organiser or to GoatConf, ever; supporters
  pay suppliers or give in kind.
- No food or drink paid from the organiser's money, for anyone.
- No spending of the organiser's money beyond 1,000 EUR, and none while a
  supporter or in-kind route is still open.
- No spending, of anyone's money, that is not on the public ledger.
- No stretch goal announced before its line is on the ledger.
- No receipts, invoices, bank details or private addresses in this
  repository, which will be public; the ledger records that a receipt is
  in hand, not the receipt.
- No legal entity, bank account or fund for GoatConf 2027.

## Rabbit holes

- **Allocations read as prices.** The 250 EUR printing line could be far
  off; replace each allocation with a Tuzla quote before relying on it.
- **Suppliers who cannot invoice a foreign company,** or supporters who
  cannot pay a small local supplier. Whether a Tuzla café or printer can
  invoice an Austrian or German company is (unknown, needs source). Fall
  back to in kind; do not invent an intermediary that holds money.
- **A supporter offering cash** "to make it simple". The answer is always
  the supplier's invoice or in kind.
- **Accounting software.** One plain list is enough for a few dozen lines;
  stop if the ledger starts to need categories, currencies and reports.

## Appetite

**Small:** one page and one list, set up in an evening and kept current
from November 2026 to June 2027 by the organiser, a few minutes per line,
then the final account within two weeks of the event.

## Success metrics

- **The budget page is live with the site and its first line is dated
  before the first public stretch-goal announcement.** Observed by comparing
  the ledger's earliest line date with the date of the first supporter beat
  in the social calendar.
- **The organiser's fallback spent: 0 EUR, or every euro of it on the
  ledger.** Observed as the sum of ledger lines whose payer is the
  organiser, in the final account.
- **No food or drink line paid by the organiser.** Observed by filtering the
  ledger's lines by item and payer; the count must be zero.
- **The final account is published within two weeks of the event.**
  Observed as the publication date of the final account on the budget page
  against the event's last day.

## Dependencies

- [Website and registration](website-and-registration.md): the budget page
  lives on muhamed.at/goatconf and is copied over with the rest.
- [Supporters and hiring](supporters-and-hiring.md): the menu is what
  supporters fund; a funded item becomes a ledger line.
- [CFP and speakers](cfp-and-speakers.md): the speaker grant pool and
  speaker dinner.
- [Activities: the lake and the town](activities-lake-and-town.md): the
  lake tickets and activity costs.
- [Operations and the day](operations-and-the-day.md): printing, supplies
  and what IPI provides in kind.
- [Dates and the core day](dates-and-the-core-day.md): head counts that
  turn estimates into amounts.
- [Extension slots and the record](extension-slots-and-the-record.md):
  extensions that use GoatConf's name report their costs to the ledger.

## Decisions already made by the organiser

- **No money passes through the organiser; sponsors give the organiser no
  money.** `sources/conversations/2026-10-07--org--no-money-through-me.md`.
- **The budget is public.**
  `sources/conversations/2026-10-07--org--no-money-through-me.md`.
- **The ledger is a budget page on muhamed.at/goatconf, written here and
  copied over.**
  `sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`
  (question 2).
- **The organiser's own money is at most 1,000 EUR.**
  `sources/conversations/2026-10-07--org--first-answers.md` (question 8).
- **That money is a fallback only.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`
  (question 1).
- **The organiser pays for no food or drink, for anyone.**
  `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **Free to attend; speakers pay their own travel.**
  `sources/conversations/2026-10-07--org--conference-vision.md`.
- **This repository will be public.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.

The 500 EUR reserve, lunch and coffee as stretch goals rather than base,
and a ledger public from the first line are choices made in auto mode in
the pitch; this PRD carries them for the organiser to approve or change.

## Open questions

- What does IPI Academy provide in kind: rooms only, or also AV, Wi-Fi,
  cleaning and staff time?
- Is the 1,000 EUR firm, or could a second personal contribution fill a
  stretch goal that falls short (never one for food or drink)?
- How is an in-kind gift valued on the ledger: the giver's estimate, a
  market price, or no amount?
- Does an extension that uses GoatConf's name but is funded entirely by its
  host appear on the ledger, or only extensions a supporter funds through
  the menu?

## Decision needed

**The ledger's shape:** where its source lives in this repository (one file
the budget page is rendered from, or the page itself), the fields every line
carries, how in-kind gifts and anonymous supporters are recorded, and how a
receipt is noted as in hand without its contents entering the public
repository. The ADR records that shape and the rule for when a menu item
counts as funded.

**Answered by the ADR** [Keep the public ledger as one CSV file here, rendered as the budget page](../adrs/budget-and-public-ledger.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** The ledger is published on goatconf.com. There are two core days, Thursday 3 and Friday 4 June 2027. See [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md), [Dates: two core days](../adrs/two-core-days-first-week.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
