---
name: sync
description: One-shot health sweep of the brain: runs sync-siblings (git-fetch each sibling, list new commits), wiki-lint (broken links, orphans, stale dates, contradictions), check-sources (verify every sources: citation resolves), brain.py validate (frontmatter conformance), and tabula index (regenerate the auto indices). Replaces standalone /lint. Load when the user says "sync", "lint", "sweep", "check the brain", "is the brain healthy", or invokes `/sync`.
---

# Sync — one-shot health sweep of the brain

Runs everything that keeps the brain coherent in a single pass. Use
this whenever you finish a batch of ingests, before / after a `/schedule`d
routine, or just want a clean baseline before publishing to the UI.

## Steps

Run each step. If a step surfaces issues, log them under that step but
**keep going** — the goal is one consolidated sweep, not bail-on-first-
error.

**Helper fan-out (parallel-first).** When a step has parallel shape —
the sibling-repo sweep across eight active repos in step 1, the
broken-citation walk across many pages in step 3, the registry
reconcile across multiple in-flight efforts in step 6 — default to
fanning out helper subagents in a single message rather than serial
tool calls. Per
[`files/wiki/brain/adrs/parallel-execution-agent-teams.md`](../../../files/wiki/brain/adrs/parallel-execution-agent-teams.md).

### 1. Sibling-repo sync

```bash
files/tools/sync-siblings.sh
```

Reports per-repo: commits since the last brain ingest/mine that named
that repo, plus the first 5 commit subjects. Repos with > 0 new commits
are candidates for `/in <repo>` after the sweep.

### 1b. Architecture drift (enola)

```bash
python3 files/tools/brain.py enola generate --refresh ../<repo>   # the repo(s) step 1a named
python3 files/tools/brain.py enola generate                       # only when the binary or an explainer moved
git diff files/wiki/_state/enola/receipts.json | grep -E '^[-+].*(content_digest|git_commit)'
python3 files/tools/brain.py enola coverage
```

Refreshes the repositories that moved into the existing union, one at a
time (about 100 s each on the brain's cluster against 15 to 30 minutes for
a full regeneration), or regenerates
the whole cluster when the binary or an explainer changed (refresh refuses
an extractor-version mismatch by design), then reads the drift out of git. A changed
`content_digest` is *architecture* movement; a changed `git_commit`
with a stable digest is mere commit churn — the distinction step 1
cannot draw. Commit the updated `receipts.json` so the brain's record
of "what architecture did we last synthesize against" advances
alongside the sync cursors.

`enola coverage` answers the question the digest cannot: **which
cross-repo edges actually resolved**. A service reported `isolated`
with zero detected edges and one whose outbound edges simply could not
be followed look identical in a fact count, and only the first is a
finding about the architecture — the second is a finding about the
snapshot. Report it as a line in the sweep, not as a list of edges.

**Do not use `brain.py enola diff` for this step.** It compares the
recorded receipts against each repo's live `.enola/receipt.json`, and
that artifact is written by `generate` itself — so chaining
`generate && diff` compares a baseline against a snapshot taken
seconds earlier and reports every repo `unchanged` by construction,
while running `diff` alone compares two views of the same prior
snapshot. There is no ordering that makes it work, because `generate`
calls `_enola_record()` unconditionally with no opt-out: the previous
baseline is gone the moment the snapshot refreshes. The only baseline
that survives a `generate` is the committed `receipts.json`, which is
why this step reads git. (Found 2026-08-03: the step as originally
written reported all seven repos unchanged while three of them
had moved; step 5's `receipt-citations`
detector caught the same drift two steps later. A `--no-record` flag
on `generate` would let `diff` serve this purpose properly — worth
doing, but it is a `brain.py` change rather than a skill fix.)

