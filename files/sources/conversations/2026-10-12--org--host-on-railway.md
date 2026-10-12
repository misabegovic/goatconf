---
title: "goatconf.ba moves from GitHub Pages to Railway, as a static site"
date: 2026-10-12
kind: conversation
---

After the agent files merged, the organiser wrote, verbatim:

> I want to host it on Railway instead

Asked three questions, the organiser answered:

- Who pays Railway (the free plan has no custom domains, the Hobby plan is 5 USD a month): "I pay it myself".
- How the bare domain works, since Railway needs CNAME flattening or ALIAS records at the root: "Cloudflare DNS (Recommended)".
- How publishing works: "Every merge to main".

While answering, the organiser added, verbatim:

> We should just make it a static site

Shown a draft amendment to the website decision (a Railway service serving `files/site` from `main` as plain files with no build and no server code; every merge to `main` publishes; the organiser pays the Hobby plan directly and it is listed in the public budget; goatconf.ba's nameservers move to Cloudflare's free DNS; the repository may stay private; `publish-site.sh`, the `gh-pages` branch and the `CNAME` file go), the organiser wrote, verbatim:

> Yes

Read as: the amendment is approved, with a PR opened and merged for it.
