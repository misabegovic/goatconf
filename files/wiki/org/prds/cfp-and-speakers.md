---
title: "An open call by Google Form, judged by the organiser, filling every room's slots, and travel that speakers fund"
kind: initiative
status: living
updated: 2026-10-17
parent_epic: goatconf-2027
appetite: medium
confidence: medium
supersedes: org/pitches/cfp-and-speakers.md
sources:
  - sources/conversations/2026-10-17--org--dejan-talk.md
  - sources/conversations/2026-10-14--org--speakers-before-sessions.md
  - sources/conversations/2026-10-14--org--speakers-dinner.md
  - sources/conversations/2026-10-13--org--speaker-profile-required.md
  - sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md
  - sources/conversations/2026-10-07--org--space-to-hang-out.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/speakers/live360-2021-call-for-speakers.md
  - sources/web/speakers/pycon-us-2026-speaking-guidelines.md
  - sources/web/speakers/europython-2026-financial-aid.md
  - sources/web/speakers/writethedocs-portland-2026-opportunity-grants.md
  - sources/web/funding/euruko-2024-sponsoring.md
  - sources/web/tooling/sessionize-anonymous-mode.md
  - sources/web/tooling/pretalx-review-docs.md
---

# An open call by Google Form, judged by the organiser, filling every room's slots, and travel that speakers fund

Product requirements for GoatConf 2027's program. It graduates the pitch
[An open CFP for self-funded speakers](../pitches/cfp-and-speakers.md), on
which the organiser bet on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`), and sits
under the epic [GoatConf 2027](../epics/goatconf-2027.md).

## Objective

**A main-day program of three to four strong talks, one or two invited from
the organiser's network and the rest chosen from an open call run on a
simple form, with every speaker told plainly before they apply that their
travel is their own.**

## Background

The program is what attendees travel for: "You need talks, because
otherwise why would your boss let you go?"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
Why a Conference). GoatConf's main day is deliberately small: three to four
talks, "very spacious: mostly hanging out, a few strong talks"
(`sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md`,
question 3), with IPI Academy used only for lectures and the coffee and
lunch breaks in town, one to two hours each
(`sources/conversations/2026-10-07--org--space-to-hang-out.md`).

Speakers pay their own way: "only apply if you can get your travel costs
covered, I don't cover that", with "like 100 euros per speaker" floated and
"maybe not even that"
(`sources/conversations/2026-10-07--org--conference-vision.md`). Since then
the organiser has said their own money is a fallback only: "Normally, I pay
for nothing also"
(`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`,
question 1). Self-funded travel narrows the pool to speakers whose
employers pay or who can afford it
([speaker persona](../../../.claude/personas/users/speaker.md)).

The guide says to open a CFP four to six months before the event (guide,
§ When to CFP), which for early June 2027 means between December 2026 and
February 2027.

## Affected personas

- **[Speaker](../../../.claude/personas/users/speaker.md).** *Now:* no call
  exists. *Target:* a call that states up front what GoatConf gives (a
  place on stage, a free registration, clear answers to every logistical
  question, the low cost of a stay in Tuzla) and what it does not (travel),
  a fair review that does not see whether they asked for a grant, a prompt
  answer whether accepted or not, and real homes for good proposals that
  do not fit three to four slots.
- **[Attendee](../../../.claude/personas/users/attendee.md).** *Now:* no
  program. *Target:* a few strong talks across disciplines, announced early
  enough to justify the trip, with most of the day left for people.

Secondary:

- **[Hiring partner](../../../.claude/personas/users/hiring-partner.md)**:
  a company that pays its own speaker's travel, or funds a grant pool, is
  thanked as a supporter, and never buys a talk.
- **[Extension host](../../../.claude/personas/users/extension-host.md)**:
  hosts of workshops and fringe events are where proposals that do not fit
  the main day can land.
- **[Volunteer](../../../.claude/personas/users/volunteer.md)**: one may
  own the anonymising step or speaker care.

## Now / Perceived / Target

- **Now (2026-10-07):** no call, no invited speaker named, no committee,
  no form. The organiser has decided the selection model (invited plus open
  call) and the tool (a simple form, reviewed in a shared sheet).
- **Perceived:** (unknown, needs source) how many proposals a first
  edition with self-funded travel attracts is not known; the risk runs both
  ways, too few from outside the organiser's network, or far more good
  proposals than three to four slots.
- **Target:** one or two invited speakers confirmed before the call opens;
  an open call published between December 2026 and February 2027 on a
  simple form; anonymised review by a small committee across disciplines;
  three to four main-day talks confirmed and announced; a short waitlist;
  every speaker with one complete acceptance message.

## Scope

The invited speakers come first: one or two, both from the organiser's
network, confirmed before the call opens so it launches with a reason to
submit (`sources/conversations/2026-10-07--org--talks-team-and-site.md`,
questions 1 and 2; guide, § CFP or curated?). The open call fills the
remaining main-day slots and is where disciplines beyond the organiser's
Ruby network get their place.

The call text says what program GoatConf wants (talks for an open,
multi-discipline, English-speaking audience, the slot length, the closing
date, first-time speakers welcome; guide, § How to run a CFP), and puts the
money first, in a sentence like Live! 360's "Speakers are responsible for
their own travel costs and incidentals"
(`sources/web/speakers/live360-2021-call-for-speakers.md`). It says that
proposals far outnumber slots and points to the workshop day, hubs and
fringe events as real places for them.

Proposals arrive through a simple form, Tally or a Google Form, and the
committee reviews in a shared sheet
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`,
question 4); Tally is free with data stored in Europe
(`sources/web/tooling/tally-pricing.md`). For anonymised review, one person
copies proposals into a reviewers' sheet without names or bios, the step
Sessionize and pretalx automate
(`sources/web/tooling/sessionize-anonymous-mode.md`,
`sources/web/tooling/pretalx-review-docs.md`). A committee of three to five
across disciplines scores on clarity, relevance and fit, and the program is
assembled as a whole rather than by score (guide, § Build a CFP committee).

