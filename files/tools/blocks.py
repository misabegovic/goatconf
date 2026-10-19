"""The one way a page marks a part a tool writes:

    <!-- gen:NAME tools/TOOL.py -->
    ...
    <!-- /gen:NAME -->

The opening comment names the part and the tool that owns it, so whoever
edits a page by hand knows what is written over and by what.

(ADR wiki/org/adrs/one-page-frame-and-one-site-build.md)
"""
from __future__ import annotations

import re


def marks(name: str, tool: str) -> tuple[str, str]:
    """The opening and closing comments of a part."""
    return f"<!-- gen:{name} {tool} -->", f"<!-- /gen:{name} -->"


def pattern(name: str, trailing_newline: bool = False) -> re.Pattern:
    """A part with its markers, whatever is inside it."""
    return re.compile(r"<!-- gen:" + re.escape(name) + r" [^>]*-->.*?<!-- /gen:" + re.escape(name) + r" -->"
                      + (r"\n?" if trailing_newline else ""), re.S)


def wrap(name: str, tool: str, body: str, sep: str = "\n") -> str:
    start, end = marks(name, tool)
    return f"{start}{sep}{body}{sep}{end}"


def fill(text: str, name: str, tool: str, body: str, where: str) -> str:
    """The text with the part's inside replaced; a page without the part is an error."""
    pat = pattern(name)
    if not pat.search(text):
        raise SystemExit(f"{where} has no {marks(name, tool)[0]} block")
    return pat.sub(lambda _m: wrap(name, tool, body), text, count=1)
