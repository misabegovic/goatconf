# Supporters

One Markdown file per company that supports GoatConf. Most are online
supporters: one level, 500 EUR plus VAT where it applies, invoiced by the
organiser's Austrian business, with nothing at the venue. A company may
instead pay a supplier directly for one named thing, or give in kind. A
host (a person, group or company) that funds and organises an event the
organiser accepted is listed too, if it agrees, with a line naming the
event. A
community partner that gives in kind, such as by sharing GoatConf on
its social media, is listed the same way, with a line saying how it
helps. No
supporter pays for a named speaker's travel. Name the file after the
company in lowercase words joined by hyphens. Copy `_template.md` to start
one.

- `name`, `url`: required.
- `logo`: required, the supporter's logo saved under
  `site/img/supporters/` (SVG or PNG on a transparent or white background).
- `funds`: required, how they support, in plain words, for example
  "Online supporter" or "The printing, paid to the printer". Their
  "thank you" card reads "for funding" and this line; a line that starts
  with what they do, such as "Funding and organising the meetup", is used
  as it stands ("for funding and organising the meetup").
- `thanks`: optional, the last line of their "thank you" card exactly as
  written, in place of the one made from `funds`, for example "for
  funding and organising the meetup, as part of the official program of
  GoatConf 2027 in Tuzla." Only the card shows it.
- `host: yes`: optional, for the host and partner, IPI Academy. It is listed
  first, before every other supporter, and its "thank you" card thanks it for
  hosting.
- `support_them`: optional, ways people can support the supporter, each a
  short `text` and a `url` starting `https://`, shown on their profile under
  "How to support them", for example
  `- {text: "Become a monthly donor", url: "https://example.org/donate"}`.
- `events`: optional, for a host that funds and organises accepted events:
  their record names in `extensions/`, for example `[bh-professionals-meetup]`.
  The supporter's profile then shows those events and offers each event's
  card next to the thank-you card, and a link to the profile shows the
  first event's card as its preview.
- `logo_on: dark`: optional, for a logo made for a dark background (white
  lettering); it is shown on the site's dark blue. The default is `light`.

Each supporter gets a profile, `site/supporter-<file name>.html`, where they
download their thank-you card (square and wide), rendered with
`python3 tools/shareables.py render --only supporter-<file name>`. The
supporters page and the home page link to it.

Run `python3 tools/speakers.py build`; the local CI checks it, and fails while
a supporter's cards are missing.
