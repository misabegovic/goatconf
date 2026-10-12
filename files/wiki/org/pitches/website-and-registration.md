---
title: "A website of plain pages and a free registration with a cap"
kind: pitch
status: superseded
updated: 2026-10-07
appetite: small
confidence: low
sources:
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/tooling/pretix-hosted-pricing.md
  - sources/web/tooling/pretix-features.md
  - sources/web/tooling/tito-pricing.md
  - sources/web/tooling/luma-pricing.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/web/github-pages-limits.md
  - sources/web/web/cloudflare-pages-limits.md
  - sources/web/web/netlify-pricing.md
  - sources/web/web/cloudflare-registrar.md
  - sources/web/web/cfdomainpricing-com-price.md
  - sources/web/web/namepros-ba-thread-2021.md
  - sources/web/web/tldes-ba-registrar-prices.md
  - sources/web/web/domaindetails-ba.md
  - sources/web/funding/fosdem-charter.md
superseded_by: org/prds/website-and-registration.md
---

# A website of plain pages and a free registration with a cap


> **Bet on and graduated, 2026-10-07.** The organiser bet on this pitch; it continues as [website-and-registration.md](../prds/website-and-registration.md). This page is kept as the pre-bet record.

Area pitch under [One goat feeds the town](one-goat-minimal-core-and-extensions.md).
Pre-bet, shaped in auto mode on 2026-10-07.

## Problem

GoatConf needs two public surfaces before almost anything else: a site
that makes the event feel real, and a way for 120 to 300 people to say
they are coming to a free event. The guide puts the site first: "As soon
as you have a date and venue, put up a simple website", saying when and
where, who it is for and why come, with the code of conduct, travel basics
and an accessibility section added early
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Your website). It is also what sponsors read to judge whether the event
is credible (same source).

Registration is "needed (if permitted, something like that)" in the
organiser's words (`sources/conversations/2026-10-07--org--conference-vision.md`):
a free event still needs a head count for the room, a waiting list when
the cap is reached, and a list at the door. The organiser's own money is
capped at 1,000 EUR (`sources/conversations/2026-10-07--org--first-answers.md`),
so both surfaces should cost close to nothing.

## Appetite

**Small:** a few evenings for a first version, then steady additions as
the event fills in. The site starts with one page and grows; registration
is configured once and opened when the date and room are signed.

## Solution

### The site

- **Plain HTML pages, no build step.** A handful of pages (home, program,
  travel and stay, accessibility, code of conduct, extensions, sponsors,
  contact) needs no static site generator. Designed with impeccable (see
  [Design with impeccable](design-with-impeccable.md)).
