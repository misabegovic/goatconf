---
title: "Build the pages in plain HTML and CSS, with the goat everywhere and playful"
kind: decision
status: accepted
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/design-with-impeccable.md
sources:
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/web/organiser/muhamed-at-about.md
  - sources/web/funding/euruko-2024-why-the-goat.md
---

# Build the pages in plain HTML and CSS, with the goat everywhere and playful

Answers the "Decision needed" of
[Design with impeccable](../prds/design-with-impeccable.md). Accepted 2026-10-07 from the organiser's answers
(`sources/conversations/2026-10-07--org--adr-answers.md`, questions 5 and
6), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

The site's pages are hand-written HTML and CSS with no build step, kept
in a `site/` folder in this repository and copied into
muhamed.at/goatconf as they are. The one generated part is the extension
list, built from the extension records before a copy. The visual world
puts the goat everywhere and plays with it: in the mark and the favicon,
as illustrations through the pages, on the badges and room signs, on the
social cards and the "I'm attending" image, and in the slide template.
Impeccable's `init` is answered with this stack, and DESIGN.md records
the goat's place in it.

## Why

The organiser chose plain HTML and CSS over the host site's own stack or
a static site generator. With no build step, the copy into muhamed.at is
a copy and nothing more, nothing can break between this repository and
the live site, and a volunteer can fix a typo without installing
anything. Impeccable works on the files directly.

The organiser chose the playful goat over a small mark or a mark and a
story. The goat is the name's whole story: the Tuzla saying "The whole of
Tuzla milked one goat" and the man who hid his goat
(`sources/web/funding/euruko-2024-why-the-goat.md`). A playful goat on
every surface makes GoatConf recognisable at a glance and gives people
something they want to share.

## How

DESIGN.md names the goat's forms (the mark, a few poses, the patterns it
can make) and the rules that keep play from turning into noise: the
goat never covers the when, where and how to register, never stands in
for text a screen reader needs, and never appears beside the code of
conduct or the budget ledger in a way that makes them read as a joke.
The host kit carries the same goat so extension hosts can use it.

The pages live inside muhamed.at, which runs on a clone of pi-brain
(`sources/web/organiser/muhamed-at-about.md`), under the path the
organiser chose (`sources/conversations/2026-10-07--org--talks-team-and-site.md`).
Whether that site serves a folder of plain HTML as it is, or needs the
pages wrapped in its own layout, is (unknown, needs source) and is the
first thing to check before the first copy.

## Alternatives

- **Plain HTML and CSS** *(chosen)*: no build, no breakage, easy copying.
- **Whatever muhamed.at uses:** native to the host, at the cost of tying
  GoatConf's pages to that site's tooling.
- **A static site generator:** Markdown sources and templates, with a
  build step to install and maintain.
- **The goat as a mark and a short story, or a mark only:** quieter and
  safer, and less of what the organiser wants GoatConf to feel like.

## Consequences

- **Opens:** a site anyone can edit, and a look that carries onto every
  printed and shared thing.
- **Costs:** shared parts (the header, the footer) are repeated in each
  page by hand; the page count stays small enough for that.
- **Costs:** illustrations take design time; impeccable's asset step and
  the host kit carry them, and none is paid for from the 1,000 EUR
  without a line on the ledger.
- **Closes:** content managed outside this repository.

## Linked PRD

[Design with impeccable](../prds/design-with-impeccable.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-12, the mark is the seal with the EuRuKo 2024 goat.** The organiser chose a round seal as GoatConf's mark: the EuRuKo 2024 goat, unchanged, in a coin at the centre; a band of the site's hoof prints around it for the community; THE ONE THAT FEEDS THE COMMUNITY across the top of the ring and GOATCONF · 2027 along the bottom; blue and yellow. Below about 64 pixels the small form, the goat in a disc, stands in. Every brand file is built from one source by `files/tools/brand.py` into `site/brand/`, and the site's brand page offers them for download. The goat remains everywhere as the ADR asks; the sticker goat drawing stays on the site until the site rework (source: sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md).
- **2026-10-12.** The site is published on goatconf.com from this repository, not copied into muhamed.at. See [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
