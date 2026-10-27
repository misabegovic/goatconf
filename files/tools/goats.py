#!/usr/bin/env python3
"""The GoatConf goat, drawn once, and each speaker's own goat.

The goat is drawn in parts (horns, ears, face, snout, body, hooves) in the
head's own coordinates. A speaker's goat is the same goat with traits taken
from their photo: hair, beard, glasses, a cap, what they wear and what they
hold. A speaker record names its goat's traits under `goat:`; this module
draws it, as a peek over their card or whole, for their page and their
shareable cards.

  sheet OUT.html   write a page showing every speaker's goat, for review

Usage: python3 tools/goats.py sheet OUT.html
(ADR wiki/org/adrs/goat-mascot.md)
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

INK = "#051d47"
COAT = "#fffaf0"
HORN = "#ffd400"
BLUSH = "#f3b3ac"
LINE = f'stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"'

HORNS = (f'<path d="M86 56C82 39 70 28 55 30 44 32 39 42 44 50c4-7 12-9 19-5 7 4 11 10 14 15z" fill="{HORN}" {LINE}/>'
         f'<path d="M114 56c4-17 16-28 31-26 11 2 16 12 11 20-4-7-12-9-19-5-7 4-11 10-14 15z" fill="{HORN}" {LINE}/>'
         f'<path d="M62 38c4 1 8 4 11 8M138 38c-4 1-8 4-11 8" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>')
EARS = (f'<path d="M58 82c-12-4-24-2-32 6 9 7 21 9 33 5z" fill="{COAT}" {LINE}/>'
        f'<path d="M38 88c6 2 12 2 17 1" fill="none" stroke="{BLUSH}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M142 82c12-4 24-2 32 6-9 7-21 9-33 5z" fill="{COAT}" {LINE}/>'
        f'<path d="M162 88c-6 2-12 2-17 1" fill="none" stroke="{BLUSH}" stroke-width="4" stroke-linecap="round"/>')
HEAD = f'<path d="M100 48c27 0 45 17 45 40 0 15-7 25-15 33-6 14-17 21-30 21s-24-7-30-21c-8-8-15-18-15-33 0-23 18-40 45-40z" fill="{COAT}" {LINE}/>'
CURL = f'<path d="M92 50c3-6 9-8 14-5-4 1-6 4-6 8" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
BLUSHES = f'<circle cx="71" cy="108" r="7" fill="{BLUSH}" opacity=".7"/><circle cx="129" cy="108" r="7" fill="{BLUSH}" opacity=".7"/>'
EYES = (f'<ellipse cx="82" cy="90" rx="9" ry="11" fill="{INK}"/><ellipse cx="118" cy="90" rx="9" ry="11" fill="{INK}"/>'
        '<circle cx="79" cy="86" r="3.4" fill="#fff"/><circle cx="115" cy="86" r="3.4" fill="#fff"/>'
        '<circle cx="85" cy="94" r="1.6" fill="#fff"/><circle cx="121" cy="94" r="1.6" fill="#fff"/>')
SNOUT = (f'<ellipse cx="100" cy="117" rx="20" ry="13" fill="#fde6df"/>'
         f'<ellipse cx="93" cy="115" rx="2.6" ry="3.4" fill="{INK}"/><ellipse cx="107" cy="115" rx="2.6" ry="3.4" fill="{INK}"/>'
         f'<path d="M93 124q7 6 14 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
TUFT = f'<path d="M94 140c1 9 3 15 6 19 3-4 5-10 6-19" fill="{COAT}" {LINE}/>'
BODY = (f'<path d="M150 178c10-2 16-9 15-17" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>')
TORSO = 'M60 196c-4-28 12-50 40-50s44 22 40 50z'
LEGS = (f'<path d="M78 196v-22M122 196v-22" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        f'<rect x="68" y="188" width="22" height="10" rx="5" fill="{INK}"/><rect x="110" y="188" width="22" height="10" rx="5" fill="{INK}"/>')


def _hair(style: str, colour: str) -> str:
    """Hair on top of the head, under the horns' tips; `none` is bald."""
    if style == "short":
        return f'<path d="M66 66c2-16 16-24 34-24s32 8 34 24c-8-7-16-9-22-6-4-5-10-6-14-2-8-4-18-2-32 8z" fill="{colour}" {LINE}/>'
    if style == "wavy":
        return (f'<path d="M64 68c0-18 16-28 36-28s36 10 36 28c-6-6-12-6-16-2 0-6-6-10-12-8-4-6-12-6-16 0-6-2-12 2-12 8-4-4-10-4-16 2z" fill="{colour}" {LINE}/>'
                f'<path d="M84 44c-4 4-4 10 0 14M112 44c4 4 4 10 0 14" fill="none" stroke="{INK}" stroke-width="2" opacity=".5"/>')
    if style == "side":
        return f'<path d="M64 70c2-20 18-30 38-30 18 0 32 10 34 26-12-10-26-14-42-10-12 3-20 8-30 14z" fill="{colour}" {LINE}/>'
    if style == "long":
        return (f'<path d="M60 70c-6 18-6 44 2 66 6-4 8-12 8-22l-2-40z" fill="{colour}" {LINE}/>'
                f'<path d="M140 70c6 18 6 44-2 66-6-4-8-12-8-22l2-40z" fill="{colour}" {LINE}/>'
                f'<path d="M62 72c2-20 18-30 38-30s36 10 38 30c-10-10-22-14-38-12-16-2-28 2-38 12z" fill="{colour}" {LINE}/>')
    return ""


