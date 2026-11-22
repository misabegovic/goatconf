---
title: "Website and registration: goatconf.com and a free pass per core day"
kind: initiative
status: living
updated: 2026-11-22
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/website-and-registration.md
sources:
  - sources/conversations/2026-11-22--org--food-and-tuzla-open-and-close-on-phones.md
  - sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md
  - sources/conversations/2026-11-22--org--sections-start-closed-speakers-open.md
  - sources/conversations/2026-11-22--org--ship-the-collapsible-home-page.md
  - sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md
  - sources/conversations/2026-11-22--org--first-visit-stays-see-you-fixed-open-ship-when-ready.md
  - sources/conversations/2026-11-22--org--speakers-section-also-collapsed-by-default.md
  - sources/conversations/2026-11-22--org--date-place-and-free-on-speaker-and-register-pages.md
  - sources/conversations/2026-11-22--org--section-goats-too-small-and-cut-off.md
  - sources/conversations/2026-11-22--org--no-goat-beside-the-organising-link.md
  - sources/conversations/2026-11-22--org--hosts-need-not-pay-for-everything.md
  - sources/conversations/2026-11-22--org--organising-row-off-the-home-page.md
  - sources/conversations/2026-11-22--org--ship-round-twelve-when-ready.md
  - sources/conversations/2026-11-22--org--organisers-own-page-and-see-you-in-tuzla.md
  - sources/conversations/2026-11-21--org--links-clickable-and-dark-mode-love.md
  - sources/conversations/2026-11-21--org--minimal-chosen-phone-hooves-light-and-dark.md
  - sources/conversations/2026-11-21--org--continue-iterating-round-four.md
  - sources/conversations/2026-11-21--org--continue-iterating.md
  - sources/conversations/2026-11-21--org--keep-iterating.md
  - sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md
  - sources/conversations/2026-11-07--org--home-goats-stay.md
  - sources/conversations/2026-11-07--org--home-page-order.md
  - sources/conversations/2026-11-07--org--register-page-and-hallway-track.md
  - sources/conversations/2026-10-13--org--online-supporters-through-the-business.md
  - sources/conversations/2026-10-12--org--google-forms-built-and-published.md
  - sources/conversations/2026-10-12--org--session-registration-later.md
  - sources/conversations/2026-10-12--org--approval-back-on.md
  - sources/conversations/2026-10-12--org--first-come-luma-only.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-14--org--catch-up-stale-pages.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--bet-on-every-pitch.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md
  - sources/conversations/2026-10-07--org--no-money-through-me.md
  - sources/conversations/2026-10-07--org--conference-vision.md
  - sources/conversations/2026-10-07--org--first-answers.md
  - sources/web/organiser/muhamed-at-about.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
  - sources/web/tooling/pretix-hosted-pricing.md
  - sources/web/tooling/pretix-features.md
  - sources/web/tooling/tito-pricing.md
  - sources/web/tooling/luma-pricing.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/funding/fosdem-charter.md
---

# Website and registration: goatconf.com and a free pass per core day

A child of the epic [GoatConf 2027: a minimal core others extend](../epics/goatconf-2027.md).
It graduates the pitch
[A website of plain pages and a free registration with a cap](../pitches/website-and-registration.md),
bet on by the organiser on 2026-10-07
(`sources/conversations/2026-10-07--org--bet-on-every-pitch.md`).

## Objective

**GoatConf has a site at muhamed.at/goatconf, written in this repository
and copied over when published, that says when, where, who and why, and
carries the code of conduct, travel basics, the program, the extension
list and the public budget; and, from the day IPI confirms the date, a
free registration capped at about 120 with a waiting list.**

## Background

