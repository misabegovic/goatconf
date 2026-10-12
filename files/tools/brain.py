#!/usr/bin/env python3
"""brain — small CLI for keeping the brain wiki coherent at scale.

Subcommands:
  validate    — check frontmatter conformance across all wiki pages
  check       — verify every wiki page's `sources:` citations resolve
                (file paths exist, URLs return 2xx). --no-net skips URL
                checks.
  stats       — counts by kind / status / team / repo / confidence;
                orphans; stale pages
  views       — emit auto-generated index pages under wiki/_views/
                (also computes consumed_by reverse edges and token
                counts in pages.json)
  coverage    — for a sibling repo, show top-level dirs covered vs not
                by pages claiming that repo
  serve       — read-only HTTP API over the brain (pages, views,
                search proxy to mempalace). localhost only.
  promote     — scaffold an initiative page from an insight; set
                supersedes / superseded_by both ways.
  cluster     — TF-IDF + HDBSCAN clustering across wiki bodies.
  check-home-fresh — CI guard: any wiki/ edit on the current branch
                must be paired with a wiki/index.md edit (the home
                page dashboard). See wiki/brain/adrs/home-content-shape.md.
  sync-cursor — get/set/diff per-sibling-repo sync cursors at
                wiki/_state/sync-cursors.json. wiki-ingest consults
                these to do incremental ingests instead of re-walking
                whole sibling trees on every pass.

Run with the mempalace venv:
  ~/.local/share/mempalace-venv/bin/python3 tools/brain.py <cmd>
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import functools
import hashlib
import http.server
import math
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

# Locate the brain repo root. Default: the parent of tools/ relative to
# this script. `$BRAIN_DIR` overrides — set it when running tools/brain.py
# against a brain shell scaffolded by `brain.py init` at a different
# location (per the extractable-brain-shell PRD).
REPO = Path(
    os.environ.get("BRAIN_DIR")
    or Path(__file__).resolve().parent.parent
).resolve()
WIKI = REPO / "wiki"


def config_path() -> Path:
    """tabula's config, read as tabula reads it: `tabula.config.yml`, with
    `brain.config.yml` as the fallback for the release tabula keeps it."""
    new = REPO / "tabula.config.yml"
    return new if new.exists() or not (REPO / "brain.config.yml").exists() else REPO / "brain.config.yml"
INDEX = WIKI / "index.md"
TEMPLATES = REPO / "tools" / "templates"


def _load_repo_dotenv() -> None:
    """Fold the repo-local .env into the environment (environ wins).

    The .env is the machine-local config surface (LOCAL_FIRST,
    BRAIN_PROJECTS_ROOT); it is gitignored, so values never leak
    into CI — the runner simply falls back to defaults.
    """
    dotenv = REPO / ".env"
    if not dotenv.exists():
        return
    for line in dotenv.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_repo_dotenv()

PROJECTS = Path(
    os.environ.get("BRAIN_PROJECTS_ROOT", str(Path.home() / "projects"))
).expanduser()

SYNC_CURSORS = WIKI / "_state" / "sync-cursors.json"
EFFORTS_DIR = WIKI / "_state" / "efforts"
ATTENTION_DIR = WIKI / "_state" / "attention"
ATTENTION_TIERS = ("now", "next", "watch", "untriaged")
ENOLA_RECEIPTS = WIKI / "_state" / "enola" / "receipts.json"
ENOLA_VERDICTS = WIKI / "_state" / "enola" / "finding-verdicts.json"
SCHEDULE_STATE = WIKI / "_state" / "schedule.json"
ENOLA_VERDICT_KINDS = ("accepted", "rejected", "noise")
ENOLA_CONFIG = REPO / "mcp-arch.yaml"


def today_utc() -> dt.date:
    """Today's date in UTC.

    Used everywhere `views`, `validate`, and `cmd_*` need a "today"
    so the result is invariant across local timezones — otherwise
    the CI runner (UTC) and a developer's machine (e.g. CEST) can
    write different dates into auto-generated `wiki/_views/*` files,
    failing the "views are up to date" gate.
    """
    return dt.datetime.now(dt.timezone.utc).date()

VALID_KINDS = {
    "reference", "initiative", "decision", "entity", "meta", "overlap",
    "insight", "epic", "idea", "pitch",
    # Since 2026-09-22, tabula's definitions layer: an agent page (a
    # mandate and the verbs it may call) and a workflow page (steps that
    # name an agent and the journal entry each leaves). Validated in
    # depth by tabula; brain.py only admits the kinds.
    "agent", "workflow", "architecture",
    # Since 2026-09-24, a library entry (wiki/tabula/adrs/the-library-page.tabula):
    # brain.py checks its kind, its headings and its two closed fields; the
    # parsed sections (provenance, roles, signatures, alternatives, laws,
    # guarantees) are tabula's alone.
    "pattern",
}
# The frontmatter a kind requires beyond REQUIRED_FIELDS, each from its
# closed set, as tabula's schema states it.
REQUIRED_VALUES_BY_KIND = {
    "pattern": {
        "form": ["style", "pattern", "practice", "tactic", "technology"],
        "domain": ["software", "hardware"],
    },
}
# `draft | living | superseded | archived` is the brain's general
# lifecycle. `proposed | accepted | deprecated` is Nygard's canonical
# ADR lifecycle, accepted alongside for `kind: decision`. `suggested`
# is the AI-suggestion shape (used with `ai_suggestion: true`) and
# graduates to `accepted` when a human approves.
VALID_STATUSES = {
    "draft", "living", "superseded", "archived",
    "proposed", "accepted", "deprecated", "suggested",
}
VALID_CONFIDENCES = {"high", "medium", "low"}
REQUIRED_FIELDS = {"title", "kind", "status", "updated", "sources"}

# Names valid in `repos:` and `affects:` lists. `brain` and `org` are
# meta levels (the brain itself / the organisation as a whole), used
# by org-level pages and brain self-tracking.
# Four scope tiers, read from tabula.config.yml's `<tier>_repos` lists,
# the one place tabula and this file share (`tabula scope add|tier` writes
# them with the AGENTS.md tables). `active`: the estate modifies it.
# `reference`: outside code read for what it teaches. `frozen`: tracked once,
# now closed to the operator, shelf true as of a stated date. Per
# wiki/brain/adrs/scope-says-whose-code-it-is.md and
# wiki/tabula/adrs/cursors-and-scope-in-tabula.tabula.
def _config_tiers() -> dict:
    # A scratch brain (BRAIN_DIR) with no config of its own reads the tiers
    # of the brain this tool belongs to, as the hard-coded sets once did.
    path = config_path()
    if not path.exists():
        home = Path(__file__).resolve().parent.parent
        path = next((home / n for n in ("tabula.config.yml", "brain.config.yml") if (home / n).exists()), path)
    try:
        cfg = yaml.safe_load(path.read_text()) or {}
    except (OSError, yaml.YAMLError):
        cfg = {}
    return {t: set(cfg.get(f"{t}_repos") or []) for t in ("active", "reference", "frozen", "archived")}


_TIERS = _config_tiers()
ACTIVE_REPOS = _TIERS["active"]
REFERENCE_REPOS = _TIERS["reference"]
FROZEN_REPOS = _TIERS["frozen"]
SCOPE_TIERS = {"active": ACTIVE_REPOS, "reference": REFERENCE_REPOS,
               "frozen": FROZEN_REPOS}
ARCHIVED_REPOS = _TIERS["archived"]
META_LEVELS = {"brain", "org"}
VALID_REPOS = (ACTIVE_REPOS | REFERENCE_REPOS | FROZEN_REPOS
               | ARCHIVED_REPOS | META_LEVELS)

# Each list is the *minimum* set of `## ` headings the validator
# requires. For `kind: decision`, two valid section sets coexist —
# the brain's legacy What/Why/How/Alternatives/Consequences and
# Nygard's canonical Context/Alternatives/Consequences (the "Decision"
# is implicit in the page title under MADR conventions). The
# validator accepts either; new ADRs should follow the Nygard set
# per `tools/templates/adr.md`.
REQUIRED_SECTIONS_BY_KIND = {
    "overlap": ["Items", "Overlap", "Recommendation"],
    "insight": ["Pattern", "Evidence", "Affected personas", "Implications",
                "Status"],
    "epic": ["Objective", "Background", "Affected personas", "Scope",
             "No-gos", "Children", "Success metrics"],
    # `kind: pitch` — pre-bet Shape Up pitch. Per
    # `wiki/brain/adrs/shape-up-pitches.md`.
    "pitch": ["Problem", "Appetite", "Solution", "Rabbit holes", "No-gos"],
    # `kind: idea` — raw scratchpad / "potentially useful" content
    # distinct from the formal AI-suggestion ADR/PRD pipeline. Per
    # `wiki/brain/ai-suggestions/adrs/ideas-vs-suggestions-vs-permanent-separation.md`.
    "idea": ["What", "Why interesting", "Maturity"],
    # `kind: pattern`, a library entry. Per
    # `wiki/tabula/adrs/the-library-page.tabula`.
    "pattern": ["What it is", "Where it came from", "Outcomes it trades"],
}
DECISION_SECTION_SETS = [
    # Legacy (pre-2026-05-03 templates).
    ["What", "Why", "How", "Alternatives", "Consequences"],
    # Nygard / MADR / AWS prescriptive guidance — the research-grounded
    # canonical shape, used by `tools/templates/adr.md` from 2026-05-03.
    ["Context", "Alternatives", "Consequences"],
    # AI-suggestion variant — `tools/templates/adr-ai-suggestion.md`.
    ["Context", "Inferred decision", "Considered options (agent surfacing)",
     "Inferred consequences"],
]
# `kind: initiative` accepts any of three valid section shapes
# (legacy / new PRD / AI-suggestion PRD). Validation passes if any
# of the listed shapes is fully present.
INITIATIVE_SECTION_SETS = [
    # Legacy What/How/Why/Now/Perceived/Target (pre-2026-05-03).
    ["What", "How", "Why", "Now", "Perceived", "Target"],
    # 2026-05-03 PRD template — Aha! / ProductPlan-grounded sections.
    ["Objective", "Background", "Affected personas", "Scope",
     "No-gos", "Rabbit holes", "Appetite", "Decision needed"],
    # AI-suggestion PRD variant — `tools/templates/prd-ai-suggestion.md`.
    ["Why the agent suggests this", "Inferred objective",
     "Affected personas (agent-inferred)", "Scope (suggested)",
     "Suggested next step"],
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

# The brain UI's home page (wiki/index.md) is an agent-maintained
# dashboard with a fixed section list, the home contract per
# wiki/brain/adrs/home-content-shape.md. Section anchor + name +
# owning skill are constants; `empty` is computed per call by
# parsing the home file. Adding a section here is a deliberate
# schema change (PRD-level decision).
HOME_SECTIONS = [
    {"anchor": "what-changed",        "name": "What changed",        "maintained_by": "/in"},
    {"anchor": "drift-surface",       "name": "Drift surface",       "maintained_by": "/groom"},
    {"anchor": "open-initiatives",    "name": "Open initiatives",    "maintained_by": "/shape"},
    {"anchor": "recent-decisions",    "name": "Recent decisions",    "maintained_by": "/shape"},
    {"anchor": "insights-now",        "name": "Insights now",        "maintained_by": "/feedback"},
    {"anchor": "brain-trajectory",    "name": "Brain trajectory",    "maintained_by": "/sync"},
    {"anchor": "curated-picks",       "name": "Curated picks",       "maintained_by": "/in"},
    {"anchor": "where-to-find-things", "name": "Where to find things", "maintained_by": "/in"},
]


def home_sections_state() -> list[dict]:
    """Read wiki/index.md and return per-section metadata for pages.json.

    Each entry: {anchor, name, maintained_by, empty}. `empty` is True
    when the section's body contains the empty marker
    `<!-- home-section: empty ... -->` or when the section heading
    is absent.

    See wiki/brain/adrs/home-content-shape.md § How for the
    convention.
    """
    out: list[dict] = []
    if not INDEX.exists():
        for s in HOME_SECTIONS:
            out.append({**s, "empty": True})
        return out
    text = INDEX.read_text()
    for s in HOME_SECTIONS:
        heading = re.compile(r"^## " + re.escape(s["name"]) + r"\s*$", re.MULTILINE)
        m = heading.search(text)
        if not m:
            out.append({**s, "empty": True})
            continue
        rest = text[m.end():]
        next_h = re.search(r"^## ", rest, re.MULTILINE)
        body = rest[:next_h.start()] if next_h else rest
        empty = "<!-- home-section: empty" in body
        out.append({**s, "empty": empty})
    return out

REPO_SKIP_DIRS = {
    ".git", "node_modules", "vendor", "tmp", "log", "coverage",
    ".bundle", ".cache", "dist", "build", "target", "__pycache__",
}


PAGE_SUFFIXES = (".md", ".tabula")


def wiki_files() -> list[Path]:
    """Every page file under wiki/: `.md`, and since 2026-09-22 `.tabula`, a
    page with spec sections after the prose (see wiki/tabula/adrs/
    the-tabula-file-parsed-and-evaluated.md). Sorted; no other filtering."""
    return sorted(p for p in WIKI.rglob("*") if p.is_file() and p.suffix in PAGE_SUFFIXES)


def wiki_pages() -> list[Path]:
    """All wiki pages except index.md and anything under wiki/_*/."""
    out = []
    for p in wiki_files():
        rel = p.relative_to(WIKI)
        if rel == Path("index.md"):
            continue
        if any(part.startswith("_") for part in rel.parts):
            continue
        out.append(p)
    return sorted(out)


def parse(path: Path) -> tuple[dict, str] | None:
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    return meta, m.group(2)


def index_links() -> set[str]:
    """Return set of hrefs (wiki-relative) referenced from any index.md.

    Walks `wiki/index.md` plus every nested `wiki/<dir>/index.md`
    (excluding `wiki/_*/`). Per-repo nested structure — where a repo's
    ADRs and PRDs are listed in `wiki/<repo>/index.md` rather than the
    top-level index — should not produce orphans.
    """
    out: set[str] = set()
    for index_file in WIKI.rglob("index.md"):
        rel = index_file.relative_to(WIKI)
        if any(part.startswith("_") for part in rel.parts):
            continue
        text = index_file.read_text()
        index_dir = index_file.parent
        for href in re.findall(r"\]\(([^)]+\.(?:md|tabula))\)", text):
            target = (index_dir / href).resolve()
            try:
                rel_target = target.relative_to(WIKI)
                out.add(str(rel_target))
            except ValueError:
                continue
    return out


_TIKTOKEN_ENC = None


def approx_tokens(body: str) -> int:
    """Token count via tiktoken cl100k_base when available; chars/4 fallback.

    cl100k_base is OpenAI's tokenizer; close enough to Anthropic's for
    load-planning heuristics. Falling back to chars/4 keeps the function
    cheap and pure when the dep is missing.
    """
    global _TIKTOKEN_ENC
    if _TIKTOKEN_ENC is None:
        try:
            import tiktoken  # type: ignore
            _TIKTOKEN_ENC = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _TIKTOKEN_ENC = False  # sentinel: missing
    if _TIKTOKEN_ENC:
        return len(_TIKTOKEN_ENC.encode(body))
    return max(1, len(body) // 4)


def cmd_validate(_args) -> int:
    errors: list[str] = []
    pages = wiki_pages()
    on_disk = {str(p.relative_to(WIKI)) for p in pages}

    for p in pages:
        rel = p.relative_to(REPO)
        parsed = parse(p)
        if parsed is None:
            errors.append(f"{rel}: missing or unparseable frontmatter")
            continue
        meta, body = parsed

        missing = REQUIRED_FIELDS - set(meta or {})
        if missing:
            errors.append(f"{rel}: missing fields: {sorted(missing)}")

        kind = meta.get("kind")
        if kind not in VALID_KINDS:
            errors.append(f"{rel}: invalid kind {kind!r}")
        values = REQUIRED_VALUES_BY_KIND.get(kind, {}) if isinstance(kind, str) else {}
        for field, allowed in values.items():
            if meta.get(field) not in allowed:
                errors.append(f"{rel}: invalid {field} {meta.get(field)!r}; "
                              f"a {kind} page's {field} is one of {allowed}")

        status = meta.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{rel}: invalid status {status!r}")

        conf = meta.get("confidence")
        if conf is not None and conf not in VALID_CONFIDENCES:
            errors.append(f"{rel}: invalid confidence {conf!r}")

        upd = meta.get("updated")
        if isinstance(upd, str):
            try:
                dt.date.fromisoformat(upd)
            except ValueError:
                errors.append(f"{rel}: updated is not ISO date: {upd!r}")
        elif not isinstance(upd, dt.date):
            errors.append(f"{rel}: updated is not a date: {upd!r}")

        srcs = meta.get("sources") or []
        if status != "draft" and not srcs and "sources" not in missing:
            errors.append(f"{rel}: non-draft page has empty sources")

        for dep in meta.get("depends_on") or []:
            if dep not in on_disk:
                errors.append(f"{rel}: depends_on points at unknown page: {dep}")

        for r in meta.get("repos") or []:
            if r not in VALID_REPOS:
                errors.append(f"{rel}: repos contains unknown repo: {r}")
        for r in meta.get("affects") or []:
            if r not in VALID_REPOS:
                errors.append(f"{rel}: affects contains unknown repo: {r}")

        for field in ("supersedes", "superseded_by"):
            ref = meta.get(field)
            if ref and ref not in on_disk:
                errors.append(f"{rel}: {field} points at unknown page: {ref}")

        rel_to_wiki = p.relative_to(WIKI)
        parts = rel_to_wiki.parts
        if kind == "epic":
            if len(parts) >= 3 and parts[1] == "epics":
                scope = parts[0]
                slug_with_ext = parts[-1]
                expected_adr = f"{scope}/adrs/{slug_with_ext}"
                if expected_adr in on_disk:
                    errors.append(
                        f"{rel}: kind=epic must not have a matching ADR "
                        f"at wiki/{expected_adr} — epics have no umbrella "
                        f"ADR pair (decisions live in children)"
                    )
            else:
                errors.append(
                    f"{rel}: kind=epic must live at "
                    f"wiki/<scope>/epics/<slug>.md"
                )

        parent_epic = meta.get("parent_epic")
        if parent_epic and parts:
            scope = parts[0]
            expected = f"{scope}/epics/{parent_epic}.md"
            if expected not in on_disk:
                errors.append(
                    f"{rel}: parent_epic={parent_epic!r} does not resolve "
                    f"— expected wiki/{expected} to exist"
                )

        present = set(HEADING_RE.findall(body))
        if kind == "decision":
            # `kind: decision` accepts any of several section shapes
            # (legacy / Nygard / AI-suggestion). Validation passes if
            # *any* of the listed shapes is fully present.
            if not any(all(s in present for s in shape)
                       for shape in DECISION_SECTION_SETS):
                errors.append(
                    f"{rel}: kind=decision missing required sections; "
                    f"need one of {DECISION_SECTION_SETS}"
                )
        elif kind == "initiative":
            # Same shape-flexibility for `kind: initiative` —
            # legacy / new PRD / AI-suggestion variants all valid.
            if not any(all(s in present for s in shape)
                       for shape in INITIATIVE_SECTION_SETS):
                errors.append(
                    f"{rel}: kind=initiative missing required sections; "
                    f"need one of {INITIATIVE_SECTION_SETS}"
                )
        else:
            required_sections = REQUIRED_SECTIONS_BY_KIND.get(kind, [])
            if required_sections:
                missing_sections = [s for s in required_sections
                                    if s not in present]
                if missing_sections:
                    errors.append(
                        f"{rel}: kind={kind} missing required sections: "
                        f"{missing_sections}"
                    )

    indexed = index_links()
    orphan = sorted(on_disk - indexed)
    if orphan:
        for o in orphan:
            errors.append(f"orphan (not in index.md): wiki/{o}")
    dead = sorted(indexed - on_disk)
    for d in dead:
        if not (WIKI / d).exists():
            errors.append(f"dead index link: wiki/{d}")

    if errors:
        for e in errors:
            print(f"ERROR  {e}")
        print(f"\n{len(errors)} error(s) across {len(pages)} page(s)")
        return 1

    print(f"OK  {len(pages)} page(s) valid")
    return 0


def _classify_source(src: str, page: Path | None = None) -> str:
    if src.startswith(("http://", "https://")):
        return "url"
    if src.startswith("~"):
        return "home-path"
    if src.startswith("/"):
        return "abs-path"
    if src.startswith(("sources/", "tools/", "wiki/", "log/", ".claude/",
                       "../")):
        return "repo-path"
    # Anything that actually resolves — repo-root files like AGENTS.md or
    # mcp-arch.yaml, top-level dirs the prefix list never learned about
    # (.github/, ui/), and page-relative citations. The prefix list stays
    # ahead of this so a *missing* wiki/… path still reports broken rather
    # than merely unclassifiable; this only rescues citations that are real
    # and were being reported as suspicious for their shape alone.
    if (REPO / src).exists():
        return "repo-path"
    if page is not None and (page.parent / src).exists():
        return "repo-path"
    return "unknown"


@functools.lru_cache(maxsize=None)
def _sibling_recent_refs(sibling: str) -> tuple[str, ...]:
    res = subprocess.run(
        ["git", "-C", sibling, "for-each-ref",
         "--sort=-committerdate",
         "--format=%(refname:short)",
         "refs/heads", "refs/remotes/origin"],
        capture_output=True, text=True, timeout=10,
    )
    if res.returncode != 0:
        return ()
    return tuple(r for r in res.stdout.split() if not r.endswith("/HEAD"))


@functools.lru_cache(maxsize=None)
def _branch_carrying_path(sibling: str, rel: str) -> str | None:
    refs = _sibling_recent_refs(sibling)
    if not refs:
        return None
    batch = subprocess.run(
        ["git", "-C", sibling, "cat-file", "--batch-check=%(objectname)"],
        input="".join(f"{ref}:{rel}\n" for ref in refs),
        capture_output=True, text=True, timeout=30,
    )
    if batch.returncode != 0:
        return None
    for ref, line in zip(refs, batch.stdout.splitlines()):
        if "missing" not in line:
            return ref
    return None


def _check_path(p: str, page: Path | None = None) -> tuple[str, str]:
    """Resolve a cited path. Returns (status, detail) where status is
    one of 'ok' / 'broken' / 'skipped'. 'skipped' is used when the path
    points into a sibling repo that doesn't exist on this machine (e.g.
    the CI runner doesn't have ~/projects/<repo>): that's not a
    broken citation, just unverifiable here.
    """
    if " (" in p:
        status, detail = _check_path(p[:p.index(" (")].rstrip(), page=page)
        if status == "broken":
            return "skipped", "annotated citation marks a path knowingly not current: " + p
        return status, detail

    candidate = Path(os.path.expanduser(p))

    # Legacy-path remap: brain pages were authored assuming
    # `~/projects/<repo>/...` but the operator may have configured
    # `$BRAIN_PROJECTS_ROOT` to point elsewhere (e.g. `~/src/`).
    # If the literal path doesn't exist but `PROJECTS/<repo>/<rest>`
    # does, prefer that. Mirrors the per-skill sibling-repo handling.
    if candidate.is_absolute() and not candidate.exists():
        try:
            home_projects = Path(os.path.expanduser("~/projects"))
            rel = candidate.relative_to(home_projects)
            if rel.parts and PROJECTS != home_projects:
                remapped = PROJECTS / rel
                if remapped.exists():
                    return "ok", str(remapped)
        except ValueError:
            pass

    # Detect "sibling repo not on this machine" — a path under the
    # configured PROJECTS root where <repo> doesn't exist locally.
    if candidate.is_absolute():
        try:
            rel_to_projects = candidate.relative_to(PROJECTS)
            if rel_to_projects.parts:
                sibling = PROJECTS / rel_to_projects.parts[0]
                if not sibling.exists():
                    return "skipped", (
                        f"sibling repo not on this machine: {sibling}"
                    )
        except ValueError:
            pass
        # Also check legacy ~/projects/ root for the skip-when-absent
        try:
            home_projects = Path(os.path.expanduser("~/projects"))
            rel_to_home = candidate.relative_to(home_projects)
            if rel_to_home.parts:
                # Sibling not at PROJECTS root → skip rather than fail
                sibling_at_projects = PROJECTS / rel_to_home.parts[0]
                if not sibling_at_projects.exists():
                    return "skipped", (
                        f"sibling repo not on this machine: {sibling_at_projects}"
                    )
        except ValueError:
            pass

    # Branch-aware fallback: a sibling-repo path absent from the
    # working tree may still exist on another local/remote branch tip
    # (e.g. prototype-branch work cited before its main merge). That is
    # the feature-branch caveat from the sibling-handling rule, not a
    # broken citation.
    if candidate.is_absolute() and not candidate.exists():
        for root in (PROJECTS, Path(os.path.expanduser("~/projects"))):
            try:
                rel = candidate.relative_to(root)
            except ValueError:
                continue
            if len(rel.parts) < 2:
                continue
            sibling = PROJECTS / rel.parts[0]
            if not (sibling / ".git").exists():
                continue
            inner = "/".join(rel.parts[1:])
            ref = _branch_carrying_path(str(sibling), inner)
            if ref:
                return "skipped", (
                    f"on branch {ref} of {sibling.name}, "
                    f"not in the working tree"
                )
            break

    if candidate.is_absolute() and candidate.exists():
        return "ok", str(candidate)
    if page is not None and not candidate.is_absolute():
        page_rel = (page.parent / candidate).resolve()
        if page_rel.exists():
            return "ok", str(page_rel)
    repo_rel = (REPO / candidate).resolve()
    if repo_rel.exists():
        return "ok", str(repo_rel)
    return "broken", f"missing: {repo_rel}"


def _check_url(url: str, timeout: int = 6) -> tuple[bool, str]:
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "brain-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if 200 <= resp.status < 400:
                return True, str(resp.status)
            return False, str(resp.status)
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                req2 = urllib.request.Request(url, headers={
                    "User-Agent": "brain-check",
                    "Range": "bytes=0-0",
                })
                with urllib.request.urlopen(req2, timeout=timeout) as resp2:
                    return (200 <= resp2.status < 400), str(resp2.status)
            except Exception as e2:
                return False, f"GET failed: {e2}"
        return False, f"{e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def cmd_check(args) -> int:
    """Verify every wiki page's sources: frontmatter resolves."""
    pages = wiki_pages()
    if args.page:
        target = WIKI / args.page
        if not target.exists():
            print(f"page not found: {target}")
            return 2
        pages = [target]

    broken: list[tuple[Path, str, str, str]] = []
    suspicious: list[tuple[Path, str]] = []
    skipped: list[tuple[Path, str, str]] = []
    checked = 0

    for p in pages:
        parsed = parse(p)
        if parsed is None:
            continue
        meta, _ = parsed
        for src in (meta.get("sources") or []):
            if not isinstance(src, str):
                continue
            checked += 1
            kind = _classify_source(src, page=p)
            if kind == "url":
                if args.no_net:
                    continue
                ok, reason = _check_url(src)
                if not ok:
                    broken.append((p, src, kind, reason))
            elif kind in ("home-path", "abs-path", "repo-path"):
                status, detail = _check_path(src, page=p)
                if status == "broken":
                    broken.append((p, src, kind, detail))
                elif status == "skipped":
                    skipped.append((p, src, detail))
            else:
                suspicious.append((p, src))

    if broken:
        print(f"BROKEN ({len(broken)}):")
        for page, src, kind, reason in broken:
            print(f"  {page.relative_to(REPO)}")
            print(f"    {kind}: {src}  →  {reason}")
    if suspicious:
        print(f"\nSUSPICIOUS ({len(suspicious)}):")
        for page, src in suspicious:
            print(f"  {page.relative_to(REPO)}: {src}")
    if skipped and args.verbose:
        print(f"\nSKIPPED ({len(skipped)}, sibling repos not on this machine):")
        for page, src, _ in skipped:
            print(f"  {page.relative_to(REPO)}: {src}")

    print(f"\n{checked} sources checked across {len(pages)} pages")
    if broken:
        print(f"  {len(broken)} broken")
    if suspicious:
        print(f"  {len(suspicious)} suspicious (couldn't classify)")
    if skipped:
        print(f"  {len(skipped)} skipped (sibling repos not on this machine; "
              f"use --verbose to list)")

    return 1 if broken else 0


def cmd_stats(_args) -> int:
    pages = wiki_pages()
    by_kind: dict[str, int] = collections.Counter()
    by_status: dict[str, int] = collections.Counter()
    by_conf: dict[str, int] = collections.Counter()
    by_team: dict[str, int] = collections.Counter()
    by_repo: dict[str, int] = collections.Counter()
    stale: list[tuple[Path, int]] = []
    today = today_utc()

    for p in pages:
        parsed = parse(p)
        if parsed is None:
            continue
        meta, _ = parsed
        by_kind[meta.get("kind", "?")] += 1
        by_status[meta.get("status", "?")] += 1
        by_conf[meta.get("confidence", "?")] += 1
        if t := meta.get("team"):
            by_team[t] += 1
        for r in meta.get("repos") or []:
            by_repo[r] += 1
        upd = meta.get("updated")
        if isinstance(upd, str):
            try:
                upd = dt.date.fromisoformat(upd)
            except ValueError:
                continue
        if isinstance(upd, dt.date):
            age = (today - upd).days
            if age > 90:
                stale.append((p, age))

    def show(label: str, counter):
        print(f"\n{label}:")
        for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {k:<14} {v}")

    print(f"pages: {len(pages)}")
    show("by kind", by_kind)
    show("by status", by_status)
    show("by confidence", by_conf)
    if by_team:
        show("by team", by_team)
    if by_repo:
        show("by repo", by_repo)

    indexed = index_links()
    on_disk = {str(p.relative_to(WIKI)) for p in pages}
    orphan = sorted(on_disk - indexed)
    if orphan:
        print("\norphans (not in index.md):")
        for o in orphan:
            print(f"  wiki/{o}")
    if stale:
        print(f"\nstale (>90 days): {len(stale)}")
        for p, age in sorted(stale, key=lambda x: -x[1]):
            print(f"  {p.relative_to(REPO)}  ({age} days)")
    return 0


def collect_pages_data() -> list[dict]:
    """Build the structured per-page list used by views and serve."""
    pages = wiki_pages()
    out = []
    for p in pages:
        parsed = parse(p)
        if parsed is None:
            continue
        meta, body = parsed
        entry = {"path": str(p.relative_to(WIKI)), **meta}
        u = entry.get("updated")
        if isinstance(u, dt.date):
            entry["updated"] = u.isoformat()
        entry["tokens"] = approx_tokens(body)
        out.append(entry)

    # Compute reverse edges for depends_on → consumed_by.
    consumed_by: dict[str, list[str]] = collections.defaultdict(list)
    for entry in out:
        for dep in entry.get("depends_on") or []:
            consumed_by[dep].append(entry["path"])
    for entry in out:
        rev = sorted(consumed_by.get(entry["path"], []))
        if rev:
            entry["consumed_by"] = rev

    # Compute reverse edges for affects → affected_by.
    # `affects:` is a list of repo names. For each page X with
    # affects=[r1, r2, ...], the repo's index page (`<r>/index.md`)
    # gets X listed under `affected_by:`. This surfaces cross-level
    # propagation from the repo side.
    by_repo_affected: dict[str, list[str]] = collections.defaultdict(list)
    for entry in out:
        for r in entry.get("affects") or []:
            by_repo_affected[r].append(entry["path"])
    for entry in out:
        path = entry["path"]
        # Only repo index pages collect affected_by.
        # Match `<repo>/index.md` exactly (no nested folders).
        parts = path.split("/")
        if len(parts) == 2 and parts[1] == "index.md":
            repo = parts[0]
            affecting = sorted(
                p for p in by_repo_affected.get(repo, []) if p != path
            )
            if affecting:
                entry["affected_by"] = affecting

    # Compute reverse edges for parent_epic → child_prds + child_adrs.
    # parent_epic: <slug> on a page (PRD or ADR) names the epic this
    # work belongs to. The epic page (kind: epic) collects child_prds
    # and child_adrs separately, so readers can see PRD vs ADR
    # membership at a glance without filtering by kind.
    epic_children_prds: dict[str, list[str]] = collections.defaultdict(list)
    epic_children_adrs: dict[str, list[str]] = collections.defaultdict(list)
    for entry in out:
        parent = entry.get("parent_epic")
        if not parent:
            continue
        path = entry["path"]
        path_parts = path.split("/")
        if not path_parts:
            continue
        scope = path_parts[0]
        epic_path = f"{scope}/epics/{parent}.md"
        if entry.get("kind") == "decision":
            epic_children_adrs[epic_path].append(path)
        else:
            epic_children_prds[epic_path].append(path)
    for entry in out:
        if entry.get("kind") != "epic":
            continue
        path = entry["path"]
        cp = sorted(epic_children_prds.get(path, []))
        ca = sorted(epic_children_adrs.get(path, []))
        if cp:
            entry["child_prds"] = cp
        if ca:
            entry["child_adrs"] = ca
    return out


def cmd_views(_args) -> int:
    views_dir = WIKI / "_views"
    views_dir.mkdir(exist_ok=True)

    entries = collect_pages_data()

    by_kind: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)
    by_team: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)
    by_repo: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)

    for entry in entries:
        title = entry.get("title", entry["path"])
        status = entry.get("status", "?")
        rec = (title, entry["path"], status)
        by_kind[entry.get("kind", "?")].append(rec)
        if t := entry.get("team"):
            by_team[t].append(rec)
        for r in entry.get("repos") or []:
            by_repo[r].append(rec)

    today = today_utc().isoformat()

    def write_view(name: str, title: str, groups: dict):
        lines = [
            "---",
            f"title: {title}",
            "kind: meta",
            "status: living",
            f"updated: {today}",
            "confidence: high",
            "sources:",
            "  - tools/brain.py",
            "---",
            "",
            f"# {title}",
            "",
            "Auto-generated by `python tools/brain.py views`. Do not edit "
            "by hand.",
            "",
        ]
        for key in sorted(groups):
            lines.append(f"## {key}")
            lines.append("")
            for ttl, rel, status in sorted(groups[key]):
                lines.append(f"- [{ttl}](../{rel}) — *{status}*")
            lines.append("")
        (views_dir / name).write_text("\n".join(lines))

    write_view("by-kind.md", "Index — by kind", by_kind)
    write_view("by-team.md", "Index — by team", by_team)
    write_view("by-repo.md", "Index — by repo", by_repo)
    write_ai_suggestions_view(views_dir, entries, today)
    write_by_epic_view(views_dir, entries, today)
    write_attention_view(views_dir, today)

    json_out = {
        "generated": today,
        "home_sections": home_sections_state(),
        "pages": entries,
    }
    (views_dir / "pages.json").write_text(json.dumps(json_out, indent=2))

    print(f"wrote {views_dir.relative_to(REPO)}/by-kind.md, by-team.md, "
          f"by-repo.md, by-epic.md, ai-suggestions.md, pages.json")
    print(f"  {len(entries)} pages indexed; "
          f"{sum(1 for e in entries if 'consumed_by' in e)} carry "
          f"computed consumed_by edges; "
          f"{sum(1 for e in entries if 'affected_by' in e)} repos "
          f"carry computed affected_by edges; "
          f"{sum(1 for e in entries if e.get('ai_suggestion'))} "
          f"AI-suggestion drafts cataloged")
    return 0


def scope_for_path(path: str) -> tuple[str, str]:
    """Return (scope_label, scope_slug) for a wiki-relative path.

    `scope_slug` matches a directory name under `wiki/`:
    - "brain" for `brain/...`
    - "org" for `org/...`
    - "<repo>" for any active or archived repo (e.g. "website")
    - "(other)" for paths that don't fit (e.g. wiki-root pages)

    `scope_label` is the human-friendly version with parenthetical
    qualifier: "website (per-repo)", "org (organisation-wide)",
    "brain (meta)", "(other)".
    """
    parts = path.split("/")
    if len(parts) < 2:
        return ("(other)", "(other)")
    head = parts[0]
    if head == "brain":
        return ("brain (meta)", "brain")
    if head == "org":
        return ("org (organisation-wide)", "org")
    if head in VALID_REPOS - META_LEVELS:
        return (f"{head} (per-repo)", head)
    return ("(other)", head)


def write_ai_suggestions_view(views_dir, entries, today):
    """Emit `wiki/_views/ai-suggestions.md` cataloging every page with
    `ai_suggestion: true` across all scopes (per-repo / org / brain).

    The view is the input both to the Starlight UI surface and to
    human review — humans navigating to it should see at a glance
    which suggestions are awaiting review, grouped by scope, with
    enough context to decide whether to dig in.
    """
    suggestions = [e for e in entries if e.get("ai_suggestion")]
    by_scope: dict[str, list[dict]] = collections.defaultdict(list)
    for s in suggestions:
        label, _slug = scope_for_path(s["path"])
        by_scope[label].append(s)

    total = len(suggestions)
    scope_count = len([k for k, v in by_scope.items() if v])

    lines = [
        "---",
        "title: AI suggestions — drafts for human review",
        "kind: meta",
        "status: living",
        f"updated: {today}",
        "confidence: high",
        "sources:",
        "  - tools/brain.py",
        "---",
        "",
        "# AI suggestions — drafts for human review",
        "",
        "Auto-generated by `python tools/brain.py views`. Do not edit "
        "by hand.",
        "",
        "Aggregates every page with `ai_suggestion: true` across the "
        "brain's three scopes: per-repo, org (organisation-wide), and "
        "brain (meta). See `AGENTS.md` § Governance > "
        "`ai_suggestion` for what these are and how they graduate.",
        "",
        f"**{total}** suggestion(s) in **{scope_count}** scope(s) "
        f"awaiting human review.",
        "",
    ]

    if total == 0:
        lines.extend([
            "No AI-suggestion drafts at the moment. The brain is in "
            "a clean human-approved state.",
            "",
        ])
    else:
        # Stable scope ordering: brain → org → per-repo (alphabetical) → other.
        def scope_sort_key(label: str) -> tuple:
            if label.startswith("brain"):
                return (0, label)
            if label.startswith("org"):
                return (1, label)
            if label == "(other)":
                return (3, label)
            return (2, label)

        for scope_label in sorted(by_scope, key=scope_sort_key):
            scope_entries = by_scope[scope_label]
            adrs = [e for e in scope_entries
                    if e.get("kind") == "decision"]
            prds = [e for e in scope_entries
                    if e.get("kind") == "initiative"]
            other = [e for e in scope_entries
                     if e.get("kind") not in ("decision", "initiative")]

            lines.append(f"## {scope_label} — {len(scope_entries)} suggestion(s)")
            lines.append("")

            def emit_kind_block(kind_label: str, items: list[dict]):
                if not items:
                    return
                lines.append(f"### {kind_label}")
                lines.append("")
                for e in sorted(items, key=lambda x: x["path"]):
                    title = e.get("title", e["path"])
                    status = e.get("status", "?")
                    rel = e["path"]
                    lines.append(
                        f"- [{title}](../{rel}) — *{status}* — "
                        f"`{rel}`"
                    )
                lines.append("")

            emit_kind_block("ADRs", adrs)
            emit_kind_block("PRDs", prds)
            emit_kind_block("Other", other)

    lines.extend([
        "## How to graduate a suggestion",
        "",
        "Per `AGENTS.md` § Governance > `ai_suggestion` > Graduation, "
        "a graduation PR:",
        "",
        "1. Drops `ai_suggestion: true` from frontmatter.",
        "2. Removes the AI-suggestion banner.",
        "3. Bumps `confidence:` (typically `low` → `medium`).",
        "4. Changes `status:` from `suggested` to `accepted` (ADR) "
        "or `living` (PRD).",
        "5. Moves the file from `<scope>/ai-suggestions/{adrs,prds}/` "
        "to `<scope>/{adrs,prds}/`.",
        "6. Reshapes inference-mode language to direct-mode and "
        "fixes any factual errors the human reviewer catches.",
        "",
        "Re-scoping is allowed during graduation if the human "
        "decides the suggestion belongs at a different scope.",
        "",
    ])

    (views_dir / "ai-suggestions.md").write_text("\n".join(lines))


