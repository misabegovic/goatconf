# Supporters

One Markdown file per company that supports GoatConf. Most are online
supporters: one level, 500 EUR plus VAT where it applies, invoiced by the
organiser's Austrian business, with nothing at the venue. A company may
instead pay a supplier directly for one named thing, or give in kind. No
supporter pays for a named speaker's travel. Name the file after the
company in lowercase words joined by hyphens. Copy `_template.md` to start
one.

- `name`, `url`: required.
- `logo`: required, the supporter's logo saved under
  `site/img/supporters/` (SVG or PNG on a transparent or white background).
- `funds`: required, how they support, in plain words, for example
  "Online supporter" or "The printing, paid to the printer".

Run `python3 tools/speakers.py build`; the local CI checks it.
