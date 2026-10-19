---
title: "The organiser approves the ADR for one page frame, one marker style and one site build"
date: 2026-10-19
kind: conversation
---

Shown a plain explanation of the proposed ADR
`wiki/org/adrs/one-page-frame-and-one-site-build.md` (merged as proposed in
PR #121), the organiser wrote, verbatim:

> lets see if we should approve 121, what is it?

Asked whether to approve it, they picked "Approve, check first": mark it
accepted and build it in small pull requests, the HTML check first, then the
shared helpers, the shared frame, one marker style and the one build command,
then the day times, each with before and after screenshots.

Asked who merges, they picked "Yes, merge each": the agent merges each pull
request once the local CI passes and the screenshots match, so the next one
starts from main.
