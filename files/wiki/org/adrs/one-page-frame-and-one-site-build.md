---
title: "Give every page one shared frame, one marker style and one build, and lint the HTML"
kind: decision
status: accepted
updated: 2026-10-19
confidence: medium
depends_on:
  - org/prds/website-and-registration.md
sources:
  - sources/conversations/2026-10-19--org--site-frame-adr-approved.md
  - sources/conversations/2026-10-19--org--site-review-decisions.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-07--brain--local-ci-only.md
---

# Give every page one shared frame, one marker style and one build, and lint the HTML

Proposed on 2026-10-19 from the organiser's review of the whole site, where
they answered "ADR, then refactor" for the page frame, "Add it, in the same
ADR" for an HTML check, and "Yes, in the ADR" for taking the day hours from
the program's day plan (source:
sources/conversations/2026-10-19--org--site-review-decisions.md). Accepted
the same day: the organiser approved it with the HTML check to land first,
each step in its own pull request with before and after screenshots
(source: sources/conversations/2026-10-19--org--site-frame-adr-approved.md).

## Context

The site is plain HTML and CSS with no build step for the hand-written
pages, published from `site/` on every merge to `main` (source:
sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md).
Some pages are written whole by generators in `tools/` (the program, the
speakers and supporters, the events people add), and some hand-written pages
carry generated parts (the top bar, the link-preview tags, the home page's
days, speakers and supporters, the travel page's maps). The review of
2026-10-19 found the cost of that mix (source:
sources/conversations/2026-10-19--org--site-review-decisions.md):

- **The page frame is copied in about thirteen places.** The head
  boilerplate, the footer and the goat sprite are copied by hand into each
  hand-written page and written again, separately, by three generators. Only
  the top bar is written from one place and checked. The footer drifted as a
  result: until 2026-10-19 only the home page's footer linked the events
  people add.
- **Six marker styles.** Each tool marks its generated parts its own way, and
  the home page alone is written by six tools. Nothing says which tool owns a
  block.
- **No single rebuild.** After a speaker change, four tools have to be run in
  the right order, and only experience says which.
- **Facts typed twice.** The core days' hours live in the program's day plan,
  and are typed again in the program page's prose, in llms.txt and on the
  register page; CI would not notice them drift.
- **CI checks generated output, not HTML.** The local CI checks that every
  generated page and block is current, but not that a page's tags balance,
  its ids are unique, its links and anchors resolve or its images exist. The
  review found a duplicated id on the home page by hand.
- **Repeated helpers.** Reading records, and the write-or-check loop, are
  written out in each generator.

## Decision

Keep plain HTML that is served as it is, with generated parts. Add no
template engine and no build step for publishing. Within that:

1. **One frame module.** A shared module in `tools/` owns the head
   boilerplate, the footer and the goat sprite, and uses the top bar the
   navigation tool already writes. The generators build their pages through
   it. Hand-written pages carry the footer and the sprite as generated
   blocks, which the module writes and the local CI checks, the way the top
   bar is written and checked today. A link added to the footer is added in
   one place.
2. **One marker style.** Every generated block opens and closes with the same
   kind of comment, naming the block and the tool that owns it, and one
   shared helper replaces a block. The existing blocks move to it.
3. **One build.** One command builds the whole site, running every generator
   in the order they depend on each other, and its check mode is what the
   local CI runs for the generated parts.
4. **The day plan, once.** The core days' hours in the program page's prose,
   in llms.txt and on the register page come from the program's day plan.
5. **An HTML lint in the local CI.** A check using only Python's standard
   library reads every page and fails on unbalanced tags, duplicate ids,
   internal links or anchors that do not resolve, images that are missing or
   have no alt text, and more or fewer than one `h1`, one `main` and one
   banner. It lands first, so the refactor behind it has a safety net.
6. **Shared helpers.** Reading records, escaping, frontmatter and the
   write-or-check loop move into one module the tools import.

## Alternatives

- **A template engine** (Jinja or similar, with a template and a built copy
  of every page). It removes the copying completely, but puts every page in
  two places, adds a real build step before publishing, and makes the pages
  harder to edit in place, against the plain-HTML stance of the site.
- **A static site generator** (Eleventy, Astro and the like). The same gains
  and costs as a template engine, plus a Node toolchain this repository does
  not otherwise need.
- **A footer check only.** The smallest step: check the footer like the top
  bar, and leave the rest. It stops the drift that was seen, but not the
  copies, the markers, the rebuild order or the doubled facts.
- **Do nothing.** Every new page and footer link stays a hand edit in many
  places, and the next drift is found by a visitor.

## Consequences

- **Closes** hand edits to a page's frame: the footer, the sprite and the
  head are changed in the frame module, and the CI refuses a page whose
  frame differs.
- **Opens** new pages with the full frame for nothing, one command to bring
  the site current, and a CI that catches broken HTML, ids, links and images
  before they are published.
- **Costs** a refactor across the generators, the hand-written pages and the
  tests, in several small pull requests (the lint first, then the helpers,
  the frame, the markers and the build, then the day plan), each checked by
  full-page screenshots at phone, tablet and desktop widths. Every page's
  diff is noisy once, when its frame moves into marked blocks. The local CI
  takes a few seconds longer.
- **Keeps** the publish workflow as it is: CI stays local, as decided on
  2026-10-07 (source: sources/conversations/2026-10-07--brain--local-ci-only.md).

## Open questions

- Should the 404 page come from the frame too? It differs (a base address, no
  link-preview tags, not in the sitemap), so it may stay hand-written.
- Should the lint also warn, without failing, on images that lack a width
  and height?
- Should the one build also render the share cards and the brand files? They
  need Chrome, so the proposal leaves them out, as their own commands.

## Related

- [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md)
- [Build the pages in plain HTML and CSS](design-with-impeccable.md)
- [Website and registration](../prds/website-and-registration.md)
- `sources/conversations/2026-10-19--org--site-review-decisions.md`
