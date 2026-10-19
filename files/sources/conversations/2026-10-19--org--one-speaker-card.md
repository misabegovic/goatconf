---
title: "One speaker card on the home page and the speakers page"
date: 2026-10-19
kind: conversation
---

After each session's area and "For:" line showed on the speakers page
(PR #133), the organiser wrote, verbatim:

> Should we also render that on the homepage for speakers? Why are we using different cards for speakers on different sites? Shouldn't we use the same card type?

The agent found no recorded decision behind the two cards: the home page
built its own compact sticker (`speaker_sticker` in `tools/home.py`, role
and talk inside the blue name band, a square photo), and the speakers page
built another (`speaker_card` in `tools/speakers.py`, role, talk, area and
"For:" line on white under the band), each with its own CSS, and they had
drifted apart.

Asked which card both pages should use, the organiser picked "The speakers
page card": one builder for both pages, the home page keeping its album
numbers and its "Your session here?" places.
