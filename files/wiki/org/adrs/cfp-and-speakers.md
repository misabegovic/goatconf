---
title: "Take talks through Google Forms and review them blind with a panel of two or three"
kind: decision
status: superseded
updated: 2026-10-12
confidence: medium
depends_on:
  - org/prds/cfp-and-speakers.md
sources:
  - sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md
  - sources/conversations/2026-10-07--org--adr-answers.md
  - sources/conversations/2026-10-07--org--adrs-approved.md
  - sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md
  - sources/conversations/2026-10-07--org--talks-team-and-site.md
  - sources/web/tooling/google-forms-response-destination.md
  - sources/web/tooling/tally-pricing.md
  - sources/web/tooling/sessionize-anonymous-mode.md
  - sources/web/tooling/pretalx-review-docs.md
  - sources/web/speakers/pycon-us-2026-speaking-guidelines.md
  - sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md
superseded_by: org/adrs/call-organiser-judges.md
---

# Take talks through Google Forms and review them blind with a panel of two or three

> **Superseded 2026-10-12** by [call organiser judges](call-organiser-judges.md), on the organiser's approval (`sources/conversations/2026-10-12--org--goatconf-ba-program-forms-approved.md`). Kept as the record of the earlier decision.

Answers the "Decision needed" of
[An open call by simple form](../prds/cfp-and-speakers.md). Accepted 2026-10-07 from the organiser's answers
(`sources/conversations/2026-10-07--org--adr-answers.md`, questions 2 and
8), and approved by the organiser (`sources/conversations/2026-10-07--org--adrs-approved.md`).

## What

The call for talks is a Google Form. Its responses land in a linked
response sheet that only the organiser and one volunteer, the CFP
domain owner, can open. That volunteer copies each proposal into a
separate reviewers' sheet without the name, bio, links or the grant
question. Two or three reviewers score the proposals blind there. The
organiser then makes the final picks with names visible, to balance the
program across disciplines and voices. The extension form is a second
Google Form on the same account.

## Why

The organiser chose a simple form and a shared sheet
(`sources/conversations/2026-10-07--org--coc-ledger-registration-cfp.md`),
then Google Forms over Tally, and an anonymised review by a small panel.
Google Forms stores responses "in a linked Google Sheet", and "when you
create a new response spreadsheet, form collaborators automatically get
access to it" (`sources/web/tooling/google-forms-response-destination.md`).
That second line is why reviewers are never collaborators on the form:
they would see every name. The copy step by hand is what Sessionize and
pretalx automate as anonymous review
(`sources/web/tooling/sessionize-anonymous-mode.md`,
`sources/web/tooling/pretalx-review-docs.md`), and at a few dozen
proposals one volunteer can do it in an evening.

Final picks with names visible follow the guide's advice that a program
is assembled as a whole, not ranked by score
(`sources/web/guides/rubyevents-how-to-organize-a-ruby-conference.md`,
§ Build a CFP committee); the blind scores keep the first read fair, and
the organiser's read keeps the day from being four talks by the same
kind of person.

## How

The form asks for the title, a short abstract for the program, a longer
description for reviewers, the intended audience, the speaker's name,
email and short bio, whether this is a first talk, and, only if a
supporter funds a speaker grant, a separate question about it, which
never reaches the reviewers' sheet, as PyCon US keeps its grant checkbox
from reviewers (`sources/web/speakers/pycon-us-2026-speaking-guidelines.md`).
A proposal whose abstract names its speaker is lightly edited in the
reviewers' copy, and the edit is noted.

The panel is the two or three reviewers, chosen across disciplines, plus
the organiser as the final reader; the PRD's committee of three to five
narrows to this on the organiser's answer. Reviewers score clarity,
relevance and fit. Responses and both sheets are deleted once the
speakers are announced and the waiting list is no longer needed; nothing
from them enters this public repository.

## Alternatives

- **Google Forms with a blind panel** *(chosen)*: free, familiar to
  speakers, and the organiser's choice.
- **Tally:** free with data stored in Europe
  (`sources/web/tooling/tally-pricing.md`), which would have eased the
  data notice; the organiser preferred Google Forms.
- **The organiser alone, anonymised:** one reader is faster, but the
  panel spreads the judgement across disciplines.
- **Open review:** simpler, and the bias the blind read exists to remove.
- **Sessionize or pretalx:** anonymity built in, at the cost of a second
  account for every reviewer and a tool to learn.

## Consequences

- **Opens:** a call that any speaker can answer in a browser, and a
  review that does not depend on the organiser's network knowing names.
- **Costs:** the copy step is manual; a slip leaks a name to the panel.
- **Costs:** Google holds the responses; the call's notice says so and
  says when they are deleted.
- **Closes:** inline reviewer comments and scoring features of a CFP tool.

## Linked PRD

[An open call by simple form](../prds/cfp-and-speakers.md). The
extension form follows the same tool:
[Extension slots and the record](extension-slots-and-the-record.md).

## Build notes

*(empty until the work ships)*
