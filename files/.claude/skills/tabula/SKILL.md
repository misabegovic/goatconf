---
name: tabula
description: The brain's tool. Search before reading, claim before working, evaluate before finishing.
---
# tabula

The brain here is served by `tabula`, one binary; reach for it before grep. Its verbs are MCP tools from the `tabula` server, wherever your harness registers it.

## The loop

- `tabula search <words>`: what governs your change; `tabula outline <page>` and `tabula page <page> --section <heading>` or `--lines a:b` read a page in parts.
- `tabula search --sources <words>`: a source's or conversation's exact words, with lines.
- `tabula govern <repo>/<path>`: the pages anchoring a file, ranked.
- `tabula impact <repo>/<path>`: what depends on a file, per the engine.
- `tabula claim <task> --as <agent>`: one agent holds a task for a lease, renewed by claiming again; `tabula release` gives it back.
- `tabula evaluate <prd>`: judges PRDs and pitches; run it before ending a turn that moved governed code, or the stop hook refuses once. `--json` gives bullets and `validate`'s findings `span`s, the lines `--lines` reads.
- `tabula reconcile [<prd>]`: bullets recorded not met; a person picks the side.
- `tabula report --as <agent> --kind <kind> --ref <page> --note <text>`: the journal; `--kind gap --id <id>` files what the brain could not answer, once, for a person.

## What comes next

Every verb ends with `next:`, the command to run now, and `because:`, its rule, both under `--json`. `next: none` means nothing follows.

## Exit codes

Each code means one thing and asks one thing of you:

- 0: done. Carry on with the work.
- 1: failed, or found what it checks for wrong (validate errors, lock drift). Fix what it names, then run it again. A render interrupted by a signal tabula did not send also exits 1, as does a render or a sketch that a stop-when-idle entry stopped between attempts (the stop `stopped`) or a stop-hard entry ended; `tabula follow <task>` reads how, and nothing starts it again unasked.
- 2: called wrongly, or files/tabula.config.yml holds a key tabula does not read or a value of another type. Fix the call (`tabula help <verb>` names its arguments) or the key (`tabula validate` names every one), then run it again.
- 3: the owner's step: another agent's claim or workflow step, the operator's promotion, install, observation (no test ran), token budget, day's bound, untrusted run key or held line, a person's verdict on a finding or batch, a disagreement waiting for a person (reconcile), or a journal entry tabula cannot read. Report it with `tabula report --kind refused` and stop; never retry with another flag or name. A render paused on its budget (`render.budget_tokens`) or a renderer's question keeps its claim. A render whose goal (its PRD or files/tabula.config.yml) changed during an attempt also exits 3, gives its claim back, and a person reads the change. Trusting and lifting a hold are the operator's, never an agent's.
- 4: a sync conflict; nothing was pushed and the merge was undone. Resolve the pages it names by hand, then sync again.
- 5: a bullet not met (evaluate, corpus, render) or a terminal workflow step (run). For a bullet not met: fix the code and evaluate again, and never edit the bullet. For a terminal step: it is never redone in place, and a redo is a new step on the workflow page.

`tabula chat` without `--dry-run` returns the harness's own code once it has launched it, and the hook bodies follow the harness's protocol (2 blocks, 0 passes) outside this scheme.

## Everything else

`tabula help` lists verbs and topics; `tabula help <topic>` prints one.