def _beard(style: str, colour: str) -> str:
    """A beard over the chin; the goat's own tuft when there is none."""
    if style == "full":
        return f'<path d="M62 110c0 30 16 58 38 64 22-6 38-34 38-64-8 12-20 20-38 20s-30-8-38-20z" fill="{colour}" {LINE}/>'
    if style == "short":
        return f'<path d="M68 116c2 20 14 36 32 40 18-4 30-20 32-40-8 9-18 14-32 14s-24-5-32-14z" fill="{colour}" {LINE}/>'
    if style == "goatee":
        return f'<path d="M86 132c2 16 8 30 14 40 6-10 12-24 14-40-8 4-20 4-28 0z" fill="{colour}" {LINE}/>'
    if style == "long":
        return f'<path d="M84 130c0 26 8 50 16 64 8-14 16-38 16-64-8 5-24 5-32 0z" fill="{colour}" {LINE}/>'
    if style == "stubble":
        return f'<path d="M70 114c4 16 14 26 30 28 16-2 26-12 30-28-8 8-18 12-30 12s-22-4-30-12z" fill="{colour}" opacity=".45"/>' + TUFT
    return TUFT


def _glasses(style: str) -> str:
    if style == "rect":
        return f'<g fill="none" stroke="{INK}" stroke-width="4"><rect x="66" y="78" width="32" height="24" rx="6"/><rect x="102" y="78" width="32" height="24" rx="6"/><path d="M98 88h4M66 86l-8-3M134 86l8-3"/></g>'
    if style == "thin":
        return f'<g fill="none" stroke="{INK}" stroke-width="2.5"><rect x="67" y="80" width="30" height="20" rx="4"/><rect x="103" y="80" width="30" height="20" rx="4"/><path d="M97 88h6M67 86l-8-3M133 86l8-3"/></g>'
    if style == "round":
        return f'<g fill="none" stroke="{INK}" stroke-width="3"><circle cx="82" cy="90" r="14"/><circle cx="118" cy="90" r="14"/><path d="M96 89h8"/></g>'
    if style == "grey":
        return f'<g fill="none" stroke="#5b6475" stroke-width="3.5"><rect x="66" y="79" width="32" height="22" rx="7"/><rect x="102" y="79" width="32" height="22" rx="7"/><path d="M98 88h4M66 86l-8-3M134 86l8-3"/></g>'
    if style == "sun":
        return (f'<g {LINE}><path d="M64 80h34c0 14-6 22-17 22s-17-8-17-22zM102 80h34c0 14-6 22-17 22s-17-8-17-22z" fill="#1d2433"/></g>'
                f'<path d="M98 84h4" stroke="{INK}" stroke-width="3"/><path d="M70 84l8 0M108 84l8 0" stroke="#fff" stroke-width="2" opacity=".5"/>')
    return ""


def _cap(colour: str) -> str:
    return (f'<path d="M62 66c0-24 16-34 38-34s38 10 38 34z" fill="{colour}" {LINE}/>'
            f'<path d="M56 66h88c4 0 6 6 0 8H56c-6-2-4-8 0-8z" fill="{colour}" {LINE}/>'
            f'<rect x="90" y="40" width="20" height="9" rx="2" fill="#fff" opacity=".8"/>')


