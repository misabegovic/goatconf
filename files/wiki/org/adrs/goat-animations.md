---
title: "Goat animations: a peek set and a whole set of painted frames per goat, swapped like the looking frames"
kind: decision
status: accepted
updated: 2026-10-31
confidence: medium
affects:
  - org
sources:
  - wiki/org/prds/goat-animations.md
  - sources/conversations/2026-10-31--org--goat-animations-bet.md
  - site/album.js
  - site/goatchi.js
  - tools/goat_atlas.py
---

# Goat animations: a peek set and a whole set of painted frames per goat, swapped like the looking frames

## Context

[The plan](../prds/goat-animations.md) asks for petting, moving ears and tails, and more tricks for every goat. The
speakers' goats already swap whole painted frames to look around, from a sheet laid out like their own cell, which
keeps each frame aligned to the goat (source: site/album.js).

## Decision

1. **Tap to pet first, with no new art.** The first tap on a goat shows a small heart rising and a happy squash, and
   the goat says a line; the next tap plays a trick, as today. It ships before the art.
2. **Two painted sets per goat, from ChatGPT.** A peek set (ears flicked, petted, a yawn, a sneeze, a hoof raised to
   scratch, a wink) for every goat that peeks, and a whole set (ears flicked, tail wagging, petted, a stretch with a
   yawn, a sneeze, an ear scratch with a hind hoof) for Goatchi's goats; each set one 3 by 2 sheet in the same framing
   as the goat's peek or sitting picture, the plain goat first as the reference. The organiser sends the sheets.
3. **Swapped like the looking frames.** Each goat's set is cut to its cell's frame and laid out as one sheet per goat,
   loaded after the page; the companion swaps the whole picture for a moment, then back.
4. **Moves.** Ears and, on whole goats, the tail move now and then while waiting; the petted frame shows on a pet; the
   yawn, sneeze, scratch and wink join the tricks and the moves while waiting. Reduced motion keeps the blink only.
5. **Goatchi blinks**, with a blink frame per goat type from the same sheets.

## Alternatives

- **Animate parts in code** (ears rotated, a tail on a hinge): fewer paintings, but the watercolour goats are not
  painted in layers and look stiff when cut apart. Not chosen.
- **Only the plain goat and speakers first.** Offered; the organiser bet on every goat at once.

## Consequences

- About 30 to 40 sheets on the organiser's phone; some weight per goat, loaded late.
- The companion's frame swap grows from looking to a few named moves.

## Linked PRD

[More goat animations](../prds/goat-animations.md)
