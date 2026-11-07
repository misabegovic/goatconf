---
title: "The speaker pages ask you to register, and their session text reads at body size"
date: 2026-11-07
kind: conversation
---

After the program page's change, the organiser asked, verbatim:

> What do you think of the speakers page?

The agent's view: the speaker pages are the site's strongest, but
neither the speakers page nor any speaker's page asked the visitor to
register (only the menu and the footer link to it), though the speaker
cards and announcement posts link straight to the speaker pages. It also
noted the speakers page's intro of caveats, its classroom header photo,
the full-width phone cards (about 5,600 px for eight), and the session
text set smaller and lighter than the bio.

Asked, the organiser chose:

- **Register:** on every speaker's page, and on the speakers page.
- **Session text:** at body size and full ink, like the bio.
- **Left as they are:** the speakers page's intro, the phone cards, and
  the header photo.

Built as, by tools/speakers.py:

- Every speaker's page, under their session: a button "Register for
  free to hear [first name]" to the Luma event, with "Free, for
  everyone. Luma emails you when you are in.", before "See the whole
  program" and "All speakers".
- The speakers page closes on "Come and hear them": the two days, the
  hallway track and Saturday at the lakes, the same register button, and
  beside it "Want to be on this page?" with the open call and a link to
  propose a session.
- The buttons' links come from forms.yml through tools/formlinks.py, as
  on the register page; the speaker pages do not load Luma's checkout
  script, so the button opens Luma's own page.
- A speaker's session description is set at the bio's size and ink.
