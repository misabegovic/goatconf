---
title: "A cute goat mascot that peeks over the open slots, in roles from the EuRuKo 2024 goat multiverse"
kind: decision
status: accepted
updated: 2026-10-27
confidence: medium
depends_on:
  - org/prds/design-with-impeccable.md
sources:
  - sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md
  - sources/conversations/2026-10-27--org--mascot-watercolour.md
  - sources/conversations/2026-10-27--org--goat-everywhere.md
  - sources/conversations/2026-10-27--org--speaker-goats.md
  - sources/conversations/2026-10-27--org--goat-peek-home.md
  - sources/conversations/2026-10-27--org--goat-mascot-approved.md
  - sources/conversations/2026-10-27--org--goat-mascot.md
  - sources/conversations/2026-10-27--org--still-stickers.md
  - sources/web/organiser/euruko-2024-figma-file-2026-10-27.md
  - sources/web/organiser/euruko-2024-podcast-notes.md
  - sources/web/models/enola-tech-mascot-2026-10-27.md
  - sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md
  - sources/web/funding/euruko-2024-why-the-goat.md
---

# A cute goat mascot that peeks over the open slots, in roles from the EuRuKo 2024 goat multiverse

Proposed on 2026-10-27. The organiser asked to improve "this drawn goat on
the site that is shown everywhere", closer to "the goat multiverse topic of
euruko 2024", as "some sort of mascot that pops up and it's cute", like
enola.tech's cat. Shown sketches, they chose a flat goat, a peek that rises
on hover, and a role that matches the slot (source:
sources/conversations/2026-10-27--org--goat-mascot.md). Accepted the same
day: the organiser chose "Approve, start building" (source:
sources/conversations/2026-10-27--org--goat-mascot-approved.md).

## Context

- **The goat on the site today is a faint line drawing.** One SVG symbol in
  the shared page frame (`tools/frame.py`), drawn in the slot-line colour at
  70% opacity in the corner of every open "Yours?" slot, 23 of them on the
  home page and the Make it yours page, and as the placeholder where a
  speaker or a venue has no photo yet. It has no face and no character.
- **The mark is a different goat.** The seal uses the EuRuKo 2024 goat,
  unchanged, and the brand kit is built from it; the line goat was kept "on
  the site until the site rework" (source:
  sources/conversations/2026-10-12--org--brand-seal-and-euruko-goat.md).
- **The goat multiverse was a 2024 theme.** The organiser's EuRuKo 2024
  notes list "Mascot (G.O.A.T.) + goat story in Tuzla" and "Goat multiverse"
  among the conference's themes (source:
  sources/web/organiser/euruko-2024-podcast-notes.md). The 2024 design file
  shows what that meant: one "Multiverse Goat" in many roles, a wall of
  twelve (samurai, coder, painter, pirate, chef and more), trading cards
  such as "The Panonnian Pirate", and a main mascot, a white goat in a red
  fes and embroidered vest holding a fildžan of coffee. The goat hidden by
  its stone house and the Pannonian pirate tie it to Tuzla's own stories,
  the hidden goat and the salt sea (source:
  sources/web/organiser/euruko-2024-figma-file-2026-10-27.md;
  sources/web/funding/euruko-2024-why-the-goat.md). The 2024 goats are
  3D-style renders on dark red, far from this site's flat blue album.
- **The pop-up reference.** enola.tech's flat cat sits in the hero and
  peeks over the edges of cards and panels, each on a loop that never stops
  (source: sources/web/models/enola-tech-mascot-2026-10-27.md).
- **The organiser does not want things moving on their own.** The same day
  they had the cards' entrance animation removed: "becomes annoying"
  (source: sources/conversations/2026-10-27--org--still-stickers.md).

## Decision

1. **One flat goat, drawn in code.** A cute goat with large eyes, a cream
   coat, an ink outline and yellow horns curled back, in the site's own
   colours, drawn as SVG parts (head, ears, horns, eyes, body, hooves) in the
   frame's sprite. Roles are small layers on the same goat, so every role is
   the same character. It replaces the line goat symbol. The seal and the
   brand kit keep the EuRuKo 2024 goat; the mascot is not the mark.
