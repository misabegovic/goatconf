---
name: ask
description: Single entry point for everything that *queries* the brain. Auto-routes the question to wiki-query (factual), wiki-plan (planning a task), wiki-overlap (checking duplication), or wiki-coverage (gap analysis on a repo). Load when the user says "ask", "query", "what is", "how do we", "plan", "outline", "coverage", "overlap", "duplicate", or invokes `/ask`.
---

# Ask — single entry for querying the brain

You are working in `~/projects/brain`. There are four read-side
operations underneath this one skill — `wiki-query`, `wiki-plan`,
`wiki-overlap`, `wiki-coverage`. This skill picks the right one based
on the phrasing of the question.

## Routing

Default is `wiki-query` (factual lookup). Promote to a more specific
skill when the phrasing matches:

| Phrasing cue                                              | Skill          |
|-----------------------------------------------------------|----------------|
| "plan", "outline the work", "what do I need for X", "how should I approach X" | `wiki-plan`    |
| "overlap", "duplicate", "stepping on", "anyone else doing X", "is anything similar in flight" | `wiki-overlap` |
| "coverage", "what's missing in repo X", "how much do we know about repo X", "what isn't documented in X" | `wiki-coverage`|
| "who calls X", "what depends on X", "what would break if I change X", "how coupled is X", "what does the graph say about X" | the architecture graph *first* — `brain.py enola impact <symbol>` and `brain.py enola findings --repo <repo>`, then `wiki-query` for the narrative around the answer |
| "what is", "where is", "why did we", "have we discussed", "show me", anything else factual | `wiki-query` (default) |

The graph row is a *deterministic* answer where the wiki carries a
synthesised one, so it goes first when the question is structural —
the wiki says why a thing exists, the graph says what actually
touches it. Findings are candidates to verify rather than verdicts;
three explainer classes are already judged permanent noise, so
never relay one as fact without confirming it against the code. Skip
the row silently when the graph is absent on the machine. Per
[`files/wiki/brain/adrs/architecture-graph-consumption.md`](../../../files/wiki/brain/adrs/architecture-graph-consumption.md).

A question can legitimately span multiple skills (e.g. "plan a refactor
of the CFP scoring process, is anyone else working on it?"). In
that case run them in order: `wiki-plan` first, then `wiki-overlap` as
part of step 4 of the plan protocol. Don't fork into parallel skills;
chain them.

## Overrides

The user can force a route with a leading marker:

- `query: <question>` — factual lookup, even if phrasing sounds like a plan.
- `plan: <task>` — go straight to `wiki-plan`.
- `overlap: <topic>` — go straight to `wiki-overlap`.
- `coverage: <repo>` — go straight to `wiki-coverage`.

## Announce before acting

Before running, state in one sentence which skill(s) you're picking
and why. Example:

> "Reading this as a coverage question on `infrastructure` — running wiki-coverage."

If you're chaining (plan → overlap), say so.

## Then

Hand off to the chosen skill and follow its full protocol. This skill
is just the dispatcher.

`wiki-query` and `wiki-plan` don't write to the wiki by default;
`wiki-overlap` writes overlap pages; `wiki-coverage` may append to a
reference page. Each underlying skill's done-check applies as written.

## Done check

- [ ] Routing decision was announced.
- [ ] Underlying skill ran its full protocol.
- [ ] If two skills chained, both produced their expected output.
