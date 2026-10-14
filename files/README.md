# goatconf

The knowledge base for goatconf, the conference: an LLM-maintained wiki
of the program, speakers, sponsors, venue, attendees and the decisions
behind them.

Two rules hold for supporters: **they are online only** (one level, 500
EUR, invoiced by the organiser's Austrian business, nothing at the venue;
or they pay a supplier directly), and **they never buy content**. The
budget is private.

This repository is meant to be public. Anyone can add a side event,
workshop, hub or activity by pull request (see `AGENTS.md`).

It is a brain in the LLM-wiki pattern, scaffolded empty on 2026-10-07
and inheriting its machinery (governance, skills, templates, validator,
hooks, CI) from [claude-brain](https://github.com/misabegovic/claude-brain).
[`AGENTS.md`](AGENTS.md) is the schema agents follow; `CLAUDE.md` links
to it.

On 2026-10-08 the repository also became a
[pi-brain](https://github.com/misabegovic/pi-brain) clone: the root now
carries the pi-brain substrate and everything goatconf moved under
`files/`, which from the repository root is this directory: the brain
home described above.

## Layout

- `sources/`: raw inputs, immutable once added.
- `wiki/`: the synthesis; `wiki/index.md` is the home.
- `log/log.md`: the operations log.
- `site/`: the website, plain HTML and CSS, published at goatconf.com on GitHub Pages (see `site/README.md`).
- `extensions/`: one file per extension people add around the conference (see `extensions/README.md`).
- `program/`, `speakers/`, `supporters/`: one file per accepted session, speaker and supporter, built into the site (each folder has a `README.md`).
- `places/places.yml`: the places to eat and stay shown on the travel page.
- `forms.yml`: the addresses of the Google Forms and the Luma event the site links to.
- `tools/`: `brain.py` (validate, check, views, search, stats), the generators that build and check parts of the site (program, speakers, extensions, places, navigation, link previews, files for agents), hooks, templates, CI.
- `.claude/`: skills, slash commands, agent personas, settings. Sessions start at the repository root, whose `.claude/settings.json` links to the settings here.

## Getting started

```bash
tools/setup-local.sh      # prerequisites, venv, git hooks, and a first CI run
bash tools/ci-local.sh    # the full CI, any time
```

CI is local only. The one GitHub Actions workflow publishes `site/` to
GitHub Pages and checks nothing. Every `git push` runs
`tools/ci-local.sh` first and is refused if a step fails. What it checks
is listed in [`AGENTS.md`](AGENTS.md) § Local CI. Its checks look only at
this folder, not at the pi-brain layer at the repository root.

Then talk to the agent: `/in <source>` to add material, `/capture org`
for something just decided, `/ask <question>` to query, `/shape` to turn
an idea into a pitch, PRD or ADR.
