---
title: "The travel page, redesigned: ways in first, then what things cost"
date: 2026-11-07
kind: conversation
---

After the talk page's redesign, the organiser asked, verbatim:

> Ok. What do you think of the travel page? Should we improve it?

The agent's view: the facts are thorough, dated and honest, and the two
drawn maps are the page's best part, but it read as a reference document.
It was one prose page, about 12,000 px tall on a desktop and 16,500 px on
a phone, opening on a PDF download, with "which airport, how long, what
does it cost" spread over five dense bullets, the low cost scattered
between "Staying" and "Money", no way to jump around, and 20 car rental
names and 21 places to eat in full.

Asked, the organiser chose:

- **Scope:** an album redesign like the talk page, keeping every current
  fact.
- **Lead with:** the ways in, then what things cost.
- **The 21 places to eat:** stay on the page, folded on phones.
- **The open lines:** the hotel block is still waiting ("We are still
  waiting to hear whether IPI Academy can offer a block of rooms"), and
  how widely cards are taken is still unknown.

Built as, on travel.html:

- The lede: "Fly into Tuzla, Sarajevo or Banja Luka, then stay in a town
  where a room starts at about 38 € a night."
- Jump links under the page head (Ways in, Costs, Routes, Staying,
  Eating, Good to know, June), sticky on wide screens, in the flow on
  phones.
- **Ways in:** four numbered stickers, Tuzla, Sarajevo, Banja Luka and By
  bus, each with its time and cost from the details below.
- **What things cost:** the currency and cash lines beside a price list
  of a guesthouse, Hotel Vertigos and a mid-range hotel a night, a meal,
  a cappuccino, a bus ticket and the lakes, each with when it was checked.
- **Getting here:** one block per airport (Tuzla, Sarajevo, Banja Luka)
  and one for bus or train; the transfer companies split into the block
  of the airport they serve; renting a car below, with the 20 company
  names at Sarajevo airport folded behind "The 20 companies with desks
  there".
- **Staying** and **Places to eat** keep their maps and lists from
  tools/places.py; on a phone the food list shows the first five, with
  "Show all places to eat", which works without a script.
- **Good to know** (time zone, Wi-Fi, phones, visas, police
  registration, health) and **June in Tuzla** (weather, the lakes, and
  the guide to Tuzla) end the page.