2. **Roles from the multiverse, matched to the slot.** The first set, from
   the organiser's sketches: the goat; the speaker, with a microphone; the
   host, the 2024 Bosnian goat with fes, vest and fildžan; the coder, with
   glasses and a laptop; the cook, with a toque and ćevapi; the Pannonian
   pirate, with a tricorn, an eye patch and a salt crystal; and the hidden
   goat, peeking from the doorway of a little stone house. A slot names its
   role, and one table in the tools maps the kinds of slot to roles:
   - **Session slots** ("Your session here?", "The first speaker could be
     you"), and the podcast and karaoke kinds: the speaker.
   - **Event slots** ("Your event, any day", evening events, meetups): the
     host.
   - **Hackathons:** the coder.
   - **Trips:** the Pannonian pirate.
   - **"Something else?":** the hidden goat.
   - **Everything else** (hikes, "Your logo", a speaker or venue with no
     photo yet): the plain goat.
3. **It peeks, and rises a little when you point.** On an open slot the
   goat's head, horns and front hooves show over the slot's top edge, as if
   it were behind the slot. It does not move on load or on scroll and never
   loops. When the slot is hovered or focused, the goat rises a little,
   about a third of a rem, over about 200ms, and settles back when you
   leave; with reduced motion it stays where it is. On a phone, with no
   hover, it simply sits there. Where a speaker or a venue has no photo, the
   whole goat sits in the photo's place, still.
4. **Decorative only.** The goat is hidden from screen readers and carries
   no text or link of its own; the slot keeps its words and its stamp. It
   never covers the when, the where or how to register, and it does not
   appear on the code of conduct, keeping the rule that the goat never makes
   it read as a joke (see [design with impeccable](design-with-impeccable.md)).
5. **Written down where the look is written.** DESIGN.md gets a section on
   the mascot (its parts, colours, roles, the peek and the hover rise), and
   `.impeccable/design.json` matches it; the impeccable ADR gets an
   amendment pointing here.
6. **Built in small steps, each shown in the browser first.** First the goat
   and the peek on the home page's open slots, with the roles; then the Make
   it yours page and the photo placeholders; then the design notes. The
   organiser sees each step next to the live site before it ships.

## Alternatives

- **The 2024 Bosnian goat and the multiverse renders as they are.** The
  strongest tie to EuRuKo, and the organiser's own images, but they are
  large 3D-style renders in another palette, heavy on a phone, and they
  cannot be given a new role without making new images. Not chosen.
- **A human illustrator draws the goat.** The best drawing, at a cost and a
  wait. Left open: if an illustrator draws GoatConf's goat later, the parts
  and the role table stay, and only the drawing changes.
- **The goat only in a few chosen places** (the 404 page, the end of the
  home page, empty lists), with the line goat kept in the slots. Fewer
  surprises, less character. Not chosen.
- **A peek on a loop, as on enola.tech, or one pop-up per page.** More life,
  but it is the kind of movement the organiser just had removed from the
  cards. Not chosen.
- **Do nothing.** The line goat stays: quiet, faceless, and unrelated to the
  goat in the seal.

## Consequences

- Every page's sprite grows by the goat's parts and roles, a few kilobytes
  of inline SVG, once per page.
- A new role means drawing one small layer and adding a line to the role
  table; the goat itself is drawn once.
- The faint line goat retires, along with the `.ghost` look; the open slot
  keeps its dashed border, number and stamp.
- The hover rise is the only motion the cards keep, and only when the
  visitor points at a slot.
- The shareables, the brand kit and the seal are unchanged by this decision.

## Open questions

- A hiker goat for hikes, and a role for the Saturday at the lakes, or the
  plain goat until there is one.
- Whether the mascot later appears on the 404 page, the shareable cards, or
  the "See you in Tuzla" close.
- Whether the cook gets a place: the food guide has no open slot today.

## Build notes

- **2026-10-27, step one: the home page.** The goat is drawn in parts in the
  frame's sprite (`tools/frame.py`), with one symbol per role (the goat, the
  speaker, the host, the coder, the pirate and the hidden goat) and the table
  of which kind of slot gets which role; `tools/home.py` and the home page's
  hand-written slots use it, and `goatconf.css` places the peek and the
  hover rise and gives rows with a peek more room. The cook waits until a
  slot needs it. The Make it yours page and the photo placeholders keep the
  line goat until step two (source:
  sources/conversations/2026-10-27--org--goat-peek-home.md).
