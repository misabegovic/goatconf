---
title: "Build the pages in plain HTML and CSS, with the goat everywhere and playful"
kind: decision
status: accepted
updated: 2026-11-21
confidence: medium
depends_on:
  - org/prds/design-with-impeccable.md
sources:
  - sources/conversations/2026-11-21--org--continue-iterating-round-four.md
  - sources/conversations/2026-11-21--org--continue-iterating.md
  - sources/conversations/2026-11-21--org--keep-iterating.md
  - sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md
  - sources/conversations/2026-10-27--org--goat-mascot.md
  - sources/conversations/2026-10-27--org--sticker-packs.md
  - sources/conversations/2026-10-27--org--still-stickers.md
  - sources/conversations/2026-10-26--org--matte-stickers.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
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
- **2026-10-13, no budget page.** The budget is private, so the site has no budget page and no ledger, and the mentions of the budget ledger above no longer hold. The rule that the goat never makes the code of conduct read as a joke stands (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
- **2026-10-26, matte stickers.** The stickers lose their diagonal gloss and every shadow gets shorter and lighter (stickers, number pills, album pages, the spread, buttons, the seal), so the album reads as paper rather than glossy app cards; DESIGN.md's Gloss Rule becomes the Matte Rule (source: sources/conversations/2026-10-26--org--matte-stickers.md).
- **2026-10-27, still stickers.** The stickers no longer peel and settle as they come into view; the organiser found it annoying. They keep their tilt and sit still from the first paint (source: sources/conversations/2026-10-27--org--still-stickers.md).
- **2026-10-27, the goat mascot and the stickers.** A second goat joins the mark: a flat, cute mascot drawn in code, in roles from the EuRuKo 2024 goat multiverse, peeking over the open slots and the speaker cards, and each speaker's own goat drawn from their photo; the faint ghost goat is retired, and DESIGN.md's rule against a second goat drawing now allows the mascot. The same drawings make the sticker packs on the Stickers page. See [the goat mascot](goat-mascot.md) and [the sticker packs](sticker-packs.md) (sources: sources/conversations/2026-10-27--org--goat-mascot.md, sources/conversations/2026-10-27--org--sticker-packs.md).
- **2026-11-21, the album keeps its own rules.** Decided on the local branch `site/phone-first-and-one-ask` and pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md). The stamp red darkens from #e30613 to #c80510, so the "Yours?" lettering is at least 4.5:1 on the slot fill (5.4:1 measured, from 4.35:1). The slot line rises from 42% to 60% album blue, so the dashed outline is at least 3:1 against the slot fill (3.3:1, from 2.2:1). The six fact stickers on the home page that had no number get one, through the same pass in `tools/home.py` that numbers the rest. A focused button shows a night-blue ring and a yellow ring outside its white die-cut edge, visible on the blue cover and on white. The cover's three links are at least 44 pixels tall on a phone. The gap between a band's intro line and its first row closes where no goat peeks over that row. DESIGN.md says, as an exception to the Yellow Means Stuck Rule, that a button is the one yellow fill that is not a number or a fact, and it no longer says both "two across on phones" and "one after another": the lists a visitor reads go one after another on phones, as the organiser chose in October.
- **2026-11-21, round two: the album's grammar on the closing page, the statue, the unannounced session and the session sticker.** Second round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--keep-iterating.md). The closing page letters its dates and place and gives the waving goat room; "Why a goat" closes on a photo sticker of the statue; a session not yet announced is an empty printed slot inside a stuck speaker card, with no stamp; an announced session on a speaker's page is a fact-coloured sticker; the footer's links sit in four groups under small lettered labels. DESIGN.md records each, and its Layout section says how far the phone's vertical rhythm closes.
- **2026-11-21, round three: tighter compositions, and the sticker felt under the pointer.** Third round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--continue-iterating.md). DESIGN.md records: the closing page as one row; the session slot one line tall at the card's foot; the statue as a small photo sticker beside its sentence; the back cover's groups in one row; the page-head photo as a corner sticker on phones; a button that lifts when pointed at and presses flat when pressed, with no movement under reduced motion; the unprinted-sticker placeholder under a loading photo; the caret and scrollbars in the album's colours. Stickers still do not animate as they come into view (source: sources/conversations/2026-10-27--org--still-stickers.md).
- **2026-11-21, round four: the statue and the seal share a column, a place as a compact row.** Fourth round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--continue-iterating-round-four.md). DESIGN.md records the shiny page's left column (the seal with the statue photo sticker overlapping its lower corner and the sentence beside the photo), the head without a picture, the open rooms as small drawn slots in one printed box, and the place row on a phone. The question of how much blue the site uses is answered on two variant branches, each with its own amendment.
- **2026-11-21, less blue, calm.** Variant branch `site/less-blue-calm`, one of two built for the organiser to choose between by eye; pending approval, nothing published. The page ground is the pale slot tint (page-print), printed with hoof marks in album blue at 5%, in place of the saturated album blue. Blue stays where it marks the album as GoatConf's: the top bar, the band across each album page, the cover and the page heads, the photo stickers' captions, the one night-blue goat-story page and the back cover. It leaves the fact stickers, the ticket and the session sticker, which become white stickers with a 2px album-blue keyline, album-blue lettering and ink text; their numbers stay yellow. Yellow stays the one bright signal (numbers, buttons, the rule under a band, the year); red stays on stamps. It moves past three earlier decisions, which stay on the work branch until the organiser chooses: the Korzo walk becoming the sticker album on an album-blue ground (sources/conversations/2026-10-12--org--site-rework-approved.md and DESIGN.md's Album Blue as "the ground of the whole site"), the fact sticker as an album-blue sticker with yellow lettering, and the yellow focus ring on the blue ground. The share cards (`tools/shareables.py`) and the brand files (`tools/brand.py`) are not rendered again here; they follow the chosen look as the next step, once the organiser has chosen between the variants, and until then they differ from the site. Measures: the blue share of the whole page, counted on full-page screenshots of the home, program, register, speakers and one speaker page as pixels with a hue of 200 to 250 degrees and over 30% saturation, is at most a third at 1440 and at 390 wide (it was 31% to 61%); every text and ground pair passes 4.5:1, or 3:1 for large lettering; a focus ring shows on every ground (album blue on paper and white, yellow on the blues); no page is taller than on the work branch. (source: sources/conversations/2026-11-21--org--continue-iterating-round-four.md).
