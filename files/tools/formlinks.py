#!/usr/bin/env python3
"""The site's form links: write them into the pages, and check them.

Every link to a form on the site is an anchor with data-form="<key>", where
<key> is one of the keys in forms.yml (talk, add, register, contact).
forms.yml holds the published URLs: Google Forms, or for registration the
Luma event. This tool copies them into the pages so the site stays plain
HTML. A Luma event link also gets data-luma-action and data-luma-event-id,
so Luma's checkout script opens registration over the page.

  links            write every data-form anchor's href from forms.yml
  check            fail if an anchor's href differs from forms.yml, or an
                   anchor names a key forms.yml does not have
  check --publish  also fail while any form URL is still empty

Usage: python3 tools/formlinks.py <links|check> [--publish]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
FORMS = ROOT / "forms.yml"
PENDING = "contact.html#forms-pending"
ANCHOR = re.compile(r'<a\b([^>]*?)\bdata-form="([a-z]+)"([^>]*)>')
HREF = re.compile(r'\bhref="[^"]*"')
URL = re.compile(r"^https://(docs\.google\.com/forms/|forms\.gle/|luma\.com/event/evt-[A-Za-z0-9]+$)")
LUMA = re.compile(r"^https://luma\.com/event/(evt-[A-Za-z0-9]+)$")
LUMA_ATTRS = re.compile(r'\s*\bdata-luma-(?:action|event-id)="[^"]*"')


def forms() -> dict:
    data = yaml.safe_load(FORMS.read_text(encoding="utf-8")) or {}
    return {k: (v or "").strip() for k, v in data.items()}


def target(urls: dict, key: str) -> str:
    return urls.get(key) or PENDING


def anchor(tag: str, url: str) -> str:
    href = f'href="{url}"'
    tag = HREF.sub(href, tag, count=1) if HREF.search(tag) else tag.replace("<a ", f"<a {href} ", 1)
    tag = LUMA_ATTRS.sub("", tag)
    luma = LUMA.match(url)
    if luma:
        tag = tag[:-1] + f' data-luma-action="checkout" data-luma-event-id="{luma.group(1)}">'
    return tag


def rewrite(text: str, urls: dict) -> str:
    return ANCHOR.sub(lambda m: anchor(m.group(0), target(urls, m.group(2))), text)


def pages():
    return sorted(SITE.glob("*.html"))


def cmd_links(_args) -> int:
    urls = forms()
    for p in pages():
        old = p.read_text(encoding="utf-8")
        new = rewrite(old, urls)
        if new != old:
            p.write_text(new, encoding="utf-8")
            print(f"updated site/{p.name}")
    return 0


def cmd_check(args) -> int:
    urls = forms()
    bad = []
    for key, url in urls.items():
        if url and not URL.match(url):
            bad.append(f"forms.yml: {key} is not a Google Forms or Luma event URL: {url}")
    used = set()
    for p in pages():
        text = p.read_text(encoding="utf-8")
        for m in ANCHOR.finditer(text):
            key = m.group(2)
            used.add(key)
            if key not in urls:
                bad.append(f"{p.name}: data-form=\"{key}\" is not a key in forms.yml")
                continue
            if m.group(0) != anchor(m.group(0), target(urls, key)):
                bad.append(f"{p.name}: the {key} link is out of date: run python3 tools/formlinks.py links")
    if args.publish:
        for key in sorted(used):
            if not urls.get(key):
                bad.append(f"forms.yml: {key} has no URL yet; publish the form and paste its responder link (tools/google-forms/README.md)")
    for b in bad:
        print(b)
    print(f"site links: {len(bad)} problem(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("links")
    c = sub.add_parser("check")
    c.add_argument("--publish", action="store_true")
    args = ap.parse_args(argv)
    return cmd_links(args) if args.cmd == "links" else cmd_check(args)


if __name__ == "__main__":
    sys.exit(main())