The guide puts the site first: "As soon as you have a date and venue,
put up a simple website", saying when, where, who it is for and why
come, with the code of conduct, travel basics and accessibility added
early (`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Your website). It is also what supporters read to judge whether an
event is credible.

The organiser has decided where the site lives and how it is made: a
page on their own site, no new domain, with the page sources "in
goatconf, copied over", designed with impeccable here
(`sources/conversations/2026-10-07--org--talks-team-and-site.md`), at
the path /goatconf
(`sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`).
muhamed.at runs on a clone of pi-brain
(`sources/web/organiser/muhamed-at-about.md`), so the copied pages follow
that site's conventions. The public budget ledger is one of the site's
pages, written here and copied over like the rest
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).

Registration was "needed (if permitted, something like that)"
(`sources/conversations/2026-10-07--org--conference-vision.md`). The
organiser has since set its cap ("I would register per hall capacity",
about 120,
`sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`)
and its timing: it opens as soon as IPI confirms the date in writing,
likely November 2026
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`).

## Affected personas

- [Attendee](../../../.claude/personas/users/attendee.md). Today there is
  nothing to read and nowhere to sign up. With this shipped, an attendee
  finds the date, the place, the cost of the trip and the code of conduct
  on one site, registers for free with a name and an email, and reconfirms
  once in spring.
- [Speaker](../../../.claude/personas/users/speaker.md). Finds the call
  for talks and its terms (travel is theirs) on the site, and later their
  own talk on the program.
- [Extension host](../../../.claude/personas/users/extension-host.md).
  Sees their addition on the site's extension list, built from the record
  files in this repository.
- [Hiring partner](../../../.claude/personas/users/hiring-partner.md).
  Reads the supporters page and the charter, and reaches only attendees
  who chose to be seen.

## Now / Perceived / Target

