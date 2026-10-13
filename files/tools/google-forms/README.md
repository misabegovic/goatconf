# The Google Forms behind goatconf.com

Three Google Forms take everything except registration, which is the Luma
event in `files/forms.yml`. The Luma event asks for a name and an email, and
one optional, multi-line question: why the person wants to come, to help the
organiser confirm registrations (added 2026-10-13). They were built by hand on 2026-10-12 and live,
with their response spreadsheets, in the organiser's GoatConf folder in
Google Drive (its link is kept out of this public repository).
The folder is shared with the organising team, so they see the responses
too, code of conduct reports from the contact form included; the privacy
question on the talk and add forms says so.

Their public links are in `files/forms.yml`. To change a form, edit it in
Drive; the link stays the same. If a form is ever replaced, paste its new
responder link (Publish, then Copy responder link) into `files/forms.yml`,
run `python3 files/tools/formlinks.py links`, then the local CI, and commit.

## GoatConf 2027: propose a session

Collects the respondent's email, sends them a copy of their answers, emails
the organiser on every response, and writes to the spreadsheet "GoatConf 2027
responses". It asks, in this order (required unless marked optional): title;
format (talk, panel, workshop, something else); what it is about; who it is
for (optional); discipline (engineering, design, product, founding a company,
or other); preferred day (Thursday 3 June, Friday 4 June, either); the name
or names of everyone speaking; a link about you (optional); whether it is
their first talk; their travel (optional): they need no travel support, their company
covers it and is then listed on the site as a supporter, or they pay their
own and would welcome a refund if the budget allows, never promised; anything to make it work for them (optional); a short bio
for a speaker profile (optional); whether a speaker profile may be
published if the session is accepted; the code of conduct; and consent to the
privacy notice. A speaker's photo comes later by email, once the session is
accepted (`files/speakers/README.md`).

The session comes before the name, so the spreadsheet can be read the same
way: hide the name columns while reading.

## GoatConf 2027: add something

The same email, copy and notification settings, with its own spreadsheet. It
asks, all required: the name of what is added; the kind (fringe event,
workshop, community hub, activity, another venue, support, hiring, something
else); the host; where; when it starts and ends (date and time); the cost for
people who join; how people join; who pays (and, for support, the supplier
paid directly); a public contact; a short description; acceptance of the
charter and the code of conduct; and consent to the privacy notice.

## GoatConf 2027: contact the organiser

Collects no email address, so a code of conduct report can be anonymous; it
emails the organiser on every response and has its own spreadsheet. It asks
what the message is about (a question, a code of conduct report, supporting
GoatConf, press, my data, or other), and then optionally a name and an email
for an answer, the message (required), and a news opt-in.

## After a response

- **A talk is accepted:** add a record to `files/program/` (see its
  README), run `python3 files/tools/program.py build`, commit.
- **An addition is accepted:** add a record to `files/extensions/` from the
  form's answers, run `python3 files/tools/extensions.py build` and
  `python3 files/tools/program.py build` (Saturday and the days around the
  talks are listed on the program), commit.
- Then merge to `main`: Railway publishes the site.