def _top(kind: str, colour: str) -> str:
    """What they wear, over the body."""
    out = f'<path d="{TORSO}" fill="{colour}" {LINE}/>'
    if kind == "hoodie":
        out += (f'<path d="M72 152c8 10 18 14 28 14s20-4 28-14" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
                f'<path d="M92 166v14M108 166v14" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    elif kind == "sweater":
        out += f'<path d="M80 150c6 6 13 9 20 9s14-3 20-9" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".35"/>'
    elif kind == "shirt":
        out += f'<path d="M88 148l12 14 12-14" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><circle cx="100" cy="172" r="2" fill="{INK}"/><circle cx="100" cy="184" r="2" fill="{INK}"/>'
    else:
        out += f'<path d="M86 148c4 6 9 8 14 8s10-2 14-8" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    return out


def _prop(kind: str) -> str:
    """What they hold, in the front hoof."""
    if kind == "mic":
        return (f'<path d="M150 170l-14-26" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                f'<circle cx="134" cy="140" r="9" fill="#2f3747" {LINE}/>'
                f'<rect x="142" y="162" width="14" height="10" rx="5" fill="{INK}" transform="rotate(-30 149 167)"/>')
    if kind == "clicker":
        return (f'<rect x="138" y="148" width="12" height="22" rx="4" fill="#2f3747" {LINE}/><circle cx="144" cy="155" r="2.4" fill="#ffd400"/>'
                f'<rect x="136" y="166" width="16" height="10" rx="5" fill="{INK}"/>')
    if kind == "cat":
        return (f'<path d="M110 196c-4-20 6-36 26-38 20 2 30 18 26 38z" fill="#9a7a5a" {LINE}/>'
                f'<path d="M122 162l2-14 8 10M150 162l-2-14-8 10" fill="#9a7a5a" {LINE}/>'
                f'<circle cx="130" cy="172" r="2.4" fill="{INK}"/><circle cx="142" cy="172" r="2.4" fill="{INK}"/>'
                f'<path d="M132 180q4 3 8 0" fill="none" stroke="{INK}" stroke-width="2"/>')
    if kind == "book":
        return (f'<path d="M126 150l30-6v30l-30 6z" fill="#c0392b" {LINE}/><path d="M131 158l20-4M131 165l20-4" stroke="#fff" stroke-width="2"/>'
                f'<rect x="120" y="172" width="16" height="10" rx="5" fill="{INK}"/>')
    if kind == "laptop":
        return (f'<path d="M52 200l10-44h76l10 44z" fill="{HORN}" {LINE}/><circle cx="100" cy="178" r="7" fill="none" stroke="{INK}" stroke-width="3"/>'
                f'<rect x="58" y="160" width="14" height="10" rx="5" fill="{INK}" transform="rotate(-20 65 165)"/>'
                f'<rect x="128" y="160" width="14" height="10" rx="5" fill="{INK}" transform="rotate(20 135 165)"/>')
    return ""


def head(traits: dict) -> str:
    """The head with the speaker's traits, in the head's own coordinates."""
    hair = traits.get("hair", "none")
    hair_colour = traits.get("hair_colour", "#4a3324")
    beard = traits.get("beard", "")
    beard_colour = traits.get("beard_colour", hair_colour)
    out = EARS
    if hair == "long":
        out = _hair("long", hair_colour).split("/>", 2)[0] + "/>" + _hair("long", hair_colour).split("/>", 2)[1] + "/>" + out
    out += HORNS + HEAD + ("" if hair != "none" or traits.get("cap") else CURL)
    if hair == "long":
        out += _hair("long", hair_colour).split("/>", 2)[2]
    elif hair != "none":
        out += _hair(hair, hair_colour)
    out += BLUSHES + _beard(beard, beard_colour) + SNOUT + EYES + _glasses(traits.get("glasses", ""))
    if traits.get("cap"):
        out += _cap(traits["cap"])
    return out


def whole(traits: dict) -> str:
    """The speaker's goat, sitting: the viewBox is 0 18 200 186."""
    top = _top(traits.get("top", "tee"), traits.get("top_colour", "#2b3a55"))
    return (f'<svg class="goat-whole" aria-hidden="true" focusable="false" viewBox="0 18 200 186">{BODY}{top}{LEGS}'
            f'{head(traits)}{_prop(traits.get("prop", ""))}</svg>')


def peek(traits: dict) -> str:
    """The speaker's goat peeking over the top edge of their card: the viewBox ends at the edge, so the rest is hidden."""
    return (f'<svg class="peek peek--face" aria-hidden="true" focusable="false" viewBox="0 18 200 146">{head(traits)}'
            f'<rect x="56" y="152" width="24" height="13" rx="6.5" fill="{INK}"/><rect x="120" y="152" width="24" height="13" rx="6.5" fill="{INK}"/></svg>')


# What a speaker record's `goat:` may say, each a choice from the drawn parts.
CHOICES = {"hair": ("none", "short", "wavy", "side", "long"), "beard": ("", "full", "short", "goatee", "long", "stubble"),
           "glasses": ("", "rect", "thin", "round", "grey", "sun"), "top": ("tee", "hoodie", "sweater", "shirt"),
           "prop": ("", "mic", "clicker", "cat", "book", "laptop")}
COLOURS = ("hair_colour", "beard_colour", "top_colour", "cap")


def problems(goat) -> list:
    """What is wrong with a speaker record's `goat:`, if anything."""
    import re
    if goat is None:
        return []
    if not isinstance(goat, dict):
        return ["goat must be a set of traits, for example {hair: short, hair_colour: '#2b2522', top: hoodie}"]
    out = []
    for key, value in goat.items():
        if key in CHOICES:
            if (value or "") not in CHOICES[key]:
                out.append(f"goat {key} must be one of: {', '.join(c or '(none)' for c in CHOICES[key])}")
        elif key in COLOURS:
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(value)):
                out.append(f"goat {key} must be a colour like '#2b2522'")
        else:
            out.append(f"goat has no trait '{key}': use {', '.join(list(CHOICES) + list(COLOURS))}")
    return out


