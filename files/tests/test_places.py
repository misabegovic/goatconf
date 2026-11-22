"""Places on the travel page: only approved places show, and pins never overlap."""

import importlib
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def test_unapproved_places_stay_off_the_page():
    places = importlib.reload(importlib.import_module("places"))
    data, ways = places.load()
    for section in ("eat", "stay"):
        for p in data[section]:
            p["approved"] = False
        assert "still checking" in places.block(data, ways, section, False)


def test_approved_places_get_a_map_and_far_ones_are_noted():
    places = importlib.reload(importlib.import_module("places"))
    data, ways = places.load()
    for p in data["eat"]:
        p["approved"] = True
    html = places.block(data, ways, "eat", False)
    assert '<svg class="map"' in html and "OpenStreetMap" in html
    assert html.count('class="place"') == len(data["eat"])
    far = [p for p in data["eat"] if places.metres((data["ipi"]["lat"], data["ipi"]["lon"]), (p["lat"], p["lon"])) > places.NEAR_M]
    assert html.count("Off the map") == len(far)


def test_pins_are_pushed_apart_and_off_ipi():
    places = importlib.reload(importlib.import_module("places"))
    out = places.relax([(100, 100), (101, 100), (100, 101)], 20, fixed=[(100, 100, 30)])
    for i in range(len(out)):
        assert math.hypot(out[i][0] - 100, out[i][1] - 100) >= 50 - 0.5
        for j in range(i + 1, len(out)):
            assert math.hypot(out[i][0] - out[j][0], out[i][1] - out[j][1]) >= 40


def test_a_pins_press_area_is_the_ground_nearest_to_it():
    """Where two pins' rings meet, each keeps its own side of the line midway between them, and a pin alone keeps
    its whole ring (sources/conversations/2026-11-22--org--anything-left-lets-iterate.md)."""
    places = importlib.reload(importlib.import_module("places"))
    pins = [(0, 0), (100, 0), (50, 90), (400, 400)]
    shapes = places.cells(pins, 73.6)
    assert shapes[3] is None and all(s for s in shapes[:3])
    for i, (x, y) in enumerate(pins[:3]):
        corners = [(x + px, y + py) for px, py in shapes[i]]
        for cx, cy in corners:
            own = math.hypot(cx - x, cy - y)
            assert own <= 73.6 + 0.01
            assert all(own <= math.hypot(cx - qx, cy - qy) + 0.01 for qx, qy in pins)
        # The dot itself (48 units at its phone size, pins standing 100 apart) is inside its own share.
        edges = zip(corners, corners[1:] + corners[:1])
        assert all(abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / math.hypot(bx - ax, by - ay) >= 48 for (ax, ay), (bx, by) in edges)
