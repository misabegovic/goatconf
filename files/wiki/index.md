---
title: "goatconf brain: home"
kind: meta
status: draft
updated: 2026-10-14
sources: []
---

# goatconf brain

The LLM-maintained knowledge base for goatconf, the conference: program,
speakers, sponsors, venue, attendees, budget and the decisions behind
them. It was scaffolded empty on 2026-10-07 and inherits its
machinery from claude-brain (see [`AGENTS.md`](../AGENTS.md) § Lineage).
What is known is on [GoatConf 2027: what is known](org/goatconf-2027.md);
what is proposed is on the [pitches hub](org/pitches/index.md).

## What changed

<!-- home-section: filled; maintained-by: /shape; updated: 2026-10-14 -->
- **2026-10-14**: **The dinner line, softer.** The talk page's speakers dinner line ends at "GoatConf pays for it if the budget allows." and no longer says everyone otherwise pays for their own meal ([what is known](org/goatconf-2027.md); source: sources/conversations/2026-10-14--org--dinner-wording.md).
- **2026-10-14**: **No travel terms under the speakers.** The speakers page drops "Getting speakers here"; who pays for travel is said only where people apply to speak (source: sources/conversations/2026-10-14--org--speakers-page-no-travel.md). The home page drops its travel sentence too, so on the site the terms are only on the talk page, where people apply (sources: sources/conversations/2026-10-14--org--refund-some-or-all.md, sources/conversations/2026-10-14--org--travel-terms-only-on-talk-page.md).
- **2026-10-14**: **Each speaker's own link preview.** A shared speaker page now shows that speaker's card (photo, name, role) instead of the generic GoatConf banner; the local CI fails while a published speaker has no preview card (source: sources/conversations/2026-10-14--org--speaker-link-previews.md).
- **2026-10-14**: **Eight places on the home page.** "Who is speaking" now plans for eight speakers, four to a row, and fills each open place with a call-for-proposals card, so there is no ragged last row; the speakers page is unchanged (source: sources/conversations/2026-10-14--org--home-eight-places.md).
- **2026-10-14**: **A sixth speaker, Jan Grodowski, listed fourth.** A Staff Software Engineer on Shopify's Database Platform team in Salzburg and author of the undercover gem (over 32 million downloads), who ran a workshop at RubyConf Austria 2026, is confirmed with his session to come. The home page now shows all six speakers it has room for ([Jan Grodowski](org/speakers/jan-grodowski.md); source: sources/conversations/2026-10-14--org--jan-grodowski.md).
- **2026-10-14**: **A fifth speaker, Cristian Planas, listed last.** The author of Rails Scales! (Pragmatic Bookshelf, 2025), long at Zendesk and now at Combinaut, is confirmed with his session to come ([Cristian Planas](org/speakers/cristian-planas.md); source: sources/conversations/2026-10-14--org--cristian-planas.md).
- **2026-10-14**: **A fourth speaker, Carmine Paolino, listed second.** The creator of RubyLLM and founder of Plenty in Berlin, who spoke at RubyConf Austria 2026, is confirmed with his session to come. The order is now Paul Campbell, Carmine Paolino, Dejan Menges, Amar Mahmutbegović ([Carmine Paolino](org/speakers/carmine-paolino.md); source: sources/conversations/2026-10-14--org--carmine-paolino.md).
- **2026-10-14**: **Speakers in the organiser's order.** The speakers are listed by an `order` the organiser sets, not alphabetically: Paul Campbell, Dejan Menges, then Amar Mahmutbegović ([Speaker profiles](org/adrs/speakers-and-travel-supporters.md); source: sources/conversations/2026-10-14--org--speaker-order.md).
- **2026-10-14**: **A third speaker, Paul Campbell.** The co-founder and CEO of Tito, the Dublin ticketing company, and organiser of Funconf, is confirmed with his session to come, with his Confex bio and the portrait from his own site ([Paul Campbell](org/speakers/paul-campbell.md); source: sources/conversations/2026-10-14--org--paul-campbell.md).
- **2026-10-14**: **A second speaker, from Tuzla.** [Amar Mahmutbegović](org/speakers/amar-mahmutbegovic.md), co-founder and Head of Engineering at Semblie, a Tuzla hardware company, and author of C++ in Embedded Systems (Packt, 2025), is confirmed with his session to come. The square "I'm speaking" card now fits a long name on one line (source: sources/conversations/2026-10-14--org--amar-mahmutbegovic.md).
- **2026-10-14**: **Speakers' roles, everywhere their name is.** A speaker record takes an optional one-line `role` ("Staff Engineer at Vinted"), shown on their page, the speakers and home pages, the "I'm speaking" cards and the files for agents; text only, never an employer's logo ([Speaker profiles](org/adrs/speakers-and-travel-supporters.md); source: sources/conversations/2026-10-14--org--speaker-role-and-employer.md).
- **2026-10-14**: **The first speaker, before his session.** Confirmed speakers can now be published before their session has a slot or a topic. [Dejan Menges](org/speakers/dejan-menges.md) is the first: his own short bio, the headshot from his last conference, links, and an "I'm speaking" card. A speaker's page now marks Speakers in the top bar ([CFP and speakers](org/prds/cfp-and-speakers.md); source: sources/conversations/2026-10-14--org--speakers-before-sessions.md).
- **2026-10-14**: **A speakers dinner.** Every accepted speaker is invited, with the date to come, paid from online supporters' money if the budget allows; the talk page and the live talk form say so ([CFP and speakers](org/prds/cfp-and-speakers.md); source: sources/conversations/2026-10-14--org--speakers-dinner.md).
- **2026-10-14**: **Twelve open questions decided.** Leftover supporter money pays more of this year's costs, then carries to the next GoatConf. The session-registration tool is picked when the program fills, and check-in uses Luma's app. The open-to-work question is dropped for 2027, and the check-in target is 120 people. The main hall has 120 seats, the organiser is the only code-of-conduct contact for now, and IPI's verbal acceptance is enough. Event records gain the kind "Something else" ([what is known](org/goatconf-2027.md); source: sources/conversations/2026-10-14--org--decisions-one-by-one.md).
- **2026-10-14**: **Loose ends fixed.** Sessions started at the repository root now load the project settings, so the Notion deny-list and the push preflight are in force; `LOCAL_FIRST` counts quoted or not; stale tool wording is corrected; the home-page and README freshness checks now look at this brain, not the root; and the root pi-brain pages point here (source: sources/conversations/2026-10-14--org--remaining-loose-ends.md).
- **2026-10-14**: **Stale pages caught up.** The facts page, the epic, seven PRDs, six ADRs, the drumbeat drafts, `PRODUCT.md`, `README.md` and the Local CI section of `AGENTS.md` now match the decisions of 2026-10-12 and 2026-10-13: registration on Luma with no limit, a private budget with no ledger, no fixed reply time, and required speaker profiles. No new decision was made ([what is known](org/goatconf-2027.md)).
- **2026-10-13**: **Speaker profiles are required.** Proposing a session means agreeing that, if accepted, GoatConf publishes the speaker's profile and promotes them on social media ([speaker profiles](org/adrs/speakers-and-travel-supporters.md)).
- **2026-10-13**: **Mouth-watering food photos, picked one by one.** The organiser chose all twelve food photos from candidate sheets; they are not freely licensed and come down if an owner asks. The ćevapi card is now tuzlanski ćevapi, in lepinja dipped in broth, and tufahija says it has walnuts inside ([images of Tuzla](org/tuzla-images.md), [Tuzla for GoatConf](org/tuzla.md)).
- **2026-10-13**: **Sarma instead of uštipci.** Cabbage rolls, priced from three Tuzla menus ([images of Tuzla](org/tuzla-images.md)).
- **2026-10-13**: **Punjene paprike instead of sataraš.** Stuffed peppers, priced from three Tuzla menus, replace sataraš, which was less Bosnian and priced only in Sarajevo ([images of Tuzla](org/tuzla-images.md)).
- **2026-10-13**: **Uštipci instead of đul pita.** Đul pita had no price anywhere, so uštipci with cheese and kajmak took its place ([images of Tuzla](org/tuzla-images.md)).
- **2026-10-13**: **Prices on the food cards.** Each dish on the home page shows a price range in euro from Tuzla menus and Bosnian news, checked 2026-10-13; none was found for đul pita ([Tuzla for GoatConf](org/tuzla.md)).
- **2026-10-13**: **New kinds of event to propose.** Evening event, community trip, meetup, live podcast, hike, hackathon and karaoke, on the site and the live form; support moved to the supporters page ([extension slots](org/prds/extension-slots-and-the-record.md)).
- **2026-10-13**: **The Tuzla section, filled out.** The home page tells the salt story, the goat legend behind the seal, and how to get there, with two more city photos ([images of Tuzla](org/tuzla-images.md), [Tuzla's history](org/tuzla/history-and-old-town.md)).
- **2026-10-13**: **More vegetarian and vegan food.** The home page adds sataraš and krompiruša (an ajvar photo was added and then removed) and a tip to ask for posno; the travel page lists two more places with vegetarian dishes and marks Mozaik and Pekara Hukić from their menus. No fully vegetarian or vegan place was found near IPI ([Tuzla for GoatConf](org/tuzla.md), [images](org/tuzla-images.md)).
- **2026-10-13**: **No fixed reply time for proposals.** The three-week reply is withdrawn: everyone still hears back, the organiser builds the agenda at their own pace, and a proposal not picked straight away may be kept in case someone drops out ([the call](org/adrs/call-organiser-judges.md)).
- **2026-10-13**: **Speaker travel choices, and why-come on Luma.** The talk form asks about travel with three choices: no support needed, the speaker's company covers it (and is listed as a supporter, the same as online supporters), or a refund if the budget allows, never promised. Luma asks one optional question, why the person wants to come, to help confirm registrations ([online supporters decision](org/adrs/online-supporters-through-the-business.md), [the call](org/prds/cfp-and-speakers.md)).
- **2026-10-13**: **The lakes are open in GoatConf week.** The salt lakes' swimming season opens on 1 June, as the organiser confirmed, which closes the open question on early-June swimming ([Tuzla for GoatConf](org/tuzla.md), [activities](org/prds/activities-lake-and-town.md)). The organiser plans Saturday's lake day, so the program stamps it "Planned" (the goat hunt too), and the lakes are an activity after the talks every day, since many people go around 17:00 or 18:00 ([activities decision](org/adrs/activities-lake-and-town.md)).
- **2026-10-13**: **Begova čorba instead of fruit.** The home page's food section shows begova čorba, a chicken soup, after grah, and the fruit market photo is gone ([images of Tuzla](org/tuzla-images.md)).
- **2026-10-13**: **The pita tags, corrected.** On the home page's food section, burek is a pita with meat, sirnica a pita with cheese and zeljanica a pita with cheese and spinach, as the organiser said; the bean stew is called grah and the coffee Bosnian coffee ([images of Tuzla](org/tuzla-images.md)).
- **2026-10-13**: **Online supporters, and a private budget.** Companies can support GoatConf online for 500 EUR, paid to the organiser's Austrian business, with nothing at the venue; no supporter pays for a named speaker's travel, and speakers' travel is refunded only if the budget allows. The budget page and ledger are gone. Drafted first as an AI suggestion (`org/ai-suggestions/`, now empty) and accepted as [the online supporters decision](org/adrs/online-supporters-through-the-business.md).
- **2026-10-12**: **A seal, posts and a reworked site.** GoatConf's mark is a seal with the EuRuKo 2024 goat: "the one that feeds the community". Banners, a Luma cover, link previews and launch posts are made from it, every page shares one top bar, and the home page shows the days, the speakers and the supporters. The first five weekly posts are drafted for the organiser to publish ([the drumbeat](org/outreach/drumbeat.md)).
- **2026-10-12**: **goatconf.ba, two core days and Google Forms, approved.** The organiser approved the four drafts and moved the site to its own domain. The core days are Thursday 3 and Friday 4 June 2027, 10:00 to 17:00, in every available IPI room in parallel, with Saturday 5 June free for the community. The organiser judges every proposal, with no strict deadline. Talks, additions, registration and contact all go through Google Forms, and the site is published on GitHub Pages ([website decision](org/adrs/goatconf-ba-and-google-forms.md), [two core days](org/adrs/two-core-days-first-week.md)).
- **2026-10-12**: **Places to eat, still being checked.** A web search could not confirm any vegan or vegetarian place on Freedom Square, so the travel page says the list is being checked. A draft message to the cafés, for the organiser to send, is at [café message draft](org/outreach/cafe-message-draft.md), and the search is logged in the sources. The food section also has a bean-stew photo now.
- **2026-10-12**: **The IPI letter follows the new plan, unsent.** The Bosnian date proposal now offers two core days, Thursday 3 and Friday 4 June 2027, with Saturday free, and two first-week options. It waits for the organiser's decisions before it is sent ([IPI letter](org/outreach/ipi-proposal.md)).
- **2026-10-12**: **The site pitches to the people who come.** The home page leads with the extendable part and has three ways in: attend, speak, or add something. Four licensed food photos are added, with vegan and vegetarian notes, and the list of places is still to come ([images](org/tuzla-images.md)).
- **2026-10-12**: **The organiser judges every proposal, extension listings included, with no strict deadlines.** The call may open sooner than the calendar says. A [draft ADR](org/adrs/call-organiser-judges.md) would replace the accepted blind panel and the fixed call window, and waits for approval.
- **2026-10-12**: **Slots filled as we go.** The organiser says the slots will be filled as proposals come in, depending on interest and quality of ideas. The [format draft](org/adrs/core-day-parallel-tracks.md) lists the calendar and judging questions this raises, against the CFP's fixed dates and its blind panel.
- **2026-10-12**: **Two core days, drafted for approval.** The organiser asks for Thursday 3 and Friday 4 June 2027 as core days, with Saturday 5 June free for the lake and the community. Slots run 45 to 60 minutes, an hour in the organiser's chain, with a one-hour break after each slot except the last, in all available rooms, seven at most. The [format draft](org/adrs/core-day-parallel-tracks.md) sets out what this would change, including the conflicts with a few strong talks and with open rooms. This breaks the one-core-day rule, so the [draft ADR](org/adrs/two-core-days-first-week.md) waits for approval and nothing is changed yet.
- **2026-10-12**: **Keynotes and a first-week plan, for now.** The three to four main-day talks are keynotes, all of them, and planning is for the first week of June 2027 until IPI answers in writing. Both points change accepted decisions, so the [draft ADR](org/adrs/open-program-every-room.md) lists them rather than applying them.
- **2026-10-12**: **An open program, drafted as a suggestion.** The organiser picked "Open everything" for the rooms and days, including the core day, and confirms sessions posted in open rooms. The [draft ADR](org/adrs/open-program-every-room.md) lists what that would change, and the core-day rules, the CFP's April target and the charter's fringe wording stand until the organiser approves.
- **2026-10-12**: **IPI's rooms, checked against the record.** The June message and the 2026-10-07 answers disagree on the largest hall (150 or under 120) and on sound. The [IPI Academy](org/ipi-academy.md) page now shows both figures, a wheelchair column for the rooms, the room arithmetic, and the five points IPI still has to confirm.
- **2026-10-10**: **The charter and the extensions page.** One page says what GoatConf is and will not do; each extension is a short file in `extensions/`, checked by `tools/extensions.py` and listed on the site, with the check in the local CI ([ADR](org/adrs/extension-slots-and-the-record.md)).
- **2026-10-08**: **The repository is now also a pi-brain clone.** The goatconf brain moved under `files/`; the repo root carries the pi-brain substrate (its own `wiki/`, `sources/`, `log/` and `brain.config.yml`). All content here is unchanged; only the path gained a `files/` prefix, and the tooling was repointed (`AGENTS.md` at `../AGENTS.md` § Layout).
- **2026-10-08**: **IPI's rooms by the numbers.** The June visit notes give the room ladder (a 150-seat ground-floor hall down to a 13-seat club room), the 15:30 constraint in the second June week, IPI's marketing support and its two-to-three-day expectation ([IPI Academy](org/ipi-academy.md)). A second photo pass added Bosnian food (burek, sirnica, begova čorba) and two day-trip castles to the candidates ([images](org/tuzla-images.md)).
- **2026-10-08**: **Site and program direction from the organiser.**
  Richer photos (Bosnian food, day-trip castles, a summer hero), accommodation prices with where to book, speaker profiles that feed the program, the lake as an everyday hangout with the day-after trip open (Lukomir named), and a sharper "make your own GoatConf" story ([direction](org/tuzla.md), [images](org/tuzla-images.md)).
- **2026-10-07**: **The site redesigned as a walk down the Korzo.** Every stop is a full-width photo of Tuzla with an enamel street sign, the light moving from afternoon to dusk; the hall stop uses IPI Academy's own photos, students' faces blurred ([images](org/tuzla-images.md)).
- **2026-10-07**: **Photos on the site.** Freedom Square, the salt lake and the old town now sit on the home page as postcards, each credited in its caption ([images](org/tuzla-images.md)).
- **2026-10-07**: **The IPI letter is ready to fill in.** The saying is confirmed as "Cijela Tuzla jednu kozu muzla"; bracketed fillers mark the recipient, their role and the date ([IPI letter](org/outreach/ipi-proposal.md)).
- **2026-10-07**: **Twenty-five free photos of Tuzla.** Freedom Square, the salt lakes, the old town, Modrac, the Kapija memorial and ćevapi, each with its licence and credit line, plus who to ask for the city's drone shots and the lakes' June gallery ([images](org/tuzla-images.md)).
- **2026-10-07**: **Everything about Tuzla, pulled in.** Over fifty new snapshots: history, the goat, the old town on foot, food, flights and buses, visas and roaming (EU roaming does not cover BiH), day trips, the local tech scene and June events ([Tuzla](org/tuzla.md), [history and the old town](org/tuzla/history-and-old-town.md)).
- **2026-10-07**: **Website v1 drafted, and the IPI letter.** The site is a hand-drawn treasure map of Tuzla with a goat walking the trail as you scroll, plain HTML and CSS in `site/`, designed with impeccable (`PRODUCT.md`, the direction on `.impeccable/surfaces/`). The date proposal to IPI is drafted in Bosnian, a formal letter with a short personal note, for the organiser to send ([IPI letter](org/outreach/ipi-proposal.md)).
- **2026-10-07**: **Eleven ADRs accepted, one per PRD.** Asked one at a time, the organiser chose Luma for registration and the email list, Google Forms for talks and extensions with a blind review by two or three, extensions as Markdown files, plain HTML and CSS with the goat everywhere, a CSV ledger, two long breaks, the goat hunt run by the organiser, RubyConf Austria's code of conduct, and a calendar anchored to IPI's answer ([ADRs](org/index.md)).
- **2026-10-07**: **Every pitch bet on.** The umbrella became the [GoatConf 2027 epic](org/epics/goatconf-2027.md) and each area a PRD under it, eleven in all, awaiting the organiser's approval before their ADRs are written.
- **2026-10-07**: **goatconf will be public.** Extension hosts contribute here by pull request or through a form. Everything is written as public from now; the inherited files are scrubbed of the private estate they came from, and the public history is to start from one clean commit when the organiser flips visibility.
- **2026-10-07**: **Registration opens with the date; the CFP is a simple form.** The public ledger is a page on muhamed.at/goatconf; the code-of-conduct contacts are the organiser and someone at IPI. A spring reconfirmation keeps early free places from going to waste ([website pitch](org/pitches/website-and-registration.md)).
- **2026-10-07**: **No food or drink from the organiser, ever,** for anyone: supporters cover it or people pay their own. The fallback's food and water lines are gone; volunteers' lunch joins the supporters' menu. The site is muhamed.at/goatconf ([budget pitch](org/pitches/budget-a-goat-and-a-menu.md)).
- **2026-10-07**: **Run from Vienna, a site under muhamed.at.** No co-organiser; IPI students and community volunteers; one or two invited speakers from the organiser's network plus an open call; the website written here and published under muhamed.at, so this repository stays private ([facts](org/goatconf-2027.md)).
- **2026-10-07**: **Three to four talks; breaks on Freedom Square,** under five minutes' walk from IPI. The CFP now says most good proposals will find their place on the workshop day, in hubs or at fringe events ([dates pitch](org/pitches/dates-format-and-schedule.md), [CFP pitch](org/pitches/cfp-and-speakers.md)).
- **2026-10-07**: **Few talks, long breaks in town.** IPI is only for lectures; coffee and lunch happen on the town square near IPI, one to two hours each. The core day is sketched at four or five talks ([dates pitch](org/pitches/dates-format-and-schedule.md)).
- **2026-10-07**: **Six date options for IPI.** All four first proposals go to IPI, plus two midweek options (Tuesday to Friday, in either week) where every lecture day is a weekday and the weekend after is free ([dates pitch](org/pitches/dates-format-and-schedule.md)).
- **2026-10-07**: **Dates stay open: four options to propose to IPI.** The first or second week of June 2027, with a Saturday or a Friday core day, compared on the lake season, holidays, who the day suits and IPI's own calendar, with the four questions to ask IPI ([dates pitch](org/pitches/dates-format-and-schedule.md)).
- **2026-10-07**: **The core day caps at IPI's hall, about 120.** From the organiser: several other rooms for workshops, projector, sound and Wi-Fi but no microphone or recording, step-free to the main hall and first floor, Saturday or weekday both fine. The organiser's 1,000 EUR is a fallback only; normally they pay nothing. See [IPI Academy](org/ipi-academy.md).
- **2026-10-07**: **No money goes through the organiser, and the budget is public.** Supporters pay suppliers directly or give in kind; a public ledger records every line from the first payment ([budget pitch](org/pitches/budget-a-goat-and-a-menu.md)). The organiser has visited [IPI Academy](org/ipi-academy.md) many times in 2026, so the next venue step is writing down what they know and agreeing dates in writing.
- **2026-10-07**: **CI is local, and every push runs it.** Four rule checks (sources additive, the confidence floor, no em dashes, no AI attribution), the full CI chained into the pre-push hook, one-command setup, and no GitHub Actions, on the organiser's decision. The confidence check caught the [organiser](org/organiser.md) and [guide reading](org/prior-art/rubyevents-conference-guide.md) pages at high; both are back to medium.
- **2026-10-07**: **Eleven pitches for GoatConf 2027, all pre-bet.** An [umbrella](org/pitches/one-goat-minimal-core-and-extensions.md) for the minimal core and its extension points, named after Tuzla's goat, and ten area pitches from the website to the [road to June](org/pitches/the-road-to-june-2027.md). Proposed dates: 10 to 13 June 2027, one core day on Saturday 12 June. Grounded in about 170 snapshots, the [RubyEvents guide](org/prior-art/rubyevents-conference-guide.md) and a [Tuzla facts page](org/tuzla.md). Nothing is decided until the organiser bets.
- **2026-10-07**: The brain was scaffolded from claude-brain; the [organiser](org/organiser.md) and the venue, [IPI Academy](org/ipi-academy.md), recorded.

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Open initiatives

<!-- home-section: filled; maintained-by: /shape; updated: 2026-10-07 -->
- [GoatConf 2027](org/epics/goatconf-2027.md): the epic, with eleven approved PRDs under `org/prds/` and their accepted ADRs under `org/adrs/`.

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Recent decisions

<!-- home-section: filled; maintained-by: /shape; updated: 2026-10-13 -->
- **2026-10-13** (accepted): [Online supporters pay the organiser's Austrian business; the budget becomes private](org/adrs/online-supporters-through-the-business.md). It supersedes [a CSV ledger](org/adrs/budget-and-public-ledger.md).
- **2026-10-12** (accepted): [goatconf.com on GitHub Pages, with every intake through Google Forms](org/adrs/goatconf-ba-and-google-forms.md); [two core days, 3 and 4 June 2027](org/adrs/two-core-days-first-week.md); [every room in parallel](org/adrs/core-day-parallel-tracks.md); [the organiser judges every proposal](org/adrs/call-organiser-judges.md); [every room open](org/adrs/open-program-every-room.md). These supersede the Luma, blind-panel and one-core-day decisions.
- **2026-10-07** (accepted): [Register on Luma, capped at the hall](org/adrs/website-and-registration.md); [Google Forms and a blind panel for talks](org/adrs/cfp-and-speakers.md); [extensions as Markdown files](org/adrs/extension-slots-and-the-record.md); [RubyConf Austria's code of conduct](org/adrs/operations-and-the-day.md); [a CSV ledger](org/adrs/budget-and-public-ledger.md); and six more in [the org hub](org/index.md).

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Drift surface

<!-- home-section: empty; maintained-by: /groom -->
*(empty: no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Insights now

<!-- home-section: empty; maintained-by: /feedback -->
*(empty: no feedback ingested yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Brain trajectory

<!-- home-section: empty; maintained-by: /groom -->
*(empty: no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Curated picks

<!-- home-section: empty; maintained-by: /groom -->
*(empty: no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Where to find things

- [Brain (meta level)](brain/index.md): how this brain works.
- [Org (the conference as a whole)](org/index.md): way of working,
  strategy, cross-area decisions.
- [GoatConf 2027: what is known](org/goatconf-2027.md): Tuzla, June
  2027, IPI Academy, free, 120 to 300 people, a 1,000 EUR ceiling.
- [The drumbeat](org/outreach/drumbeat.md): the weekly posts, drafted for
  the organiser to publish, from launch to June 2027.
- Area shelves (program, speakers, sponsors, venue, …) arrive as
  content earns them: `wiki/<area>/index.md`.
