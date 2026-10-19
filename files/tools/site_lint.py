#!/usr/bin/env python3
"""The site's HTML, checked: what a broken page would show a visitor.

Reads every site/*.html with Python's own HTML parser and fails on:

  - tags that are not closed, or closed out of order
  - an id used twice on one page
  - a link, image or file inside the site that does not exist, or a
    #fragment that names no id on its page
  - an <img> with no alt attribute
  - a page without exactly one <h1> and one <main>, or with more than one
    banner (a <header> outside <main>, <article>, <aside>, <nav> and
    <section>)

Links to other sites, mail and phone links are not followed.

  check     print every problem; fail if there is one

Usage: python3 tools/site_lint.py check
(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SECTIONING = {"main", "article", "aside", "nav", "section"}
EXTERNAL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)


class Page(HTMLParser):
    def __init__(self, name: str):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.stack: list[tuple[str, int]] = []
        self.problems: list[str] = []
        self.ids: dict[str, int] = {}
        self.refs: list[tuple[str, int]] = []   # (url, line)
        self.h1 = self.main = self.banners = 0

    def where(self) -> int:
        return self.getpos()[0]

    def note(self, line: int, text: str) -> None:
        self.problems.append(f"site/{self.name}:{line}: {text}")

    def handle_starttag(self, tag, attrs, closed=False):
        a = dict(attrs)
        line = self.where()
        if "id" in a and a["id"] is not None:
            if a["id"] in self.ids:
                self.note(line, f'id "{a["id"]}" is used twice (first on line {self.ids[a["id"]]})')
            else:
                self.ids[a["id"]] = line
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append((a[key], line))
        for key in ("srcset",):
            if a.get(key):
                self.refs.extend((part.strip().split(" ")[0], line) for part in a[key].split(",") if part.strip())
        if tag == "img" and "alt" not in a:
            self.note(line, f'<img src="{a.get("src", "")}"> has no alt attribute')
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if tag == "header" and not any(t in SECTIONING for t, _ in self.stack):
            self.banners += 1
        if tag not in VOID and not closed:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.note(self.where(), f"</{tag}> closes nothing")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        if any(t == tag for t, _ in self.stack):
            while self.stack and self.stack[-1][0] != tag:
                t, line = self.stack.pop()
                self.note(line, f"<{t}> is not closed before </{tag}> on line {self.where()}")
            self.stack.pop()
        else:
            self.note(self.where(), f"</{tag}> closes nothing")

    def finish(self) -> None:
        self.close()
        for t, line in self.stack:
            if t not in ("html", "body", "head"):
                self.note(line, f"<{t}> is never closed")
        if self.h1 != 1:
            self.note(1, f"has {self.h1} <h1> elements, not one")
        if self.main != 1:
            self.note(1, f"has {self.main} <main> elements, not one")
        if self.banners > 1:
            self.note(1, f"has {self.banners} banners (<header> outside main and sections), not one")


def parse(path: Path) -> Page:
    page = Page(path.name)
    page.feed(path.read_text(encoding="utf-8"))
    page.finish()
    return page


def check_links(pages: dict[str, Page]) -> list[str]:
    problems = []
    for name, page in pages.items():
        for url, line in page.refs:
            if EXTERNAL.match(url) or url.startswith("data:"):
                continue
            parts = urlsplit(url)
            target_name = unquote(parts.path).lstrip("/") or (name if not parts.path else "index.html")
            if parts.path == "" or parts.path == "/":
                target_name = name if parts.path == "" else "index.html"
            target = SITE / target_name
            if target.is_dir():
                target = target / "index.html"
            if not target.exists() and not (SITE / f"{target_name}.html").exists():
                problems.append(f"site/{name}:{line}: {url} points to {target_name}, which does not exist")
                continue
            if parts.fragment:
                page_name = target.name if target.suffix == ".html" else f"{target_name}.html"
                other = pages.get(page_name)
                if other is not None and parts.fragment not in other.ids:
                    problems.append(f"site/{name}:{line}: {url} names #{parts.fragment}, which is not an id on {page_name}")
    return problems


def cmd_check(_args) -> int:
    pages = {p.name: parse(p) for p in sorted(SITE.glob("*.html"))}
    problems = [x for page in pages.values() for x in page.problems] + check_links(pages)
    for x in problems:
        print(x)
    if not problems:
        print(f"site HTML: {len(pages)} pages, no problems")
    return 1 if problems else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    args = ap.parse_args(argv)
    return cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
