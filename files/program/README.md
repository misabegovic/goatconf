# The program

One Markdown file per accepted session, named `<day>-<start>-<room>.md`
(for example `2027-06-03-1000-hall-ground.md`). The frontmatter is the
record; the body is the speaker's own short description. Copy
`_template.md` to start one.

- `format`: `talk`, `panel`, `workshop` or `other`.
- `day`: `2027-06-03` or `2027-06-04`, the two core days.
- `start`: `"10:00"`, `"12:00"`, `"14:00"` or `"16:00"` on Thursday;
  `"09:30"`, `"11:30"`, `"13:30"` or `"15:30"` on Friday, which starts half an
  hour earlier so the midday break covers Džuma prayer. Every slot is one
  hour. Each day's times live in `DAY_PLAN` in `tools/program.py`.
- `room`: one of the room keys in `tools/program.py`.
- `profiles`: optional, a list of speaker file names from `speakers/`
  (for example `[ada-lovelace]`); the program then links the names to
  their profiles.
- `accepted: yes` once the organiser has accepted the proposal and the
  speaker has confirmed.
- `signup`: optional and unused for now: a link where people save a seat in
  the session, if session sign-ups are introduced later. Once set, the program,
  the speaker's page and the agent files show it as "Save a seat".

Then run `python3 tools/program.py build` to rebuild `site/program.html`.
`python3 tools/program.py check` checks the records; the local CI runs both.