- **2026-10-27, each speaker's own goat.** `tools/goats.py` draws the goat
  once, in parts, and each speaker's goat from the traits in their record;
  the frame's sprite takes its parts from it. `tools/speakers.py` checks the
  traits and puts the goat on the cards and the speaker pages, and
  `tools/shareables.py` on the share cards, all re-rendered. The program's
  session cards get the goat when the first session has a slot: today no
  session does (source: sources/conversations/2026-10-27--org--speaker-goats.md).
- **2026-10-27, step two: everywhere else.** The Make it yours page's open
  slots peek, the speakers and supporters pages' invitations peek, and a
  venue or a speaker with no photo shows the whole goat sitting (`#goat-sit`
  in the sprite). The faint line goat and its `.ghost` styles are gone
  (source: sources/conversations/2026-10-27--org--goat-everywhere.md).
- **2026-10-27, step three: the design notes.** DESIGN.md describes the
  goat mascot, the stickers and the peek rise, and drops the ghost goat;
  `.impeccable/design.json` matches, and the impeccable ADR has an
  amendment (source: sources/conversations/2026-10-27--org--goat-mascot-approved.md).

## Related

- [Design with impeccable](design-with-impeccable.md): the album look, the
  goat everywhere and the rule for the code of conduct.
- [One page frame and one site build](one-page-frame-and-one-site-build.md):
  the frame module that holds the sprite.
- sources/conversations/2026-10-27--org--goat-mascot.md
- sources/web/organiser/euruko-2024-figma-file-2026-10-27.md

## Amendments

- **2026-10-27, each speaker's own goat.** Every published speaker gets
  their own goat, drawn from their photo: the same goat with their hair,
  beard, glasses or cap, what they wear, and what they hold (a microphone, a
  clicker, or something from the photo), never a logo from their clothes.
  The traits live in the speaker's record under `goat`, chosen from drawn
  parts. The goat peeks over their card on the home page and the speakers
  page, sits beside their bio on their own page, and sits at the edge of
  their photo on their "I'm speaking" and announcement cards; once their
  sessions are on the program, it will peek over those too. A goat goes live
  once the organiser approves it, and a speaker can ask for a change or for
  no goat (source: sources/conversations/2026-10-27--org--speaker-goats.md).
- **2026-10-27, a new base look, to come from an illustrator.** The goat
  drawn in code stays on the site for now, but its look is to be replaced:
  the organiser chose a watercolour storybook goat (fluffy, cream, golden
  horns curled back, big friendly eyes), explored with an image generator
  and to be drawn by an illustrator so that GoatConf owns it outright. The
  goat multiverse becomes the same goat across art styles, the watercolour
  goat being the everyday one; the peek, the roles, the speaker goats and
  the stickers carry over to the new drawing once it exists. Moving like
  enola's cat (a bob, a blink, the peek rising) is wanted for the new goat;
  how much movement is to be settled when it arrives (source:
  sources/conversations/2026-10-27--org--mascot-watercolour.md).
- **2026-10-27, the painted goat on the site, one at a time.** The
  watercolour goat replaces the drawn goat everywhere now, painted with an
  image generator by the agent, as the organiser asked ("you are the
  illustrator"); the illustrator's final drawing can still replace it later.
  Every role, each speaker's own goat (described from their photos in words,
  never uploading a photo), the sitting goat, the sleeping goat on the 404
  page, the stickers and the share cards are painted. With the script a
  visitor sees one goat at a time: it stands inside the open slot or speaker
  card nearest the middle of the screen, in that slot's role or as that
  speaker's goat, and hops to the next as they scroll or point; it pops up,
  ducks when the pointer comes close, and while it waits bobs, wiggles,
  stretches, plays peek-a-boo or looks around. Turning is the goat's own
  painted head turned left or right, never a mirrored or spun picture, and
  only the head changes, so its body and legs are always the painted goat's
  own. It must work on a bad connection: one small sprite sheet per set of
  goats, the turned heads loaded after the page, the goat shown only once its
  picture has loaded, moves by transform only, and no companion on Save-Data
  or 2G. Without the script every slot keeps its own still goat; with
  reduced motion the goat appears and stays still. On the share cards the
  speaker's whole goat sits in the bottom corner, never cut off (source:
  sources/conversations/2026-10-27--org--illustrated-goat-on-the-site.md).
