#!/usr/bin/env python3
"""The goats post ("The goats are in"): the card with the painted goats, still and animated.

The card's lettering and seal come from tools/shareables.py (headless Chrome); the goats are laid on it here, each
fitted into its own cell of a grid so no two touch. The animation has them pop up one by one, stretch and settle,
bob and wiggle for a while, then duck away so the loop starts again.

  render    write site/share/post-goats-are-in-{square,wide}.png, .mp4 and .gif (needs Chrome, Pillow, ffmpeg
            and the painted masters in art/goat/)

Usage: python3 tools/goats_post.py render
(ADR wiki/org/adrs/goat-mascot.md)
"""
from __future__ import annotations

import math
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand  # noqa: E402
import goat_atlas  # noqa: E402
import shareables  # noqa: E402

OUT = shareables.OUT
SCENES = ("sticker-salt-lakes", "sticker-hike", "sticker-cevapi", "sticker-pannonian-sea")
ROLES = ("sticker-host", "sticker-coder", "sticker-pirate", "sticker-cook")
# Each card: its size, and the box the goats fill (left, top, right, bottom), as two rows of four.
CARDS = {"square": (1080, 1080, (40, 372, 1040, 1052)), "wide": (1200, 675, (470, 150, 1176, 660))}
FPS = 25
GAP = 14


def goat(pose: str):
    from PIL import Image
    im = Image.open(goat_atlas.ART / f"{pose}.webp").convert("RGBA")
    return im.crop(im.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox())


def layout(box):
    """Each goat fitted into its own cell, standing on the cell's floor and centred in it."""
    from PIL import Image
    x0, y0, x1, y1 = box
    rows = (SCENES, ROLES)
    cw, ch = (x1 - x0) / 4, (y1 - y0) / 2
    placed = []
    for r, row in enumerate(rows):
        for c, pose in enumerate(row):
            im = goat(pose)
            k = min((cw - GAP) / im.width, (ch - GAP) / im.height)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
            x = round(x0 + c * cw + (cw - im.width) / 2)
            y = round(y0 + (r + 1) * ch - GAP / 2 - im.height)
            placed.append((im, x, y))
    return placed


def overlaps(placed) -> bool:
    boxes = [(x, y, x + im.width, y + im.height) for im, x, y in placed]
    return any(a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3] for i, a in enumerate(boxes) for b in boxes[i + 1:])


def pose_at(t: float, i: int, total: float):
    """A goat's scale, lift and tilt at time t: popping up in turn, idling, then ducking away at the end."""
    start = 0.35 + i * 0.13
    leave = total - 0.75 + i * 0.03
    if t < start:
        return 0.0, 0.0, 0.0
    if t > leave:
        u = min(1.0, (t - leave) / 0.32)
        return max(0.0, 1.0 - u * u * 1.05), 0.0, 0.0
    u = (t - start) / 0.55
    if u < 1:
        # Out from nothing, a little too big and tall, then a squash, then settled.
        keys = ((0, 0.0), (0.55, 1.1), (0.78, 0.95), (1, 1.0))
        for (a, va), (b, vb) in zip(keys, keys[1:]):
            if a <= u <= b:
                s = va + (vb - va) * (0.5 - 0.5 * math.cos(math.pi * (u - a) / (b - a)))
                return s, 0.0, 0.0
    idle = t - start - 0.55
    lift = 7 * max(0.0, math.sin(idle * 2 * math.pi / 1.6 + i * 0.9))
    tilt = 4 * math.sin(idle * 2 * math.pi / 0.9) * math.exp(-((idle - 1.2 - (i % 4) * 0.35) ** 2) / 0.05)
    return 1.0, lift, tilt


def frame(bg, placed, t: float, total: float):
    from PIL import Image
    canvas = bg.copy()
    for i, (im, x, y) in enumerate(placed):
        s, lift, tilt = pose_at(t, i, total)
        if s <= 0.01:
            continue
        g = im if (s == 1 and not tilt) else im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.BICUBIC)
        if tilt:
            g = g.rotate(tilt, resample=Image.BICUBIC, expand=True)
        # Anchored at the middle of its feet.
        gx = round(x + im.width / 2 - g.width / 2)
        gy = round(y + im.height - g.height - lift)
        canvas.alpha_composite(g, (gx, gy))
    return canvas


def render() -> int:
    from PIL import Image
    exe = brand.chrome()
    total = 5.0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, (w, h, box) in CARDS.items():
            shareables.render(f"bg-{name}.png", w, h, shareables.goats_post(w, h, name == "square", crowd_in=False), tmp, exe)
            bg = Image.open(OUT / f"bg-{name}.png").convert("RGBA")
            (OUT / f"bg-{name}.png").unlink()
            placed = layout(box)
            if overlaps(placed):
                raise SystemExit(f"the goats overlap on the {name} card")
            # The still card: every goat settled.
            frame(bg, placed, total / 2, total).convert("RGB").save(OUT / f"post-goats-are-in-{name}.png", optimize=True)
            frames = tmp / name
            frames.mkdir()
            for f in range(int(total * FPS)):
                frame(bg, placed, f / FPS, total).convert("RGB").save(frames / f"{f:04d}.png")
            mp4 = OUT / f"post-goats-are-in-{name}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
                            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2:color=0x0b3d91", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(mp4)], check=True)
            gif = OUT / f"post-goats-are-in-{name}.gif"
            scale = "720:-1" if name == "square" else "800:-1"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
                            "-vf", f"fps=15,scale={scale}:flags=lanczos,split[a][b];[a]palettegen=max_colors=200:stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a",
                            "-loop", "0", str(gif)], check=True)
            for f in (OUT / f"post-goats-are-in-{name}.png", mp4, gif):
                print(f"wrote site/share/{f.name}: {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(render() if (sys.argv[1:] or ["render"])[0] == "render" else 1)
