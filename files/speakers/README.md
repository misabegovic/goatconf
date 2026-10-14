# Speakers

One Markdown file per confirmed speaker. Every speaker
agrees on the talk form to a public profile and to social media promotion
(required since 2026-10-13), named after them in lowercase words joined by hyphens
(for example `ada-lovelace.md`). Copy `_template.md` to start one. The body
is their bio in their own words, at most 120 words.

- `name`: required.
- `publish: yes`: required. The speaker agreed to this public profile on the
  talk form; the check refuses a record without it.
- `photo`: optional, a file the speaker sent, saved under
  `site/img/speakers/`. Without one the profile shows the goat.
- `links`: optional, a list of web addresses.
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

A confirmed speaker can be added before their session has a slot or a
topic (since 2026-10-14): their page then says the session will be on the
program soon. If they have not sent a photo or a bio, a public one from
their own site or a conference they spoke at may be used, with where it
came from recorded under `sources/web/speakers/`.

Link a session to its speakers with `profiles: [ada-lovelace]` in its
record under `program/`. Then run `python3 tools/speakers.py build` and
`python3 tools/program.py build`. The local CI checks both.

Leave out lines you do not use. `travel_funded_by` is retired: no
supporter pays for a named speaker's travel, and the check refuses it.