Accepted speakers are told before anyone is announced, declined speakers
promptly, and a short waitlist is kept (guide, § Accepted, declined, and
waitlisted speakers). Each accepted speaker gets one message with
everything (date, what GoatConf gives, how to reach Tuzla, where to stay,
deadlines, the code of conduct), and first-time speakers get a check-in a
few weeks out (guide, § What speakers need).

A speaker grant exists only if a supporter funds it, as a named item on
the supporters' menu, the way EuRuKo 2024 sold "Speaker Travel &
Accommodation" support (`sources/web/funding/euruko-2024-sponsoring.md`).
If it exists, the request is a separate question reviewers never see, as
at PyCon US, whose grant checkbox "is not seen by the proposal reviewers"
(`sources/web/speakers/pycon-us-2026-speaking-guidelines.md`), with a cap
per person as at EuroPython
(`sources/web/speakers/europython-2026-financial-aid.md`) and recipients
not named, as at Write the Docs
(`sources/web/speakers/writethedocs-portland-2026-opportunity-grants.md`).
The supporter pays the speaker's travel supplier or the speaker directly;
nothing passes through the organiser. If no supporter funds it, there is no
grant, and the call says so.

## No-gos

- No speaker travel or accommodation paid from the organiser's fallback
  money.
- No money for speakers passing through the organiser.
- No paid speaking slots; supporters do not buy talks.
- No speaker announced publicly before they have confirmed.
- No parallel talks on the main day and no more than four talks there.
- No proposals, names, bios or reviewer scores in this repository, which
  will be public; they stay in the form tool and the shared sheet.
- No speaker dinner or other food and drink from the organiser's money; a
  dinner happens only if a supporter funds it.

## Rabbit holes

- **Only local or only wealthy speakers.** Without a grant the program may
  skew to people whose employers fly them. The answer is a supporter-funded
  grant, not the organiser's money; if none comes, the call says so plainly
  and the committee weighs the mix.
- **Far more proposals than slots.** With three to four talks and one or
  two of them invited, most good proposals will not fit. Stop trying to fit
  them into the main day; route them to workshops and extensions.
- **Anonymity by hand.** Copying proposals without names is manual and easy
  to get wrong. One person owns it, and nobody else sees the original sheet
  until review is done.
- **Adopting a full CFP platform.** With three to four slots a sheet is
  enough; Sessionize and pretalx stay noted for a larger edition.

## Appetite

**Medium:** writing the call, inviting speakers and outreach run from
November to January, the call stays open a few weeks, review and assembly
run into spring, and speaker care runs until the day. The work is light in
any one week but spans six months, and anonymised review by hand is the
part that grows with the number of proposals.

## Success metrics

- **One or two invited speakers confirmed before the call opens.** Observed
  as the confirmation date recorded in this brain against the call's
  publication date.
- **The call opens by 28 February 2027 and receives at least 20
  proposals.** Observed as the call's publication date and the row count of
  the form tool's export at close.
- **Proposals from at least three disciplines (engineering, design,
  product, founding).** Observed by counting a discipline field in the form
  export at close; if the form does not ask, recorded as not checked.
- **Three to four main-day talks confirmed and announced by 30 April
  2027,** every accepted and declined speaker answered within two weeks of
  review closing. Observed from the program page on the site and the dates
  of the answers in the review sheet.

## Dependencies

- [Dates and the core day](dates-and-the-core-day.md): the slot count,
  length and the workshop day the call points to.
- [Website and registration](website-and-registration.md): the call is
  published on muhamed.at/goatconf; speakers get a free registration.
- [Supporters and hiring](supporters-and-hiring.md): the speaker grant pool
  and speaker dinner exist only as funded menu items.
- [Budget and the public ledger](budget-and-public-ledger.md): a funded
  grant appears on the ledger as a line.
- [Extension slots and the record](extension-slots-and-the-record.md): uses
  the same form tool, and is where proposals that do not fit can go.
- [Social drumbeat](social-drumbeat.md): announces the call and the
  speakers.
- [Operations and the day](operations-and-the-day.md): the code of conduct
  speakers agree to.

## Decisions already made by the organiser