- **Published under muhamed.at, written here.** The organiser chose a
  page on their own site rather than a new domain, with the page sources
  kept and designed in goatconf and "copied into your site when
  published" (`sources/conversations/2026-10-07--org--talks-team-and-site.md`).
  The organiser's site runs on a clone of pi-brain
  (`sources/web/organiser/muhamed-at-about.md`), so the copy follows that
  site's own conventions. This costs nothing and needs no new hosting;
  the pages are published at muhamed.at/goatconf, and their sources sit
  in this repository, which is to be public as well
  (`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
  Each publish is a public act and the organiser's.
- **The hosting and domain options checked before that choice,** kept for
  a later edition that wants its own address. Three free hosts:
  - GitHub Pages serves free accounts from **public** repositories only;
    private repositories need a paid plan, and it is "not intended for or
    allowed to be used as a free web-hosting service to run your online
    business" (`sources/web/web/github-pages-limits.md`). A free,
    non-commercial conference site fits.
  - Cloudflare Pages' free plan allows 500 builds a month and 100 custom
    domains per project (`sources/web/web/cloudflare-pages-limits.md`).
  - Netlify's free plan is metered in credits (15 per production deploy,
    20 per GB of bandwidth, 300 a month), the tightest of the three
    (`sources/web/web/netlify-pricing.md`).
- **A domain, if ever wanted.** A `.com` costs about 10.46 USD a year at Cloudflare's
  at-cost registrar (`sources/web/web/cloudflare-registrar.md`,
  `sources/web/web/cfdomainpricing-com-price.md`, a third-party tracker).
  A `.ba` is local and says where the event is, but its price and rules
  are unclear: a 2021 forum post gives 80 BAM the first year and 30 BAM to
  renew, open to anyone, through local registrars
  (`sources/web/web/namepros-ba-thread-2021.md`); foreign registrars list
  47.50 to 289 USD (`sources/web/web/tldes-ba-registrar-prices.md`); and
  one site says a local presence is required
  (`sources/web/web/domaindetails-ba.md`). Unverified.
- **The extension list is part of the site**, rendered from the extension
  files the umbrella pitch describes, so a new fringe event shows up
  without hand-editing a page.
- **Content order follows the guide:** first when, where, who and why;
  then the code of conduct and travel basics; then the CFP, the sponsor
  page and the program as they exist (guide, § Your website). The trip is
  sold before the lineup: Tuzla, the lake, the low cost (guide, § What
  you are selling).

### Registration

- **pretix, hosted.** Free tickets cost 0.50 EUR each, but "500 free
  tickets per year" are included (`sources/web/tooling/pretix-hosted-pricing.md`),
  so 120 to 300 attendees cost nothing. It has a waiting list and a
  check-in app (`sources/web/tooling/pretix-features.md`), and the guide
  notes Baltic Ruby uses it.
- **Fallbacks:** Tito ("Free events: Free",
  `sources/web/tooling/tito-pricing.md`), the Ruby conference default per
  the guide; Luma ("Free, forever", unlimited guests,
  `sources/web/tooling/luma-pricing.md`); Tally as a plain form with data
  stored in Europe (`sources/web/tooling/tally-pricing.md`).
- **Collect only what the event needs:** a name for the badge, an email,
  and optional questions (dietary needs if a meal is ever sponsored,
  accessibility needs, whether the attendee wants hiring partners to see
  them). This follows FOSDEM's charter line that "attendees are not
  required to submit personal information to attend unless law or safety
  mandate it" (`sources/web/funding/fosdem-charter.md`).
- **Opens when the date is confirmed,** likely November 2026, on the
  organiser's choice
  (`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).
  Seven months is a long time to hold a free place, so registration asks
  people to reconfirm in the spring (one email, one click), releases
  places not reconfirmed to the waiting list, and sends a last reminder
  the week before.
- **A cap matched to the hall, about 120** (the organiser: "I would
  register per hall capacity",
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`),
  with a waiting list, and an
  overbooking margin set from experience of free events, where some
  registrants never come. The margin is (unknown, needs source) until
  measured.

## Rabbit holes

- **Building a custom site or registration system.** Tempting for a
  technical organiser; it costs the evenings the program needs.
- **No-shows at a free event.** A free ticket is easy to take and easy to
  forget. Reminders, and releasing unconfirmed places from the waiting
  list, matter more than the tool.
- **Data protection.** A list of names and emails is personal data under
  Bosnian and EU rules; how the law applies here is for the operations
  pitch (unknown, needs source).
- **A public repository** is the cheapest free hosting route, and it would
  also hold the extension files. Publishing it is a public act and the
  organiser's decision.

## No-gos

- No paid tickets, and no "supporter" upsell in registration.
- No data collected that the event does not use.
- No login or account system on the site.

## Choices made in auto mode

- **pretix over Tito and Luma.** Because its free quota covers the whole
  event, it is a European company, and it has a waiting list and check-in.
  Tito is the stronger habit in the Ruby world, and is the first fallback.
- **Plain HTML over a site generator.** Because a few pages do not need a
  build, and impeccable works on HTML and CSS directly.
- **The extension list is rendered into the pages before they are
  copied.** Because the site lives on muhamed.at, the list cannot be built
  there from goatconf's files; it is built here and copied with the rest.

## Open questions for the organiser

