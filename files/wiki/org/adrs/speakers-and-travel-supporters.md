---
title: "Speaker profiles and travel supporters: consented records, a speakers page and a supporters wall"
kind: decision
status: accepted
updated: 2026-10-13
confidence: medium
depends_on:
  - org/prds/cfp-and-speakers.md
  - org/prds/supporters-and-hiring.md
sources:
  - sources/conversations/2026-10-13--org--speaker-profile-required.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--speakers-and-supporters-approved.md
  - sources/conversations/2026-10-12--org--google-forms-built-and-published.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
---

# Speaker profiles and travel supporters: consented records, a speakers page and a supporters wall

Accepted 2026-10-12 by the organiser
(`sources/conversations/2026-10-12--org--speakers-and-supporters-approved.md`).

## What

goatconf.com gets a speakers page and a supporters page. Each speaker with an
accepted session who agrees to a public profile has one record in
`files/speakers/`: name, a bio in their own words, an optional photo and
links, and the supporter who paid their travel, if any. Each company that
pays a named thing, starting with speakers' travel, has one record in
`files/supporters/`: name, logo, link and exactly what it funds. The
supporters page shows every supporter's logo together; a speaker's profile
also shows the logo of the supporter who paid their travel. Sessions on the
program link to their speakers' profiles. A speaker without a photo gets the
goat in its place (source: sources/conversations/2026-10-12--org--speakers-and-supporters-approved.md).

## Why

The organiser asked for a place for speaker profiles and for the logos of
companies that sponsor speakers' travel (source:
sources/conversations/2026-10-12--org--speakers-and-supporters-approved.md).
Speakers pay their own travel unless a supporter covers it, and no money
passes through the organiser (source:
sources/conversations/2026-10-07--org--no-money-through-me.md), so a
company paying a ticket or room straight to the supplier is the natural
first thing to thank in public. The repository is public (source:
sources/conversations/2026-10-07--org--goatconf-will-be-public.md), so a
profile goes up only with the speaker's consent.

## How

- The records are Markdown with frontmatter, like the program and the
  extensions. `files/tools/speakers.py` checks them and builds
  `site/speakers.html` and `site/supporters.html`; the local CI runs both.
- The check refuses a speaker record without `publish: yes`, a bio over 120
  words, a photo or logo that is not in the site's image folders, and a
  `travel_funded_by` that names no supporter record.
- A session links to profiles with `profiles: [slug]`; the program shows
  the plain names when no published profile exists.
- The talk form asks for a short bio and whether a profile may be published
  if the session is accepted; the photo comes later by email (source:
  sources/conversations/2026-10-12--org--google-forms-built-and-published.md).
- Every supporter payment is still a line in the public ledger; the budget
  and add pages point to the supporters page.

## Alternatives

- **Logos only beside the travel they funded, with no wall.** Closer to the
  pitch's "supporters, not tiers of logos", but less visible to companies
  deciding whether to fund; the organiser chose the wall.
- **Profiles only, logos later.** Simpler now, but leaves sponsors of travel
  with nothing to point to.
- **No photos.** Nothing to collect or store; the organiser chose optional
  photos with the goat as the default.

## Consequences

- Accepted speakers' names, bios and photos become public, and only with
  consent; proposals, rejected speakers and reviewer notes still never enter
  the repository.
- A supporters wall shows logos together; the charter still holds that a
  supporter is thanked for exactly what they funded and buys no content, so
  each logo carries its `funds` line.
- Two more record folders and a generator to keep current; the local CI
  guards them.

## Related

- [The call for talks and speakers](../prds/cfp-and-speakers.md)
- [Supporters and hiring](../prds/supporters-and-hiring.md)
- [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md)
- [Program: every room open](open-program-every-room.md)

## Amendments
- **2026-10-13, online supporters and no travel per speaker.** Supporters are online only: one level, 500 EUR, paid to the organiser's Austrian business, or a supplier paid directly. No supporter pays for a named speaker's travel; `travel_funded_by` is retired and the check refuses it. Speakers pay their own travel, refunded only if the budget allows, never promised ([Online supporters pay the organiser's Austrian business](online-supporters-through-the-business.md); source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
