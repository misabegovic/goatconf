---
title: "Keep the email list in Luma, and the weekly beats as one calendar page here"
kind: decision
status: accepted
updated: 2026-10-24
confidence: medium
depends_on:
  - org/prds/social-drumbeat.md
sources:
  - sources/conversations/2026-10-24--org--tuesday-and-saturday-posts.md
  - sources/conversations/2026-10-18--org--social-plan-to-june.md
  - sources/conversations/2026-10-15--org--announcing-on-linkedin-and-x.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/web/tooling/luma-pricing.md
  - sources/web/tooling/luma-privacy-policy.md
  - sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md
  - sources/web/social/goatconf-linkedin-2026-10-15.md
  - sources/web/social/goatconf-x-2026-10-15.md
---

# Keep the email list in Luma, and the weekly beats as one calendar page here

Answers the "Decision needed" of
[A weekly drumbeat](../prds/social-drumbeat.md). Accepted 2026-10-07 from
the organiser's answer
(`sources/conversations/2026-10-07--org--adr-answers.md`, question 7), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

GoatConf's one owned channel, the email list, lives in Luma. People who
register get updates as guests of the core-day event; people who only
want news follow GoatConf on Luma before or without registering. No
second newsletter tool is used. The weekly beats are kept as one
calendar page in this repository; nothing about subscribers is.

## Why

The organiser chose Luma's own updates over a separate newsletter tool or
no list. Registration is already on Luma
([Website and registration](website-and-registration.md)), so a second
tool would ask people to sign up twice and hold a second copy of their
data. Luma's free plan sends "up to 500 invites or newsletters per week"
and blasts to an event's guests without limit
(`sources/web/tooling/luma-pricing.md`), which covers an event capped at
about 120 and a following of a few hundred.

## How

Consent is the act of registering or following, and the registration
notice says what updates people will get and how to stop them, as Bosnia
and Herzegovina's data law asks
(`sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md`).
Subscriber data stays in Luma and never enters this public repository.

The calendar page holds one entry per beat: the week, the beat, its
channels (the email list, LinkedIn, the community chat, the open
network), a draft of the words, and its state (drafted, approved,
published). Dates are filled in once IPI confirms, following the road's
anchored steps ([The road to June 2027](road-to-june-2027.md)). An agent
or a volunteer drafts; every post is published by the organiser or by
the social volunteer the organiser names, because anything that reaches
the public is the organiser's call
(`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`).

## Alternatives

- **Luma's own updates** *(chosen)*: one tool, one copy of the data,
  consent at registration.
- **A separate newsletter tool:** double opt-in and archives, at the cost
  of a second sign-up and a second processor of the same people's data.
- **No email list:** simplest, and it leaves GoatConf with no channel it
  owns when a platform changes its reach.

## Consequences

- **Opens:** registrants and followers reached from one place.
- **Costs:** the list is only as portable as Luma's CSV export, and Luma
  does not say where it stores the data
  (`sources/web/tooling/luma-privacy-policy.md`); the same open question
  as registration.
- **Costs:** whether people can follow GoatConf on Luma before the event
  page exists, and how that page is set up, is (unverified, 2026-10-07),
  and it decides whether the list can open before registration does.

## Linked PRD

[A weekly drumbeat](../prds/social-drumbeat.md).

## Build notes

*(empty until the work ships)*

## Amendments

- **2026-10-24, two posts a week: the plan on Saturdays, news and Tuzla on Tuesdays.** Week 2 did not go out on Tuesday 20 October; the organiser posted it on Saturday 24 October 2026 and chose to post twice a week. The planned posts keep their order and go on Saturdays, from week 2 on 24 October 2026 to week 33 on 29 May 2027; "See you Thursday" stays on Tuesday 1 June 2027, and the event-day posts and the thank-you on Tuesday 8 June 2027 keep their dates. Every Tuesday from 27 October 2026 is a second slot: news first (a speaker, a supporter, an event), otherwise a short Tuzla post, drafted about a month ahead. Each post on [The drumbeat](../outreach/drumbeat.md) now links its images at goatconf.com/share/, and no share page is added to the site. This replaces the 2026-10-18 amendment's "every Tuesday" (source: sources/conversations/2026-10-24--org--tuesday-and-saturday-posts.md).
- **2026-10-18, the calendar is dated to June 2027.** On the organiser's answers, one post goes every Tuesday from 20 October 2026 to 1 June 2027, then on each event day and a thank-you on 8 June 2027, all fully drafted on [The drumbeat](../outreach/drumbeat.md). Week 1 is published (source: sources/conversations/2026-10-18--org--social-plan-to-june.md).
- **2026-10-12, registration is back on Luma, the channels are chosen, and the calendar exists.** Registration moved to the organiser's Luma event (source: sources/conversations/2026-10-12--org--registration-on-luma.md), so registered guests can again get Luma updates; the earlier amendment's "Luma is no longer used" no longer holds. People who tick the news question on the contact form are the other part of the list. The organiser chose the channels: LinkedIn; X, Bluesky and Mastodon; and Luma with link previews (source: sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md). The calendar is [The drumbeat](../outreach/drumbeat.md), with the launch sequence drafted and the images in `site/share/`.
- **2026-10-12.** Luma is no longer used. The email list is the people who tick an optional, unticked question on the registration or contact Google Form asking to be sent news about GoatConf; news goes by email from the organiser's Google account. Subscriber data stays in the organiser's Google Sheets and never enters this public repository. The weekly beats calendar here is unchanged. See [Website: goatconf.com and Google Forms](goatconf-ba-and-google-forms.md) (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
- **2026-10-12.** IPI Academy has accepted the dates, Thursday 3 and Friday 4 June 2027 as core days and Saturday 5 June as the community day, and GoatConf has access to all seven rooms, as the organiser reported; no written copy is in the brain. The posts can carry the dates now (`sources/conversations/2026-10-12--org--ipi-accepted-dates-all-rooms.md`).
- **2026-10-15, GoatConf's own accounts.** The LinkedIn page (linkedin.com/company/goatconf) and the X account (@goatconf) are live, checked on 2026-10-15, so the posts go from GoatConf itself; the start is LinkedIn and X, with Bluesky and Mastodon for later, and nothing has been posted yet (sources: sources/conversations/2026-10-15--org--announcing-on-linkedin-and-x.md, sources/web/social/goatconf-linkedin-2026-10-15.md, sources/web/social/goatconf-x-2026-10-15.md).
