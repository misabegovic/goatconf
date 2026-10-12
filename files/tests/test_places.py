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
