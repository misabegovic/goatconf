---
title: "The \"I'm speaking\" cards show the session's title before it has a slot"
date: 2026-10-26
kind: conversation
---

After Paul Campbell's session, "The story of CARLOS", reached his page (sources/conversations/2026-10-26--org--paul-campbell-carlos.md), the organiser asked, verbatim:

> and on his card?

His card on the speakers page and his sticker on the home page already showed "Talk: The story of CARLOS", but his "I'm speaking" cards (square, wide and the link preview) still said "Tuzla · 3–5 June 2027": tools/shareables.py only took a title from a session on the program. Asked whether the cards should show the session title before it has a slot, the organiser chose "Yes, for every speaker (Recommended)".

So a speaker's cards now read "Talk: <title>" (or the record's own format) from the record's `talk` while the session has no slot, and the cards of the three speakers with one, Paul Campbell, Dejan Menges and Christoph Lipautz, are rendered again.
