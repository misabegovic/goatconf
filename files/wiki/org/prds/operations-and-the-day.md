---
title: "Operations: volunteers who own a domain, the rules, and the day"
kind: initiative
status: living
updated: 2026-10-18
parent_epic: goatconf-2027
appetite: medium
confidence: medium
supersedes: org/pitches/operations-people-rules-and-the-day.md
sources:
  - sources/conversations/2026-10-18--org--speaker-travel-first-recording-main-hall-150.md
  - sources/conversations/2026-10-14--org--decisions-one-by-one.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--session-registration-later.md
  - sources/conversations/2026-10-12--org--approval-back-on.md
  - sources/conversations/2026-10-12--org--first-come-luma-only.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/organiser/muhamed-at-home.md
  - sources/web/organiser/muhamed-at-about.md
  - sources/web/venue/ipi-akademija-about.md
  - sources/web/coc/geek-feminism-anti-harassment-policy.md
  - sources/web/coc/ada-initiative-conference-policies.md
  - sources/web/coc/contributor-covenant-3-0.md
  - sources/web/coc/confcodeofconduct-com.md
  - sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md
  - sources/web/legal/tk-program-rada-skupstine-2026.md
  - sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md
  - sources/web/funding/fosdem-charter.md
  - sources/web/tooling/fosdem-video-equipment-overview.md
---

# Operations: volunteers who own a domain, the rules, and the day

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md),
graduated from the pitch
[Operations: run from Vienna, volunteers who own a domain, the rules, and the day](../pitches/operations-people-rules-and-the-day.md),
on which the organiser bet on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`). This
PRD waits for the organiser's approval before its ADR is written.

## Objective

**GoatConf runs on the day without needing the organiser at any one
post: every domain has a volunteer owner from IPI's students or the
community, a code of conduct names two reachable contacts, the local
rules on gatherings and personal data are met, and a run sheet covers the
day and what can go wrong.**

## Background

The organiser lives in Vienna ("Based in Vienna, working remotely across
Europe", `sources/web/organiser/muhamed-at-home.md`) and runs GoatConf
from there with volunteers and no co-organiser
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`). The
RubyEvents guide is blunt: "You cannot run a conference alone. You can
try, but you will make yourself miserable", and on the day "as much as
possible should already be someone else's problem"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Volunteers & Team and § Before you arrive). It also says "The burden is
meaningfully lighter with two people"; the organiser chose otherwise, so
the volunteers' domain owners and IPI Academy, as host of the building,
carry that weight.

Nobody is paid: the organiser's own money is a fallback of at most
1,000 EUR (`sources/conversations/2026-10-07--org--first-answers.md`),
"Just in case there are any expenses I need to cover. Normally, I pay for
nothing also"
(`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`),
never spent on food or drink for anyone
(`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`),
and no money passes through the organiser
(`sources/conversations/2026-10-07--org--no-money-through-me.md`).
Meanwhile the event has to meet Tuzla Canton's law on public gathering
and Bosnia and Herzegovina's personal data law, have a code of conduct
that someone can enforce, and survive whatever goes wrong.

## Affected personas

- [Volunteer](../../../.claude/personas/users/volunteer.md). Today there
  are none. With this work each volunteer owns one domain, knows the
  others from a call every two weeks, and on the day does not need the
  organiser to make a decision in that domain. What they get back is set
  with IPI and with them; a lunch only if a supporter pays for it.
- [Attendee](../../../.claude/personas/users/attendee.md). They get a
  door that opens on time, a code of conduct with two people they can
  reach, published accessibility facts, a return time announced at every
  long break, and the assurance that their registration data is kept
  only until the feedback survey and shared with nobody.
- [Speaker](../../../.claude/personas/users/speaker.md). They get a
  named person who looks after them on the day, a quiet room and water,
  and an honest note that the hall has no microphone and no recording.
- [Extension host](../../../.claude/personas/users/extension-host.md).
  They accept the code of conduct when they submit, and a volunteer owns
  their listing and answers their questions.

## Now / Perceived / Target

- **Now (2026-10-07).** No volunteer is recruited, no code of conduct is
  written, and no run sheet exists. The facts known: the code-of-conduct
  contacts are the organiser and a staff member from IPI
  (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`);
  which staff member is (unknown, needs source). IPI has "an active
  student association, Student Club of the IPI Academy"
  (`sources/web/venue/ipi-akademija-about.md`). The hall seats about 120,
  has a projector, sound and Wi-Fi, no microphone and no recording, and
  the main hall and first floor are step-free; whether there is an
  accessible toilet is (unknown, needs source)
  (`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
- **Perceived.** Running from Vienna is believed workable because the
  organiser knows IPI well (`sources/conversations/2026-10-07--org--no-money-through-me.md`)
  and has run EuRuKo 2024 and RubyConf Austria
  (`sources/web/organiser/muhamed-at-about.md`). The risk is that
  the day's small decisions (a late speaker, a lost group at lunch, a
  conduct report) still flow to the one person who is busiest. The legal
  reading below is the agent's, not legal advice, and new canton laws on
  events were due as proposals in June 2026
  (`sources/web/legal/tk-program-rada-skupstine-2026.md`); whether they
  changed anything is (unknown, needs source).
