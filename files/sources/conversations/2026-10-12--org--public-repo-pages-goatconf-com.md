---
title: "A new public repository, GitHub Pages published by one Actions workflow, and goatconf.com"
date: 2026-10-12
kind: conversation
---

After the move to Railway merged, the organiser asked, verbatim:

> Or we could also keep it public, right?

and then:

> Any reason to bot keep it public as the repo? And just do github pages

and then:

> Ok, we should use github actions to publish the site

Shown a draft amendment (one workflow, `.github/workflows/publish-site.yml`, uploads `files/site` unchanged and deploys it to GitHub Pages on each push to `main` that changes `files/site/`, using only GitHub's own Pages actions, with the local CI still the only CI and checking that this is the only workflow; Railway, its budget line and the Cloudflare step dropped), the organiser wrote, verbatim:

> Just flip it as public and prepare everything. goatconf.com is what I own on Namecheap, need to get that ready too

Told that flipping the existing repository would make all 166 commits and 33 pull requests public, including the files from before the scrub, the organiser answered three questions:

- How the repository goes public: "New public repo (Recommended)": this repository becomes goatconf-archive and stays private, and a new public misabegovic/goatconf starts from one clean commit.
- The address: "goatconf.com everywhere".
- The DNS at Namecheap: "You do it, I give steps".

Read as: the amendment is approved; the agent prepares everything, creates the public repository and turns on Pages; the organiser sets the DNS.
