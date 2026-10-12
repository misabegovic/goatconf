# Supporters

One Markdown file per company that pays a named thing, such as a speaker's
travel, straight to the supplier (the charter: no money passes through the
organiser, and a supporter is thanked for exactly what they funded). Name
the file after the company in lowercase words joined by hyphens. Copy
`_template.md` to start one.

- `name`, `url`: required.
- `logo`: required, the supporter's logo saved under
  `site/img/supporters/` (SVG or PNG on a transparent or white background).
- `funds`: required, exactly what they pay for, in plain words, for
  example "Travel for two speakers" or "The travel grant pot".

Every payment also goes into `site/ledger.csv`. A speaker whose travel a
supporter paid names them with `travel_funded_by` in their record, and the
logo then shows on that speaker's profile too. Run
`python3 tools/speakers.py build`; the local CI checks it.
