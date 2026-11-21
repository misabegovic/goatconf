---
title: "Website and registration: goatconf.com and a free pass per core day"
kind: initiative
status: living
updated: 2026-11-21
parent_epic: goatconf-2027
appetite: small
confidence: medium
supersedes: org/pitches/website-and-registration.md
sources:
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
