---
title: "Christoph Lipautz's talk shows on his page, and his other public profiles join his links"
date: 2026-10-15
kind: conversation
---

The organiser wrote, verbatim:

> nice. now, I don't think we added all information we could about
> Christoph? his page is missing some information about his session at
> the very least. idk about his profile

Done on 2026-10-15:

- Speaker records gain optional `talk` and `talk_about` fields: the
  proposed session's title and the speaker's own words on it, shown on
  their page and card with the day and time to be announced while the
  session has no slot. Once a program record links the session the
  fields come off the record; the check asks for that. Documented in
  `speakers/README.md`, tested in `tests/test_speakers.py`.
- His record now carries "Back to the Future" and his words on it,
  verbatim from the form: the abstract paragraph and the answer to
  "Who is it for?"
  (sources/cfp/2026-10-15--christoph-lipautz--back-to-the-future.md).
  The slot stays "Decide later"
  (sources/conversations/2026-10-15--org--christoph-lipautz.md), and
  his preference for Thursday 3 June stays in the form copy.
- His `links` gain his public GitHub and Bluesky profiles, found and
  verified on 2026-10-15
  (sources/web/speakers/christoph-lipautz-github-2026-10-15.md,
  sources/web/speakers/christoph-lipautz-bluesky-2026-10-15.md); the X
  link he gave stays first.
- His page's session block, the speakers page card and the shared-link
  description now say the talk, in place of "The session will be on the
  program soon."
