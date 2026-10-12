---
name: groom
description: Knowledge garbage-collection sweep over the brain. Distinct from /sync — /sync is mechanical (broken links, validate); /groom makes value judgements (confidence demotion when sources have moved, insight decay flagging, superseded → archived transitions). Load when the user says "groom", "decay", "archive", "knowledge gc", "is anything stale", or invokes `/groom`.
---

# Groom — knowledge garbage collection

You are working in `~/projects/brain`. Permanent knowledge bases rot
when nothing actively prunes them. `/sync` catches structural rot;
`/groom` catches *epistemic* rot — pages that may still be technically
valid but are no longer trustworthy at their stated confidence, or
insights that have lingered without action for too long.

This skill makes value judgements. Every decision is logged. When in
doubt, **flag for human review** rather than acting silently.

## Half-life policy (per `files/AGENTS.md`)

| Page kind     | "Fresh"     | "Aging"      | "Stale"        |
|---------------|-------------|--------------|----------------|
| `reference`   | < 90 days   | 90–180 days  | > 180 days     |
| `initiative`  | < 30 days   | 30–60 days   | > 60 days      |
| `decision`    | < 1 year    | 1–2 years    | > 2 years      |
| `entity`      | < 180 days  | 180–365 days | > 365 days     |
| `insight`     | < 30 days   | 30–90 days   | > 90 days      |
| `overlap`     | < 60 days   | 60–120 days  | > 120 days     |

Plus: a page's clock resets on a *content* edit (not a frontmatter-only
bump). Use git blame / `git log -p` to confirm if unsure.

## Protocol

### 1. Load the corpus

```bash
tabula index --json 2>/dev/null   # every page's frontmatter + reverse edges, keyed by path
```

Walk every page. For each, compute: kind, age (today − `updated:`),
confidence, whether the cited sources have moved (use git on the
relevant sibling repo where possible).

### 2. Decisions per page

| Trigger                                                                                       | Action                                                                                  |
|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| `reference` + age > 90d + cited sibling repo has moved > 30 commits since `updated:`           | Demote `confidence: high → medium`. Note in the page's intro: *(stale; sources moved)*. |
| `reference` + age > 180d + sources still moving                                                | Flag for re-validation. Do *not* edit — surface in the log instead.                     |
| `initiative` + status `living` + age > 60d                                                     | Flag *"is this still active?"*. Surface for human / authoring team.                     |
| `initiative` + status `living` + cited PRs/commits all merged                                  | Flag *"likely shipped — promote to reference or archive"*.                              |
| `insight` + status `draft\|living` + age > 90d + no `superseded_by`                            | Flag *"act, dismiss, or restate"*. Surface for review.                                  |
| Any kind + status `superseded` + age > 365d                                                    | Move to `files/wiki/_archive/<original-path>`. Update index. Page remains readable.           |
| Any kind + status `archived`                                                                   | Already moved; verify it's under `files/wiki/_archive/`.                                      |
| `decision` + age > 2y + a newer decision page references the same topic                       | Flag for *"supersede the old one explicitly"*.                                          |
| Any kind + a receipt citation with verdict `stale` or `malformed` (`brain.py enola citations`) | Flag for *re-verification* — the graph content moved past the cited digest (stale) or the citation breaks the grammar (malformed). Never auto-edit; re-verifying is a judgment task. **Before re-reading the code, ask the history what moved**: `brain.py enola history blame <name-or-path> <repo>` reports when the cited thing entered the architecture and when it left, which usually turns "this digest is old" into "this claim died on a specific day for a specific reason". Experimental upstream; skips cleanly. Per [`brain/adrs/receipt-claim-verification.md`](../../../files/wiki/brain/adrs/receipt-claim-verification.md). |
| A page's architecture claim contradicted by a graph finding (`brain.py enola findings --repo <repo>`) | Flag the contradiction for judgment — **never apply it**. A finding is a candidate to verify, not a verdict, and the corpus already carries three explainer classes judged permanent noise. Resolving it means reading the code, then either correcting the page or recording the finding as `rejected` with the reason. Per [`brain/adrs/architecture-graph-consumption.md`](../../../files/wiki/brain/adrs/architecture-graph-consumption.md). |
| A ledger entry whose finding no longer appears in the graph (`brain.py enola findings --all`) | Ledger hygiene: the code moved past a recorded judgment. An `accepted` entry whose finding is gone is usually **good news** — the thing got fixed — and its `cited_at` page may now be stale. A `rejected` entry that vanished can be dropped. `noise` entries stay regardless; they describe the explainer, not the code. |
| A dangling-code-anchor finding (`intent` explainer) — a page's derived anchor covers a path the graph measures nothing at | Resolve against the measured tree, never by guess; `brain.py enola govern <page-or-path>` locates both ends. Three outcomes: the path **moved** → verify the rename in the sibling's git history, then fix the citation in place; the path is **prototype/branch-only or deliberately removed** → annotate the citation with a trailing ` (…)` note so the stamp retires the anchor and `check` skips it as knowingly historical, and flag the page for re-ingest when its prose also describes the old world; the path **exists but unmeasured** → record an extraction-gap verdict with `brain.py enola judge`. Never delete a citation to silence a finding. The 2026-08-06 groom is the worked example (45 → 16 → 2, six renames fixed, eight annotations, two gap verdicts). |