**Skip-when-absent:** if the enola binary or config is missing on
this machine, `generate` prints one skip line and exits 0 — never
treat that as a failure, and remote CI must never depend on this
step. With no snapshot there is no `receipts.json` change either, so
the git read is trivially empty: say *"the graph was not asked"*
rather than *"the graph agreed"*, per the substrate ADR's named-skip
rule. Per
[`files/wiki/brain/adrs/architecture-graph-substrate.md`](../../../files/wiki/brain/adrs/architecture-graph-substrate.md).

Then report the **count** of unjudged finding classes, never the list:

```bash
python3 files/tools/brain.py enola findings | tail -1
```

And read the movement out of the committed series:

```bash
python3 files/tools/brain.py enola trend --last 5
```

Its last line — *"since the previous snapshot: +3 — brain 97→100"* —
is the sentence this step wants. The counts come from the
`insight_count` field each `generate` records into `receipts.json`,
read back out of git history, so it works anywhere the receipts are
committed and needs no local graph. Skip-when-absent applies: with
no committed history it prints a named skip and exits 0.

One line in the sweep output — *"N findings in the cluster, M shown"* —
and nothing more. **Do not enumerate them here.** A list of findings in
a sweep's output is a backlog by another name, which
[`architecture-graph-consumption`](../../../files/wiki/brain/adrs/architecture-graph-consumption.md)
forbids in its first no-go; the findings surface is pulled by whoever
is already reasoning about a change, not pushed by the health sweep.
If the count has moved sharply since the last sync, that is worth a
sentence in the briefing — *"the graph gained 14 findings this week"* —
because it says the architecture moved, which is the same signal
step 1b exists for.

### 2. Wiki lint

Apply the `wiki-lint` skill in full:

- index integrity (every entry exists; no dead links)
- orphan pages (on disk but not in `files/wiki/index.md`)
- frontmatter validity
- stale-date flag (only if upstream sources moved)
- contradiction sweep across overlapping pages
- source-citation spot check

Surface judgement calls in the consolidated log line at the end.

### 3. Source-link check

```bash
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py check
```

Walks every page's `sources:` frontmatter, verifies each path/URL
resolves. Add `--no-net` if offline or the network is flaky. Broken
sources go into the consolidated log line.

### 4. Schema validate

```bash
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py validate
```

Frontmatter conformance, required-section presence per kind,
`depends_on` / `supersedes` / `superseded_by` referential integrity,
orphans, dead index links. Must exit 0 — if not, fix before continuing
(this is structural, not stylistic).

### 5. Reflection-check — drift detectors

```bash
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py reflection-check
```

Runs the nine deterministic drift detectors per
[`files/wiki/brain/ai-suggestions/prds/reflection-validator-suite.md`](../../../files/wiki/brain/ai-suggestions/prds/reflection-validator-suite.md):

- `links` — every files/wiki/-internal markdown link resolves.
- `confidence-floor` — `confidence: high` pages > 30 days old.
- `active-scope` — files/AGENTS.md table matches `files/wiki/<repo>/` folders
  **and** `ACTIVE_REPOS` in `files/tools/brain.py`. Three surfaces mean
  "active"; the constant went unchecked until 2026-08-03, when it
  sat two days behind the schema and the sibling sweep silently
  skipped two repos.
- `supersedes-cycles` — `superseded_by:` chains have no cycles.
- `page-size` — pages > 500 lines (advisory; not enforced).
- `sources-exist` — every `sources:` path resolves on disk.
- `sync-drift` — sibling-repo HEAD vs cursor commit-count delta.
- `epic-children` — `parent_epic:` claims resolve and the epic
  page mentions the child by slug.
- `sources-immutability` — `files/sources/` tree has no modifications
  vs git baseline.
- `receipt-citations` — receipt citations in wiki prose match the
  recorded `content_digest`s in `files/wiki/_state/enola/receipts.json`
  (verdicts stale / unknown-repo / malformed surface as findings;
  `/groom` owns the re-verification decision).

Findings are warnings, not errors. Surface them; act on them as
part of the sweep where they're cheap to fix (broken links,
orphaned epic-children, stale sources). Defer judgment-heavy
findings (page-size on epics; confidence-floor demotion) to
`/groom`.