- **Target.** By May 2027: a volunteer owner for every domain, a code of
  conduct published on the site with both contacts and a phone number, a
  registration form that states its data terms, a run sheet with an owner
  per part, and a plan for what goes wrong. After the event: the list
  deleted after the feedback survey, and an honest note on what to keep
  and what to cut.

## Scope

**People.** Volunteers from both pools, IPI's students and the
community, on the organiser's choice
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`), each
owning one domain. The domains follow the guide's list (social and
marketing, catering logistics, design and swag, speakers and the CFP, the
MC; § What volunteers actually do), with catering logistics reduced to
the lunch and coffee list for Freedom Square and any supporter-funded
coffee, and two added for GoatConf: **extensions**, the person who helps
hosts and watches the listings the agent checks and the organiser merges
(`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`),
and **the door**, registration on the day. A short call every two weeks
from February 2027 (guide, § Building the team).

**The code of conduct.** One text, its reporting details, the two named
contacts with a phone number, ten minutes on stage at the start of the
core day (guide, § Code of conduct), and the rule that it applies to
every extension listed under GoatConf's name. A template alone is not
enough: one source says templates "should not be considered as
enforceable" without the event's own reporting details
(`sources/web/coc/confcodeofconduct-com.md`).

**The rules.** Under Tuzla Canton's law on public gathering, gatherings
for cultural and similar interests not aimed at earning income are not
notified (Article 35), unless their character or numbers call for extra
security, with notice at least five days ahead (Article 36)
(`sources/web/legal/tk-zakon-o-javnom-okupljanju-1-12.md`). A free,
indoor, registered conference reads as not requiring notice; a courtesy
notice remains an option for the organiser or IPI. Bosnia and
Herzegovina's personal data law, aligned with the GDPR
(`sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md`),
means the registration form says who holds the data, why, on what basis,
for how long and what rights people have; GoatConf keeps the list until
the feedback survey is sent, then deletes it, and shares it with nobody,
after FOSDEM's charter (`sources/web/funding/fosdem-charter.md`). The
accessibility facts known are published.

**The day.** A run sheet with an owner for each part: the door, the
stage and the MC, the speakers, the hiring corner if there is one, the
breaks on Freedom Square (one to two hours each, under five minutes from
IPI, `sources/conversations/2026-10-07--org--space-to-hang-out.md`,
`sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md`)
with a volunteer walking the square before the hall reopens, first aid,
and someone to call. Registration runs from a printed list with badges
and a volunteer who does nothing else until the door is done (guide,
§ Registration). Speakers project their voice. A plan for what goes
wrong: a speaker stuck in transit, a dead projector, a conduct report,
rain on the lake day.

**After.** A feedback survey within a week, the money settled on the
public ledger within two weeks, and a note on what to keep and cut that
becomes the first page of the reusable kit (guide, § After The
Conference).

## No-gos

- No paid staff, and nothing from the organiser's fallback money for
  staffing, food or drink.
- No co-organiser; the domain owners and IPI carry the load.
- No attendee data kept after the feedback survey, sold or shared.
- No extension listed whose host has not accepted the code of conduct.
- No recording in the core unless a supporter funds the equipment
  directly; IPI's hall records nothing.
- No public act (a police notice, a message to attendees, a post) sent by
  an agent; the agent drafts, the organiser sends.

## Rabbit holes

- **The organiser doing everything from Vienna.** The largest risk, taken
  knowingly. If the run sheet has the organiser's name on more than the
  opening and the conduct contact, stop and find an owner.
- **Volunteers without a domain.** Help that is not owned gets dropped;
  do not recruit people without something to own.
- **Becoming a legal project.** The two laws are read once, the reading
  is checked with IPI, and the questions that remain go to the organiser.
  If it needs a lawyer, re-pitch.
- **Video.** Recording only happens if a supporter funds it, run the way
  FOSDEM's volunteers do (a camera, a mixer and a slide capture per room,
  with a checklist, `sources/web/tooling/fosdem-video-equipment-overview.md`).
  Do not plan around it.

## Appetite

**Medium.** The work is spread over eight months rather than heavy at
any point: recruiting volunteers from November 2026, the code of conduct
and the registration form's data terms before registration opens, a call
every two weeks from February 2027, and the run sheet by May 2027. It is
more than a list and less than a full cycle of build.

## Success metrics

- **Every domain on the run sheet has a named volunteer owner by
  15 May 2027.** Observed as the run sheet page in this repository, with
  no domain owned by "the organiser" except the opening and the conduct
  contact.
- **The code of conduct is live with both contacts and a phone number
  before registration opens.** Observed as the commit date of the code of
  conduct page against the date registration opens on the site.
- **The registration list is deleted within a week of the feedback survey
  being sent.** Observed as a dated note under `sources/` recording the
  deletion and the survey's send date.
- **Volunteers attending at least half the calls every two weeks: four or
  more.** Observed as attendance noted in each call's record under
  `sources/conversations/`.

## Dependencies

- [Dates and the core day](./dates-and-the-core-day.md): the day the run
  sheet covers, and the shape of the breaks.
- [Website and registration](./website-and-registration.md): the code of
  conduct page, the registration form and its data terms.
- [Extension slots and the record](./extension-slots-and-the-record.md):
  the code-of-conduct acceptance in the record, and the extensions
  domain.
- [CFP and speakers](./cfp-and-speakers.md): the speakers domain and the
  waitlist for a speaker who cannot come.
- [Budget and the public ledger](./budget-and-public-ledger.md): any
  supporter-funded coffee, lunch for volunteers or video.
- [Activities: the lake and the town](./activities-lake-and-town.md): the
  rain plan and the goat hunt's owner.
- [The road to June 2027](./road-to-june-2027.md): when each step is due.

## Decisions already made by the organiser

- No co-organiser; the organiser manages from Vienna with volunteers
  (`sources/conversations/2026-10-07--org--talks-team-and-site.md`).
- Volunteers are IPI's students and community volunteers together
  (`sources/conversations/2026-10-07--org--talks-team-and-site.md`).
- The code-of-conduct contacts are the organiser and a staff member from
  IPI Academy
  (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
- Registration opens when IPI confirms the date in writing, likely
  November 2026
  (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
- Registration is capped at the hall's capacity, about 120; the hall has
  no microphone and no recording, and speakers project their voice
  (`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
