# The program

One Markdown file per accepted session, named `<day>-<start>-<room>.md`
(for example `2027-06-03-1000-hall-ground.md`). The frontmatter is the
record; the body is the speaker's own short description. Copy
`_template.md` to start one. `title`, `speakers`, `format`, `day`, `start`,
`room` and `accepted` are required.

- `title`: the session's title.
- `speakers`: the speakers' names as they should appear, for example
  `Ada Lovelace and Grace Hopper`.
- `format`: `talk`, `panel`, `workshop` or `other`.
- `format_name`: optional, only with `format: other`: what the session is
  called, one line of at most 30 characters (for example `Live coding` or
  `Fireside chat`). It shows in place of "Session" on the program, the
  session's page, the speaker's page and `program.json`.
- `day`: `2027-06-03` or `2027-06-04`, the two core days.
- `start`: `"10:00"`, `"12:00"`, `"14:00"` or `"16:00"` on Thursday;
  `"09:30"`, `"11:30"`, `"13:30"` or `"15:30"` on Friday, which starts half an
  hour earlier so the midday break covers Džuma prayer. Every slot is one
  hour. Each day's times live in `DAY_PLAN` in `tools/program.py`.
- `room`: one of the room keys in `tools/program.py`.
- `profiles`: optional, a list of speaker file names from `speakers/`
  (for example `[ada-lovelace]`); the program then links the names to
  their profiles.
- `area`: optional, the session's area, or a list of areas (for example
  `[ai-ml, product]`), as the proposal form's area question gives them,
  where speakers pick all that apply: `engineering`, `ai-ml`, `data`,
  `ux-ui`, `product`, `research`, `business` (the business of software) or
  `leadership`. Each shows as a tag on the program, the session's page and
  the speaker's page and card, and `program.json` lists them as `areas`.
- `for`: optional, who the session is for: the speaker's answer to the
  form's "Who is it for?", lightly trimmed to one line of at most 100
  characters without changing what it says. It shows as a "For:" line
  beside the tags, and both go into `program.json`.
- `accepted: yes` once the organiser has accepted the proposal and the
  speaker has confirmed.
- `signup`: optional and unused for now: a link where people save a seat in
  the session, if session sign-ups are introduced later. Once set, the program,
  the speaker's page and the agent files show it as "Save a seat".

Then run `python3 tools/program.py build` to rebuild `site/program.html` and
each session's own page, `site/session-<title>.html` (for example
`session-salt-goats-and-servers.html`), which the session's sticker on the
program opens. Two sessions may not share a title, since the title names the
page.
`python3 tools/program.py check` checks the records; the local CI runs both.
