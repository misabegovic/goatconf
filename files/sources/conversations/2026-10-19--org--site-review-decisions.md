---
title: "A full review of goatconf.com, and the organiser's call on each finding"
date: 2026-10-19
kind: conversation
---

The organiser asked, verbatim:

> I want to explore and review the entire website. and explore if there are any issues, inconsistencies, dry instances, things to improve, especially from a perspective of a person visiting the website, but also from structural points of view

The site was reviewed on 2026-10-19 from four sides (the visitor, the facts
against the brain, the code's structure, and accessibility, search and
speed), and looked at in a browser at desktop and phone widths. Shown the
findings, the organiser wrote, verbatim:

> ok, lets go through these one by one and make decisions for each. ask me one by one

Their answers, one question at a time:

**Facts that were stale or contradicted each other**

1. **Jan Grodowski's cards and photo**, reachable on goatconf.com by their
   address while his record is on hold: "Leave as is".
2. **The register page's "The organiser confirms each registration,
   usually within a few days."**: "Drop the sentence". It reads "Tickets
   are free. Leave your name and email, and Luma emails you when you are
   in."
3. **The code of conduct's search and preview text, "how to reach the two
   people who enforce it"**: "how to make a report". It reads "…and how to
   make a confidential report."
4. **The home page's "The organiser pays for no food or drink"**, against
   the speakers dinner the organiser pays for: "No food or drink is
   provided".
5. **llms.txt's "Speakers pay their own travel; a refund only if the
   budget allows", and the agent and calendar files calling the lake day
   and the goat hunt "events people add"**: "Match the pages".
6. **The program page's "No evening events or meetups yet"**, below the
   BH Professionals Meetup: "Drop the line".
7. **The speakers page's "Each session is on the program with its day,
   time and room"**: "Slots come later". It reads "Days, times and rooms
   are set closer to the event; the program shows each session once it
   has its slot."
8. **The contact page's "To add an event or support GoatConf: use the
   proposal form"**: "Split into two lines", one to propose an event and
   one to the supporters page.
9. **The propose an event page's recording line without the budget
   caveat**: "Add the caveat".
10. **The program page's "Every slot is one hour: a talk with time for
    questions, a panel, or a workshop"**: "Add both", something else and
    two half-hour sessions sharing a slot.

**What a first-time visitor runs into**

11. **The program's 50 open cards against 6 reserved**: "Keep the full
    grid".
12. **No dates for would-be speakers** (no deadline, no reply time):
    "Keep it open".
13. **"What is decided" as the first stickers' heading, with "In English"
    and "120 to 300 people" further down**: "Leave it".
14. **The home page's length, with the food table and the price list**:
    "Leave it".
15. **Breaks read "Coffee on Freedom Square, one hour"**: "Hour off: cafés
    on Freedom Square".
16. **"The organiser" 41 times in visitor text, mixed with "we"**: "We"
    throughout, naming the organiser where a person matters.
17. **The travel page reading like research notes, with four date and four
    currency formats**: "Visitor-friendly, one format".
18. **A "Good to know" section on the travel page**: "Add, known facts
    only" (the time zone, the venue's Wi-Fi, flying into Sarajevo).
19. **The supporters page: who a supporter reaches, a button, and the
    unnamed Austrian business.** The organiser wrote, verbatim:

    > do 1. and maybe dont mention the austrian business part, just mention they can reach me

    Read as: add the audience line and a "Become a supporter" button, drop
    the Austrian business from the site, and say supporters can reach the
    organiser.
20. **The open-source wording in the full code of conduct**: "Leave it".
    Guide dogs were not asked again: the organiser decided "Keep it as it
    is" on 2026-10-13
    (`sources/conversations/2026-10-13--org--outside-review-fixes.md`).

**Repeated and inconsistent text**

21. **The goat story told three ways**: "One man", the full story once, in
    "Why a goat".
22. **Lines repeated across pages** (the Ruby line, the recording caveat,
    the session seats, "More than one of each"): "Leave them".
23. **The events page's four names, linked from one footer**: "Events
    people add", in every footer.
24. **Three date windows for events people add**: "Only 2–6 June".
25. **"Run a session", "Propose a session" and "How to propose a
    session"**: "Propose a session" everywhere.
26. **The airport at "about 13 km" and "about 13 to 16 km"**: "About 15
    km".

**What the browser showed**

27. **The empty left half of the home cover on desktop**: "Leave it".
28. **The tall "3–5 June" sticker with one small line.** The organiser
    wrote, verbatim:

    > leave it for now, I will iterate a bit later on some design changes on the hero section

29. **The program's day switcher floating over the room cards**: "Give it
    a backing strip".

**Speed, accessibility and search**

30. **Seal and lockup SVGs at 184 KB each, from an embedded font**: "Text
    to outlines".
31. **About 5.4 MB of photos on the home page**: "WebP + sizes".
32. **12 published images no page uses**: "Move out of site/" (Jan
    Grodowski's photo stays, per answer 1).
33. **No 404 page**: "Add a GoatConf 404".
34. **The page title outside `main` on inner pages, and `id="goat"` twice
    on the home page**: "Fix both".
35. **The travel maps' pins.** The organiser picked hiding the pins from
    keyboards and screen readers, with the list as the accessible version
    and bigger pins on phones, and wrote, verbatim:

    > do 1. but also when someone clicks on a pin, they are led to the place of that pin on the list...

36. **Links in white areas hard to tell from text**: "Blue underline in
    white areas".
37. **The heading font preloaded only on the home page, and larger than
    needed**: "Preload everywhere + trim".
38. **The home page's 353-character description**: "Facts first": "A free
    conference for people who build and sell software, in Tuzla, Bosnia
    and Herzegovina, 3–5 June 2027. Any language, any stack."

**Structure**

39. **The page frame copied in about 13 places, six marker styles, no
    single rebuild command**: "ADR, then refactor".
40. **A site lint step in the local CI**: "Add it, in the same ADR".
41. **The day hours typed outside the program's day plan**: "Yes, in the
    ADR".
42. **About 25 dead CSS rules and phone rules overriding each other**:
    "All of it now".
43. **Merges publishing without a check of the merged result**: "Rebase
    before merge".
44. **site/README.md published at goatconf.com/README.md**: "Move it out
    of site/".

Asked how the changes should land, the organiser picked "~10 themed PRs":
stale facts first, then wording and labels, supporters, travel, page
structure and the 404 page, speed, CSS, the README move, the PR skill, and
the ADR draft, each stopping before the merge.
