#!/usr/bin/env python3
"""The goat's images on the site, cut from the painted masters in art/goat/ (ADR wiki/org/adrs/goat-mascot.md).

A set of goats that peek (the roles, the speakers) is one sprite sheet: each goat once, in a column of
cells whose edge line is the same, and beside them only the patch around each goat's eyes, closed. So a
page fetches one small image for every goat on it, a blink is that patch shown over the eyes for a moment,
and the companion goat (site/album.js) changes role without asking the network for anything. Beside each sheet
is a second one, sheet-<set>-turns.webp, with only each goat's head turned left and right: the companion
loads it after the page and swaps the head band when the goat turns, so the body under it is always the
painted goat's own. A goat shown on its own (a speaker's sitting goat, the sleeping goat) is one image.

The masters stay on the organiser's machine (generated images are kept out of this public repository,
.gitignore); only manifest.json is tracked, so a fresh clone can check the site and place the goats, and
only redrawing needs the masters. frame.py and speakers.py place the goats with goat(); manifest.json says, for each master, its group and
the line its hooves rest on (edge), the box around its closed eyes (eyes), and for a goat that turns, the
padding around its turned frames and how far down the head band reaches (turn).

  build    write site/img/goat/: the sheets and the single goats (needs Pillow)
  check    fail if an image is missing or does not match the masters

Usage: python3 tools/goat_atlas.py <build|check>
"""
from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art" / "goat"
OUT = ROOT / "site" / "img" / "goat"
WEB = "img/goat"
# Each sheet's goats, and how tall each goat stands above its edge, in sheet pixels: about twice the size
# it shows at, so it stays sharp on a phone's screen.
# The goat's scenes on the Tuzla and food photos, by photo: the companion visits a photo as that photo's scene.
# The goat's scenes on the Tuzla and food photos, by photo: the companion visits a photo as one of that photo's
# scenes, a different one each visit where a photo has several.
SCENES = {"img/city-lakes-aerial-summer.jpg": ("sticker-salt-lakes", "sticker-pannonian-sea", "sticker-beach"),
          "img/city-square-fountain-summer.jpg": ("sticker-salt",),
          "img/city-korzo-clock.jpg": ("standing", "sticker-korzo"),
          "img/city-aerial-summer.jpg": ("sticker-hike",),
          "img/food-burek.jpg": ("sticker-burek",), "img/food-cevapi.jpg": ("sticker-cevapi",), "img/food-coffee.jpg": ("sticker-fildzan",),
          # every other food and Tuzla photo on the home page, each with its own scene (organiser, 2026-10-31)
          "img/city-old-town-aerial-paving.jpg": ("sticker-old-town",), "img/city-archaeological-park.jpg": ("sticker-neolithic",),
          "img/food-grah.jpg": ("sticker-grah",), "img/food-punjene-paprike.jpg": ("sticker-punjene-paprike",),
          "img/food-begova-corba.jpg": ("sticker-begova-corba",), "img/food-zeljanica.jpg": ("sticker-zeljanica",),
          "img/food-sirnica.jpg": ("sticker-sirnica",), "img/food-krompirusa.jpg": ("sticker-krompirusa",),
          "img/food-sarma.jpg": ("sticker-sarma",), "img/food-tufahija.jpg": ("sticker-tufahija",),
          "img/food-hurmasice.jpg": ("sticker-hurmasice",)}
# Scenes a page places by hand: the goat waving or jumping for joy at the end, the goat statue after the goat hunt.
HAND_SCENES = ("waving", "jumping", "sticker-goat-statue")
SETS = {"roles": (("peeking", "peek-host", "peek-coder", "peek-speaker", "peek-cook", "peek-pirate", "peek-hidden"), 190),
        "sitting": (("sitting",), 320),
        # The waving goat says goodbye at the end of the home page.
        "scenes": (tuple(dict.fromkeys(p for poses in SCENES.values() for p in poses)) + HAND_SCENES, 240)}
# The speakers whose whole sitting goat sits on their card on the home and Speakers pages and on the bands of
# their own page, where their goat peeking over the card looked cut off; the others peek (sources/conversations/2026-10-27--org--goat-tap-polish.md).
# Every speaker now peeks with head, chest and hooves over the card, painted looking in nine directions, so none sits
# whole on its card any more (organiser, 2026-10-31: "I want all speakers goats to be peeking goats").
WHOLE_ON_CARD = ()
# The goats shown on their own, and their long side in pixels.
SINGLE = 480
# How far, in master pixels, the turned head band and the body overlap where they meet.
OVERLAP = 20
QUALITY = 74


@lru_cache(maxsize=None)
def manifest() -> dict:
    return json.loads((ART / "manifest.json").read_text(encoding="utf-8"))


