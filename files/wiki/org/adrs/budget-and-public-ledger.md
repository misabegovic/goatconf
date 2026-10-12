---
title: "Keep the public ledger as one CSV file here, rendered as the budget page"
kind: decision
status: accepted
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/budget-and-public-ledger.md
sources:
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
---

# Keep the public ledger as one CSV file here, rendered as the budget page

Answers the "Decision needed" of
[Budget and the public ledger](../prds/budget-and-public-ledger.md).
Accepted 2026-10-07 from the organiser's answer
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 10), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

The ledger is one CSV file in this repository, `ledger.csv` in the
`site/` folder beside the pages. It is the only source of truth for
GoatConf's money: every line is added by a commit, so its history is
public and auditable. The budget page at muhamed.at/goatconf shows it as
a table, built from the file before each copy.

## Why

The organiser asked for a public budget ("We also need to be transparent
about the budget", `sources/conversations/2026-10-07--org--no-money-through-me.md`)
shown on the site (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`),
and picked a CSV file here over a hand-edited table or a public Google
Sheet. A file in git shows not just the current numbers but every change
to them, with a date and a reason, which a sheet's own history does not
show the public. A CSV opens in any spreadsheet tool for anyone who
wants to check the sums.

## How

Each line carries the date; the item; whether it is base or a menu item;
who covered it (the organiser, a named supporter, "an anonymous
supporter", or in kind from whom); the supplier; the amount in euros, or
an in-kind estimate marked as such; whether the supplier's receipt is in
hand, as yes or no; and a short note. Receipts themselves never enter
this public repository; the organiser keeps them, and the line only says
whether one exists.

An item on the menu counts as funded only when its line is in the ledger
with a supplier named and the supporter's commitment in writing; until
then the site shows it as open. Nothing is announced as funded before
that, after the guide's rule that a stretch goal is announced when the
money is there (`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Base budget and stretch goals). The organiser's own fallback appears in
the same file, line by line, only when it is spent
(`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
A final account, the file as it stands plus a two-line summary, is
published within two weeks of the core day.

## Alternatives

- **A CSV file here** *(chosen)*: public history of every change, and
  readable by people and tools.
- **A Markdown table on a wiki page:** readable, but awkward to sum and
  easy to break by hand.
- **A public Google Sheet:** easy to edit, with its history held by
  Google and not shown to the public.

## Consequences

- **Opens:** anyone can audit GoatConf's money from the repository alone.
- **Costs:** a ledger line is a commit, so whoever keeps it needs git or
  an agent's help.
- **Costs:** a supporter's name in the ledger is public the moment it is
  committed; the supporter agrees to it, or is listed as anonymous.

## Linked PRD

[Budget and the public ledger](../prds/budget-and-public-ledger.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-12.** The public ledger is published on goatconf.com, not muhamed.at/goatconf. See [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