- Breaks happen on Freedom Square, under five minutes from IPI, one to
  two hours each
  (`sources/conversations/2026-10-07--org--space-to-hang-out.md`,
  `sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md`).
- The organiser pays for no food or drink, for anyone
  (`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
- No money passes through the organiser; the budget is public
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- Extensions come in by pull request or the CFP's form tool; an agent
  checks each and the organiser merges
  (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

## Open questions

- Which IPI staff member is the second code-of-conduct contact (unknown,
  needs source).
- Would IPI's student club take on volunteering, and what would its
  members want in return?
- Who is the data controller for the registration list, the organiser or
  IPI as host (unknown, needs source)?
- Is a courtesy notice to the police wanted, and is it the organiser's or
  IPI's to send?
- Is there an accessible toilet on the step-free floors (unknown, needs
  source)?

## Decision needed

**Which code of conduct GoatConf adopts, and how a report reaches the two
contacts.** The pitch chose the Geek Feminism / Ada Initiative
anti-harassment policy, public domain and written for in-person events
with a staff procedure
(`sources/web/coc/geek-feminism-anti-harassment-policy.md`,
`sources/web/coc/ada-initiative-conference-policies.md`), over the
Contributor Covenant 3.0 under CC BY-SA 4.0
(`sources/web/coc/contributor-covenant-3-0.md`); the ADR makes and
records that choice, and records with it the run sheet's shape: the
domains, one owner each, and the path a problem travels on the day.

**Answered by the ADR** [Adopt RubyConf Austria's code of conduct and its reporting route, with an IPI contact added](../adrs/operations-and-the-day.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** There are two core days, Thursday 3 and Friday 4 June 2027, in every available room in parallel. Check-in uses the registration sheet's export, printed per day, since Luma is no longer used; the door volunteer closes a full room. Code-of-conduct reports can also come through the contact form on goatconf.com. See [Dates: two core days](../adrs/two-core-days-first-week.md), [Core days: parallel rooms](../adrs/core-day-parallel-tracks.md), [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. Registration and the run sheet no longer wait on IPI (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-14, read with the later decisions.** "Luma is no longer used" in the first amendment above no longer holds: registration is on the organiser's Luma event, not a Google Form, with no limit; the organiser approves each registration, seats are first come, first served at each room's door, and ticket holders register for sessions later, with the tool not decided yet (sources: sources/conversations/2026-10-12--org--registration-on-luma.md, sources/conversations/2026-10-12--org--first-come-luma-only.md, sources/conversations/2026-10-12--org--approval-back-on.md, sources/conversations/2026-10-12--org--session-registration-later.md). How check-in works is (unknown, needs source), and so is who controls registrants' data on Luma and where Luma keeps it. The body's final account on the public ledger no longer holds: the budget is private, with no budget page and no public ledger; online supporters pay the organiser's Austrian business 500 EUR for online perks only, and speakers' travel is refunded only if the budget allows, never promised (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
- **2026-10-14, check-in and the code-of-conduct team.** Check-in uses Luma's free check-in app, scanning each guest's QR code at the door. The organiser is the only code-of-conduct contact until IPI names a member of staff (source: sources/conversations/2026-10-14--org--decisions-one-by-one.md). Who controls registrants' data on Luma, and where Luma keeps it, is still (unknown, needs source).
- **2026-10-18, recording in the two big halls.** The no-go on recording in the core no longer holds as written: GoatConf aims to record the sessions in the main hall and the first-floor hall, not promised yet, and how it is paid for and done is (unknown, needs source). The main hall is given as 150 seats on the site (source: sources/conversations/2026-10-18--org--speaker-travel-first-recording-main-hall-150.md).
