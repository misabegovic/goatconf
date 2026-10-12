---
title: "Write each extension as one Markdown file with frontmatter, checked by an agent and merged by the organiser"
kind: decision
status: accepted
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/extension-slots-and-the-record.md
sources:
  - sources/conversations/2026-10-12--org--accepted-events-and-hackathons.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/web/models/fosdem-2026-fringe.md
  - sources/web/models/edfringe-the-fringe-story.md
  - sources/web/funding/fosdem-charter.md
  - sources/web/tooling/google-forms-response-destination.md
---

# Write each extension as one Markdown file with frontmatter, checked by an agent and merged by the organiser

Answers the "Decision needed" of
[Extension slots and the record](../prds/extension-slots-and-the-record.md).
Accepted 2026-10-07 from the organiser's answers
(`sources/conversations/2026-10-07--org--adr-answers.md`, questions 2 and
3), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

Every extension (a fringe event, workshop, hub, activity, venue, support
item or hiring slot) is one Markdown file with frontmatter, kept in an
`extensions/` folder at the root of this repository, one file per
extension, named after it in kebab-case. The frontmatter carries the
record; the body is a short description in the host's words. The
website's extension list is built from these files before each copy into
muhamed.at/goatconf.

## Why

The organiser picked Markdown with frontmatter over plain text or a data
file. It is the one format that both people and the list builder read
first: a host sees a readable page, the builder reads fields, and a pull
request diff shows exactly what a host asked for. It is also the shape
every page in this brain already has, so the same agent and the same
checks read it.

The record itself is FOSDEM's fringe row, where each independent event
carries the event, location, start, end, cost, registration and contact
(`sources/web/models/fosdem-2026-fringe.md`), with GoatConf's two
additions from the PRD.

## How

The frontmatter fields, in this order, are: the name; the kind of slot
(one of the seven); the host, a person or group; the location; the start
and the end; the cost to attend, or "free"; how to register, or "no
registration"; who pays for it, which for a support item names the
supplier the supporter pays (no money passes through the organiser,
`sources/conversations/2026-10-07--org--no-money-through-me.md`); a
public contact the host chooses; and the host's acceptance of the charter
and the code of conduct, which must be yes.

A host who uses git opens a pull request adding the file. A host who
does not fills in the extension Google Form, whose questions are those
same fields in the same order; the extensions volunteer turns each
response into the file and opens the pull request. The form's responses
are deleted once the file exists, so nothing private outlives the
public listing.

An agent reads each extension pull request and comments one summary:
whether every field is present, whether the kind is one of the seven,
whether the dates fall in the GoatConf week or say why not, whether the
acceptance is yes, and whether anything in the description reads as
"GoatConf presents" or as content for sale against the charter
(`sources/web/funding/fosdem-charter.md`). It never judges taste, the way
the Edinburgh Fringe Society chose "to take no part in vetting the
festival's programme" (`sources/web/models/edfringe-the-fringe-story.md`).
The organiser merges (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

## Alternatives

- **Markdown with frontmatter** *(chosen)*: readable by people and by the
  builder, and the brain's own page shape.
- **Plain text, people first:** friendlier to write, but the list builder
  would have to guess fields.
- **A structured data file (YAML or JSON), builder first:** strict, and
  hostile to a host who writes a paragraph.
- **A spreadsheet of extensions:** easy to fill in, with no diff, no
  review and no public history.

## Consequences

- **Opens:** a public, reviewable history of every extension, and one
  list builder for the site.
- **Opens:** the agent's check can grow into a test in the local CI once
  the first records exist.
- **Costs:** a volunteer's time for every host who uses the form.
- **Costs:** the contact on a record is public; the form says so before a
  host submits.

## Linked PRD

[Extension slots and the record](../prds/extension-slots-and-the-record.md).

## Build notes

**2026-10-10.** Built as decided. Records live in `extensions/` with a
`README.md` and a `_template.md`; neither counts as a record. The
frontmatter keys are `name`, `kind`, `host`, `location`, `start`, `end`,
`cost`, `registration`, `paid_by`, `contact` and `accepts`, plus `supplier`
for support and `outside_week_reason` for dates outside the GoatConf week
(taken as 25 May to 20 June 2027 until IPI confirms the days).
`tools/extensions.py check` is the agent's check and prints the summary it
posts on a pull request; `tools/extensions.py build` writes
`site/extensions.html` from the records that pass. The local CI runs both, so
a failing record or a stale page stops the push, which is the growth into CI
this ADR anticipated. The charter is `site/charter.html`.

## Amendments

- **2026-10-12.** The extension Google Form and the published list move to goatconf.com, and the organiser judges every listing before its record is merged. The record format and the build are unchanged. See [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md), [The call: the organiser judges](call-organiser-judges.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. The listing window stays 25 May to 20 June 2027, around the confirmed days, for arrivals and trips (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-12, only accepted events are part of GoatConf.** Not everything people propose becomes part of the conference (source: sources/conversations/2026-10-12--org--accepted-events-and-hackathons.md). The organiser accepts an event only if it follows the code of conduct and the charter and fits the program (its time, its place, who it is for, how it sits next to the talks), and may decline or ask for changes for any of those reasons. A record carries `accepted: yes`, set by the organiser only; until then it is not listed. Accepted events are official GoatConf events, shared with attendees and named "<name>, part of GoatConf 2027", run and paid for by their host directly; "GoatConf presents" stays refused, because the organiser does not run them. Events not accepted are not listed and may not use GoatConf's name. Hackathons are a kind of their own: people and companies who suggest one organise all of it, the room, theme, judging, prizes and costs, paid directly to suppliers, and may not collect attendees' data or recruit beyond what people opt into. The proposal page and every link to it are called "Propose an event" instead of "Add something". This replaces the earlier rules that listings are checked only against the charter and the code of conduct and "never for taste", and that each says it is run independently.
