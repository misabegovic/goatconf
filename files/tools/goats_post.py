#!/usr/bin/env python3
"""The goats post ("The goats are in"): the card with the painted goats, still and animated.

The card's lettering and seal come from tools/shareables.py (headless Chrome); the goats are laid on it here, each
fitted into its own cell of a grid so no two touch. The animation has them pop up one by one, stretch and settle,
bob and wiggle for a while, then duck away so the loop starts again.

  render      write site/share/post-goats-are-in-{square,wide}.png, .mp4 and .gif (needs Chrome, Pillow, ffmpeg
              and the painted masters in art/goat/)
  one-by-one  write site/share/post-goats-one-by-one-{square,wide}.mp4 and .gif: one goat at a time,
              whole, each changing into the next at once in the same place, every speaker's goat among them

Usage: python3 tools/goats_post.py <render|one-by-one>
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


# One goat at a time, whole, standing in the same place, each changing into the next at once and doing its own
# small move while it is there: (the goat, its move). Turning heads waits until the whole goats' turned heads are
# painted.
SEQUENCE = (
    ("sticker-host", "pop"),
    ("speaker-paul-campbell-sitting", "wiggle"),
    ("sticker-salt-lakes", "float"),
    ("speaker-carmine-paolino-sitting", "pop"),
    ("sticker-hike", "walk"),
    ("speaker-roy-tomeij-sitting", "jump"),
    ("sticker-coder", "munch"),
    ("speaker-dejan-menges-sitting", "wave"),
    ("sticker-cevapi", "munch"),
    ("speaker-amar-mahmutbegovic-sitting", "wiggle"),
    ("sticker-pannonian-sea", "jump"),
    ("speaker-cristian-planas-sitting", "pop"),
    ("sticker-pirate", "wave"),
    ("speaker-christoph-lipautz-sitting", "jump"),
    ("sticker-fildzan", "munch"),
    ("speaker-predrag-radenkovic-sitting", "wave"),
    ("sticker-burek", "pop"),
)
BEAT = 2.0      # seconds each goat is on screen
# Each card: size, the goat's centre, the line it stands on, and how tall it is.
STAGES = {"square": (1080, 1080, 540, 1010, 590), "wide": (1200, 675, 830, 640, 450)}


def ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, u)))


def keys(u, ks):
    """A value at u along (time, value) keys, eased between them."""
    for (a, va), (b, vb) in zip(ks, ks[1:]):
        if a <= u <= b:
            return va + (vb - va) * ease((u - a) / (b - a))
    return ks[-1][1]


def move(name, u):
    """A goat's own small move at u (0 to 1 of its time on screen): lift (a share of its height), scale x and y, tilt."""
    lift, sx, sy, rot = 0.0, 1.0, 1.0, 0.0
    if name == "pop":
        sy = keys(u, ((0, 1), (0.35, 1), (0.5, 1.03), (0.65, 0.99), (0.75, 1.0), (1, 1)))
        sx = 2 - sy
    elif name == "float":
        lift = 0.012 * math.sin(u * 2 * math.pi * 1.5)
        rot = 2 * math.sin(u * 2 * math.pi * 1.1)
    elif name == "wiggle":
        rot = 4 * math.sin(u * 2 * math.pi * 1.5) * math.sin(math.pi * u)
    elif name == "walk":
        steps = math.sin(u * math.pi * 6) * math.sin(math.pi * u)
        lift, rot = 0.008 * abs(steps), 1.5 * steps
    elif name == "munch":
        b = math.sin(u * math.pi * 6) ** 2 if 0.2 < u < 0.8 else 0
        sy, sx = 1 - 0.025 * b, 1 + 0.02 * b
    elif name == "jump":
        lift = 0.06 * math.sin(math.pi * max(0.0, min(1.0, (u - 0.3) / 0.35)))
    elif name == "wave":
        rot = 3 * math.sin(u * 2 * math.pi * 2) * math.sin(math.pi * u)
    return lift, sx, sy, rot


def load(pose):
    """A goat and, for a peeking goat, its turned heads, all the same size; and where its slot's edge is."""
    from PIL import Image
    man = goat_atlas.manifest()
    peek = pose.endswith(":peek")
    name = pose.split(":")[0]
    base = Image.open(goat_atlas.ART / f"{name}.webp").convert("RGBA")
    m = man[name]
    if not peek:
        box = base.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
        return {"front": base.crop(box)}, None
    pad = (m.get("turn") or {}).get("pad", 0)
    canvas = Image.new("RGBA", (base.width + 2 * pad, base.height + 2 * pad), (0, 0, 0, 0))
    canvas.alpha_composite(base, (pad, pad))
    views = {"front": canvas}
    for side in ("left", "right"):
        f = goat_atlas.ART / f"{name}-turn-{side}.webp"
        views[side] = Image.open(f).convert("RGBA").resize(canvas.size) if f.exists() else canvas
    return views, m["edge"] + pad


def one_by_one() -> int:
    from PIL import Image
    exe = brand.chrome()
    total = BEAT * len(SEQUENCE)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        goats = [load(p)[0]["front"] for p, _ in SEQUENCE]
        for name, (w, h, cx, floor, tall) in STAGES.items():
            shareables.render(f"bg-{name}.png", w, h, shareables.goats_post(w, h, name == "square", crowd_in=False), tmp, exe)
            bg = Image.open(OUT / f"bg-{name}.png").convert("RGBA")
            (OUT / f"bg-{name}.png").unlink()
            sized = [g.resize((round(g.width * tall / g.height), tall), Image.LANCZOS) for g in goats]
            frames = tmp / f"one-{name}"
            frames.mkdir()
            for f in range(int(total * FPS)):
                t = f / FPS
                k = min(int(t // BEAT), len(SEQUENCE) - 1)
                lift, sx, sy, rot = move(SEQUENCE[k][1], (t - k * BEAT) / BEAT)
                g = sized[k]
                im = g if (sx == 1 and sy == 1) else g.resize((round(g.width * sx), round(g.height * sy)), Image.BICUBIC)
                if rot:
                    im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
                canvas = bg.copy()
                # Standing on the same line, the middle of its feet in the same place.
                canvas.alpha_composite(im, (round(cx - im.width / 2), round(floor - im.height + (im.height - g.height * sy) / 2 - lift * tall)))
                canvas.convert("RGB").save(frames / f"{f:04d}.png")
            mp4 = OUT / f"post-goats-one-by-one-{name}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
                            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2:color=0x0b3d91", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                            "-crf", "21", "-movflags", "+faststart", str(mp4)], check=True)
            gif = OUT / f"post-goats-one-by-one-{name}.gif"
            scale = "540:-1" if name == "square" else "640:-1"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "%04d.png"),
                            "-vf", f"fps=10,scale={scale}:flags=lanczos,split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];[b][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
                            "-loop", "0", str(gif)], check=True)
            for f in (mp4, gif):
                print(f"wrote site/share/{f.name}: {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["render"])[0]
    sys.exit(render() if cmd == "render" else one_by_one() if cmd == "one-by-one" else 1)
