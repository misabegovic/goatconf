# Speakers

One Markdown file per confirmed speaker. Every speaker
agrees on the talk form to a public profile and to social media promotion
(required since 2026-10-13), named after them in lowercase words joined by hyphens
(for example `ada-lovelace.md`). Copy `_template.md` to start one. The body
is their bio in their own words, at most 120 words.

- `name`: required.
- `publish: yes`: required. The speaker agreed to this public profile on the
  talk form; the check refuses a record without it.
- `hold`: optional, one line of at most 80 characters while a record
  must stay off the site, for example `waiting for his employer's
  approval`. The record is kept and checked, but the speaker comes off
  the speakers page, the home page and the files for agents, and their
  own page is removed from `site/` on the next build, until the line is
  gone. Their `order` keeps its place in the no-two-share check, and a
  session reaching the program while they are held still fails the
  check.
- `photo`: optional, a file the speaker sent, saved under
  `site/img/speakers/`. Without one the profile shows the goat.
- `links`: optional, a list of web addresses.
- `support_them`: optional, ways people can support the speaker (their
  book, their open-source project, their company), each a short `text` and
  a `url` starting `https://`, shown on their page under "How to support
  them", for example `- {text: "Read her book", url: "https://example.com"}`.
  The speaker agrees to these as they agree to their profile.
- `order`: optional, a whole number from 1 setting where the speaker is
  listed: on the speakers page, the home page and the files for agents, 1
  comes first. The organiser sets it by the speaker's standing, not the
  alphabet. Speakers without one come after, by name. No two speakers may
  share a number; the check refuses it.
- `role`: optional, one line of at most 80 characters saying what they do
  and where, as they would put it (for example `Staff Engineer at Vinted`,
  `Independent consultant`). It shows under their name on their page, the
  speakers page, the home page, their "I'm speaking" cards and the files for
  agents. Text only: an employer's logo never appears, so it cannot read as
  a supporter.
- `talk`: optional, the title of the session they proposed, one line of at
  most 80 characters (for example `Back to the Future`). It shows on
  their page, their card on the speakers page, their sticker on the
  home page and their "I'm speaking" cards while the session has no slot.
- `talk_about`: optional, their own words on what the session is about,
  at most 300 words; it needs `talk`. Separate paragraphs stay separate
  paragraphs on the page.
- `talk_format`: optional, `talk`, `panel`, `workshop` or `other`; a talk
  if left out.
- `talk_format_name`: optional, only with `talk_format: other`: what the
  session is called, one line of at most 30 characters (for example
  `Live coding`). It shows in place of "Session"; it needs `talk`.
- `talk_area`: optional, the session's area, or a list of areas (for
  example `[ai-ml, product]`), as the proposal form's area question gives
  them: `engineering`, `ai-ml`, `data`, `ux-ui`, `product`, `research`,
  `business` (the business of software) or `leadership`. Each shows as a
  tag on their page and their card on the speakers page.
- `talk_for`: optional, who the session is for: their answer to the form's
  "Who is it for?", lightly trimmed to one line of at most 100 characters
  without changing what it says (for example `anyone working with
  real-life codebases`). It shows as a "For:" line next to the tags.

A confirmed speaker can be added before their session has a slot (since
2026-10-14): their page then says the session will be on the program
soon, or, when the record carries `talk` and `talk_about`, shows the
session's title and their words on it with the day and time to be
announced (since 2026-10-15). Remove both once the session is on the
program: the program record is its source then, and the check refuses a
record that keeps a second copy of a session. If they have not sent a
photo or a bio, a public one from their own site or a conference they
spoke at may be used, with where it came from recorded under
`sources/web/speakers/`.

Link a session to its speakers with `profiles: [ada-lovelace]` in its
record under `program/`, and drop the speaker record's `talk`,
`talk_about` and other `talk_` fields in the same change, carrying the
area and who it is for over as the program record's `area` and `for`. Then run `python3 tools/speakers.py build`
and `python3 tools/program.py build`. The local CI checks both.

Each speaker has three cards made by `python3 tools/shareables.py render`
(it needs Chrome): `speaker-<name>-square.png` and `-wide.png` to post, and
`-preview.png`, the 1200 by 630 image their page shows when its link is
shared. Their page shows the wide card under "Your card: I'm speaking",
with both sizes to download, as a supporter's page shows theirs.
GoatConf's own card announcing them, "Confirmed speaker at GoatConf 2027"
(`speaker-<name>-announce-square.png` and `-wide.png`), links to their
page; it shows under "The announcement card" and is what the drumbeat's
spotlights post. The local CI fails while a published speaker lacks it. Render them before building the pages; the local CI fails while a
published speaker has no preview card, so a shared link never falls back to
the generic banner. Render them again when a name, role or photo changes.

Leave out lines you do not use. `travel_funded_by` is retired, and the check refuses it: a speaker's
own company that covers their travel is a supporter record in
`supporters/` instead, like Meister for Christoph Lipautz.
