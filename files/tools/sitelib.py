"""Helpers the site's generators share: records, frontmatter, escaping, and
writing or checking the pages they build.

(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

import frame
import images


def records(folder: Path, paths=None) -> list[Path]:
    """The record files in a folder, or the paths given; README.md and files starting with "_" are not records."""
    if paths:
        return [Path(p) for p in paths]
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.md") if p.name != "README.md" and not p.name.startswith("_"))


def parse(path: Path):
    """A record's frontmatter, its body, and what is wrong with them."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text, ["no frontmatter block"]
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as err:
        return None, m.group(2), [f"frontmatter is not valid YAML ({err.__class__.__name__})"]
    return meta, m.group(2).strip(), []


def esc(v) -> str:
    return html.escape(str(v))


def prune(found, pages: dict, check: bool, tool: str, why: str) -> int:
    """Remove (or, when checking, report) built pages that no record asks for any more."""
    stale = 0
    for old in found:
        if old in pages:
            continue
        if check:
            print(f"site/{old.name} {why}: run python3 {tool}")
            stale += 1
        else:
            old.unlink()
            print(f"removed site/{old.name}")
    return stale


def write_or_check(pages: dict, check: bool, tool: str) -> int:
    """Write each page in the shared frame, its photos wrapped for WebP; when checking, count the pages that differ."""
    stale = 0
    for path, want in pages.items():
        want = images.wrap(frame.frame(want))
        if check:
            have = path.read_text(encoding="utf-8") if path.exists() else ""
            if have != want:
                print(f"site/{path.name} is out of date: run python3 {tool}")
                stale += 1
            else:
                print(f"site/{path.name} is current")
        else:
            path.write_text(want, encoding="utf-8")
            print(f"wrote site/{path.name}")
    return stale