def sets() -> dict:
    """Each sheet's goats in order, and their height above the edge: the fixed sets, and the speakers'."""
    out = dict(SETS)
    out["speakers"] = (tuple(sorted(k for k, v in manifest().items() if v["group"] == "speakers")), 190)
    if WHOLE_ON_CARD:
        out["cards"] = (tuple(f"speaker-{s}-sitting" for s in WHOLE_ON_CARD if f"speaker-{s}-sitting" in manifest()), 300)
    return out


# Goatchi's goats, each shown on its own: the plain goat and the role goats a visitor can keep, the goat eating
# what it is fed, and (in singles) the sleeping goat (ADR goat-tamagotchi-on-the-site).
GOATCHI_GOATS = ("sitting", "sticker-host", "sticker-coder", "sticker-speaker", "sticker-cook", "sticker-pirate", "sticker-hidden")
GOATCHI_FOOD = ("sticker-burek", "sticker-cevapi", "sticker-fildzan")
# In Goatchi's challenge mode a neglected goat goes exploring: the goat hiking above Tuzla.
GOATCHI_GONE = "sticker-hike"
# Goatchi as a full game (ADR goatchi-full-game): each goat type's own poses, so a kept goat eats, sleeps, plays and
# shows its mood as itself. A pose's master is named for its type and pose (pirate-eating); the plain goat's poses
# painted earlier stand in for the ones it already has.
GOATCHI_TYPES = {"sitting": "goat", "sticker-host": "host", "sticker-coder": "coder", "sticker-speaker": "speaker",
                 "sticker-cook": "cook", "sticker-pirate": "pirate", "sticker-hidden": "hidden"}
GOATCHI_POSES = ("eating", "sleeping", "playing", "hungry", "sulking", "happy", "hiking", "packing")
GOATCHI_PAINTED = {"goat-eating": GOATCHI_FOOD, "goat-sleeping": ("asleep",), "goat-happy": ("jumping",), "goat-hiking": (GOATCHI_GONE,)}


def goatchi_poses(goat: str) -> dict:
    """A goat's own poses that are painted, each as the masters it may show (the plain goat eats three dishes)."""
    kind = GOATCHI_TYPES.get(goat)
    if not kind:
        return {}
    out = {}
    for pose in GOATCHI_POSES:
        names = tuple(n for n in GOATCHI_PAINTED.get(f"{kind}-{pose}", (f"{kind}-{pose}",)) if n in manifest())
        if names:
            out[pose] = names
    return out


def singles() -> tuple:
    poses = tuple(sorted({n for g in GOATCHI_GOATS for names in goatchi_poses(g).values() for n in names}
                         - {"asleep", GOATCHI_GONE, *GOATCHI_FOOD}))
    return (("asleep",) + GOATCHI_GOATS + GOATCHI_FOOD + (GOATCHI_GONE,)
            + tuple(sorted(k for k, v in manifest().items() if v["group"] == "speakers-sitting")) + poses)