# Drafts from the speakers' photos, for review before they go into the records.
DRAFTS = {
    "paul-campbell": {"hair": "wavy", "hair_colour": "#2b2522", "beard": "full", "beard_colour": "#2b2522", "glasses": "rect", "top": "tee", "top_colour": "#d9dde3", "prop": "mic"},
    "roy-tomeij": {"hair": "none", "glasses": "grey", "top": "sweater", "top_colour": "#c58a2a", "prop": "mic"},
    "carmine-paolino": {"hair": "none", "cap": "#3a3d42", "beard": "stubble", "beard_colour": "#b0703c", "glasses": "sun", "top": "tee", "top_colour": "#25272b", "prop": "mic"},
    "dejan-menges": {"hair": "short", "hair_colour": "#3b3634", "beard": "goatee", "beard_colour": "#8c8a88", "top": "tee", "top_colour": "#1f3a64", "prop": "clicker"},
    "jan-grodowski": {"hair": "side", "hair_colour": "#7a5232", "beard": "stubble", "beard_colour": "#a07850", "glasses": "rect", "top": "tee", "top_colour": "#25272b", "prop": "mic"},
    "amar-mahmutbegovic": {"hair": "none", "beard": "full", "beard_colour": "#7a5232", "top": "shirt", "top_colour": "#1d2d50", "prop": "mic"},
    "cristian-planas": {"hair": "wavy", "hair_colour": "#2b2522", "beard": "short", "beard_colour": "#3b302a", "top": "tee", "top_colour": "#6b6f75", "prop": "mic"},
    "christoph-lipautz": {"hair": "long", "hair_colour": "#5a3c28", "beard": "long", "beard_colour": "#5a3c28", "glasses": "thin", "top": "tee", "top_colour": "#25272b", "prop": "cat"},
    "predrag-radenkovic": {"hair": "short", "hair_colour": "#2b2522", "beard": "short", "beard_colour": "#2b2522", "top": "hoodie", "top_colour": "#1f2b45", "prop": "mic"},
}


def sheet(out: Path) -> None:
    root = Path(__file__).resolve().parent.parent
    cells = []
    for slug, traits in DRAFTS.items():  # the drafts the records were made from
        name = slug.replace("-", " ").title()
        cells.append(f'<figure><img src="file://{root}/site/img/speakers/{slug}.jpg" alt=""><div class="g">{whole(traits)}</div>'
                     f'<div class="p"><div class="card"></div>{peek(traits)}</div><figcaption>{html.escape(name)}</figcaption></figure>')
    out.write_text(f"""<!doctype html><meta charset="utf-8"><title>Speaker goats, drafts</title>
<style>body{{margin:0;padding:24px;background:#0b3d91;font-family:system-ui,sans-serif}}
h1{{color:#ffd400;font-size:22px;margin:0 0 16px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#fff;border-radius:12px;padding:12px;display:grid;grid-template-columns:120px 1fr 1fr;gap:10px;align-items:end}}
figure img{{width:120px;height:120px;object-fit:cover;border-radius:8px}}
.g svg{{width:100%;height:auto;background:#edf2fb;border-radius:8px}}
.p{{position:relative;height:130px}} .p .card{{position:absolute;left:0;right:0;bottom:0;height:40px;background:#0b3d91;border-radius:6px 6px 0 0}}
.p .peek{{position:absolute;right:8px;bottom:34px;width:90%}}
figcaption{{grid-column:1/-1;font-weight:700;color:#12204a}}</style>
<h1>Each speaker's goat, from their photo (drafts)</h1><div class="grid">{''.join(cells)}</div>""", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "sheet":
        sheet(Path(sys.argv[2]))
    else:
        print(__doc__)
        sys.exit(2)
