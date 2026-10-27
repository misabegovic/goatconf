---
title: "GoatConf sticker packs: one set, as transparent images, a print sheet and a Telegram pack, on a Stickers page"
kind: decision
status: accepted
updated: 2026-10-27
confidence: medium
depends_on:
  - org/prds/design-with-impeccable.md
sources:
  - sources/conversations/2026-10-27--org--sticker-packs.md
  - sources/conversations/2026-10-27--org--speaker-goats.md
  - sources/conversations/2026-10-27--org--goat-mascot.md
  - sources/web/organiser/euruko-2024-figma-file-2026-10-27.md
  - sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md
---

# GoatConf sticker packs: one set, as transparent images, a print sheet and a Telegram pack, on a Stickers page

Proposed on 2026-10-27. The organiser asked for the goats to be
"downloadable as sticker packs", and for "sticker packs for goatconf that
can be downloaded... not only goats, just stickers in general for the
conference". Asked one question at a time, they chose digital and printable
packs, all four kinds of sticker, and a Stickers page (source:
sources/conversations/2026-10-27--org--sticker-packs.md). Accepted the same
day: the organiser chose "Approve, start building".

## Context

- **The site is already a sticker album.** Stickers, numbers and "Yours?"
  stamps are its look (see [design with impeccable](design-with-impeccable.md)).
- **The goat is drawn in code.** One goat in parts, its roles from the
  EuRuKo 2024 goat multiverse, and each speaker's own goat from their photo,
  all drawn by `tools/goats.py` ([the goat mascot](goat-mascot.md)).
- **The mark is downloadable already.** The brand page offers the seal and
  the coin, built by `tools/brand.py` (source:
  sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md).
- **Stickers were part of EuRuKo 2024.** The 2024 print order had an A5
  sticker sheet per attendee, and the design file has a sticker pack with the
  goat, the hex mark and the event's motifs (source:
  sources/web/organiser/euruko-2024-figma-file-2026-10-27.md).
- **Image tools are at hand.** The share cards are HTML rendered to PNG by
  headless Chrome (`tools/shareables.py`), which can also print a page to PDF.

## Decision

1. **One set of stickers, drawn in code.** Every sticker is an SVG drawing in
   the site's colours with a white die-cut edge, so it reads as a sticker on
   any background. The goats come from `tools/goats.py`; a new tool draws the
   rest and builds the packs.
2. **Four groups in the first set.**
   - **The goat's roles:** the goat, the speaker, the host with fes and
     fildžan, the coder, the cook, the Pannonian pirate and the hidden goat,
     whole and sitting.
   - **The speaker goats:** each published speaker's own goat, in a pack of
     their own, with the speaker's name under it.
   - **The mark and words:** the seal, the coin, the "Yours?" stamp, "I'm
     speaking", "Tuzla, 3–5 June 2027", "The one that feeds the community",
     and hoof prints.
   - **Tuzla things:** a salt crystal, a wave of the Pannonian sea, a
     fildžan, ćevapi, burek, the goat statue and the salt lakes.
3. **Three ways to take them.**
   - **A zip of transparent images:** every sticker as a 512-pixel PNG,
     which chats and slides take as it is, with the SVG beside it.
   - **A print sheet:** an A4 PDF with the stickers laid out with cutting
     room, to print at home or take to a print shop.
   - **A Telegram pack:** the PNGs already meet Telegram's rules for static
     stickers (512 pixels on the long side). Creating the pack with
     Telegram's sticker bot is done from the organiser's own account, so it
     is the organiser's act; once it exists, its link goes on the page.
4. **A Stickers page.** A new page, `stickers.html`, shows every sticker,
   group by group, with the downloads, and the footer and the brand page link
   to it. Each speaker's page offers their own goat as a sticker to download.
   The page says the stickers are free to use for sharing GoatConf, and that
   the speaker goats show real people, to share and not to mock.
5. **A speaker's change reaches the packs.** The packs are built from the
   same records as the site, so a speaker who asks for a change, or for no
   goat, is changed or removed in the next build; the local CI checks the
   packs are current, as it does the share cards.
6. **Built in small steps, each shown in the browser first.** First the
   page with the goat's roles and the mark and words, the zip and the print
   sheet; then the Tuzla things; then the speakers' pack and each speaker's
   sticker; the Telegram link when the organiser has created the pack.

## Alternatives

- **Chat packs only.** Easiest to share, but nothing to print, and every app
  has its own rules. Not chosen.
- **A print sheet only,** like 2024's. Good at the event, little use before
  it. Not chosen.
- **Stickers drawn by hand as image files.** Free in style, but every
  change, and every new speaker, means drawing again; the code-drawn goat
  already has the speakers' traits. Not chosen.
- **Stickers on the brand page.** Fewer pages, but the brand page is for the
  mark, and the stickers would crowd it. Not chosen.
- **Do nothing.** The goats stay on the site only.

## Consequences

- The repository carries the PNGs, the zip and the PDF, a few megabytes,
  rebuilt when a sticker or a speaker changes.
- The footer gains a link; the brand page gains a pointer.
- A new speaker gets their sticker as soon as their goat is in their record.
- The Telegram pack depends on the organiser creating it, and is updated by
  hand through the bot when stickers change.

## Open questions

- WhatsApp and Signal packs, which need their own app or upload steps.
- Printed stickers for the event itself, and who pays for them, which is a
  budget question and stays off the site.

## Related

- [The goat mascot](goat-mascot.md): the goat, its roles and the speaker
  goats.
- [Design with impeccable](design-with-impeccable.md): the album look.
- sources/conversations/2026-10-27--org--sticker-packs.md
