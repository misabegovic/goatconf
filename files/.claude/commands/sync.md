---
description: One-shot health sweep — siblings + lint + check-sources + validate + views
---

Apply the `sync` skill.

Runs the full sweep: `files/tools/sync-siblings.sh`, the `wiki-lint` skill,
`files/tools/check-sources.py`, `python files/tools/brain.py validate`, and
`tabula index`. Surface anything that needs judgement
in the consolidated `sync —` log line.

`$ARGUMENTS` is currently unused; the sweep is whole-corpus.
