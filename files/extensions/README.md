# Extensions

Everything around GoatConf's day of talks is added by the people who come:
a workshop, a meetup, a dinner, a city walk, a community corner, a supporter
paying for coffee. Each one is a short file in this folder, and the site's
extensions page is built from these files.

## Add yours

1. Copy `_template.md` to a new file named after your extension, in
   lowercase with dashes, for example `rust-meetup-at-the-lake.md`.
2. Fill in every field and write a few sentences below the second `---`
   about what it is and who it is for.
3. Open a pull request. An agent checks the file and comments what, if
   anything, needs a change; the organiser merges it.

No git? Fill in the extension form instead (it opens with the call for
talks) and a volunteer turns your answers into the same file.

## The fields

| Field | What to write |
|-------|---------------|
| `name` | The name of your extension. Not "GoatConf presents"; it is yours. |
| `kind` | One of `evening-event`, `trip`, `meetup`, `podcast`, `hike`, `hackathon`, `karaoke` (the kinds on the form), or `workshop`, `hub`, `activity`, `venue`, `support` (older kinds, still accepted). |
| `host` | You, your group or your company. |
| `location` | Where it happens, with an address. |
| `start`, `end` | `YYYY-MM-DD HH:MM`, or just `YYYY-MM-DD` for a whole day. |
| `cost` | What it costs to join, or `free`. |
| `registration` | A link, or `no registration`. |
| `paid_by` | Who covers its costs. GoatConf never does. |
| `supplier` | For `support` only: the supplier the supporter pays directly. |
| `contact` | A public contact you choose. It will be shown on the site. |
| `accepts` | `yes`: you accept the charter and the code of conduct. |
| `accepted` | Set to `yes` by the organiser only. Until then the record is not listed and is not part of GoatConf. |
| `outside_week_reason` | Only if your dates fall outside the GoatConf week: why. |

The rules every listing follows are on the charter page (`site/charter.html`):
the core never depends on an extension; only events the organiser accepts
become part of GoatConf and are listed, judged against the charter, the
code of conduct and how they fit the program; each is named as part of
GoatConf 2027 and run by its host; and each host carries its own costs and
risks.

## Checking and building

```
python3 tools/extensions.py check      # what the agent checks
python3 tools/extensions.py build      # rebuild site/extensions.html
```

The local CI runs both, so a record that fails the check, or a page that
was not rebuilt, stops the push.
