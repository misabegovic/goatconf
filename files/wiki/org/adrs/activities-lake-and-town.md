---
title: "The organiser runs the goat hunt; the core publishes prices, the breaks list and the lake day"
kind: decision
status: accepted
updated: 2026-10-13
confidence: medium
depends_on:
  - org/prds/activities-lake-and-town.md
sources:
  - sources/conversations/2026-10-13--org--lakes-planned-and-every-evening.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/web/funding/euruko-2024-why-the-goat.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/models/bansko-nomad-fest-life-in-bansko.md
  - sources/web/tuzla/tuzla-wikipedia.md
---

# The organiser runs the goat hunt; the core publishes prices, the breaks list and the lake day

Answers the "Decision needed" of
[Activities: the salt lake, a goat hunt, and a cheap city](../prds/activities-lake-and-town.md).
Accepted 2026-10-07 from the organiser's answer
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 11), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

The town-wide goat hunt is part of the core and the organiser runs it,
on the day before or after the core day, never on it. Its clues tell the
goat story and end at the goat statue
(`sources/web/funding/euruko-2024-why-the-goat.md`). Beside it, the core
publishes a prices page with a "last checked" date, a short list of
cafés and places to eat around Freedom Square for the long breaks, the
lake day with its rain plan, and an activities page that links every
activity extension.

## Why

The organiser chose to run the hunt rather than hand it to a host or
skip it. It is the organiser's signature: the guide cites their
"city-wide treasure hunt throughout Vienna during RubyConf Austria"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Beyond the talks), and the story it tells is the conference's name.
Keeping it off the core day keeps the organiser free for the hall on the
day that needs them most.

## How

The organiser writes the clues in spring and walks the route on a visit
to Tuzla before the event. Teams form at the start from whoever turns
up, mixing strangers. It costs nothing to join; anything a team buys on
the way, it pays for itself. If the organiser is needed elsewhere on the
day, the written clues and the route let a volunteer run it instead.

The prices page lists food, coffee, the lake ticket and the tourist
train with the date each was checked, after Bansko Nomad Fest's cost
table (`sources/web/models/bansko-nomad-fest-life-in-bansko.md`). The
breaks list names a few places on and around the square, each person
paying their own (`sources/conversations/2026-10-07--org--space-to-hang-out.md`).
The lake day's rain plan is the park cafés and an indoor fringe event,
since June is Tuzla's wettest month (`sources/web/tuzla/tuzla-wikipedia.md`).

## Alternatives

- **The organiser runs it** *(chosen)*: the organiser's signature,
  unchanged.
- **Hand it to a host with the clues:** fits the PRD's rule that the day
  should not need the organiser; the organiser preferred to run it.
- **Skip it in 2027:** less work, and the one activity that ties the name
  to the place goes missing.

## Consequences

- **Opens:** the goat story told in the town itself, by the person who
  knows it best.
- **Costs:** one more thing on the organiser, who runs the event from
  Vienna without a co-organiser; the written clues are the fallback.
- **Costs:** the core now holds one activity of its own, so the rule
  that the core never depends on an extension is unaffected, but the
  core's own load grows.

## Linked PRD

[Activities: the salt lake, a goat hunt, and a cheap city](../prds/activities-lake-and-town.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-13, the lake day is planned by the organiser, and the lakes fit every evening.** The organiser plans Saturday's lake day; nobody else needs to own it, so the program stamps it "Planned", as it does the goat hunt. Many people go to the lakes around 17:00 or 18:00, so the lakes are also an activity after the talks on both core days (source: sources/conversations/2026-10-13--org--lakes-planned-and-every-evening.md).
- **2026-10-12.** The day after the talks is Saturday 5 June 2027, the community day. See [Dates: two core days](two-core-days-first-week.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
