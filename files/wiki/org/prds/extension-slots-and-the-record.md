---
title: "Extension slots and the record: how anyone adds to GoatConf"
kind: initiative
status: living
updated: 2026-10-13
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/one-goat-minimal-core-and-extensions.md
sources:
  - sources/conversations/2026-10-13--org--evening-event-karaoke-hackathon.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/web/models/fosdem-2026-fringe.md
  - sources/web/models/edfringe-the-fringe-story.md
  - sources/web/models/devcon-8-community-hubs-rfp.md
  - sources/web/models/tedx-rules.md
  - sources/web/models/london-tech-week-fringe-tiers-search-summary.md
  - sources/web/funding/fosdem-charter.md
  - sources/web/hiring/strangeloop-privacy-policy.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
---

# Extension slots and the record: how anyone adds to GoatConf

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md).
It graduates the extension half of the umbrella pitch
[One goat feeds the town](../pitches/one-goat-minimal-core-and-extensions.md),
bet on by the organiser on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`). The
list of what the core guarantees lives in the epic; this PRD covers the
mechanism others use to add to it, and the one-page charter that binds
every addition.

## Objective

**Anyone who wants to add something to GoatConf 2027 can do it with one
short record, by pull request or by form, and see it listed on the
website after an agent's check and the organiser's merge, under one
page of rules that never change per extension.**

## Background

The organiser asked for an event that is "minimalistic and
extendable... Like the Pi agent. I will provide the minimum needed for a
conference and folks can extend", and named expo and booths as "maybe
the extensible part" and hiring as a way companies could help
(`sources/conversations/2026-10-07--org--conference-vision.md`). The
first answers put the framework second to the event: "Both, event
first", with slot rules written so others can reuse them later
(`sources/conversations/2026-10-07--org--first-answers.md`, question 1).

The organiser runs GoatConf from Vienna with no co-organiser, so an
extension negotiated one by one makes the organiser the bottleneck. The
RubyEvents guide's advice is that "by the time the day comes, as much as
possible should already be someone else's problem"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Before you arrive). A single shared record and fixed rules let hosts
add to the event without a negotiation each.

The organiser has since decided how submissions arrive and who lands
them: hosts who use git open a pull request to this repository, which is
to become public; others use the same form tool as the call for talks;
an agent checks each pull request against the record and the charter and
comments a summary; the organiser merges
(`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

## Affected personas

- [Extension host](../../../.claude/personas/users/extension-host.md).
  Today there is nothing to extend and no terms to read. With this
  shipped, a host reads one charter, fills in one record, and finds the
  addition on the website's calendar with their own contact on it,
  without asking the organiser for anything.
- [Attendee](../../../.claude/personas/users/attendee.md). Finds every
  fringe event, workshop, hub and activity in one list, each marked as
  independently organised, with its cost and how to register.
- [Hiring partner](../../../.claude/personas/users/hiring-partner.md).
  Has a named way in (the hiring slot) on terms that protect attendees'
  data.
- [Volunteer](../../../.claude/personas/users/volunteer.md). Turns form
  submissions into record files, using the one form tool they already
  learn for the call for talks.

## Now / Perceived / Target

- **Now (2026-10-07):** no extension exists, no record format is written
  down, no charter is published, and this repository is private
  (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).
  The mechanism exists only as the umbrella pitch.
- **Perceived:** that hosts will come once the slots are announced. No
  host has been asked, so this is a belief (unverified, 2026-10-07).
  Another belief worth checking is that "listed, not curated" is enough
  distance between GoatConf and an extension's risks in Tuzla; whether it
  is locally is (unknown, needs source).
- **Target:** a published charter page; a record format every extension
  uses; pull requests and form submissions arriving at one place; an
  agent's summary comment on each pull request; the organiser merging;
  and the website's extension list built from the record files.

## Scope

**The seven kinds of slot.** Every extension is one of these:

- **Fringe event:** a meetup, dinner, party, hackathon or talk series
  outside the main room, run and paid for by its host, as on FOSDEM's
  fringe list (`sources/web/models/fosdem-2026-fringe.md`).
