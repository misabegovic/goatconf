---
title: "Goatchi built and shipped: local storage only, no cookies"
date: 2026-10-28
kind: conversation
---

While Goatchi was being built (wiki/org/adrs/goat-tamagotchi-on-the-site.md), the organiser asked, verbatim:

> Do we use cookies or local storage?

The agent answered that Goatchi uses the browser's local storage, that nothing else on the site stores anything (no cookies, no analytics, no trackers), that local storage stays on the device and is never sent with requests, and that storage a visitor asks for, keeping the goat they picked, is commonly read as exempt from the consent banner rule in the EU. It changed the script so nothing is written until a goat is picked.

Shown Goatchi in the browser (picking, feeding, playing, sleep, the bars, sulking after 30 hours and a week, the countdown, the cheers, swap and let go asking first, nothing stored before a goat is picked, and only a footer link on other pages), the organiser chose "Ship it (Recommended)".