@lru_cache(maxsize=None)
def layout(name: str) -> dict:
    """Where each goat sits on a sheet, and its eye patch, in sheet pixels."""
    man = manifest()
    poses, above = sets()[name]
    edge_of = {p: man[p]["edge"] or man[p]["h"] for p in poses}
    # One scale for the set, from its typical goat, so goats stand the same height; the hidden goat
    # shows only its head, so it keeps the scale and stays small.
    edges = sorted(edge_of[p] for p in poses if p != "peek-hidden")
    k = above / edges[len(edges) // 2]
    top = max(round(edge_of[p] * k) for p in poses)
    below = max(round((man[p]["h"] - edge_of[p]) * k) for p in poses)
    cell_w = max(round(man[p]["w"] * k) for p in poses) + 8
    cell_h = top + below + 4
    cells, px, py, patch_w, ty, turn_w = {}, cell_w, 0, 0, 0, 0
    for i, p in enumerate(poses):
        w, h = round(man[p]["w"] * k), round(man[p]["h"] * k)
        x, y = (cell_w - w) // 2, top - round(edge_of[p] * k)
        cell = {"row": i, "w": w, "h": h, "x": x, "y": y, "eyes": None}
        box = man[p]["eyes"]
        if box:
            bx0, by0 = int(box[0] * k), int(box[1] * k)
            bw, bh = int(box[2] * k + 1) - bx0, int(box[3] * k + 1) - by0
            cell["eyes"] = {"x": x + bx0, "y": y + by0, "w": bw, "h": bh, "sx": px, "sy": py, "bx": bx0, "by": by0}
            py += bh + 2
            patch_w = max(patch_w, bw)
        tr = man[p].get("turn")
        if tr:
            pad = tr["pad"] * k
            bw, bh = round(man[p]["w"] * k + 2 * pad), round(tr["band"] * k)
            # The band ends below the last row the turn changes; the body shows from OVERLAP above that end, so
            # the two meet on the same paint and no seam shows.
            cell["turn"] = {"x": round(x - pad), "y": round(y - pad), "w": bw, "h": bh, "ty": ty, "cut": round(y - pad + bh - OVERLAP * k)}
            ty += bh + 2
            turn_w = max(turn_w, bw)
        cells[p] = cell
    height = max(cell_h * len(poses), py)
    return {"file": f"{WEB}/sheet-{name}.webp", "cell_w": cell_w, "cell_h": cell_h, "edge": top,
            "width": cell_w + patch_w, "height": height, "scale": k, "cells": cells,
            "turns": {"file": f"{WEB}/sheet-{name}-turns.webp", "width": 2 * turn_w + 2, "height": max(ty, 1)} if turn_w else None}


def gazers() -> tuple:
    """The goats painted looking in nine directions."""
    return tuple(sorted(k for k, v in manifest().items() if v.get("gaze")))


def gaze_layout(pose: str) -> dict:
    """A gaze sheet: three by three cells, each the size of the goat's cell on its own sheet."""
    L = layout(sheet_of(pose))
    return {"file": f"{WEB}/gaze-{pose}.webp", "cell_w": L["cell_w"], "cell_h": L["cell_h"],
            "width": 3 * L["cell_w"], "height": 3 * L["cell_h"], "cell": L["cells"][pose]}


def sheet_of(pose: str):
    for name, (poses, _) in sets().items():
        if pose in poses:
            return name
    return None


def has(pose: str) -> bool:
    return pose in manifest()


def stamped(path: str) -> str:
    """An image's address with a stamp of its content, so a repainted goat reaches browsers that cached the last one."""
    import hashlib
    f = ROOT / "site" / path
    return f"{path}?v={hashlib.sha1(f.read_bytes()).hexdigest()[:8]}" if f.exists() else path


def _pct(n: float) -> str:
    return f"{round(n, 3):g}%"


def goat(pose: str, cls: str, beat: int = 0) -> str:
    """A goat from its sheet: a box the cell's shape, painted from the sheet, with its eye patch over it.
    The sizes are shares of the box, so the box's width in the CSS sets the goat's size."""
    L = layout(sheet_of(pose))
    c = L["cells"][pose]
    W, H, cw, ch = L["width"], L["height"], L["cell_w"], L["cell_h"]
    y0 = c["row"] * ch
    style = (f'--beat:-{beat}s;--edge:{_pct(100 * L["edge"] / ch)};aspect-ratio:{cw}/{ch};background-image:url({stamped(L["file"])});'
             f'background-size:{_pct(100 * W / cw)} auto;background-position:0 {_pct(100 * y0 / (H - ch)) if H > ch else "0"}')
    eyes = ""
    e = c["eyes"]
    if e:
        eyes = (f'<i class="goat-blink" style="left:{_pct(100 * e["x"] / cw)};top:{_pct(100 * e["y"] / ch)};'
                f'width:{_pct(100 * e["w"] / cw)};height:{_pct(100 * e["h"] / ch)};background-size:{_pct(100 * W / e["w"])} auto;'
                f'background-position:{_pct(100 * e["sx"] / (W - e["w"]))} {_pct(100 * e["sy"] / (H - e["h"]))}"></i>')
    turn = ""
    tr = c.get("turn")
    if tr:
        T = L["turns"]
        # For the companion: the head band's box on the cell, its sheet, and where its left and right heads are on it.
        turn = (f' data-turn="{stamped(T["file"])}|{_pct(100 * tr["x"] / cw)}|{_pct(100 * tr["y"] / ch)}|{_pct(100 * tr["w"] / cw)}|'
                f'{_pct(100 * tr["h"] / ch)}|{_pct(100 * T["width"] / tr["w"])}|{_pct(100 * tr["ty"] / (T["height"] - tr["h"])) if T["height"] > tr["h"] else "0%"}|'
                f'{_pct(100 * (tr["w"] + 2) / (T["width"] - tr["w"]))}|{_pct(100 * tr["cut"] / ch)}"')
    gaze = f' data-gaze="{stamped(gaze_layout(pose)["file"])}"' if manifest()[pose].get("gaze") else ""
    return f'<span class="goat {cls}" aria-hidden="true" data-goat="{pose}"{turn}{gaze} style="{style}">{eyes}</span>'


def single(pose: str) -> tuple[str, int, int]:
    """A goat shown on its own: its file and size."""
    m = manifest()[pose]
    k = SINGLE / max(m["w"], m["h"])
    return stamped(f"{WEB}/{pose}.webp"), round(m["w"] * k), round(m["h"] * k)


def _images():
    """Every image the site needs, with its size and a function that draws it (with Pillow)."""
    def open_(p, size):
        from PIL import Image
        return Image.open(ART / f"{p}.webp").convert("RGBA").resize(size, Image.LANCZOS)

    for name in sets():
        L = layout(name)

        def draw(L=L):
            from PIL import Image
            sheet = Image.new("RGBA", (L["width"], L["height"]), (0, 0, 0, 0))
            for p, c in L["cells"].items():
                sheet.alpha_composite(open_(p, (c["w"], c["h"])), (c["x"], c["row"] * L["cell_h"] + c["y"]))
                e = c["eyes"]
                if e:
                    under = open_(p, (c["w"], c["h"]))
                    under.alpha_composite(Image.open(ART / f"{p}-blink.webp").convert("RGBA").resize((c["w"], c["h"]), Image.LANCZOS))
                    sheet.alpha_composite(under.crop((e["bx"], e["by"], e["bx"] + e["w"], e["by"] + e["h"])), (e["sx"], e["sy"]))
            return sheet
        yield ROOT / "site" / L["file"], (L["width"], L["height"]), draw
        if L["turns"]:
            T = L["turns"]

            def draw_turns(L=L, T=T):
                from PIL import Image
                sheet = Image.new("RGBA", (T["width"], T["height"]), (0, 0, 0, 0))
                for p, c in L["cells"].items():
                    tr = c.get("turn")
                    if not tr:
                        continue
                    for col, side in enumerate(("left", "right")):
                        f = Image.open(ART / f"{p}-turn-{side}.webp").convert("RGBA")
                        full = f.resize((tr["w"], round(f.height * tr["w"] / f.width)), Image.LANCZOS)
                        sheet.alpha_composite(full.crop((0, 0, tr["w"], tr["h"])), (col * (tr["w"] + 2), tr["ty"]))
                return sheet
            yield ROOT / "site" / T["file"], (T["width"], T["height"]), draw_turns
    # A speaker's goat painted looking in nine directions (ADR goatchi-full-game, amended 2026-10-31): a sheet of
    # nine cells, each the shape of the goat's cell on its own sheet, the goat in the same place in each, so the
    # companion swaps the whole sheet in and only the head seems to move.
    for p in gazers():
        G = gaze_layout(p)

        def draw_gaze(p=p, G=G):
            from PIL import Image
            sheet = Image.new("RGBA", (G["width"], G["height"]), (0, 0, 0, 0))
            c = G["cell"]
            for r in range(3):
                for col in range(3):
                    sheet.alpha_composite(open_(f"{p}-gaze-{r}{col}", (c["w"], c["h"])), (col * G["cell_w"] + c["x"], r * G["cell_h"] + c["y"]))
            return sheet
        yield ROOT / "site" / G["file"], (G["width"], G["height"]), draw_gaze
    for p in singles():
        path, w, h = single(p)
        path = path.split("?")[0]
        yield ROOT / "site" / path, (w, h), (lambda p=p, w=w, h=h: open_(p, (w, h)))


def masters() -> bool:
    """Whether the painted masters are on this machine."""
    return all((ART / f"{p}.webp").exists() for p in manifest())


def build() -> int:
    if not masters():
        print("the goat's painted masters are not on this machine (art/goat/ is kept out of the repository): checking instead")
        return check()
    OUT.mkdir(parents=True, exist_ok=True)
    keep = set()
    for path, _, draw in _images():
        draw().save(path, quality=QUALITY, method=6)
        keep.add(path.name)
        print(f"wrote {path.relative_to(ROOT)}: {path.stat().st_size // 1024} KB")
    for old in OUT.glob("*.webp"):
        if old.name not in keep:
            old.unlink()
            print(f"removed {old.relative_to(ROOT)}")
    return 0


def webp_size(path: Path) -> tuple[int, int]:
    """A WebP image's size, read from its header, so the check needs no Pillow."""
    head = path.read_bytes()[:30]
    if head[12:16] == b"VP8X":
        return 1 + int.from_bytes(head[24:27], "little"), 1 + int.from_bytes(head[27:30], "little")
    if head[12:16] == b"VP8L":
        bits = int.from_bytes(head[21:25], "little")
        return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    return int.from_bytes(head[26:28], "little") & 0x3FFF, int.from_bytes(head[28:30], "little") & 0x3FFF


def check() -> int:
    bad = []
    names = set()
    for path, size, _ in _images():
        names.add(path.name)
        if not path.exists():
            bad.append(f"{path.relative_to(ROOT)} is missing")
        elif webp_size(path) != size:
            bad.append(f"{path.relative_to(ROOT)} does not match the masters")
    bad += [f"{p.relative_to(ROOT)} is not made from a master" for p in OUT.glob("*.webp") if p.name not in names]
    for b in bad:
        print(b + ": run python3 tools/goat_atlas.py build")
    if not bad:
        print("the goat's images are current")
    return 1 if bad else 0


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["check"])[0]
    sys.exit(build() if cmd == "build" else check())
