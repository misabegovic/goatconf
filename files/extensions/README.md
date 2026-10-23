# Extensions

Everything around GoatConf's two days of sessions is added by the people
who come: a workshop, a meetup, a dinner, a city walk, a community corner, a
supporter paying for coffee. Each one is a short file in this folder, and
the site's Make it yours page (`goatconf.com/extend`) lists the accepted
ones, with how to host, what to run, and places in Tuzla to ask.

## Add yours

1. Copy `_template.md` to a new file named after your extension, in
   lowercase with dashes, for example `rust-meetup-at-the-lake.md`. Once
   accepted, it gets its own page named after the file:
   `goatconf.com/event-rust-meetup-at-the-lake`.
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
| `kind` | One of `evening-event`, `trip`, `meetup`, `podcast`, `hike`, `hackathon`, `karaoke`, `other` (the kinds on the form; `other` is "Something else"), or `workshop`, `hub`, `activity`, `venue`, `support` (older kinds, still accepted). |
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

## When it can happen

Any day from 2 to 6 June 2027. On Thursday 3 and Friday 4 June the sessions
run all day, so an event those days is before or after them, or fits inside
one hour off: Thursday at 11:00, 13:00 or 15:00, Friday at 10:30 or 14:30.
An event in an hour off is free, and Friday's 12:30 hour stays free for
Džuma and lunch. The check enforces this, from the day times in
`tools/program.py`.

## Places to ask

`places/venues.yml` lists places in Tuzla a host could ask, shown on the
same page with filters. GoatConf has arranged nothing with them. Only places
the organiser approves (`approved: yes`) appear; each has its sources, its
distance from IPI Academy and, where one was found, a photo whose record sits
in `assets/images/venues/`.

## Checking and building

```
python3 tools/extensions.py check        # what the agent checks, events and venues
python3 tools/extensions.py build        # rebuild site/extend.html and each event's page
python3 tools/extensions.py build --all  # preview every venue, approved or not
```

The local CI runs both, so a record that fails the check, or a page that
was not rebuilt, stops the push.