- **Workshop:** a hands-on session in a room the host brings, or in one
  of IPI's other rooms if one is free; the organiser reports "several"
  (`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
- **Hub:** a corner in the venue run by a community, on Devcon's terms:
  community-driven, "free of marketing and branding", staffed by its
  hosts (`sources/web/models/devcon-8-community-hubs-rfp.md`).
- **Activity:** the salt lake, a city walk, a treasure hunt, a day trip
  (guide, § Beyond the talks).
- **Venue:** another space in Tuzla that hosts part of the event.
- **Support:** a supporter pays a supplier directly, or gives in kind,
  for a named item, and is thanked for it. No money passes through the
  organiser
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- **Hiring:** a job-board entry, a job corner or office hours, with
  attendees opting in and their data never sold or shared, as in Strange
  Loop's policy (`sources/web/hiring/strangeloop-privacy-policy.md`).

**The shared record.** Every slot uses the same short record, adapted
from FOSDEM's fringe list, where each independent event is one row
carrying the event, location, start, end, cost, registration and contact
(`sources/web/models/fosdem-2026-fringe.md`). GoatConf adds two fields:
the kind of slot, and who pays for it. An extension is one short plain
text file holding that record, kept in this repository.

**The four rules.**

1. **The core never depends on an extension.** If a host, supporter or
   venue falls through, nothing in the core changes.
2. **Listed, not curated.** A submission is checked only against the
   charter and the code of conduct, never for taste, the way the
   Edinburgh Fringe Society chose "to take no part in vetting the
   festival's programme" (`sources/web/models/edfringe-the-fringe-story.md`).
   The list says, as FOSDEM's does, that these events are organised
   independently.
3. **Honest names.** An extension is "<name>, a GoatConf fringe event",
   never "GoatConf presents" (`sources/web/models/tedx-rules.md` is the
   strict end of this rule).
4. **The host carries its own costs and risks.** GoatConf lends its
   audience and its calendar, not money.

**How an extension arrives and lands.** A host who uses git opens a pull
request adding the record file. A host who does not fills in the form
in the same form tool as the call for talks (Tally or Google Forms), and
a volunteer turns the submission into the file. An agent checks each
extension pull request against the record and the charter and comments a
summary; the organiser merges
(`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

**The one-page charter.** One public page says what GoatConf is and what
it will not do, taken from FOSDEM's charter: attending is free; nobody
has to hand over personal data the event does not need ("unless law or
safety mandate it"); supporters do not buy program content; content and
money are kept apart (`sources/web/funding/fosdem-charter.md`). Two
lines are GoatConf's own, from the organiser: no money passes through
the organiser, and the budget is public
(`sources/conversations/2026-10-07--org--no-money-through-me.md`). The
charter also states the four rules above, so a host reads one page.

## No-gos

- No vetting for taste, quality or fit; only the charter and the code of
  conduct.
- No organiser money spent on any extension, and none on food or drink
  for anyone
  (`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
- No money from a supporter or host paid to the organiser.
- No listing fee in 2027, for communities or for companies.
- No attendee data handed to a host or hiring partner without the
  attendee's explicit choice.
- No separate extensions repository; extensions live in this one.
- No second form tool for extensions.
- No app, account or login for hosts.
- No reusable kit extracted before the 2027 event.

## Rabbit holes

- **Vetting creep.** Once listings exist there will be pressure to judge
  them. Anything beyond the charter and the code of conduct needs its own
  decision; stop and re-pitch.
- **A fringe bigger than the conference.** Company events can crowd out
  community ones. London Tech Week lists not-for-profits free and
  charges businesses
  (`sources/web/models/london-tech-week-fringe-tiers-search-summary.md`,
  a search summary only); that split is for a later edition.
- **Growing the record.** Every field added is a field a form-filling
  host has to answer. If the record needs more than one or two more
  fields, stop and re-pitch.
- **An agent that decides.** The agent's job is a summary comment. If it
  starts approving, rejecting or editing submissions, it has crossed into
  the organiser's merge.
- **Liability.** An activity at the lake carries GoatConf's name in the
  attendee's eyes. Whether honest names and the independence line are
  enough locally is (unknown, needs source); that question belongs to
  operations, not to this mechanism.
- **Rooms at IPI for workshops and hubs.** How many of IPI's rooms are
  free on which days waits on IPI's answer to the date options.

## Appetite

**Small.** The umbrella pitch set a big appetite for the exploration and
a small one per area once bet on. What is left is a record format, a
charter page, a form shared with the call for talks, and an agent check
on pull requests: an evening or two each, from one organiser part-time.
If any part needs more, it is cut back to what a host strictly needs.

## Success metrics

- **At least five extensions listed** by the week before the event, none
  run by the organiser. Observed as a count of extension record files in
  this repository on that date.
- **Every extension pull request carries the agent's summary comment
  before it is merged.** Observed from the merged pull requests touching
  extension records on the repository host, counted at the event.
- **No extension listing breaks the honest-name rule.** Observed by
  reading each record's name against "a GoatConf fringe event" at the
  final count.
- **The charter page is published before the first extension is listed.**
  Observed from the publish date of the charter page on
  muhamed.at/goatconf against the date of the first merged record.

## Dependencies

- [Website and registration](website-and-registration.md): the
  extension list is built from the record files and copied with the rest
  of the site; the charter is one of its pages.
- [CFP and speakers](cfp-and-speakers.md): the form tool is shared.
- [Supporters and hiring](supporters-and-hiring.md): the support and
  hiring slots use this record.
- [Budget and the public ledger](budget-and-public-ledger.md): a support
  extension's item appears on the ledger.
- [Activities: the lake and the town](activities-lake-and-town.md): the
  activity slot.
- [Operations and the day](operations-and-the-day.md): the code of
  conduct every extension inherits.
- [Dates and the core day](dates-and-the-core-day.md): the days around
  the core day are where extensions run.

## Decisions already made by the organiser

- **Extensions arrive by form or pull request.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.
- **Pull requests go to this repository, which will be public;** there
  is no separate extensions repository. Same source.
- **The form is the same tool as the call for talks** (Tally or Google
  Forms). Same source; the call's tool is a simple form,
  `sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`.
- **An agent checks each extension against the record and charter and
  comments a summary; the organiser merges.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.
- **No money passes through the organiser, and the budget is public.**
  `sources/conversations/2026-10-07--org--no-money-through-me.md`.
- **The organiser's own money is a fallback only, and never pays for food
  or drink.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`,
  `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **Event first, framework second.**
  `sources/conversations/2026-10-07--org--first-answers.md`, question 1.

## Open questions

- Should a commercial expo exist at all, or only hubs and sponsor-funded
  support? The organiser named expo and booths as "maybe the extensible
  part"; the pitch left it open.
- When does the repository become public, so hosts can open pull
  requests? Until then, the form is the only route.
- Who among the volunteers turns form submissions into files.
- Is there a deadline for extensions to be listed before the event?
  (unknown, needs source)

## Decision needed

The ADR records the extension record's exact fields and their order
(FOSDEM's seven plus kind of slot and who pays), where the record files
live in this repository, how the form's questions map onto those fields,
and what the agent's check compares and says in its summary comment. The
one real choice in it is the file format of a record: plain text read by
people first, or a structured format read by the site's list builder
first.

**Answered by the ADR** [Write each extension as one Markdown file with frontmatter, checked by an agent and merged by the organiser](../adrs/extension-slots-and-the-record.md), accepted 2026-10-07.

## Amendments

- **2026-10-13, the kinds renamed.** The list of events to propose is now Evening event, Community trip, Meetup, Live podcast, Hike, Hackathon, Karaoke and Something else, replacing Fringe event, Workshop, Community hub, Activity, Another venue, Support and Hiring; support is handled on the supporters page (source: sources/conversations/2026-10-13--org--evening-event-karaoke-hackathon.md).
- **2026-10-12.** Additions arrive through the add-something Google Form on goatconf.com, and the extension list is published there rather than on muhamed.at/goatconf. The organiser judges every listing. Events run independently by their hosts on the days around the core days, or on Saturday 5 June, are listed as GoatConf fringe events; sessions in the core days' rooms and slots are part of the program. See [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md), [The call: the organiser judges](../adrs/call-organiser-judges.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
