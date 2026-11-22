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
  slot-line: "rgb(11 61 145 / 0.6)"
  ink: "#12204a"
  ink-soft: "#46557a"
  yellow: "#ffd400"
  red: "#c80510"
  veg-tint: "#d9f2df"
  veg-ink: "#0f4d24"
typography:
  display:
    fontFamily: "Bricolage Grotesque, Atkinson Hyperlegible Next, sans-serif"
    fontSize: "clamp(2.8rem, 0.8rem + 4.4vw, 5rem)"
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
  button:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.album-night}"
    rounded: "{rounded.button}"
    padding: "0.75em 1.3em"
  ticket:
    backgroundColor: "{colors.album}"
    textColor: "{colors.page}"
    rounded: "{rounded.sticker}"
    padding: "{spacing.die-cut}"
  status-sticker:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.album-night}"
    rounded: "{rounded.button}"
    padding: "0.8em 1.15em"
  band:
    backgroundColor: "{colors.album}"
    textColor: "{colors.page}"
    typography: "{typography.headline}"
    padding: "1.1rem calc(clamp(1.25rem, 3.5vw, 3rem) - 0.42rem) 1rem"
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

GoatConf is a sticker album opened flat on an album-blue ground. The organiser sticks in the core facts as matte die-cut stickers; every other numbered slot is printed empty on the white page and waits for whoever brings a talk, a workshop or a walk. The album is the whole site: a blue ground printed with faint cloven-hoof marks, white album pages with rounded corners, a blue band across the top of each page inside a thin white edge, a numbered sequence that runs through the whole album, a night-blue "shiny" page for the goat story, and a night-blue back cover.

The material is printed paper and vinyl, not screen chrome. Stickers have a white die-cut border and a short, light lift off the page, with no gloss; empty slots are flat, dashed and printed in the album's own blue at low strength, each with a faint goat silhouette and a printed number. Hierarchy comes from scale contrast in condensed uppercase lettering, not from weight changes or colour noise. The goat itself appears once per spread as a die-cut yellow sticker with a white edge.

The world refuses the dark tech-conference hero with a speaker grid. It also refuses to pretend: what is decided is stuck in, what is undecided stays an empty printed slot, and nothing is announced as a sticker before it is true.

**Key Characteristics:**
- Album-blue ground with a faint hoof-print pattern; white pages float on it with rounded corners and a soft drop.
- Two states of every fact: a stuck-in sticker (decided) or an empty printed slot (undecided or open to you).
- One numbered sequence across the album, yellow on stickers, printed on slots.
- Condensed uppercase Bricolage lettering at strong scale contrast; Atkinson Hyperlegible Next for reading.
- Stickers sit still in their slots, tilted, with no entrance animation.

## The mark

GoatConf's mark is a round seal: the EuRuKo 2024 goat in a coin at the centre, a band of the site's cloven hoof prints around it (the community that comes to the one goat), THE ONE THAT FEEDS THE COMMUNITY across the top of the ring and GOATCONF · 2027 along the bottom, set in Bricolage Grotesque, extra bold, 75% width. It is blue on yellow or yellow on blue; in one colour, any palette colour or black. Below about 64 pixels the small form, the goat in a disc, stands in for it; it is also the favicon and the home-screen icon. The wordmark is GOATCONF in the same face, beside the small form (horizontal) or stacked as GOAT / CONF beside the seal with the line "The one that feeds the community." Every file is built by `tools/brand.py` into `site/brand/` and offered on `brand.html`.

## Colors

> **The chosen look: minimal, in light and dark (2026-11-21, `sources/conversations/2026-11-21--org--minimal-chosen-phone-hooves-light-and-dark.md`), unpublished until approved.** The ground is paper, the pale page-print tint, printed with hoof marks; blue is only lettering and line: headings, links, keylines, the solid edge of a stuck sticker and the seal. The top bar, the cover, the page heads, the goat-story page and the back cover are white or paper with ink text; a band is album-blue lettering over its yellow rule; a photo caption is ink lettering on white; the year sits on a yellow chip; a button is a yellow sticker with a solid lip. Where the text below says the ground is album blue or a surface is blue, this note is the newer rule.
>
> **Themes.** Light is as above. Dark is the album at night, each token with its second value: ground and slot fill `#051534`, page `#0c2757`, sticker `#14387a` with a lit edge, ink `#e8eefc`, soft ink `#b6c5e8`, big lettering `#f3f6ff`, link and line blue `#a9c4ff`, slot line that blue at 60%, stamp red `#ff8a8a` printed without the multiply blend, hoof marks in the lettering blue at 12%, yellow unchanged. The site follows the system setting; a control in every footer and in the phone menu lets a visitor choose System, Light or Dark. Supporter logos, the maps, card previews and the Goatchi postcards keep a light tile in both themes. On a phone the page's side margin is 1.5rem and its inner padding 0.85rem, and the marks are printed small and close, so they show in the margins and between pages.
>
> **Cards and brand files.** A share card has one look, the light one: paper with hoof marks, blue lettering, yellow rule, the seal. The marks themselves are unchanged.

A saturated album blue in three depths, white and a pale printed blue for the pages, and two signal colours that each own a narrow job.

### Primary
- **Album Blue** (album): lettering and line only: the band's lettering, the fact-sticker body, photo-sticker captions, page titles and in-page links on white.
- **Cover Blue** (album-deep): the album cover. The left page of the opening spread and the page-head strip on every inner page.
- **Night Blue** (album-night): the darkest binding. The sticky top bar, the shiny goat-story page and the back cover; also the ink on yellow surfaces.

### Secondary
- **Signal Yellow** (yellow): numbers, the big facts and the status. Stuck-in sticker numbers, fact-sticker figures, the place-sticker caption (TUZLA), the registration status sticker, the year in the mark, and the shiny page title. It also carries the album's printed trim: the rule under every band, link underlines on blue, the crest disc and the focus ring on blue.

