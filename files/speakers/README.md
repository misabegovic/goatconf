# Speakers

One Markdown file per speaker with an accepted session who agreed to a
public profile, named after them in lowercase words joined by hyphens
(for example `ada-lovelace.md`). Copy `_template.md` to start one. The body
is their bio in their own words, at most 120 words.

- `name`: required.
- `publish: yes`: required. The speaker agreed to this public profile; the
  check refuses a record without it.
- `photo`: optional, a file the speaker sent, saved under
  `site/img/speakers/`. Without one the profile shows the goat.
- `links`: optional, a list of web addresses.

Link a session to its speakers with `profiles: [ada-lovelace]` in its
record under `program/`. Then run `python3 tools/speakers.py build` and
`python3 tools/program.py build`. The local CI checks both.

Leave out lines you do not use. `travel_funded_by` is retired: no
supporter pays for a named speaker's travel, and the check refuses it.
