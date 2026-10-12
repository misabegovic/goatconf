---
title: "One goat feeds the town: GoatConf's minimal core and its extension points"
kind: pitch
status: superseded
updated: 2026-10-07
appetite: big
confidence: low
sources:
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--organiser.md
  - sources/conversations/2026-10-07--org--venue-ipi.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/funding/euruko-2024-why-the-goat.md
  - sources/web/models/fosdem-2026-fringe.md
  - sources/web/models/edfringe-the-fringe-story.md
  - sources/web/models/devcon-8-community-hubs-rfp.md
  - sources/web/models/tedx-rules.md
  - sources/web/models/london-tech-week-fringe-tiers-search-summary.md
  - sources/web/funding/fosdem-charter.md
  - sources/web/hiring/strangeloop-privacy-policy.md
  - https://github.com/misabegovic/claude-brain/blob/main/wiki/pi/permanent/purpose.md
superseded_by: org/epics/goatconf-2027.md
---

# One goat feeds the town: GoatConf's minimal core and its extension points


> **Bet on and graduated, 2026-10-07.** The organiser bet on this pitch; it continues as [goatconf-2027.md](../epics/goatconf-2027.md). This page is kept as the pre-bet record.

The umbrella pitch for GoatConf 2027. Pre-bet: nothing here is decided.
Shaped in auto mode on 2026-10-07; the choices the agent made, and why,
are listed under [Choices made in auto mode](#choices-made-in-auto-mode).
The area pitches hang under it; see the [pitches hub](index.md).

## Problem

The organiser wants a free conference for 120 to 300 people in Tuzla in
the first or second week of June 2027, with at most 1,000 EUR of their
own money, speakers paying their own travel, and the organiser living in
Vienna (`sources/conversations/2026-10-07--org--conference-vision.md`,
`2026-10-07--org--first-answers.md`, [the organiser](../organiser.md)).
They also want it "minimalistic and extendable... Like the Pi agent":
"I will provide the minimum needed for a conference and folks can
extend."

Three things make that hard.

First, the money. A conventional regional conference covers its base
budget (venue, basic audio and video, a ticketing platform, a speaker
honorarium) from ticket sales, and treats everything else as stretch
goals (`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Base budget and stretch goals). GoatConf sells no tickets. Its base has
to fit inside 1,000 EUR plus what IPI Academy gives in kind, and every
stretch goal has to be paid for by someone else.

Second, the organiser's time. Expo, booths, hiring, extra venues and
activities are all things the organiser said others could bring. If each
of them is negotiated one by one, from Vienna, the organiser becomes the
bottleneck the minimal core was meant to avoid. The guide's advice is
that "by the time the day comes, as much as possible should already be
someone else's problem" (same source, § Before you arrive).

Third, the calendar. The guide says a first conference needs about a
year and that "six months is doable but stressful"; from 2026-10-07 to
early June 2027 is about eight months. Sponsor budgets are often set "by
the previous November for the following year" (same source, § Give
yourself a year, § Lower your expectations). Whatever the core is, it has
to be small enough to stand up in that time.

The name already carries the answer. EuRuKo 2024, which the organiser
founded and organised, was pitched as a "G.O.A.T." edition after Tuzla's
goat: when Austria-Hungary ordered goats gone, one man hid his, "that
one goat ended up feeding the entire community", and everyone in Bosnia
and Herzegovina knows the saying "The whole of Tuzla milked one goat"
(`sources/web/funding/euruko-2024-why-the-goat.md`). GoatConf is that
idea taken home to Tuzla: one small thing the organiser provides, which
everyone else can draw on and add to.

## Appetite

**Big, as an exploration; small per area once bet on.** This pitch sets
the frame every area pitch works inside, so the time to get it right is
worth spending now. The core it describes has to be buildable by one
organiser, part-time, from Vienna, with volunteers, between November 2026
and June 2027, and its base budget has to fit 1,000 EUR. If a part of the
core cannot meet that, it moves out of the core and becomes an
extension.

## Solution

Three parts: the goat (the core the organiser guarantees), the milking
(the extension points anyone can use), and the kit (what others can reuse
after 2027). The shape follows Pi, which its makers describe as "a
minimal, extensible agent harness that you can make your own": a small
core and extensions that add the rest (claude-brain's reading of Pi,
linked in sources).

### The goat: the core

The core is everything GoatConf promises, and nothing else. If it is not
on this list, the organiser does not provide it.

- **A date and a room.** One week in June 2027 and the main hall at
  [IPI Academy](../ipi-academy.md), agreed in writing before anything is
  announced (guide, § Before You Commit).
- **One program.** A single track of talks chosen through an open call
  for proposals, so everyone shares the same frame of reference (guide,
  § Single track). Workshops run in a second room if IPI has one.
- **Free registration with a cap** matched to the room, collecting only
  what the event needs.
- **A website** that says when, where, who it is for and why come, and
  carries the schedule, travel basics, accessibility facts, the code of
  conduct and the list of extensions (guide, § Your website).
- **A code of conduct**, a named person to report to, and ten minutes at
  the start of the day explaining it (guide, § Code of conduct).
- **Long breaks in town** instead of catering: coffee and lunch on the
  Freedom Square, under five minutes from IPI, one to two hours each, with IPI used only for
  lectures (`sources/conversations/2026-10-07--org--space-to-hang-out.md`;
  guide, § Lunch, § Expensive mistakes). Few talks, much time to hang
  out; Tuzla being inexpensive is the point.
- **A one-page charter** that says what GoatConf is and what it will not
  do, taken from FOSDEM's: attending is free; nobody has to hand over
  personal data the event does not need; sponsors do not buy program
  content; content and money are kept apart
  (`sources/web/funding/fosdem-charter.md`). Two lines are GoatConf's
  own, from the organiser: **no money passes through the organiser**,
  and **the budget is public**
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).

The length of the event (one day, two, or two plus an activity day) is
left to the format pitch; the core works for any of them.

### The milking: extension points

Anyone can add to GoatConf through one of a few kinds of slot. Every slot
uses **the same small record**, adapted from FOSDEM's fringe list, where
each independent event is one row: event, location, starts, ends, cost,
registration, contact (`sources/web/models/fosdem-2026-fringe.md`).
GoatConf adds two fields: the kind of slot, and who pays for it. That
record is the extension interface, the way a tool definition is Pi's.

The kinds of slot:

- **Fringe event:** a meetup, dinner, party, hackathon or talk series
  outside the main room, run and paid for by its host. FOSDEM lists
  dozens, from free to paid, including a company happy hour and a
  "HackerTrain" whose cost is "your own train ticket" (same source).
- **Workshop:** a hands-on session in a room the host brings, or in an
  IPI room if one is free.
- **Hub:** a corner inside the venue run by a community, on Devcon's
  terms: "driven by communities rather than a specific project or
  company", "free of marketing and branding", staffed by its hosts
  (`sources/web/models/devcon-8-community-hubs-rfp.md`).
- **Activity:** the salt lake, a city walk, a treasure hunt, a day trip.
  The guide calls these the best thing a conference can add, and names
  the organiser's own Vienna treasure hunt (guide, § Beyond the talks).
- **Venue:** another space in Tuzla that hosts part of the event.
- **Support:** a sponsor pays for a stretch goal and is thanked for it:
  coffee, video recording, a speaker contribution, a travel grant, an
  after-party. These are the guide's stretch goals, and its "beyond the
  logo" sponsors who want to *do* something (guide, § Beyond the logo).
- **Hiring:** a job-board entry, a job corner, office hours. Attendees opt
  in and their data is never sold or shared; Strange Loop's rule is
  "never share or sell", with badge scanning the attendee's choice
  (`sources/web/hiring/strangeloop-privacy-policy.md`).

Four rules hold every slot together:

1. **The core never depends on an extension.** If a fringe event, a
   sponsor or a venue falls through, nothing in the core changes. This
   is what keeps the organiser's promise small enough to keep.
2. **Listed, not curated.** GoatConf checks a submission only against
   the charter and the code of conduct, not for taste, the way the
   Edinburgh Fringe Society chose "to take no part in vetting the
   festival's programme" (`sources/web/models/edfringe-the-fringe-story.md`).
   Each listing names its own contact, and the list says, as FOSDEM's
   does, that these events are "organised independently" (FOSDEM fringe
   source).
3. **Honest names.** An extension is "<name>, a GoatConf fringe event",
   never "GoatConf presents". TEDx is the strict end of this ("never
   communicate 'TED is coming to (my city)'"); GoatConf needs only the
   one line (`sources/web/models/tedx-rules.md`).
4. **The host carries its own costs and risks.** GoatConf lends its
   audience and its calendar, not its money.

An extension is **one short file**: the record, written in plain text,
kept with the rest of the event in one place and shown on the website's
calendar. Hosts open a pull request to this repository, which is to be
public; hosts who do not use git send the same fields through a form
(the same form tool as the call for talks), and a volunteer turns it into
the file. An agent checks each extension pull request against the record
and the charter and comments a summary; the organiser merges (organiser's choice,
`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`). That keeps the list readable by
people and by agents, and lets the whole calendar be rebuilt from files,
the same way Pi extensions and this brain's pages are files.

### The kit: what others reuse

After the 2027 event, the parts that worked (the core list, the charter,
the extension record, the website template, the area playbooks) are
written up as a kit someone else can use for their own small, free
conference. Event first: nothing is extracted before GoatConf 2027 has
tested it (`sources/conversations/2026-10-07--org--first-answers.md`,
question 1).

### How it graduates

On a bet, this pitch becomes an **epic, "GoatConf 2027"**, with one child
per area pitch the organiser also bets on. The epic carries the core
list, the charter and the extension record; each child carries its own
work.

## Rabbit holes

- **Vetting creep.** Once listings exist, there will be pressure to judge
  them. The only checks are the charter and the code of conduct;
  anything more needs its own decision.
- **A fringe bigger than the conference.** Company events can crowd out
  community ones. London Tech Week lists not-for-profits free and
  charges businesses (`sources/web/models/london-tech-week-fringe-tiers-search-summary.md`,
  a search summary only); GoatConf may need the same split later.
- **Money with nowhere to go.** The organiser decided that no money goes
  through them (`sources/conversations/2026-10-07--org--no-money-through-me.md`),
  so a supporter pays a supplier or gives in kind. Supporters used to
  paying an event an invoice will need that explained once, plainly.
- **Rooms at IPI for extensions.** Workshops and hubs inside the venue
  depend on rooms whose number and size are unknown
  ([IPI Academy](../ipi-academy.md), § Unknown).
- **Liability.** An activity at the salt lake or a party is run by its
  host, but attendees will see GoatConf's name on it. The honest-name
  rule and the independence line help; whether they are enough locally is
  (unknown, needs source).
- **Building the kit too early.** Making the framework general before the
  event has run would cost the eight months the event needs.

## No-gos

- No paid tickets.
- No organiser money spent on an extension.
- No attendee data sold, shared or handed to sponsors without the
  attendee's explicit choice.
- No multi-track main program in 2027.
- No catering and no hotel room blocks in the core.
- No app; the website and the files are the interface.
- No kit extraction before the 2027 event.

## Choices made in auto mode

The organiser asked for these pitches in auto mode
(`sources/conversations/2026-10-07--org--first-answers.md`, question 5).
Each choice below is the agent's recommendation, recorded so it can be
overturned.

- **The core includes a charter.** Because a framework others extend
  needs rules that do not change per extension, and FOSDEM shows one page
  can carry them. Alternative: rules per slot only; rejected because it
  repeats the same terms seven times.
- **Breaks in town are in the core; catering is not.** Because the guide
  names catering as an expensive mistake and Tuzla is cheap to eat in.
  Catering can return as a support extension.
- **Listing is free for everyone in 2027.** Because the first year needs
  extensions more than revenue, and charging companies needs someone to
  invoice them. Alternative: London Tech Week's free-for-communities,
  paid-for-business split; deferred to a later edition.
- **Hubs are in, a commercial expo is not named.** Because Devcon's hub
  rules fit the free, community spirit; a sponsor who wants a booth can
  come through the support slot. The organiser named expo and booths as
  "maybe the extensible part", so this is open to their bet.
- **An extension is a file, with a form for people who do not use git.**
  Because it matches the Pi model the organiser named and keeps the
  calendar rebuildable, while not shutting out hosts who never touch a
  repository. Whether those files live in a public repository is a
  public act, and the organiser's to decide (AGENTS.md, Public acts).
- **The name story leads.** Because the organiser's own EuRuKo already
  used it, it is local and true, and it explains the minimal-core idea in
  one sentence.

## Open questions for the organiser

- Is the core list right: anything missing, anything that should be an
  extension instead?
- Should a commercial expo exist at all, or only hubs and sponsor-funded
  support?
