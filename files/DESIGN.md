---
name: GoatConf
description: A free conference in Tuzla, told as a sticker album where decided facts are stuck in and everything undecided waits as an empty printed slot.
colors:
  album: "#0b3d91"
  album-deep: "#072a66"
  album-night: "#051d47"
  album-soft: "#c9d7f5"
  page: "#ffffff"
  page-print: "#edf2fb"
  slot-line: "rgb(11 61 145 / 0.42)"
  ink: "#12204a"
  ink-soft: "#46557a"
  yellow: "#ffd400"
  red: "#e30613"
  veg-tint: "#d9f2df"
  veg-ink: "#0f4d24"
typography:
  display:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(3.6rem, 2rem + 7vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.86
    letterSpacing: "0.005em"
    fontVariation: "'wdth' 75"
  headline:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(2.1rem, 1.4rem + 3vw, 3.75rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "0.005em"
    fontVariation: "'wdth' 78"
  fact:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(2.2rem, 1.5rem + 2.5vw, 3.4rem)"
    fontWeight: 800
    lineHeight: 0.9
    fontFeature: "'tnum' 1"
    fontVariation: "'wdth' 75"
  title:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(1.7rem, 1.3rem + 1.4vw, 2.4rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "0.005em"
    fontVariation: "'wdth' 78"
  lede:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(1.3rem, 1.1rem + 0.8vw, 1.75rem)"
    fontWeight: 700
    lineHeight: 1.2
    fontVariation: "'wdth' 88"
  label:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 800
    lineHeight: 1.05
    fontVariation: "'wdth' 80"
  nav:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 700
    letterSpacing: "0.03em"
    fontVariation: "'wdth' 85"
  body:
    fontFamily: "Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "clamp(1.0625rem, 0.98rem + 0.3vw, 1.1875rem)"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "0.98rem"
    fontWeight: 400
    lineHeight: 1.35
  credit:
    fontFamily: "Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 400
    lineHeight: 1.45
rounded:
  photo-inner: "0.35rem"
  button: "0.45rem"
  sticker: "0.6rem"
  page: "0.8rem"
  pill: "1.05rem"
  round: "50%"
spacing:
  pad: "clamp(1.1rem, 4vw, 3.5rem)"
  space: "clamp(2.5rem, 1.8rem + 3vw, 5rem)"
  page-inset: "clamp(1.25rem, 3.5vw, 3rem)"
  die-cut: "0.42rem"
  slot-gap: "1.6rem 1.3rem"
  slot-gap-phone: "1.2rem 0.9rem"
  wrap-max: "82rem"
  prose-max: "58rem"
components:
  sticker-photo:
    backgroundColor: "{colors.page}"
    rounded: "{rounded.sticker}"
    padding: "{spacing.die-cut}"
  sticker-photo-caption:
    backgroundColor: "{colors.album}"
    textColor: "{colors.page}"
    typography: "{typography.label}"
    padding: "0.45rem 0.6rem 0.5rem"
  sticker-place-caption:
    backgroundColor: "{colors.album}"
    textColor: "{colors.yellow}"
    padding: "0.6rem 0.6rem 0.55rem"
  sticker-fact:
    backgroundColor: "{colors.album}"
    textColor: "{colors.yellow}"
    typography: "{typography.fact}"
    rounded: "{rounded.sticker}"
    padding: "1.2rem 1.1rem"
  slot:
    backgroundColor: "{colors.page-print}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sticker}"
    padding: "1.1rem 1.1rem 1.2rem"
    height: "9rem"
  number-stuck:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.album-night}"
    rounded: "{rounded.pill}"
    height: "2.1rem"
    width: "2.1rem"
  number-printed:
    backgroundColor: "{colors.page-print}"
    textColor: "{colors.album}"
    rounded: "{rounded.pill}"
    height: "2.1rem"
    width: "2.1rem"
  stamp-yours:
    textColor: "{colors.red}"
    rounded: "{rounded.photo-inner}"
    padding: "0.05em 0.45em"
  status-sticker:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.album-night}"
    rounded: "{rounded.button}"
    padding: "0.8em 1.15em"
  band:
    backgroundColor: "{colors.album}"
    textColor: "{colors.page}"
    typography: "{typography.headline}"
    padding: "1.1rem clamp(1.25rem, 3.5vw, 3rem) 1rem"
  album-page:
    backgroundColor: "{colors.page}"
    textColor: "{colors.ink}"
    rounded: "{rounded.page}"
    padding: "0 clamp(1.25rem, 3.5vw, 3rem) clamp(1.75rem, 3.5vw, 3rem)"
  spread-cover:
    backgroundColor: "{colors.album-deep}"
    textColor: "{colors.page}"
    padding: "clamp(1.5rem, 3.5vw, 3.25rem)"
  spread-page:
    backgroundColor: "{colors.page}"
    textColor: "{colors.ink}"
    padding: "clamp(1.5rem, 3.5vw, 3rem)"
  shiny-page:
    backgroundColor: "{colors.album-night}"
    textColor: "{colors.page}"
    rounded: "{rounded.page}"
    padding: "clamp(1.75rem, 4vw, 3.5rem)"
  topbar:
    backgroundColor: "{colors.album-night}"
    textColor: "{colors.page}"
    typography: "{typography.nav}"
    padding: "0.6rem clamp(1.1rem, 4vw, 3.5rem)"
  back-cover:
    backgroundColor: "{colors.album-night}"
    textColor: "{colors.album-soft}"
    padding: "3rem 0 3.5rem"
  page-head:
    backgroundColor: "{colors.album-deep}"
    textColor: "{colors.page}"
    rounded: "{rounded.page}"
    padding: "clamp(1.5rem, 4vw, 3rem)"
  prose-page:
    backgroundColor: "{colors.page}"
    textColor: "{colors.ink}"
    rounded: "{rounded.page}"
    padding: "clamp(1.5rem, 4vw, 3.25rem)"
    width: "58rem"
  tag:
    backgroundColor: "{colors.page-print}"
    textColor: "{colors.ink}"
    rounded: "1rem"
    padding: "0.1rem 0.5rem"
  tag-veg:
    backgroundColor: "{colors.veg-tint}"
    textColor: "{colors.veg-ink}"
    rounded: "1rem"
    padding: "0.1rem 0.5rem"
---

# Design System: GoatConf

## Overview

**Creative North Star: "The Sticker Album"**

GoatConf is a sticker album opened flat on an album-blue ground. The organiser sticks in the core facts as glossy die-cut stickers; every other numbered slot is printed empty on the white page and waits for whoever brings a talk, a workshop or a walk. The album is the whole site: a blue ground printed with faint cloven-hoof marks, white album pages with rounded corners, a blue band across the top of each page, a numbered sequence that runs through the whole album, a night-blue "shiny" page for the goat story, and a night-blue back cover.

The material is printed paper and vinyl, not screen chrome. Stickers have a white die-cut border, a soft lift off the page and a diagonal gloss; empty slots are flat, dashed and printed in the album's own blue at low strength, each with a faint goat silhouette and a printed number. Hierarchy comes from scale contrast in condensed uppercase lettering, not from weight changes or colour noise. The goat itself appears once per spread as a die-cut yellow sticker with a white edge.

The world refuses the dark tech-conference hero with a speaker grid. It also refuses to pretend: what is decided is stuck in, what is undecided stays an empty printed slot, and nothing is announced as a sticker before it is true.

**Key Characteristics:**
- Album-blue ground with a faint hoof-print pattern; white pages float on it with rounded corners and a soft drop.
- Two states of every fact: a stuck-in sticker (decided) or an empty printed slot (undecided or open to you).
- One numbered sequence across the album, yellow on stickers, printed on slots.
- Condensed uppercase Bricolage lettering at strong scale contrast; Atkinson Hyperlegible Next for reading.
- Stickers peel and settle once as they enter view; reduced motion shows them already stuck.

## The mark

GoatConf's mark is a round seal: the EuRuKo 2024 goat in a coin at the centre, a band of the site's cloven hoof prints around it (the community that comes to the one goat), THE ONE THAT FEEDS THE COMMUNITY across the top of the ring and GOATCONF · 2027 along the bottom, set in Bricolage Grotesque, extra bold, 75% width. It is blue on yellow or yellow on blue; in one colour, any palette colour or black. Below about 64 pixels the small form, the goat in a disc, stands in for it; it is also the favicon and the home-screen icon. The wordmark is GOATCONF in the same face, beside the small form (horizontal) or stacked as GOAT / CONF beside the seal with the line "The one that feeds the community." Every file is built by `tools/brand.py` into `site/brand/` and offered on `brand.html`.

## Colors

A saturated album blue in three depths, white and a pale printed blue for the pages, and two signal colours that each own a narrow job.

### Primary
- **Album Blue** (album): the ground of the whole site, behind everything, printed with the hoof pattern at 6% white. Also the album-page band, the fact-sticker body, photo-sticker captions, page titles and in-page links on white.
- **Cover Blue** (album-deep): the album cover. The left page of the opening spread and the page-head strip on every inner page.
- **Night Blue** (album-night): the darkest binding. The sticky top bar, the shiny goat-story page and the back cover; also the ink on yellow surfaces.

### Secondary
- **Signal Yellow** (yellow): numbers, the big facts and the status. Stuck-in sticker numbers, fact-sticker figures, the place-sticker caption (TUZLA), the registration status sticker, the year in the mark, and the shiny page title. It also carries the album's printed trim: the rule under every band, link underlines on blue, the crest disc and the focus ring on blue.

### Tertiary
- **Stamp Red** (red): the "Yours?" stamp and nothing else. It is set with a multiply blend so it reads as ink pressed onto the printed slot.

### Neutral
- **Page White** (page): album pages, the right page of the spread, the prose page, and every sticker's die-cut border.
- **Page Print** (page-print): the flat fill of an empty printed slot, the default tag, and the image placeholder under a loading photo.
- **Slot Line** (slot-line): album blue at 42%. Dashed slot outlines, the ring of a printed number, the ghost goat, the name line in a slot and the dotted leaders of the price list.
- **Album Ink** (ink): body text on white pages.
- **Soft Ink** (ink-soft): slot explanations and "last checked" notes on white.
- **Pale Album** (album-soft): secondary text on the blues (cover sub-line, fact-sticker explanations, back cover, inner-page lede).
- **Vegan Tint and Ink** (veg-tint, veg-ink): only the "vegan" tag on food stickers, so the vegan marker reads at a glance without borrowing the signal colours.

### Named Rules
**The Red Stamp Rule.** Red appears only as the "Yours?" stamp on an empty slot. It never marks an error, a price, a link or a heading.

**The Yellow Means Stuck Rule.** Yellow fills only things that are decided or numbered: a stuck-in number, a fact, the status. An empty slot never carries a yellow fill; its number is printed in blue.

## Typography

**Display Font:** Bricolage Grotesque, self-hosted as a variable font with a width axis (75% to 100%), falling back to Atkinson Hyperlegible Next
**Body Font:** Atkinson Hyperlegible Next, self-hosted, falling back to system-ui

**Character:** The lettering is the album's printed type: Bricolage at weight 800, condensed (width 75% to 85%), always uppercase, set tight. Atkinson Hyperlegible Next carries every sentence a visitor actually reads, at a generous size and 1.6 leading.

### Hierarchy
- **Display** (800, width 75%, clamp(3.6rem, 2rem + 7vw, 6rem), 0.86; 3.4rem on phones): the cover title, GOATCONF over a yellow 2027. Once per site.
- **Headline** (800, width 78%, clamp(2.1rem, 1.4rem + 3vw, 3.75rem), 0.95): the band across each album page, the shiny page title, the inner-page sign.
- **Fact** (800, width 75%, clamp(2.2rem, 1.5rem + 2.5vw, 3.4rem), 0.9, tabular figures; 2.2rem on phones): the yellow figure on a fact sticker (FREE, JUNE 2027, 0.00 €). The place-sticker caption (TUZLA) is lettered in yellow at this same scale.
- **Title** (800, width 78%, clamp(1.7rem, 1.3rem + 1.4vw, 2.4rem), 0.95): the spread's page title and prose-page headings (clamp(1.5rem, 1.2rem + 1.2vw, 2.1rem)); section sub-heads on album pages are 1.5rem.
- **Lede** (700, width 88%, clamp(1.3rem, 1.1rem + 0.8vw, 1.75rem), 1.2): the cover lede and the inner-page lede, in display lettering but sentence case.
- **Label** (800, width 80%, 1.15rem, 1.05, uppercase; 1rem on phones): photo-sticker captions, slot titles (1.5rem), stamps (1.05rem), printed and stuck numbers (1.05rem), prices (1.6rem, tabular).
- **Nav** (700, width 85%, 0.95rem, 0.03em, uppercase): the top-bar links.
- **Body** (400, clamp(1.0625rem, 0.98rem + 0.3vw, 1.1875rem), 1.6): all running text, held to 62ch (74ch on wide copy, 58ch on the shiny page).
- **Small / Credit** (400, 0.98rem at 1.35; 0.82rem at 1.45): slot and fact explanations; checked dates.

### Named Rules
**The Lettered, Not Typed Rule.** Every heading, caption, number and stamp is Bricolage at 800, condensed and uppercase. Weight never varies to make hierarchy; size does.

**The Reading Face Rule.** Any sentence longer than a label is Atkinson Hyperlegible Next, never the display face.

## Layout

The site is a column of album pages on the blue ground, each at most 82rem wide with a side margin of clamp(1.1rem, 4vw, 3.5rem), separated by clamp(2.5rem, 1.8rem + 3vw, 5rem). The opening spread is two pages in one rounded frame (0.9fr cover, 1.1fr page) that stack on screens under 62rem with the spine shadow turning horizontal. Album pages run a two-column grid (1fr copy, 1.2fr stickers) that collapses to one column under 62rem.

Slots and stickers sit in auto-filling grids (minimum 12.5rem per cell, gap 1.6rem by 1.3rem). The opening page is a fixed three-by-two grid; the food page three across; the add-your-own page four across. Under 48rem every slot grid becomes two across with a 1.2rem by 0.9rem gap, so stickers stay sticker-sized on phones rather than going full width. The top bar is sticky; under 48rem its links move to their own row and scroll sideways rather than wrap.

Inner pages share one shape: a cover-blue page-head (sign, lede, a tilted photo sticker on the right, stacked under 62rem) followed by one white prose page, 58rem at most, and a plain footer on the blue.

## Elevation & Depth

Depth is physical: paper pages cast a long soft drop onto the blue, stickers lift a little off the page, and the spread has a spine. Nothing is flat-shadowed by default except the empty slots, which are printed and therefore sit in the page.

### Shadow Vocabulary
- **Sticker lift** (`box-shadow: 0 0.7rem 1.2rem -0.6rem rgb(0 0 0 / 0.55), 0 0 0 1px rgb(0 0 0 / 0.08)`): every stuck sticker at rest, and the inner-page photo sticker.
- **Peel lift** (`box-shadow: 0 1.6rem 2.2rem -1rem rgb(0 0 0 / 0.6), 0 0 0 1px rgb(0 0 0 / 0.08)`): a sticker held off the page before it settles.
- **Page drop** (`box-shadow: 0 2rem 3rem -2rem rgb(0 0 0 / 0.55)`): album pages and the prose page on the blue ground. The spread uses a deeper drop (`0 2.5rem 4rem -2rem rgb(0 0 0 / 0.6)`).
- **Spine** (`box-shadow: inset -1.4rem 0 1.6rem -1.2rem rgb(0 0 0 / 0.55)` on the cover, `inset 1.4rem 0 1.6rem -1.2rem rgb(0 0 0 / 0.25)` on the page): the fold between the spread's two pages.
- **Number lift** (`box-shadow: 0 0.3rem 0.6rem -0.3rem rgb(0 0 0 / 0.6)`): the small yellow number sticker on a stuck sticker.
- **Goat lift** (`filter: drop-shadow(0 0.7rem 0.6rem rgb(0 0 0 / 0.45))`): under the die-cut goat, after its white edge.

### Named Rules
**The Printed Is Flat Rule.** An empty slot, a printed number, the ghost goat and the stamp have no shadow. Only things stuck onto the page lift.

**The Gloss Rule.** Every sticker carries the same diagonal gloss, a 115-degree white sheen (40% at the top-left corner, clear through the middle, 18% at the far corner). Printed parts of the page never do.

## Shapes

Corners are soft and consistent: pages and the spread at 0.8rem, stickers and slots at 0.6rem, the photo inside a sticker at 0.35rem so the white die-cut border keeps an even width (0.42rem) all round. Numbers are pill-shaped stickers (1.05rem radius); the crest and the status dot are circles. The stamp is a 3px rectangle with 0.35rem corners, rotated -9 degrees.

Stickers are set at small individual tilts between -2 and 2 degrees, set per sticker; the inner-page photo sticker sits at 2 degrees and the goat at -6. Album pages clip to their rounded corners so the blue band runs edge to edge without a seam. Borders exist only as print: the dashed slot outline, the dotted price leader, the solid name line and the yellow rule under each band.

## Components

### Sticker
Glossy vinyl stuck onto the page: white die-cut border, sticker lift, diagonal gloss, a small tilt.
- **Photo sticker:** a 4:5 photo (4:3.4 on album pages, 4:3.2 on the food page) over an album-blue caption strip lettered in white.
- **Place sticker:** a photo sticker whose caption is a place name lettered in yellow at near fact scale (TUZLA).
- **Fact sticker:** an album-blue sticker whose white die-cut border is drawn inset; a big yellow fact over a short pale-album explanation.
- **Tag:** a small pill under a food sticker's caption: page-print by default, the vegan tint for vegan dishes.

### Printed Slot
The empty place in the album: page-print fill, a 2px dashed slot-line outline, 0.6rem corners, at least 9rem tall. It carries a printed number at the top, a faint ghost goat in the top-right corner (slot-line, 70%), a blue lettered title and a soft-ink explanation. Open slots add the red "Yours?" stamp at the bottom right; slots for things a host will add carry a printed name line instead of an explanation.

### Numbered Sequence
One run of numbers through the whole album, so a reader can see the gaps. On a stuck sticker the number is a yellow pill sticker overlapping the top-left corner with its own lift; on an empty slot the same number is printed in place: no fill, album-blue figure, a 2px slot-line ring.

### Album Page and Band
A white page with 0.8rem corners and the page drop. Its heading is the band: album blue, white headline lettering, a 0.45rem yellow rule beneath, running edge to edge across the top of the page.

### Spread
The opening: one rounded frame holding the cover-blue left page (the goat sticker, the cover title, the lede, the yellow status sticker and two links) and the white right page ("Stuck in so far": four stickers and two slots), joined by the spine shadow.

### Die-cut Goat
The one goat mark as a sticker: night-blue line drawing with a yellow fill, a 3px white edge cut around the silhouette, the goat lift, set at -6 degrees. It appears on the cover and, larger, on the shiny page. The mini crest (a yellow disc with the goat) marks the top bar, the back cover and the inner-page home link.

### Status Sticker
The registration status: a yellow pill-cornered sticker (0.45rem) with a night-blue dot and night-blue lettering. It states what is true now, never a date that is not confirmed.

### Price List
Item, a dotted slot-line leader, and the price lettered in album blue at 1.6rem with tabular figures. Followed by a soft-ink "last checked" line.

### Shiny Page
The one solid beat: a night-blue page with a white die-cut border drawn inset (0.42rem), the big goat on the left, the yellow title and the saying lettered in white on the right.

### Navigation
The top bar is night blue and sticky: the mini crest and GOATCONF with a yellow 2027 on the left, uppercase condensed links on the right that turn yellow on hover. Links in running text are underlined in yellow on blue and in album blue on white, thickening from 2px to 4px on hover. Focus is a 3px yellow ring on blue and a 3px album-blue ring on white pages. The "go" link (a larger lettered link, 750 weight) leads each page's call to action.

### Back Cover
The footer as the album's back cover: night blue, the crest and mark in white, pale-album text, white links.

### Inner Page-head and Prose Page
Every inner page opens on a cover-blue strip: the crest home link, the sign in headline lettering, a pale-album lede, and a photo set as a sticker (white border, lift, 2 degrees). Below it, one white prose page at most 58rem wide, headings lettered in album blue, list markers in album blue, an album-blue table head on the budget ledger, and a printed-slot style empty state when a list has nothing yet.

### Motion
**Peel and settle.** On the album, each sticker starts lifted (rotated 7 degrees further, shifted 0.6rem right and 0.9rem up, scaled 1.04, peel lift) and settles once into its slot when 35% of it is in view, over 900ms on `cubic-bezier(0.16, 1, 0.3, 1)`, staggered 120ms plus 90ms per sticker. The peeled start is set by a one-line script in the head before first paint, only when motion is allowed and IntersectionObserver exists, so a sticker never flashes stuck and then jumps. Without the script, or with reduced motion, every sticker is simply stuck. A settled sticker never peels again.

**Goat wiggle.** On hover the die-cut goat turns from -6 to 4 degrees and grows 5% over 500ms on the same curve; reduced motion holds it still.

## Do's and Don'ts

### Do:
- **Do** show a decided fact as a stuck-in sticker and an undecided or open one as an empty printed slot, with its reason in the slot's explanation.
- **Do** give every sticker and slot the next number in the album's single sequence.
- **Do** keep stickers sticker-sized: two across on phones, never full-width cards.
- **Do** set a small per-sticker tilt between -2 and 2 degrees, and vary it between neighbours.
- **Do not** print photo credits on the site; the organiser decided on 2026-10-12 to show no credits (`sources/conversations/2026-10-12--org--no-photo-credits.md`).
- **Do** write plain sentences: one idea per sentence, common words, and no em dashes anywhere, including captions, alt text and generated pages.

### Don't:
- **Don't** use red for anything but the "Yours?" stamp.
- **Don't** put a fact on a sticker before it is true: an unconfirmed date stays "June 2027" on the fact sticker and an empty slot for the exact days.
- **Don't** give printed things (slots, printed numbers, ghost goats, stamps) a lift or gloss, or stuck stickers a dashed outline.
- **Don't** write self-aware copy about the album, the design or the site itself; the page talks about the conference, Tuzla and the visitor.
- **Don't** add small labels above headings, glyph icons, or a second goat drawing; the band, the numbers and the one goat mark carry the page.
- **Don't** let the goat cover a fact, stand in for text a screen reader needs, or appear on the code of conduct or budget content as a joke.

### Sanctioned detector exceptions
The detector exceptions in `.impeccable/config.json` that this world relies on:
- **nested-cards** on `site/index.html`: stickers and printed slots stuck on album pages are the album's grammar, sanctioned by the finish review of 2026-10-12.
- **clipped-overflow-container** on `site/*.html`: album pages clip to their rounded corners so the band has no seam; nothing positioned leaves the page padding.

Three older entries are inherited from the Korzo world and are now obsolete: **cream-palette** (it cites the retired Afternoon Stone page colour; the pages are now white and the ground album blue), and **tight-leading** and **cramped-padding** on `site/index.html` (their reasons cite Korzo type values and the `.hero__sign` and `.stop` elements, which no longer exist). They were removed from the config on 2026-10-14.
