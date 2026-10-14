---
title: "Design with impeccable: one look for the site, the shareables and the hosts"
kind: initiative
status: living
updated: 2026-10-14
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/design-with-impeccable.md
sources:
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/web/funding/euruko-2024-why-the-goat.md
  - sources/web/organiser/muhamed-at-about.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - .claude/skills/impeccable/SKILL.md
  - .claude/skills/impeccable/reference/init.md
---

# Design with impeccable: one look for the site, the shareables and the hosts

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md).
It graduates the pitch
[Design with impeccable](../pitches/design-with-impeccable.md), bet on by
the organiser on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`).

## Objective

**GoatConf has one visual world, written down in this repository as
PRODUCT.md and DESIGN.md through impeccable, that the website, the
things attendees and speakers share, the day's badges and signs, and
every extension host's poster all follow.**

## Background

The organiser asked for "design (with impeccable)"
(`sources/conversations/2026-10-07--org--conference-vision.md`), and
impeccable 4.1.0 was installed in this repository only, with the update
check and choice reporting off, to be used for PRODUCT.md, DESIGN.md and
the website (`sources/conversations/2026-10-07--org--first-answers.md`,
question 4). The site's pages are designed here with impeccable and
copied into muhamed.at/goatconf
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`,
`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).

A conference's design is more than its site. The guide asks for
"something to share" (speaker cards, "I'm attending" images, a
copy-paste blurb, venue photos) because "the best promotion usually does
not come from the conference account"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Give attendees something to share). And GoatConf is built to be
extended: hosts will make their own posters and pages, and can match the
event only if the look is written down as rules
([Extension slots and the record](extension-slots-and-the-record.md)).

The identity material is local and specific: Tuzla's goat and the saying
"The whole of Tuzla milked one goat", the story behind the organiser's
EuRuKo 2024 (`sources/web/funding/euruko-2024-why-the-goat.md`), the
salt lake, and a cheap, warm city. The guide's warning applies: "Don't
accidentally build a generic conference when you could build one that
feels like something special" (guide, § Know what your event is).

## Affected personas

- [Attendee](../../../.claude/personas/users/attendee.md). Today there is
  nothing to look at or share. With this shipped, an attendee meets one
  recognisable look on the site, on an "I'm attending" image they can
  post, and on the badge and signs on the day.
- [Speaker](../../../.claude/personas/users/speaker.md). Gets a speaker
  card to share and, if they want one, a slide template.
- [Extension host](../../../.claude/personas/users/extension-host.md).
  Gets a small host kit (logo, colours, type, a few rules) to make a
  matching poster in spring, without asking the organiser.
- [Volunteer](../../../.claude/personas/users/volunteer.md). Prints and
  puts up signs from templates rather than designing them.

## Now / Perceived / Target

- **Now (2026-10-07):** impeccable is installed and its hook is
  registered in this repository's settings
  (`.claude/settings.json`); no PRODUCT.md, no DESIGN.md, no logo and no
  surface exists.
- **Perceived:** that the brain already holds most of what impeccable's
  `init` interview asks (who the users are, what the event makes
  possible, what is different about it). The interview has not been run,
  so this is unverified (2026-10-07).
- **Target:** PRODUCT.md and DESIGN.md committed in this repository; the
  website's first page built on them; social and speaker templates; a
  sponsor sheet; badges and room signs; a slide template; and a host kit,
  all from one look.

## Scope

**Product truth first.** Impeccable's `init` "captures durable product
truth in PRODUCT.md. It does not invent a visual world and does not
write DESIGN.md" (`.claude/skills/impeccable/reference/init.md`). It
interviews the organiser and asks the stack question before anything is
built. PRODUCT.md summarises what the brain holds
([GoatConf 2027: what is known](../goatconf-2027.md), the personas, the
epic and the charter); the brain stays the source of truth.

**One visual world.** Impeccable's flow for a new surface creates a
visual direction, and its `document` command records the result in
DESIGN.md (`.claude/skills/impeccable/SKILL.md`, command table).
DESIGN.md says where the goat appears and where it does not.

**The surfaces, in order of need:** the website's first page; a social
card template and an "I'm attending" image; speaker cards; a one-page
supporters sheet; badges and room signs; a slide template for the MC and
for speakers who want one.

**The host kit.** The logo, colours, type and a few rules from
DESIGN.md, packaged so an extension host can make a matching poster. It
is started now because hosts make materials in spring 2027, ahead of the
reusable kit that is extracted only after the event.

**The pages fit their host site.** The site's pages are copied into
muhamed.at, which runs on a clone of pi-brain
(`sources/web/organiser/muhamed-at-about.md`), so the look works inside
that site rather than against it.

## No-gos

- No paid design work from the organiser's money, which is a fallback
  only (`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`).
- No merchandise in the core; printing and merchandise are support
  extensions a supporter pays a supplier for directly
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- No design decision kept only in someone's head or a private file;
  PRODUCT.md and DESIGN.md are committed, in a repository that will be
  public (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).
- No second source of truth: PRODUCT.md summarises the wiki, never
  replaces it.
- No turning impeccable's update check or choice reporting back on.

## Rabbit holes

- **A brand project.** A logo competition, a mascot, a type foundry: all
  pleasant, none needed for a first edition. Stop at what the surfaces
  need.
- **Overusing the goat.** The story is strong once; on every surface it
  becomes a joke.
- **Echoing EuRuKo 2024's look.** The name story is shared with the
  organiser's earlier event; the visual world should be GoatConf's own,
  unless the organiser says otherwise.
- **Impeccable's network calls.** New visual concepts are fetched from
  impeccable's catalogue; nothing else should leave the machine. If a
  step needs more, stop and ask.
- **Fighting the host site.** If the look needs muhamed.at's own layout
  rebuilt, stop and re-pitch.

## Appetite

**Small.** An interview and a first direction in a week of evenings, the
website's first page built on it, and a short DESIGN.md others can
follow. The later surfaces are templates from the same look, made as
each is needed.

## Success metrics

- **PRODUCT.md and DESIGN.md are committed before the website's first
  page is published.** Observed from the commit dates of both files
  against the page's first publish date.
- **Every surface named here exists as a file in this repository by the
  week before the event.** Observed as a count of the templates
  (social card, "I'm attending" image, speaker card, supporters sheet,
  badge, room sign, slide template) at that date.
- **The host kit is published before the first extension is listed.**
  Observed from the host kit's commit date against the first merged
  extension record.
- **At least one extension host uses the host kit.** Observed from a
  host's poster or page linked in their extension record.

## Dependencies

- [Website and registration](website-and-registration.md): the first
  surface built on the look.
- [Extension slots and the record](extension-slots-and-the-record.md):
  the hosts who use the host kit.
- [Social drumbeat](social-drumbeat.md): uses the social and speaker
  templates.
- [Supporters and hiring](supporters-and-hiring.md): uses the supporters
  sheet.
- [Operations and the day](operations-and-the-day.md): badges and signs.
- [CFP and speakers](cfp-and-speakers.md): speaker cards and the slide
  template.

## Decisions already made by the organiser

- **Design with impeccable.**
  `sources/conversations/2026-10-07--org--conference-vision.md`.
- **Impeccable installed in this repository only, update check and choice
  reporting off, used for PRODUCT.md, DESIGN.md and the website.**
  `sources/conversations/2026-10-07--org--first-answers.md`, question 4.
- **Pages are designed here and copied into the organiser's site.**
  `sources/conversations/2026-10-07--org--talks-team-and-site.md`.
- **The site path is muhamed.at/goatconf.**
  `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **This repository will be public.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.
- **The organiser's money is a fallback only.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`.

## Open questions

- Is there any binding visual constraint already: a colour, a logo idea,
  the goat statue?
- Should the look nod to EuRuKo 2024's G.O.A.T. edition, or stand apart?
- Who prints badges and signs, and who pays the printer directly?
  (unknown, needs source)

## Decision needed

The answer to impeccable's stack question for the pages: plain HTML and
CSS with no build step (the pitch's recommendation), a framework, or the
conventions of the organiser's pi-brain site. The ADR records that
choice and the visual direction DESIGN.md commits to, including where
the goat appears.

**Answered by the ADR** [Build the pages in plain HTML and CSS, with the goat everywhere and playful](../adrs/design-with-impeccable.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** The site is published on goatconf.com from this repository, not copied into muhamed.at. See [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-14, read with the later decisions.** The site no longer sits inside muhamed.at, so the body's rule against fighting that site's look, and its pi-brain layout, no longer constrains the design (source: sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md).
