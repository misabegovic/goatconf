---
title: "goatconf becomes an empty shell brain inheriting from claude-brain"
date: 2026-10-07
kind: conversation
---

The operator asked, verbatim:

> Hello. I want to work on goatconf. Make it an empty shell brain inheriting from claude-brain

`misabegovic/goatconf` was private, created 2026-09-03, holding only a one-line README. Asked three questions, the operator chose:

- What "inheriting from claude-brain" should mean: **Copy the full machinery** (claude-brain's governance in AGENTS.md trimmed of its estate specifics, the .claude skills, personas and settings, tools/templates, brain.py and its validator, the git hooks and the CI script, plus an empty wiki/sources/log; goatconf then runs on its own). The alternatives offered were `tabula init` and a thin `brain.py init` kernel calling claude-brain's tools through BRAIN_DIR.
- What goatconf is: **A conference**.
- Whether claude-brain should register goatconf as one of its products: **Yes, register it**. Later the same day the operator reversed this (see 2026-10-07--brain--everything-in-goatconf.md).

Done the same day (commit 326c41f): machinery copied from claude-brain at 61a2812, every skill but `attention`, the four agent personas only, settings with no machine paths and every Notion write denied, gates falling back to brain.py when no tabula is installed; the code-graph layer, the UI, the evals and the harness left behind.