`/groom` does **not** delete pages. Archive moves are reversible (just
move back). Confidence demotions are reversible (next ingest can promote).

### 3. Reserved archive folder

`files/wiki/_archive/` is a tooling-output folder like `_views` and
`_overlaps` — lint and orphan checks skip it. Pages there keep their
relative paths (e.g. `files/wiki/_archive/feature-x.md`) so backlinks
continue to resolve.

When archiving:

1. `mv files/wiki/<page>.md files/wiki/_archive/<page>.md`
2. Update `files/wiki/index.md` — replace the entry with one in an `## Archive`
   section (group all archived links there).
3. For any page in `files/wiki/` that links to the archived one, leave the
   link as-is (Quartz's broken-link warning is a feature here — humans
   can decide whether to update).

### 4. Surface judgement calls

Anything that needs human review goes in the consolidated `groom —`
log line as a bulleted block. Flagged-for-review pages are *not*
edited; only the log surfaces them.

```
YYYY-MM-DD groom — walked <N> pages: <D> demoted, <A> archived,
   <F> flagged
   - flagged: files/wiki/<page>.md (<reason>)
   - flagged: files/wiki/<page>.md (<reason>)
```

### 5. Validate

```bash
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py validate
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py intent stamp
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py export
tabula index
```

Validate must exit 0 — archive moves can break index links, the views
regen captures the new state. The export re-derives the mirror cardo
compiles after status flips (superseded to archived changes the
compiled knowledge node); the stamp keeps pages free of a derived block.

## What groom is *not*

- **Not deletion.** Archive ≠ delete. Demotion ≠ removal.
- **Not silent re-synthesis.** If a page is genuinely wrong, that's
  `/in` (re-ingest) territory or human edit territory. `/groom` only
  changes status / confidence / location.
- **Not run on every push.** This is a periodic operation —
  recommended cadence in `files/wiki/brain-roadmap.md` is monthly.

## Done check

- [ ] Every page in `files/wiki/` was assessed against the half-life table.
- [ ] Each action taken is in the consolidated log line.
- [ ] Every flagged-for-review page is named under the log line, with
      a one-line reason.
- [ ] `brain.py validate` is clean.
- [ ] `files/wiki/_views/` regenerated.
- [ ] `files/wiki/index.md` § Drift surface updated with the top-N
      Now-vs-Perceived gaps from this groom pass. Per
      [`files/wiki/brain/adrs/home-content-shape.md`](../../../files/wiki/brain/adrs/home-content-shape.md):
      every files/wiki/ edit must be paired with a files/wiki/index.md edit.
- [ ] No page was edited beyond the documented actions (status,
      confidence, location, intro stale-tag).
