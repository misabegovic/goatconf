---
title: "Website: goatconf.com on GitHub Pages, with every intake through Google Forms"
kind: decision
status: accepted
updated: 2026-10-17
confidence: medium
depends_on:
  - org/prds/website-and-registration.md
  - org/prds/cfp-and-speakers.md
  - org/prds/extension-slots-and-the-record.md
supersedes: org/adrs/website-and-registration.md
sources:
  - sources/conversations/2026-10-17--org--organiser-block-below-the-goat.md
  - sources/conversations/2026-10-13--org--forms-on-goatconf-com.md
  - sources/conversations/2026-10-12--org--approval-back-on.md
  - sources/conversations/2026-10-12--org--luma-no-approval-hidden-list.md
  - sources/conversations/2026-10-12--org--site-rework-approved.md
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-12--org--registration-on-luma.md
  - sources/conversations/2026-10-12--org--goatconf-drive-folder.md
  - sources/conversations/2026-10-12--org--google-forms-built-and-published.md
  - sources/conversations/2026-10-07--org--goatconf-will-be-public.md
  - sources/conversations/2026-10-07--brain--local-ci-only.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/web/tooling/github-pages-docs-2026-10-12.md
  - sources/conversations/2026-10-12--org--host-on-railway.md
  - sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md
  - sources/web/tooling/railway-static-hosting-2026-10-12.md
  - sources/web/tooling/google-forms-response-destination.md
  - sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md
---

# Website: goatconf.com on GitHub Pages, with every intake through Google Forms

Accepted 2026-10-12 by the organiser
(`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`,
questions 1 to 3). Supersedes
[Register on Luma, with pages copied into muhamed.at/goatconf](website-and-registration.md).

## What

GoatConf has its own home, goatconf.ba, and no longer lives under
muhamed.at. The site is the plain HTML in `files/site/`, published on
GitHub Pages from this repository. Everything that comes in arrives
through Google Forms, owned by the organiser's Google account, with the
responses in Google Sheets:

- **Talk proposals,** the call for talks
  ([the call](call-organiser-judges.md)).
- **Add something,** for anyone adding an event, a workshop, an activity,
  a venue, support or hiring.
- **Registration,** one free pass per core day, replacing Luma.
- **Contact,** which also takes code-of-conduct reports.

## Why