### 6. Stamp intent + regenerate views

```bash
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py intent stamp
~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py export
tabula index
```

The stamp (tabula's) is idempotent: it writes what a page's sentences
say into its fields, keeps hand-written seams, layers and claims under
`intent:` and removes any derived block. `tabula export` (through
`brain.py export`) then rewrites the frontmatter-only mirror cardo
compiles, from every page's frontmatter (files/AGENTS.md § Conventions):
the sweep's chance to catch a stale export before preflight fails it.

Refreshes `files/wiki/_views/by-{kind,team,repo}.md` and `ai-suggestions.md`
(the views the UI renders). The per-page index other skills read is
`tabula index --json`, printed on demand and never committed. Always run last so views reflect any
fixes from earlier steps.

### 7. Reconcile parallel-effort registry

If `files/wiki/_state/efforts/` contains records, walk each:

1. **Match against open PRs.** For each record with a recorded
   `brain_pr` or `target_prs`, run `gh pr view <pr> --json
   mergedAt,state` and update the record's `status` accordingly:
   - All recorded PRs `mergedAt` non-null → `status: merged`.
   - Any recorded PR `state: CLOSED` and `mergedAt` null → keep
     `status: in-flight` and surface for the operator (was
     the PR abandoned or just closed without merge?).
2. **Detect orphaned worktrees.** Walk `git worktree list` (in
   the brain primary checkout *and* in each sibling repo whose
   `.claude/worktrees/` exists). Worktrees whose path doesn't
   match any registry record's `brain_worktree` /
   `target_worktrees` are **orphaned** — surface them, don't
   auto-reap.
3. **Surface stale registry records.** Records older than 90
   days with `status: merged` or `status: abandoned` get
   archived under `files/wiki/_archive/efforts/<slug>.json` (move,
   not copy) — keeps `files/wiki/_state/efforts/` scoped to
   recent-and-active efforts.

Use `~/.local/share/mempalace-venv/bin/python3 files/tools/brain.py
efforts list --json` to read records; `efforts mark <slug>
<status>` to update; `mv` for the archive step. The reconcile
step runs after the views regen so any `files/wiki/_archive/efforts/`
moves are reflected in the regenerated index.

### 8. Rotate the operations log if oversized

`files/log/log.md` grows monotonically. When it crosses **2,000 lines** (or
~200 KB), `/sync` rotates it — this step is mechanical, no judgement:

1. Move the current `files/log/log.md` to `log/archive/log-YYYY-MM-DD.md`
   (date = today, the day rotation runs).
2. Create a fresh `files/log/log.md` whose first two lines are:

   ```
   # Operations log
   Previous: log/archive/log-YYYY-MM-DD.md
   ```

Archived log files are read-only after rotation; never edit them.
Search across the full history with `grep -r "<query>" log/`.

## Log

Single consolidated log line:

```
YYYY-MM-DD sync — siblings:<N moved>, lint:<N issues fixed/M surfaced>,
   check-sources:<N broken>, validate:<ok|N errors>, views:<regenerated>
```

If the sweep surfaced anything that needs human judgement (a
contradiction, an orphan to delete vs expand, a broken upstream URL),
add a short bulleted block under the line.

## Done check

- [ ] All five steps ran (none silently skipped).
- [ ] `brain.py validate` exited 0 by the end.
- [ ] `files/wiki/_views/` was regenerated.
- [ ] `files/wiki/index.md` § What changed updated with merge events
      since the last sync; § Brain trajectory rewritten if the
      brain's trajectory has materially shifted. Per
      [`files/wiki/brain/adrs/home-content-shape.md`](../../../files/wiki/brain/adrs/home-content-shape.md):
      every files/wiki/ edit must be paired with a files/wiki/index.md edit.
- [ ] One consolidated `sync —` line in `files/log/log.md`.
- [ ] Anything that needs human judgement is surfaced under that line.
