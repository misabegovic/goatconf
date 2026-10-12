---
title: "Focus on local CI: the rule gaps closed, every push gated, one-command setup, never GitHub Actions"
date: 2026-10-07
kind: conversation
---

The operator wrote, verbatim:

> Also focus on local CI

Shown the gaps (sources/ add-only checked only against uncommitted changes; the confidence floor, the no-em-dash rule and the no-AI-attribution rule enforced nowhere, and the agent itself having set two pages to `confidence: high`; pushes running only preflight; no GitHub workflows at all) and asked what "focus on local CI" should mean, the operator chose all four options, verbatim labels:

1. **Close the rule gaps (Recommended)**: CI checks against the base branch for sources/ add-only, the confidence floor, no em dashes in new or changed lines, and no AI attribution in commit messages, each with its own test.
2. **Chain it into every push**: the pre-push hook runs the full tools/ci-local.sh, not just preflight, and refuses the push if any step fails.
3. **One-command setup**: tools/setup-local.sh also installs the git hooks and checks prerequisites, so a fresh clone has local CI working in one step.
4. **Never use GitHub Actions**: CI is local only for goatconf, the way claude-brain decided on 2026-10-05, and no .github/workflows is ever added.