- **Invited plus open call: one or two invited, the rest from the call.**
  `sources/conversations/2026-10-07--org--talks-team-and-site.md`
  (question 1).
- **Both invited speakers come from the organiser's network.**
  `sources/conversations/2026-10-07--org--talks-team-and-site.md`
  (question 2).
- **Three to four talks on the main day.**
  `sources/conversations/2026-10-07--org--freedom-square-and-few-talks.md`
  (question 3).
- **The call uses a simple form; the committee reviews in a shared
  sheet.** `sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`
  (question 4).
- **Speakers pay their own travel.**
  `sources/conversations/2026-10-07--org--conference-vision.md`.
- **The organiser's money is a fallback only, at most 1,000 EUR, and never
  pays for food or drink.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`
  and `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **No money passes through the organiser.**
  `sources/conversations/2026-10-07--org--no-money-through-me.md`.
- **Extension submissions use the same form tool as the CFP.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.

Moving the floated 100 EUR contribution into a supporter-funded pool is a
choice made in auto mode in the pitch; the organiser has not ruled on it.

## Open questions

- Who are the one or two invited speakers?
- Who sits on the committee with the organiser, across disciplines?
- Talk length: 30 minutes, as in the guide's 30-30 format, or shorter?
- Does the call also take workshop proposals, or do workshops come only
  through extension slots?
- Is the 100 EUR per speaker off the table, or open if a supporter funds
  it?

## Decision needed

**Which simple form tool runs the call (Tally or a Google Form) and how the
anonymised review is set up around it:** the questions on the form, where
the grant question sits so reviewers never see it, who copies proposals
into the reviewers' sheet, and how long the data is kept. The extension
submissions use the same tool, so the ADR's choice binds that PRD too.

**Answered by the ADR** [Take talks through Google Forms and review them blind with a panel of two or three](../adrs/cfp-and-speakers.md), accepted 2026-10-07.

## Amendments

- **2026-10-13, profiles are required.** Proposing a session means agreeing that, if accepted, the speaker's profile is published and promoted on social media (source: sources/conversations/2026-10-13--org--speaker-profile-required.md).
- **2026-10-13, the travel question.** The talk form asks about travel with three optional choices: no travel support needed; the speaker's company covers it and is then listed on the site as a supporter; or the speaker pays and would welcome a refund if the budget allows, never promised. It replaced the travel grant question (source: sources/conversations/2026-10-13--org--speaker-travel-and-luma-question.md).
- **2026-10-12.** The call is a Google Form on goatconf.com, open now with no strict deadline, and the organiser judges every proposal, reading it first without the name. The blind panel of two or three and the fixed window are superseded. Slots are the four one-hour slots in every room on both core days, filled as proposals are accepted; the talks are the keynotes. Accepted talks become program records built into the program page. See [The call: the organiser judges](../adrs/call-organiser-judges.md), [Core days: parallel rooms](../adrs/core-day-parallel-tracks.md), [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-13, superseded in part.** The no-gos on money through the organiser and the public budget no longer hold: online supporters pay the organiser's Austrian business, the budget is private, and speakers' travel is refunded only if the budget allows ([Online supporters pay the organiser's Austrian business](../adrs/online-supporters-through-the-business.md); source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
- **2026-10-14, the speakers dinner.** Every accepted speaker is invited to a speakers dinner, with the date still to come. It is paid from online supporters' money, as an event cost, if the budget allows; the organiser's own money never pays for it, and until it is funded everyone pays for their own meal. The talk page and the live talk form say so (source: sources/conversations/2026-10-14--org--speakers-dinner.md).
- **2026-10-14, speakers before their sessions.** A confirmed speaker who has agreed to a public profile can be published before their session has a slot or a topic; their page says the session will be on the program soon. The first is [Dejan Menges](../speakers/dejan-menges.md), whose bio is the short bio on his own site and whose photo comes from his last conference's speaker page, on the organiser's choice (source: sources/conversations/2026-10-14--org--speakers-before-sessions.md).
- **2026-10-15, the talk shows before its slot.** A record can carry the proposed session's title and the speaker's own words on it while it has no slot: the page and card show them with the day and time to be announced, in place of "The session will be on the program soon.", and the check asks for the fields to come off once the session is on the program. First used for [Christoph Lipautz](../speakers/christoph-lipautz.md) (source: sources/conversations/2026-10-15--org--christoph-talk-on-his-page.md).
- **2026-10-17, room for a longer talk text.** A speaker's own words on a talk without a slot may run to 300 words, up from 120, so a proposal's full answer fits; the bio stays at 120. First used for [Dejan Menges](../speakers/dejan-menges.md), whose four paragraphs show in full (source: sources/conversations/2026-10-17--org--dejan-talk.md).
- **2026-10-15, a record can be held from the site.** A speaker record can carry a `hold` line while the speaker must not show, for example while their employer clears the engagement: the record is kept and checked but listed nowhere, their page comes down on the next build, and their order keeps its place in the no-two-share check; removing the line publishes them again. First used for [Jan Grodowski](../speakers/jan-grodowski.md) (source: sources/conversations/2026-10-15--org--hold-jan-grodowski.md).
