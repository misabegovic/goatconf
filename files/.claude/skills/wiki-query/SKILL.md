---
name: wiki-query
description: Answer a question from the brain — consult index.md, read candidate pages, fall back to mempalace for verbatim/cross-conversation context, answer with citations to wiki pages and source paths, and file any reusable reasoning back into the wiki. Load when the user asks a factual or contextual question that the brain plausibly knows the answer to ("what is X", "where do we...", "why did we decide...", "have we discussed...").
---

# Query the brain

The brain is an LLM-maintained wiki at `~/projects/brain`. It points at raw
sources (sibling repos, Notion exports, ad-hoc notes) and at a mempalace
verbatim index for cross-conversation/source recall.

## Protocol

### 1. Start with `files/wiki/index.md`

Open it. Skim section headings and one-line hooks for plausible candidates.
Don't grep blindly — the index exists so the agent doesn't have to.

### 2. Read candidate pages

Read them in full, including their frontmatter `sources:` block. Chase
cross-links that look load-bearing.

### 3. Reach for mempalace when the wiki is thin

The wiki is a *synthesis*; mempalace is a read-only retrieval surface over
whatever was previously mined. Use it when:

- The wiki cites a long source and you need the exact wording.
- The wiki is silent on the question and you suspect prior conversations
  or source files cover it.
- You want to verify the wiki's claim against the source.

```bash
mempalace search "<phrasing close to what the source would say>"
mempalace status   # which wings exist; treat counts as a snapshot, not live
```

Mention the search key in your answer so the user can rerun it. The palace
is *not* refreshed automatically — mining is intentionally not part of the
active workflow yet, so a miss is "not in the snapshot," not "doesn't exist."

### 3b. Reach for the architecture graph when the question is structural

*"Who calls X"*, *"what depends on X"*, *"what breaks if I change
X"*, *"how coupled is X"* — the graph answers these
deterministically where the wiki answers them from synthesis.
`brain.py enola impact <symbol>` and `brain.py enola findings --repo
<repo>` — and for *"which decisions govern this file?"* or *"what
code does this page actually cover?"*, `brain.py enola govern
<target>` answers in either direction with the relation trail
attached. Prefer the graph *first* for these and the wiki for the
narrative around the answer: the wiki says why a thing exists, the
graph says what actually touches it, and where they disagree the
disagreement is itself the finding — surface it rather than picking
a side.

*"When did X appear"*, *"which change introduced this cycle"*, *"what
did this look like in March"* — these are **temporal**, and a snapshot
cannot answer them however good it is. `brain.py enola history blame
<name-or-path> <repo>` reports when something entered the architecture
and when it left; `history log` walks the recorded revisions and
`history show <rev>` expands one of them. Reach for these before
`git log -S`, which reconstructs the same answer from text and misses
the structural half. Experimental upstream — the format may change, and
nothing in the wiki cites it yet, so treat its output as a lead to
confirm rather than as a citable fact.

`/ask`'s routing table sends explicitly structural phrasings here
already, but a question can turn structural halfway through an
answer, and this skill is also invoked directly. Findings are
candidates to verify rather than verdicts; three explainer classes
are judged permanent noise, so never relay one as fact without
confirming it against the code. Skip silently when the graph is
absent on the machine. Per
[`files/wiki/brain/adrs/architecture-graph-consumption.md`](../../../files/wiki/brain/adrs/architecture-graph-consumption.md).

### 4. Answer with citations

Every non-trivial claim cites either:

- A wiki page (`files/wiki/org/goatconf-2027.md#venue`)
- A source path (`~/projects/<repo>/files/AGENTS.md`)
- A mempalace search key (`mempalace search "..."`)

If you can't cite anything, say so explicitly: *"the brain doesn't cover
this — mempalace returned nothing relevant either."* Don't invent.

### 5. File reusable reasoning back

If answering required synthesis you'd want again, the answer should not
remain only in this chat. Either:

- Edit the relevant wiki page to incorporate the conclusion (with citation),
  update its `updated:` date, and append a `files/log/log.md` line:
  `YYYY-MM-DD query — <question> → <pages updated>`.
- Or, if the synthesis spans pages that don't exist yet, run the
  `wiki-ingest` skill on the conversation as the "source" — same protocol.

If the answer is purely retrieval (no synthesis), don't pollute the wiki.
The wiki is for understanding, not for chat logs.
