"""The brand kit's drawing rules (tools/brand.py): the goat's outline and the lockup's lettering."""

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import brand  # noqa: E402


def ink_span(run: str, x: float, size: float, spacing: float) -> tuple[float, float]:
    """Where a run's ink starts and ends when `straight` sets it from x."""
    gs = brand.glyphs(run)
    adv = brand.advances(gs, size, spacing)
    last_x = x + sum(adv[:-1])
    return x + brand.ink(gs[0]["d"])[0] * size / 1000, last_x + brand.ink(gs[-1]["d"])[1] * size / 1000


def test_ink_reads_every_point_of_an_outline():
    assert brand.ink("M9 0 132 660H373L494 0H325ZM126 110V208H386V110Z") == (9, 494, 660)
    left, right, top = brand.ink("M0 0Q50 100 100 0Z")  # a curve tops out at half its control point's height
    assert (left, right) == (0, 100) and math.isclose(top, 50)


def test_the_lockups_word_and_line_share_their_edges():
    wx, size, word_spacing = brand.fitted("word", 372, 876, spacing=0.5)
    lx, line_size, line_spacing = brand.fitted("line", 372, 876, size=32)
    for span in (ink_span("word", wx, size, word_spacing), ink_span("line", lx, line_size, line_spacing)):
        assert math.isclose(span[0], 372, abs_tol=0.01) and math.isclose(span[1], 876, abs_tol=0.01)
    assert line_spacing > 0, "the line is spaced out to the wordmark, never squeezed"


def test_the_line_is_lettered_like_the_seal():
    text, weight, width, _ = brand.RUNS["line"]
    assert text == brand.TOP_LINE and text == text.upper()
    assert (weight, width) == brand.RUNS["top"][1:3]


def test_the_trace_loses_its_one_pixel_steps():
    pts = brand.goat_points([[0, 0], [10, 0], [10, 1], [20, 10], [0, 10], [0, 0.5]])
    assert pts == [(0, 0.25), (10, 0.5), (20, 10), (0, 10)]


def test_no_curve_handle_overshoots_its_segment():
    """A handle longer than its segment drew a spur where a short segment met a long one."""
    for loop in brand.goat_path().split("Z"):
        if not loop.strip():
            continue
        n = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", loop)]
        x, y = n[0], n[1]
        for i in range(2, len(n), 6):
            ax, ay, bx, by, ex, ey = n[i:i + 6]
            reach = math.hypot(ex - x, ey - y)
            assert math.hypot(ax - x, ay - y) <= reach / 3 + 0.2
            assert math.hypot(bx - ex, by - ey) <= reach / 3 + 0.2
            x, y = ex, ey


def test_the_goat_is_cut_under_its_ring():
    for body, ring in ((brand.seal_body("#000", "#fff"), 68), (brand.coin_body("#000", "#fff"), 128)):
        assert '<clipPath id="' in body and f'<circle cx="150" cy="150" r="{ring}"/></clipPath>' in body
        assert f'<circle cx="150" cy="150" r="{ring}" fill="none"' in body