### Tertiary
- **Stamp Red** (red, #c80510): the "Yours?" stamp and nothing else. It is set with a multiply blend so it reads as ink pressed onto the printed slot. The value is dark enough that the stamp's lettering holds at least 4.5:1 on every surface it is pressed onto: the slot's page-print fill (5.4:1), the slot's hover fill (5.0:1) and white (6.0:1). The brighter #e30613 it replaces measured 4.35:1 on the slot fill.

### Neutral
- **Page White** (page): album pages, the right page of the spread, the prose page, and every sticker's die-cut border.
- **Page Print** (page-print): the ground of the whole site, printed with the hoof pattern in album blue at 13%; the flat fill of an empty printed slot, the default tag, and the image placeholder under a loading photo.
- **Slot Line** (slot-line): album blue at 60%, which holds at least 3:1 against the slot's page-print fill (3.3:1) and against white (3.5:1); at 42% it measured 2.2:1. Dashed slot outlines, the ring of a printed number, the name line in a slot and the dotted leaders of the price list.
- **Album Ink** (ink): body text on white pages.
- **Soft Ink** (ink-soft): slot explanations and "last checked" notes on white.
- **Pale Album** (album-soft): secondary text on the blues (cover sub-line, fact-sticker explanations, back cover, inner-page lede).
- **Vegan Tint and Ink** (veg-tint, veg-ink): only the "vegan" tag on food stickers, so the vegan marker reads at a glance without borrowing the signal colours.

### Named Rules
**The Red Stamp Rule.** Red appears only as the "Yours?" stamp on an empty slot. It never marks an error, a price, a link or a heading.

**The Yellow Means Stuck Rule.** Yellow fills only things that are decided or numbered: a stuck-in number, a fact, the status. An empty slot never carries a yellow fill; its number is printed in blue. The one exception is the button: a button is a yellow die-cut sticker you press (Register, Propose a session, Play Goatchi, and Register in the top bar), so a yellow fill that is not a number or a fact is always something to press, and nothing else on a page is filled yellow.

**The Yellow At Night Rule (a designer's choice, for the organiser to look at again).** Since round ten (`sources/conversations/2026-11-22--org--fix-all.md`) the dark theme keeps yellow for what asks to be pressed or is being pointed at: the Register buttons, the year chip, the seal, focus and hover. The number on a sticker, the rule under a heading, the rule over the footer, a place's number and the goat's speech are drawn in the line blue instead: a number is the page colour with a 2px line-blue ring and pale lettering (13.5 to 1 on the page colour). On the home page that takes the elements showing yellow from 76 to 9. The light theme keeps every yellow it had.

## Typography

**Display Font:** Bricolage Grotesque, self-hosted as a variable font with a width axis (75% to 100%), falling back to Atkinson Hyperlegible Next
**Body Font:** Atkinson Hyperlegible Next, self-hosted, falling back to system-ui

**Character:** The lettering is the album's printed type: Bricolage at weight 800, condensed (width 75% to 85%), always uppercase, set tight. Atkinson Hyperlegible Next carries every sentence a visitor actually reads, at a generous size and 1.6 leading.

### Hierarchy
- **Display** (800, width 75%, clamp(2.8rem, 0.8rem + 4.4vw, 5rem), 0.86; 3rem on phones): the cover title, GOATCONF over a yellow 2027, beside the seal. Once per site.
- **Headline** (800, width 78%, clamp(2.1rem, 1.4rem + 3vw, 3.75rem), 0.95): the band across each album page, the shiny page title, the inner-page sign.
- **Fact** (800, width 75%, clamp(2.2rem, 1.5rem + 2.5vw, 3.4rem), 0.9, tabular figures; 2.2rem on phones): the yellow figure on a fact sticker (FREE, JUNE 2027, 0.00 €). The place-sticker caption (TUZLA) is lettered in yellow at this same scale.
- **Title** (800, width 78%, clamp(1.7rem, 1.3rem + 1.4vw, 2.4rem), 0.95): the spread's page title and prose-page headings (clamp(1.5rem, 1.2rem + 1.2vw, 2.1rem)); section sub-heads on album pages are 1.5rem.
- **Lede** (700, width 88%, clamp(1.3rem, 1.1rem + 0.8vw, 1.75rem), 1.2): the cover lede and the inner-page lede, in display lettering but sentence case.
- **Label** (800, width 80%, 1.15rem, 1.05, uppercase; 1rem on phones): photo-sticker captions, slot titles (1.5rem), stamps (1.05rem), printed and stuck numbers (1.05rem), prices (1.6rem, tabular).
- **Nav** (700, width 85%, 0.95rem, 0.03em, uppercase): the top-bar links.
- **Body** (400, clamp(1.0625rem, 0.98rem + 0.3vw, 1.1875rem), 1.6): all running text, held to 62ch (74ch on wide copy, 58ch on the shiny page).
- **Small / Credit** (400, 0.98rem at 1.35; 0.82rem at 1.45): slot and fact explanations; checked dates.

### Type scale
Since 2026-11-22 (`sources/conversations/2026-11-22--org--continue-round-nine.md`) every size set in rem comes from one scale of fourteen steps. Since round ten (`sources/conversations/2026-11-22--org--fix-all.md`) the sizes that grow with the window come from eight named steps too, where there were four named and twenty-three written out by hand; the second table lists them.

| Step | rem | Used for |
|---|---|---|
| 1 | 0.75 | the smallest print: postcard captions, map credit |
| 2 | 0.8 | tags, group labels, credits |
| 3 | 0.85 | card small print, checked dates |
| 4 | 0.9 | card body, captions |
| 5 | 0.95 | slot and fact explanations, nav, footer |
| 6 | 1.05 | stamps, numbers, labels |
| 7 | 1.15 | photo captions, prices on cards |
| 8 | 1.2 | card titles, buttons in the ticket |
| 9 | 1.35 | bar mark, card names on phones |
| 10 | 1.5 | slot titles, sub-heads |
| 11 | 1.6 | prices in a price list |
| 12 | 2.2 | facts on phones |
| 13 | 3 | the cover title on phones |
| 14 | 4.6 | the ticket's FREE on phones |

| Fluid step | From, to (rem) | Used for |
|---|---|---|
| `--step-0` | 1.0625 to 1.1875 | running text |
| `--step-sub` | 1.15 to 1.45 | the place line on the closing page, the statue's line |
| `--step-1` | 1.3 to 1.75 | ledes, the saying, the cover's date line |
| `--step-title` | 1.45 to 2 | a prose page's headings, "What is decided", long facts, the ticket's dates |
| `--step-fact` | 1.7 to 2.5 | the facts on stickers, day names, session formats |
| `--step-head` | 1.75 to 3 | the band over every album page, place names on photo stickers, the closing page's dates |
| `--step-2` | 2.1 to 3.75 | an inner page's sign, the shiny page's title |
| `--step-3` | 3.4 to 5.7 | the cover title, the ticket's FREE |

Running text is held to 62 characters a line (74 on wide copy). Headings balance their lines; times, dates and prices use tabular figures.

### Named Rules
**The Lettered, Not Typed Rule.** Every heading, caption, number and stamp is Bricolage at 800, condensed and uppercase. Weight never varies to make hierarchy; size does.

**The Reading Face Rule.** Any sentence longer than a label is Atkinson Hyperlegible Next, never the display face.

## Layout

The site is a column of album pages on the blue ground, each at most 82rem wide with a side margin of clamp(1.1rem, 4vw, 3.5rem), separated by clamp(2.5rem, 1.8rem + 3vw, 5rem). The opening spread is two pages in one rounded frame (1fr cover, 1.2fr page), 53rem tall on wide screens, that stack on screens under 62rem with the spine shadow turning horizontal. Album pages run a two-column grid (1fr copy, 1.2fr stickers) that collapses to one column under 62rem.

Slots and stickers sit in auto-filling grids (minimum 12.5rem per cell, gap 1.6rem by 1.3rem). The opening page is a photo column: three across, the Tuzla and IPI Academy photos each two cells wide and two tall, the facts beside them, so the numbers still read 1 to 6 (on phones, one sticker after another, at most 26rem wide); the food page three across; the add-your-own page four across. Under 48rem the stickers a visitor reads go one after another, in the album's order, in one centred column at most 26rem wide: the opening page's six, the days, the speakers, the Tuzla photos, the food and the supporters, each as the organiser chose after seeing them two across (`sources/conversations/2026-10-17--org--three-days-mobile-and-open-wording.md`, `sources/conversations/2026-10-18--org--what-is-decided-one-by-one.md`, `sources/conversations/2026-10-18--org--speakers-one-by-one-on-mobile.md`, `sources/conversations/2026-10-18--org--tuzla-and-food-one-by-one-on-mobile.md`, `sources/conversations/2026-10-20--org--hero-phone-list.md`). Between album pages a phone keeps 1.75rem, and stacked stickers with no goat between them sit 1.1rem apart; a row with a goat over it keeps the room the goat needs. The small grids stay two across with a 1.2rem by 0.9rem gap: the kinds of event, the numbers on fact stickers beside copy, the faces on the register page and the photos of past conferences. The top bar is sticky. On wide screens it has one button, Register, filled in yellow; every other item, Host an event and Propose a session included, is a plain link. Under 48rem it is one row about 3.5rem tall: the mark with its year, a compact yellow Register button and a Menu button, each at least 44 pixels tall, so registering is one tap away at every scroll position. Menu opens a night-blue panel under the bar with the four page links, centred, one per row, then three separate centred buttons of one width: Host an event and Propose a session outlined in yellow, Register filled in yellow (the organiser, 2026-10-23, `sources/conversations/2026-10-23--org--phone-menu.md`). On 2026-10-23 the organiser took Register out of the phone bar, when the build that had it dropped the year; the 2026-11-21 iteration puts it back with the year kept at every width down to 320 pixels, for the organiser to approve (`sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md`).

Inner pages share one shape: a cover-blue page-head (sign, lede, a tilted photo sticker on the right, stacked under 62rem) followed by one white prose page, 58rem at most, and a plain footer on the blue. Make it yours and Propose a session follow the page-head with album pages instead, each with its band and a two-column grid of copy and stickers; on Propose a session, what a speaker gets comes first as numbered fact stickers, two across on wide screens and one after another on phones at most 26rem wide (an empty printed slot for anything not promised yet); the formats follow as open slots with one goat, over the first, so the rows close up; and travel comes after them with a price list of a stay. On one column the cards come before the text in their section: the stickers after the first paragraph, the format slots before their details (the organiser, 2026-11-07, `sources/conversations/2026-11-07--org--talk-page-phone.md`). Getting here, staying and money follows them too: jump links in the day menu's night-blue pill (sticky on wide screens, in the flow on phones), the ways in as four numbered fact stickers, then a price list, then the details in two even columns; on a phone the food list shows its first five places behind a "Show all" toggle that needs no script (`sources/conversations/2026-11-07--org--travel-page-redesign.md`). Register follows them in short: the button beside four fact stickers, then who is speaking as small square photo stickers with the name on an album-blue strip (eight across, two on a phone), then the days and how it works (`sources/conversations/2026-11-07--org--register-page-and-hallway-track.md`). The program opens on the same faces strip, "Confirmed so far", and at every width folds a slot's open rooms into one dashed line beside its cards, so a slot shows what is there and how much is still open (`sources/conversations/2026-11-07--org--program-page-lineup.md`). The home page keeps every speaker card and every dish on a phone, never the faces strip or a fold, so each goat on them stays a stop for the companion goat (`sources/conversations/2026-11-07--org--home-goats-stay.md`). **Set aside for the home page on 2026-11-22 (round fourteen):** the organiser decided that every section of the home page but the hero and the free ticket opens and closes, that they start closed except the speakers, and that the last state is remembered (`sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md`, `sources/conversations/2026-11-22--org--sections-start-closed-speakers-open.md`). Every speaker card and every dish is still on the page in full and is one tap away; a goat inside a closed section or a closed list is not a stop until it is opened. See "Sections and lists that open and close" below.

### Spacing scale
Since round ten (`sources/conversations/2026-11-22--org--fix-all.md`) the room between a heading and its text, between two pieces of text and between two sections comes from one scale of six steps and the section step. The right-hand column is what was measured on the site before, in pixels, on a phone and on a wide screen.

| Step | rem (px) | Used for | Before |
|---|---|---|---|
| `--gap-1` | 0.25 (4) | the lines of one item (a place's lines, a slot's time and its open rooms on a phone) | 3, 5, 6 |
| `--gap-2` | 0.5 (8) | the items of a list in running text, a line under a card's title | 7, 9, 10, 11 |
| `--gap-3` | 0.75 (12) | a sub-heading and the text it heads; the sign and its lede on a phone | 6, 10, 13, 14, 16, 17, 19 |
| `--gap-4` | 1 (16) | a paragraph and the next; a band and the first thing under it on a phone | 14, 17, 18, 19, 22, 32 |
| `--gap-5` | 1.5 (24) | text and the cards beside it in the flow, either way round; text and the next sub-heading; two sections on a phone | 0, 6, 19, 22, 26, 28, 29, 32, 48 |
| `--gap-6` | 2.5 (40) | a band and the first thing under it on a wide screen; the last text and the next heading of a prose page; text and a row of cards a goat peeks over | 35, 38, 40, 48, 62 |
| `--space` | 2.4 to 4.7 (67 at 1440) | two sections on a wide screen | 67 |

A gap that is part of a card's own drawing (the ticket, a sticker's caption, a goat's room over a row) is not on the scale.

## Elevation & Depth

Depth is physical but quiet: paper pages cast a short soft drop onto the blue, stickers lift a little off the page, and the spread has a spine. Nothing is flat-shadowed by default except the empty slots, which are printed and therefore sit in the page.

### Shadow Vocabulary
- **Sticker lift** (`box-shadow: 0 0.2rem 0.35rem -0.15rem rgb(0 0 0 / 0.3), 0 0 0 1px rgb(0 0 0 / 0.08)`): every stuck sticker at rest, and the inner-page photo sticker.
- **Page drop** (`box-shadow: 0 0.6rem 1rem -0.8rem rgb(0 0 0 / 0.3)`): album pages and the prose page on the blue ground. The spread uses a deeper drop (`0 0.8rem 1.4rem -1rem rgb(0 0 0 / 0.35)`).
- **Spine** (`box-shadow: inset -1.4rem 0 1.6rem -1.2rem rgb(0 0 0 / 0.55)` on the cover, `inset 1.4rem 0 1.6rem -1.2rem rgb(0 0 0 / 0.25)` on the page): the fold between the spread's two pages.
- **Number lift** (`box-shadow: 0 0.15rem 0.3rem -0.1rem rgb(0 0 0 / 0.35)`): the small yellow number sticker on a stuck sticker.
- **Goat lift** (`filter: drop-shadow(0 0.7rem 0.6rem rgb(0 0 0 / 0.45))`): under the die-cut goat, after its white edge.

### Named Rules
**The Printed Is Flat Rule.** An empty slot, a printed number and the stamp have no shadow. Only things stuck onto the page lift.

**The Matte Rule.** Stickers are matte: no sheen, no gradient, so photos keep their true colours and a fact sticker reads as flat printed blue. Their shadows stay short and light, so they sit on the page rather than float above it (organiser's choice, 2026-10-26, "not too glossy").

## Shapes

Corners are soft and consistent: pages and the spread at 0.8rem, stickers and slots at 0.6rem, the photo inside a sticker at 0.35rem so the white die-cut border keeps an even width (0.42rem) all round. Numbers are pill-shaped stickers (1.05rem radius); the crest and the status dot are circles. The stamp is a 3px rectangle with 0.35rem corners, rotated -9 degrees.

Stickers are set at small individual tilts between -2 and 2 degrees, set per sticker; the inner-page photo sticker sits at 2 degrees and the goat at -6. Album pages clip to their rounded corners; the blue band sits inside a 0.42rem white edge at the top and sides, like the white border of a fact sticker, so the page reads whole against the album-blue ground. Borders exist only as print: the dashed slot outline, the dotted price leader, the solid name line and the yellow rule under each band.

## Components

### Sticker
Matte vinyl stuck onto the page: white die-cut border, sticker lift, a small tilt.
- **Photo sticker:** a 4:5 photo (4:3.4 on album pages, 4:3.2 on the food page) over an album-blue caption strip lettered in white.
- **Place sticker:** a photo sticker whose caption is a place name lettered in yellow at near fact scale (TUZLA).
- **Fact sticker:** a white sticker with a solid 2px album-blue edge and a solid lip under it; a big album-blue fact over a short soft-ink explanation, its number in yellow.
- **Tag:** a small pill under a food sticker's caption: page-print by default, the vegan tint for vegan dishes.

### Printed Slot
The empty place in the album: page-print fill, a 2px dashed slot-line outline, 0.6rem corners, at least 9rem tall. It carries the goat mascot peeking over its top edge, a printed number at the top, a blue lettered title and a soft-ink explanation. Open slots add the red "Yours?" stamp at the bottom right; slots for things a host will add carry a printed name line instead of an explanation.

### Numbered Sequence
One run of numbers through the whole album, so a reader can see the gaps. On a stuck sticker the number is a yellow pill sticker overlapping the top-left corner with its own lift; on an empty slot the same number is printed in place: no fill, album-blue figure, a 2px slot-line ring. On the home page every fact sticker carries its number, the ones beside copy included (the supporter's price, the organiser's numbers); `tools/home.py` numbers them all in one pass.

### Album Page and Band
A white page with 0.8rem corners and the page drop. Its heading is the band: album blue, white headline lettering, a 0.45rem yellow rule beneath, running across the top of the page inside a 0.42rem white edge with 0.4rem corners. The edge keeps the page's silhouette whole, since the band and the ground are the same blue.

### Spread
The opening: one rounded frame holding the cover-blue left page (the seal beside the cover title, the lede, the Register button and three links) and the white right page ("What is decided": two big photo stickers, three fact stickers with large yellow lettering, and one slot), joined by the spine shadow.

### Die-cut Goat
The one goat mark as a sticker: night-blue line drawing with a yellow fill, a 3px white edge cut around the silhouette, the goat lift, set at -6 degrees. It appears on the cover and, larger, on the shiny page. The mini crest (a yellow disc with the goat) marks the top bar, the back cover and the inner-page home link.

### Goat Mascot
A second goat, kept apart from the mark: a painted watercolour storybook goat, fluffy and cream, with big brown eyes, pink inner ears, a small beard, dark hooves and golden horns curled back. It is painted, not drawn in code: the masters stay on the organiser's machine and `tools/goat_atlas.py` builds the site's images from them, one sprite sheet per set of goats, so a page fetches one small image for all its goats. It comes in roles from the EuRuKo 2024 goat multiverse: the goat, the speaker (microphone), the host (fes and fildžan), the coder (round glasses, laptop), the cook (chef's hat, ćevapi), the Pannonian pirate (tricorn, eye patch) and the hidden goat. On an open slot it peeks over the top edge, its hooves on the edge, in the role the slot's kind gets; where a speaker or a venue has no photo it sits whole; on the 404 page it sleeps. Each speaker has their own painted goat (hair, beard, glasses or cap, what they wear, never a logo), peeking over their card, sitting beside their bio and sitting whole in the corner of their share cards. It blinks, each goat on its own beat. It is decorative and hidden from screen readers. The seal keeps the EuRuKo 2024 goat; the mascot never replaces the mark.

**One goat at a time.** With the script, a visitor sees one goat: it stands inside the open slot or speaker card nearest the middle of the screen, as that slot's role or that speaker's own goat, and hops to the next one as they scroll or point. Without the script every slot keeps its own goat; on Save-Data or 2G there is none; with reduced motion it appears where it is and stays still.

**The goat on a photo of Tuzla (a designer's choice, for the organiser to look at again).** Since round eleven (`sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md`), on the photos of "Tuzla, the host town" the goat's painted scene is a third as wide as the photo (it was two thirds and covered more than two fifths of the picture) and stands in the photo's lower right corner, on the photo's bottom edge beside the caption, so the middle of the picture and its subject stay clear. It arrives by fading in while it rises a little (520ms, no overshoot, no tilt) and leaves by fading out as it sinks (300ms); with reduced motion it is simply there. Every photo keeps its goat stop (`sources/conversations/2026-11-07--org--home-goats-stay.md`). A goat on a food card and the goat by the statue keep their own places and take the same gentle arrival.

### Stickers
The sticker packs (stickers.html) take the same drawings: the goat's roles, the speakers' goats with their names on a blue label, the mark and a few words lettered in Bricolage, and Tuzla things, each with a white die-cut edge and a soft lift on a transparent 512-pixel square, in a zip and on an A4 print sheet.

### Share cards, light and dark
Since round eleven (`sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md`) every still card that `tools/shareables.py` renders exists twice. The light card is the one shipped in round six and keeps its address, so no link already shared breaks: paper `#edf2fb` with the hoof marks, lettering `#0b3d91`, ink `#12204a`, soft ink `#46557a`. The dark card has the same name ending in `-dark`: night ground `#051534` with the hoof marks in the line blue, lettering `#f3f6ff`, ink `#e8eefc`, soft ink `#b6c5e8`, a photo ring in the sticker blue `#14387a`. Both keep the seal and the yellow rule along the foot, which is the card's signature when it is seen alone in a feed (a designer's choice at night, where the site itself drops the yellow rule). A supporter's logo keeps the ground it was drawn for in both. A page's link preview stays the light card, one per page.

Where a page offers a card (a speaker's own card and the card announcing them, a supporter's cards, an event's card) each shape shows its light and its dark card side by side, each one a link that downloads it, labelled "Light" and "Dark" under the picture in the standalone link style with its arrow; it works without the script. The brand page lists every such card in one place.

**The goat says a line.** On a speaker's own card and on the card announcing them the goat says "See you in Tuzla!" in the site's own speech bubble: yellow with night lettering in both versions, up and to the left of the goat's head with its tail corner towards the goat, lettered at 38 pixels on the square card and 30 on the wide one so it reads at the size a card has in a feed. The organiser picked the line (`sources/conversations/2026-11-22--org--organisers-own-page-and-see-you-in-tuzla.md`) from eight candidates, each already on the site or in the organiser's recorded words (`sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md`); it carries the exclamation mark every line the goat says on the site carries. The bubble keeps clear of the name, the role, the session and the seal: on the card with the longest role it is 23 pixels from the nearest line. The link preview a speaker's page shows (1200 by 630, shown small where a link unfurls) carries no bubble. `SPEAKER_SAYS` in `tools/shareables.py` holds the line; a record's own `card_says:` line wins. The site's own speaker cards keep no standing bubble: there the goat already says its lines when it is tapped.

### Ticket
The home page's "Get your free ticket" page holds one sticker cut as a ticket: album blue inside the white die-cut border, a dashed tear line with a notch bitten out of each end, and a number like any other sticker. The larger part letters FREE in yellow at fact scale over the dates and the place in white; the stub holds the Register button and one line on what registering gets you. On wide screens the stub is on the right; under 48rem it is below, with the tear line across. It is matte and tilted like every sticker, and it is the only ticket on the site. The place reads with its address, and under the button a plain link adds the three days to a calendar.

### Button
A yellow die-cut sticker you press: yellow fill, night-blue lettering, a white die-cut ring, set at -1 degree. Pointed at, it lifts: it turns to 1 degree, rises 0.25rem, grows 3% and casts a longer shadow, over 180ms. Pressed, it goes flat: back to -1 degree, 3% smaller, the shadow gone, the yellow a shade darker. With reduced motion it does not move; only the yellow changes. Focused, it gets two more rings outside the white one, night blue then yellow, so the focus shows on the blue cover and on a white page alike.

### Closing Page
The home page's last page, "See you in Tuzla". On wide screens, since round ten (`sources/conversations/2026-11-22--org--fix-all.md`): "Free to attend." in soft ink, then the dates across the page on one line at heading size (two balanced lines where the window is narrower), then one row with the place lettered on the left and the Register button beside it. The waving goat, when it is here, stands at the right end of the page beyond the dates, 8rem to 10rem wide; the dates never run under it, and nothing in the middle of the page is held empty for it or moves when it comes. On a phone the lettering, the button and the goat stack, the goat centred below the button. Nothing else is on the page.

### Who's organising: a page, linked from the supporters section and the footer
Since round twelve (`sources/conversations/2026-11-22--org--organisers-own-page-and-see-you-in-tuzla.md`) "Who's organising" is a page of its own, `organising.html`, and no longer a section of the home page. The page opens on the inner page-head (the sign, the section's first sentence as the lede, the host goat as its mark), then one sheet without a heading of its own (the host and the expected size, the two links, the four numbered fact stickers two by two with the host goat's stop over the first), then "Conferences run before" (the two conferences side by side on a wide screen, the four photos in a row, the line that these were past conferences). Every sentence is the home section's own; none is added, cut or reworded, and the stickers are numbered from 1 on their own page. Since round thirteen (`sources/conversations/2026-11-22--org--organising-row-off-the-home-page.md`) the home page has no row or section for it. The link "Who's organising" sits in the supporters section, beside "The supporters" under "Who makes it possible", lettered like every link on its own; and the link keeps the old section's address (`#organiser`), so a link shared before lands beside it. The host goat's stop stood at the end of that row for one round; the organiser removed it on 2026-11-22 (`sources/conversations/2026-11-22--org--no-goat-beside-the-organising-link.md`): "The host goat doesn't need to show up next to the who is organising link on homepage". That is the one stop the organiser has taken off the home page since deciding on 7 November that the goats stay (`sources/conversations/2026-11-07--org--home-goats-stay.md`); every other stop stays, and the host goat keeps its stop on the organising page. Every footer links the page in "The conference"; it is not in the top bar. Between 1024 and 1440 pixels wide the footer's four groups sit two and two, where they used to sit three and one left alone; from 1440 they share one row.

### Sections and lists that open and close
Since round fourteen the home page is a set of sections a visitor opens and closes, and the browser remembers what they last chose. It is the organiser's decision of 2026-11-22, in three messages: "We should probably have every section as collapsable? Also probably should store latest preference in localstore so folks keep last state?", "Only leave the free ticket section as one that can't be collapsed and the hero section", and "They start closed probably? Speakers section stays open?" (`sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md`, `sources/conversations/2026-11-22--org--sections-start-closed-speakers-open.md`); and published on "Ok, ship when ready" (`sources/conversations/2026-11-22--org--ship-the-collapsible-home-page.md`). It sets aside the persona study's verdict, which kept every section open and closed two lists on a phone only; the study's dissents are kept in the second source.

**What a first visit shows, on a phone and on a wide screen (amended 2026-11-22, `sources/conversations/2026-11-22--org--speakers-section-also-collapsed-by-default.md`).** The organiser, after seeing the page live: "Ok. Let's have speakers section also collapsed by default?" So every section that opens and closes starts closed, "Who is speaking" too, which reverses the organiser's earlier "Speakers section stays open?" and "Keep as it is" of the same day. The hero (the cover and "What is decided"), "Get your free ticket" and "See you in Tuzla" are open and have no control. A browser that already remembers a choice for the speakers keeps it; one that remembers nothing for them shows them closed. The closed speakers row carries the lineup on its own: the eight faces, a press on which opens the section, and "View all speakers", on a phone as well. A page opts in with `data-folds` on its main; `data-fold="never"` on a section gives it no control and `data-fold="open"` would start one open, so the same mechanism can serve another long page.

**The control is the heading.** The heading stays a heading; the script puts a button around its words, so a screen reader hears "Tuzla, the host town, button, collapsed" inside the page's outline. The album's arrow stands before the words, pointing down while the section is closed and up while it is open; the whole heading row is the press area, never under 44 pixels tall, with the 3px focus mark inside its edge and the yellow press the list rows have. Enter and Space work as on any button.

**Remembered, never a trap.** The last state of each section and each list is kept in this browser under one key, `folds`, beside `theme`, one entry a page; nothing is sent anywhere and there is no cookie. A script in the page's head marks the closed sections as the page is read, before the first paint, so a remembered state that differs from the first-visit one does not make the page jump. A link to a section or to anything inside one, a link to a sentence, and find in page open what they land in for that visit and do not change what is remembered. With storage blocked or cleared the page is the first-visit page and works the same. Without the script nothing is closed, no control shows and the lists still open and close on their own; and if the script file never arrives everything opens when the page has loaded. On paper everything is open.

**One family, one level (amended 2026-11-22, `sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md`, `sources/conversations/2026-11-22--org--first-visit-stays-see-you-fixed-open-ship-when-ready.md`).** The organiser, about the live page: "The meals section behaves weird when collapsed due to goats changing", then "Let's improve those aspects now for each section when collapsed vs opened"; and, asked, chose that "See you in Tuzla" is "fixed open". So three things have no control now: the hero, "Get your free ticket" and "See you in Tuzla". Ten sections open and close. The paragraph folds of round ten are gone and so are the two lists that closed on a phone inside an opened section: opening a section shows all of it, one tap and one result. Every open section ends with "Show less", which closes it and puts the heading and the keyboard back where the visitor is. One control above the first section, "Open all sections" or "Close all sections", at the left where the headings' arrows are.

**A closed row.** On a phone it is the heading and one line: the three dates; the speakers' faces and "View all speakers"; the strip of six Tuzla photos with "Six photos of Tuzla" under it; six of the dishes with "Twelve dishes, with prices"; the "Propose a session" button; "Propose yours" and "Host an event" (the label the cover gives the same page); the supporters' logos, each a link, and "How to support"; the statue sentence; the two conduct links; "Play Goatchi". What does not fit a line on a phone (the program link, the travel link) is on the row from 48rem up. A press on a strip of pictures opens the section. From 62rem a closed row is one line: the heading, then what the row shows, then the rule under both, about 86 pixels tall; where the words do not fit they take a second line. A heading wraps the same way closed and open, because no heading makes room for a goat. "Why a goat" is drawn as the others are in both states: the same heading size and rule, and on a phone its heading first and the seal after the words. A link to any section lands with the section's top 3rem under the bar's reserve, one margin for all.

**Goats.** Each section that opens and closes has one goat of its own and one place for it: the section's top edge at its right end, where the goat peeks over as a goat peeks over any card. It is the same character every time and the same size on every row (2.8rem on a phone, up to 4.2rem on a wide screen): the plain goat for the days, support and conduct, the speaker for the speakers and the proposals, the pirate for Tuzla, the cook for the food, the host for "Make it yours", the hidden goat for its own story, the coder for Goatchi. It stands outside the row's boxes, in the space between two rows, so nothing on a row or under it moves when the goat arrives, leaves or changes, and it is the section's stop whether the section is closed or open. The cook no longer stands in the food heading, which wrapped and left a hollow band for it. While a section is closed no goat inside it is a stop, by any way of calling the goat: the page coming to rest, the pointer, a tap. A goat never covers a word, a link, a button or a stamp: where it would at a slot's right end it stands at the left, then smaller, and where no place is clear that slot is not a stop at that width. The photo in "How we treat each other" is no longer a stop. A press on a goat is for the goat and never opens or closes a section; a press on a heading never sets the goat off. When a section opens or closes under the goat it leaves at once and comes back where it may stand. This sets aside, for closed sections, the decision of 7 November that the home page's goats stay (`sources/conversations/2026-11-07--org--home-goats-stay.md`); every goat inside returns when its section is opened.

**The section's goat at a size that reads, and never cut (amended 2026-11-22, `sources/conversations/2026-11-22--org--section-goats-too-small-and-cut-off.md`).** The organiser, about the published page: "Goats seem to small now and the text and the goat can be cut off by the section it is in apparently?", then "Maybe it's on mobile only? Check". It was not on a phone only. Measured: the goat on a row was 45 by 48 pixels at 390 and 63 by 68 at 1440, where the goat on a slot of the cover is 83 wide on that phone and the goat on a heading was 86 before that day; and while a section was open, its own page clipped the goat and its speech bubble, which stand above the top edge. This replaces the sizes in the paragraph above. A section's goat is 5.2rem wide at every width, the width of the goat on a slot of the cover (83 by 89 pixels drawn), and rises 4.8rem over the section's top edge with its hooves on the edge. The room for it is kept above every section that opens and closes, in both states and whether or not a goat is there: 3.75rem between two sections on a phone, 4.2rem from 48rem and 4.5rem from 62rem, which with the lower padding of a closed row is as tall as the goat; so a goat this size covers nothing, no row makes way for it, and it is never made smaller. "Open all sections" keeps its distance to the first section. A section that opens and closes does not clip what leaves its page, closed or open. The goat's speech bubble on a section opens beside its head, inside the room between two sections, on one line; a bubble over its head would lie on the row above. A row is a stop only while the goat and its bubble are clear of the sticky top bar, and a link to a section lands with the section's top 5.6rem under the bar's reserve, so the goat that comes to it stands whole. The first-visit page is 324 pixels taller on a phone 390 wide and 48 taller at 1440.

**A goat on a top edge overlays what is above it; no room is kept for a goat (amended 2026-11-22, `sources/conversations/2026-11-22--org--goats-overlay-no-empty-room.md`, `sources/conversations/2026-11-22--org--speaker-goats-on-the-left-and-smaller.md`).** The organiser asked "Why are some speakers goats showing up on the left side and smaller?"; shown a fix that kept room above every slot a goat stands on, asked "Why do we need empty spaces between? Can't the goats have overlay over the sections above?"; and added "If a goat is drawn above a link, clicking on a goat should not trigger that link". This withdraws two things written above on this page, for every goat that stands on the top edge of a slot or of a section. The rule that such a goat covers no word, link, button or stamp, and stands at the left, then smaller, or not at all where it would, is withdrawn: it was the review's and the builder's, never the organiser's, and it is what moved goats to the left and shrank them (at five widths, 126 of the 210 places a goat stands over a slot). The room kept between two sections for the section's goat, in the paragraph directly above (3.75rem to 4.5rem), is withdrawn too: the sections stand as far apart as before it, and the home page is as tall as before it. What holds now. Every goat on a top edge stands at its own full size at the right end, on every slot and every section, at every width; a section's goat stays 5.2rem wide. It is drawn in front of whatever is above its seat, the section, the card or the paragraph, with a soft shadow so it reads as standing on the edge, and its speech bubble is drawn in front as well. Nothing is cut by a page's clipped corners and a slot or row is a stop only while the goat and its bubble are clear of the sticky top bar. A press on the goat is the goat's alone: it follows no link, presses no button, opens no card and opens or closes no section under it; the goat's picture takes the press and only its empty corners let one through. What it stands over can still be pressed beside it, and where a small link would be left with no 44 pixels to press, that one goat stands further along the edge by the least that leaves them (no seat is in that case today). A goat does not lie over the face in a speaker's photo. Closed rows hold still, nothing inside a closed section is a stop, and each speaker's card has that speaker's own goat. The goats that stand inside their own picture (on a photo of Tuzla, by the statue, the waving goat) are as they were.

**For the organiser to revisit (a designer's choices, none of them the organiser's words):** the arrow before the words; a goat lying over the words above its seat, its shadow, and the share of its picture that takes a press; the size of a section's goat, the room kept for it between two sections and where its bubble opens; which character stands on which section; the cook moved from the food heading to the food section's corner, at the size every section's goat has; the goat's stop taken off the conduct photo; a goat standing smaller or not at all where it would cover words; "Host an event" as the short label on the closed "Make it yours" row; what a phone leaves off a closed row; "Open all sections".

### Round sixteen: what the day's work left open
On the organiser's "Anything left? Let's iterate" (`sources/conversations/2026-11-22--org--anything-left-lets-iterate.md`), with the open faults of the same day's independent review. No sentence on the site is new: where a fix needed words, they are words the site already carried, and each is named with where it stood.

- **One price on the closed Tuzla row.** From 390 pixels wide up to 48rem the closed row "Tuzla, the host town" carries "A simple meal 4.60 €" on the line of "Six photos of Tuzla". It is the first line of that section's own price list, "What things cost in town". A narrower phone has no room for it beside the count, and the one line of a wide screen has none either. The row keeps its height.
- **Tap targets on a phone.** A place's contacts on the host page stand in one row, each 44 pixels tall, where they stood one under another on a 30 pixel pitch. The finder's checkbox is pressed through its whole row. The brand page's file links, the links under "How to support them" on a speaker's and a supporter's page, and "Propose a session" under each slot of the program take a press 44 pixels tall and are drawn as before. The host page and the supporter pages are taller on a phone for it; no other page is.
- **A tag is not a button.** "Fits an hour off" and "Ask GoatConf first" on a place are filled as every tag is and marked with a dot before the words: a full dot for the first, a ring for the second. The 2px outline in the link blue, which is the drawing of "Menu" and "Open all sections", is gone from them.
- **Cards to share, behind one closed row.** On a speaker's page, a supporter's page and an event's page the cards to download wait behind one closed row at the foot of the page, "Cards to share", the heading an event's page already gave its cards. Only the card's owner needs them, and the page is read mostly by visitors. The row is the browser's own disclosure, so it opens without the script, and it is not remembered. Inside, each kind of card keeps its heading as a sub-heading, with its two shapes in light and dark as before. On a speaker's page the row is a band like the page's others and carries the speaker's goat: one goat for the one section, where two sections each had one. A press on the goat does the goat's trick and does not open or close the row.
- **The arrow of a link that leaves the site stays with the link's last word.** It is drawn on a no-break space inside the link's own line, where it could wrap to a line of its own. The home page's back cover gains one line on a phone for it.
- **At night.** The host finder's hint takes the soft ink, where the browser's grey stood. The two dark logo tiles on the closed supporters row get the thin lit ring a photo has at night. A supporter's sticker and the supporters' chips already had a pale edge and keep it.
- **One drawing for everything that opens.** A row that opens a list (the brand page's three lists of cards, the travel page's rental companies, "Cards to share") is drawn as the home page's headings are: the album's arrow before lettered words, down while closed and up while open, never underlined, the whole row the press area and at least 44 pixels tall. A button that shows more of a list ("Show all places to eat") is the home page's outlined button.
- **A supporter's sticker takes a whole row on a phone,** the logo beside the name and the line, where two ragged stickers stood side by side. A logo on the home page's closed supporters row lifts when pointed at, as a supporter's sticker does.
- **The cards' foot line.** "Tuzla · 3–5 June 2027" and the page's address stay two parts, and the dot between them belongs to the address: when the address takes a line of its own, no dot is left hanging at the end of the first line. The speakers' cards are rendered again for it.
- **The cards' weight.** A card of flat colour is saved with a palette of 256 colours when the palette reproduces the full colour render at a peak signal to noise ratio of 45 dB or better, where the eye finds no difference; a card built around a photograph and any card under that mark keep full colour.
- **The top bar is one row at every width.** From 56rem the links hold one row, set a little closer under 68rem; under 56rem the bar is the phone's, with the mark, Register and Menu. It was two rows tall from 48rem to about 68rem.
- **The brand page's card list on a phone** sets a speaker's two kinds of card side by side, each a label over its square and its wide card, every link 44 pixels tall, where six ragged lines stood.
- **Forced colours.** The arrow of a link that leaves the site, the rule under a closed row on a wide screen, and the tile behind a logo in a page head and behind a past conference's logo are kept when the system's colours take over.
- **"Who pays" comes before the propose button on a phone,** by order alone: the same words, so a host reads who pays before deciding. On a wide screen it stays at the head of the right-hand column.

**For the organiser to revisit (a designer's choices, none of them the organiser's words):** the one price on the closed Tuzla row; the dot and the ring on the two tags; the cards behind a closed row on a speaker's, a supporter's and an event's page, and one goat on that row where two bands each had one; 56rem as the width where the bar becomes the phone's; 45 dB as the mark for a palette; the host page and the supporter pages growing on a phone for the 44 pixel rows.

### When, where and free under a page head
A page a visitor may land on first says when and where GoatConf is and that it is free, in the cover's own words and never in new ones (`sources/conversations/2026-11-22--org--date-place-and-free-on-speaker-and-register-pages.md`). Under a speaker's lede: the cover's line "3–5 June 2027 · Tuzla, Bosnia and Herzegovina", lettered as the cover letters it but at the sub-heading's size, then "Free to attend." and the link "Register for free". The register page carries the line above its lede. It is part of the lede's block, so the page head keeps its shape.

### The stressed line
A sentence a reader must not miss, where a decision is made, is lettered and not boxed: under a sub-heading of its own, in the display face at 700 and 1.2rem, in ink, at most 34 characters a line. It has no fill, no rule beside it and no sticker; the page around it stays as calm as before. The first one, since round thirteen (`sources/conversations/2026-11-22--org--hosts-need-not-pay-for-everything.md`), is "Who pays" on the host page, at the head of the guide's right-hand column in "How to host", directly above "In an hour off": "You run it. You do not have to pay for everything: it is fine if the people who come pay for themselves, as long as the listing says what it costs." It is the sentence the proposal form carries, word for word, so the site and the form say the same thing; the organiser approved it and its publishing (`sources/conversations/2026-11-22--org--ship-round-thirteen-when-ready.md`).

### Session Slot and Session Sticker
A speaker card whose session is not announced yet holds an empty printed slot under the role: page-print fill, the dashed slot-line outline, "Session to be announced" lettered in album blue at label size, one line tall, at the foot of the card, so the slots of a row line up. It has no stamp and no goat: the place is the speaker's, not open. On a speaker's own page an announced session is a sticker in the fact sticker's colours: album blue inside the white die-cut border, the format and time in white label lettering, the title in yellow at 1.8rem to 2.6rem, the description in white at body size, tilted under half a degree. A session still to come on that page is the same empty printed slot.

### Open Rooms and Place Rows
On the program, a slot's open rooms are one printed box beside the slot's cards, as tall as they are: a small empty slot drawn for each open room, over one line. On a phone it is the line alone. On Make it yours a place is a sticker with its photo on wide screens; under 48rem it is a compact row, the photo a 5rem square beside the name plate and its lines in small type, and the list folds after eight places behind a control that needs no script.

### Status Sticker
The registration status: a yellow pill-cornered sticker (0.45rem) with a night-blue dot and night-blue lettering. It states what is true now, never a date that is not confirmed.

### Price List
Item, a dotted slot-line leader, and the price lettered in album blue at 1.6rem with tabular figures. Followed by a soft-ink "last checked" line.

### Shiny Page
The one solid beat: a night-blue page with a white die-cut border drawn inset (0.42rem), the big goat on the left, the yellow title and the saying lettered in white on the right. On wide screens the seal shares the left column with a photo sticker of Tuzla's goat statue, 10rem to 12rem wide, overlapping the seal's lower corner, numbered like every sticker, its one sentence lettered in white beside it; the painted statue stands at the photo's corner as the goat's stop. On a phone the page closes on one row, the sentence and the photo at 7rem.

### Navigation
The top bar is night blue and sticky: the mini crest and GOATCONF with a yellow 2027 on the left, uppercase condensed links on the right that turn yellow on hover. On wide screens Register is the bar's only button. On phones the bar shows the mark, Register and Menu, and every link folds into the Menu panel; the menu is a `<details>`, so it opens without a script. Links in running text are underlined in yellow on blue and in album blue on white, thickening from 2px to 4px on hover. Focus is a 3px album-blue ring on every ground; a button's ring is described under Button. Links a visitor taps are at least 44 pixels tall on phones, the cover's three links included. The "go" link (a larger lettered link, 750 weight) leads each page's call to action. **The jump row.** Since round ten (`sources/conversations/2026-11-22--org--fix-all.md`) the links that jump down a page (the program's three days, the travel page's seven parts) are a row of their own. On a wide screen the row is as wide as the window, opaque, lettered at the right, with one line under it; it sticks directly under the top bar, whatever the bar's height, and a heading it jumps to lands under the row. Because the row spans the window, no heading can sit beside it or show through it. On a phone the program's row takes no screen while a visitor reads down the page and comes back the moment they scroll up; without the script it stays where it is written, between two sections, and takes no screen at all. The travel page's row stays in the page. Every link in it is at least 44 by 44.

### What is clickable
One system, in both themes (`sources/conversations/2026-11-21--org--links-clickable-and-dark-mode-love.md`). A reader can tell what is a link without pointing at it, and nothing that is not a link looks like one.
- **Headings and labels** are plain lettering: never underlined, no arrow, no pointer.
- **A link in a sentence** is underlined, 2px, in the lettering blue of its theme, 0.22em under the text. Pointed at, focused or pressed, it becomes a yellow marker stroke with night lettering. The rule never catches a card, a slot, a sticker or a button. Colour alone never marks a link.
- **A link on its own** ("See the program") is the same underlined lettering, a step larger, ending in a small drawn arrow that moves a little when pointed at. On a phone it is at least 44 pixels tall.
- **A link that leaves the site** ends in a small drawn corner arrow and tells a screen reader "(another site)". The compact rows of contact links under a place or a speaker (a website, a phone number, a map) are underlined without the arrow.
- **A sticker or card that is a link** (a day, a speaker, a supporter, an accepted event) carries the same small arrow in its lower corner, speaker cards, face stickers and supporter stickers included, and lifts when pointed at; the whole sticker is the link. A photo sticker that is not a link has no chip, no pointer and does not move.
- **A slot stamped "Yours?"** is always a link to where it invites. It answers as a whole: its outline turns solid, its fill lifts, its stamp grows.
- **The top bar** marks the page you are on with a filled tab, and a link pointed at with the same tab, lighter. **The footer** underlines its links and marks the page you are on.
- **A button** is the yellow sticker with its lip (night blue by day, a darker yellow at night); nothing else is filled yellow at rest, tags included.
- **Lettering that is not a link** (a step's lead-in, a venue's subtitle, "Added:") is ink, never link blue.
- Everything pressable has a pressed state, and the focus ring is as before.
- **A press on the goat is for the goat.** The goat stands inside the slot it visits, and where that slot is a link a press on the goat used to give the whole slot its pressed yellow (the rule above, added in round eight, broke the line under Motion that a tap never flashes the slot). Since round eleven (`sources/conversations/2026-11-22--org--goat-tap-flash-and-light-dark-cards.md`) a slot takes its pressed look only when the slot itself is pressed; its words then turn to the ink that reads on yellow; and the pointed-at look is kept for screens that have a pointer, so a touch on the goat leaves nothing behind on the slot.

### Back Cover
The footer as the album's back cover: night blue, the crest and mark in white, pale-album text, white links. The links sit in four groups, each a small lettered label in yellow (pale album on inner pages) over its links in one row: the four groups side by side on wide screens, one under another on phones, each link still 44 pixels tall there. Inner pages carry the same groups on the blue ground.

### Inner Page-head and Prose Page
Every inner page opens on a cover-blue strip: the crest home link, the sign in headline lettering, a pale-album lede, and a photo set as a sticker (white border, lift, 2 degrees). On a phone the photo is a small square sticker, 5.5rem, in the strip's top right corner beside the sign; a speaker's portrait, a supporter's logo and the mark keep their own size. The program, speakers and propose pages each open on their own picture, and no two pages of one footer group share one; a page with no fitting picture opens without one, its sign and lede across the strip. Below it, one white prose page at most 58rem wide, headings lettered in album blue, list markers in album blue, an album-blue table head on the budget ledger, and a printed-slot style empty state when a list has nothing yet.

### Loading Photo, Caret and Scrollbars
Until a photo loads, its place in a sticker shows an unprinted sticker: the page-print fill printed with the album's hoof marks in slot-line blue. The text caret is album blue on white and yellow on the blues; scrollbars are yellow on night blue.

### Motion
**Stickers stay still.** Stickers are stuck in from the first paint and do not animate as they come into view; the organiser found the peel and settle annoying (2026-10-27).

**Peek rise.** When an open slot or a speaker card is hovered or focused, its goat rises 0.45rem over 220ms on the same curve and settles back; reduced motion keeps it where it is.

**The companion's moves.** All by transform, nothing by position. It pops up with a stretch, an overshoot, a squash on landing and a settle (640ms); it ducks with a small lift and then down behind the edge (420ms). When a mouse pointer comes within 260px it turns its painted head towards it, and looks at you again when the pointer is over it. It hops between slots in an arc with a crouch, a stretch on take-off and a squash on landing (620 to 900ms), and turns its painted head towards where it is going. While it waits, every 3 to 6 seconds it bobs, wiggles, stretches, plays peek-a-boo or looks around, turning its painted head left and right with a small lift (300ms a turn); the turned heads load after the page, and until they arrive it looks at you. Tapped or clicked, it plays the next of its tricks, with a line said between each: a jump for joy (760ms), a somersault in the air (1000ms), and a shake of its painted head (left, right, left and back, 300ms a turn with 280ms between). The line shows in a yellow bubble beside its head, in the numbers' badge style, at most 12rem wide so a long line wraps, fitted to its longest line when it does, for 1300ms plus 45ms a character; it is picked at random, never twice running, from what every goat says and, for a speaker's goat, its own lines (tools/frame.py). A goat peeking over a slot is painted only down to the edge, so it bounces (no higher than 9% of its height) and ducks and pops up instead of jumping or flipping. A tap on the goat never follows the slot's link, selects the text around it or flashes the slot. Predrag Radenkovic's, Christoph Lipautz's, Amar Mahmutbegović's and Cristian Planas's whole sitting goats sit on their cards and bands instead of peeking, sized to stand as tall above the card as a peeking goat, and do the whole goat's tricks. On a band, a whole goat sits in front of it with its feet 1.4rem under the yellow line, as tall as the band allows below the page's clipped top edge. On a phone a band with a goat keeps 6.1rem clear on its right and fills each heading line before wrapping (text-wrap: pretty), so the heading wraps before the goat; the goat is 5.4rem wide, and the cook over the food section 7rem, with 7.4rem kept clear. A band with a peeking goat is at least 5.25rem tall on a phone, so a one-line band is as tall as its goat and the page's clipped top edge never cuts the horns.

**Goatchi.** The goat a visitor keeps sits on the left with a yellow bubble above it, its needs on the right as bars in the yellow, red below a quarter; on a phone, one above the other. Sulking, the goat is a little desaturated. Feeding shows the painted food scene for 2.6s, sleep the sleeping goat for 3.2s, and play a jump (760ms, none with reduced motion). Its own buttons are the site's yellow buttons; let go and the confirmations are underlined text buttons. It never mirrors the picture, and only the somersault turns it over.

**Goat wiggle.** On hover the die-cut goat turns from -6 to 4 degrees and grows 5% over 500ms on the same curve; reduced motion holds it still.

## Do's and Don'ts

### Do:
- **Do** show a decided fact as a stuck-in sticker and an undecided or open one as an empty printed slot, with its reason in the slot's explanation.
- **Do** give every sticker and slot the next number in the album's single sequence.
- **Do** keep stickers sticker-sized on wide screens, and on phones list the ones a visitor reads one after another, at most 26rem wide, as the Layout section says; the small grids named there stay two across.
- **Do** keep the gap between a band's intro line and its first row of stickers short: only a row with a goat peeking over it keeps room above it.
- **Do** set a small per-sticker tilt between -2 and 2 degrees, and vary it between neighbours.
- **Do** list the cover's three links one a row on a phone, and the host page's "What you could run" one slot a row with its number beside the words and its stamp at the left, clear of the goat (`sources/conversations/2026-11-22--org--fix-all.md`).
- **Do** keep a map's labels clear of its pins and space the pins for their phone size, where they are drawn 1.6 times larger and take a tap on a clear ring 44 across; a pin moved off its place keeps a line back to it.
- **Do** keep a goat's room beside a phone heading only while the goat is on it; the heading keeps the height it has with the room, so nothing moves when the goat comes.
- **Do** check every page type under forced colours: a logo keeps its tile, a swatch its colour, a number its ring, the page you are on its mark.
- **Do** show an opened section's words in full. The paragraph folds of round ten ("More about Tuzla", `sources/conversations/2026-11-22--org--fix-all.md`) were removed in round fourteen, when whole sections began to open and close (`sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md`); a fold inside a fold is one level too many. The only second level is the two long lists on a phone.
- **Do not** print photo credits on the site; the organiser decided on 2026-10-12 to show no credits (`sources/conversations/2026-10-12--org--no-photo-credits.md`).
- **Do** write plain sentences: one idea per sentence, common words, and no em dashes anywhere, including captions, alt text and generated pages.

### Don't:
- **Don't** use red for anything but the "Yours?" stamp.
- **Don't** put a fact on a sticker before it is true: an unconfirmed date stays "June 2027" on the fact sticker and an empty slot for the exact days.
- **Don't** give printed things (slots, printed numbers, stamps) a lift, or stuck stickers a dashed outline or a gloss.
- **Don't** write self-aware copy about the album, the design or the site itself; the page talks about the conference, Tuzla and the visitor.
- **Don't** add small labels above headings, glyph icons, or goat pictures beyond the mark and the mascot; the band, the numbers, the mark and the mascot carry the page.
- **Don't** let the goat cover a fact, stand in for text a screen reader needs, or appear on the code of conduct or budget content as a joke.

### Sanctioned detector exceptions
The detector exceptions in `.impeccable/config.json` that this world relies on:
- **nested-cards** on `site/index.html`: stickers and printed slots stuck on album pages are the album's grammar, sanctioned by the finish review of 2026-10-12.
- **clipped-overflow-container** on `site/*.html`: album pages clip to their rounded corners so the band has no seam; nothing positioned leaves the page padding.

Three older entries are inherited from the Korzo world and are now obsolete: **cream-palette** (it cites the retired Afternoon Stone page colour; the pages are now white and the ground album blue), and **tight-leading** and **cramped-padding** on `site/index.html` (their reasons cite Korzo type values and the `.hero__sign` and `.stop` elements, which no longer exist). They were removed from the config on 2026-10-14.
