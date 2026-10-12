---
title: "Design with impeccable: product truth first, then one look for every surface"
kind: pitch
status: superseded
updated: 2026-10-07
appetite: small
confidence: low
sources:
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/web/funding/euruko-2024-why-the-goat.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - .claude/skills/impeccable/SKILL.md
  - .claude/skills/impeccable/reference/init.md
superseded_by: org/prds/design-with-impeccable.md
---

# Design with impeccable: product truth first, then one look for every surface


> **Bet on and graduated, 2026-10-07.** The organiser bet on this pitch; it continues as [design-with-impeccable.md](../prds/design-with-impeccable.md). This page is kept as the pre-bet record.

Area pitch under [One goat feeds the town](one-goat-minimal-core-and-extensions.md).
Pre-bet, shaped in auto mode on 2026-10-07.

## Problem

The organiser asked for "design (with impeccable)"
(`sources/conversations/2026-10-07--org--conference-vision.md`), and
impeccable 4.1.0 was installed in this repository the same day on their
choice (`sources/conversations/2026-10-07--org--first-answers.md`,
question 4). A conference's design is more than a website: the guide asks
for "something to share" (speaker cards, "I'm attending" images, a
copy-paste blurb, venue photos, city clips) because "the best promotion
usually does not come from the conference account"
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Give attendees something to share). Badges, slides templates, signs at
the venue and social images all need one look, made once, by an
organiser with no design budget.

There is also a framework angle. Extension hosts will make their own
posters and pages. If GoatConf's look is written down as rules rather
than kept in one designer's head, hosts can match it.

## Appetite

**Small:** an interview and a first direction in a week of evenings, the
website built on it, and a short design document others can follow.
Printing and merchandise are not in the appetite; they are support
extensions if a sponsor pays.

## Solution

Impeccable's own flow fits the order the work needs.

1. **Product truth first: `init`.** It "captures durable product truth in
   PRODUCT.md. It does not invent a visual world and does not write
   DESIGN.md" (`.claude/skills/impeccable/reference/init.md`). It
   interviews the organiser on who the users are, what the event makes
   possible and what is different about it, and asks the stack question
   (plain HTML and CSS, a framework, or delegated) before anything is
   built (same source). The brain already holds most answers:
   [GoatConf 2027: what is known](../goatconf-2027.md), the
   [personas](../../../.claude/personas/users/README.md), and the umbrella
   pitch's core and charter. PRODUCT.md would summarise them; the brain
   stays the source of truth.
2. **One visual world: `new-work`, then `document`.** Impeccable creates a
   visual direction for new surfaces and records the result in DESIGN.md
   (`.claude/skills/impeccable/SKILL.md`, command table). The identity
   material is already local and specific: Tuzla's goat, its statue and
   the saying "The whole of Tuzla milked one goat"
   (`sources/web/funding/euruko-2024-why-the-goat.md`), the salt lake,
   and a cheap, warm city. The guide's advice is to be tied to a place on
   purpose: "Don't accidentally build a generic conference when you could
   build one that feels like something special"
   (guide, § Know what your event is).
3. **The surfaces, in order of need:** the website's first page; a social
   card template and an "I'm attending" image; speaker cards; a one-page
   sponsor sheet; badges and room signs; a slide template for the MC and
   speakers who want one.
4. **A host kit.** The logo, colours, type and a few rules from DESIGN.md,
   packaged so an extension host can make a matching poster. This is part
   of the kit the umbrella pitch extracts after 2027, started now because
   hosts need it in spring.

Impeccable's detector runs while the site is written (its hook is
committed in this repository), so the site is checked against its design
rules as it is built.

## Rabbit holes

- **A brand project.** A logo competition, a mascot, a type foundry: all
  pleasant, none needed for a first edition.
- **Overusing the goat.** The story is strong once; a goat on every
  surface turns it into a joke. DESIGN.md should say where it appears.
- **Impeccable's network calls.** New visual concepts are fetched from
  impeccable's catalogue; the update check and choice reporting are
  switched off in this repository's settings. Nothing else is sent.
- **Echoing EuRuKo 2024's look.** The name story is shared with the
  organiser's own earlier event; the visual world should be GoatConf's.

## No-gos

- No paid design work from the organiser's 1,000 EUR.
- No merchandise in the core.
- No design decision recorded only in a file nobody can read; DESIGN.md
  is committed.

## Choices made in auto mode

- **PRODUCT.md summarises the brain rather than replacing it.** Because
  two sources of truth drift; the wiki stays canonical.
- **The website is the first surface.** Because the guide puts it first
  and every later surface borrows from it.
- **A host kit is in this pitch, not deferred.** Because extension hosts
  make materials in spring 2027, before the kit is extracted.

## Open questions for the organiser

- Any binding visual constraint already: a colour, a logo idea, the goat
  statue?
- Should the look nod to EuRuKo 2024's G.O.A.T., or stand apart?
- Plain HTML and CSS for the site, or a framework you prefer?
