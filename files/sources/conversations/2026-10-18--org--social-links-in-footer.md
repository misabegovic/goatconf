---
title: "GoatConf's LinkedIn and X in every footer, on the contact page and in the event data"
date: 2026-10-18
kind: conversation
---

The organiser asked, verbatim:

> Ok. Do we have social profiles links in our footer for GoatConf?

The agent answered no: no page linked GoatConf's own accounts. The
brain knows two, both live on 2026-10-15: linkedin.com/company/goatconf
and x.com/goatconf (sources/web/social/goatconf-linkedin-2026-10-15.md,
sources/web/social/goatconf-x-2026-10-15.md); Bluesky and Mastodon are
in the channel plan for later, with no account recorded. The organiser
chose:

- **Accounts:** LinkedIn and X.
- **Style:** small icons with names.
- **Also:** the event data for search engines and agents (schema.org
  `sameAs`, and `llms.txt`), and the contact page.

Built as: `tools/nav.py`, which already writes the top bar into every
page, holds the accounts (`SOCIAL`) and writes a "Follow GoatConf" line
with a labelled icon per account into every footer and into the marked
spot on the contact page; the CI's top bar check keeps every page
current. A new account is added once, in `SOCIAL`.