The organiser chose goatconf.ba, Google Forms for everything ("lets do
all through google forms ?") and GitHub Pages
(`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`).
One form tool means one place for every response and one privacy notice.
GitHub Pages serves a branch's root folder
(`sources/web/tooling/github-pages-docs-2026-10-12.md`), and the
repository is to be public
(`sources/conversations/2026-10-07--org--goatconf-will-be-public.md`),
so the site needs no other host.

## How

**Publishing.** A local script pushes the contents of `files/site/` to a
`gh-pages` branch, whose root is the Pages source. No GitHub Actions are
used, as the local-CI rule requires
(`sources/conversations/2026-10-07--brain--local-ci-only.md`). The site
carries a `CNAME` file for goatconf.ba; the domain's apex `A` records
point at GitHub Pages, and HTTPS is enforced
(`sources/web/tooling/github-pages-docs-2026-10-12.md`). Publishing stays
the organiser's act.

**The forms.** A Google Apps Script kept in the repository,
`files/tools/google-forms/create-forms.gs`, creates the four forms, each
with its questions, its privacy notice and a linked response sheet
(`sources/web/tooling/google-forms-response-destination.md`), and emails
the organiser on every response. The organiser runs it once. The forms'
public links are written into the site's pages from one file in the
repository, so every button on the site points at the live form.

**Registration.** One response per person per day, asking a name, an
email address, the days, and two optional questions: accessibility
needs, and whether hiring partners may see them. Google Forms has no
waiting list, so the cap is per room at the door: whoever is there first
takes the seat, and the door volunteer closes a full room. The privacy
notice says who holds the data, why, on what basis, for how long and
what rights people have, as Bosnia and Herzegovina's personal data law
asks (`sources/web/legal/bih-zakon-o-zastiti-licnih-podataka-12-25.md`).

**From response to page.** An accepted talk becomes a record in
`files/program/`, built into `site/program.html` by
`files/tools/program.py`. An accepted addition becomes a record in
`files/extensions/`, built into `site/extensions.html` as before. Both
builds are checked by the local CI.

## Alternatives

- **Luma for registration.** Superseded: one tool for every intake.
- **muhamed.at/goatconf, copied by hand.** Superseded by goatconf.ba.
- **Netlify or Cloudflare Pages.** Not chosen.
- **GitHub issue forms.** Not chosen: they need a GitHub account and make
  proposals public.

## Consequences

- **Closes:** Luma, its waiting list and its check-in app; the copy into
  muhamed.at.
- **Opens:** a domain of its own, live forms on every page, and a program
  and extension list built from records.
- **Costs:** no automatic waiting list or capacity cap; the organiser
  turns accepted responses into records; the forms depend on one Google
  account.
- **Operator steps:** register goatconf.ba, set its DNS, make the
  repository public, run the forms script once, and publish. Each is the
  organiser's act.

## Amendments

- **2026-10-12, one navigation and a reordered home page.** Every page has the same top bar: Program, Speakers, Travel and Supporters, with Give a talk and Register as buttons; the other pages are in the footer. The home page runs: the cover with the seal, the three days, who is speaking, give a talk, Tuzla, food, add your own, the supporters with the budget, why a goat, and the code of conduct. The days come from the program's day plan and the speakers and supporters from their records, so the home page fills in as people confirm (source: sources/conversations/2026-10-12--org--site-rework-approved.md).
- **2026-10-12, registration moves to Luma.** The organiser supplied the embed code for a Luma event, so registration runs there instead of on a Google Form; the talk, add-something and contact forms stay Google Forms (source: sources/conversations/2026-10-12--org--registration-on-luma.md). The register page's button opens Luma's checkout over the page, `forms.yml` holds the event link, and the forms script no longer builds a registration form. The event requires the host's approval for each registration and asks no questions beyond name and email, so the days, accessibility needs, open-to-work and news opt-in questions the Google Form asked are not collected unless they are added on Luma.

- **2026-10-12, the forms are built by hand and live in the shared Drive folder.** Instead of the Apps Script, the three Google Forms (propose a session, add something, contact) were built by hand in the organiser's GoatConf folder in Google Drive and published; the script was removed from the repository (source: sources/conversations/2026-10-12--org--google-forms-built-and-published.md). Google Forms' own settings replace what the script did: an email to the organiser on every response, a copy to the respondent on the talk and add forms, and a responses spreadsheet per form in the folder. The separate sheet that hid speakers' names is dropped; the organiser hides the name columns while reading. The folder is shared with the organising team, who therefore see responses too, code of conduct reports included, on the organiser's choice (source: sources/conversations/2026-10-12--org--goatconf-drive-folder.md).
- **2026-10-12, the site moves to Railway.** goatconf.ba is served by Railway instead of GitHub Pages (source: sources/conversations/2026-10-12--org--host-on-railway.md). It stays a static site: a Railway service deploys the `files/site` folder from `main` as plain files, with no build and no server code, and only changes under `files/site/` start a deploy; Railway serves a folder with an `index.html` as static files (source: sources/web/tooling/railway-static-hosting-2026-10-12.md). Every merge to `main` publishes, so the local CI, which fails while any generated page is stale or any form link is empty, is the last check before the public sees a change. The organiser pays Railway's Hobby plan, 5 USD a month, directly, and it is a line in the public budget as paid by the organiser, so no money passes through the organiser. goatconf.ba's nameservers move to Cloudflare's free DNS, because Railway serves a bare domain only through CNAME flattening or ALIAS records (source: sources/web/tooling/railway-static-hosting-2026-10-12.md); Railway issues the HTTPS certificate. Railway does not need the repository to be public, so making it public stays a separate choice. `publish-site.sh`, the `gh-pages` branch and the `CNAME` and `.nojekyll` files are retired.
- **2026-10-12, back to GitHub Pages, published by one Actions workflow, at goatconf.com.** This amendment replaces the Railway one above (source: sources/conversations/2026-10-12--org--public-repo-pages-goatconf-com.md). The site's address is goatconf.com, which the organiser owns at Namecheap; goatconf.ba is not used. The code lives in a new public repository, misabegovic/goatconf, which starts from one clean commit; the earlier private repository is kept, renamed goatconf-archive, so nothing from before the scrub becomes public. GitHub Pages serves the site. One GitHub Actions workflow, `.github/workflows/publish-site.yml`, uploads `files/site` unchanged and deploys it on every push to `main` that changes `files/site/`, and can be run by hand; it builds and checks nothing. The local CI stays the only CI, and it fails if any other workflow appears or this one changes shape. Every merge to `main` still publishes. Railway, its budget line and the Cloudflare step are dropped; the DNS is four A records and a `www` CNAME at Namecheap.
- **2026-10-12, no approval, and a hidden guest list.** Luma no longer asks the organiser to approve each registration: everyone who registers gets their free ticket straight away. The guest list, which Luma showed to registered guests, is hidden, so the registration list is not shared, as the charter says (source: sources/conversations/2026-10-12--org--luma-no-approval-hidden-list.md). This replaces the approval step in the amendment on registration moving to Luma.
- **2026-10-12, approval back on.** The organiser chose to keep approving each registration on Luma after all, so "Require Approval" is on again; the guest list stays hidden, and the main registration has no limit (source: sources/conversations/2026-10-12--org--approval-back-on.md). This replaces the "no approval" part of the amendment above.
- **2026-10-17, who's organising, below why a goat.** On the organiser's ask, the organiser block (the organiser, IPI Academy, the fact stickers and the conferences run before) moves from after the three days to after why a goat, so the home page runs: the cover with the seal, the three days, who is speaking, give a talk, Tuzla, food, propose an event, the supporters, why a goat, who's organising, and the code of conduct; the album's numbers follow the new order (source: sources/conversations/2026-10-17--org--organiser-block-below-the-goat.md).

## Related

- [Website and registration](../prds/website-and-registration.md)
- [The superseded Luma decision](website-and-registration.md)
- [The call: the organiser judges](call-organiser-judges.md)
- [Program: every room open](open-program-every-room.md)
- [Extension slots and the record](../prds/extension-slots-and-the-record.md)
- **2026-10-13, the forms point to goatconf.com.** The propose-a-session and add-something forms still linked to goatconf.ba, which no longer resolves; both now link to goatconf.com, and the add-something form is titled "GoatConf 2027: propose an event" like the site. The data notes keep "organising team", because the Drive folder has another editor (source: sources/conversations/2026-10-13--org--forms-on-goatconf-com.md).