- **Now (2026-10-07):** no site, no registration. The path,
  muhamed.at/goatconf, and the way pages are made (here, copied over) are
  decided. This repository is private and is to become public
  (`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).
- **Perceived:** that a free event fills its room. A free place is easy
  to take and easy to forget, and the no-show rate for GoatConf is
  (unknown, needs source) until measured.
- **Target:** a first page live as soon as the date is confirmed, pages
  added as the event fills in, registration open from the confirmation
  with a cap of about 120 and a waiting list, and a check-in list on the
  day.

## Scope

**The site.** A handful of plain pages: home, program, travel and stay,
accessibility, code of conduct, extensions, supporters, the budget
ledger, contact. They are written and designed in this repository with
impeccable (see [Design with impeccable](design-with-impeccable.md)) and
copied into muhamed.at/goatconf when published; each publish is a public
act and the organiser's. Content follows the guide's order: first when,
where, who and why; then the code of conduct and travel basics; then the
call for talks, the supporters page and the program as they exist. The
trip is sold before the lineup: Tuzla, the lake, the low cost (guide,
§ What you are selling). The extension list is built here from the
extension record files and copied with the rest, since muhamed.at cannot
read this repository's files itself. Everything is in English
(`sources/conversations/2026-10-07--org--first-answers.md`, question 7).

**Registration.** Free, capped at about 120, with a waiting list. It
collects only what the event needs: a name for the badge, an email, and
optional questions (accessibility needs, and whether the attendee wants
hiring partners to see them), following FOSDEM's charter line that
"attendees are not required to submit personal information to attend
unless law or safety mandate it" (`sources/web/funding/fosdem-charter.md`).
It opens when IPI confirms the date. Because a free place is held for
about seven months, registrants reconfirm once in spring, unconfirmed
places go to the waiting list, and a last reminder goes out the week
before. On the day, a check-in list confirms who came.

The pitch recommended hosted pretix, whose plan includes "500 free
tickets per year" and has a waiting list and check-in
(`sources/web/tooling/pretix-hosted-pricing.md`,
`sources/web/tooling/pretix-features.md`), with Tito
(`sources/web/tooling/tito-pricing.md`), Luma
(`sources/web/tooling/luma-pricing.md`) and a plain Tally form
(`sources/web/tooling/tally-pricing.md`) as fallbacks. That choice is the
ADR's to make.

## No-gos

- No paid tickets, and no "supporter" upsell in registration.
- No data collected that the event does not use; nothing sold or shared.
- No login or account system on the site.
- No new domain for 2027.
- No custom-built site generator or registration system.
- No registration before IPI confirms the date in writing.
- No payment taken through the site; no money passes through the
  organiser
  (`sources/conversations/2026-10-07--org--no-money-through-me.md`).
- No publishing without the organiser.

## Rabbit holes

- **Building a custom site or registration system.** Tempting for a
  technical organiser; it costs the evenings the program needs. Stop and
  use a hosted tool.
- **Fighting the host site's conventions.** muhamed.at is a pi-brain
  clone; if the copied pages need that site changed in more than small
  ways, stop and re-pitch.
- **No-shows.** Reminders and releasing unconfirmed places matter more
  than the tool. An overbooking margin is (unknown, needs source) until
  measured; do not guess one larger than the waiting list can absorb.
- **Data protection.** Names and emails are personal data under Bosnian
  and EU rules; how the law applies is for operations (unknown, needs
  source).
- **The list builder.** Rendering the extension list must stay a small
  step; if it grows into a site generator, stop.

## Appetite

**Small.** A few evenings for a first page and the registration set-up,
then steady additions as the event fills in. The site grows from one
page; registration is configured once and opened on the confirmation.

## Success metrics

- **The first page is live at muhamed.at/goatconf within two weeks of
  IPI's written confirmation.** Observed from the page's first publish
  date against the confirmation's date in `sources/`.
- **Registration opens within a week of IPI's written confirmation.**
  Observed from the registration tool's opening date.
- **90 or more of about 120 registrants check in on the day.** Observed
  from the registration tool's check-in export, counted the day after.
- **No registration question beyond name, email and the optional ones
  named here.** Observed from the registration form's own export of its
  questions at opening.

## Dependencies

- [Dates and the core day](dates-and-the-core-day.md): the confirmed date
  opens registration and the cap comes from the hall.
- [Design with impeccable](design-with-impeccable.md): the look the pages
  are built on.
- [Extension slots and the record](extension-slots-and-the-record.md):
  the record files the extension list is built from, and the charter
  page.
- [Budget and the public ledger](budget-and-public-ledger.md): the ledger
  is a page on this site.
- [CFP and speakers](cfp-and-speakers.md): the call is linked from the
  site, and the program comes from it.
- [Operations and the day](operations-and-the-day.md): the code of
  conduct, the data-protection question and check-in on the day.

## Decisions already made by the organiser

- **The site is a page on muhamed.at, no new domain.**
  `sources/conversations/2026-10-07--org--talks-team-and-site.md`.
- **Pages are written and designed in this repository and copied over
  when published.** Same source.
- **The path is /goatconf.**
  `sources/conversations/2026-10-07--org--no-food-or-drinks-and-site-path.md`.
- **The public budget ledger is a page on muhamed.at/goatconf.**
  `sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`.
- **Registration opens when the date is confirmed in writing.** Same
  source.
- **The call for talks uses a simple form.** Same source.
- **Registration is capped at the hall, about 120.**
  `sources/conversations/2026-10-07--org--ipi-rooms-and-fallback-money.md`.
- **This repository will be public.**
  `sources/conversations/2026-10-07--org--goatconf-will-be-public.md`.
- **English.** `sources/conversations/2026-10-07--org--first-answers.md`,
  question 7.

## Open questions

- Is registration legally or practically required, and what does the law
  ask of the list it keeps? (unknown, needs source)
- How the copied pages fit muhamed.at's own layout and navigation.
- What overbooking margin, if any, the waiting list allows.

## Decision needed

Which registration tool GoatConf uses: hosted pretix (free quota,
waiting list, check-in), Tito, Luma, or a plain form in the same tool as
the call for talks. The ADR also records how the pages are copied into
muhamed.at/goatconf and how the extension list is built before the copy.

**Answered by the ADR** [Register on Luma, capped at the hall, with pages copied into muhamed.at/goatconf](../adrs/website-and-registration.md), accepted 2026-10-07.

## Amendments

- **2026-10-12.** The site's home is goatconf.com, published on GitHub Pages from this repository; muhamed.at/goatconf is superseded. Registration is a Google Form, one free pass per core day, replacing Luma; the cap is per room at the door. Talk proposals, add-something submissions and contact (including code-of-conduct reports) are Google Forms too, created by the script in the repository. See [Website: goatconf.com and Google Forms](../adrs/goatconf-ba-and-google-forms.md), [Dates: two core days](../adrs/two-core-days-first-week.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. Nothing on the site or the registration form waits on IPI any longer (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-14, read with the later decisions.** The first amendment above no longer holds on registration or the forms: registration is on the organiser's Luma event, not a Google Form, with no limit; the organiser approves each registration, seats are first come, first served at each room's door, and ticket holders register for sessions later, with the tool not decided yet (sources: sources/conversations/2026-10-12--org--registration-on-luma.md, sources/conversations/2026-10-12--org--first-come-luma-only.md, sources/conversations/2026-10-12--org--approval-back-on.md, sources/conversations/2026-10-12--org--session-registration-later.md). The talk, propose-an-event and contact forms are Google Forms built by hand in the organiser's Drive folder, not by a script (source: sources/conversations/2026-10-12--org--google-forms-built-and-published.md). The budget page in the body is gone: the budget is private, with no budget page and no public ledger; online supporters pay the organiser's Austrian business 500 EUR for online perks only, and speakers' travel is refunded only if the budget allows, never promised (source: sources/conversations/2026-10-13--org--online-supporters-through-the-business.md).
- **2026-11-07, the register page refreshed.** register.html stays short but moves to album pages: the button beside four stickers (Free, Two days, Hour off, Saturday), every listed speaker's photo and name from the speaker records, the days with seats as three steps, getting here with what a stay costs and a link to the travel page, then how it works and your data (source: sources/conversations/2026-11-07--org--register-page-and-hallway-track.md).
- **2026-11-07, the home page in the attendee's order.** The home page runs days, speakers, Tuzla and food, then a "Get your free ticket" band with the Register button, then the doors (propose a session, make it yours, support) and the rest. On a phone it keeps every speaker card and every dish, so the goats on them stay for the companion goat to visit (sources: sources/conversations/2026-11-07--org--home-page-order.md, sources/conversations/2026-11-07--org--home-goats-stay.md).
- **2026-11-21, one ask, and registering within reach on a phone.** Decided on the local branch `site/phone-first-and-one-ask` and pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--design-iteration-on-a-branch.md). Each change is judged by a measure taken on the built pages. (1) A register control is reachable in the sticky top bar at every scroll position at 390 pixels wide, and it and Menu are each at least 44 pixels tall and wide; the mark keeps its year down to 320 pixels wide. This puts back the Register button the organiser took out of the phone bar on 2026-10-23, when the build that had it dropped the year (source: sources/conversations/2026-10-23--org--phone-menu.md). (2) The register page's Luma button is within the first 600 pixels at 390 wide, in the page head, with one line under it saying what registering gets you; the "Your ticket" section below keeps its four stickers and has no second copy of the head's button. (3) The top bar on wide screens has exactly one button-styled item, Register; Host an event and Propose a session are plain links, and every link label to the hosting page that names the act says "Host an event", the cover's included. (4) The line beside each register button says what registering gets you in facts the site already states, and no longer reads as a queue; the site still does not say that the organiser approves each registration (source: sources/conversations/2026-10-18--org--registration-approval-not-on-the-site.md). (5) The home page's "Get your free ticket" page is one ticket-shaped sticker with the date, the place, "free" and the button. (6) On a phone the home page keeps every sticker one after another and keeps every speaker card, Tuzla photo and dish, so every goat stop stays (sources: sources/conversations/2026-11-07--org--home-goats-stay.md, sources/conversations/2026-10-18--org--speakers-one-by-one-on-mobile.md, sources/conversations/2026-10-18--org--tuzla-and-food-one-by-one-on-mobile.md, sources/conversations/2026-10-20--org--hero-phone-list.md); the page gets shorter only by closing empty gaps, and its height at 390 and at 1440 wide is recorded before and after. A second local branch, `site/phone-two-across`, holds a sketch of the same page with the photo stickers two across on a phone, every card kept, to show the organiser beside it: it measures 22,013 pixels at 390 wide and brings back speaker cards of uneven length and prices that wrap beside the food goat, so it is not proposed. No layout that keeps every card reaches the 14,000 pixels first aimed at.
- **2026-11-21, round two: an ending, the address, one sequence on the register page, a footer to scan.** Second round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--keep-iterating.md). Each change is judged on the built pages. (1) The home page's last page, "See you in Tuzla", letters the dates at headline size and the place under them, keeps its sentence word for word and its Register button, and shows the waving goat at least 8rem wide on a wide screen; on a phone the goat stays centred below the button, as the organiser chose (source: sources/conversations/2026-10-27--org--see-you-goat-on-phones.md). (2) "Why a goat" ends on the organiser's own photo of the goat statue as a photo sticker, beside the sentence the published post uses, "Today the goat has its own statue, in front of Hotel Tuzla."; the thin line "Tuzla has a statue of the goat." is gone and the painted statue stays as the goat's stop (sources: sources/conversations/2026-11-21--org--goat-statue-photo.md, sources/conversations/2026-11-21--org--why-a-goat-published.md). The goat hunt is not named anywhere (source: sources/conversations/2026-11-21--org--goat-hunt-not-promised-for-now.md). (3) The venue's address, Kulina bana 2, Tuzla, is on the home page where the venue is named: under the IPI Academy photo on the opening page and on the ticket; the ticket's stub links the calendar file the program page already offers, as "Add to calendar" (source: sources/conversations/2026-10-12--org--site-for-agents.md). (4) The register page reads as one sequence below its head: what the ticket gets you as four stickers in one row at 1440 pixels wide, the days with the seats, who is speaking, getting here, how it works; no page on it has a column left more than half empty at 1440 wide, and its sections together are no taller than before at 1440 or at 390 (the footer's groups add height under every page, the register page's included). Its speakers strip and its lines on getting here stay, as chosen on 2026-11-07 (source: sources/conversations/2026-11-07--org--register-page-and-hallway-track.md). (5) Every footer keeps every link (15 on inner pages, 14 on the home page's back cover) and shows them in four named groups a visitor can scan. (6) On a phone the home page gets shorter only by closing space that is empty and that no goat needs, between stacked stickers and around bands; no card is removed or made smaller, and the lists stay one after another. Its height at 390 wide is recorded before (29,694) and after. (7) The line beside the register button on a speaker's page goes back to "Free, for everyone. Luma emails you when you are in.", which the organiser said stays on 2026-11-07 and round one had reworded (source: sources/conversations/2026-11-07--org--meet-them-in-person.md).
- **2026-11-21, round three: nothing gets longer.** Third round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--continue-iterating.md). The round's first measure: no page is taller than at the end of round two, at 1440 or at 390 pixels wide; the heights of the home, register, program, travel and one speaker page are recorded for both rounds. (1) The footer keeps its four groups and every link, and is no taller than in round one at 1440 (404 pixels on the home page, 222 on an inner page); at 390 each group is a label over one wrapped row of links, shorter than round two's two columns, with every link still 44 pixels tall. (2) "See you in Tuzla" is one composition, the lettering, the button and the goat side by side on a wide screen, within 20 pixels of its round-one height (339 at 1440, 333 at 390); the sentence keeps its words, and on a phone the goat stays below the button (source: sources/conversations/2026-10-27--org--see-you-goat-on-phones.md). (3) On the register page at 1440, "The days" has no white under its left column and "Getting here" reads as three even columns under the page's own labels (ways in, staying, accessibility), with no sentence added or dropped. (4) "Why a goat" keeps the statue photo and its sentence and is no taller than in round one (618 at 1440, 1,047 at 390). (5) On a phone an inner page's head shows its photo as a small sticker beside the title, so the page's first section starts higher; a speaker's portrait, a supporter's logo and the mark keep their size. (6) The program, speakers and propose pages no longer open on the same photo: the program shows Freedom Square, the speakers page the goat as a speaker, the propose page keeps the lecture hall; only photos already recorded as fine for the site are used (wiki/org/tuzla-images.md). (7) The home page's supporters are stuck in as numbered stickers, as on the supporters page, one after another on a phone as before (source: sources/conversations/2026-10-18--org--supporters-and-run-a-session-on-mobile.md). (8) A button's hover and press are plainly felt, a loading photo shows an unprinted sticker, and the caret and scrollbars take the album's colours; reduced motion keeps every sticker still. The travel page's seven jump links stay as the organiser chose them on 2026-11-07 (source: sources/conversations/2026-11-07--org--travel-page-redesign.md).
- **2026-11-21, round four: the statue at a proper size, a head image of its own, and one pass for consistency.** Fourth round on the local branch `site/phone-first-and-one-ask`, pending the organiser's approval from screenshots; nothing is published before that (source: sources/conversations/2026-11-21--org--continue-iterating-round-four.md). Nothing gets longer: no page is taller than at the end of round three, at 1440 or at 390 pixels wide. (1) In "Why a goat" on a wide screen the statue photo is a sticker at least 10rem wide again, sharing the left column with the seal, its sentence beside it, and the page is no taller than in round three (599 pixels at 1440); on a phone the row stays as it was. (2) The supporters, contact, charter and accessibility pages no longer open on the same picture: supporters keeps the Korzo, the charter shows the painted goat as a host, and contact and accessibility open without a picture, since no photo recorded as fine for the site fits them and the goat stays off pages that carry code of conduct reports or access needs. (3) One pass over every page at 320, 360, 390, 768, 1024 and 1440 pixels wide finds no horizontal scroll, exactly one button in the wide top bar, Register in the phone bar, four footer groups, a number sequence with no gap or repeat on each page, and a visible focus ring on a button, a text link, a sticker link, a slot link, the menu and the calendar link; what differed is fixed and listed in the round's report. The organiser's later words on how much blue the site uses are built as two variants on their own branches, not here.
- **2026-11-21, the minimal look, chosen, with light and dark themes.** The organiser chose the minimal look and asked for better hoof marks on a phone and proper light and dark themes (source: sources/conversations/2026-11-21--org--minimal-chosen-phone-hooves-light-and-dark.md). The design decisions and their measures are in the design ADR's amendment of the same date. For a visitor: the site follows their system's light or dark setting, they can choose another with a small control in the footer or the phone menu, and no page is taller than before at 1440 or at 390 pixels wide.
- **2026-11-21, a quieter cover.** On the organiser's ask, the paragraph "An excuse to hang out with like-minded people and learn from folks sharing their current best.", which they had proposed on 2026-10-12 (source: sources/conversations/2026-10-12--org--bolder-opening.md), leaves the home page's cover; the files agents read keep it until the organiser decides. The cover reads in one order: the mark and name, the date and place, the promise as one sentence, who it is for in a quieter line with its words unchanged, the button, the three links. Measured at 390 wide the cover is 588 pixels tall, from 706, and the Register button sits at 460, from 578; at 1440 the opening spread is 826 tall, from 907 (source: sources/conversations/2026-11-21--org--links-clickable-and-dark-mode-love.md).
- **2026-11-22, who's organising on a page of its own.** The home page's "Who's organising" section becomes the page `organising.html`, with every sentence, sticker, logo, photo and credit as it was, and the home page keeps a link to it where the section stood, with the host goat's stop (source: sources/conversations/2026-11-22--org--organisers-own-page-and-see-you-in-tuzla.md; published on the organiser's "Ok, ship when ready", source: sources/conversations/2026-11-22--org--ship-round-twelve-when-ready.md). The home page's order is otherwise as decided on 2026-11-07.
- **2026-11-22, no row for who's organising on the home page.** The row that linked to the organising page leaves the home page. The link sits in the supporters section beside "The supporters", with the host goat's stop and the old address `#organiser`, and in every footer (source: sources/conversations/2026-11-22--org--organising-row-off-the-home-page.md). The home page's "Make it yours" text says a host does not have to pay for everything (source: sources/conversations/2026-11-22--org--hosts-need-not-pay-for-everything.md).
- **2026-11-22, no goat beside the organising link.** In the home page's supporters section the links "The supporters" and "Who's organising" stay, the second still under the address `#organiser`; the host goat's stop beside them is removed on the organiser's word (source: sources/conversations/2026-11-22--org--no-goat-beside-the-organising-link.md). Item 6 of the 2026-11-21 amendment, that every goat stop stays on a phone, holds for every other stop.
- **2026-11-22, a proposal: two lists open and close on a phone.** Not approved and not published; built on the branch `site/phone-folds-tuzla-and-food` for the organiser to judge from images. The organiser asked, verbatim: "I'm also thinking to have the food section collapsable and extendable by default? So folks that want to learn can open/close sections like food and Tuzla the host town? ... Could work for all sections probably below the hero section", and then "Figure it out with personas" (source: sources/conversations/2026-11-22--org--food-and-tuzla-open-and-close-on-phones.md). This reopens item 6 of the 2026-11-21 amendment ("keeps every speaker card, Tuzla photo and dish, so every goat stop stays") for the six Tuzla photos and the twelve dishes on a phone, and for nothing else. What still stands of that item and of the decision of 7 November: every speaker card stays; every sticker list is one after another when shown; the page gets no list folded on a wide screen; and as many goat stops as can be kept are kept, with each closed list's goats appearing in turn on its control. The persona study found that every other section carries an action, a date, a price, a logo or the code of conduct, and stays open.
- **2026-11-22, the home page's sections open and close, start closed, and are remembered.** This replaces the proposal directly above, which was never published. The organiser, before seeing that proposal, verbatim: "We should probably have every section as collapsable? Also probably should store latest preference in localstore so folks keep last state?"; then "Only leave the free ticket section as one that can't be collapsed and the hero section" (source: sources/conversations/2026-11-22--org--every-section-collapsible-and-remembered.md); then, on what a first visit shows, "They start closed probably? Speakers section stays open?" (source: sources/conversations/2026-11-22--org--sections-start-closed-speakers-open.md); and, given the whole of it in summary, "Ok, ship when ready" (source: sources/conversations/2026-11-22--org--ship-the-collapsible-home-page.md). The last two are the organiser deciding over the persona study's verdict, which kept every section open and closed two lists on a phone only; the study's dissents are kept in the second source. What the home page must now do. (1) The hero and "Get your free ticket" have no control and are always open. (2) "Who is speaking" starts open and can be closed; every other section starts closed and can be opened, on a phone and on a wide screen. (3) A closed section shows its heading and one row made only of what it holds, and that row keeps in sight each section's action, the three dates, every supporter's logo and the two conduct links; a test holds each link, picture and line on a closed row to its section. (4) The last state of each section and list is kept in the visitor's browser under one key and sent nowhere; a remembered state does not make the page jump on load. (5) A link to a section or into one, a link to a sentence, and find in page open what they land in, whatever is remembered, without changing it. (6) With storage blocked the page is the first-visit page and works; without the script nothing is closed; if the script file fails to arrive nothing stays closed. (7) Keyboard and screen reader: the heading is still a heading, the control is a button inside it that says whether the section is open. (8) An opened section shows its words in full: the paragraph folds of round ten are removed; the six Tuzla photos and the twelve dishes stay a second level on a phone only. This sets aside item 6 of the 2026-11-21 amendment and the decision of 7 November for the home page's closed sections: every card, photo, dish and goat is still on the page and returns when its section is opened. Measures: which sections are open on a first visit at both widths; the page's height on a first visit and with everything closed; where the speakers and the ticket sit; goat stops on a first visit, all closed and all open; shift on load with a remembered state; every home page anchor opened by a link with everything remembered closed; the page with script off, with storage blocked and by keyboard alone.
- **2026-11-22, the sections right in both states, closed and open.** The organiser, about the live page, verbatim: "The meals section behaves weird when collapsed due to goats changing", then "Let's improve those aspects now for each section when collapsed vs opened" (source: sources/conversations/2026-11-22--org--meals-section-weird-when-collapsed.md); and by choice among offered answers: the first visit on a phone is to "Keep as it is", "See you in Tuzla" is to "Make it fixed open", and this work is to "Ship when ready" (source: sources/conversations/2026-11-22--org--first-visit-stays-see-you-fixed-open-ship-when-ready.md). The second choice amends "Only leave the free ticket section as one that can't be collapsed and the hero section": three sections have no control now. An independent review's faults about these states were taken with it (listed in the first source). What the home page must now do, beyond the amendment above. (1) A closed row holds still: no layout shift on it or under it while the goat arrives, leaves or changes. (2) Opening a section opens all of it; there is one level of fold on the page; every open section ends with a control that closes it. (3) A press on a closed row's strip of pictures opens the section. (4) From a wide screen a closed row is one line of about 86 pixels; on a phone it is the heading and one line where the words fit. (5) A heading wraps the same closed and open. (6) "Why a goat" is drawn as the other sections are in both states. (7) A link to any section lands at one distance under the bar. (8) A goat never covers a word, a link, a button or a stamp, and none stands inside a closed section. (9) A press on a goat does not open or close a section, and a press on a heading does not set the goat off. (10) The open phone menu is never taller than the window and scrolls on its own. (11) Every footer shows the theme control, on a phone too. Measures: layout shift per closed row over a goat's coming and going at both widths; closed row heights; what every goat stop covers with all sections open; the goat's box on each closed row; the menu's reach at 667 by 375; the browser check in tests/browser/folds.mjs.
- **2026-11-22, the speakers start closed too.** The organiser, after seeing the published page, verbatim: "Ok. Let's have speakers section also collapsed by default?" (source: sources/conversations/2026-11-22--org--speakers-section-also-collapsed-by-default.md). This reverses the organiser's own "Speakers section stays open?" and the choice "Keep as it is" of the same day; both stay on record. On a first visit every section that opens and closes is closed, at every width; the hero, "Get your free ticket" and "See you in Tuzla" are open and have no control. A browser that remembers a choice for the speakers keeps it; one that remembers none shows them closed. The closed speakers row carries the eight faces and "View all speakers" on a phone as on a wide screen. Measures: which sections are closed on a first visit; the first-visit height at 390 and 1440 and where the ticket starts; a remembered "open" for the speakers still opening them; a link to an id inside the speakers opening the section.
- **2026-11-22, the speaker pages and the register page say when, where and that it is free.** An independent review found that a visitor arriving from a shared speaker card is never told the dates and meets "free" three screens down, and that the register page's first phone screen has no date or city. Asked how the fix should go out, the organiser chose "Ship with existing words (Recommended)" (source: sources/conversations/2026-11-22--org--date-place-and-free-on-speaker-and-register-pages.md). Under each speaker's lede the page now carries the cover's line "3–5 June 2027 · Tuzla, Bosnia and Herzegovina", then "Free to attend." and a link "Register for free" to the register page; the register page carries the same line above its lede. Every word is already on the home page, and a test holds the line to the cover's. Measures: the line and the link present on every speaker page and the line on the register page; how far down a phone screen each stands; the pages' heights before and after.
- **2026-11-22, the section goats at a size that reads, and never cut.** The organiser, about the published page, verbatim: "Goats seem to small now and the text and the goat can be cut off by the section it is in apparently?", then "Maybe it's on mobile only? Check" (source: sources/conversations/2026-11-22--org--section-goats-too-small-and-cut-off.md). Measured, it was at every width: the goat on a section's row was 45 by 48 pixels on a phone 390 wide and 63 by 68 at 1440, and while a section was open its own page clipped the goat and its speech bubble whole. What the home page must now do, with everything the amendment of the sections' two states asks still holding. (1) A section's goat is as wide as the goat on a slot of the cover, 80 pixels or more at every width. (2) The goat, its trick and its speech bubble are whole in every state: clipped by nothing they stand in, never under the sticky top bar, inside the window, the bubble's words on two lines at most. (3) The room for the goat is kept above every section that opens and closes whether or not a goat is there, so a closed row still holds still, with no layout shift as a goat comes, goes, does its trick or speaks. (4) A goat covers no word, link, button or stamp, and is not made smaller to manage it. (5) A press on the goat does not open or close a section. Measures: the goat's drawn size on every row at 390 and 1440; the count of goats and bubbles clipped, closed and open, at both widths; the layout shift while a goat is pressed on each closed row; the first-visit page height at 390 and 1440 before and after.