def write_by_epic_view(views_dir, entries, today):
    """Emit `wiki/_views/by-epic.md` listing every kind:epic page
    with its children (PRDs + ADRs split, with status inline).

    Per the multi-prd-epic-shape ADR, the view is the brain's
    aggregated index of umbrella-scale work and lets a reader
    answer "what big initiatives are in flight, and how much of
    each has shipped" at a glance. When no epics exist (the v1
    baseline), the view is written as an empty stub so the
    views-up-to-date CI gate has a stable baseline to diff
    against.
    """
    epics = [e for e in entries if e.get("kind") == "epic"]
    by_path = {e["path"]: e for e in entries}

    lines = [
        "---",
        "title: Index — by epic",
        "kind: meta",
        "status: living",
        f"updated: {today}",
        "confidence: high",
        "sources:",
        "  - tools/brain.py",
        "---",
        "",
        "# Index — by epic",
        "",
        "Auto-generated by `python tools/brain.py views`. Do not edit "
        "by hand.",
        "",
        "Aggregates every `kind: epic` umbrella with its children "
        "(`parent_epic:` reverse-edges, split into PRD and ADR "
        "membership). Per `wiki/brain/adrs/multi-prd-epic-shape.md`.",
        "",
        f"**{len(epics)}** epic(s) in flight.",
        "",
    ]

    if not epics:
        lines.extend([
            "No epics yet. The first `/shape <scope> --epic <pitch>` "
            "invocation creates the first one.",
            "",
        ])
    else:
        for epic in sorted(epics, key=lambda e: e["path"]):
            title = epic.get("title", epic["path"])
            status = epic.get("status", "?")
            rel = epic["path"]
            lines.append(f"## [{title}](../{rel}) — *{status}*")
            lines.append("")

            def emit_children(label: str, paths: list[str]):
                if not paths:
                    return
                lines.append(f"### {label}")
                lines.append("")
                for cp in sorted(paths):
                    child = by_path.get(cp, {})
                    ctitle = child.get("title", cp)
                    cstatus = child.get("status", "?")
                    lines.append(
                        f"- [{ctitle}](../{cp}) — *{cstatus}*"
                    )
                lines.append("")

            emit_children("PRDs", epic.get("child_prds") or [])
            emit_children("ADRs", epic.get("child_adrs") or [])

            if not (epic.get("child_prds") or epic.get("child_adrs")):
                lines.append("*(no children yet)*")
                lines.append("")

    (views_dir / "by-epic.md").write_text("\n".join(lines))


def cmd_coverage(args) -> int:
    repo_name = args.repo
    repo_path = PROJECTS / repo_name
    if not repo_path.exists():
        print(_missing_sibling_msg(repo_path))
        return 1

    pages = wiki_pages()
    relevant: list[tuple[Path, dict, str]] = []
    for p in pages:
        parsed = parse(p)
        if parsed is None:
            continue
        meta, body = parsed
        if repo_name in (meta.get("repos") or []):
            relevant.append((p, meta, body))

    repo_dirs = sorted(
        d.name for d in repo_path.iterdir()
        if d.is_dir() and d.name not in REPO_SKIP_DIRS
        and not d.name.startswith(".")
    )

    covered: set[str] = set()
    coverage_by_dir: dict[str, list[str]] = collections.defaultdict(list)
    for d in repo_dirs:
        for p, meta, body in relevant:
            srcs_str = " ".join(str(s) for s in (meta.get("sources") or []))
            if d in body or d in srcs_str:
                covered.add(d)
                coverage_by_dir[d].append(str(p.relative_to(REPO)))

    uncovered = [d for d in repo_dirs if d not in covered]

    print(f"coverage for {repo_name} (top-level dirs):")
    print(f"  pages claiming this repo: {len(relevant)}")
    print(f"  dirs covered: {len(covered)}/{len(repo_dirs)}")

    if covered:
        print("\ncovered:")
        for d in sorted(covered):
            pages_for_d = coverage_by_dir[d]
            print(f"  {d:<20} {pages_for_d[0]}"
                  f"{' (+' + str(len(pages_for_d)-1) + ' more)' if len(pages_for_d) > 1 else ''}")

    if uncovered:
        print("\nuncovered:")
        for d in uncovered:
            print(f"  {d}")

    return 0 if not uncovered else 2


def cmd_serve(args) -> int:
    """Read-only HTTP API for the brain. localhost only by default."""
    port = args.port
    host = args.host

    entries_cache: list[dict] = []

    def refresh_cache():
        entries_cache.clear()
        entries_cache.extend(collect_pages_data())

    refresh_cache()

    class Handler(http.server.BaseHTTPRequestHandler):
        def _send_json(self, code: int, body) -> None:
            data = json.dumps(body, indent=2).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _send_text(self, code: int, body: str,
                       ctype: str = "text/markdown; charset=utf-8") -> None:
            data = body.encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, fmt, *args):
            sys.stderr.write(f"{self.address_string()} - {fmt % args}\n")

        def do_GET(self):  # noqa: N802
            url = urllib.parse.urlparse(self.path)
            path = url.path.rstrip("/") or "/"
            qs = urllib.parse.parse_qs(url.query)

            if path == "/":
                self._send_json(200, {
                    "endpoints": [
                        "/pages.json",
                        "/pages/<wiki-relative-path>",
                        "/views/by-kind",
                        "/views/by-team",
                        "/views/by-repo",
                        "/search?q=<query>",
                        "/refresh",
                    ],
                    "page_count": len(entries_cache),
                })
                return

            if path == "/pages.json":
                self._send_json(200, {
                    "generated": today_utc().isoformat(),
                    "pages": entries_cache,
                })
                return

            if path.startswith("/pages/"):
                rel = path[len("/pages/"):]
                target = WIKI / rel
                if not target.exists() or ".." in rel:
                    self._send_json(404, {"error": "not found"})
                    return
                parsed = parse(target)
                if parsed is None:
                    self._send_json(500, {"error": "unparseable"})
                    return
                meta, body = parsed
                u = meta.get("updated")
                if isinstance(u, dt.date):
                    meta["updated"] = u.isoformat()
                self._send_json(200, {
                    "path": rel,
                    "meta": meta,
                    "body": body,
                    "tokens": approx_tokens(body),
                })
                return

            if path.startswith("/views/"):
                axis = path[len("/views/"):]
                if axis not in {"by-kind", "by-team", "by-repo"}:
                    self._send_json(404, {"error": "unknown view"})
                    return
                groups: dict[str, list[dict]] = collections.defaultdict(list)
                for entry in entries_cache:
                    keys: list[str] = []
                    if axis == "by-kind":
                        keys = [entry.get("kind", "?")]
                    elif axis == "by-team":
                        if t := entry.get("team"):
                            keys = [t]
                    elif axis == "by-repo":
                        keys = list(entry.get("repos") or [])
                    for k in keys:
                        groups[k].append({
                            "path": entry["path"],
                            "title": entry.get("title", entry["path"]),
                            "status": entry.get("status", "?"),
                        })
                self._send_json(200, {"axis": axis, "groups": dict(groups)})
                return

            if path == "/search":
                q = (qs.get("q") or [""])[0]
                if not q:
                    self._send_json(400, {"error": "missing q"})
                    return
                try:
                    out = subprocess.run(
                        ["mempalace", "search", q],
                        check=False, capture_output=True, text=True, timeout=30,
                    )
                    self._send_json(200, {
                        "query": q,
                        "stdout": out.stdout,
                        "stderr": out.stderr,
                        "returncode": out.returncode,
                    })
                except FileNotFoundError:
                    self._send_json(503, {"error": "mempalace not on PATH"})
                except subprocess.TimeoutExpired:
                    self._send_json(504, {"error": "mempalace search timed out"})
                return

            if path == "/refresh":
                refresh_cache()
                self._send_json(200, {"refreshed": len(entries_cache)})
                return

            self._send_json(404, {"error": "unknown endpoint"})

        def do_POST(self):  # noqa: N802
            self._send_json(405, {"error": "read-only"})

    with socketserver.TCPServer((host, port), Handler) as httpd:
        print(f"brain serving on http://{host}:{port}")
        print(f"  {len(entries_cache)} pages cached; GET /refresh to reload")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nshutting down")
    return 0


def cmd_cluster(args) -> int:
    """TF-IDF + HDBSCAN over wiki page bodies.

    Surfaces clusters of related pages — especially clusters that span
    multiple teams or repos, which are overlap candidates `/overlap`
    might want to follow up on. This is the at-scale path for Goal 2;
    when the corpus is small (< ~10 pages) it just reports that.
    """
    pages = wiki_pages()
    parsed_pages = []
    for p in pages:
        parsed = parse(p)
        if parsed is None:
            continue
        meta, body = parsed
        parsed_pages.append((p, meta, body))

    n = len(parsed_pages)
    if n < args.min_corpus:
        print(f"corpus too small for clustering: {n} pages "
              f"(need ≥ {args.min_corpus}). Run /overlap pair-wise instead.")
        return 0

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import HDBSCAN
    except ImportError as e:
        print(f"missing dep: {e}. install scikit-learn into the mempalace venv.")
        return 1

    docs = [body for _, _, body in parsed_pages]
    vec = TfidfVectorizer(stop_words="english", max_features=4096,
                          ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(docs).toarray()

    min_cluster = max(2, args.min_cluster)
    hdb = HDBSCAN(min_cluster_size=min_cluster, metric="euclidean", copy=True)
    labels = hdb.fit_predict(X)

    clusters: dict[int, list[int]] = collections.defaultdict(list)
    for idx, lbl in enumerate(labels):
        clusters[int(lbl)].append(idx)

    noise = clusters.pop(-1, [])
    print(f"clustered {n} pages into {len(clusters)} clusters; "
          f"{len(noise)} pages classified as noise (no cluster).")

    overlap_candidates = []
    for lbl, idxs in sorted(clusters.items()):
        page_metas = [parsed_pages[i][1] for i in idxs]
        teams = sorted({m.get("team") for m in page_metas if m.get("team")})
        all_repos = set()
        for m in page_metas:
            for r in m.get("repos") or []:
                all_repos.add(r)
        is_candidate = len(teams) > 1 or len(all_repos) > 1
        marker = "★ overlap candidate" if is_candidate else ""
        print(f"\ncluster {lbl} ({len(idxs)} pages) "
              f"{marker}")
        if teams:
            print(f"  teams: {', '.join(teams)}")
        if all_repos:
            print(f"  repos: {', '.join(sorted(all_repos))}")
        for i in idxs:
            p, meta, _ = parsed_pages[i]
            print(f"  - {p.relative_to(WIKI)}  "
                  f"({meta.get('kind', '?')}, {meta.get('status', '?')})")
        if is_candidate:
            overlap_candidates.append((lbl, idxs))

    if overlap_candidates:
        print(f"\n{len(overlap_candidates)} overlap-candidate cluster(s) "
              f"flagged. Run `/overlap` on each to investigate.")

    return 0


def cmd_promote(args) -> int:
    insight_rel = args.insight
    insight_path = (WIKI / insight_rel).resolve()
    if not insight_path.exists() or WIKI not in insight_path.parents:
        print(f"insight not found under wiki/: {insight_rel}")
        return 1

    parsed = parse(insight_path)
    if parsed is None:
        print(f"unparseable: {insight_path}")
        return 1
    meta, _body = parsed
    if meta.get("kind") != "insight":
        print(f"not a kind: insight page (got kind={meta.get('kind')!r})")
        return 1
    if meta.get("status") == "superseded":
        print(f"already superseded: {insight_path.relative_to(REPO)}")
        return 1

    insight_name = insight_path.name
    insight_slug = insight_path.stem
    initiative_slug = args.slug or f"{insight_slug}-initiative"
    initiative_path = WIKI / f"{initiative_slug}.md"
    if initiative_path.exists():
        print(f"target already exists: {initiative_path.relative_to(REPO)}")
        return 1

    today = today_utc().isoformat()
    title = meta.get("title", insight_slug)

    init_fm: dict = {
        "title": f"{title} — initiative",
        "kind": "initiative",
        "status": "draft",
        "updated": today,
        "confidence": "low",
        "supersedes": insight_name,
    }
    if t := meta.get("team"):
        init_fm["team"] = t
    if d := meta.get("division"):
        init_fm["division"] = d
    if r := meta.get("repos"):
        init_fm["repos"] = r
    init_fm["sources"] = list(meta.get("sources") or [])

    fm_yaml = yaml.safe_dump(init_fm, sort_keys=False).strip()
    body = f"""# {init_fm['title']}

Promoted from [{insight_name}](./{insight_name}). The insight remains
the evidence record; this initiative is what we plan to do about it.

## What
TODO — define the work, derived from the insight's `## Pattern`.

## How
TODO — implementation approach, sequencing, dependencies.

## Why
TODO — extract from the insight's `## Implications`.

## Now
TODO — current state once work begins.

## Perceived
TODO — what the org currently believes about this area.

## Target
TODO — desired end state.
"""
    initiative_path.write_text(f"---\n{fm_yaml}\n---\n\n{body}")

    text = insight_path.read_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        print("could not re-split insight frontmatter; aborting in-place edit")
        return 1
    fm_text = parts[1]
    fm_text = re.sub(r"^status:.*$", "status: superseded", fm_text,
                     count=1, flags=re.MULTILINE)
    if "superseded_by:" not in fm_text:
        fm_text = fm_text.rstrip() + f"\nsuperseded_by: {initiative_slug}.md\n"
    insight_path.write_text(f"---{fm_text}---{parts[2]}")

    print(f"promoted {insight_path.relative_to(REPO)} → "
          f"{initiative_path.relative_to(REPO)}")
    print(f"next: edit {initiative_path.relative_to(REPO)} to fill the TODOs")
    print("then: update wiki/index.md and run `brain.py validate views`")
    return 0


def cmd_personas(args) -> int:
    """Infer the RFC persona pool for a wiki page.

    Reads `wiki/<path>` frontmatter, walks `.claude/personas/{team,
    users,agents}/`, and prints the pool the `rfc` skill would
    consult. Sole purpose: deterministic pool inference visible to
    the operator before the LLM-driven `rfc` skill runs.
    """
    page_rel = args.page
    page_path = (WIKI / page_rel).resolve()
    if not page_path.exists() or WIKI not in page_path.parents:
        print(f"page not found under wiki/: {page_rel}")
        return 1

    parsed = parse(page_path)
    if parsed is None:
        print(f"unparseable frontmatter: {page_rel}")
        return 1
    meta, body = parsed

    personas_dir = REPO / ".claude" / "personas"
    pool: list[tuple[str, str, str]] = []  # (level, slug, frontmatter dict label)
    seen: set[str] = set()

    def add(level: str, slug: str, label: str):
        key = f"{level}/{slug}"
        if key in seen:
            return
        seen.add(key)
        pool.append((level, slug, label))

    # Always: agent personas (PM / Tech Lead / Developer).
    for slug in ("pm-agent", "tech-lead-agent", "developer-agent"):
        if (personas_dir / "agents" / f"{slug}.md").exists():
            add("agents", slug, slug.replace("-", " "))

    # Team personas matching `team:` or relevant to `repos:` /
    # `affects:`.
    page_team = meta.get("team")
    page_repos = set(meta.get("repos") or [])
    page_affects = set(meta.get("affects") or [])
    repo_set = page_repos | page_affects

    team_dir = personas_dir / "team"
    if team_dir.exists():
        for f in sorted(team_dir.glob("*.md")):
            if f.name == "README.md":
                continue
            p_parsed = parse(f)
            if p_parsed is None:
                continue
            p_meta, _ = p_parsed
            persona_team = p_meta.get("team")
            label_name = p_meta.get("name", f.stem)
            label_role = p_meta.get("role", "")
            label = f"{label_name} — {label_role}".strip(" —")
            # Match team directly.
            if page_team and persona_team and page_team == persona_team:
                add("team", f.stem, label)
                continue
            # Platform / Architect / Engineering Manager / VP roles
            # are cross-repo by nature — include if any repo is set.
            cross_repo_roles = (
                "Platform", "Engineering", "Architect", "Autonomous",
            )
            persona_div = p_meta.get("division", "")
            if repo_set and any(
                r in label_role or r in persona_div
                for r in cross_repo_roles
            ):
                add("team", f.stem, label)

    # User personas explicitly named under `## Affected personas`.
    affected_section = ""
    in_section = False
    for line in body.splitlines():
        if re.match(r"^##\s+Affected personas\b", line):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            affected_section += line + "\n"

    if affected_section:
        users_dir = personas_dir / "users"
        if users_dir.exists():
            for f in sorted(users_dir.glob("*.md")):
                if f.name == "README.md":
                    continue
                slug = f.stem
                # Match by slug or by display name in the section.
                if slug in affected_section:
                    p_parsed = parse(f)
                    if p_parsed:
                        p_meta, _ = p_parsed
                        label = (
                            f"{p_meta.get('name', slug)} — "
                            f"{p_meta.get('role', 'user persona')}"
                        )
                    else:
                        label = slug
                    add("users", slug, label)

    # Cap at 6 to keep RFC bounded.
    capped = pool[:6]
    overflow = pool[6:]

    print(f"RFC pool for wiki/{page_rel}:")
    for level, slug, label in capped:
        print(f"  - [{level}] {label}")
    if overflow:
        print(f"  ({len(overflow)} more inferred but capped: "
              f"{', '.join(s for _, s, _ in overflow)})")
    return 0


def cmd_rotate_log(_args) -> int:
    """Rotate `log/log.md` if it exceeds the size threshold.

    Per AGENTS.md § Audit log § Rotation policy:
    - Threshold: 2,000 lines OR ~200 KB.
    - On rotation: move current log/log.md → log/archive/log-<UTC>.md
      and create a fresh log/log.md with a one-line pointer back.
    - Mechanical, no judgement.

    Idempotent: if the threshold isn't reached, returns 0 with a
    "no rotation needed" message.
    """
    log_dir = REPO / "log"
    log_path = log_dir / "log.md"
    if not log_path.exists():
        print("no log/log.md to rotate")
        return 0

    text = log_path.read_text()
    lines = text.splitlines()
    size_bytes = len(text.encode())

    THRESH_LINES = 2000
    THRESH_BYTES = 200 * 1024  # 200 KB

    if len(lines) < THRESH_LINES and size_bytes < THRESH_BYTES:
        print(
            f"no rotation needed: {len(lines)} lines, "
            f"{size_bytes} bytes "
            f"(threshold: {THRESH_LINES} lines / "
            f"{THRESH_BYTES} bytes)"
        )
        return 0

    archive_dir = log_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    today = today_utc().isoformat()
    archive_path = archive_dir / f"log-{today}.md"

    if archive_path.exists():
        print(f"refusing to overwrite existing archive: "
              f"{archive_path.relative_to(REPO)}")
        return 1

    archive_path.write_text(text)
    fresh = (
        "# Log\n\n"
        "Append-only. Newest entries at the bottom. One line per "
        "operation:\n"
        "`YYYY-MM-DD <ingest|query|lint|meta> — <summary>`.\n\n"
        f"Previous: log/archive/log-{today}.md\n"
    )
    log_path.write_text(fresh)

    print(
        f"rotated log/log.md → {archive_path.relative_to(REPO)} "
        f"({len(lines)} lines, {size_bytes} bytes)"
    )
    return 0


def cmd_snapshot(_args) -> int:
    """Write a brain snapshot — corpus shape at a point in time.

    Drops a JSON file under `wiki/_views/snapshots/<UTC-date>.json`
    summarising:
      - per-kind / per-status / per-team / per-repo counts
      - per-page (path → kind, status, confidence, updated, tokens)
      - aggregate token total
      - count of pages flagged stale per `cmd_stats`'s thresholds

    Snapshots compose: diffing two of them shows brain motion over
    time. Cheap to produce; safe to run as part of /sync.
    """
    entries = collect_pages_data()
    snap_dir = WIKI / "_views" / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)

    today = today_utc().isoformat()
    by_kind: dict = collections.Counter()
    by_status: dict = collections.Counter()
    by_team: dict = collections.Counter()
    by_repo: dict = collections.Counter()
    by_conf: dict = collections.Counter()
    total_tokens = 0
    pages_summary = []
    for e in entries:
        by_kind[e.get("kind", "?")] += 1
        by_status[e.get("status", "?")] += 1
        by_team[e.get("team", "(none)")] += 1
        for r in e.get("repos") or []:
            by_repo[r] += 1
        by_conf[e.get("confidence", "(none)")] += 1
        total_tokens += int(e.get("tokens", 0) or 0)
        pages_summary.append({
            "path": e["path"],
            "kind": e.get("kind"),
            "status": e.get("status"),
            "confidence": e.get("confidence"),
            "updated": e.get("updated"),
            "tokens": e.get("tokens"),
        })

    snap = {
        "generated": today,
        "totals": {
            "pages": len(entries),
            "tokens": total_tokens,
        },
        "by_kind": dict(by_kind),
        "by_status": dict(by_status),
        "by_team": dict(by_team),
        "by_repo": dict(by_repo),
        "by_confidence": dict(by_conf),
        "pages": pages_summary,
    }

    out = snap_dir / f"{today}.json"
    out.write_text(json.dumps(snap, indent=2, sort_keys=False))
    print(f"wrote {out.relative_to(REPO)}")
    print(f"  {snap['totals']['pages']} pages, "
          f"{snap['totals']['tokens']} tokens")
    return 0


# Notion write tools that must always be deny-listed in
# .claude/settings.json. The CI guard `check-no-notion-writes`
# enforces both directions: every name here is in `deny`, and
# nothing else under tools/ or .claude/ invokes them.
# Every Notion write tool that must stay denied, on BOTH server prefixes.
# Both, because the deny list is keyed on the full tool name and each tool
# used to be gated on one prefix while open on the other — so the doctrine
# silently depended on which Notion server happened to be connected. That
# gap is how the mirror page could be created and synced on 2026-07-31/08-01
# while settings.json appeared to forbid it. (Closed 2026-08-03.)
_NOTION_WRITE_BASENAMES = (
    "notion-create-pages",
    "notion-create-database",
    "notion-create-comment",
    "notion-create-view",
    "notion-create-attachment",
    "notion-update-page",
    "notion-update-data-source",
    "notion-update-view",
    "notion-duplicate-page",
    "notion-move-pages",
)
_NOTION_SERVERS = ("claude_ai_Notion", "notion")

# The single named exception, per AGENTS.md § Notion is read-only and the
# allow-list at wiki/_state/attention/notion-mirror.json: the attention-board
# mirror page may be rewritten. Tool-level permissions cannot scope to a page
# id, so this tool is *permitted* on the connected server and the page-scoping
# is a convention the agent keeps. The guard below therefore checks that the
# exception is documented and singular rather than pretending it is closed.
NOTION_MIRROR_WRITE_TOOL = "mcp__claude_ai_Notion__notion-update-page"
NOTION_MIRROR_ALLOWLIST = ("wiki", "_state", "attention", "notion-mirror.json")

# Everything above stays denied except the single permitted exception — and
# the exception is one tool on one server, so the same basename on the other
# prefix remains required-denied. Subtracting only the exact exception is the
# point: an earlier version of this fix dropped `notion-update-page` from the
# basename list altogether, which quietly ungated it on both prefixes.
NOTION_WRITE_TOOLS = tuple(
    tool for base in _NOTION_WRITE_BASENAMES for server in _NOTION_SERVERS
    if (tool := f"mcp__{server}__{base}") != NOTION_MIRROR_WRITE_TOOL
)


def cmd_check_no_notion_writes(_args) -> int:
    """Enforce the read-only Notion doctrine.

    Two checks:
    1. Every NOTION_WRITE_TOOLS entry must appear in the `deny` list
       of .claude/settings.json. Drift from this list is forbidden.
    2. No other tracked file (under .claude/, tools/, .github/) may
       *use* a Notion write tool name. Settings + this file (which
       defines the list) + AGENTS.md (which documents it) are the
       only allowed mentions.
    """
    settings_path = REPO / ".claude" / "settings.json"
    if not settings_path.exists():
        print(f"missing: {settings_path.relative_to(REPO)}")
        return 1

    settings = json.loads(settings_path.read_text())
    deny = set(settings.get("permissions", {}).get("deny", []))
    missing = [t for t in NOTION_WRITE_TOOLS if t not in deny]
    if missing:
        print("ERROR  Notion write tools missing from "
              ".claude/settings.json deny list:")
        for t in missing:
            print(f"  - {t}")
        return 1

    # The mirror exception: permitted, so it cannot be checked by absence.
    # What is checkable is that the exception stays *documented and
    # singular* — an allow-list naming exactly one page id. Without that,
    # a permitted update-page is an unbounded write capability with no
    # record of what it is for.
    allowlist = REPO.joinpath(*NOTION_MIRROR_ALLOWLIST)
    if NOTION_MIRROR_WRITE_TOOL not in deny:
        if not allowlist.exists():
            print(f"ERROR  {NOTION_MIRROR_WRITE_TOOL} is permitted but "
                  f"{allowlist.relative_to(REPO)} is missing — a page-write "
                  "capability with no recorded scope.")
            return 1
        try:
            mirror = json.loads(allowlist.read_text())
        except json.JSONDecodeError as exc:
            print(f"ERROR  {allowlist.relative_to(REPO)} is not valid JSON: {exc}")
            return 1
        page_id = mirror.get("page_id")
        if not page_id:
            print(f"ERROR  {allowlist.relative_to(REPO)} names no page_id — "
                  "the mirror exception must name exactly one page.")
            return 1
        extra = [k for k in ("page_ids", "pages") if k in mirror]
        if extra:
            print(f"ERROR  {allowlist.relative_to(REPO)} carries {extra} — "
                  "the exception is one page, not a list.")
            return 1
        print(f"OK  Notion mirror exception scoped to a single page "
              f"({page_id[:8]}…); every other write tool denied on both "
              f"server prefixes")

    # Allowed mentions: the deny list itself, this enforcement code,
    # and the AGENTS.md doctrine + the seeded ADR.
    allowed_mentions = {
        ".claude/settings.json",
        "tools/brain.py",
        "AGENTS.md",
        "wiki/brain/adrs/notion-is-read-only.md",
    }

    rogue: list[tuple[str, int, str]] = []
    scan_roots = [".claude", "tools", ".github"]
    # Skip transient agent harness state and tool caches.
    skip_dir_names = {
        "__pycache__", "node_modules", ".cache",
        "worktrees",  # .claude/worktrees/ is the subagent harness's workspace
    }
    skip_suffixes = {".pyc", ".pyo"}
    for root in scan_roots:
        root_path = REPO / root
        if not root_path.exists():
            continue
        for p in root_path.rglob("*"):
            if not p.is_file():
                continue
            # Use the path relative to REPO for the skip check, not
            # the absolute path. Otherwise running this inside a
            # worktree (where REPO itself sits under .claude/worktrees/)
            # would skip every file the absolute path traverses through.
            rel_path = p.relative_to(REPO)
            if any(part in skip_dir_names for part in rel_path.parts):
                continue
            if p.suffix in skip_suffixes:
                continue
            rel = str(rel_path)
            if rel in allowed_mentions:
                continue
            try:
                text = p.read_text(errors="ignore")
            except Exception:
                continue
            for tool in NOTION_WRITE_TOOLS:
                for ln, line in enumerate(text.splitlines(), 1):
                    if tool in line:
                        rogue.append((rel, ln, tool))

    if rogue:
        print("ERROR  Notion write tool names found outside the deny "
              "list / doctrine:")
        for rel, ln, tool in rogue:
            print(f"  {rel}:{ln}: {tool}")
        return 1

    print(f"OK  Notion read-only enforcement intact: "
          f"{len(NOTION_WRITE_TOOLS)} write tools deny-listed")
    return 0


def cmd_check_home_fresh(args) -> int:
    """Verify any wiki/ change on this branch is paired with a wiki/index.md change.

    The brain UI's home page (wiki/index.md) is an agent-maintained
    dashboard. Per wiki/brain/adrs/home-content-shape.md, every
    wiki/ edit must update the relevant home-page section in the
    same PR. The local Stop hook (tools/home-staleness.sh) catches
    accidents during a session; this command is the load-bearing
    CI guard that catches whatever the hook missed.

    Triggering paths: wiki/** except wiki/_views/**, wiki/_archive/**,
    and wiki/index.md itself. Modified or added.
    """
    base = getattr(args, "base", "origin/main") or "origin/main"
    diff_cmd = ["git", "diff", "--name-only", f"{base}...HEAD"]
    try:
        diff = subprocess.check_output(diff_cmd, text=True,
                                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # If the base ref doesn't exist (fresh clone, force-pushed
        # main, etc.), be loud — better to fail CI visibly than to
        # silently let a bypass through.
        print(f"ERR: git diff failed against {base}: {e.stderr}", file=sys.stderr)
        return 1

    files = [line for line in diff.splitlines() if line]
    triggers: list[str] = []
    home_touched = False
    for f in files:
        if f == "wiki/index.md":
            home_touched = True
            continue
        if f.startswith("wiki/_views/"):
            continue
        if f.startswith("wiki/_archive/"):
            continue
        # Machine state (the inbox queue, sync cursors, promotion
        # records), not reader-facing content; a queue line must not
        # require a home-page entry. Also, in a pi-brain-nested checkout
        # the root brain's wiki/ changes surface here under the same
        # relative names, and the root inbox is not this brain's content.
        if f.startswith("wiki/_state/"):
            continue
        if f.startswith("wiki/"):
            triggers.append(f)

    if triggers and not home_touched:
        print("ERROR  this branch modifies wiki/ content but does not "
              "update wiki/index.md (the home page).", file=sys.stderr)
        print("Triggering files:", file=sys.stderr)
        for t in triggers:
            print(f"  - {t}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Per wiki/brain/adrs/home-content-shape.md, every wiki/ "
              "edit must update the relevant section on wiki/index.md.",
              file=sys.stderr)
        return 1

    if triggers and not _home_rendered_changed(base):
        print("ERROR  wiki/index.md changed, but nothing a reader can "
              "see changed.", file=sys.stderr)
        print("", file=sys.stderr)
        print("The home page's rendered text (HTML comments stripped) is "
              "identical to the base. An entry written as an HTML comment "
              "satisfies the file-touched check while rendering to nobody "
              "— between 2026-05-18 and 2026-07-31, 300+ consecutive "
              "entries went in that way and the home page showed May for "
              "two and a half months.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Write the entry as visible prose in the relevant section.",
              file=sys.stderr)
        return 1

    if triggers:
        print(f"OK  home page rendered content changed alongside "
              f"{len(triggers)} wiki/ change(s).")
    else:
        print("OK  no wiki/ changes that require a home-page update.")
    return 0


def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def _home_rendered_changed(base: str) -> bool:
    """True if wiki/index.md's *rendered* text differs from the base.

    The file-touched check above is satisfied by any byte change,
    including an HTML comment that renders to nobody. This compares
    what a reader actually sees, so a comment-only edit fails the
    gate. Per wiki/brain/adrs/home-content-shape.md; added 2026-07-31
    after the comment-only drift was found.

    Errs open (returns True) when the base blob can't be read — a
    fresh clone or a first-commit home page shouldn't fail CI on an
    unreadable comparison point.
    """
    try:
        before = subprocess.check_output(
            ["git", "show", f"{base}:wiki/index.md"],
            text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return True
    try:
        after = (WIKI / "index.md").read_text()
    except OSError:
        return True
    return _strip_html_comments(before).split() != \
        _strip_html_comments(after).split()


README_TRIGGER_ALWAYS = {
    "AGENTS.md",
    "tools/brain.py",
    ".claude/settings.json",
}


def _is_readme_trigger(path: str, status: str) -> bool:
    """Return True iff a path+git-status pair counts as a README-staleness trigger.

    Trigger paths (any one suffices) on add or modify:
        - AGENTS.md (schema / governance change)
        - tools/brain.py (validator / view emit / scope rules)
        - tools/templates/** (ADR / PRD template structure)
        - .claude/settings.json (hooks, permissions, slash commands)
        - .claude/skills/** (skill protocol changes)
        - ui/astro.config.mjs / ui/serve.mjs / ui/Dockerfile
          (UI substrate)

    Note: earlier shapes triggered on `wiki/<scope>/ai-suggestions/**`
    and `wiki/_views/*.md` adds, intending to catch "new shelf
    appearing." That heuristic was too broad — every new draft
    fired the check, even within an existing shelf, which doesn't
    affect README content. Removed in favour of the always-trigger
    set; "new shelf" cases will be caught indirectly when AGENTS.md
    or `tools/brain.py` is updated to introduce them.
    """
    if path in README_TRIGGER_ALWAYS:
        return status in {"A", "M"}
    if path.startswith("tools/templates/"):
        return status in {"A", "M"}
    if path.startswith(".claude/skills/"):
        return status in {"A", "M"}
    if path in {"ui/astro.config.mjs", "ui/serve.mjs", "ui/Dockerfile"}:
        return status in {"A", "M"}
    return False


def cmd_check_readme_fresh(args) -> int:
    """CI gate: verify significant changes on this branch are paired with a README.md edit.

    Mirrors check-home-fresh's shape but for README.md instead of
    wiki/index.md. The trigger set is governance/tooling/schema-
    affecting changes (per tools/readme-staleness.sh and AGENTS.md
    governance discussions). README freshness is enforced at PR
    time as a hard gate; in-session reminders are not used (see
    user direction 2026-05-03 question #9).

    Trigger paths: see _is_readme_trigger above.
    """
    base = getattr(args, "base", "origin/main") or "origin/main"
    diff_cmd = ["git", "diff", "--name-status", f"{base}...HEAD"]
    try:
        diff = subprocess.check_output(diff_cmd, text=True,
                                       stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"ERR: git diff failed against {base}: {e.stderr}", file=sys.stderr)
        return 1

    triggers: list[str] = []
    readme_touched = False
    for line in diff.splitlines():
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0][0]  # First char (handles R100 etc.)
        path = parts[-1]      # Last entry (handles renames -> dest)
        # The pi-brain conversion nested this brain under files/; a README
        # edit shows as README.md from the brain home or files/README.md
        # from the repository root.
        if path in ("README.md", "files/README.md"):
            readme_touched = True
            continue
        if _is_readme_trigger(path, status):
            triggers.append(f"{status} {path}")

    if triggers and not readme_touched:
        print("ERROR  this branch has significant changes but does not "
              "update README.md.", file=sys.stderr)
        print("Triggering files:", file=sys.stderr)
        for t in triggers:
            print(f"  - {t}", file=sys.stderr)
        print("", file=sys.stderr)
        print("Per the readme-staleness convention (tools/readme-"
              "staleness.sh § Significant-change patterns), changes "
              "to schema / governance / tooling / templates / hooks / "
              "skills / UI substrate / new ai-suggestions shelves / "
              "new auto-generated views must be reflected in README.md.",
              file=sys.stderr)
        print("", file=sys.stderr)
        print("Either:", file=sys.stderr)
        print("  - Edit README.md to reflect the change (recommended), or",
              file=sys.stderr)
        print("  - Make a no-op edit to README.md (e.g. clarify a sentence) "
              "to acknowledge that README.md was reviewed and no "
              "substantive change is needed.", file=sys.stderr)
        return 1

    if triggers:
        print(f"OK  README.md touched alongside {len(triggers)} "
              f"significant change(s).")
    else:
        print("OK  no significant changes that require a README update.")
    return 0


def _missing_sibling_msg(repo_path: Path) -> str:
    """Single source of truth for the 'sibling repo missing' message.

    Bakes in the $BRAIN_PROJECTS_ROOT hint so any operator hitting the
    error sees the override knob inline. Per
    wiki/brain/adrs/configurable-projects-dir.md.
    """
    return (
        f"sibling repo not found at {repo_path} — set "
        f"$BRAIN_PROJECTS_ROOT (currently "
        f"{'set to ' + str(PROJECTS) if 'BRAIN_PROJECTS_ROOT' in os.environ else 'unset; default ' + str(PROJECTS)})"
        " or create the directory"
    )


def _sibling_repo(repo_name: str) -> Path:
    """Resolve a sibling-repo name to its filesystem path."""
    p = PROJECTS / repo_name
    if not p.exists():
        raise SystemExit(_missing_sibling_msg(p))
    if not (p / ".git").exists():
        raise SystemExit(f"{p} is not a git repository")
    return p


def _git(args: list[str], cwd: Path) -> str:
    return subprocess.check_output(
        ["git"] + args, cwd=cwd, text=True
    ).strip()


def _https_of_remote(remote: str) -> str | None:
    m = (re.fullmatch(r"[\w.-]+@([\w.-]+):(.+?)(?:\.git)?/?", remote)
         or re.fullmatch(r"(?:ssh|git|https?)://(?:[^@/]+@)?([\w.-]+)(?::\d+)?/(.+?)(?:\.git)?/?", remote))
    return f"https://{m.group(1)}/{m.group(2)}" if m else None


def _origin_https(repo: Path | None = None) -> str | None:
    """This checkout's own repository as an https URL, read from its origin
    remote rather than written down: the brain changed repositories on
    2026-09-14 and every written copy of the old path kept pointing at the
    retired one. None with no git or no origin."""
    try:
        remote = _git(["remote", "get-url", "origin"], repo or REPO)
    except (OSError, subprocess.CalledProcessError):
        return None
    return _https_of_remote(remote)


def _read_cursors() -> dict:
    if not SYNC_CURSORS.exists():
        return {"version": 1, "generated": today_utc().isoformat(), "cursors": {}}
    return json.loads(SYNC_CURSORS.read_text())


def _write_cursors(data: dict) -> None:
    SYNC_CURSORS.parent.mkdir(exist_ok=True)
    data["generated"] = today_utc().isoformat()
    SYNC_CURSORS.write_text(json.dumps(data, indent=2) + "\n")


def cmd_sync_cursor(args) -> int:
    """Manage per-sibling-repo sync cursors at wiki/_state/sync-cursors.json.

    Subcommands (via the `op` argument):
      get [<repo>]   — print the cursor for one repo, or all if omitted.
      set <repo>     — advance the cursor to the sibling repo's current
                       HEAD. Requires the sibling to be on its main branch
                       with a clean tree (per AGENTS.md § Sibling-repo
                       handling). Refuses if either rule is violated.
      diff <repo>    — list paths changed in the sibling repo since the
                       cursor's SHA. Output is one path per line, suitable
                       for piping into `git ls-files | grep -F -f -`.

    The cursor is the brain's record of "what was the last sibling-repo
    state we ingested?" — wiki-ingest skill protocol consults it before
    walking a sibling tree, so subsequent passes only process changed
    files instead of re-walking everything.
    """
    op = args.op
    data = _read_cursors()
    cursors = data.setdefault("cursors", {})

    if op == "get":
        if args.repo:
            entry = cursors.get(args.repo)
            if not entry:
                print(f"no cursor for {args.repo}", file=sys.stderr)
                return 1
            print(json.dumps(entry, indent=2))
        else:
            print(json.dumps(cursors, indent=2))
        return 0

    if op == "set":
        repo_path = _sibling_repo(args.repo)
        branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
        if branch not in ("main", "master"):
            print(
                f"refusing to set cursor for {args.repo}: branch={branch!r} "
                "(sibling-repo handling rule requires main/master); use "
                "--force to override",
                file=sys.stderr,
            )
            if not getattr(args, "force", False):
                return 1
        dirty = subprocess.run(
            ["git", "diff", "--quiet"], cwd=repo_path
        ).returncode != 0 or subprocess.run(
            ["git", "diff", "--cached", "--quiet"], cwd=repo_path
        ).returncode != 0
        if dirty and not getattr(args, "force", False):
            print(
                f"refusing to set cursor for {args.repo}: working tree "
                "is dirty; commit/stash or pass --force",
                file=sys.stderr,
            )
            return 1
        sha = _git(["rev-parse", "HEAD"], repo_path)
        cursors[args.repo] = {
            "sha": sha,
            "branch": branch,
            "synced_at": dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "tree_state": "dirty" if dirty else "clean",
            "scope": args.scope or "full-tree",
            "synced_by": args.synced_by or "(unspecified)",
        }
        _write_cursors(data)
        print(f"OK  {args.repo} cursor → {sha[:8]} (branch={branch})")
        return 0

    if op == "diff":
        repo_path = _sibling_repo(args.repo)
        entry = cursors.get(args.repo)
        if not entry:
            # No cursor — fall back to "everything", which we represent
            # as printing all tracked files. Caller decides what to do.
            paths = _git(["ls-files"], repo_path).splitlines()
            print(
                f"# no cursor for {args.repo} — first-pass ingest "
                f"({len(paths)} tracked files)",
                file=sys.stderr,
            )
            for p in paths:
                print(p)
            return 0
        cursor_sha = entry["sha"]
        # If the cursor SHA isn't reachable (rebase / force-push), fall
        # back to a full re-ingest with a loud warning.
        try:
            _git(["cat-file", "-e", cursor_sha], repo_path)
        except subprocess.CalledProcessError:
            print(
                f"WARN: cursor {cursor_sha[:8]} for {args.repo} not "
                "reachable in sibling repo (rebased? force-pushed?). "
                "Falling back to full-tree listing.",
                file=sys.stderr,
            )
            for p in _git(["ls-files"], repo_path).splitlines():
                print(p)
            return 0
        head_sha = _git(["rev-parse", "HEAD"], repo_path)
        if cursor_sha == head_sha:
            print(f"# {args.repo} is at cursor (no changes since "
                  f"{cursor_sha[:8]})", file=sys.stderr)
            return 0
        diff = _git(
            ["diff", "--name-only", f"{cursor_sha}..HEAD"], repo_path
        )
        for p in diff.splitlines():
            if p:
                print(p)
        return 0

    print(f"unknown sync-cursor op: {op!r}", file=sys.stderr)
    return 1


def _enola_bin() -> str | None:
    """The enola binary, resolved config-first: mcp-arch.yaml may name a
    `binary:` (a wrapper-owned key the engine ignores), so a guinea-pig
    checkout can run a dev build while every other checkout keeps the pin —
    the same per-checkout pattern as output.dir. PATH and the pinned install
    location are the fallbacks.
    """
    try:
        import yaml as _yaml
        cfg = _yaml.safe_load(ENOLA_CONFIG.read_text())
        declared = (cfg or {}).get("binary")
        if declared:
            p = Path(declared).expanduser()
            if p.exists():
                return str(p)
    except Exception:
        pass
    found = shutil.which("enola")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "enola"
    return str(fallback) if fallback.exists() else None


def _enola_env() -> dict:
    """The environment every enola call runs under: the caller's, minus the
    gem variables a login shell leaks, with the Ruby the Prism provider names
    leading PATH. Rubydex lists the bundle through `bundle` on PATH and Prism
    runs under the interpreter the config names; under RVM's GEM_PATH the
    first fails to read and the second fails its probe, and each degrades to
    a named skip that reads as "fewer facts" rather than as an error.

    ENOLA_NO_UPDATE_CHECK is set here and nowhere else in this file: every
    subcommand and --generate otherwise spawns a detached release check when
    enola's 12-hour cache is due, and a four-segment channel version is not
    one upstream suppresses (wiki/tabula/adrs/brain-tooling-follow-ups.tabula).
    """
    env = {k: v for k, v in os.environ.items() if k not in ("GEM_HOME", "GEM_PATH")}
    env["ENOLA_NO_UPDATE_CHECK"] = "1"
    interpreter = None
    try:
        import yaml as _yaml
        cfg = _yaml.safe_load(ENOLA_CONFIG.read_text()) or {}
        for provider in cfg.get("providers") or []:
            command = provider.get("command") or []
            if command and "ruby" in Path(command[0]).name:
                interpreter = Path(command[0]).expanduser()
                break
    except Exception:
        interpreter = None
    if interpreter is not None and interpreter.parent.is_dir():
        env["PATH"] = f"{interpreter.parent}{os.pathsep}{env.get('PATH', '')}"
    return env


MEMBER_CONFIG_MARKER = "# generated by brain.py enola generate"


def write_member_configs(repo_paths) -> list:
    """Give every cluster member the brain's provider and ignore settings as
    its own mcp-arch.yaml, so the per-repository session hooks grade under
    the same settings the cluster does.

    The hook resolves its config as the repository's own mcp-arch.yaml or
    built-in defaults, never a config kept elsewhere; without this file a
    hook snapshots with no providers and no ignore globs and declines every
    grade as incomparable. The file carries a marker and is rewritten on
    every generate; a config the repository tracks itself is left alone.
    Excluded from git per clone like the artifact directories.
    """
    try:
        import yaml as _yaml
        cfg = _yaml.safe_load(ENOLA_CONFIG.read_text()) or {}
    except Exception:
        return []
    providers = []
    for provider in cfg.get("providers") or []:
        entry = dict(provider)
        command = list(entry.get("command") or [])
        if command:
            entry["command"] = [str((ENOLA_CONFIG.parent / c).resolve()) if c.startswith(".")
                                else c for c in command]
        providers.append(entry)
    body = {"repo": ".", "repos": ["."]}
    if cfg.get("ignore"):
        body["ignore"] = list(cfg["ignore"])
    if providers:
        body["providers"] = providers
    rendered = (MEMBER_CONFIG_MARKER + "\n# The brain's provider and ignore settings for this "
                "repository's own session hooks.\n# Rewritten on every generate; "
                "not tracked here.\n" + _yaml.safe_dump(body, sort_keys=False))
    written = []
    for path in repo_paths:
        target = Path(path) / "mcp-arch.yaml"
        if not (Path(path) / ".git").exists():
            continue
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", "mcp-arch.yaml"],
                                 cwd=str(path), capture_output=True, text=True)
        if tracked.returncode == 0:
            continue
        if target.exists() and MEMBER_CONFIG_MARKER not in target.read_text():
            continue
        if not target.exists() or target.read_text() != rendered:
            target.write_text(rendered)
            written.append(str(target))
    return written


