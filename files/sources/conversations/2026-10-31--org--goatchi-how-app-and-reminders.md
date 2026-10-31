---
title: "How Goatchi grows: one image per pose from the atlas, installable, with opt-in reminders made on the device"
date: 2026-10-31
kind: conversation
---

Asked how the new goat poses should be made and served (one image per pose cut by tools/goat_atlas.py, one sheet per goat type, animating parts of fewer paintings, or nothing), the organiser chose "Extend the atlas, one image per pose (Recommended)", described as: each type's eight poses become masters named like "pirate-eating", each cut into one small image as Goatchi uses today; Goatchi loads only the kept goat's eight images, about 240 KB, after a goat is picked; one pose that drifts is easy to redo.

While the decision record was being written, the organiser wrote, verbatim:

> I'm also thinking we could ship a browser extension or something? PWA only for goatchi? Have like device local notifications from the browser itself or something

The agent answered that an installable Goatchi (a manifest and a service worker for the Goatchi page) is easy and fits, with an icon on the home screen and play offline; that reminders after the page is closed need Web Push and so a server, which keeps an identifier for each device, against the plan's "no server" and "no notifications"; that a browser extension can remind on the device without a server but runs on computers, not phones, needs a store listing and is a second codebase. Offered installable without notifications, installable with reminders as a later pitch, an extension as well, or neither, the organiser answered, verbatim:

> Let's do 1 ... But is there no way to have checks on local storage run periodically and notify locally only in case something happens?

The agent answered: while Goatchi is open, a timer can check the goat and show a notification on the device; after it is closed, only on Android and on computers in Chrome or Edge, and only once Goatchi is installed, periodic background sync can wake Goatchi's service worker now and then to read the goat (kept for it in the browser's IndexedDB, as a service worker cannot read local storage) and show a notification made on the device, with nothing sent anywhere; the browser decides when, at best about once or twice a day; on iPhone and in Firefox there is no way without a push server. Asked whether Goatchi should offer that, the organiser chose "Opt-in, local only (Recommended)", described as: off by default; a player who installs Goatchi can turn on "Tell me when my goat needs me"; notifications come from the device, never a server, at most once a day; the plan's no-go becomes "no notifications unless the player turns them on".
