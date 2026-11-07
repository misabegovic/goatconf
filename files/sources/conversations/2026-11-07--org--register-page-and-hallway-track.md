---
title: "The register page refreshed, and the hour off named as the hallway track"
date: 2026-11-07
kind: conversation
---

After the travel page's redesign, the organiser asked, verbatim:

> What do you think of the register page?

The agent's view: it works and is honest (the button first, the days
from DAY_PLAN, a clear "Your data"), and it should stay short, but it
never linked to getting here or said what the trip costs, gave no reason
to come at the last step (no speakers, no hour off, no Saturday), read
"Seats" as one block that sounds like "you might not get in", repeated
"free" three times, and looked unlike the talk and travel pages.

Asked, the organiser chose:

- **Scope:** a light album refresh, staying short.
- **Speakers:** a small strip of the published speakers' photos and
  names, generated from the speaker records, with a link to the speakers
  page.
- **Lines to add:** getting here and its cost, the hour off, and
  Saturday at the lakes. Not chosen: a line that food is your own.

With the hour off, the organiser wrote, verbatim:

> You know, the hour off is supposed to highlight the importance of the hallway track and networking. We don't mention that anywhere on the site

The agent confirmed that "hallway track" and networking appeared nowhere
on the site; the hour off was described only by where it happens. Asked,
the organiser chose:

- **Where:** everywhere the hour off is named: the register page, the
  home page's days, the talk page, the program page's intro (and each
  session page's line) and llms.txt; the program's "Hour off" rows stay
  short.
- **Wording:** name it, then explain: "the hallway track, in the cafés
  on Freedom Square. Meet the speakers and each other." The agent left
  out the offered phrase "the people who build what you use", since not
  every speaker builds something people use.

Built as:

- register.html as album pages: "Your ticket" (the button and the
  volunteer line beside four stickers: Free, Two days, Hour off, Saturday),
  "Who is speaking" (every listed speaker's photo and name, written by
  tools/home.py into a new register-speakers part), "The days" with
  "Seats in the rooms" as three steps, "Getting here" with the routes, a
  room from about 38 € a night and a link to the travel page, and "How it
  works" beside "Your data". The lede names the hallway track.
- The home page's day stickers read "Hours off, for the hallway track:
  the cafés on Freedom Square and lunch in town." (tools/home.py).
- The talk page's lede, its "An hour off" sticker and its slot list name
  the hallway track.
- The program page's "How a day runs" and every session page's line say
  the hour off is the hallway track, to talk to the people you just heard
  and meet each other (tools/program.py).
- llms.txt's Format line: "with an hour off after each slot: the hallway
  track, in the cafés on Freedom Square, to meet the speakers and each
  other." (tools/agents.py).