def _enola_repos() -> list[Path]:
    """Repo paths from mcp-arch.yaml's `repos:` block (config-relative)."""
    if not ENOLA_CONFIG.exists():
        return []
    paths = []
    in_repos = False
    for line in ENOLA_CONFIG.read_text().splitlines():
        if line.startswith("repos:"):
            in_repos = True
            continue
        if in_repos:
            m = re.match(r"\s+-\s+(\S+)", line)
            if m:
                paths.append(Path(os.path.normpath(ENOLA_CONFIG.parent / m.group(1))))
            elif line.strip() and not line.startswith(" "):
                break
    return paths


def _enola_live_receipt(repo_path: Path) -> dict | None:
    receipt = repo_path / _enola_artifact_dir() / "receipt.json"
    if not receipt.exists():
        return None
    try:
        return json.loads(receipt.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _enola_entry(receipt: dict) -> dict:
    git = receipt.get("git", {})
    quality = receipt.get("quality", {})
    return {
        "snapshot_id": receipt.get("snapshot_id"),
        "enola_version": receipt.get("enola_version"),
        "generated_at": receipt.get("generated_at"),
        "git_ref": git.get("ref"),
        "git_commit": git.get("commit"),
        "git_dirty": git.get("dirty"),
        "fact_count": receipt.get("fact_count"),
        "insight_count": receipt.get("insight_count"),
        "duration": receipt.get("duration"),
        "files_parsed": quality.get("files_parsed"),
        "parse_errors": quality.get("parse_errors"),
    }


INTENT_VIA_KINDS = {
    "http", "http-client", "grpc", "graphql", "kafka", "import",
    "shared_symbols", "object-storage",
}

INTENT_FENCE_BEGIN = "# BEGIN compiled-intent (generated by `brain.py intent compile` from wiki declares: frontmatter — edits here are overwritten)"
INTENT_FENCE_END = "# END compiled-intent"


PAGE_RELATION_KEYS = (
    ("depends_on", "depends-on"),
    ("supersedes", "supersedes"),
    ("superseded_by", "superseded-by"),
)

PAGE_ORIGIN_CHANNELS = {
    "slack", "langfuse", "notion", "github", "web", "repo", "other",
}

CORRELATING_KINDS = ("overlap", "insight")


def _classify_source_channel(source: str) -> str:
    """Map one sources: entry to its enola origin channel — keyed on the
    sources/ path prefixes the ingest conventions enforce, unknown → other,
    never a guess. The sole judgment call is conversations/: a snapshot is
    slack only when its filename says so.
    """
    s = str(source)
    name = s.rsplit("/", 1)[-1]
    if "sources/langfuse/" in s:
        return "langfuse"
    if "sources/notion/" in s or "notion.so" in s:
        return "notion"
    if "sources/github/" in s:
        return "github"
    if "sources/web/" in s:
        return "web"
    if "sources/conversations/" in s:
        return "slack" if "slack" in name else "other"
    if "sources/" in s:
        return "other"
    if s.startswith("http"):
        return "web"
    return "repo"


def _derive_page_block(rel: Path, meta: dict) -> tuple[dict | None, list[str]]:
    """Derive a page's engine block (the `page:` half cardo reads under
    enola_intent in the export mirror) from its frontmatter: the deterministic
    mapping `export` writes and the export-current detector re-derives.
    kind becomes type, repos becomes scope, and the relation fields become
    typed edges named by repo-relative path.
    """
    errors: list[str] = []
    kind = meta.get("kind")
    if not kind:
        errors.append(f"{rel}: no kind: — a page cannot compile without one")
        return None, errors
    block: dict = {"type": str(kind)}
    if meta.get("status"):
        block["status"] = str(meta["status"])
    if meta.get("repos"):
        block["scope"] = [str(r) for r in meta["repos"]]
    if meta.get("affects"):
        block["affects"] = [str(a) for a in meta["affects"]]
    sources = [str(s) for s in (meta.get("sources") or [])]
    if sources:
        block["origin"] = sorted({_classify_source_channel(s) for s in sources})
    relations: list[dict] = []
    if meta.get("parent_epic"):
        relations.append({"rel": "part-of",
                          "to": f"wiki/{rel.parts[0]}/epics/{meta['parent_epic']}.md"})
    # parent: <page>#<part> names the part a child architecture page refines;
    # tabula's stamp derives the same relation, the fragment dropped.
    if meta.get("parent") and str(meta["parent"]).strip():
        page = str(meta["parent"]).strip().split("#", 1)[0]
        to = page if page.startswith("wiki/") else f"wiki/{page}"
        if not (REPO / to).exists():
            errors.append(f"{rel}: parent target {to} does not exist")
        relations.append({"rel": "part-of", "to": to})
    for key, rel_name in PAGE_RELATION_KEYS:
        vals = meta.get(key) or []
        if isinstance(vals, str):
            vals = [vals]
        for v in vals:
            v = str(v)
            to = v if v.startswith("wiki/") else f"wiki/{v}"
            if not (REPO / to).exists():
                errors.append(f"{rel}: {key} target {to} does not exist")
            relations.append({"rel": rel_name, "to": to})
    if str(kind) in CORRELATING_KINDS:
        seen = {(r["rel"], r["to"]) for r in relations}
        page_dir = Path("wiki") / rel.parent
        for s in sources:
            if not s.endswith(PAGE_SUFFIXES) or s.startswith("~") or \
                    s.startswith("http") or "sources/" in s:
                continue
            to = os.path.normpath(page_dir / s).replace(os.sep, "/")
            if not to.startswith("wiki/") or not (REPO / to).exists():
                continue
            if ("relates-to", to) in seen:
                continue
            seen.add(("relates-to", to))
            relations.append({"rel": "relates-to", "to": to})
    if relations:
        block["relations"] = relations
    anchors: list[dict] = []
    seen_anchor: set = set()
    for s in sources:
        if not s.startswith("~/projects/"):
            continue
        rest = s[len("~/projects/"):]
        if " " in rest or "(" in rest:
            continue
        repo_name, _, anchor_path = rest.partition("/")
        # The first segment is the repository only when the projects root IS
        # `~/projects`. Under a nested root (`~/projects/<group>`) the first
        # segment names the group, not a repository, and every such anchor
        # dangles because no repository of that name is in any cluster.
        #
        anchor_path = anchor_path.rstrip("/")
        if not repo_name or not anchor_path or (repo_name, anchor_path) in seen_anchor:
            continue
        seen_anchor.add((repo_name, anchor_path))
        anchors.append({"repo": repo_name, "path": anchor_path})
    # governs: is written only by tabula's intent stamp, from a page's
    # ***intent*** sentences and an architecture page's parts, as
    # <repo>/<path>; both derivations read it as anchors so they agree.
    governs = meta.get("governs") or []
    if isinstance(governs, str):
        governs = [governs]
    for g in governs:
        repo_name, _, anchor_path = str(g).partition("/")
        anchor_path = anchor_path.rstrip("/")
        if not repo_name or not anchor_path or (repo_name, anchor_path) in seen_anchor:
            continue
        seen_anchor.add((repo_name, anchor_path))
        anchors.append({"repo": repo_name, "path": anchor_path})
    if anchors:
        block["anchors"] = sorted(anchors, key=lambda a: (a["repo"], a["path"]))
    return block, errors


INTENT_KEY = "intent"
OLD_INTENT_KEY = "enola_intent"
INTENT_HALVES = ("consumes", "layers", "claims")
EXPORT_COMPILED_HEADER = "# Compiled by `tabula "


def _intent_halves(meta: dict) -> tuple[dict, str | None]:
    """The hand-written halves a page holds (consumes, layers, claims), read
    from `intent:` first and from the old `enola_intent:` key during the
    transition, in the engine's order. A half held under both keys with
    different content is refused with the half named, never merged; the
    same half under both is read once. tabula's `intent::halves` twin.
    """
    def held(under: str, key: str):
        block = meta.get(under)
        if not isinstance(block, dict):
            return None
        v = block.get(key)
        return v if v not in (None, "", [], {}) else None
    new_block = meta.get(INTENT_KEY)
    if new_block is not None and not isinstance(new_block, dict):
        return {}, (f"{INTENT_KEY}: is not a mapping, so its consumes, layers "
                    "and claims cannot be read")
    out: dict = {}
    for key in INTENT_HALVES:
        a, b = held(INTENT_KEY, key), held(OLD_INTENT_KEY, key)
        if a is not None and b is not None and a != b:
            return {}, (f"{key} is held under both {INTENT_KEY}: and "
                        f"{OLD_INTENT_KEY}: with different content; keep one "
                        f"under {INTENT_KEY}:")
        v = a if a is not None else b
        if v is not None:
            out[key] = v
    return out, None


@functools.lru_cache(maxsize=1)
def _tabula_bin() -> str | None:
    """The tabula binary that authors pages and writes the export: $TABULA_BIN,
    else `tabula` on PATH, and only one that knows `export`. An older tabula
    still writes the derived enola_intent block into pages, so it is treated
    as absent rather than allowed to undo the cutover.
    """
    cand = os.environ.get("TABULA_BIN") or shutil.which("tabula")
    if not cand or not os.access(cand, os.X_OK):
        return None
    try:
        probe = subprocess.run([cand, "export", "--help"], capture_output=True,
                               text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return cand if probe.returncode == 0 else None


def _tabula_skip(what: str) -> str:
    return (f"{what}: not asked: no tabula that knows `export` (set TABULA_BIN "
            "or put a current tabula on PATH)")


def _run_tabula(args: list[str], quiet: bool = False) -> int:
    binary = _tabula_bin()
    if binary is None:
        return -1
    out = subprocess.run([binary, "--root", str(REPO), *args],
                         capture_output=True, text=True)
    if not quiet:
        sys.stdout.write(out.stdout)
    sys.stderr.write(out.stderr)
    return out.returncode


def _export_label() -> str:
    """The brain's label as the engine names a member: the origin remote's
    repository name when the brain is its repository's root, else the
    directory's name. tabula's `export::label_of` twin."""
    root = REPO.resolve()
    def git(*a):
        r = subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    top = git("rev-parse", "--show-toplevel")
    if top and Path(top).resolve() == root:
        url = git("remote", "get-url", "origin")
        if url:
            name = re.split(r"[/:]", url.rstrip("/").removesuffix(".git"))[-1]
            if name:
                return name
    return root.name or "brain"


def _export_mirror_dir() -> Path:
    return REPO / ".tabula" / "export" / f"{_export_label()}-pages"


def _export_plan() -> tuple[dict, list[str], str | None]:
    """What `brain.py export` writes, computed without touching disk:
    ({path: bytes}, notes, refusal). The mirror holds, per page, a
    frontmatter-only file at its repository-relative path with the derived
    page block and the hand-written halves under the engine's key; laws/*.yaml
    are copied into enola/constraints/ under tabula's header. Architecture
    pages' laws compile only in tabula, and are named rather than written.
    """
    mirror = _export_mirror_dir()
    files: dict = {}
    notes: list[str] = []
    for page in wiki_files():
        rel = page.relative_to(WIKI)
        if rel.parts[0] in ("_views", "_archive"):
            continue
        parsed = parse(page)
        if not parsed:
            continue
        meta, _ = parsed
        block, _errors = _derive_page_block(rel, meta)
        if block is None:
            continue
        halves, refused = _intent_halves(meta)
        if refused:
            return {}, notes, f"wiki/{rel}: {refused}"
        doc = {OLD_INTENT_KEY: {"page": block, **halves}}
        body = yaml.safe_dump(doc, sort_keys=False, default_flow_style=False,
                              width=1000, allow_unicode=True)
        files[mirror / "wiki" / rel] = f"---\n{body}---\n".encode()
    laws = REPO / "laws"
    own = REPO / "enola" / "constraints"
    if laws.is_dir():
        for law in sorted(p for p in laws.iterdir()
                          if p.is_file() and p.suffix in (".yaml", ".yml")):
            header = (f"{EXPORT_COMPILED_HEADER}export` from `laws/{law.name}`; "
                      "edit that file, not this one.\n")
            files[own / f"{law.stem}.yaml"] = header.encode() + law.read_bytes()
    return files, notes, None


def _export_stale(files: dict) -> list[Path]:
    mirror = _export_mirror_dir()
    stale = [p for p in mirror.rglob("*") if p.is_file() and p not in files] \
        if mirror.is_dir() else []
    own = REPO / "enola" / "constraints"
    if own.is_dir():
        for p in own.iterdir():
            if p.is_file() and p not in files:
                first = (p.read_text(errors="ignore").splitlines() or [""])[0]
                if first.startswith(EXPORT_COMPILED_HEADER) and "export` from `laws/" in first:
                    stale.append(p)
    return sorted(stale)


def cmd_export(args) -> int:
    """`brain.py export`: write what the engine reads from what the brain
    authors. Delegates to `tabula export` when a current tabula is present
    (it alone compiles architecture pages' laws); otherwise, or with
    --python, writes the twin: the page mirror and the laws/ copies.
    """
    check = getattr(args, "check", False)
    if not getattr(args, "python", False) and _tabula_bin() is not None:
        return _run_tabula(["export", *(["--check"] if check else [])])
    if not getattr(args, "python", False):
        print("export: " + _tabula_skip("tabula export") + "; writing brain.py's "
              "twin (page mirror and laws/ copies; architecture pages' laws not "
              "compiled)", file=sys.stderr)
    files, _notes, refused = _export_plan()
    if refused:
        print(f"export: refused: {refused}; nothing was written", file=sys.stderr)
        return 2
    stale = _export_stale(files)
    rel = lambda p: os.path.relpath(p, REPO)
    if check:
        for p, b in files.items():
            if not p.exists() or p.read_bytes() != b:
                print(f"export: stale: {rel(p)}", file=sys.stderr)
                return 1
        if stale:
            print(f"export: stale: {rel(stale[0])}", file=sys.stderr)
            return 1
        print(f"export: current ({len(files)} file(s))")
        return 0
    wrote = unchanged = 0
    for p, b in files.items():
        if p.exists() and p.read_bytes() == b:
            unchanged += 1
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
        wrote += 1
    for p in stale:
        p.unlink()
    mirror = _export_mirror_dir()
    if mirror.is_dir():
        for d in sorted((d for d in mirror.rglob("*") if d.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
    print(f"export: wrote {wrote}, removed {len(stale)}, unchanged {unchanged} "
          f"file(s) under {rel(mirror)} and enola/constraints/")
    return 0


def _wiki_declares() -> tuple[dict, list[str]]:
    """Aggregate every wiki page's declares: frontmatter into the corpus
    model. Returns ({repo: {"consumes": [...], "layers": [...]}}, errors);
    a seam declared on two pages is an error, never a merge — one seam, one
    deciding page.
    """
    corpus: dict = {}
    errors: list[str] = []
    seen_seam: dict = {}
    seen_layers: dict = {}
    for page in wiki_files():
        rel = page.relative_to(WIKI)
        if rel.parts[0] in ("_views", "_archive"):
            continue
        parsed = parse(page)
        if not parsed:
            continue
        meta, _ = parsed
        dec, refused = _intent_halves(meta)
        if refused:
            errors.append(f"{rel}: {refused}")
            continue
        for c in dec.get("consumes") or []:
            repo, target, via = c.get("repo"), c.get("target"), c.get("via")
            if not (repo and target and via):
                errors.append(f"{rel}: declares.consumes entry needs repo, target, via: {c}")
                continue
            if via not in INTENT_VIA_KINDS:
                errors.append(f"{rel}: declares.consumes via {via!r} is not a linker mechanism (allowed: {', '.join(sorted(INTENT_VIA_KINDS))})")
                continue
            key = (repo, target, via)
            if key in seen_seam:
                errors.append(f"{rel}: seam {repo} -> {target} via {via} already declared by {seen_seam[key]}")
                continue
            seen_seam[key] = str(rel)
            corpus.setdefault(repo, {}).setdefault("consumes", []).append(
                {"repo": target, "via": via})
        for lay in dec.get("layers") or []:
            repo = lay.get("repo")
            entries = lay.get("order") or []
            if not repo or not entries:
                errors.append(f"{rel}: declares.layers entry needs repo and order: {lay}")
                continue
            if repo in seen_layers:
                errors.append(f"{rel}: layers for {repo} already declared by {seen_layers[repo]}")
                continue
            seen_layers[repo] = str(rel)
            rendered = []
            for en in entries:
                if not (isinstance(en, dict) and en.get("name") and en.get("paths")):
                    errors.append(f"{rel}: layers.order entry needs name and paths: {en}")
                    break
                rendered.append({"name": en["name"], "paths": list(en["paths"])})
            else:
                corpus.setdefault(repo, {})["layers"] = rendered
    for repo in corpus:
        if "consumes" in corpus[repo]:
            corpus[repo]["consumes"].sort(key=lambda c: (c["repo"], c["via"]))
    return corpus, errors


def _render_intent_block(corpus: dict) -> str:
    lines = [INTENT_FENCE_BEGIN, "intent:"]
    for repo in sorted(corpus):
        lines.append(f"  {repo}:")
        entry = corpus[repo]
        if entry.get("consumes"):
            lines.append("    consumes:")
            for c in entry["consumes"]:
                lines.append(f"      - repo: {c['repo']}")
                lines.append(f"        via: {c['via']}")
        if entry.get("layers"):
            lines.append("    layers:")
            for lay in entry["layers"]:
                lines.append(f"      - name: {lay['name']}")
                paths = ", ".join(f'"{p}"' for p in lay["paths"])
                lines.append(f"        paths: [{paths}]")
    lines.append(INTENT_FENCE_END)
    return "\n".join(lines) + "\n"


def cmd_intent(args) -> int:
    """`brain.py intent compile` — the wiki is the compile source: declares:
    frontmatter aggregates into the cluster config's fenced intent block.
    Idempotent; an intent block outside the fence is an error, not a merge.
    """
    if args.op == "stamp":
        # The stamp is tabula's: it writes what a page's sentences say into its
        # fields (governs:, depends_on and the rest), removes a derived
        # enola_intent block and moves hand-written halves to intent:. A second
        # implementation here drifted on governs: and flipped three
        # architecture pages back and forth, so brain.py delegates and names
        # the skip when no current tabula is present.
        code = _run_tabula(["intent", "stamp"])
        if code == -1:
            print("intent: " + _tabula_skip("intent stamp"), file=sys.stderr)
            return 0
        return code
    if args.op != "compile":
        print(f"intent: unknown op {args.op!r} (supported: compile, stamp)", file=sys.stderr)
        return 2
    corpus, errors = _wiki_declares()
    if errors:
        for e in errors:
            print(f"intent-compile ERROR: {e}", file=sys.stderr)
        return 1
    text = ENOLA_CONFIG.read_text() if ENOLA_CONFIG.exists() else ""
    if INTENT_FENCE_BEGIN in text or re.search(r"^intent:", text, re.M):
        print("intent-compile ERROR: the cluster config carries an intent block, but the wiki "
              "is the source now: pages carry intent: frontmatter and tabula export writes the "
              "mirror enola's mdintent extractor compiles; "
              "directly. Delete the config-side block.", file=sys.stderr)
        return 1
    print(f"intent: wiki-native — {sum(len(v.get('consumes', [])) for v in corpus.values())} seam(s), "
          f"{sum(1 for v in corpus.values() if v.get('layers'))} layer set(s) in intent: frontmatter, "
          f"compiled by enola at snapshot time; nothing to generate")
    return 0


_UNION_SEAM_CACHE: dict = {}


def _union_seam_edges(union: Path) -> list:
    """The cross-repo dependency facts of the union, read once per process.

    Service-to-service edges are named "<consumer> -> <provider>"; every
    other line is skipped on the raw text before it is parsed, because the
    union is a half-gigabyte with providers on and a claim check must not
    cost a full parse per claim.
    """
    key = (str(union), union.stat().st_mtime_ns)
    if key in _UNION_SEAM_CACHE:
        return _UNION_SEAM_CACHE[key]
    out = []
    with open(union) as fh:
        for line in fh:
            if '"kind":"dependency"' not in line or " -> " not in line or '"via":' not in line:
                continue
            try:
                f = json.loads(line)
            except json.JSONDecodeError:
                continue
            if f.get("kind") == "dependency" and f.get("kind") and (f.get("props") or {}).get("via"):
                out.append(f)
    _UNION_SEAM_CACHE[key] = out
    return out


_REPO_FACTS_CACHE: dict = {}


def _read_repo_facts(repo_path: Path):
    facts_path = repo_path / _enola_artifact_dir() / "facts.jsonl"
    if not facts_path.exists():
        return None
    # One read per artifact per process: several claims name the same repo,
    # and each artifact is the union as of that repo's turn.
    key = (str(facts_path), facts_path.stat().st_mtime_ns)
    if key in _REPO_FACTS_CACHE:
        return _REPO_FACTS_CACHE[key]
    label = repo_path.name
    out = []
    own = f'"repo":"{label}"'
    with open(facts_path) as fh:
        for line in fh:
            # A per-repo artifact holds the union as of that repo's turn, which
            # with providers on is a half-gigabyte of other repositories' facts.
            # Decide on the raw line before paying for the parse: only this
            # repo's facts, and legacy lines that carry no label at all.
            if own not in line and '"repo":' in line:
                continue
            try:
                f = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (f.get("repo") or label) != label:
                continue
            fl = f.get("file") or ""
            if fl.startswith(label + "/"):
                f["file"] = fl[len(label) + 1:]
            out.append(f)
    _REPO_FACTS_CACHE[key] = out
    return out


def _eval_claim(c: dict, repo_paths: dict) -> tuple[str, str]:
    """Evaluate one structured claim. Returns (verdict, detail): verdict is
    pass | fail | not-asked | malformed.
    """
    metric = c.get("metric")
    if metric == "fact-count":
        repo, kind, want = c.get("repo"), c.get("kind"), c.get("value")
        if not (repo and kind) or want is None:
            return "malformed", f"fact-count needs repo, kind, value: {c}"
        rp = repo_paths.get(repo)
        if rp is None:
            return "not-asked", f"repo {repo} not in the cluster"
        facts_list = _read_repo_facts(rp)
        if facts_list is None:
            return "not-asked", f"no graph artifacts for {repo}"
        fprefix = c.get("file_prefix")
        nprefix = c.get("name_prefix")
        distinct = c.get("distinct")
        seen = set()
        n = 0
        for f in facts_list:
            if f.get("kind") != kind:
                continue
            if fprefix and not (f.get("file") or "").startswith(fprefix):
                continue
            if nprefix and not (f.get("name") or "").startswith(nprefix):
                continue
            if distinct:
                seen.add(f.get(distinct) or (f.get("props") or {}).get(distinct) or "")
            else:
                n += 1
        got = len(seen) if distinct else n
        if got == want:
            return "pass", f"{repo} {kind} = {got}"
        return "fail", f"{repo} {kind} = {got}, page claims {want}"
    if metric == "seam":
        consumer, provider, via = c.get("consumer"), c.get("provider"), c.get("via")
        if not (consumer and provider and via):
            return "malformed", f"seam needs consumer, provider, via: {c}"
        repos = _enola_repos()
        if not repos:
            return "not-asked", "no cluster config"
        union = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
        if not union.exists():
            return "not-asked", "no union artifacts"
        for f in _union_seam_edges(union):
            if (f.get("repo") == consumer
                    and f.get("name") == f"{consumer} -> {provider}"
                    and via in ((f.get("props") or {}).get("via") or [])):
                return "pass", f"{consumer} -> {provider} via {via} measured"
        return "fail", f"no measured edge {consumer} -> {provider} via {via}"
    return "malformed", f"unknown metric {metric!r}"


def _wiki_claims() -> list[tuple[str, dict]]:
    out = []
    for page in wiki_files():
        rel = page.relative_to(WIKI)
        if rel.parts[0] in ("_views", "_archive"):
            continue
        parsed = parse(page)
        if not parsed:
            continue
        meta, _ = parsed
        for c in _intent_halves(meta)[0].get("claims") or []:
            if isinstance(c, dict):
                out.append((str(rel), c))
    return out


def _enola_artifact_dir() -> str:
    """The per-repo artifact dirname enola writes, read from the cluster
    config's output.dir rather than assumed. Parallel checkouts point their
    runs at a sibling dirname (.enola-b) so two sessions never fight over one
    artifact directory; whatever the config says is what the wrapper reads.
    """
    try:
        import yaml as _yaml
        cfg = _yaml.safe_load(ENOLA_CONFIG.read_text())
        d = ((cfg or {}).get("output") or {}).get("dir")
        if d:
            return d
    except Exception:
        pass
    return ".enola"


ARTIFACT_DIRS = (".enola-brain/", ".enola-cluster/", "mcp-arch.yaml")


def write_local_excludes(repo_paths) -> list:
    """Hide this machine's artifact directories from git, per clone.

    Twenty-one working trees carry untracked `.enola-brain` and `.enola-cluster`
    directories and not one repository gitignores them — hundreds of megabytes
    of facts, one `git clean -fd` from vanishing and one careless `git add -A`
    from being committed.

    `.git/info/exclude` rather than a tracked `.gitignore`: these repositories
    are shared with people who do not run this brain, and asking them to carry
    an ignore rule for an artifact only this machine produces is a coupling that
    would be correctly rejected in review. It is also twenty-one pull requests.
    Not a global core.excludesFile either — that silently reaches every
    repository on the machine, including ones with no relationship to this
    brain.
    """
    written = []
    for path in repo_paths:
        info = Path(path) / ".git" / "info"
        if not info.parent.is_dir():
            continue
        info.mkdir(parents=True, exist_ok=True)
        exclude = info / "exclude"
        existing = exclude.read_text() if exclude.exists() else ""
        missing = [d for d in ARTIFACT_DIRS if d not in existing]
        if not missing:
            continue
        block = ("\n# Machine-local architecture-graph artifacts (brain.py enola,\n"
                 "# mue cluster). Not tracked anywhere: they are this machine's.\n"
                 + "\n".join(missing) + "\n")
        exclude.write_text(existing.rstrip("\n") + "\n" + block if existing else block.lstrip("\n"))
        written.append(Path(path).name)
    return written


def fact_identity(raw) -> str:
    """What a fact IS, for digest purposes: kind, name, file, and relations.

    Not the whole fact. `unmatched_by_clients` is written by the cross-repo
    layer and depends on which OTHER repositories were loaded, yet it lands on
    an own-labelled fact — 5,096 of them — so a repository digested differently
    depending on the cluster's membership. Adding a repository to the cluster
    and removing it can stale receipt citations about code that never changed.

    An allow-list rather than a deny-list of prop names, because a deny-list has
    to be maintained by whoever writes the next cross-repo layer, and that is
    the contract that left the pollution count reading ten while it was
    nineteen. The default has to be safe: a prop invented later is excluded from
    identity until someone argues it belongs.

    The cost is real. `target_source` on an association says whether a target
    was declared, derived or read through a hop, and two graphs differing only
    in that now digest alike. That trade buys a digest that moves when the code
    moves; prop-level drift detection would be its own decision.
    """
    fact = json.loads(raw) if isinstance(raw, str) else raw
    relations = sorted(
        f"{(r or {}).get('kind')}\u0000{(r or {}).get('target')}"
        for r in (fact.get("relations") or [])
    )
    return "\u0001".join([
        str(fact.get("kind") or ""),
        str(fact.get("name") or ""),
        str(fact.get("file") or ""),
        "\u0002".join(relations),
    ])


def union_health(union_dir, configured, receipted=None) -> dict:
    """Whether the cross-repo union exists and covers the cluster.

    `pollution` alone cannot answer this, and on 2026-08-08 that mattered:
    `--per-repo` ran with the brain's working directory, so enola discovered the
    cluster config and wrote each single-repo graph over the union's copy. Every
    repository then held exactly its own facts, the pollution check reported
    "OK", and the union had been destroyed. The check was true and useless — the
    same shape as a coverage number from an extractor that examined nothing.

    Two questions, therefore, not one: does any repository hold someone else's
    facts, and does the union still hold everyone's.

    `receipted` names the repositories the last generate actually walked, and is
    passed rather than read so the answer depends only on the arguments. Reading
    it from module state made this function consult the live machine from inside
    a temp-directory test, and the test that caught that was one written against
    the old behaviour half an hour earlier.
    """
    facts = Path(union_dir) / "facts.jsonl"
    configured = [str(c) for c in configured]
    if not facts.exists():
        return {"ok": False, "repos": 0,
                "detail": f"no union at {union_dir} — the cross-repo graph is absent"}
    seen = set()
    for line in facts.read_text(errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            label = json.loads(line).get("repo")
        except Exception:
            continue
        if label:
            seen.add(label)
    missing = sorted(set(configured) - seen)
    # The comment that used to sit here named the distinction and the code did
    # not make it: a repository absent from the union and one that was walked
    # and had nothing to give both came out as "absent", and the check cried
    # wolf about a repository with no code (only JSON and markdown) on every
    # run. A receipt is the evidence that the walk happened, so it is what
    # separates them. Reporting the two identically is the same defect the
    # check exists to catch, one level up.
    receipted = set(receipted or ())
    empty = [r for r in missing if r in receipted]
    absent = [r for r in missing if r not in receipted]
    detail = f"union holds {len(seen)} of {len(configured)} configured repositories"
    if empty:
        detail += f"; walked and emitted nothing: {', '.join(empty)}"
    if absent:
        return {"ok": False, "repos": len(seen),
                "detail": detail + f"; ABSENT, no receipt: {', '.join(absent)}"}
    return {"ok": True, "repos": len(seen), "detail": detail}


def _enola_label_map() -> dict:
    """Checkout directory name -> the label enola gave that repository's facts.

    Read from the workspace receipt enola keeps under ~/.enola/graphs for the
    graph whose repositories include this brain. The label comes from the git
    remote, so a second checkout (`brain-2`, `website-2`) is labelled like
    the first, and any check that compares the union against directory names
    reports it missing while it is there. Identity for repositories the receipt
    does not name.
    """
    graphs = Path.home() / ".enola" / "graphs"
    if not graphs.is_dir():
        return {}
    for receipt in sorted(graphs.glob("*.json")):
        try:
            repos = json.loads(receipt.read_text(errors="ignore")).get("repos") or []
        except Exception:
            continue
        paths = {Path(str(r.get("path") or "")).resolve(): r for r in repos}
        if REPO.resolve() not in paths:
            continue
        return {p.name: str(r.get("label") or p.name) for p, r in paths.items()}
    return {}


def _receipted_repos() -> set:
    """Repositories the last generate recorded a receipt for — evidence the walk
    happened, whatever it produced."""
    try:
        data = json.loads((REPO / "wiki/_state/enola/receipts.json").read_text())
    except Exception:
        return set()
    return set(data) if isinstance(data, dict) else set()


def coupling_metrics(edges, nodes=None) -> dict:
    """The Lakos suite over one component graph.

    CD (cumulative component dependency) counts, for each component, how many
    components it depends on transitively **including itself** — so a graph with
    no edges has CCD equal to N, not zero. ACD is the mean: the number of
    components a change to an average one can reach. Propagation cost is CCD
    over N-squared, read as "a change to an average element can potentially
    affect X% of the system".

    NCCD normalises CCD against a balanced binary tree of the same size, which
    is what makes it comparable across codebases of different sizes. The
    literature reads NCCD > 2.0 as "probably contains cycles"; measured across
    19 repositories here that threshold agrees 9 times and misses 10, always in
    the same direction — below the line with cycles present, because a small
    repository with a tight two-module cycle has a low average dependency and
    the cycle barely moves the mean detecting it. The absolute threshold is
    therefore computed and reported but never used as a verdict; see
    `rank_within_estate`.
    """
    node_set = set(nodes or [])
    for a, b in edges:
        node_set.add(a)
        node_set.add(b)
    ordered = sorted(node_set)
    index = {name: i for i, name in enumerate(ordered)}
    n = len(ordered)
    if n == 0:
        return {"components": 0, "edges": 0, "ccd": 0, "acd": 0.0,
                "nccd": 0.0, "propagation_cost": 0.0}

    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[index[a]].add(index[b])

    ccd = 0
    for start in range(n):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in adjacency[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        ccd += len(seen)

    balanced = sum(math.floor(math.log2(k + 1)) + 1 for k in range(n))
    return {
        "components": n,
        "edges": len(set(edges)),
        "ccd": ccd,
        "acd": round(ccd / n, 2),
        "nccd": round(ccd / balanced, 2) if balanced else 0.0,
        "propagation_cost": round(100 * ccd / (n * n), 2),
    }


def coupling_by_language(triples) -> dict:
    """One metric set per language subgraph, never merged.

    A repository holding a Rails app and an Ember app holds two graphs that
    barely reference each other. Combining them grows N-squared while leaving
    reachability alone, so the combined propagation cost lands *below* either
    constituent: the monolith reads 0.8% while its ruby half reads 3.5%. A
    reader given the combined number concludes the opposite of the truth.
    """
    per_language = collections.defaultdict(list)
    for a, b, language in triples:
        per_language[language or "unknown"].append((a, b))
    return {lang: coupling_metrics(edges) for lang, edges in per_language.items()}


def rank_within_estate(rows, field) -> list:
    """Rank by percentile inside this estate rather than against a threshold.

    The research backlog's own validity section asks for exactly this: a
    threshold calibrated on Go fires constantly on Rails, so distributions
    within a codebase are both more honest and more useful than absolute
    cut-offs. It is also the only defensible option here, since the one absolute
    threshold on offer was measured wrong 10 times out of 12.
    """
    ordered = sorted(rows, key=lambda r: r.get(field) or 0, reverse=True)
    total = len(ordered)
    out = []
    for position, row in enumerate(ordered):
        enriched = dict(row)
        enriched["percentile"] = int(round(100 * (total - position) / total))
        out.append(enriched)
    return out


def enola_pollution_report(repo_paths) -> list:
    """Repositories whose own `.enola` holds facts labelled for another repo.

    The cluster's `output.dir` is resolved with `filepath.Join(repoPath, dir)`
    per repository as the engine walks them, so every repository receives the
    accumulating union as of its own turn and only the last one is complete.
    Pointed at `.enola`, that means a repository's own graph directory holds
    mostly other people's code, and nothing says so: no error, no warning, and
    every extra fact is a true fact about a real codebase.

    Returns a list rather than a count on purpose. This was recorded once as
    "ten repositories, historical" and was eighteen and current, because the
    number lived in a paragraph. Repositories are actionable; a total is not.
    """
    found = []
    for path in repo_paths:
        path = Path(path)
        facts = path / ".enola" / "facts.jsonl"
        if not facts.exists():
            # Absent is not pollution. A repository with no graph degrades to a
            # named skip, which every rule here already handles.
            continue
        own_label = _enola_recorded_label(path / ".enola") or path.name
        own = 0
        foreign = {}
        for line in facts.read_text(errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                label = json.loads(line).get("repo")
            except Exception:
                continue
            if not label:
                continue
            if label == own_label:
                own += 1
            else:
                foreign[label] = foreign.get(label, 0) + 1
        if foreign:
            found.append({
                "repo": own_label,
                "path": str(path),
                "own": own,
                "foreign": dict(sorted(foreign.items())),
            })
    return found


def _enola_recorded_label(snapshot_dir: Path) -> str:
    """The repo label a snapshot's own meta records, or "" when it records none.

    enola labels facts from the git remote (`website`), not from the checkout
    directory (`website-2`), so a second checkout read against its directory
    name looked wholly foreign to itself ("own 0, foreign website N"). The
    snapshot's meta is what labelled the facts, so it is what the facts are
    compared against.
    """
    meta = snapshot_dir / "snapshot.meta.json"
    if not meta.exists():
        return ""
    try:
        return str(json.loads(meta.read_text(errors="ignore")).get("repo_label") or "")
    except Exception:
        return ""


def _enola_content_digests() -> dict:
    """Per-repo order-insensitive digests over fact content.

    Drift keys on this digest rather than upstream snapshot_id: the
    2026-07-30 build found snapshot_id nondeterministic whenever the TS
    resolver sees duplicate candidate paths for an import (the trigger
    was ember_app's types/ shadow tree, since excluded from the
    cluster). Facts sort before hashing so parallel extraction order
    can never re-introduce the problem.

    Each repo's digest reads that repo's OWN .enola/facts.jsonl,
    filtered to facts carrying its label. Until 2026-08-04 the digests
    were sliced out of the final union instead, and the union's label
    assignment depends on append-chain history (the engine
    retroactively bulk-labels inherited facts), so an operationally
    different regen moved every digest without any repo content
    moving — invalidating receipt citations that the content never
    contradicted. The own-file set is the repo's fresh extraction and
    is stable across regens; repos whose own file is absent fall back
    to the union slice, which is better than no digest.
    """
    repos = _enola_repos()
    if not repos:
        return {}

    def digest(facts):
        return "sha256:" + hashlib.sha256(
            "\n".join(sorted(set(facts))).encode()
        ).hexdigest()

    def own_file_facts(path, name):
        facts = []
        with open(path) as fh:
            for line in fh:
                try:
                    fact = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (fact.get("repo") or name) == name:
                    facts.append(fact_identity(fact))
        return facts

    digests = {}
    missing = []
    for repo_path in repos:
        facts_path = repo_path / _enola_artifact_dir() / "facts.jsonl"
        if facts_path.exists():
            digests[repo_path.name] = digest(
                own_file_facts(facts_path, repo_path.name))
        else:
            missing.append(repo_path.name)
    if missing:
        union_path = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
        if union_path.exists():
            per_repo: dict[str, list] = {}
            with open(union_path) as fh:
                for line in fh:
                    try:
                        fact = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    per_repo.setdefault(fact.get("repo") or "(unlabeled)",
                                        []).append(
                        json.dumps(fact, sort_keys=True))
            for name in missing:
                if name in per_repo:
                    digests[name] = digest(per_repo[name])
    return digests


ENOLA_PROGRESS_MARKERS = ("[engine] found ", "[engine] wrote ", "[providers] ")


def _enola_run_streaming(argv: list) -> tuple:
    """Run the binary with its progress visible, returning (code, tail).

    A cluster generation is minutes at best and over an hour when a binary
    upgrade empties the extractor cache, and buffering all of it meant the
    only way to learn which repository a long run was inside was reading the
    process's open file descriptors from /proc. The engine already logs a
    line per repository as it starts one; this forwards those and keeps the
    rest for the error path.
    """
    started = time.monotonic()
    tail = collections.deque(maxlen=200)
    proc = subprocess.Popen(argv, cwd=REPO, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True,
                            bufsize=1, env=_enola_env())
    for line in proc.stdout:
        line = line.rstrip()
        tail.append(line)
        if any(marker in line for marker in ENOLA_PROGRESS_MARKERS):
            print(f"  [{time.monotonic() - started:6.0f}s] {line[:160]}",
                  flush=True)
    proc.wait()
    return proc.returncode, "\n".join(tail)


def _enola_seconds(duration: str) -> float:
    """Parse Go's duration spelling (1m20.9s, 583ms, 2.1s) into seconds."""
    if not duration:
        return 0.0
    match = re.match(r"(?:(\d+)h)?(?:(\d+)m)?(?:([\d.]+)(ms|µs|s))?$", duration)
    if not match:
        return 0.0
    hours, minutes, value, unit = match.groups()
    seconds = float(hours or 0) * 3600 + float(minutes or 0) * 60
    if value:
        scale = {"s": 1.0, "ms": 0.001, "µs": 0.000001}[unit]
        seconds += float(value) * scale
    return seconds


def _enola_report_slowest(recorded: dict, top: int = 3) -> None:
    """Name what the run spent its time on, so the next slow one is read."""
    timed = [(name, _enola_seconds(entry.get("duration") or ""))
             for name, entry in recorded.items()]
    timed = [pair for pair in timed if pair[1] > 0]
    if not timed:
        return
    total = sum(seconds for _, seconds in timed)
    timed.sort(key=lambda pair: pair[1], reverse=True)
    slowest = ", ".join(f"{name} {seconds:.0f}s" for name, seconds in timed[:top])
    print(f"generation time {total:.0f}s across {len(timed)} repositories; "
          f"slowest {slowest}")


def _enola_record() -> dict:
    """Aggregate per-repo receipt.json files into the committed state."""
    recorded = {}
    digests = _enola_content_digests()
    for repo_path in _enola_repos():
        receipt = _enola_live_receipt(repo_path)
        if receipt:
            entry = _enola_entry(receipt)
            entry["content_digest"] = digests.get(repo_path.name)
            recorded[repo_path.name] = entry
    ENOLA_RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
    ENOLA_RECEIPTS.write_text(json.dumps(recorded, indent=2) + "\n")
    return recorded


_SYMBOL_INDEX_MEMO: dict = {}


def _enola_symbol_repo_index() -> dict:
    """Memoized on the union file's identity: `_enola_findings` builds this
    index and `ledger-hygiene` asks for it again in the same run, which on
    2026-08-22 was two full parses of a 883 MB, 2.3M-fact union (5.6 s each)
    for one 988k-entry map. A regenerate changes size or mtime and misses.
    """
    repos = _enola_repos()
    if not repos:
        return {}
    facts_path = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
    try:
        st = facts_path.stat()
    except OSError:
        return {}
    key = (str(facts_path), st.st_size, st.st_mtime_ns)
    hit = _SYMBOL_INDEX_MEMO.get(key)
    if hit is None:
        hit = _SYMBOL_INDEX_MEMO[key] = _enola_symbol_repo_index_scan()
    return hit


def _enola_symbol_repo_index_scan() -> dict:
    """Map module/symbol names to their owning repo from the fact set.

    Findings whose evidence carries only a symbol (`exported-surface`
    names `app/components/common.Carousel`, never a file) are otherwise
    unattributable, and an unattributed finding cannot be narrowed by
    repo — which is the whole point of the merged surface.
    """
    repos = _enola_repos()
    if not repos:
        return {}
    facts_path = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
    if not facts_path.exists():
        return {}
    index = {}
    with open(facts_path) as fh:
        for line in fh:
            try:
                fact = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = fact.get("name")
            if name and name not in index:
                index[name] = fact.get("repo")
    return index


def _enola_finding_repo(finding: dict, repo_names: set,
                        symbol_index: dict) -> str:
    """Attribute a finding to the repo its evidence names.

    Never to the file it was read from: the per-repo insights.json
    files are cumulative in config order, so the file a finding appears
    in says nothing about what it describes.
    """
    evidence = finding.get("evidence") or []
    for item in evidence:
        head = (item.get("file") or "").split("/")[0]
        if head in repo_names:
            return head
    for item in evidence:
        symbol = item.get("symbol") or ""
        while symbol:
            owner = symbol_index.get(symbol)
            if owner:
                return owner
            symbol = symbol.rpartition(".")[0]
    for item in evidence:
        # Layer violations name an unprefixed path (`app/jobs/_coupling.rb`)
        # where god-class names a prefixed one; walk up to the module.
        path = (item.get("file") or "").rpartition("/")[0]
        while path:
            owner = symbol_index.get(path)
            if owner:
                return owner
            path = path.rpartition("/")[0]
    for item in evidence:
        owner = symbol_index.get(item.get("fact") or "")
        if owner:
            return owner
    title = finding.get("title") or ""
    for name in sorted(repo_names, key=len, reverse=True):
        if name in title:
            return name
    return "(unattributed)"


def _enola_finding_anchor(finding: dict) -> str:
    """The most stable identifier in a finding's evidence."""
    for item in finding.get("evidence") or []:
        for key in ("symbol", "file", "fact"):
            value = item.get(key)
            if value:
                return value
    return (finding.get("title") or "").strip()


def _enola_finding_signature(finding: dict, repo: str) -> str:
    """Identity that survives the finding's description changing.

    Titles carry counts — the coupling-cluster title names 267 modules
    today — so a title-keyed verdict would be orphaned by any code
    change. Explainer plus owning repo plus primary evidence anchor is
    stable across snapshots.
    """
    anchor = _enola_finding_anchor(finding)
    if anchor.startswith(f"{repo}/"):
        anchor = anchor[len(repo) + 1:]
    return f"{finding.get('source')}:{repo}:{anchor}"


def _enola_snapshotted_repos() -> tuple[set, set]:
    """(repos with an insights.json, repos in the cluster without one).

    Callers must be able to tell "this repo has no findings" from "this
    repo was never looked at" — the ADR's binding no-silent-empty rule.
    """
    have, missing = set(), set()
    for repo_path in _enola_repos():
        target = have if (repo_path / _enola_artifact_dir() / "insights.json").exists() \
            else missing
        target.add(repo_path.name)
    return have, missing


def _enola_findings() -> list[dict]:
    """Every distinct finding across the cluster, attributed and keyed.

    Each explainer keeps a top-N over a graph that accumulates in
    config order, so no single insights.json holds the cluster's whole
    result set — reading only the newest silently drops findings from
    every repo the monolith outweighs.
    """
    repo_paths = _enola_repos()
    repo_names = {p.name for p in repo_paths}
    symbol_index = _enola_symbol_repo_index()
    merged = {}
    for repo_path in repo_paths:
        path = repo_path / _enola_artifact_dir() / "insights.json"
        if not path.exists():
            continue
        try:
            findings = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        for finding in findings:
            repo = _enola_finding_repo(finding, repo_names, symbol_index)
            signature = _enola_finding_signature(finding, repo)
            # Aggregate findings (crossrepo bundles every edge into one
            # item) anchor on their *first* evidence entry, so a later,
            # richer version of the same aggregate collides with a
            # thinner one. First-seen-wins silently discarded the
            # `a -> b` edge because an earlier repo's
            # snapshot carried the same anchor with fewer edges.
            prior = merged.get(signature)
            if prior and len(prior["evidence"]) >= len(finding.get("evidence") or []):
                continue
            merged[signature] = {
                "signature": signature,
                "repo": repo,
                "explainer": finding.get("source"),
                "title": finding.get("title"),
                "confidence": finding.get("confidence"),
                "description": finding.get("description"),
                "evidence": finding.get("evidence") or [],
            }
    return sorted(merged.values(),
                  key=lambda f: (f["repo"], f["explainer"] or "",
                                 f["title"] or ""))


def _enola_load_verdicts() -> dict:
    """The judgment ledger — absence of an entry means unjudged.

    There is no pending state by construction: nothing writes an entry
    until a judgment is made, and nothing enumerates the unjudged set
    as work. That is what keeps this a memory rather than a backlog.
    """
    if not ENOLA_VERDICTS.exists():
        return {"entries": []}
    try:
        return json.loads(ENOLA_VERDICTS.read_text())
    except (json.JSONDecodeError, OSError):
        return {"entries": []}


def _enola_verdict_for(finding: dict, ledger: dict) -> dict | None:
    """Exact signature first, then class rules."""
    for entry in ledger.get("entries") or []:
        if entry.get("signature") == finding["signature"]:
            return entry
    for entry in ledger.get("entries") or []:
        match = entry.get("match")
        if not match:
            continue
        explainer = match.get("explainer")
        if explainer and explainer != finding["explainer"]:
            continue
        prefix = match.get("title_prefix")
        if prefix and not (finding["title"] or "").startswith(prefix):
            continue
        repo = match.get("repo")
        if repo and repo != finding["repo"]:
            continue
        return entry
    return None


def _enola_impact(symbol: str) -> dict | None:
    """Fan-in, fan-out and callers for a symbol, from the fact set.

    Computed here rather than through the MCP server because MCP is
    absent in headless and scheduled runs, and the call relations are
    already on disk.
    """
    repos = _enola_repos()
    if not repos:
        return None
    facts_path = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
    if not facts_path.exists():
        return None
    callers, callees, located = [], [], None
    with open(facts_path) as fh:
        for line in fh:
            try:
                fact = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = fact.get("name")
            if name == symbol and located is None:
                located = {"repo": fact.get("repo"), "file": fact.get("file"),
                           "kind": fact.get("kind")}
            for relation in fact.get("relations") or []:
                if relation.get("kind") != "calls":
                    continue
                if relation.get("target") == symbol and name != symbol:
                    callers.append(name)
                elif name == symbol:
                    callees.append(relation.get("target"))
    if located is None and not callers and not callees:
        return None
    return {
        "symbol": symbol,
        "located": located,
        "fan_in": len(set(callers)),
        "fan_out": len(set(callees)),
        "callers": sorted(set(c for c in callers if c)),
        "callees": sorted(set(c for c in callees if c)),
    }


def _enola_govern(target: str) -> dict | None:
    """The reverse query, headless: which compiled pages govern a file or
    symbol, and which code a page governs.

    Reads the union facts.jsonl directly because MCP is absent in headless
    and scheduled runs. Joins in both the label-prefixed and repo-relative
    file forms, mirroring the engine's own anchor join.
    """
    repos = _enola_repos()
    if not repos:
        return None
    facts_path = repos[-1] / _enola_artifact_dir() / "facts.jsonl"
    if not facts_path.exists():
        return None
    anchors, pages, relations = [], {}, {}
    measured = []
    located = None
    with open(facts_path) as fh:
        for line in fh:
            try:
                fact = json.loads(line)
            except json.JSONDecodeError:
                continue
            props = fact.get("props") or {}
            if fact.get("kind") == "intent":
                ikind = props.get("intent_kind")
                if ikind == "anchor":
                    anchors.append((props.get("intent_owner"), props.get("path"),
                                    fact.get("file")))
                elif ikind == "page":
                    pages[fact.get("file")] = (props.get("page_type"),
                                               props.get("status"))
                elif ikind == "relation":
                    relations.setdefault(fact.get("file"), []).append(
                        (props.get("rel"), props.get("to")))
                continue
            repo, file = fact.get("repo"), fact.get("file")
            if not repo or not file:
                continue
            measured.append((repo, file))
            if located is None and (fact.get("name") == target or file == target
                                    or _strip_label(file, repo) == target):
                located = (repo, file)
    if not pages:
        return {"not_asked": True}
    page_file = next((f for f in pages
                      if f == target or _strip_label(f, f.split("/", 1)[0]) == target),
                     None)
    if page_file is not None:
        coverage = []
        for owner, path, source in anchors:
            if source != page_file:
                continue
            hits = {f for r, f in measured if r == owner
                    and (path in (f, _strip_label(f, r))
                         or f.startswith(path + "/")
                         or _strip_label(f, r).startswith(path + "/"))}
            coverage.append({"repo": owner, "path": path, "files": len(hits)})
        return {"page": page_file, "meta": pages[page_file], "coverage": coverage}
    if located is None:
        return None
    repo, file = located
    forms = {file, _strip_label(file, repo)}
    governing = []
    for owner, path, source in anchors:
        if owner != repo:
            continue
        if any(path == f or f.startswith(path + "/") for f in forms):
            meta = pages.get(source, ("", ""))
            governing.append({"page": source, "meta": meta,
                              "relations": [
                                  {"rel": rel, "to": to,
                                   "meta": next((pages[p] for p in pages
                                                 if p == to or _strip_label(p, p.split("/", 1)[0]) == to),
                                                None)}
                                  for rel, to in relations.get(source, [])]})
    return {"target": file, "repo": repo,
            "governing": sorted(governing, key=lambda g: g["page"])}


def _strip_label(file: str, repo: str) -> str:
    return file[len(repo) + 1:] if repo and file.startswith(repo + "/") else file


def _enola_govern_pr(repo: str, pr: int) -> int:
    """Review mode: the governing trail for a whole sibling-repo PR.

    Resolves the PR's changed files through the sibling checkout's own
    `gh` remote, runs the reverse query per file, and reports the union
    of governing pages grouped by page — plus the files nothing governs
    and the files the graph has not measured, kept distinct per the
    asked-versus-agreed rule. Degrades to a named skip when the graph
    or `gh` is absent, per the no-graph-step-blocks rule.
    """
    sibling = PROJECTS / repo
    if not sibling.is_dir():
        print(f"enola govern --pr: no sibling checkout at {sibling} — skipping")
        return 0
    try:
        out = subprocess.run(["gh", "pr", "diff", str(pr), "--name-only"],
                             cwd=sibling, capture_output=True, text=True,
                             timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"enola govern --pr: gh unavailable ({exc}) — skipping")
        return 0
    if out.returncode != 0:
        print(f"enola govern --pr: gh pr diff failed for {repo}#{pr}: "
              f"{out.stderr.strip()[:200]}")
        return 1
    files = [f for f in out.stdout.splitlines() if f.strip()]
    if not files:
        print(f"enola govern --pr: {repo}#{pr} has no changed files")
        return 0
    by_page: dict[str, dict] = {}
    ungoverned, unmeasured = [], []
    for f in files:
        result = _enola_govern(f"{repo}/{f}")
        if result is None:
            unmeasured.append(f)
            continue
        if result.get("not_asked"):
            print("enola: no knowledge pages compiled into the snapshot — "
                  "the reverse query was not asked")
            return 0
        governing = result.get("governing") or []
        if not governing:
            ungoverned.append(f)
            continue
        for gov in governing:
            entry = by_page.setdefault(gov["page"],
                                       {"meta": gov["meta"], "files": []})
            entry["files"].append(f)
    print(f"{repo}#{pr} — {len(files)} changed file(s)")
    for page in sorted(by_page):
        ptype, pstatus = by_page[page]["meta"]
        suffix = f" ({ptype}, {pstatus})" if ptype or pstatus else ""
        print(f"  governed by {page}{suffix}")
        for f in by_page[page]["files"]:
            print(f"      {f}")
    if ungoverned:
        print(f"  no governing page ({len(ungoverned)} file(s) — asked, "
              "none governs):")
        for f in ungoverned:
            print(f"      {f}")
    if unmeasured:
        print(f"  not measured ({len(unmeasured)} file(s) — the graph was "
              "not asked; specs, fixtures and unindexed kinds land here):")
        for f in unmeasured:
            print(f"      {f}")
    return 0


ENOLA_CITATION_RX = re.compile(
    r"enola receipt (?P<repo>[\w.-]+) "
    r"`sha256:(?P<digest>[0-9a-f]{12,})…?` "
    r"@ `(?P<commit>[0-9a-f]{7,40})`, "
    r"(?P<date>\d{4}-\d{2}-\d{2})"
)


def _enola_wiki_citations() -> list[dict]:
    """Extract receipt citations from wiki prose and verdict them.

    Grammar per wiki/brain/adrs/receipt-claim-verification.md. A
    window around each occurrence is whitespace-normalized before
    matching so citations wrapped across lines still parse. Windows
    mentioning `enola receipt` without any `sha256:` nearby are prose
    discussion, not citation attempts, and are ignored; with one,
    grammar failure is verdict `malformed`.
    """
    recorded = {}
    if ENOLA_RECEIPTS.exists():
        try:
            recorded = json.loads(ENOLA_RECEIPTS.read_text())
        except json.JSONDecodeError:
            pass
    citations = []
    for page in wiki_files():
        rel = page.relative_to(WIKI)
        if rel.parts[0] in ("_views", "_archive"):
            continue
        text = page.read_text()
        lowered = text.lower()
        start = 0
        while True:
            idx = lowered.find("enola receipt", start)
            if idx == -1:
                break
            start = idx + 1
            window = re.sub(r"\s+", " ", text[idx:idx + 300])
            if "sha256:" not in window[:60]:
                continue
            lead = re.sub(r"\s+", " ", text[max(0, idx - 60):idx]).lower()
            if "e.g." in lead or "for example" in lead:
                continue
            lineno = text.count("\n", 0, idx) + 1
            m = ENOLA_CITATION_RX.match(window)
            if not m:
                citations.append({"page": str(rel), "line": lineno,
                                  "repo": None, "digest": None,
                                  "verdict": "malformed"})
                continue
            repo, digest = m.group("repo"), m.group("digest")
            entry = recorded.get(repo)
            if entry is None:
                verdict = "unknown-repo"
            else:
                current = (entry.get("content_digest") or "").removeprefix("sha256:")
                verdict = "verified" if current.startswith(digest) else "stale"
            citations.append({"page": str(rel), "line": lineno,
                              "repo": repo, "digest": digest,
                              "verdict": verdict})
    return citations


def cmd_enola(args) -> int:
    """Wrap the enola architecture-graph tool for brain workflows.

    Subcommands (via the `op` argument):
      generate       — run `enola --generate mcp-arch.yaml`, then record
                       every repo's receipt into
                       wiki/_state/enola/receipts.json.
      receipt [<repo>] — print recorded receipt entry/entries.
      diff           — compare recorded receipts against each repo's live
                       .enola/receipt.json; report drift at repo
                       granularity with fact-count deltas. Skips (exit 0,
                       one line) when the binary, config, or state is
                       absent — remote CI never depends on enola.
      findings       — the cluster's distinct explainer findings, merged
                       across every repo's cumulative insights.json,
                       attributed to the repo their evidence names, with
                       anything already judged noise or rejected hidden
                       unless --all.
      judge          — record a verdict (accepted / rejected / noise) for
                       one finding signature. Write-on-judgment: the
                       ledger has no pending state, and nothing here
                       enumerates unjudged findings as work.
      impact         — fan-in / fan-out / callers for a symbol, read from
                       the on-disk fact set rather than the MCP server so
                       headless and scheduled runs keep working.

    Per wiki/brain/adrs/architecture-graph-consumption.md.
    """
    op = args.op

    if op == "generate" and getattr(args, "per_repo", False):
        binary = _enola_bin()
        if binary is None:
            print("enola binary not found (~/.local/bin/enola)", file=sys.stderr)
            return 1
        repos = _enola_repos()
        # Opt-in rather than a step of the cluster run: twenty extra snapshots
        # on every regeneration would serve sessions that may never happen, and
        # an absent graph already degrades to a named skip.
        print(f"generating a single-repo graph in each of {len(repos)} repositories")
        write_local_excludes(repos)
        write_member_configs(repos)
        failed = []
        for path in repos:
            # cwd is the repository, not the brain. Run from the brain and
            # enola discovers the cluster config there, writes the single-repo
            # graph into the cluster's output directory, and overwrites the
            # union's copy — which is exactly how the union was destroyed on
            # 2026-08-08 while every check reported clean.
            result = subprocess.run([binary, "--generate", str(path)],
                                    cwd=str(path), capture_output=True, text=True,
                                    env=_enola_env())
            state = "OK " if result.returncode == 0 else "FAIL"
            if result.returncode != 0:
                failed.append(Path(path).name)
            print(f"  {state} {Path(path).name}")
        write_local_excludes(repos)
        if failed:
            print(f"\n{len(failed)} failed: {', '.join(failed)}")
        return 0

    if op == "generate":
        binary = _enola_bin()
        if binary is None:
            print("enola binary not found (~/.local/bin/enola); "
                  "install per wiki/brain/adrs/architecture-graph-substrate.md",
                  file=sys.stderr)
            return 1
        if not ENOLA_CONFIG.exists():
            print(f"missing {ENOLA_CONFIG}", file=sys.stderr)
            return 1
        # The page mirror is a cluster member, so it is written before the
        # snapshot reads it; an absent tabula falls back to brain.py's twin.
        if cmd_export(argparse.Namespace(check=False, python=False)) not in (0,):
            print("enola: export failed; the snapshot would read a stale page mirror",
                  file=sys.stderr)
            return 1
        refresh = getattr(args, "refresh", None)
        argv = [binary, "--generate", str(ENOLA_CONFIG)]
        if refresh:
            # One repository re-read into the existing union, replacing its
            # slice; the other twenty-one are not touched. Named the way
            # repos: names it (a sibling directory), resolved against the
            # config like repos: is, and refused by enola itself when it is
            # not a member, when no union exists, or when the union was built
            # by another extractor version.
            target = (ENOLA_CONFIG.parent / refresh).resolve()
            if not target.is_dir():
                print(f"enola: --refresh names no directory: {refresh}", file=sys.stderr)
                return 1
            argv = [binary, "--generate", "--refresh", str(target), str(ENOLA_CONFIG)]
        returncode, tail = _enola_run_streaming(argv)
        if returncode != 0:
            print(tail, file=sys.stderr)
            return returncode
        recorded = _enola_record()
        for name, entry in sorted(recorded.items()):
            took = f" in {entry['duration']}" if entry.get("duration") else ""
            print(f"OK  {name}: {entry['fact_count']} facts @ "
                  f"{(entry['git_commit'] or '')[:8]}"
                  f"{' (dirty)' if entry['git_dirty'] else ''}{took}")
        _enola_report_slowest(recorded)
        # The check calls itself, which was the Tech Lead's dissent when it
        # shipped without a caller. The whole finding is that a silent wrong
        # answer survived two months and one fix aimed at the wrong tool; a
        # check nobody invokes is how there is a fourth discovery. It reports.
        polluted = enola_pollution_report(_enola_repos())
        if polluted:
            print(f"\nWARNING  {len(polluted)} repository graph(s) hold another "
                  f"repository's facts: {', '.join(e['repo'] for e in polluted)}")
            print("         run `brain.py enola pollution` for the breakdown")
        write_local_excludes(_enola_repos())
        configs = write_member_configs(_enola_repos())
        if configs:
            print(f"member configs written for the session hooks: {len(configs)}")
        # Debt surfaces at creation: the digests this generate just moved may
        # have staled prose citations, and finding that out on a failing CI
        # run later is how the 0.4.6 regeneration was experienced. The join
        # is the citations inventory this tool already keeps; re-verifying
        # stays judgment work and is deliberately not automated here.
        staled = [c for c in _enola_wiki_citations() if c["verdict"] == "stale"]
        if staled:
            print(f"\nDEBT  this generate staled {len(staled)} receipt "
                  f"citation(s); re-verify or annotate before promoting:")
            for c in staled:
                print(f"      {c['page']}:{c['line']} ({c['repo'] or '(unparsed)'})")
        return 0

    if op == "metrics":
        union = REPO / _enola_artifact_dir() / "facts.jsonl"
        if not union.exists():
            print("enola: no union snapshot — skipping metrics "
                  "(run `brain.py enola generate`)")
            return 0
        triples = collections.defaultdict(list)
        for line in union.read_text(errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                fact = json.loads(line)
            except Exception:
                continue
            if fact.get("kind") != "dependency":
                continue
            name = fact.get("name") or ""
            if " -> " not in name:
                continue
            props = fact.get("props") or {}
            # Lakos metrics describe your components, not the gems you depend
            # on. Including externals dilutes rather than inflates — they are
            # leaves with high in-degree and no edges back, so they add
            # components without adding reachability, and a Ruby graph reads a
            # lower ACD with them than without. The hub list they produce is
            # standard-library and framework gems.
            if props.get("source") != "internal":
                continue
            a, b = name.split(" -> ", 1)
            lang = props.get("language") or "unknown"
            triples[fact.get("repo")].append((a, b, lang))

        rows = []
        for repo, items in triples.items():
            for lang, metrics in coupling_by_language(items).items():
                if metrics["components"] < 10:
                    # Too small for a mean to say anything. Skipped rather than
                    # reported, because a three-component graph produces a
                    # confident number about nothing.
                    continue
                rows.append({"key": f"{repo}/{lang}", **metrics})
        if not rows:
            print("enola: no component dependency edges to measure")
            return 0

        # Ranked by NCCD, not propagation cost. Propagation cost is CCD over
        # N-squared, so it rewards being small: a 12-component graph reads 21.5%
        # and tops the estate while saying nothing. NCCD normalises against a
        # balanced tree of the same size, which is the entire reason it exists.
        ranked = rank_within_estate(rows, "nccd")
        print(f"{'repo/language':<28}{'comps':>7}{'edges':>7}{'ACD':>8}"
              f"{'NCCD':>7}{'prop%':>7}{'pct':>5}")
        for row in ranked:
            print(f"{row['key']:<28}{row['components']:7}{row['edges']:7}"
                  f"{row['acd']:8.1f}{row['nccd']:7.2f}"
                  f"{row['propagation_cost']:7.1f}{row['percentile']:5}")
        print("\nRanked within this estate, not against a literature threshold: "
              "NCCD > 2.0\nis read as 'probably contains cycles' and agrees 9 "
              "times of 19 here, missing\n10 — always below the line with cycles "
              "present. Language subgraphs are never\nmerged; combining a Rails "
              "and an Ember graph dilutes propagation below both.")
        return 0

    if op == "excludes":
        written = write_local_excludes(_enola_repos())
        if not written:
            print("OK  every clone already excludes the artifact directories")
        else:
            print(f"excluded artifact dirs in {len(written)} clone(s): "
                  f"{', '.join(written)}")
        return 0

    if op == "pollution":
        repos = _enola_repos()
        polluted = enola_pollution_report(repos)
        # Asked as a second question, because the first one answers "OK" just as
        # loudly when the union has been destroyed as when everything is well.
        labels = _enola_label_map()
        union = union_health(REPO / _enola_artifact_dir(),
                             [labels.get(Path(r).name, Path(r).name) for r in repos],
                             receipted={labels.get(r, r) for r in _receipted_repos()})
        if not polluted:
            print("OK  every repository's .enola holds only its own facts")
            print(("OK  " if union["ok"] else "WARNING  ") + union["detail"])
            return 0
        print(f"{len(polluted)} repository graph(s) hold facts belonging to "
              f"another repository:")
        for entry in polluted:
            foreign = ", ".join(f"{name} {count}"
                                for name, count in entry["foreign"].items())
            print(f"  {entry['repo']:<20} own {entry['own']}, foreign: {foreign}")
        print("\nAnything reading one of these in isolation answers from a wider "
              "world without saying so.")
        # Reports, never blocks: no graph-dependent step in this brain may stop
        # work. The Tech Lead dissented on that in council and the follow-on is a
        # caller at the end of `enola generate`, not a gate here.
        return 0

    if op == "receipt":
        if not ENOLA_RECEIPTS.exists():
            print("no recorded receipts (run: brain.py enola generate)",
                  file=sys.stderr)
            return 1
        recorded = json.loads(ENOLA_RECEIPTS.read_text())
        if args.repo:
            entry = recorded.get(args.repo)
            if not entry:
                print(f"no receipt for {args.repo}", file=sys.stderr)
                return 1
            print(json.dumps(entry, indent=2))
        else:
            print(json.dumps(recorded, indent=2))
        return 0

    if op == "findings":
        if not _enola_repos():
            print("enola: no cluster config — skipping findings")
            return 0
        findings = _enola_findings()
        if not findings:
            print("enola: no snapshot artifacts on this machine — "
                  "skipping findings (run `brain.py enola generate`)")
            return 0
        ledger = _enola_load_verdicts()
        rows = []
        for finding in findings:
            verdict = _enola_verdict_for(finding, ledger)
            kind = (verdict or {}).get("verdict")
            if not args.all and kind in ("noise", "rejected"):
                continue
            if args.repo and finding["repo"] != args.repo:
                continue
            if args.explainer and finding["explainer"] != args.explainer:
                continue
            if (args.min_confidence is not None
                    and (finding["confidence"] or 0) < args.min_confidence):
                continue
            rows.append((finding, verdict))
        if args.json:
            print(json.dumps([{**f, "verdict": v} for f, v in rows],
                             indent=2))
            return 0
        for finding, verdict in rows:
            mark = f" [{verdict['verdict']}]" if verdict else ""
            print(f"{finding['repo']}  {finding['explainer']}  "
                  f"conf={finding['confidence']}{mark}")
            print(f"    {finding['title']}")
            print(f"    sig: {finding['signature']}")
        print(f"\n{len(rows)} finding(s) shown"
              f"{' (including judged)' if args.all else ''}"
              f" of {len(findings)} in the cluster.")
        _, missing = _enola_snapshotted_repos()
        if missing:
            print(f"enola: no snapshot for {', '.join(sorted(missing))} — "
                  f"not searched (regenerate to include)")
        return 0

    if op == "judge":
        if args.verdict not in ENOLA_VERDICT_KINDS:
            print(f"verdict must be one of {', '.join(ENOLA_VERDICT_KINDS)}",
                  file=sys.stderr)
            return 1
        ledger = _enola_load_verdicts()
        entries = [e for e in (ledger.get("entries") or [])
                   if e.get("signature") != args.signature]
        entry = {
            "signature": args.signature,
            "verdict": args.verdict,
            "why": args.why,
            "recorded": today_utc().isoformat(),
        }
        if args.cited_at:
            entry["cited_at"] = args.cited_at
        entries.append(entry)
        ledger["entries"] = sorted(
            entries, key=lambda e: (e.get("signature") or "",
                                    str(e.get("match") or "")))
        ENOLA_VERDICTS.parent.mkdir(parents=True, exist_ok=True)
        ENOLA_VERDICTS.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"recorded {args.verdict}: {args.signature}")
        return 0

    if op == "impact":
        result = _enola_impact(args.symbol)
        if result is None:
            print(f"enola: no snapshot fact for {args.symbol!r} "
                  "(absent graph, or the symbol is not extracted)")
            return 0
        located = result["located"] or {}
        print(f"{result['symbol']}  fan-in {result['fan_in']}  "
              f"fan-out {result['fan_out']}")
        if located:
            print(f"    {located.get('repo')}: {located.get('file')}")
        for caller in result["callers"][:args.limit]:
            print(f"    <- {caller}")
        if len(result["callers"]) > args.limit:
            print(f"    <- … {len(result['callers']) - args.limit} more")
        return 0

    if op == "govern":
        if getattr(args, "pr", None):
            if not args.repo:
                print("enola govern --pr: --repo <repo> is required")
                return 2
            return _enola_govern_pr(args.repo, args.pr)
        if not args.target:
            print("enola govern: a target or --pr <number> is required")
            return 2
        result = _enola_govern(args.target)
        if result is None:
            print(f"enola: nothing measured matches {args.target!r} "
                  "(not a compiled page, fact name, or measured file)")
            return 0
        if result.get("not_asked"):
            print("enola: no knowledge pages compiled into the snapshot — "
                  "the reverse query was not asked")
            return 0
        if "coverage" in result:
            ptype, pstatus = result["meta"]
            print(f"{result['page']} ({ptype}, {pstatus})")
            if not result["coverage"]:
                print("    no anchors — the page governs no code directly")
            for cov in result["coverage"]:
                print(f"    anchors {cov['repo']} {cov['path']} — "
                      f"{cov['files']} measured file(s)")
            return 0
        print(f"{result['target']} ({result['repo']})")
        if not result["governing"]:
            print("    no governing page — asked, none governs")
        for gov in result["governing"]:
            ptype, pstatus = gov["meta"]
            suffix = f" ({ptype}, {pstatus})" if ptype or pstatus else ""
            print(f"    governed by {gov['page']}{suffix}")
            for rel in gov["relations"]:
                rmeta = rel["meta"]
                rsuffix = f" ({rmeta[0]}, {rmeta[1]})" if rmeta else ""
                print(f"        {rel['rel']} {rel['to']}{rsuffix}")
        return 0

    if op == "diff":
        if _enola_bin() is None or not ENOLA_CONFIG.exists():
            print("enola: absent on this machine — skipping "
                  "architecture drift check")
            return 0
        if not ENOLA_RECEIPTS.exists():
            print("enola: no recorded receipts yet — run "
                  "`brain.py enola generate` to baseline")
            return 0
        recorded = json.loads(ENOLA_RECEIPTS.read_text())
        digests = _enola_content_digests()
        for repo_path in _enola_repos():
            name = repo_path.name
            live = _enola_live_receipt(repo_path)
            prior = recorded.get(name)
            if live is None:
                print(f"enola: {name}: no live snapshot "
                      "(regenerate to compare)")
                continue
            if prior is None:
                print(f"enola: {name}: unrecorded "
                      f"({live.get('fact_count')} facts)")
                continue
            live_digest = digests.get(name)
            if live_digest and prior.get("content_digest"):
                if live_digest == prior["content_digest"]:
                    print(f"enola: {name}: unchanged")
                    continue
            elif live.get("snapshot_id") == prior.get("snapshot_id"):
                print(f"enola: {name}: unchanged")
                continue
            delta = (live.get("fact_count") or 0) - (prior.get("fact_count") or 0)
            print(f"enola: {name}: DRIFTED "
                  f"({prior.get('fact_count')} → {live.get('fact_count')} "
                  f"facts, {'+' if delta >= 0 else ''}{delta}; "
                  f"{(prior.get('git_commit') or '')[:8]} → "
                  f"{(live.get('git', {}).get('commit') or '')[:8]})")
        return 0

    if op == "citations":
        citations = _enola_wiki_citations()
        if not ENOLA_RECEIPTS.exists():
            print("enola: no recorded receipts — repo verdicts degrade "
                  "to unknown-repo", file=sys.stderr)
        for c in citations:
            digest = f" sha256:{c['digest']}…" if c["digest"] else ""
            repo = c["repo"] or "(unparsed)"
            print(f"enola-citation: {c['verdict']:12s} "
                  f"{c['page']}:{c['line']} {repo}{digest}")
        counts = {}
        for c in citations:
            counts[c["verdict"]] = counts.get(c["verdict"], 0) + 1
        print(f"# {len(citations)} citation(s): "
              + (", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
                 or "none"), file=sys.stderr)
        return 0

    if op == "trend":
        # Findings themselves are machine-local by design (the consumption
        # ADR's pull-only no-go), but each generate records a per-repo
        # insight_count into receipts.json, and receipts.json is committed.
        # So git history already holds the series — this reads it out.
        # /sync step 1b asks for a sentence when the count has moved
        # sharply; before this existed that instruction could only be
        # followed by hand-rolling git archaeology, so in practice it was
        # not followed at all.
        limit = getattr(args, "last", None) or 10
        repo_filter = getattr(args, "repo", None)
        rev = subprocess.run(
            ["git", "log", f"-{limit}", "--format=%H %ad", "--date=short",
             "--", str(ENOLA_RECEIPTS.relative_to(REPO))],
            cwd=REPO, capture_output=True, text=True,
        )
        if rev.returncode != 0 or not rev.stdout.strip():
            print("enola: no committed receipts history — the graph was "
                  "not asked (nothing to trend)", file=sys.stderr)
            return 0
        series = []
        for line in rev.stdout.strip().splitlines():
            sha, _, date = line.partition(" ")
            blob = subprocess.run(
                ["git", "show", f"{sha}:{ENOLA_RECEIPTS.relative_to(REPO)}"],
                cwd=REPO, capture_output=True, text=True,
            )
            if blob.returncode != 0:
                continue
            try:
                recorded = json.loads(blob.stdout)
            except json.JSONDecodeError:
                continue
            counts = {
                name: entry.get("insight_count") or 0
                for name, entry in recorded.items()
                if isinstance(entry, dict)
                and (repo_filter is None or name == repo_filter)
            }
            if counts:
                series.append((date, sha[:8], counts))
        if not series:
            print("enola: receipts history carries no insight_count "
                  "(recorded before the field existed)", file=sys.stderr)
            return 0
        # Oldest first so the reader scans forward in time.
        series.reverse()
        repos = sorted({r for _, _, c in series for r in c})
        print(f"# enola finding trend — {len(series)} snapshot(s), "
              f"oldest first")
        for date, sha, counts in series:
            total = sum(counts.values())
            per = "  ".join(f"{r}={counts[r]}" for r in repos if r in counts)
            print(f"{date} {sha}  total={total:<5} {per}")
        first_total = sum(series[0][2].values())
        last_total = sum(series[-1][2].values())
        delta = last_total - first_total
        print(f"# {first_total} → {last_total} across the window "
              f"({delta:+d})")
        if len(series) >= 2:
            prev_total = sum(series[-2][2].values())
            step = last_total - prev_total
            moved = [
                f"{r} {series[-2][2].get(r, 0)}→{series[-1][2][r]}"
                for r in series[-1][2]
                if series[-2][2].get(r, 0) != series[-1][2][r]
            ]
            print(f"# since the previous snapshot: {step:+d}"
                  + (f" — {', '.join(moved)}" if moved else " (no repo moved)"))
        return 0

    if op in ("baseline", "check", "coverage", "doctor", "explain",
              "history"):
        return _enola_passthrough(op, args)

    print(f"unknown enola op: {op!r}", file=sys.stderr)
    return 1


def _enola_target(args) -> str:
    """Repo path for a per-repo op, or the cluster config for a whole-graph one.

    enola resolves a directory as a repository and a file as a config, so
    passing the config is how an op speaks for the cluster rather than for
    whichever directory it happened to start in.
    """
    repo = getattr(args, "repo", None)
    if not repo:
        return str(ENOLA_CONFIG)
    return _enola_member_path(repo)


def _enola_member_path(repo: str) -> str | None:
    """The checkout a repo name denotes, or None with a named refusal.

    A name that is neither a cluster member nor a directory used to fall
    through as a bare string, which enola read as a config path, found
    nothing, and then snapshotted the brain's own checkout into `.enola/`
    while reporting on it as if it were the named repo. The wrong answer
    looked like an answer.
    """
    for path in _enola_repos():
        if path.name == repo:
            return str(path)
    candidate = Path(repo).expanduser()
    if candidate.is_dir():
        return str(candidate.resolve())
    known = ", ".join(sorted(p.name for p in _enola_repos()))
    print(f"enola: {repo!r} is not a cluster member in {ENOLA_CONFIG.name} "
          f"and not a directory; known members: {known}", file=sys.stderr)
    return None


def _enola_repo_target(args) -> str | None:
    """Repo path for ops that only mean something inside one checkout.

    `doctor` asks whether this repository's session hooks fired, which a
    cluster config cannot answer — it rejects a config path outright.
    """
    repo = getattr(args, "repo", None)
    if repo:
        return _enola_member_path(repo)
    return str(REPO)


def _enola_passthrough(op: str, args) -> int:
    """Run an enola subcommand and relay it, degrading rather than failing.

    Every graph-dependent step in the brain is allowed to be skipped and
    required to say so, per AGENTS.md § Working with the architecture
    graph. A missing binary is a named skip at exit 0; the tool's own
    exit code is reported in words and deliberately not propagated, so
    `check` grades a change without any caller being able to treat the
    graph as a gate.
    """
    binary = _enola_bin()
    if binary is None:
        print(f"enola: skipped ({op}) — binary not installed on this machine")
        return 0

    argv = [binary]
    if op == "history":
        sub = getattr(args, "history_op", None) or "log"
        argv.append(sub)
        pattern = getattr(args, "pattern", None)
        if sub == "blame" and pattern:
            argv.append(pattern)
        if sub in ("show", "diff") and pattern:
            argv.append(pattern)
    elif op == "explain":
        argv.append("--explain")
    elif op == "baseline":
        argv += ["baseline", getattr(args, "baseline_op", None) or "show"]
    else:
        argv.append(op)

    target = _enola_repo_target(args) if op == "doctor" else _enola_target(args)
    if target is None:
        print(f"enola: skipped ({op}) — no such repository to run it against")
        return 0
    if op == "check" and getattr(args, "repo", None):
        # A per-repo check speaks for the cluster: the binary gets the config
        # (providers, exclusions, output.dir — the same settings the pin was
        # built under) plus the member to grade, so the baseline the pin wrote
        # is the one the check finds and the two sides are built the same way.
        # Handing the bare path instead is how five pushes declined and a
        # sixth "could not run" against an existing pin (the
        # a-check-that-can-grade trail).
        argv += ["-member", target, str(ENOLA_CONFIG)]
    else:
        argv.append(target)

    result = subprocess.run(argv, cwd=REPO, capture_output=True, text=True,
                            env=_enola_env())
    if (op == "check" and result.returncode == 2
            and "flag provided but not defined: -member" in (result.stderr or "")):
        print("enola check: the installed binary predates member grading "
              "(-member ships in newer enola releases); a bare-path check "
              "declines by construction, so this reads as NOT ASKED until "
              "the release lands and the binary is installed")
        return 0
    out = (result.stdout or "").rstrip()
    if out:
        print(out)
    err = (result.stderr or "").rstrip()
    if err and result.returncode != 0:
        print(err[-2000:], file=sys.stderr)

    if op == "check":
        verdict = {0: "clean", 1: "regression", 2: "could not run",
                   3: "declined — snapshots not comparable"}
        print(f"enola check: {verdict.get(result.returncode, result.returncode)}")
        if result.returncode == 3:
            print("enola check: treat as NOT ASKED, never as a pass")
    if op == "doctor":
        # The binary prints no version, so byte comparison is the check. The
        # MCP server holds whatever binary it started with; after an install
        # the two diverge silently, which is how the server answered from
        # 0.4.0 for two days after the disk moved to 0.4.6.
        pinned = _enola_bin()
        installed = Path.home() / ".local" / "bin" / "enola"
        if (pinned and installed.exists()
                and Path(pinned).resolve() != installed.resolve()):
            try:
                skew = Path(pinned).read_bytes() != installed.read_bytes()
            except OSError as e:
                skew = None
                print(f"enola doctor: binary skew unreadable ({e}) — named skip")
            if skew:
                print("enola doctor: the config-pinned binary differs from the "
                      "installed one — sync the copy (cp to a temp name, mv "
                      "over it) and RESTART THE MCP SERVER, which still holds "
                      "the binary it started with")
            elif skew is False:
                print("enola doctor: config-pinned binary and installed binary "
                      "are identical")
    return 0


def _write_json_whole(path: Path, data) -> None:
    # A reader or a crash mid-write sees the old record or the new one, never
    # half of either: sources/notes/tabula-gap-report--2026-09-27.md, 3.1.
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with staged.open("w") as fh:
            fh.write(json.dumps(data, indent=2) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def _effort_path(slug: str) -> Path:
    return EFFORTS_DIR / f"{slug}.json"


def _read_effort(slug: str) -> dict | None:
    p = _effort_path(slug)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def _write_effort(slug: str, record: dict) -> None:
    record["updated"] = dt.datetime.now(dt.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    _write_json_whole(_effort_path(slug), record)


EFFORT_BOUND_UNITS = ("rounds", "minutes")
EFFORT_TOKEN_TIERS = ("strong", "small")


def _effort_bound(text: str) -> dict:
    m = re.fullmatch(r"\s*(\d+)\s+(round|rounds|minute|minutes)\s*", text or "")
    if not m or int(m.group(1)) <= 0:
        raise ValueError(f"bound must be a positive whole number and a unit "
                         f"({' or '.join(EFFORT_BOUND_UNITS)}), e.g. \"90 minutes\"; got {text!r}")
    unit = m.group(2) if m.group(2).endswith("s") else m.group(2) + "s"
    return {"value": int(m.group(1)), "unit": unit,
            "set_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


def _effort_tokens(pairs: list[str]) -> dict:
    summed: dict = {}
    for pair in pairs:
        tier, _, n = pair.partition("=")
        if tier not in EFFORT_TOKEN_TIERS:
            raise ValueError(f"token tier must be one of {', '.join(EFFORT_TOKEN_TIERS)}; got {pair!r}")
        if not re.fullmatch(r"\d+", n) or int(n) <= 0:
            raise ValueError(f"tokens must be a positive whole number; got {pair!r}")
        summed[tier] = summed.get(tier, 0) + int(n)
    return summed


def _effort_bound_label(bound: dict | None) -> str:
    return f"{bound['value']} {bound['unit']}" if bound else "-"


def _list_efforts() -> list[dict]:
    if not EFFORTS_DIR.exists():
        return []
    out = []
    for p in sorted(EFFORTS_DIR.glob("*.json")):
        try:
            out.append(json.loads(p.read_text()))
        except json.JSONDecodeError as e:
            print(f"# malformed effort record at {p}: {e}", file=sys.stderr)
    return out


def cmd_efforts(args) -> int:
    """Manage in-flight effort registry at wiki/_state/efforts/<slug>.json.

    Per-effort JSON files (one per file, never co-mingled) — see
    wiki/brain/adrs/parallel-efforts-on-request.md § Decision for
    the structural rationale.

    Subcommands:
      list                       — all efforts, optionally filtered.
      get <slug>                 — one effort's record as JSON.
      set <slug>                 — create/update a record (used by /spawn).
      mark <slug> <status>       — set status (in-flight | merged |
                                   abandoned | orphaned).

    `set --bound "<n> rounds|minutes"` records the owner's bound and
    `--tokens <tier>=<n>` adds to that tier (strong or small); `resume <slug>
    --bound ...` raises an exhausted owner's bound, keeping the old one in
    bound_history and the owner id unchanged. A bound or token number is
    written only as the caller reports it; a malformed one is refused with
    exit 2 and nothing written.
    """
    op = args.op

    if op == "list":
        records = _list_efforts()
        status_filter = getattr(args, "status", None)
        if status_filter:
            records = [r for r in records if r.get("status") == status_filter]
        as_json = getattr(args, "json", False)
        if as_json:
            print(json.dumps(records, indent=2))
            return 0
        if not records:
            print("# no efforts in registry", file=sys.stderr)
            return 0
        # human-readable table
        for r in records:
            slug = r.get("slug", "?")
            status = r.get("status", "?")
            brain_branch = r.get("brain_branch", "?")
            targets = ",".join(r.get("targets", [])) or "-"
            spawn = r.get("spawned_at", "?")
            owner_state = r.get("owner_state")
            owner_id = r.get("owner_agent_id")
            if owner_state == "none-dispatched":
                owner_cell = "none-dispatched"
            elif owner_state and owner_id:
                owner_cell = f"{owner_state}:{owner_id[:8]}"
            elif owner_state:
                owner_cell = owner_state
            else:
                owner_cell = "-"
            tokens = ",".join(f"{tier}:{n}" for tier, n in sorted((r.get("tokens") or {}).items())) or "-"
            print(
                f"{slug}\t{status}\t{brain_branch}\t"
                f"targets={targets}\towner={owner_cell}\tspawned={spawn}\t"
                f"bound={_effort_bound_label(r.get('bound'))}\ttokens={tokens}"
            )
        return 0

    if op == "get":
        record = _read_effort(args.slug)
        if record is None:
            print(f"no effort record for {args.slug!r}", file=sys.stderr)
            return 1
        print(json.dumps(record, indent=2))
        return 0

    if op == "set":
        try:
            bound = _effort_bound(args.bound) if args.bound is not None else None
            tokens = _effort_tokens(args.tokens or [])
        except ValueError as e:
            print(f"efforts set: {e}; nothing written", file=sys.stderr)
            return 2
        existing = _read_effort(args.slug) or {}
        record = dict(existing)
        record["slug"] = args.slug
        if args.brain_branch:
            record["brain_branch"] = args.brain_branch
        if args.brain_worktree:
            record["brain_worktree"] = args.brain_worktree
        if args.targets is not None:
            record["targets"] = args.targets
        if args.target_branches is not None:
            record["target_branches"] = dict(args.target_branches)
        if args.target_worktrees is not None:
            record["target_worktrees"] = dict(args.target_worktrees)
        if args.brain_pr:
            record["brain_pr"] = args.brain_pr
        if args.target_prs is not None:
            record["target_prs"] = dict(args.target_prs)
        if args.notes:
            record["notes"] = args.notes
        if args.status:
            record["status"] = args.status
        if args.owner_agent_id is not None:
            record["owner_agent_id"] = args.owner_agent_id
        if args.owner_dispatched_at is not None:
            record["owner_dispatched_at"] = args.owner_dispatched_at
        if args.owner_state is not None:
            record["owner_state"] = args.owner_state
        if args.helpers_dispatched is not None:
            record["helpers_dispatched"] = args.helpers_dispatched
        if bound is not None:
            record["bound"] = bound
        if tokens:
            spent = dict(record.get("tokens") or {})
            for tier, n in tokens.items():
                spent[tier] = spent.get(tier, 0) + n
            record["tokens"] = spent
        if "spawned_at" not in record:
            record["spawned_at"] = dt.datetime.now(dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        record.setdefault("status", "in-flight")
        record.setdefault("targets", [])
        _write_effort(args.slug, record)
        print(json.dumps(record, indent=2))
        return 0

    if op == "resume":
        record = _read_effort(args.slug)
        if record is None:
            print(f"efforts resume: no effort record for {args.slug!r}; nothing written", file=sys.stderr)
            return 2
        current = record.get("bound")
        if not current:
            print(f"efforts resume: {args.slug!r} has no bound to raise; record one with "
                  f"`efforts set --bound` at dispatch; nothing written", file=sys.stderr)
            return 2
        try:
            raised = _effort_bound(args.bound)
        except ValueError as e:
            print(f"efforts resume: {e}; nothing written", file=sys.stderr)
            return 2
        if raised["unit"] != current["unit"] or raised["value"] <= current["value"]:
            print(f"efforts resume: the new bound must be larger than "
                  f"{_effort_bound_label(current)} in the same unit; got "
                  f"{_effort_bound_label(raised)}; nothing written", file=sys.stderr)
            return 2
        record["bound_history"] = [*(record.get("bound_history") or []), current]
        record["bound"] = raised
        record["owner_state"] = "active"
        _write_effort(args.slug, record)
        print(json.dumps(record, indent=2))
        return 0

    if op == "mark":
        record = _read_effort(args.slug)
        if record is None:
            print(f"no effort record for {args.slug!r}", file=sys.stderr)
            return 1
        valid = {"in-flight", "merged", "abandoned", "orphaned"}
        if args.status not in valid:
            print(f"status must be one of {sorted(valid)}", file=sys.stderr)
            return 1
        record["status"] = args.status
        _write_effort(args.slug, record)
        print(json.dumps(record, indent=2))
        return 0

    print(f"unknown efforts op: {op!r}", file=sys.stderr)
    return 1


def cmd_rebase(args) -> int:
    """Cheap-rebase the current branch onto origin/main, regenerating
    deterministic auto-files (wiki/_views/) on conflict. Per
    wiki/brain/adrs/parallel-efforts-on-request.md § Decision.

    Steps:
      1. fetch origin
      2. rebase current branch on origin/main
      3. on wiki/_views/ conflict: regenerate via brain.py views and
         git add wiki/_views/, then git rebase --continue
      4. on wiki/index.md or other content conflict: stop and surface;
         the operator resolves by hand
      5. on success: report the rebased commit; force-push is the
         operator's separate step (per the verify-before-chain rule
         in feedback_force_push_verify_commit.md, /rebase deliberately
         does NOT chain the push)
    """
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], REPO)
    if branch in ("main", "master"):
        print(f"refusing to rebase {branch!r} onto origin/main", file=sys.stderr)
        return 1

    print(f"# fetching origin", file=sys.stderr)
    subprocess.run(["git", "fetch", "origin", "--prune"], cwd=REPO, check=True)

    base = args.base or "origin/main"
    print(f"# rebasing {branch} onto {base}", file=sys.stderr)
    rc = subprocess.run(["git", "rebase", base], cwd=REPO).returncode
    if rc == 0:
        head = _git(["rev-parse", "HEAD"], REPO)
        print(f"rebased clean to {head[:8]}", file=sys.stderr)
        print(head)
        return 0

    # rebase paused on conflict — try to auto-resolve wiki/_views/
    while True:
        unmerged = _git(["diff", "--name-only", "--diff-filter=U"], REPO).splitlines()
        if not unmerged:
            break
        views_only = all(p.startswith("wiki/_views/") for p in unmerged if p)
        if not views_only:
            print(
                "# rebase conflict in non-views paths — resolve by hand:",
                file=sys.stderr,
            )
            for p in unmerged:
                print(f"  {p}", file=sys.stderr)
            return 2
        print("# auto-resolving wiki/_views/ via brain.py views", file=sys.stderr)
        # accept theirs first, then regenerate against the merged tree
        for p in unmerged:
            subprocess.run(["git", "checkout", "--theirs", p], cwd=REPO, check=True)
        subprocess.run(
            [sys.executable, str(REPO / "tools" / "brain.py"), "views"],
            cwd=REPO, check=True,
        )
        subprocess.run(["git", "add", "wiki/_views/"], cwd=REPO, check=True)
        rc = subprocess.run(["git", "rebase", "--continue"],
                            cwd=REPO,
                            env={**os.environ, "GIT_EDITOR": "true"}
                            ).returncode
        if rc == 0:
            head = _git(["rev-parse", "HEAD"], REPO)
            print(f"rebased to {head[:8]} (views auto-regenerated)", file=sys.stderr)
            print(head)
            return 0
        # else continue loop — there may be more views conflicts in later commits

    head = _git(["rev-parse", "HEAD"], REPO)
    print(f"rebased to {head[:8]}", file=sys.stderr)
    print(head)
    return 0


BRAIN_HOOK_SCRIPT = '''#!/usr/bin/env bash
# brain:managed:hook version=2
# Pre-tool hook: surface relevant brain pages before sibling-repo source search.
# Installed by ~/projects/brain/tools/brain.py install-sibling.
#
# This file is regenerated by every install pass — if you want to customise,
# fork by removing the `brain:managed:hook` marker on line 1.

set -uo pipefail

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null)

case "$tool_name" in
  Grep|Glob|Read) ;;
  *) exit 0 ;;
esac

REPO="__REPO__"
BRAIN_DIR="${BRAIN_DIR:-$HOME/projects/brain}"

[ -d "$BRAIN_DIR/wiki/$REPO" ] || exit 0

pattern=$(echo "$input" | jq -r '
  .tool_input.pattern //
  .tool_input.glob //
  .tool_input.file_path //
  empty' 2>/dev/null)

[ -z "$pattern" ] && exit 0
[ "${#pattern}" -lt 4 ] && exit 0

# tabula (the Rust tool, a sibling at ../tabula) answers in tens of milliseconds; brain.py takes over a second on a
# thousand pages, so under the half-second budget below it has been timing out
# and this hook has been silent (measured 2026-09-21). Prefer the binary when
# it is built; the Python path stays as the fallback and behaves the same.
RS="${TABULA:-$(dirname "$BRAIN_DIR")/tabula/target/release/tabula}"
if [ -x "$RS" ]; then
  match=$(BRAIN_SCHEMA="$BRAIN_DIR/AGENTS.md" timeout 0.5s "$RS" --root "$BRAIN_DIR" search "$pattern" \\
            --repo "$REPO" --top 1 --json 2>/dev/null \\
            | jq -r '.results[0].path // empty' 2>/dev/null)
elif command -v python3 >/dev/null 2>&1; then
  match=$(timeout 0.5s python3 "$BRAIN_DIR/tools/brain.py" search "$pattern" \\
            --repo "$REPO" --top 1 --json 2>/dev/null \\
            | jq -r '.results[0].path // empty' 2>/dev/null)
fi
if true; then
  if [ -n "$match" ]; then
    cat >&2 <<EOF
[brain] $REPO has synthesis at: $BRAIN_DIR/wiki/$match
        Read it before scanning source — it may answer the question.
EOF
  fi
fi

exit 0
'''


MANAGED_BLOCK_TEMPLATE = '''<!-- brain:managed:start -->

## Brain — synthesis layer for this repo

This repo (`__REPO__`) is described and tracked in **`__BRAIN_DIR__`**, a
local LLM-maintained knowledge base. The brain holds the *why* and *how*
at a level the source alone doesn't surface — architecture, conventions,
decision history (ADRs), in-flight initiatives (PRDs), cross-product
overlaps.

### Read the brain BEFORE searching source

When asked about this repo's architecture, conventions, "why does X work
this way," or any feature spanning multiple files — read brain pages first.
Source code is the implementation; the brain explains the shape.

**Top entry points for `__REPO__`:**

__ENTRY_POINTS__

**Decisions and initiatives:**

- `__BRAIN_DIR__/wiki/__REPO__/adrs/` — accepted ADRs (kind: decision)
- `__BRAIN_DIR__/wiki/__REPO__/prds/` — committed PRDs (kind: initiative)
- `__BRAIN_DIR__/wiki/__REPO__/ai-suggestions/` — agent-authored drafts
  awaiting human review; **not** decisions, **not** product state

### Cross-product context

Decisions affecting multiple repos live at:

- `__BRAIN_DIR__/wiki/org/` — cross-cutting (auth / AI surfaces / CI /
  domain mapping / frontend stacks / runtime topology)
- `__BRAIN_DIR__/wiki/patterns/` — patterns from feedback / observed work
- `__BRAIN_DIR__/wiki/_overlaps/` — surfaced cross-team duplications

### Querying the brain

If `python3 __BRAIN_DIR__/tools/brain.py search '<query>'` is available,
prefer it over manual file walks. It returns ranked pages with title,
kind, confidence, score, excerpt.

### When to write to the brain

The brain has its own write workflow — never edit `__BRAIN_DIR__/wiki/`
directly from this repo. Instead, `cd __BRAIN_DIR__` and use the brain's
slash commands (`/shape`, `/in`, `/capture`).

<!-- brain:managed:manifest version="1" repo="__REPO__" generated="__DATE__" -->
<!-- brain:managed:end -->
'''


def _list_entry_points(brain_dir: Path, repo: str) -> str:
    """Build the bullet list of brain entry points for the repo."""
    repo_dir = brain_dir / "wiki" / repo
    candidates = [
        ("index.md", "repo navigation hub"),
        ("permanent/architecture.md", "durable shape"),
        ("permanent/architecture/index.md", "durable shape (folder hub)"),
        ("permanent/conventions.md", "code style + idioms"),
        ("permanent/conventions/index.md", "code style + idioms (folder hub)"),
        ("permanent/interfaces.md", "external contracts"),
        ("permanent/interfaces/index.md", "external contracts (folder hub)"),
        ("permanent/domain.md", "vocabulary + entities"),
        ("permanent/purpose.md", "what this repo exists for"),
        ("state.md", "Now / Perceived / Target trajectory"),
    ]
    lines = []
    seen_purposes = set()
    for path, label in candidates:
        if (repo_dir / path).exists() and label not in seen_purposes:
            lines.append(f"- `{brain_dir}/wiki/{repo}/{path}` — {label}")
            # collapse duplicates (avoid both architecture.md and architecture/index.md)
            seen_purposes.add(label.split(" (")[0])
    if not lines:
        lines.append(
            f"- `{brain_dir}/wiki/{repo}/` — (skeleton; no top-level pages yet)"
        )
    return "\n".join(lines)


def cmd_scope(args) -> int:
    """tabula scope writes every scope surface (the AGENTS.md tables and the
    config's tier lists this file reads); brain.py no longer rewrites its own
    source. No tabula with the verb is a named refusal, not a silent pass."""
    tabula = os.environ.get("TABULA_BIN") or shutil.which("tabula")
    if not (tabula and os.access(tabula, os.X_OK)) or subprocess.run([tabula, "scope", "--help"], capture_output=True).returncode != 0:
        print("refused: brain.py scope needs a tabula with `scope` (tabula 5fd90bc or later) on PATH or in TABULA_BIN", file=sys.stderr)
        return 2
    argv = [tabula, "--root", str(REPO), "scope", args.op, args.repo]
    if args.op == "add":
        argv += ["--tier", args.tier, "--desc", args.desc]
    else:
        argv += [args.tier]
    if getattr(args, "dry_run", False):
        argv.append("--dry-run")
    return subprocess.run(argv).returncode


def cmd_install_sibling(args) -> int:
    """Install the brain's managed block + PreToolUse hook into a sibling repo.

    Per `wiki/brain/ai-suggestions/prds/sibling-repo-installer.md`.

    Idempotent: re-running updates the managed block in place. Operator-
    authored content outside the sentinel comments is never touched.

    With --uninstall, removes the managed block + hook script + settings
    entry, leaving operator-authored content intact.

    With --all, iterates every active sibling repo on disk (under
    $BRAIN_PROJECTS_ROOT, default ~/projects/).

    With --dry-run, prints what would be written without modifying disk.
    """
    if args.all_active:
        # Walk wiki/<repo>/ folders that have an active shelf; install if
        # the sibling repo is on disk, skip with a note otherwise.
        repos = []
        for child in sorted(WIKI.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("_") or child.name in {"org", "brain", "insights"}:
                continue
            if (child / "index.md").exists() and (PROJECTS / child.name).exists():
                repos.append(child.name)
        if not repos:
            print("no active sibling repos found on disk", file=sys.stderr)
            return 0
        rc = 0
        for repo in repos:
            print(f"\n--- {repo} ---", file=sys.stderr)
            args.repo = repo
            args.all_active = False
            r = cmd_install_sibling(args)
            if r != 0:
                rc = r
        return rc

    if not args.repo:
        print("repo argument required (or --all)", file=sys.stderr)
        return 2

    repo = args.repo
    sibling_root = PROJECTS / repo
    if not sibling_root.exists():
        print(f"sibling repo not found: {sibling_root}", file=sys.stderr)
        return 1
    if not (sibling_root / ".git").exists():
        print(f"warning: {sibling_root} has no .git directory", file=sys.stderr)

    brain_dir = REPO

    today = today_utc().isoformat()

    # Prefer CLAUDE.md, fall back to AGENTS.md, else create CLAUDE.md.
    claude_md = sibling_root / "CLAUDE.md"
    agents_md = sibling_root / "AGENTS.md"
    if claude_md.exists():
        target = claude_md
    elif agents_md.exists():
        target = agents_md
    else:
        target = claude_md

    # Render the managed block
    entry_points = _list_entry_points(brain_dir, repo)
    block = (
        MANAGED_BLOCK_TEMPLATE
        .replace("__REPO__", repo)
        .replace("__BRAIN_DIR__", str(brain_dir))
        .replace("__ENTRY_POINTS__", entry_points)
        .replace("__DATE__", today)
    )

    # Splice into the target file
    if args.uninstall:
        if not target.exists():
            print(f"nothing to uninstall: {target} does not exist", file=sys.stderr)
            return 0
        text = target.read_text()
        m = re.search(
            r"\n*<!-- brain:managed:start -->.*?<!-- brain:managed:end -->\n*",
            text, re.DOTALL,
        )
        if not m:
            print(f"no managed block found in {target}", file=sys.stderr)
            new_text = text
        else:
            new_text = text[:m.start()] + "\n" + text[m.end():]
            new_text = re.sub(r"\n{3,}", "\n\n", new_text)
        if args.dry_run:
            print(f"[dry-run] would update: {target}", file=sys.stderr)
        else:
            target.write_text(new_text)
            print(f"updated: {target} (managed block removed)", file=sys.stderr)
    else:
        text = target.read_text() if target.exists() else f"# {repo}\n\nSibling-repo Claude Code instructions. See managed block below.\n\n"
        if "<!-- brain:managed:start -->" in text:
            new_text = re.sub(
                r"<!-- brain:managed:start -->.*?<!-- brain:managed:end -->",
                block.strip(),
                text, count=1, flags=re.DOTALL,
            )
        else:
            new_text = text.rstrip() + "\n\n" + block + "\n"
        if args.dry_run:
            print(f"[dry-run] would update: {target}", file=sys.stderr)
        else:
            target.write_text(new_text)
            print(f"updated: {target}", file=sys.stderr)

    # Hook script
    claude_dir = sibling_root / ".claude"
    hook_path = claude_dir / "brain-hook.sh"
    if args.uninstall:
        if hook_path.exists():
            if args.dry_run:
                print(f"[dry-run] would remove: {hook_path}", file=sys.stderr)
            else:
                hook_path.unlink()
                print(f"removed: {hook_path}", file=sys.stderr)
    else:
        hook_content = BRAIN_HOOK_SCRIPT.replace("__REPO__", repo)
        if args.dry_run:
            print(f"[dry-run] would write: {hook_path}", file=sys.stderr)
        else:
            claude_dir.mkdir(exist_ok=True)
            hook_path.write_text(hook_content)
            os.chmod(hook_path, 0o755)
            print(f"wrote: {hook_path}", file=sys.stderr)

    # settings.json registration
    settings_path = claude_dir / "settings.json"
    if args.uninstall:
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text())
            except json.JSONDecodeError:
                print(f"warning: {settings_path} unparseable; not modifying", file=sys.stderr)
                return 0
            hooks = (settings.get("hooks") or {}).get("PreToolUse") or []
            hooks_filtered = [
                h for h in hooks
                if not _entry_calls_brain_hook(h)
            ]
            if len(hooks_filtered) != len(hooks):
                if args.dry_run:
                    print(f"[dry-run] would update: {settings_path}", file=sys.stderr)
                else:
                    settings.setdefault("hooks", {})["PreToolUse"] = hooks_filtered
                    if not hooks_filtered:
                        settings["hooks"].pop("PreToolUse", None)
                        if not settings["hooks"]:
                            settings.pop("hooks", None)
                    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
                    print(f"updated: {settings_path} (hook entry removed)", file=sys.stderr)
    else:
        if settings_path.exists():
            try:
                settings = json.loads(settings_path.read_text())
            except json.JSONDecodeError:
                print(f"warning: {settings_path} unparseable; refusing to modify", file=sys.stderr)
                return 1
        else:
            settings = {}
        hooks_section = settings.setdefault("hooks", {})
        pre_hooks = hooks_section.setdefault("PreToolUse", [])
        already = any(_entry_calls_brain_hook(h) for h in pre_hooks)
        if not already:
            pre_hooks.append({
                "matcher": "Grep|Glob|Read",
                "hooks": [
                    {
                        "type": "command",
                        "command": str(hook_path),
                    }
                ],
            })
            if args.dry_run:
                print(f"[dry-run] would update: {settings_path}", file=sys.stderr)
            else:
                claude_dir.mkdir(exist_ok=True)
                settings_path.write_text(json.dumps(settings, indent=2) + "\n")
                print(f"updated: {settings_path} (hook entry added)", file=sys.stderr)
        else:
            print(f"already registered: {settings_path}", file=sys.stderr)

    return 0


def cmd_verify_claims(args) -> int:
    """Extract verifiable claims from a wiki page + emit a structured
    manifest the consumer (agent / operator / LLM) can verify against
    the cited sibling-repo source.

    Per `wiki/brain/ai-suggestions/prds/scheduled-operations-and-tracking.md`
    open question §4 + the operator's 2026-05-08 directive on brain↔repo
    semantic verification.

    Three claim types extracted:

    1. **Path claims** — `~/projects/<repo>/<path>` references with
       optional `:<line>` or `:<line>-<line>` suffixes. Mechanical
       check: file exists; line range valid.
    2. **Version-pin claims** — patterns like `Pundit 2.5.2`,
       `Rails 8.1.3`, `Bun 1.0`. Mechanical check: defer (would need
       per-language manifest parsing); flagged for LLM grounding.
    3. **Identifier claims** — backticked tokens that look like
       class / module / function names appearing alongside a cited
       file path. Flagged for LLM verification.

    Output: JSON manifest with one entry per claim + a status:
    `verified` (mechanical pass) / `failed` (mechanical fail) /
    `needs-verification` (semantic — agent / LLM must read the cited
    file and judge). The LLM verifier reads the manifest, opens each
    cited file with the Read tool, and updates the status.

    The consumer runs:
        python3 tools/brain.py verify-claims <page> --json > manifest.json
        # then an LLM agent reads manifest.json, opens each cited file,
        # and produces a verified/failed verdict per claim.
    """
    page = args.page
    abs_page = (WIKI / page).resolve()
    try:
        abs_page.relative_to(WIKI)
    except ValueError:
        print(f"path escapes wiki/: {page}", file=sys.stderr)
        return 2
    if not abs_page.exists():
        print(f"page not found: {page}", file=sys.stderr)
        return 2

    parsed = parse(abs_page)
    if parsed is None:
        print(f"page has no parseable frontmatter: {page}", file=sys.stderr)
        return 2
    meta, body = parsed

    claims: list[dict] = []
    seen: set[tuple] = set()

    # Path claims with optional :line suffix.
    # Lookahead deliberately excludes `.` so file extensions like
    # `.md`/`.rb`/`.ts` aren't truncated. Sentence-end periods get
    # captured into the path; that's a heuristic-acceptable edge case
    # — the path-existence check normalises by stripping trailing
    # punctuation before resolving.
    path_rx = re.compile(
        r"~/projects/([\w-]+)/([\w./_-]+?)(?::(\d+)(?:-(\d+))?)?(?=[\s`)\],]|$)",
        re.MULTILINE,
    )
    for m in path_rx.finditer(body):
        repo = m.group(1)
        rel_path = m.group(2).rstrip(".,")  # strip trailing sentence punctuation
        line_start = int(m.group(3)) if m.group(3) else None
        line_end = int(m.group(4)) if m.group(4) else None
        key = ("path", repo, rel_path, line_start, line_end)
        if key in seen:
            continue
        seen.add(key)
        # Capture surrounding context (~80 chars on each side)
        ctx_start = max(0, m.start() - 80)
        ctx_end = min(len(body), m.end() + 80)
        context = body[ctx_start:ctx_end].replace("\n", " ").strip()
        # Mechanical check
        sibling = PROJECTS / repo
        status = "needs-verification"
        mechanical = {}
        if not sibling.exists():
            mechanical["sibling_on_disk"] = False
            status = "needs-verification"
        else:
            mechanical["sibling_on_disk"] = True
            target = sibling / rel_path
            mechanical["file_exists"] = target.exists()
            if not target.exists():
                status = "failed"
            else:
                if line_start is not None:
                    try:
                        line_count = sum(1 for _ in target.open())
                        mechanical["file_line_count"] = line_count
                        in_range = line_start <= line_count and (
                            line_end is None or line_end <= line_count
                        )
                        mechanical["lines_in_range"] = in_range
                        if not in_range:
                            status = "failed"
                        else:
                            status = "needs-verification"
                    except (OSError, UnicodeDecodeError):
                        mechanical["file_line_count"] = "(unreadable)"
                        status = "needs-verification"
                else:
                    status = "needs-verification"
        claims.append({
            "type": "path",
            "claim": m.group(0),
            "repo": repo,
            "rel_path": rel_path,
            "line_start": line_start,
            "line_end": line_end,
            "context": context,
            "mechanical": mechanical,
            "status": status,
        })

    # Version-pin claims (Title-cased identifier + space + version-like)
    version_rx = re.compile(
        r"\b([A-Z][\w]{2,})\s+(\d+\.\d+(?:\.\d+)?(?:[a-z]\d+)?)\b"
    )
    for m in version_rx.finditer(body):
        name = m.group(1)
        version = m.group(2)
        # Skip non-software-name false positives (heuristic)
        if name in {"At", "On", "By", "For", "Per", "The", "Section", "Article",
                    "Chapter", "Phase", "Step", "Option", "Ruby"}:
            # "Ruby 4.0.1" is a real claim, but it's already commonly
            # captured at the gemfile-lock level; the false-positive on
            # the word alone is the concern. Drop common short words.
            if name not in {"Ruby"}:
                continue
        key = ("version", name, version)
        if key in seen:
            continue
        seen.add(key)
        ctx_start = max(0, m.start() - 80)
        ctx_end = min(len(body), m.end() + 80)
        context = body[ctx_start:ctx_end].replace("\n", " ").strip()
        claims.append({
            "type": "version-pin",
            "claim": m.group(0),
            "name": name,
            "version": version,
            "context": context,
            "mechanical": {"reason": "version-pin requires manifest-walk verification"},
            "status": "needs-verification",
        })

    # Identifier claims — backticked code-shaped tokens within ~120
    # chars of a path claim. These are most likely class/module/method
    # names worth verifying via Grep/Read.
    if claims:  # only if we found path claims
        path_indices = [(c["context"], c["repo"], c["rel_path"])
                        for c in claims if c["type"] == "path"]
        ident_rx = re.compile(r"`([A-Z][\w]+(?:::[A-Z][\w]+)*|[a-z_][\w]+(?:#[\w_]+)?)`")
        for context, repo, rel in path_indices[:50]:  # cap to avoid combinatorial blowup
            for m in ident_rx.finditer(context):
                ident = m.group(1)
                if ident in {"AGENTS.md", "CLAUDE.md", "README.md"}:
                    continue
                key = ("ident", repo, rel, ident)
                if key in seen:
                    continue
                seen.add(key)
                claims.append({
                    "type": "identifier",
                    "claim": ident,
                    "near_path": f"~/projects/{repo}/{rel}",
                    "context": context[:200],
                    "mechanical": {"reason": "identifier verification requires Read/Grep"},
                    "status": "needs-verification",
                })

    receipt_status = {"verified": "verified", "stale": "failed",
                      "malformed": "failed",
                      "unknown-repo": "needs-verification"}
    for c in _enola_wiki_citations():
        if c["page"] != page:
            continue
        claims.append({
            "type": "receipt",
            "claim": f"enola receipt {c['repo']} sha256:{c['digest']}…"
                     if c["digest"] else "enola receipt (unparsed)",
            "context": f"{c['page']}:{c['line']}",
            "mechanical": {"verdict": c["verdict"]},
            "status": receipt_status[c["verdict"]],
        })

    # PR-state claims — "#12345 merged/shipped/open" style. Verified
    # through `gh` when the network and CLI are present; degrades to
    # needs-verification otherwise, mirroring check --no-net. Per
    # wiki/brain/claim-verification.md ("X shipped / merged" row).
    pr_rx = re.compile(
        r"\[?#(\d{4,6})\]?[^\n]{0,80}?\b(merged|shipped|landed|open|closed|unmerged)\b"
        r"|\b(merged|shipped|landed|open|closed|unmerged)\b[^\n]{0,80}?\[?#(\d{4,6})\]?",
        re.IGNORECASE,
    )
    gh_ok = shutil.which("gh") is not None and not getattr(args, "no_net", False)
    # PR numbers are only unambiguous on the repo's own shelf; a
    # "#127 merged" on one repo's shelf must not resolve against another.
    # Only the shelf named by BRAIN_PR_REPO is verified through `gh`.
    pr_repo = page.split("/", 1)[0]
    gh_ok = gh_ok and bool(os.environ.get("BRAIN_PR_REPO")) \
        and pr_repo == os.environ.get("BRAIN_PR_REPO")
    for m in pr_rx.finditer(body):
        number = m.group(1) or m.group(4)
        word = (m.group(2) or m.group(3)).lower()
        key = ("pr-state", number, word)
        if key in seen:
            continue
        seen.add(key)
        ctx = body[max(0, m.start() - 60):m.end() + 60].replace("\n", " ").strip()
        entry = {"type": "pr-state", "claim": f"#{number} {word}",
                 "repo": pr_repo, "context": ctx,
                 "mechanical": {}, "status": "needs-verification"}
        if gh_ok and (PROJECTS / pr_repo).is_dir():
            out = subprocess.run(
                ["gh", "pr", "view", number, "--json", "state,mergedAt"],
                cwd=PROJECTS / pr_repo, capture_output=True, text=True,
                timeout=30)
            if out.returncode == 0:
                state = json.loads(out.stdout)
                entry["mechanical"] = {"state": state["state"],
                                       "merged_at": state.get("mergedAt")}
                claims_merged = word in ("merged", "shipped", "landed")
                is_merged = state["state"] == "MERGED"
                if claims_merged == is_merged:
                    entry["status"] = "verified"
                elif word in ("open", "unmerged") and state["state"] == "OPEN":
                    entry["status"] = "verified"
                else:
                    entry["status"] = "failed"
            else:
                entry["mechanical"] = {"reason": "gh lookup failed (issue number, "
                                                 "cross-repo, or offline)"}
        else:
            entry["mechanical"] = {"reason": "gh or network unavailable"}
        claims.append(entry)

    summary = {
        "page": page,
        "title": meta.get("title", ""),
        "kind": meta.get("kind"),
        "status": meta.get("status"),
        "confidence": meta.get("confidence"),
        "updated": str(meta.get("updated", "")),
        "extracted_at": today_utc().isoformat(),
        "claim_count": len(claims),
        "by_status": {
            "verified": sum(1 for c in claims if c["status"] == "verified"),
            "failed": sum(1 for c in claims if c["status"] == "failed"),
            "needs-verification": sum(1 for c in claims if c["status"] == "needs-verification"),
        },
        "by_type": {
            t: sum(1 for c in claims if c["type"] == t)
            for t in ("path", "version-pin", "identifier", "receipt")
        },
        "claims": claims,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"# Verify claims — {page}")
        print(f"Title: {meta.get('title', '')}")
        print(f"Kind: {meta.get('kind')}; status: {meta.get('status')}; "
              f"confidence: {meta.get('confidence')}")
        print(f"Extracted {summary['claim_count']} claim(s):")
        print(f"  by status: {summary['by_status']}")
        print(f"  by type:   {summary['by_type']}")
        print()
        for c in claims:
            marker = {"verified": "✓", "failed": "✗", "needs-verification": "?"}[c["status"]]
            print(f"  {marker} [{c['type']}] {c['claim']}")
            if c["status"] == "failed":
                print(f"      ✗ {c['mechanical']}")
        print()
        print("(Re-run with --json for the full structured manifest. "
              "Hand the JSON to an LLM agent to verify "
              "`needs-verification` claims by reading each cited file.)")
    return 0 if all(c["status"] != "failed" for c in claims) else 1


def _attention_store_path():
    return ATTENTION_DIR / "cards.json"


def _attention_load_store() -> dict:
    path = _attention_store_path()
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            pass
    return {"_schema": "v1", "generated": None, "cards": []}


def _attention_collect() -> list[dict]:
    """Deterministic collectors only — judgment fields stay empty for
    the `attention` skill to fill. Per wiki/brain/adrs/attention-dashboard.md."""
    today = today_utc().isoformat()
    cards: list[dict] = []

    def card(cid, kind, title, command, sources, why=""):
        cards.append({
            "id": cid, "kind": kind, "title": title, "why": why,
            "tier": "untriaged", "command": command, "sources": sources,
            "status": "new", "first_seen": today, "last_seen": today,
            "origin": "collector",
        })

    if EFFORTS_DIR.exists():
        for f in sorted(EFFORTS_DIR.glob("*.json")):
            try:
                rec = json.loads(f.read_text())
            except json.JSONDecodeError:
                continue
            if rec.get("status") != "in-flight":
                continue
            slug = rec.get("slug", f.stem)
            card(f"effort:{slug}", "effort",
                 f"In-flight effort: {slug}",
                 f"/continue {slug}",
                 [str(f.relative_to(REPO))] +
                 [v for v in (rec.get("artifacts") or {}).values()])

    try:
        out = subprocess.run(
            ["gh", "pr", "list", "--state", "open",
             "--json", "number,title,isDraft"],
            capture_output=True, text=True, timeout=30, cwd=REPO)
        if out.returncode == 0:
            origin = _origin_https()
            for pr in json.loads(out.stdout or "[]"):
                n = pr["number"]
                draft = " (draft)" if pr.get("isDraft") else ""
                card(f"pr:brain#{n}", "decision-needed",
                     f"Open brain PR #{n}{draft}: {pr['title']}",
                     f"/review {n}",
                     [f"{origin}/pull/{n}"] if origin else [])
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass

    ai_files = []
    for d in WIKI.glob("**/ai-suggestions/*/"):
        ai_files.extend(d.glob("*.md"))
    pending = [f for f in ai_files
               if (parse(f) or ({},))[0].get("status") == "suggested"]
    if pending:
        card("backlog:ai-suggestions", "decision-needed",
             f"{len(pending)} AI suggestion(s) awaiting graduation review",
             "review wiki/_views/ai-suggestions.md, then /shape graduation",
             ["wiki/_views/ai-suggestions.md"])

    groom_state = WIKI / "_state" / "ai-suggestion-grooming.json"
    if groom_state.exists():
        try:
            g = json.loads(groom_state.read_text())
            if g.get("stale_count"):
                card("backlog:stale-suggestions", "decision-needed",
                     f"{g['stale_count']} AI suggestion(s) past the "
                     f"{g.get('threshold_days', 180)}-day staleness threshold",
                     "/groom",
                     [str(groom_state.relative_to(REPO))])
        except json.JSONDecodeError:
            pass

    eu_state = WIKI / "_state" / "eu-ai-act.json"
    if eu_state.exists():
        try:
            eu = json.loads(eu_state.read_text())
            deadline = eu.get("deadline")
            if deadline:
                days = (dt.date.fromisoformat(deadline) - today_utc()).days
                if 0 <= days <= 60:
                    card("deadline:eu-ai-act", "direction",
                         f"EU AI Act applies in {days} day(s) ({deadline})",
                         "/ask what EU AI Act gaps remain open?",
                         [str(eu_state.relative_to(REPO)),
                          "wiki/org/eu-ai-act.md"])
        except (json.JSONDecodeError, ValueError):
            pass

    issues_state = WIKI / "_state" / "issues.json"
    if issues_state.exists():
        try:
            iss = json.loads(issues_state.read_text())
            for repo, counts in (iss.get("repos") or {}).items():
                if not isinstance(counts, dict):
                    continue
                crit = counts.get("critical_open") or 0
                blocking = counts.get("blocking") or 0
                if crit or blocking:
                    card(f"issues:{repo}", "incident",
                         f"{repo}: {crit} critical / {blocking} blocking "
                         "issue(s) open",
                         f"/ask what are the open critical issues in {repo}?",
                         [str(issues_state.relative_to(REPO))])
        except json.JSONDecodeError:
            pass

    return cards


BEHAVIOURAL_VERBS_RX = re.compile(
    r"\b(shipped|merged|unpushed|deployed|promoted|rolled out|"
    r"live since|running since|sampling|is live|went live|is running)\b",
    re.IGNORECASE,
)
UNVERIFIED_MARKER_RX = re.compile(r"\(unverified, \d{4}-\d{2}-\d{2}\)")


def _attention_verify(store) -> int:
    """Lint behavioural claims on active cards, per
    wiki/brain/claim-verification.md: a card `why`/`title` using a
    behavioural verb must carry a `verified` stanza (method, source,
    date) or the explicit `(unverified, YYYY-MM-DD)` marker. Marking
    is always acceptable; unmarked inference never is.
    """
    offenders = []
    for c in store["cards"]:
        if c.get("status") not in ("active", "new"):
            continue
        text = f"{c.get('title', '')} {c.get('why', '')}"
        hits = sorted({m.group(0).lower()
                       for m in BEHAVIOURAL_VERBS_RX.finditer(text)})
        if not hits:
            continue
        stanza = c.get("verified")
        stanza_ok = (isinstance(stanza, dict)
                     and all(stanza.get(k) for k in ("method", "source", "date")))
        if stanza_ok or UNVERIFIED_MARKER_RX.search(text):
            continue
        offenders.append((c.get("id", "?"), hits))
    if offenders:
        print(f"attention verify: {len(offenders)} card(s) carry "
              "behavioural claims with no `verified` stanza and no "
              "`(unverified, YYYY-MM-DD)` marker "
              "(wiki/brain/claim-verification.md):")
        for cid, hits in offenders:
            print(f"  {cid} — {', '.join(hits)}")
        return 1
    print("attention verify: all behavioural claims verified or marked")
    return 0


def cmd_pr_sweep(args) -> int:
    """Every review surface of a sibling-repo PR in one call, per
    wiki/brain/claim-verification.md: inline review comments, reviews,
    issue comments, CI rollup and mergeable state. A verdict issued
    without this sweep read the body and diff alone, and can miss an
    inline comment.
    """
    repo, pr = args.repo, args.pr
    sibling = PROJECTS / repo
    if not sibling.is_dir():
        print(f"pr-sweep: no sibling checkout at {sibling}", file=sys.stderr)
        return 2

    def gh(*argv):
        out = subprocess.run(["gh", *argv], cwd=sibling,
                             capture_output=True, text=True, timeout=60)
        return out.stdout if out.returncode == 0 else None

    slug = gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
    if slug is None:
        print("pr-sweep: gh unavailable or repo unresolvable", file=sys.stderr)
        return 2
    slug = slug.strip()

    meta = gh("pr", "view", str(pr), "--json",
              "state,isDraft,mergeable,reviewDecision,mergedAt,title")
    if meta is None:
        print(f"pr-sweep: {slug}#{pr} not found", file=sys.stderr)
        return 2
    m = json.loads(meta)
    print(f"{slug}#{pr} — {m['title']}")
    print(f"  state={m['state']} draft={m['isDraft']} "
          f"mergeable={m['mergeable']} review={m['reviewDecision']} "
          f"merged={m.get('mergedAt') or '-'}")

    rollup = gh("pr", "view", str(pr), "--json", "statusCheckRollup")
    if rollup:
        checks = json.loads(rollup)["statusCheckRollup"] or []
        fails = [c for c in checks if (c.get("conclusion") or "") == "FAILURE"]
        pending = [c for c in checks
                   if (c.get("status") or "") in ("IN_PROGRESS", "QUEUED")
                   or (c.get("state") or "") == "PENDING"]
        print(f"  checks: {len(checks)} total, {len(fails)} failed, "
              f"{len(pending)} running"
              + (f" — failed: {', '.join(str(c.get('name') or c.get('context')) for c in fails)}"
                 if fails else ""))

    surfaces = [
        ("inline review comments", f"repos/{slug}/pulls/{pr}/comments",
         lambda e: f"{e['user']['login']} {e['created_at']} "
                   f"{e.get('path')}:{e.get('line') or e.get('original_line')}\n"
                   f"    {e['body']}"),
        ("reviews", f"repos/{slug}/pulls/{pr}/reviews",
         lambda e: f"{e['user']['login']} {e['state']} {e.get('submitted_at')}"
                   + (f"\n    {e['body']}" if e.get("body") else "")),
        ("issue comments", f"repos/{slug}/issues/{pr}/comments",
         lambda e: f"{e['user']['login']} {e['created_at']}\n    {e['body']}"),
    ]
    for label, endpoint, fmt in surfaces:
        raw = gh("api", endpoint)
        if raw is None:
            print(f"  {label}: (fetch failed)")
            continue
        entries = json.loads(raw)
        print(f"  {label}: {len(entries)}")
        for e in entries:
            body = fmt(e)
            if args.full:
                print(f"    - {body}")
            else:
                first = body.splitlines()
                head = first[0]
                rest = " ".join(line.strip() for line in first[1:])[:200]
                print(f"    - {head}" + (f" | {rest}" if rest else ""))
    return 0


def cmd_attention(args) -> int:
    """Refresh the attention card store (mechanical collectors only).

    Merges freshly collected cards into wiki/_state/attention/cards.json,
    preserving lifecycle status, first_seen, and groom-authored judgment
    fields across refreshes. Dismissed cards persist as tombstones and
    are never resurrected. Per wiki/brain/adrs/attention-dashboard.md.
    """
    op = getattr(args, "op", "refresh") or "refresh"
    store = _attention_load_store()
    today = today_utc().isoformat()

    if op == "list":
        for c in store["cards"]:
            print(f"{c['status']:9s} {c['tier']:9s} {c['kind']:15s} "
                  f"{c['id']:40s} {c['title'][:60]}")
        return 0

    if op == "verify":
        return _attention_verify(store)

    if op != "refresh":
        print(f"unknown attention op: {op!r}", file=sys.stderr)
        return 2

    existing = {c["id"]: c for c in store["cards"]}
    collected = _attention_collect()
    collected_ids = {c["id"] for c in collected}

    merged: list[dict] = []
    for new_card in collected:
        old = existing.pop(new_card["id"], None)
        if old is None:
            merged.append(new_card)
            continue
        if old["status"] == "dismissed":
            old["last_seen"] = today
            merged.append(old)
            continue
        old["title"] = new_card["title"]
        old["sources"] = new_card["sources"]
        old["last_seen"] = today
        if old["status"] == "gone":
            old["status"] = "new"
        if not old.get("why"):
            old["why"] = new_card["why"]
        if (old.get("tier") not in ATTENTION_TIERS
                or old.get("origin", "groom") != "groom"):
            old.setdefault("tier", "untriaged")
        merged.append(old)

    for leftover in existing.values():
        # Missing origin means groom-authored: the skill writes cards the
        # collectors know nothing about, so an absent key must never read
        # as "collector" here or the refresh would reap the groom's own
        # work. Indexing this directly crashed the scheduled run daily
        # from 2026-07-30 (KeyError: 'origin').
        if (leftover.get("origin", "groom") == "collector"
                and leftover["id"] not in collected_ids
                and leftover["status"] in ("new", "active")):
            leftover["status"] = "gone"
        merged.append(leftover)

    ATTENTION_DIR.mkdir(parents=True, exist_ok=True)
    store["cards"] = merged
    store["generated"] = today
    _attention_store_path().write_text(json.dumps(store, indent=2) + "\n")
    counts = collections.Counter(c["status"] for c in merged)
    print(f"attention: {len(merged)} cards "
          f"({', '.join(f'{v} {k}' for k, v in sorted(counts.items()))})")
    return 0


def write_attention_view(views_dir, today) -> None:
    store = _attention_load_store()
    active = [c for c in store["cards"] if c["status"] in ("new", "active")]
    by_tier: dict[str, list[dict]] = collections.defaultdict(list)
    for c in active:
        tier = c["tier"] if c["tier"] in ATTENTION_TIERS else "untriaged"
        by_tier[tier].append(c)

    lines = [
        "---",
        "title: Attention board",
        "kind: meta",
        "status: living",
        f"updated: {today}",
        "confidence: high",
        "sources:",
        "  - tools/brain.py",
        "  - wiki/_state/attention/cards.json",
        "---",
        "",
        "# Attention board",
        "",
        "Auto-generated by `python tools/brain.py views` from "
        "`wiki/_state/attention/cards.json`. Do not edit by hand. "
        "Groomed by the `attention` skill; refreshed mechanically by "
        "`brain.py attention refresh`.",
        "",
        f"Store generated: {store.get('generated') or 'never'}. "
        f"{len(active)} active card(s).",
        "",
    ]
    tier_titles = {"now": "Now", "next": "Next", "watch": "Watch",
                   "untriaged": "Untriaged (awaiting groom)"}
    for tier in ATTENTION_TIERS:
        if not by_tier.get(tier):
            continue
        lines.append(f"## {tier_titles[tier]}")
        lines.append("")
        for c in sorted(by_tier[tier], key=lambda x: (x["kind"], x["id"])):
            lines.append(f"- **{c['title']}** — `{c['kind']}`")
            if c.get("why"):
                lines.append(f"  - why now: {c['why']}")
            lines.append(f"  - run: `{c['command']}`")
            for s in c.get("sources", [])[:4]:
                lines.append(f"  - source: {s}")
        lines.append("")
    done = sum(1 for c in store["cards"] if c["status"] == "done")
    dismissed = sum(1 for c in store["cards"] if c["status"] == "dismissed")
    gone = sum(1 for c in store["cards"] if c["status"] == "gone")
    lines.append(f"*Lifecycle: {done} done, {dismissed} dismissed, "
                 f"{gone} gone (awaiting prune).*")
    lines.append("")
    (views_dir / "attention.md").write_text("\n".join(lines))


def _schedule_run_attention_refresh() -> int:
    class _A:
        op = "refresh"
    rc = cmd_attention(_A())
    if rc == 0:
        views_dir = WIKI / "_views"
        views_dir.mkdir(exist_ok=True)
        write_attention_view(views_dir, today_utc().isoformat())
        print("attention-refresh: wrote wiki/_views/attention.md")
    return rc


def cmd_status(_args) -> int:
    """Brain-wide status dashboard.

    Reads every wiki/_state/*.json + computes corpus stats; surfaces
    one-line health line per dimension (security / EU AI Act /
    issues / sync / reflection / efforts).

    Per `wiki/brain/ai-suggestions/prds/scheduled-operations-and-tracking.md`.
    """
    state_dir = WIKI / "_state"
    today = today_utc()

    print(f"# Brain status — {today.isoformat()}")
    print()

    # Corpus
    pages = wiki_pages()
    by_kind = collections.Counter()
    by_status = collections.Counter()
    by_confidence = collections.Counter()
    for p in pages:
        parsed = parse(p)
        if parsed:
            meta = parsed[0]
            by_kind[meta.get("kind", "?")] += 1
            by_status[meta.get("status", "?")] += 1
            by_confidence[meta.get("confidence", "?")] += 1
    print(f"corpus: {len(pages)} pages")
    print(f"  by kind: " + ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items())))
    print(f"  by status: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
    print(f"  by confidence: " + ", ".join(f"{k}={v}" for k, v in sorted(by_confidence.items())))
    print()

    # Security
    sec_path = state_dir / "security.json"
    if sec_path.exists():
        try:
            sec = json.loads(sec_path.read_text())
            sweep = sec.get("last_full_sweep") or "(never)"
            scanned = sum(1 for r in sec.get("repos", {}).values() if r.get("last_scan"))
            total = len(sec.get("repos", {}))
            print(f"security: last full sweep = {sweep}; {scanned}/{total} repos scanned")
            if scanned == 0:
                print(f"  (bootstrap pending — see wiki/brain/ai-suggestions/prds/scheduled-operations-and-tracking.md)")
        except json.JSONDecodeError:
            print(f"security: wiki/_state/security.json unparseable")
    else:
        print("security: wiki/_state/security.json absent")
    print()

    # EU AI Act
    eu_path = state_dir / "eu-ai-act.json"
    if eu_path.exists():
        try:
            eu = json.loads(eu_path.read_text())
            deadline = dt.date.fromisoformat(eu.get("deadline", "2026-08-02"))
            days_left = (deadline - today).days
            print(f"eu-ai-act: deadline {deadline.isoformat()} ({days_left} days)")
            print(f"  last assessment: {eu.get('last_assessment')}")
            articles = eu.get("articles", {})
            low = sum(1 for a in articles.values() if a.get("readiness") == "low")
            medium = sum(1 for a in articles.values() if a.get("readiness") == "medium")
            high = sum(1 for a in articles.values() if a.get("readiness") == "high")
            print(f"  per-Article: low={low} medium={medium} high={high}")
            print(f"  verdict: {eu.get('verdict', '(no verdict)')}")
        except (json.JSONDecodeError, ValueError):
            print(f"eu-ai-act: wiki/_state/eu-ai-act.json unparseable")
    else:
        print("eu-ai-act: wiki/_state/eu-ai-act.json absent")
    print()

    # Issues
    iss_path = state_dir / "issues.json"
    if iss_path.exists():
        try:
            iss = json.loads(iss_path.read_text())
            pull = iss.get("last_pull") or "(never)"
            populated = sum(1 for r in iss.get("repos", {}).values() if r.get("last_pull"))
            total = len(iss.get("repos", {}))
            print(f"issues: last pull = {pull}; {populated}/{total} repos populated")
        except json.JSONDecodeError:
            print(f"issues: wiki/_state/issues.json unparseable")
    else:
        print("issues: wiki/_state/issues.json absent")
    print()

    # Sync cursors
    cursor_path = SYNC_CURSORS
    if cursor_path.exists():
        try:
            cursors = json.loads(cursor_path.read_text())
            data = cursors.get("cursors") or cursors
            print(f"sync-cursors: {len(data)} sibling repos tracked")
        except json.JSONDecodeError:
            print(f"sync-cursors: unparseable")
    else:
        print("sync-cursors: absent")
    print(f"scope: {len(ACTIVE_REPOS)} active, {len(REFERENCE_REPOS)} reference, "
          f"{len(FROZEN_REPOS)} frozen")

    # Architecture receipts (enola)
    if ENOLA_RECEIPTS.exists():
        try:
            receipts = json.loads(ENOLA_RECEIPTS.read_text())
            dirty = sum(1 for e in receipts.values() if e.get("git_dirty"))
            newest = max((e.get("generated_at") or "" for e in receipts.values()),
                         default="?")
            print(f"enola: {len(receipts)} repos receipted "
                  f"(newest {newest}"
                  f"{f', {dirty} dirty' if dirty else ''}); "
                  "drift via `brain.py enola diff`")
        except json.JSONDecodeError:
            print("enola: receipts unparseable")
    else:
        print("enola: no receipts (machine-local; run `brain.py enola generate`)")

    # Scheduled-run health. Added 2026-08-01 because its absence is
    # what let the daily pipeline fail for three days unnoticed: the
    # board rendered, the cards were current, and nothing here said
    # the run that produced them had crashed.
    if SCHEDULE_STATE.exists():
        try:
            sched = json.loads(SCHEDULE_STATE.read_text())
            last = sched.get("last_run") or "?"
            failed = sched.get("failed") or []
            age = ""
            try:
                delta = (today_utc() - dt.date.fromisoformat(last)).days
                if delta > 1:
                    age = f", {delta}d stale"
            except ValueError:
                pass
            runs = sched.get("runs")
            missed = ""
            if isinstance(runs, list):
                n = sum(1 for r in runs if isinstance(r, dict) and r.get("kind") == "missed")
                missed = f"; {n} missed day(s) in the last {len(runs)} record(s)"
            if failed:
                print(f"schedule: last run {last}{age}{missed}: "
                      f"{len(failed)} FAILED: {', '.join(failed)}")
            else:
                print(f"schedule: last run {last}{age}{missed}: "
                      f"{len(sched.get('operations') or {})} operations ok")
        except json.JSONDecodeError:
            print("schedule: state unparseable")
    else:
        print("schedule: no run recorded yet "
              "(run `brain.py schedule run-due`)")

    # Finding verdicts. Judged counts only, deliberately: an "N unjudged"
    # row would be the enumeration wiki/brain/adrs/architecture-graph-
    # consumption.md rules out, arriving through a dashboard convention.
    if ENOLA_VERDICTS.exists():
        try:
            entries = json.loads(ENOLA_VERDICTS.read_text()).get("entries") or []
            tally = collections.Counter(e.get("verdict") for e in entries)
            print("enola-verdicts: "
                  + ", ".join(f"{tally.get(kind, 0)} {kind}"
                              for kind in ENOLA_VERDICT_KINDS)
                  + "; findings via `brain.py enola findings`")
        except json.JSONDecodeError:
            print("enola-verdicts: unparseable")

    # Efforts
    if EFFORTS_DIR.exists():
        records = list(EFFORTS_DIR.glob("*.json"))
        print(f"efforts: {len(records)} records in wiki/_state/efforts/")
    else:
        print("efforts: directory absent")

    # AI-suggestions backlog
    ai_dirs = list(WIKI.glob("**/ai-suggestions/*/"))
    ai_files = []
    for d in ai_dirs:
        ai_files.extend(d.glob("*.md"))
    suggested = sum(1 for f in ai_files
                    if (parse(f) or ({},))[0].get("status") == "suggested")
    superseded = sum(1 for f in ai_files
                     if (parse(f) or ({},))[0].get("status") == "superseded")
    print(f"ai-suggestions: {suggested} pending review, {superseded} graduated")

    att = _attention_load_store()
    if att.get("generated"):
        active = [c for c in att["cards"] if c["status"] in ("new", "active")]
        untriaged = sum(1 for c in active if c["tier"] == "untriaged")
        print(f"attention: {len(active)} active card(s), {untriaged} "
              f"untriaged (store generated {att['generated']}; see "
              "wiki/_views/attention.md)")
    else:
        print("attention: store empty (run `brain.py attention refresh`)")
    print()

    print("# Reflection-check (run `brain.py reflection-check` for detail)")
    return 0


def _schedule_run_security_scan() -> int:
    """Manifest-walk inventory across sibling repos.

    Scanner = "manifest-walk" — counts dependency entries in
    `Gemfile.lock`, `package.json`, `requirements.txt`,
    `Cargo.toml`, `go.mod`. Does NOT do CVE checking
    (`bundle audit` / `npm audit` / `trivy` are separate
    follow-ups). Records inventory + last_scan timestamp.
    """
    state_path = WIKI / "_state" / "security.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"_schema": "v1", "repos": {}}
    today = today_utc().isoformat()
    scanned = 0
    for repo, entry in state.get("repos", {}).items():
        sibling = PROJECTS / repo
        if not sibling.exists():
            entry["notes"] = f"(skipped — repo not on disk at {sibling})"
            continue
        manifests = {
            "Gemfile.lock": _count_gemfile_lock,
            "package.json": _count_package_json,
            "package-lock.json": _count_package_lock,
            "requirements.txt": _count_requirements,
            "Cargo.toml": _count_cargo,
            "go.mod": _count_go_mod,
        }
        inventory = {}
        for filename, counter in manifests.items():
            target = sibling / filename
            if target.exists():
                try:
                    inventory[filename] = counter(target)
                except Exception as exc:
                    inventory[filename] = f"(parse error: {exc})"
        entry["last_scan"] = today
        entry["scanner"] = "manifest-walk"
        entry["findings"] = {"critical": 0, "high": 0, "medium": 0, "low": 0,
                             "_note": "inventory only; CVE check not run"}
        entry["inventory"] = inventory
        entry["notes"] = (
            f"manifest-walk scanned {len(inventory)} files; "
            f"CVE check requires `bundle audit` / `npm audit` / `trivy` "
            f"(follow-up)."
        )
        scanned += 1
    state["last_full_sweep"] = today
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"security-scan: scanned {scanned} repo(s); wrote {state_path.relative_to(REPO)}")
    return 0


def _count_gemfile_lock(p: Path) -> int:
    """Count top-level gem entries across all GIT / PATH / GEM
    `specs:` blocks. Top-level gems are 4-space-indented `name
    (version)` lines; transitive deps live at 6-space indent."""
    n = 0
    in_specs = False
    rx = re.compile(r"^    [\w.-]+ \(.+\)$")
    for line in p.read_text().splitlines():
        if line.strip() == "specs:":
            in_specs = True
            continue
        if line and not line.startswith(" "):
            in_specs = False
            continue
        if in_specs and rx.match(line):
            n += 1
    return n


def _count_package_json(p: Path) -> int:
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError:
        return -1
    return (
        len(data.get("dependencies") or {})
        + len(data.get("devDependencies") or {})
        + len(data.get("peerDependencies") or {})
    )


def _count_package_lock(p: Path) -> int:
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError:
        return -1
    return len(data.get("packages") or data.get("dependencies") or {})


def _count_requirements(p: Path) -> int:
    n = 0
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            n += 1
    return n


def _count_cargo(p: Path) -> int:
    n = 0
    in_deps = False
    for line in p.read_text().splitlines():
        line = line.strip()
        if line.startswith("[dependencies]") or line.startswith("[dev-dependencies]"):
            in_deps = True
            continue
        if line.startswith("["):
            in_deps = False
            continue
        if in_deps and "=" in line and not line.startswith("#"):
            n += 1
    return n


def _count_go_mod(p: Path) -> int:
    n = 0
    in_require = False
    for line in p.read_text().splitlines():
        s = line.strip()
        if s.startswith("require ("):
            in_require = True
            continue
        if in_require and s == ")":
            in_require = False
            continue
        if in_require and s and not s.startswith("//"):
            n += 1
        elif s.startswith("require ") and "(" not in s:
            n += 1
    return n


def _schedule_run_eu_ai_act_countdown() -> int:
    """Refresh `wiki/_state/eu-ai-act.json` last_assessment + recompute days-to-deadline."""
    state_path = WIKI / "_state" / "eu-ai-act.json"
    if not state_path.exists():
        print(f"eu-ai-act-countdown: {state_path.relative_to(REPO)} absent", file=sys.stderr)
        return 1
    state = json.loads(state_path.read_text())
    today = today_utc()
    deadline = dt.date.fromisoformat(state.get("deadline", "2026-08-02"))
    days_left = (deadline - today).days
    state["last_assessment"] = today.isoformat()
    state["_days_left"] = days_left
    articles = state.get("articles", {})
    low = sum(1 for a in articles.values() if a.get("readiness") == "low")
    medium = sum(1 for a in articles.values() if a.get("readiness") == "medium")
    high = sum(1 for a in articles.values() if a.get("readiness") == "high")
    state["_summary"] = {"low": low, "medium": medium, "high": high}
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"eu-ai-act-countdown: {days_left} days to {deadline}; "
          f"per-Article readiness low={low} medium={medium} high={high}")
    return 0


def _schedule_run_issues_pull() -> int:
    """Pull issue counts via `gh issue list` per active sibling repo on disk."""
    state_path = WIKI / "_state" / "issues.json"
    if not state_path.exists():
        print(f"issues-pull: {state_path.relative_to(REPO)} absent", file=sys.stderr)
        return 1
    state = json.loads(state_path.read_text())
    today = today_utc().isoformat()
    populated = 0
    if not shutil.which("gh"):
        print("issues-pull: gh CLI not available; skipping", file=sys.stderr)
        return 0
    frozen_skipped = []
    for repo, entry in state.get("repos", {}).items():
        if repo in FROZEN_REPOS:
            # A frozen repository is closed to the operator: reaching for it
            # fails, and a failure here reads like "no issues". Name the skip.
            entry["notes"] = "(skipped: frozen scope tier, not reachable)"
            frozen_skipped.append(repo)
            continue
        sibling = PROJECTS / repo
        if not sibling.exists():
            entry["notes"] = f"(skipped — repo not on disk at {sibling})"
            continue
        try:
            res = subprocess.run(
                ["gh", "issue", "list", "--state", "open", "--limit", "1000",
                 "--json", "number,labels,createdAt"],
                cwd=sibling, capture_output=True, text=True, timeout=30,
            )
            if res.returncode != 0:
                entry["notes"] = f"(gh issue list failed: {res.stderr.strip()[:120]})"
                continue
            issues = json.loads(res.stdout or "[]")
        except Exception as exc:
            entry["notes"] = f"(gh issue list error: {exc})"
            continue
        critical = sum(1 for i in issues if any(
            (l.get("name") or "").lower() in ("critical", "p0", "sev-1") for l in i.get("labels", [])
        ))
        blocking = sum(1 for i in issues if any(
            (l.get("name") or "").lower() in ("blocking", "blocker") for l in i.get("labels", [])
        ))
        stale_30d = 0
        for i in issues:
            try:
                ts = i.get("createdAt", "")[:10]
                if ts and (today_utc() - dt.date.fromisoformat(ts)).days > 30:
                    stale_30d += 1
            except (ValueError, TypeError):
                continue
        entry.update({
            "last_pull": today,
            "open": len(issues),
            "critical_open": critical,
            "blocking_open": blocking,
            "stale_open_30d": stale_30d,
            "notes": "via gh issue list",
        })
        populated += 1
    state["last_pull"] = today
    state["source"] = "github-issues"
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"issues-pull: populated {populated} repo(s); skipped {len(frozen_skipped)} "
          f"frozen: {', '.join(sorted(frozen_skipped)) or 'none'}")
    return 0


def _schedule_run_notion_walk() -> int:
    """Walk sources/notion/ + flag snapshots older than 30 days."""
    notion_dir = REPO / "sources" / "notion"
    if not notion_dir.exists():
        print(f"notion-walk: {notion_dir.relative_to(REPO)} absent", file=sys.stderr)
        return 1
    today = today_utc()
    snapshots = list(notion_dir.glob("*.md"))
    stale = []
    for s in snapshots:
        # Notion snapshots carry an `updated:` or `captured:` frontmatter
        try:
            meta = (parse(s) or ({},))[0]
            ts_field = meta.get("captured") or meta.get("updated") or meta.get("fetched")
            if isinstance(ts_field, dt.date):
                age = (today - ts_field).days
            elif isinstance(ts_field, str):
                age = (today - dt.date.fromisoformat(ts_field[:10])).days
            else:
                continue
            if age > 30:
                stale.append((s.relative_to(REPO), age))
        except (ValueError, TypeError):
            continue
    cursor_path = WIKI / "_state" / "notion-cursor.json"
    state = {
        "_schema": "v1",
        "last_walk": today.isoformat(),
        "snapshot_count": len(snapshots),
        "stale_count": len(stale),
        "stale_examples": [{"path": str(p), "age_days": age} for p, age in stale[:10]],
    }
    cursor_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"notion-walk: {len(snapshots)} snapshot(s); {len(stale)} stale (>30d)")
    return 0


def _schedule_run_overlap_refresh() -> int:
    """Re-run the cluster command and dump output to wiki/_overlaps/."""
    overlap_path = WIKI / "_overlaps" / f"auto-refresh-{today_utc().isoformat()}.md"
    overlap_path.parent.mkdir(exist_ok=True)
    res = subprocess.run(
        [sys.executable, str(REPO / "tools" / "brain.py"), "cluster"],
        capture_output=True, text=True, timeout=60, cwd=REPO,
    )
    if res.returncode != 0 or res.stdout.startswith("missing dep:"):
        # A page of the error read as a scan that found nothing; 49 such
        # pages accumulated from 2026-05-08 before anyone noticed.
        reason = (res.stdout or res.stderr).strip().splitlines()[:1] or ["no output"]
        print(f"overlap-refresh: skipped, cluster could not run ({reason[0]}); no page written")
        return 0
    today = today_utc().isoformat()
    body = f"""---
title: "Auto-refreshed cluster scan {today}"
kind: overlap
status: living
updated: {today}
sources:
  - sources/notion/
  - tools/brain.py
---

# Auto-refreshed cluster scan {today}

Output of `brain.py cluster` (TF-IDF + HDBSCAN clustering over the
synthesis corpus). Run by `brain.py schedule run overlap-refresh`.

## Items

```
{res.stdout or '(no output)'}
```

## Overlap

(stub — review the cluster output and surface intersections that
warrant a `/overlap` deep-dive.)

## Recommendation

Operator decides whether any cluster warrants spawning a `/shape
org` follow-up.
"""
    overlap_path.write_text(body)
    print(f"overlap-refresh: wrote {overlap_path.relative_to(REPO)}")
    return 0


def _schedule_run_zoom_out_digest() -> int:
    """Synthesise a brain-wide zoom-out digest (deterministic, no LLM)."""
    digest_path = WIKI / "_state" / "zoom-out-digest.md"
    today = today_utc()
    # Frontmatter so Astro's docsSchema accepts it (title required).
    # Even though wiki/_state/ is a machine-readable shelf, the
    # symlinked docs/ root picks up every .md.
    parts = [
        "---",
        f'title: "Brain zoom-out digest — {today.isoformat()}"',
        "kind: meta",
        "status: living",
        f"updated: {today.isoformat()}",
        "sources: []",
        "---",
        "",
        f"# Brain zoom-out digest — {today.isoformat()}\n",
    ]

    # Recent log entries
    log_path = REPO / "log" / "log.md"
    if log_path.exists():
        log_lines = log_path.read_text().splitlines()
        recent = []
        for line in log_lines[::-1]:
            if line.startswith(today.isoformat()[:7]):  # this month
                recent.append(line)
            if len(recent) >= 30:
                break
        parts.append(f"\n## Recent log entries (this month, last 30)\n")
        for line in reversed(recent):
            parts.append(line)

    # In-flight efforts
    if EFFORTS_DIR.exists():
        efforts = list(EFFORTS_DIR.glob("*.json"))
        parts.append(f"\n## In-flight efforts ({len(efforts)})\n")
        for e in sorted(efforts):
            try:
                rec = json.loads(e.read_text())
                parts.append(f"- `{rec.get('slug', e.stem)}` — phase: "
                             f"{rec.get('phase', '?')}, status: "
                             f"{rec.get('status', '?')}")
            except json.JSONDecodeError:
                parts.append(f"- `{e.stem}` (unparseable record)")

    # AI-suggestion backlog
    ai_files = list(WIKI.glob("**/ai-suggestions/**/*.md"))
    suggested = [f for f in ai_files
                 if (parse(f) or ({},))[0].get("status") == "suggested"]
    parts.append(f"\n## AI-suggestion backlog ({len(suggested)} pending review)\n")
    for f in sorted(suggested)[:10]:
        meta = (parse(f) or ({},))[0]
        parts.append(f"- [{meta.get('title', f.name)}]({f.relative_to(WIKI)})")

    # Reflection-check summary (run quick)
    parts.append("\n## Reflection-check summary\n")
    parts.append("Run `brain.py reflection-check` for current findings.")

    digest_path.write_text("\n".join(parts) + "\n")
    print(f"zoom-out-digest: wrote {digest_path.relative_to(REPO)}")
    return 0


def _schedule_run_ai_suggestion_grooming() -> int:
    """Walk ai-suggestions/ + flag pages with `updated:` > 180 days old."""
    today = today_utc()
    threshold = today - dt.timedelta(days=180)
    ai_files = list(WIKI.glob("**/ai-suggestions/**/*.md"))
    stale = []
    for f in ai_files:
        meta = (parse(f) or ({},))[0]
        if meta.get("status") != "suggested":
            continue
        updated = meta.get("updated")
        if isinstance(updated, str):
            try:
                updated = dt.date.fromisoformat(updated)
            except ValueError:
                continue
        if not isinstance(updated, dt.date):
            continue
        if updated < threshold:
            stale.append({
                "path": str(f.relative_to(WIKI)),
                "updated": updated.isoformat(),
                "age_days": (today - updated).days,
                "title": meta.get("title", "(untitled)"),
            })
    state_path = WIKI / "_state" / "ai-suggestion-grooming.json"
    state_path.write_text(json.dumps({
        "_schema": "v1",
        "last_run": today.isoformat(),
        "threshold_days": 180,
        "stale_count": len(stale),
        "stale": stale,
    }, indent=2) + "\n")
    print(f"ai-suggestion-grooming: {len(ai_files)} ai-suggestions inspected; "
          f"{len(stale)} stale (>180d)")
    if stale:
        print("  Candidates for graduation or archive:")
        for s in stale[:10]:
            print(f"    {s['age_days']:4d}d  {s['path']}")
    return 0


SCHEDULE_HANDLERS = {
    "security-scan": _schedule_run_security_scan,
    "eu-ai-act-countdown": _schedule_run_eu_ai_act_countdown,
    "issues-pull": _schedule_run_issues_pull,
    "notion-walk": _schedule_run_notion_walk,
    "overlap-refresh": _schedule_run_overlap_refresh,
    "zoom-out-digest": _schedule_run_zoom_out_digest,
    "ai-suggestion-grooming": _schedule_run_ai_suggestion_grooming,
    "attention-refresh": _schedule_run_attention_refresh,
}


SCHEDULE_RUNS_KEPT = 90


def _schedule_runs(started: dt.datetime, outcomes: dict, timings: dict) -> list:
    """The run records, newest first and capped: this run, then one record per
    calendar day since the previous record on which no run was recorded, then
    the earlier records. The ten days without a run in September 2026 were
    invisible to a state file that held the last run only.
    """
    previous = {}
    if SCHEDULE_STATE.exists():
        try:
            previous = json.loads(SCHEDULE_STATE.read_text())
        except json.JSONDecodeError:
            previous = {}
    runs = [r for r in previous.get("runs") or [] if isinstance(r, dict)]
    day = started.date()
    missed = []
    try:
        since = dt.date.fromisoformat(runs[0]["date"] if runs else previous.get("last_run") or "")
    except (KeyError, ValueError):
        since = None
    if since is not None:
        gap = since + dt.timedelta(days=1)
        while gap < day:
            missed.insert(0, {"date": gap.isoformat(), "kind": "missed"})
            gap += dt.timedelta(days=1)
    record = {
        "date": day.isoformat(),
        "kind": "run",
        "started": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "operations": {name: {"outcome": outcome, **timings.get(name, {})}
                       for name, outcome in outcomes.items()},
    }
    return [record, *missed, *runs][:SCHEDULE_RUNS_KEPT]


def cmd_schedule(args) -> int:
    """Manage the declarative schedule at brain-schedule.yml.

    Per `wiki/brain/ai-suggestions/prds/scheduled-operations-and-tracking.md`.
    This v1 ships the config + listing only; the runner is a
    separate decision.
    """
    config_path = REPO / "brain-schedule.yml"
    if not config_path.exists():
        print(f"brain-schedule.yml not found at {config_path}", file=sys.stderr)
        return 1
    try:
        config = yaml.safe_load(config_path.read_text())
    except yaml.YAMLError as exc:
        print(f"brain-schedule.yml unparseable: {exc}", file=sys.stderr)
        return 1

    op = (args.op or "list").lower()

    if op == "list":
        print(f"# brain-schedule.yml v{config.get('version', '?')}")
        for entry in config.get("operations") or []:
            enabled = "✓" if entry.get("enabled") else "✗"
            print(f"  {enabled}  {entry.get('cadence', '?'):8s}  {entry.get('name')}")
            print(f"      {entry.get('description', '')}")
            if not entry.get("enabled") and entry.get("deferred_until"):
                print(f"      deferred until: {entry['deferred_until']}")
        return 0

    if op == "run":
        target = args.target
        if not target:
            print("schedule run requires --target <op-name>", file=sys.stderr)
            return 2
        # In-process handler first
        if target in SCHEDULE_HANDLERS:
            print(f"# running: {target}", file=sys.stderr)
            return SCHEDULE_HANDLERS[target]()
        # Fall back to handler in config (shell-out)
        for entry in config.get("operations") or []:
            if entry.get("name") == target:
                if not entry.get("enabled"):
                    print(f"operation {target!r} is disabled in brain-schedule.yml",
                          file=sys.stderr)
                    return 1
                handler = entry.get("handler")
                if not handler:
                    print(f"operation {target!r} has no handler", file=sys.stderr)
                    return 1
                print(f"# running: {target}", file=sys.stderr)
                rc = subprocess.run(handler, shell=True, cwd=REPO).returncode
                return rc
        print(f"operation {target!r} not found in brain-schedule.yml", file=sys.stderr)
        return 1

    if op == "run-due":
        # Every enabled op runs; the outcome of each is recorded so a
        # failing daily run is visible from inside the brain. Without
        # this the only witness is a GitHub Actions page nobody opens,
        # and the pipeline failed silently for three days from
        # 2026-07-30 while `brain.py status` looked entirely healthy.
        rc_total = 0
        outcomes = {}
        timings = {}
        run_started = dt.datetime.now(dt.timezone.utc)
        for entry in config.get("operations") or []:
            if not entry.get("enabled"):
                continue
            name = entry.get("name")
            print(f"# running: {name}", file=sys.stderr)
            began, clock = dt.datetime.now(dt.timezone.utc), time.monotonic()
            try:
                if name in SCHEDULE_HANDLERS:
                    rc = SCHEDULE_HANDLERS[name]()
                else:
                    handler = entry.get("handler")
                    if not handler:
                        continue
                    rc = subprocess.run(handler, shell=True,
                                        cwd=REPO).returncode
                outcomes[name] = "ok" if rc == 0 else f"exit {rc}"
            except Exception as exc:  # noqa: BLE001 — the record is the point
                # A raising handler is exactly how the KeyError went
                # unrecorded. Capture it, keep going, fail at the end.
                outcomes[name] = f"{type(exc).__name__}: {exc}"
                rc = 1
            timings[name] = {"started": began.strftime("%Y-%m-%dT%H:%M:%SZ"),
                             "seconds": round(time.monotonic() - clock, 3)}
            if rc != 0:
                rc_total = rc
        failed = {k: v for k, v in outcomes.items() if v != "ok"}
        _write_json_whole(SCHEDULE_STATE, {
            "_schema": 2,
            "last_run": today_utc().isoformat(),
            "operations": outcomes,
            "failed": sorted(failed),
            "runs": _schedule_runs(run_started, outcomes, timings),
        })
        if failed:
            print(f"# schedule: {len(failed)} operation(s) failed: "
                  f"{', '.join(sorted(failed))}", file=sys.stderr)
        return rc_total

    print(f"unknown schedule op: {op}", file=sys.stderr)
    return 2


def cmd_init(args) -> int:
    """Scaffold an empty brain shell at the target directory.

    Creates the minimum viable substrate: AGENTS.md (kernel-flavoured),
    wiki/ skeleton (index.md + brain/ + org/), tools/ pointer, an empty
    sources/, an empty log/log.md. After this, the operator fills wiki/
    with their organisation's content.

    Per `wiki/brain/ai-suggestions/prds/extractable-brain-shell.md`.
    """
    target = Path(args.path).resolve()
    if target.exists() and any(target.iterdir()):
        if not args.force:
            print(f"refusing to init non-empty directory: {target} (use --force)",
                  file=sys.stderr)
            return 1

    target.mkdir(parents=True, exist_ok=True)

    org = args.org or "<your-organisation>"

    # AGENTS.md: kernel-flavoured (no organisation specifics)
    agents_md = f'''# AGENTS.md — schema for the brain

You are the agent maintaining this brain. This file tells you how.
The methodology is the LLM-wiki pattern from
<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>.

This brain was scaffolded by `brain.py init` on {today_utc().isoformat()}
for {org}.

## Mission

Maintain a synthesis of {org} — products, repositories, decisions,
people, roadmap — accurate enough that:

1. **Codebases could be regenerated** from the specs stored here.
2. **Cross-team overlaps surface, not hide.**
3. **Autonomous agents can use this as their primary context.**

## The three layers

1. **Raw sources** (`sources/`) — immutable.
2. **The wiki** (`wiki/`) — markdown pages you own. `wiki/index.md` is
   the catalog.
3. **The schema** — this file.

## Page kinds

Set `kind:` in frontmatter:

| Kind         | Purpose                                            |
|--------------|----------------------------------------------------|
| `reference`  | How a thing *is*.                                  |
| `initiative` | Active piece of work (PRD).                        |
| `decision`   | A specific decision (ADR).                         |
| `entity`     | A person, team, division, product, customer.       |
| `meta`       | About the brain itself.                            |
| `insight`    | A pattern derived from feedback / observed work.   |
| `epic`       | Umbrella over multi-PRD/ADR work.                  |

## Active scope

Sibling repos this brain tracks:

| Repo        | Status |
|-------------|--------|
| (add yours) |        |

## Tools

- `python3 tools/brain.py validate` — frontmatter + section conformance.
- `python3 tools/brain.py check --no-net` — citation paths resolve.
- `python3 tools/brain.py views` — regenerate `wiki/_views/`.
- `python3 tools/brain.py search '<query>'` — hybrid keyword search.
- `python3 tools/brain.py install-sibling <repo>` — wire the brain into
  a sibling repo's Claude Code session.
- `python3 tools/brain.py reflection-check` — drift between brain and
  target-repo state.
- `python3 tools/brain-mcp.py` — stdio MCP server for MCP-aware clients.

## Conventions

- Filenames: kebab-case, `.md`.
- Frontmatter: every wiki page starts with YAML (`title`, `kind`,
  `status`, `updated`, `sources` required; others optional).
- Cross-links: relative markdown links between wiki pages.
- Dates: absolute (`YYYY-MM-DD`), never relative.
- Voice: present tense, declarative.
- Don't invent. If a fact is not in a source you can cite, write
  *"(unknown — needs source)"*.
- Supersede, don't silently overwrite.

This is the kernel-flavoured AGENTS.md. Edit liberally to match your
organisation's shape — add active-scope rows, ingest conventions,
cross-product cluster names, etc.
'''
    (target / "AGENTS.md").write_text(agents_md)
    # Convenience symlink for tools that expect CLAUDE.md
    try:
        (target / "CLAUDE.md").symlink_to("AGENTS.md")
    except (FileExistsError, OSError):
        pass

    # wiki/ skeleton
    (target / "wiki").mkdir(exist_ok=True)
    (target / "wiki" / "_views").mkdir(exist_ok=True)
    (target / "wiki" / "_archive").mkdir(exist_ok=True)
    (target / "wiki" / "_overlaps").mkdir(exist_ok=True)
    (target / "wiki" / "_state").mkdir(exist_ok=True)
    (target / "wiki" / "brain").mkdir(exist_ok=True)
    (target / "wiki" / "brain" / "ai-suggestions").mkdir(exist_ok=True)
    (target / "wiki" / "brain" / "adrs").mkdir(exist_ok=True)
    (target / "wiki" / "brain" / "prds").mkdir(exist_ok=True)
    (target / "wiki" / "org").mkdir(exist_ok=True)
    (target / "wiki" / "org" / "ai-suggestions").mkdir(exist_ok=True)
    (target / "wiki" / "insights").mkdir(exist_ok=True)

    # wiki/index.md — minimal home with the contract sections
    home_md = f'''---
title: "{org} brain — home"
kind: meta
status: draft
updated: {today_utc().isoformat()}
sources: []
---

# {org} brain

This is an LLM-maintained knowledge base scaffolded by `brain.py init`.
Fill it with your organisation's content — per-repo shelves, cross-
product synthesis, decisions, initiatives.

## What changed

<!-- home-section: empty; maintained-by: /shape -->
*(empty — no `/shape` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Open initiatives

<!-- home-section: empty; maintained-by: /shape -->
*(empty — no `/shape` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Recent decisions

<!-- home-section: empty; maintained-by: /shape -->
*(empty — no `/shape` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Drift surface

<!-- home-section: empty; maintained-by: /groom -->
*(empty — no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Insights now

<!-- home-section: empty; maintained-by: /feedback -->
*(empty — no `/feedback` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Brain trajectory

<!-- home-section: empty; maintained-by: /groom -->
*(empty — no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Curated picks

<!-- home-section: empty; maintained-by: /groom -->
*(empty — no `/groom` run yet)*

[See more in `wiki/_views/by-kind.md`](_views/by-kind.md)

## Where to find things

- [Brain — meta level](brain/index.md)
- [Org — methodology + cross-product](org/index.md)
- Per-repo shelves arrive as you add them: `wiki/<repo>/index.md`
'''
    (target / "wiki" / "index.md").write_text(home_md)

    # wiki/brain/index.md
    brain_idx = f'''---
title: "Brain (meta level)"
kind: meta
status: draft
updated: {today_utc().isoformat()}
sources: []
---

# Brain — meta level

This shelf tracks how the brain itself operates: schema, conventions,
tooling, governance.

## ADRs
*(none yet — `/shape brain --record <decision>` to author)*

## PRDs
*(none yet — `/shape brain <pitch>` to author)*

## AI suggestions (drafts for human review)
*(none yet)*
'''
    (target / "wiki" / "brain" / "index.md").write_text(brain_idx)

    # wiki/org/index.md
    org_idx = f'''---
title: "{org} — methodology + cross-product"
kind: meta
status: draft
updated: {today_utc().isoformat()}
sources: []
---

# {org} — methodology + cross-product

This shelf tracks how {org} works as an organisation: process,
methodology, cross-product synthesis, competitor intel, compliance.

## Pages
*(none yet — fill as your organisation's shape becomes visible)*
'''
    (target / "wiki" / "org" / "index.md").write_text(org_idx)

    # log/log.md
    (target / "log").mkdir(exist_ok=True)
    (target / "log" / "log.md").write_text(
        f"# Brain operations log\n\n"
        f"{today_utc().isoformat()} init — brain scaffolded by `brain.py init` for {org}\n"
    )

    # sources/ — empty
    (target / "sources").mkdir(exist_ok=True)
    (target / "sources" / ".gitkeep").touch()

    # .gitignore
    (target / ".gitignore").write_text(
        "# brain-shell scaffold\n"
        ".env\n"
        ".env.*\n"
        "!.env.example\n"
        "*.swp\n"
        "*~\n"
        ".DS_Store\n"
        "__pycache__/\n"
        "*.pyc\n"
        "node_modules/\n"
        ".claude/worktrees/\n"
        ".claude/scheduled_tasks.lock\n"
        "wiki/_views/home-staleness.json\n"
    )

    # Run views once so wiki/_views/by-kind.md etc. exist (the home page
    # references them).
    saved_repo = (REPO, WIKI)
    globals()["REPO"] = target
    globals()["WIKI"] = target / "wiki"
    try:
        cmd_views(args)
    except Exception as exc:
        print(f"warning: initial views regen failed: {exc}", file=sys.stderr)
    finally:
        globals()["REPO"], globals()["WIKI"] = saved_repo

    print(f"brain shell scaffolded at: {target}", file=sys.stderr)
    print(f"  AGENTS.md / CLAUDE.md (symlink)")
    print(f"  wiki/index.md  (home)")
    print(f"  wiki/brain/index.md, wiki/org/index.md (sub-hubs)")
    print(f"  log/log.md (audit trail)")
    print(f"  sources/ (empty)")
    print(f"")
    print(f"  Note: tools/ is intentionally NOT copied — point this shell at")
    print(f"  an existing brain.py via $BRAIN_DIR or copy tools/ from the")
    print(f"  reference brain. The kernel-vs-content extraction is itself an")
    print(f"  open initiative tracked in")
    print(f"  wiki/brain/ai-suggestions/prds/extractable-brain-shell.md.")
    return 0


def _entry_calls_brain_hook(entry: dict) -> bool:
    """Heuristic: does this PreToolUse entry call brain-hook.sh?"""
    if not isinstance(entry, dict):
        return False
    for h in (entry.get("hooks") or []):
        if isinstance(h, dict):
            cmd = h.get("command") or ""
            if "brain-hook.sh" in cmd:
                return True
    if "brain-hook.sh" in (entry.get("command") or ""):
        return True
    return False


def _search_semantic(query, repo_filter, kind_filter, include_superseded, top_k):
    """Rank pages by a typed judgment: one Score question per candidate page
    over its title and opening text. Returns (results, held_back, tokens), or
    None after printing a named skip, in which case the caller ranks by
    keyword. A ranking is a candidate list, never a verdict.

    Measured 2026-09-21 on 20 natural-language questions over 331 pages:
    keyword ranking put the right page in the top five 0 times, this 16 times,
    at about 52k input tokens and 3.7 s a query. Per
    wiki/brain/adrs/typed-judgments-through-one-seam.md."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import typed_judge  # noqa: PLC0415
    try:
        from typesafe_sdk import Score  # noqa: PLC0415
    except ImportError:
        print("# semantic ranking not asked: typesafe-sdk is not installed; "
              "falling back to keyword ranking", file=sys.stderr)
        return None
    levels = ["has nothing to do with the query",
              "touches the query's topic without answering it",
              "is the page a reader should open to answer the query"]
    candidates, held_back = [], 0
    allow = typed_judge.include_frozen()
    for p in wiki_pages():
        parsed = parse(p)
        if parsed is None:
            continue
        meta, body = parsed
        rel = str(p.relative_to(WIKI))
        status = meta.get("status")
        if status in ("superseded", "archived") and not include_superseded:
            continue
        if kind_filter and meta.get("kind") != kind_filter:
            continue
        if repo_filter:
            page_repos = set(meta.get("repos") or []) | set(meta.get("affects") or [])
            if repo_filter not in page_repos and not rel.startswith(f"{repo_filter}/"):
                continue
        if not typed_judge.may_send(rel, meta, FROZEN_REPOS, allow):
            held_back += 1
            continue
        opening = " ".join(re.sub(r"(?m)^(#|>|\||-|\*|```).*$", "", body).split())[:220]
        candidates.append((rel, meta, opening))
    questions = {
        f"p{i}": Score(
            instructions=(f"`query` is a reader's question. The candidate page is titled "
                          f"\"{meta.get('title', rel)}\" and begins: \"{opening}\". "
                          f"How well does this page fit?"),
            criteria=levels)
        for i, (rel, meta, opening) in enumerate(candidates)
    }
    verdict = typed_judge.judge({"query": query}, questions)
    if verdict.skipped:
        print(f"# {verdict.reason}; falling back to keyword ranking", file=sys.stderr)
        return None
    rows = []
    for i, (rel, meta, opening) in enumerate(candidates):
        a = verdict.answers.get(f"p{i}")
        if a is None:
            continue
        rows.append({"path": rel, "title": meta.get("title", ""), "kind": meta.get("kind"),
                     "confidence": meta.get("confidence"), "status": meta.get("status"),
                     "score": round(float(a.score), 3), "excerpt": opening[:160]})
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows[:top_k], held_back, verdict.input_tokens


def cmd_search(args) -> int:
    """Keyword search over the wiki/ synthesis layer.

    BM25 over each page (title weight 3×, body weight 1×), times the
    factor of the first `search.factors` row in tabula.config.yml whose
    pattern matches the page's wiki-relative path (none when the key is
    absent), times the page's confidence tier (high 1.3× / medium 1.0× /
    low 0.85×). tabula's search reads the same key, so the two rank alike.
    Returns top-K matches.

    Per `wiki/brain/ai-suggestions/prds/hybrid-search-via-brain-py.md`,
    whose path table was removed on 2026-09-30, having never matched.
    """
    CONFIDENCE_FACTORS = {"high": 1.3, "medium": 1.0, "low": 0.85}
    try:
        cfg = yaml.safe_load(config_path().read_text()) or {}
    except (OSError, yaml.YAMLError):
        cfg = {}
    try:
        path_factors = [(re.compile(str(r["pattern"])), float(r["factor"]))
                        for r in ((cfg.get("search") or {}).get("factors") or [])]
    except (re.error, KeyError, TypeError, ValueError) as e:
        print(f"refused: {config_path().name}: search.factors: {e}", file=sys.stderr)
        return 2

    def path_factor(rel_path: str) -> float:
        return next((f for pat, f in path_factors if pat.search(rel_path)), 1.0)

    def confidence_factor(meta: dict) -> float:
        return CONFIDENCE_FACTORS.get(meta.get("confidence"), 0.95)

    query_terms = [t.lower() for t in re.findall(r"\w+", args.query) if len(t) >= 2]
    if not query_terms:
        print(f"empty query terms after tokenisation: {args.query!r}", file=sys.stderr)
        return 2

    repo_filter = args.repo
    kind_filter = args.kind
    include_superseded = args.include_superseded
    top_k = args.top

    if getattr(args, "semantic", False):
        ranked = _search_semantic(args.query, repo_filter, kind_filter, include_superseded, top_k)
        if ranked is not None:
            results, held_back, tokens = ranked
            note = (f"ranked by typed judgment over {tokens} input tokens"
                    + (f"; {held_back} page(s) held back by the send guard" if held_back else ""))
            if args.json:
                print(json.dumps({"query": args.query, "ranked_by": "typed-judgment",
                                  "held_back": held_back, "input_tokens": tokens,
                                  "results": results}, indent=2))
                return 0 if results else 1
            print(f"# {note}", file=sys.stderr)
            for r in results:
                print(f"{r['score']:6.2f}  {r['path']}")
                if r["title"]:
                    print(f"        {r['title'][:120]}")
            return 0 if results else 1
        # A named skip was printed; fall through to keyword ranking.

    # BM25 (k1 1.2, b 0.75) over the candidate set, title counted three times,
    # the confidence factor applied after; the same scorer as
    # tabula's `search` (0 to 13 of 20 on the eval set, 2026-09-23). Two
    # passes: candidates first, so document frequency and average length
    # are known before any score.
    candidates = []
    for p in wiki_pages():
        parsed = parse(p)
        if parsed is None:
            continue
        meta, body = parsed
        rel = str(p.relative_to(WIKI))

        status = meta.get("status")
        if status in ("superseded", "archived") and not include_superseded:
            continue

        if kind_filter and meta.get("kind") != kind_filter:
            continue

        if repo_filter:
            page_repos = set(meta.get("repos") or []) | set(meta.get("affects") or [])
            if repo_filter not in page_repos and not rel.startswith(f"{repo_filter}/"):
                continue

        title = (meta.get("title") or "").lower()
        body_lower = body.lower()
        candidates.append((rel, meta, body, status, title, body_lower, len(re.findall(r"\w+", body_lower)) + 1))

    n = len(candidates)
    avg_len = sum(c[6] for c in candidates) / max(n, 1)
    idf = {}
    for term in query_terms:
        df = sum(1 for c in candidates if term in c[5] or term in c[4])
        idf[term] = math.log((n - df + 0.5) / (df + 0.5) + 1.0)
    k1, b = 1.2, 0.75

    results = []
    for rel, meta, body, status, title, body_lower, length in candidates:
        score = 0.0
        for term in query_terms:
            tf = body_lower.count(term) + 3 * title.count(term)
            if tf == 0:
                continue
            score += idf[term] * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / avg_len))
        if score == 0:
            continue

        score *= path_factor(str(rel))
        score *= confidence_factor(meta)

        # Build a short excerpt from the first body line containing any term
        excerpt = ""
        for line in body.splitlines():
            ll = line.lower()
            if any(t in ll for t in query_terms):
                excerpt = line.strip()[:160]
                break

        results.append({
            "path": rel,
            "title": meta.get("title", ""),
            "kind": meta.get("kind"),
            "confidence": meta.get("confidence"),
            "status": status,
            "score": round(score, 3),
            "excerpt": excerpt,
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    results = results[:top_k]

    if args.json:
        print(json.dumps({"query": args.query, "results": results}, indent=2))
        return 0 if results else 1

    if not results:
        print(f"no matches for: {args.query}", file=sys.stderr)
        return 1
    for r in results:
        marker = "[h]" if r["confidence"] == "high" else (
            "[l]" if r["confidence"] == "low" else "[m]"
        )
        print(f"{r['score']:6.2f}  {marker} {r['path']}")
        if r["title"]:
            print(f"        {r['title'][:120]}")
        if r["excerpt"]:
            print(f"        “{r['excerpt']}”")
    return 0


def cmd_reflection_check(args) -> int:
    """Detect drift between brain claims and target-repo state.

    Mechanical-only checks (deterministic, offline-safe). The
    full reflection-validator suite is described in
    `wiki/brain/ai-suggestions/prds/reflection-validator-suite.md`.

    Each sub-check prints findings to stdout (one per line) and
    contributes to the exit code. Exit 0 if every requested
    check is clean; exit 1 if anything is flagged.

    Findings are warnings by default — the check surfaces drift,
    the human acts. CI integration should read the findings,
    not the exit code, until calibration is done.
    """
    which = (args.which or "all").lower()
    findings: list[str] = []

    pages_data: list[dict] = []  # cache for cross-check use
    pages_index: dict[str, dict] = {}

    def load_pages():
        nonlocal pages_data, pages_index
        if pages_data:
            return
        for p in wiki_pages():
            parsed = parse(p)
            if parsed is None:
                continue
            meta, body = parsed
            rel = str(p.relative_to(WIKI))
            pages_data.append({"path": rel, "meta": meta, "body": body, "abs": p})
            pages_index[rel] = pages_data[-1]

    def check_links() -> int:
        """Every wiki/ markdown link resolves to a real file."""
        n = 0
        for page in wiki_files():
            rel = page.relative_to(WIKI)
            if any(part.startswith("_") for part in rel.parts):
                continue
            text = page.read_text()
            for href in re.findall(r"\]\(([^)]+)\)", text):
                href = href.split("#", 1)[0].strip()
                if not href or href.endswith("/") or href.startswith(("http://", "https://", "mailto:", "~/")):
                    continue
                if not href.endswith(PAGE_SUFFIXES):
                    continue
                target = (page.parent / href).resolve()
                try:
                    rel_target = target.relative_to(WIKI)
                except ValueError:
                    # link escapes wiki/ — out of scope
                    continue
                if not target.exists():
                    findings.append(
                        f"links: {rel} → broken link to {rel_target}"
                    )
                    n += 1
        return n

    def check_confidence_floor() -> int:
        """`confidence: high` pages whose `updated:` is > 30 days old."""
        load_pages()
        cutoff = today_utc() - dt.timedelta(days=30)
        n = 0
        for entry in pages_data:
            meta = entry["meta"]
            if meta.get("confidence") != "high":
                continue
            updated = meta.get("updated")
            if not updated:
                continue
            if isinstance(updated, str):
                try:
                    updated = dt.date.fromisoformat(updated)
                except ValueError:
                    continue
            if updated < cutoff:
                findings.append(
                    f"confidence-floor: {entry['path']} is confidence:high "
                    f"but updated:{updated} (>30d ago — needs refresh per "
                    f"AGENTS.md § Knowledge half-life)"
                )
                n += 1
        return n

    def check_active_scope() -> int:
        """AGENTS.md § Active scope matches wiki/<repo>/ folders *and*
        ACTIVE_REPOS. Three surfaces mean "active" — the schema table,
        the wiki shelves, and the constant in this file — so all three
        are compared pairwise against the table."""
        agents = (REPO / "AGENTS.md").read_text()
        # Find entries in the active-scope table
        scope_section = re.search(
            r"###?\s*Active scope.*?(?=^##\s|\Z)",
            agents, re.MULTILINE | re.DOTALL,
        )
        if not scope_section:
            findings.append("active-scope: AGENTS.md missing § Active scope")
            return 1
        body = scope_section.group(0)
        # Crudely extract repo names from the table (first column rows)
        agents_repos = set()
        for line in body.splitlines():
            m = re.match(r"\|\s*`([\w-]+)`\s*\|", line)
            if m:
                agents_repos.add(m.group(1))
        # Repos per tier, read from the status column. `active` also matches
        # the bold form the table once used.
        tiered_in_agents: dict[str, set] = {t: set() for t in SCOPE_TIERS}
        for line in body.splitlines():
            m = re.match(r"\|\s*`([\w-]+)`\s*\|\s*(?:\*\*)?(active|reference|frozen)(?:\*\*)?\s*\|", line)
            if m:
                tiered_in_agents[m.group(2)].add(m.group(1))
        active_in_agents = tiered_in_agents["active"]
        shelved_in_agents = set().union(*tiered_in_agents.values())
        # Walk wiki/ for top-level <repo>/ folders that have index.md
        wiki_repos = set()
        for child in WIKI.iterdir():
            if not child.is_dir():
                continue
            # org/, brain/ and patterns/ are brain-level shelves, not repo
            # shelves. "insights" was excluded here too, from the era when the
            # insight-pages shelf lived at wiki/insights/ — that shelf is
            # wiki/patterns/ now, and the name belongs to the analytics REPO
            # ingested 2026-08-04, so excluding it made a real repo shelf
            # invisible to this detector (found when the shelf's own ingest
            # tripped the false finding).
            # library/ is the architecture library tabula's library page
            # serves (2026-09-27), a brain-level shelf and not a repo's.
            if child.name.startswith("_") or child.name in ("org", "brain", "patterns", "library"):
                continue
            if (child / "index.md").exists():
                wiki_repos.add(child.name)
        n = 0
        only_agents = shelved_in_agents - wiki_repos
        only_wiki = wiki_repos - shelved_in_agents
        for r in sorted(only_agents):
            findings.append(
                f"active-scope: {r} has a scope tier in AGENTS.md but no wiki/{r}/index.md exists"
            )
            n += 1
        for r in sorted(only_wiki):
            findings.append(
                f"active-scope: wiki/{r}/index.md exists but {r} has no scope tier "
                f"(active, reference or frozen) in AGENTS.md"
            )
            n += 1
        for tier in ("reference", "frozen"):
            for r in sorted(tiered_in_agents[tier] - SCOPE_TIERS[tier]):
                findings.append(
                    f"active-scope: {r} is {tier} in AGENTS.md but missing from "
                    f"{tier.upper()}_REPOS in tools/brain.py"
                )
                n += 1
            for r in sorted(SCOPE_TIERS[tier] - tiered_in_agents[tier]):
                findings.append(
                    f"active-scope: {r} is in {tier.upper()}_REPOS in tools/brain.py "
                    f"but not {tier} in AGENTS.md § Active scope"
                )
                n += 1
        # Third surface: the ACTIVE_REPOS constant in this file. Nothing
        # compared it to the schema until 2026-08-03, and the gap was not
        # theoretical: a repo sat in ARCHIVED_REPOS for two days after the
        # table promoted it, so `sync-siblings.sh` skipped it while this
        # detector reported clean (a live wiki/<repo>/ shelf satisfied the
        # folder comparison above) and `test_active_repos_consistent`
        # reported clean too (it
        # asserted only a subset relation, which survives the code
        # omitting a repo the schema lists). Both directions here: a repo
        # active in the schema but absent from the constant is the drift
        # that happened, and the reverse would make the constant claim
        # scope the schema never granted.
        for r in sorted(active_in_agents - ACTIVE_REPOS):
            findings.append(
                f"active-scope: {r} is **active** in AGENTS.md but missing "
                f"from ACTIVE_REPOS in tools/brain.py — tooling that reads "
                f"the constant (sibling sweeps, validation) will skip it"
            )
            n += 1
        for r in sorted(ACTIVE_REPOS - active_in_agents):
            findings.append(
                f"active-scope: {r} is in ACTIVE_REPOS in tools/brain.py "
                f"but not **active** in AGENTS.md § Active scope"
            )
            n += 1
        return n

    def check_supersedes_cycles() -> int:
        """`supersedes:` / `superseded_by:` chains have no cycles."""
        load_pages()
        graph: dict[str, str] = {}
        for entry in pages_data:
            sb = entry["meta"].get("superseded_by")
            if sb and isinstance(sb, str):
                graph[entry["path"]] = sb.strip()
        n = 0
        for start in list(graph):
            seen = [start]
            cur = start
            while cur in graph:
                cur = graph[cur]
                if cur in seen:
                    findings.append(
                        f"supersedes-cycles: cycle detected → {' → '.join(seen + [cur])}"
                    )
                    n += 1
                    break
                seen.append(cur)
                if len(seen) > 50:
                    findings.append(
                        f"supersedes-cycles: chain too long from {start} (>50)"
                    )
                    n += 1
                    break
        return n

    def check_page_size() -> int:
        """Pages > 500 lines are flagged as split candidates.

        Excludes content-driven cases:
        - `kind: epic` — umbrella structure inherently large.
        - `status: superseded` — redirect stubs / historical content.
        - `status: accepted` ADRs — committed decisions with full
          alternatives + consequences are content-driven.
        - `status: living` PRDs / reference pages — content-driven
          (per AGENTS.md § Scale conventions: *"aim for"* not
          *"must be"*).

        The threshold remains 500 but the *flag* fires only for
        `status: draft` content where size genuinely indicates the
        author should split before shipping.
        """
        load_pages()
        n = 0
        for entry in pages_data:
            kind = entry["meta"].get("kind")
            status = entry["meta"].get("status")
            if kind == "epic":
                continue
            if status in ("superseded", "archived"):
                continue
            # Living / accepted / shipped content is content-driven
            # by the time it's stable. Only drafts trigger the flag.
            if status not in ("draft", None):
                continue
            line_count = entry["body"].count("\n")
            if line_count > 500:
                findings.append(
                    f"page-size: {entry['path']} has {line_count} body lines "
                    f"(kind={kind}, status={status}); split candidate per "
                    f"AGENTS.md § Scale conventions"
                )
                n += 1
        return n

    def check_sources_exist() -> int:
        """Every non-URL `sources:` entry resolves on disk.

        Sibling-repo paths (~/projects/<repo>/...) are skipped
        if the sibling repo isn't on this machine. The full
        check lives in `brain.py check --no-net`; this is a
        thin pointer to that.
        """
        # delegate to existing cmd_check logic
        n = 0
        for entry in pages_data or (load_pages() or pages_data):
            for src in entry["meta"].get("sources") or []:
                if not isinstance(src, str):
                    continue
                if src.startswith(("http://", "https://")):
                    continue
                kind, msg = _check_path(src, entry["abs"])
                if kind == "broken":
                    findings.append(
                        f"sources-exist: {entry['path']} cites missing path: {src}"
                    )
                    n += 1
        return n

    def check_sync_drift() -> int:
        """For each sibling repo on disk, list how many commits HEAD is
        ahead of the recorded sync-cursor."""
        cursors_path = WIKI / "_state" / "sync-cursors.json"
        if not cursors_path.exists():
            return 0
        try:
            cursors = json.loads(cursors_path.read_text())
        except json.JSONDecodeError:
            findings.append("sync-drift: wiki/_state/sync-cursors.json unparseable")
            return 1
        n = 0
        for repo, cursor in (cursors.get("cursors") or cursors).items():
            if not isinstance(cursor, dict):
                continue
            sha = cursor.get("sha")
            if not sha:
                continue
            sibling = PROJECTS / repo
            if not (sibling / ".git").exists():
                continue
            try:
                count = subprocess.run(
                    ["git", "rev-list", f"{sha}..HEAD", "--count"],
                    cwd=sibling, capture_output=True, text=True, timeout=10,
                )
                if count.returncode != 0:
                    findings.append(
                        f"sync-drift: {repo} cursor SHA {sha[:8]} not reachable from HEAD "
                        f"(rebase / force-push? — re-set cursor)"
                    )
                    n += 1
                    continue
                ahead = int((count.stdout or "0").strip() or "0")
                if ahead > 50:
                    findings.append(
                        f"sync-drift: {repo} HEAD is {ahead} commits ahead of cursor "
                        f"({sha[:8]}); consider an incremental ingest pass"
                    )
                    n += 1
            except Exception:
                continue
        return n

    def check_epic_children() -> int:
        """`parent_epic:` references resolve and the epic's `## Children`
        section lists the child by slug."""
        load_pages()
        n = 0
        # Collect epics
        epics: dict[str, dict] = {}
        for entry in pages_data:
            if entry["meta"].get("kind") == "epic":
                slug = Path(entry["path"]).stem
                epics[slug] = entry
        for entry in pages_data:
            parent = entry["meta"].get("parent_epic")
            if not parent:
                continue
            if parent not in epics:
                findings.append(
                    f"epic-children: {entry['path']} claims parent_epic={parent!r} "
                    f"but no kind:epic page with that slug exists"
                )
                n += 1
                continue
            epic = epics[parent]
            child_slug = Path(entry["path"]).stem
            if child_slug not in epic["body"]:
                findings.append(
                    f"epic-children: {entry['path']} claims parent_epic={parent!r} "
                    f"but the epic page does not mention this child by slug "
                    f"({child_slug})"
                )
                n += 1
        return n

    def check_sources_immutability() -> int:
        """`sources/` tree should be additive-only (no modified files vs git
        baseline)."""
        try:
            res = subprocess.run(
                ["git", "diff", "--name-only", "HEAD", "--", "sources/"],
                cwd=REPO, capture_output=True, text=True, timeout=10,
            )
        except Exception as exc:
            findings.append(f"sources-immutability: git diff failed: {exc}")
            return 1
        modified = [
            line for line in (res.stdout or "").splitlines()
            if line.strip() and line.startswith("sources/")
        ]
        # Filter to truly modified (not new). `git diff HEAD --name-only` lists
        # both modified and new (untracked are NOT shown by HEAD diff). We
        # need git status to tell new from modified.
        if not modified:
            return 0
        try:
            status = subprocess.run(
                ["git", "status", "--porcelain", "--", "sources/"],
                cwd=REPO, capture_output=True, text=True, timeout=10,
            )
        except Exception:
            status = None
        # Parse status: lines starting with " M" = modified tracked file
        truly_modified = []
        if status and status.returncode == 0:
            for ln in status.stdout.splitlines():
                code = ln[:2]
                path = ln[3:]
                if "M" in code and path.startswith("sources/"):
                    truly_modified.append(path)
        else:
            truly_modified = modified
        n = 0
        for path in truly_modified:
            findings.append(
                f"sources-immutability: {path} is modified relative to git "
                f"baseline (sources/ is additive-only per AGENTS.md)"
            )
            n += 1
        return n

    def check_repo_claims() -> int:
        """Heuristic brain↔repo truth check.

        Walks each page's body for `~/projects/<repo>/<path>` claims;
        if the sibling repo is on disk, verifies the path resolves.
        Skips claims about lines (`:42`) and ranges.

        Per `wiki/brain/ai-suggestions/prds/scheduled-operations-and-tracking.md`.
        Mechanical-only — no LLM verification of code semantics.
        """
        load_pages()
        n = 0
        # Match ~/projects/<repo>/<path> with optional :line suffix.
        # Lookahead excludes `.` so file extensions aren't truncated.
        rx = re.compile(
            r"~/projects/([\w-]+)/([\w./_-]+?)(?::\d+(?:-\d+)?)?(?=[\s`)\],]|$)",
            re.MULTILINE,
        )
        seen: set[tuple[str, str]] = set()  # (page_path, claimed_path)
        for entry in pages_data:
            for m in rx.finditer(entry["body"]):
                repo = m.group(1)
                rel_path = m.group(2)
                key = (entry["path"], f"{repo}/{rel_path}")
                if key in seen:
                    continue
                seen.add(key)
                sibling = PROJECTS / repo
                if not sibling.exists():
                    continue  # repo not on disk; skip
                target = sibling / rel_path
                if not target.exists():
                    if (sibling / ".git").exists() and \
                            _branch_carrying_path(str(sibling), rel_path):
                        continue
                    findings.append(
                        f"repo-claims: {entry['path']} cites "
                        f"~/projects/{repo}/{rel_path} but the path does not "
                        f"exist in the sibling repo (any branch tip)"
                    )
                    n += 1
        return n

    def check_receipt_citations() -> int:
        """Receipt citations in wiki prose match the recorded digests.

        Per wiki/brain/adrs/receipt-claim-verification.md: `stale`
        means the graph content moved past the cited digest — the
        claim needs re-verification, it is not thereby wrong.
        """
        n = 0
        for c in _enola_wiki_citations():
            if c["verdict"] == "verified":
                continue
            if c["verdict"] == "stale":
                detail = (f"cites digest {c['digest']}… for {c['repo']} but "
                          "the graph content moved — re-verify the claim")
            elif c["verdict"] == "unknown-repo":
                detail = (f"cites repo {c['repo']} which has no recorded "
                          "receipt")
            else:
                detail = "matches `enola receipt` + sha256 but not the grammar"
            findings.append(
                f"receipt-citations: {c['page']}:{c['line']} {detail}"
            )
            n += 1
        return n

    def check_archived_liveness() -> int:
        """Archived repos that are still being pushed to.

        `archived` is written once and otherwise never re-checked, so a
        repo that came back to life looks exactly like one that stayed
        dead. Cheap remote check against the GitHub owner named by
        BRAIN_GITHUB_OWNER; skips silently without `gh` or without that
        variable, so CI and offline runs are unaffected.
        """
        n = 0
        if shutil.which("gh") is None:
            return 0
        archived = re.findall(r"^\| `([\w.-]+)`\s*\|\s*archived\s*\|",
                              (REPO / "AGENTS.md").read_text(), re.M)
        owner = os.environ.get("BRAIN_GITHUB_OWNER", "")
        if not owner:
            return 0
        for repo in archived:
            try:
                out = subprocess.run(
                    ["gh", "api", f"repos/{owner}/{repo}",
                     "--jq", ".archived,.pushed_at"],
                    capture_output=True, text=True, timeout=20)
            except (subprocess.SubprocessError, OSError):
                continue
            if out.returncode != 0:
                continue
            parts = out.stdout.split()
            if len(parts) < 2:
                continue
            is_archived, pushed = parts[0], parts[1]
            if is_archived == "false":
                findings.append(
                    f"archived-liveness: {repo} is recorded archived in "
                    f"AGENTS.md but the remote is not archived "
                    f"(last push {pushed[:10]}) — re-activate ingest or "
                    f"record why not")
                n += 1
        return n

    def check_ledger_hygiene() -> int:
        """Verdict entries whose finding no longer exists in the graph.

        Both graph ADRs named the ledger's eventual grooming pass as a
        known future need, and graph-verified-ingest made it sooner by
        adding ingest-time entries alongside groom-time ones. An
        `accepted` entry whose finding is gone is usually good news —
        the thing got fixed — and its `cited_at` page may now overclaim;
        a `rejected` one that vanished can be dropped. `noise` entries
        describe the explainer rather than the code and never go stale.
        Judgment stays with /groom; this only finds the candidates.
        """
        n = 0
        if not ENOLA_VERDICTS.exists():
            return 0
        try:
            entries = json.loads(ENOLA_VERDICTS.read_text()).get("entries") or []
        except json.JSONDecodeError:
            findings.append("ledger-hygiene: finding-verdicts.json unparseable")
            return 1
        # Signatures carry the owning repo, and attribution comes from a
        # symbol index built from the last repo's fact file. Without it,
        # attribution degrades to "(unattributed)" and every signature
        # shifts — so verdicts stop matching for reasons that have nothing
        # to do with the code. Judge nothing rather than judge wrongly.
        if not _enola_symbol_repo_index():
            return 0
        live = {f["signature"] for f in _enola_findings()}
        if not live:
            return 0  # no snapshot on this machine — say nothing
        searched, _ = _enola_snapshotted_repos()
        for entry in entries:
            if entry.get("verdict") == "noise" or not entry.get("signature"):
                continue
            if entry["signature"] in live:
                continue
            # signature is "<explainer>:<repo>:<anchor>" — a verdict whose
            # repo was never searched is unknown, not stale. Without this
            # the detector reports every verdict for a repo whose snapshot
            # is merely absent.
            parts = entry["signature"].split(":")
            if len(parts) > 1 and parts[1] not in searched:
                continue
            where = f" (cited at {entry['cited_at']})" if entry.get("cited_at") else ""
            findings.append(
                f"ledger-hygiene: {entry['verdict']} verdict on "
                f"{entry['signature']} but the finding is gone from the "
                f"graph{where} — re-judge or drop")
            n += 1
        return n

    def check_compiled_claims() -> int:
        """Structured claims: frontmatter evaluated against the graph
        artifacts. Failures report; not-asked is a named skip, never a pass.
        """
        n = 0
        skipped = 0
        repo_paths = {p.name: p for p in _enola_repos()}
        for rel, c in _wiki_claims():
            verdict, detail = _eval_claim(c, repo_paths)
            if verdict in ("fail", "malformed"):
                findings.append(f"compiled-claims: {rel}: {detail}")
                n += 1
            elif verdict == "not-asked":
                skipped += 1
        if skipped:
            print(f"# compiled-claims: {skipped} claim(s) not asked (no artifacts)",
                  file=sys.stderr)
        return n

    def check_intent_compile_drift() -> int:
        """The cluster config's fenced intent block must equal what the wiki
        declares — the corpus is generated, and drift means someone edited
        the artifact instead of the source.
        """
        _, errors = _wiki_declares()
        n = 0
        for e in errors:
            findings.append(f"intent-compile-drift: {e}")
            n += 1
        if ENOLA_CONFIG.exists():
            text = ENOLA_CONFIG.read_text()
            if INTENT_FENCE_BEGIN in text or re.search(r"^intent:", text, re.M):
                findings.append("intent-compile-drift: the cluster config carries an intent block, "
                                "but the wiki is the single source (intent: frontmatter, exported by tabula and "
                                "compiled by enola's mdintent extractor) — delete it")
                n += 1
        return n

    def check_export_current() -> int:
        """No page carries a derived engine block, and the export cardo reads
        is current. Pages hold only what a person writes under intent:; tabula
        export writes the frontmatter-only mirror and enola/constraints/ from
        them (wiki/tabula/adrs/tabula-authors-cardo-reads.tabula). A page with
        a derived enola_intent.page block, or a half under both keys with
        different content, is a finding everywhere; whether the mirror is
        current is asked of `tabula export --check` where tabula is present,
        compared against brain.py's twin where only the mirror is, and named
        as not asked where neither is (CI, a fresh clone).
        """
        n = 0
        for page in wiki_files():
            rel = page.relative_to(WIKI)
            if rel.parts[0] in ("_views", "_archive"):
                continue
            parsed = parse(page)
            if not parsed:
                continue
            meta, _ = parsed
            _derived, errors = _derive_page_block(rel, meta)
            for e in errors:
                findings.append(f"export-current: {e}")
                n += 1
            old = meta.get(OLD_INTENT_KEY)
            if isinstance(old, dict) and "page" in old:
                findings.append(f"export-current: {rel}: carries a derived {OLD_INTENT_KEY}.page "
                                "block; pages hold only intent: — run `brain.py intent stamp`")
                n += 1
            _halves, refused = _intent_halves(meta)
            if refused:
                findings.append(f"export-current: {rel}: {refused}")
                n += 1
        if _tabula_bin() is not None:
            out = subprocess.run([_tabula_bin(), "--root", str(REPO), "export", "--check"],
                                 capture_output=True, text=True)
            if out.returncode != 0:
                said = (out.stderr.strip() or out.stdout.strip()).splitlines()
                findings.append("export-current: tabula export --check: "
                                + (said[0] if said else f"exit {out.returncode}")
                                + " — run `brain.py export`")
                n += 1
        elif _export_mirror_dir().is_dir():
            files, _notes, refused = _export_plan()
            if not refused:
                for p, b in files.items():
                    if not p.exists() or p.read_bytes() != b:
                        findings.append(f"export-current: {os.path.relpath(p, REPO)}: "
                                        "stale — run `brain.py export`")
                        n += 1
                        break
        else:
            print("# export-current: mirror not asked: no tabula that knows `export` "
                  "and no mirror on disk", file=sys.stderr)
        return n

    def check_success_metrics_checked() -> int:
        """Advisory: a shipped PRD that states success metrics has them
        quoted, with a verdict each, in its ADR's build notes.

        Matches the exact heading `### Success metrics, checked` rather than
        prose: the measurement that motivated this (4 of 73 build notes
        "mention" the metrics, 2026-09-21) was a prose match, which is how a
        passing mention gets counted as a check. Reports, never fails. Per
        wiki/brain/adrs/success-metrics-get-checked.md."""
        load_pages()
        n = 0
        frozen = 0
        for entry in pages_data:
            rel = entry["path"]
            parts = Path(rel).parts
            if "prds" not in parts or "ai-suggestions" in parts:
                continue
            if str(entry["meta"].get("status", "")).strip() != "superseded":
                continue
            if not re.search(r"^## Success metrics\s*$", entry["body"], re.MULTILINE):
                continue
            if parts[0] in FROZEN_REPOS:
                frozen += 1
                continue
            adr_rel = str(Path(*[("adrs" if x == "prds" else x) for x in parts]))
            adr = pages_index.get(adr_rel)
            if adr is None:
                findings.append(f"success-metrics-checked: {rel}: shipped with success "
                                f"metrics and no ADR at {adr_rel} to carry the check")
                n += 1
            elif not re.search(r"^### Success metrics, checked\s*$", adr["body"], re.MULTILINE):
                findings.append(f"success-metrics-checked: {rel}: shipped with success "
                                f"metrics; {adr_rel} has no `### Success metrics, checked` block")
                n += 1
        if frozen:
            # A frozen shelf's code is closed to the operator, so its metrics
            # cannot be observed; a finding there could never be acted on.
            print(f"# success-metrics-checked: skipped {frozen} shipped PRD(s) "
                  f"on frozen shelves, their code not reachable", file=sys.stderr)
        return n

    runners = {
        "links": check_links,
        "confidence-floor": check_confidence_floor,
        "active-scope": check_active_scope,
        "supersedes-cycles": check_supersedes_cycles,
        "page-size": check_page_size,
        "sources-exist": check_sources_exist,
        "sync-drift": check_sync_drift,
        "epic-children": check_epic_children,
        "sources-immutability": check_sources_immutability,
        "repo-claims": check_repo_claims,
        "receipt-citations": check_receipt_citations,
        "archived-liveness": check_archived_liveness,
        "ledger-hygiene": check_ledger_hygiene,
        "compiled-claims": check_compiled_claims,
        "intent-compile-drift": check_intent_compile_drift,
        "export-current": check_export_current,
        "success-metrics-checked": check_success_metrics_checked,
    }
    # Advisory detectors report and are left out of the total that decides
    # the exit status. A finding nobody must act on must not fail CI.
    advisory = {"success-metrics-checked"}

    if which == "all":
        targets = list(runners)
    elif which in runners:
        targets = [which]
    else:
        print(f"unknown reflection-check: {which!r}", file=sys.stderr)
        print(f"available: all, {', '.join(runners)}", file=sys.stderr)
        return 2

    total = 0
    for name in targets:
        before = len(findings)
        runners[name]()
        delta = len(findings) - before
        if name in advisory:
            print(f"# {name}: {delta} finding(s) (advisory, not counted)", file=sys.stderr)
            continue
        print(f"# {name}: {delta} finding(s)", file=sys.stderr)
        total += delta

    for f in findings:
        print(f)

    print(f"# reflection-check {which}: {total} total finding(s)", file=sys.stderr)
    if getattr(args, "observe", False):
        return 0
    return 0 if total == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="brain")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="check frontmatter conformance").set_defaults(
        func=cmd_validate
    )

    ap_check = sub.add_parser("check",
                              help="verify sources: citations resolve")
    ap_check.add_argument("--no-net", action="store_true",
                          help="skip URL checks")
    ap_check.add_argument("--page",
                          help="only check one page (wiki-relative path)")
    ap_check.add_argument("-v", "--verbose", action="store_true",
                          help="list skipped (sibling-repo) citations")
    ap_check.set_defaults(func=cmd_check)

    ap_intent = sub.add_parser("intent",
                               help="wiki-native intent: validate (compile) or stamp page declarations")
    ap_intent.add_argument("op", choices=["compile", "stamp"])
    ap_intent.set_defaults(func=cmd_intent)
    ap_export = sub.add_parser("export",
                               help="write the mirror and constraints cardo reads (delegates to tabula export)")
    ap_export.add_argument("--check", action="store_true",
                           help="write nothing; exit 1 naming the first stale file")
    ap_export.add_argument("--python", action="store_true",
                           help="use brain.py's twin even when tabula is present")
    ap_export.set_defaults(func=cmd_export)
    sub.add_parser("stats", help="corpus health").set_defaults(func=cmd_stats)
    ap_att = sub.add_parser("attention",
                            help="attention card store (mechanical refresh)")
    ap_att.add_argument("op", nargs="?", default="refresh",
                        choices=["refresh", "list", "verify"])
    ap_att.set_defaults(func=cmd_attention)
    ap_sweep = sub.add_parser("pr-sweep",
                              help="every review surface of a sibling PR in "
                                   "one call (comments, reviews, CI, state)")
    ap_sweep.add_argument("pr", type=int)
    ap_sweep.add_argument("--repo", required=True,
                          help="sibling repo the PR belongs to")
    ap_sweep.add_argument("--full", action="store_true",
                          help="print full comment bodies")
    ap_sweep.set_defaults(func=cmd_pr_sweep)
    sub.add_parser("views", help="emit auto-generated index pages").set_defaults(
        func=cmd_views
    )

    ap_cov = sub.add_parser("coverage", help="repo coverage gap analysis")
    ap_cov.add_argument("repo", help="sibling repo name (under $BRAIN_PROJECTS_ROOT, default ~/projects/)")
    ap_cov.set_defaults(func=cmd_coverage)

    ap_serve = sub.add_parser("serve", help="read-only HTTP API")
    ap_serve.add_argument("--host", default="127.0.0.1")
    ap_serve.add_argument("--port", type=int, default=8765)
    ap_serve.set_defaults(func=cmd_serve)

    ap_prom = sub.add_parser("promote", help="scaffold initiative from insight")
    ap_prom.add_argument("insight", help="wiki-relative path to insight page")
    ap_prom.add_argument("--slug", help="initiative slug (default: <insight>-initiative)")
    ap_prom.set_defaults(func=cmd_promote)

    ap_cl = sub.add_parser("cluster", help="TF-IDF + HDBSCAN clustering")
    ap_cl.add_argument("--min-cluster", type=int, default=2,
                       help="HDBSCAN min_cluster_size (default 2)")
    ap_cl.add_argument("--min-corpus", type=int, default=10,
                       help="skip if fewer than this many pages (default 10)")
    ap_cl.set_defaults(func=cmd_cluster)

    sub.add_parser("check-no-notion-writes",
                   help="enforce Notion read-only doctrine"
                   ).set_defaults(func=cmd_check_no_notion_writes)

    ap_chf = sub.add_parser("check-home-fresh",
                            help="verify wiki/ edits include a wiki/index.md edit")
    ap_chf.add_argument("--base", default="origin/main",
                        help="base ref for the diff (default: origin/main)")
    ap_chf.set_defaults(func=cmd_check_home_fresh)

    ap_crf = sub.add_parser("check-readme-fresh",
                            help="verify significant changes include a README.md edit")
    ap_crf.add_argument("--base", default="origin/main",
                        help="base ref for the diff (default: origin/main)")
    ap_crf.set_defaults(func=cmd_check_readme_fresh)

    ap_sc = sub.add_parser("sync-cursor",
                           help="manage sibling-repo sync cursors "
                                "(wiki/_state/sync-cursors.json)")
    sc_sub = ap_sc.add_subparsers(dest="op", required=True)
    sc_get = sc_sub.add_parser("get",
                               help="print cursor(s); omit <repo> to print all")
    sc_get.add_argument("repo", nargs="?",
                        help="sibling repo name (e.g. website)")
    sc_set = sc_sub.add_parser("set",
                               help="advance cursor to sibling repo's HEAD")
    sc_set.add_argument("repo")
    sc_set.add_argument("--scope", default=None,
                        help="full-tree | <relative path> (default: full-tree)")
    sc_set.add_argument("--synced-by", dest="synced_by", default=None,
                        help="audit reference (PR # or log line) for this advance")
    sc_set.add_argument("--force", action="store_true",
                        help="override sibling-repo-handling refusal "
                             "(branch != main, dirty tree)")
    sc_diff = sc_sub.add_parser("diff",
                                help="list paths changed in sibling repo since "
                                     "the cursor's SHA")
    sc_diff.add_argument("repo")
    ap_sc.set_defaults(func=cmd_sync_cursor)

    ap_en = sub.add_parser("enola",
                           help="architecture-graph wrapper "
                                "(receipts at wiki/_state/enola/)")
    en_sub = ap_en.add_subparsers(dest="op", required=True)
    en_gen = en_sub.add_parser("generate",
                               help="snapshot the cluster and record receipts")
    en_gen.add_argument("--per-repo", action="store_true",
                        help="instead of the cluster, give each repository its "
                             "own single-repo graph in its own .enola")
    en_gen.add_argument("--refresh", metavar="REPO",
                        help="re-read one repository (as repos: names it, e.g. "
                             "../website) into the existing union, replacing "
                             "its slice; the rest of the cluster is not re-read")
    en_receipt = en_sub.add_parser("receipt",
                                   help="print recorded receipt(s)")
    en_receipt.add_argument("repo", nargs="?",
                            help="repo name (e.g. website)")
    en_sub.add_parser("diff",
                      help="report architecture drift vs recorded receipts")
    en_sub.add_parser("metrics",
                      help="Lakos coupling suite per language subgraph, ranked "
                           "within the estate")
    en_sub.add_parser("excludes",
                      help="hide artifact dirs from git per clone "
                           "(.git/info/exclude, never a tracked .gitignore)")
    en_sub.add_parser("pollution",
                      help="name repositories whose own .enola holds another "
                           "repository's facts")
    en_sub.add_parser("citations",
                      help="inventory receipt citations in wiki prose "
                           "with verdicts")
    en_base = en_sub.add_parser("baseline",
                                help="pin/show/clear the diff baseline a "
                                     "check grades against")
    en_base.add_argument("baseline_op", nargs="?", default="show",
                         choices=["pin", "show", "clear"])
    en_base.add_argument("repo", nargs="?", help="repo name (default: cluster)")
    en_check = en_sub.add_parser("check",
                                 help="grade a change against the pinned "
                                      "baseline — reported, never a gate")
    en_check.add_argument("repo", nargs="?", help="repo name (default: cluster)")
    en_cov = en_sub.add_parser("coverage",
                               help="which cross-repo edges resolved, so an "
                                    "isolated service reads apart from an "
                                    "unfollowable one")
    en_cov.add_argument("repo", nargs="?", help="repo name (default: cluster)")
    en_sub.add_parser("doctor",
                      help="report whether the session hooks are firing, "
                           "not merely configured")
    en_exp = en_sub.add_parser("explain",
                               help="human-readable repository statistics")
    en_exp.add_argument("repo", nargs="?", help="repo name (default: cluster)")
    en_hist = en_sub.add_parser("history",
                                help="EXPERIMENTAL — when something entered "
                                     "or left the architecture")
    en_hist.add_argument("history_op", nargs="?", default="log",
                         choices=["log", "show", "diff", "blame", "gc"])
    en_hist.add_argument("pattern", nargs="?",
                         help="revision for show/diff, name or path for blame")
    en_hist.add_argument("repo", nargs="?", help="repo name (default: cluster)")
    en_trend = en_sub.add_parser("trend",
                                 help="per-repo finding counts over the "
                                      "committed receipts history")
    en_trend.add_argument("--repo", default=None, help="narrow to one repo")
    en_trend.add_argument("--last", type=int, default=10,
                          dest="last",
                          help="how many receipt commits to walk "
                               "(default 10)")
    en_find = en_sub.add_parser("findings",
                                help="merged explainer findings across the "
                                     "cluster, noise and rejections hidden")
    en_find.add_argument("--repo", default=None, help="narrow to one repo")
    en_find.add_argument("--explainer", default=None,
                         help="narrow to one explainer (e.g. god-class)")
    en_find.add_argument("--min-confidence", type=float, default=None,
                         dest="min_confidence")
    en_find.add_argument("--all", action="store_true",
                         help="include findings already judged noise "
                              "or rejected")
    en_find.add_argument("--json", action="store_true")
    en_judge = en_sub.add_parser("judge",
                                 help="record a verdict for one finding "
                                      "signature")
    en_judge.add_argument("signature")
    en_judge.add_argument("verdict",
                          help=f"one of {', '.join(ENOLA_VERDICT_KINDS)}")
    en_judge.add_argument("--why", required=True,
                          help="the reason, in a sentence")
    en_judge.add_argument("--cited-at", default=None, dest="cited_at",
                          help="wiki path where an accepted finding landed")
    en_impact = en_sub.add_parser("impact",
                                  help="fan-in / fan-out / callers for a "
                                       "symbol, from the on-disk fact set")
    en_impact.add_argument("symbol")
    en_impact.add_argument("--limit", type=int, default=20)
    en_govern = en_sub.add_parser("govern",
                                  help="which compiled pages govern a file "
                                       "or symbol — and which code a page "
                                       "governs — from the on-disk fact set")
    en_govern.add_argument("target", nargs="?")
    en_govern.add_argument("--pr", type=int,
                           help="review mode: resolve the PR's changed files "
                                "and report the union of governing pages")
    en_govern.add_argument("--repo", default=None,
                           help="sibling repo the PR belongs to "
                                "(required with --pr)")
    ap_en.set_defaults(func=cmd_enola)

    ap_eff = sub.add_parser("efforts",
                            help="manage in-flight effort registry "
                                 "(wiki/_state/efforts/<slug>.json)")
    eff_sub = ap_eff.add_subparsers(dest="op", required=True)
    eff_list = eff_sub.add_parser("list", help="list all effort records")
    eff_list.add_argument("--status", default=None,
                          help="filter by status (in-flight | merged | abandoned | orphaned)")
    eff_list.add_argument("--json", action="store_true",
                          help="emit JSON instead of the tab-separated table")
    eff_get = eff_sub.add_parser("get", help="print one effort record as JSON")
    eff_get.add_argument("slug")
    eff_set = eff_sub.add_parser("set", help="create or update an effort record")
    eff_set.add_argument("slug")
    eff_set.add_argument("--brain-branch", default=None)
    eff_set.add_argument("--brain-worktree", default=None,
                         help="absolute path to the brain worktree")
    eff_set.add_argument("--targets", nargs="*", default=None,
                         help="target sibling repos (e.g. website cfp-tool)")
    eff_set.add_argument("--target-branch", action="append", dest="target_branches",
                         type=lambda s: tuple(s.split("=", 1)), default=None,
                         metavar="REPO=BRANCH",
                         help="repeatable: per-target sibling-repo branch")
    eff_set.add_argument("--target-worktree", action="append", dest="target_worktrees",
                         type=lambda s: tuple(s.split("=", 1)), default=None,
                         metavar="REPO=PATH",
                         help="repeatable: per-target sibling-repo worktree path")
    eff_set.add_argument("--brain-pr", default=None,
                         help="brain PR URL or number")
    eff_set.add_argument("--target-pr", action="append", dest="target_prs",
                        type=lambda s: tuple(s.split("=", 1)), default=None,
                        metavar="REPO=PR",
                        help="repeatable: per-target sibling-repo PR URL or number")
    eff_set.add_argument("--notes", default=None)
    eff_set.add_argument("--status", default=None,
                         choices=["in-flight", "merged", "abandoned", "orphaned"])
    eff_set.add_argument("--owner-agent-id", dest="owner_agent_id", default=None,
                         help="opaque identifier of the dispatched owner subagent "
                              "(per parallel-execution-agent-teams ADR)")
    eff_set.add_argument("--owner-dispatched-at", dest="owner_dispatched_at",
                         default=None,
                         help="ISO-8601 UTC timestamp the owner subagent was dispatched")
    eff_set.add_argument("--owner-state", dest="owner_state", default=None,
                         choices=["active", "completed", "blocked", "none-dispatched"],
                         help="lifecycle state of the dispatched owner subagent")
    eff_set.add_argument("--helpers-dispatched", dest="helpers_dispatched",
                         type=int, default=None,
                         help="count of helper subagents the owner has fanned out")
    eff_set.add_argument("--bound", default=None, metavar='"N rounds|minutes"',
                         help="the owner's bound, recorded at dispatch")
    eff_set.add_argument("--tokens", action="append", default=None, metavar="TIER=N",
                         help="repeatable: tokens a tier (strong | small) spent, as "
                              "the harness reported them; summed per tier")
    eff_resume = eff_sub.add_parser("resume",
                                    help="raise an exhausted owner's bound; the same "
                                         "owner continues, the old bound is kept")
    eff_resume.add_argument("slug")
    eff_resume.add_argument("--bound", required=True, metavar='"N rounds|minutes"')
    eff_mark = eff_sub.add_parser("mark", help="set an effort's status")
    eff_mark.add_argument("slug")
    eff_mark.add_argument("status",
                          choices=["in-flight", "merged", "abandoned", "orphaned"])
    ap_eff.set_defaults(func=cmd_efforts)

    ap_reb = sub.add_parser("rebase",
                            help="cheap-rebase current branch onto origin/main, "
                                 "auto-resolving wiki/_views/ via regen")
    ap_reb.add_argument("--base", default="origin/main",
                        help="base ref (default: origin/main)")
    ap_reb.set_defaults(func=cmd_rebase)

    sub.add_parser("snapshot",
                   help="write a brain corpus snapshot to wiki/_views/snapshots/"
                   ).set_defaults(func=cmd_snapshot)

    sub.add_parser("rotate-log",
                   help="rotate log/log.md to log/archive/ once it crosses the threshold"
                   ).set_defaults(func=cmd_rotate_log)

    ap_pers = sub.add_parser("personas",
                             help="infer the RFC persona pool for a wiki page")
    ap_pers.add_argument("page", help="wiki-relative path to the page")
    ap_pers.set_defaults(func=cmd_personas)

    ap_scope = sub.add_parser(
        "scope",
        help="manage the active-scope registration of sibling repos"
    )
    scope_sub = ap_scope.add_subparsers(dest="op", required=True)
    ap_scope_add = scope_sub.add_parser(
        "add",
        help="register a repo as active in the AGENTS.md scope and sibling tables, "
             "ACTIVE_REPOS and the README (idempotent)"
    )
    ap_scope_add.add_argument("repo", help="local directory name under the projects root")
    ap_scope_add.add_argument("--desc", required=True,
                              help="one or two sentences for the sibling table row")
    ap_scope_add.add_argument("--tier", choices=sorted(SCOPE_TIERS), default="active",
                              help="active (the estate modifies it), reference (outside "
                                   "code read for what it teaches) or frozen (closed to "
                                   "the operator; shelf true as of a date). Default: active")
    ap_scope_add.add_argument("--dry-run", action="store_true",
                              help="report which surfaces would change without writing")
    ap_scope_tier = scope_sub.add_parser(
        "tier", help="move one repo to another scope tier on every surface")
    ap_scope_tier.add_argument("repo")
    ap_scope_tier.add_argument("tier", choices=sorted(SCOPE_TIERS))
    ap_scope_tier.add_argument("--dry-run", action="store_true")
    ap_scope.set_defaults(func=cmd_scope)

    ap_inst = sub.add_parser(
        "install-sibling",
        help="install the brain's managed block + PreToolUse hook into a sibling repo "
             "(idempotent; --uninstall to remove)"
    )
    ap_inst.add_argument("repo", nargs="?",
                         help="sibling repo name (e.g. website); omit with --all")
    ap_inst.add_argument("--all", dest="all_active", action="store_true",
                         help="install into every active sibling repo on disk")
    ap_inst.add_argument("--uninstall", action="store_true",
                         help="remove the managed block + hook + settings entry")
    ap_inst.add_argument("--dry-run", action="store_true",
                         help="print what would be written without modifying disk")
    ap_inst.set_defaults(func=cmd_install_sibling)

    sub.add_parser(
        "status",
        help="brain-wide status dashboard (reads wiki/_state/*.json + corpus)"
    ).set_defaults(func=cmd_status)

    ap_verify = sub.add_parser(
        "verify-claims",
        help="extract verifiable claims (paths, version-pins, identifiers) "
             "from a wiki page; emit a structured manifest the consumer "
             "(agent / LLM / operator) can verify against sibling-repo source"
    )
    ap_verify.add_argument("page",
                           help="wiki-relative path (e.g. website/permanent/architecture/index.md)")
    ap_verify.add_argument("--no-net", action="store_true", dest="no_net",
                           help="skip network verifications (pr-state degrades "
                                "to needs-verification)")
    ap_verify.add_argument("--json", action="store_true",
                           help="emit JSON for tool consumers")
    ap_verify.set_defaults(func=cmd_verify_claims)

    ap_sched = sub.add_parser(
        "schedule",
        help="manage the declarative schedule at brain-schedule.yml"
    )
    ap_sched.add_argument("op", nargs="?", default="list",
                          choices=["list", "run", "run-due"],
                          help="list (default) | run --target <op> | run-due")
    ap_sched.add_argument("--target",
                          help="operation name when op=run")
    ap_sched.set_defaults(func=cmd_schedule)

    ap_init = sub.add_parser(
        "init",
        help="scaffold an empty brain shell at <path> (AGENTS.md + wiki/ "
             "skeleton + log/ + sources/) — for new organisations adopting "
             "the brain pattern"
    )
    ap_init.add_argument("path", help="directory to scaffold the brain into")
    ap_init.add_argument("--org", default=None,
                         help="organisation name (default: '<your-organisation>')")
    ap_init.add_argument("--force", action="store_true",
                         help="scaffold even if the target directory is non-empty")
    ap_init.set_defaults(func=cmd_init)

    ap_search = sub.add_parser(
        "search",
        help="keyword search over the wiki/ synthesis layer "
             "(BM25, weighted by search.factors and confidence tier)"
    )
    ap_search.add_argument("query", help="search terms")
    ap_search.add_argument("--top", type=int, default=10,
                           help="max results to return (default: 10)")
    ap_search.add_argument("--repo",
                           help="filter to pages about/affecting this repo")
    ap_search.add_argument("--kind",
                           choices=["reference", "initiative", "decision", "entity",
                                    "meta", "overlap", "insight", "epic"],
                           help="filter to pages of this kind")
    ap_search.add_argument("--include-superseded", action="store_true",
                           help="include superseded/archived pages")
    ap_search.add_argument("--semantic", action="store_true",
                           help="rank by a typed judgment (TypeSafe) per candidate page "
                                "instead of keywords; needs TYPESAFE_API_KEY, costs about "
                                "0.002 USD and 4-8 s a query, falls back to keyword ranking "
                                "with a named skip. Never use from a hook")
    ap_search.add_argument("--json", action="store_true",
                           help="emit JSON output (for tool consumers)")
    ap_search.set_defaults(func=cmd_search)

    ap_refl = sub.add_parser(
        "reflection-check",
        help="detect drift between brain claims and target-repo state "
             "(links, confidence-floor age, active-scope, supersedes-cycles, "
             "page-size, sources-exist). Surfaces findings; exit 1 if any."
    )
    ap_refl.add_argument("which", nargs="?", default="all",
                         help="which check to run: links | confidence-floor | "
                              "active-scope | supersedes-cycles | page-size | "
                              "sources-exist | sync-drift | epic-children | "
                              "sources-immutability | repo-claims | "
                              "success-metrics-checked (advisory: reported, "
                              "never counted toward the exit status) | all "
                              "(default: all)")
    ap_refl.add_argument("--observe", action="store_true",
                         help="surface findings but exit 0 — for scheduled "
                              "observe-only runs where findings are data to "
                              "record, not a failure; genuine errors still "
                              "exit nonzero")
    ap_refl.set_defaults(func=cmd_reflection_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
