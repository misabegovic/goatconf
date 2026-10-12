#!/usr/bin/env python3
"""Places to eat and stay: two drawn maps and their lists, on the travel page.

The places live in places/places.yml; only those with approved: true are
shown. The streets, water and parks come from an OpenStreetMap extract kept in
sources/web/osm/. The maps are drawn as inline SVG in the site's colours, with
numbered pins that match the lists below them; pins that crowd together are
nudged apart, with a thin line back to the true spot.

  build [--check] [--all]   write the blocks between <!-- places:eat --> and
                            <!-- places:stay --> in site/travel.html; --all
                            also shows unapproved places (for a preview only);
                            --check fails if the page is not current

Usage: python3 tools/places.py build [--check] [--all]
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "places" / "places.yml"
OSM = ROOT / "sources" / "web" / "osm" / "tuzla-centre-ways-2026-10-12.json"
PAGE = ROOT / "site" / "travel.html"
W = 1000
NEAR_M = 650  # places further than this from IPI are listed, but left off the map
esc = html.escape

STREET = {"primary": 9, "trunk": 9, "secondary": 7.5, "tertiary": 6, "residential": 4.2, "unclassified": 4.2,
          "living_street": 4.2, "pedestrian": 5.5, "service": 2.4, "footway": 1.4}


def load():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    ways = json.loads(OSM.read_text(encoding="utf-8"))["ways"]
    return data, ways


class View:
    """Equirectangular projection of a lat/lon box onto a W-wide drawing."""

    def __init__(self, pts, pad=0.0011):
        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        self.s, self.n = min(lats) - pad, max(lats) + pad
        self.w, self.e = min(lons) - pad * 1.3, max(lons) + pad * 1.3
        self.k = math.cos(math.radians((self.s + self.n) / 2))
        span_x = (self.e - self.w) * self.k
        span_y = self.n - self.s
        # keep the drawing between 3:4 (tall) and 16:9 (wide)
        ratio = span_y / span_x
        if ratio > 1.3:
            extra = (span_y / 1.3 - span_x) / self.k / 2
            self.w -= extra; self.e += extra
        elif ratio < 0.56:
            extra = (span_x * 0.56 - span_y) / 2
            self.s -= extra; self.n += extra
        self.scale = W / ((self.e - self.w) * self.k)
        self.h = round((self.n - self.s) * self.scale)

    def xy(self, lat, lon):
        return ((lon - self.w) * self.k * self.scale, (self.n - lat) * self.scale)

    def inside(self, lat, lon, margin=0.002):
        return self.s - margin <= lat <= self.n + margin and self.w - margin <= lon <= self.e + margin


def path(view, geom, close=False):
    pts = [view.xy(a, b) for a, b in geom]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def base(view, ways) -> str:
    water, parks, roads, small, labels = [], [], {}, [], []
    for w in ways:
        g = w["geometry"]
        if not any(view.inside(a, b) for a, b in g):
            continue
        t = w["tags"]
        name = t.get("name", "").upper()
        if t.get("natural") == "water":
            # skip hydrants, valves and shafts that are mistagged as lakes
            if any(k in name for k in ("HIDRANT", "ŠIBER", "ŠAHT", "REZERVOAR")) or len(g) < 6:
                continue
            water.append(f'<path d="{path(view, g, True)}"/>')
        elif t.get("leisure") in ("park", "garden", "water_park"):
            parks.append(f'<path d="{path(view, g, True)}"/>')
        elif t.get("waterway") in ("river", "canal", "stream"):
            water.append(f'<path class="river" d="{path(view, g)}"/>')
        elif t.get("highway") in STREET:
            hw = t["highway"]
            if hw == "footway":
                small.append(f'<path d="{path(view, g)}"/>')
            else:
                roads.setdefault(hw, []).append(path(view, g))
    out = [f'<rect width="{W}" height="{view.h}" fill="#edf2fb"/>',
           f'<g fill="#d9f2df">{"".join(parks)}</g>',
           f'<g fill="#a9c7f2" stroke="#a9c7f2" stroke-width="3" class="water">{"".join(water)}</g>',
           f'<g fill="none" stroke="#ffffff" stroke-width="1.4" stroke-linecap="round" opacity=".9">{"".join(small)}</g>']
    order = ["service", "residential", "unclassified", "living_street", "tertiary", "secondary", "primary", "trunk", "pedestrian"]
    for hw in order:
        if hw not in roads:
            continue
        wdt = STREET[hw]
        color = "#fff3b0" if hw == "pedestrian" else "#ffffff"
        casing = "#c9d7f5"
        d = " ".join(roads[hw])
        out.append(f'<path d="{d}" fill="none" stroke="{casing}" stroke-width="{wdt + 2.4}" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{wdt}" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)


def relax(points, r, fixed=()):
    """Nudge pins apart so none overlap, and off the fixed markers; returns new positions."""
    pos = [list(p) for p in points]
    for _ in range(160):
        moved = False
        for fx, fy, fr in fixed:
            for q in pos:
                dx, dy = q[0] - fx, q[1] - fy
                d = math.hypot(dx, dy) or 0.01
                if d < r + fr + 4:
                    ux, uy = (dx / d, dy / d) if d > 0.02 else (0, 1)
                    q[0] += ux * (r + fr + 4 - d); q[1] += uy * (r + fr + 4 - d)
                    moved = True
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
                d = math.hypot(dx, dy) or 0.01
                if d < 2 * r + 4:
                    push = (2 * r + 4 - d) / 2
                    ux, uy = (dx / d, dy / d) if d > 0.02 else (1, 0)
                    pos[i][0] -= ux * push; pos[i][1] -= uy * push
                    pos[j][0] += ux * push; pos[j][1] += uy * push
                    moved = True
        if not moved:
            break
    return pos


def landmark(view, lat, lon, label, kind):
    x, y = view.xy(lat, lon)
    if kind == "ipi":
        return (f'<g transform="translate({x:.1f} {y:.1f})"><circle r="36" fill="#051d47"/><circle r="30" fill="#ffd400"/>'
                f'<text y="10" text-anchor="middle" class="map-ipi">IPI</text></g>')
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" class="map-label">{label}</text>'


def map_svg(view, ways, data, items, prefix, color, ink, title) -> str:
    pins = [view.xy(p["lat"], p["lon"]) for p in items]
    r = 30
    ix, iy = view.xy(data["ipi"]["lat"], data["ipi"]["lon"])
    placed = relax(pins, r, fixed=[(ix, iy, 36)])
    lines, dots = [], []
    for i, ((x0, y0), (x, y)) in enumerate(zip(pins, placed), start=1):
        if math.hypot(x - x0, y - y0) > 3:
            lines.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y:.1f}"/><circle cx="{x0:.1f}" cy="{y0:.1f}" r="4"/>')
        dots.append(f'<a href="#{prefix}-{i}"><g class="pin" transform="translate({x:.1f} {y:.1f})"><circle r="{r}" fill="{color}" stroke="#ffffff" stroke-width="4"/>'
                    f'<text y="11" text-anchor="middle" fill="{ink}">{i}</text></g></a>')
    lm = [landmark(view, data["trg_slobode"]["lat"], data["trg_slobode"]["lon"] - 0.0004, "Freedom Square", "label")]
    lakes = [w for w in ways if w["tags"].get("name", "").startswith("Panonsko jezero")]
    pts = [(a, b) for w in lakes for a, b in w["geometry"] if view.inside(a, b, margin=0)]
    if len(pts) > 10:
        la = sum(a for a, _ in pts) / len(pts); lo = sum(b for _, b in pts) / len(pts)
        lm.append(landmark(view, la - 0.0004, lo, "Pannonian Lakes", "label"))
    ipi = landmark(view, data["ipi"]["lat"], data["ipi"]["lon"], "IPI Academy", "ipi")
    return (f'<svg class="map" viewBox="0 0 {W} {view.h}" role="img" aria-labelledby="{prefix}-map-title">'
            f'<title id="{prefix}-map-title">{esc(title)}</title>'
            f'{base(view, ways)}<g class="map-lines" stroke="#051d47" stroke-width="2" fill="#051d47">{"".join(lines)}</g>'
            f'{"".join(lm)}{ipi}{"".join(dots)}</svg>')


def metres(a, b) -> float:
    dy = (a[0] - b[0]) * 111_320
    dx = (a[1] - b[1]) * 111_320 * math.cos(math.radians(a[0]))
    return math.hypot(dx, dy)


def direction(frm, to) -> str:
    dy, dx = to[0] - frm[0], (to[1] - frm[1]) * math.cos(math.radians(frm[0]))
    ang = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    return ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"][int((ang + 22.5) // 45) % 8]


def diet(p) -> str:
    bits = []
    if p.get("vegetarian") == "yes":
        bits.append('<span class="tag tag--veg">Vegetarian options</span>')
    if p.get("vegan") == "yes":
        bits.append('<span class="tag tag--veg">Vegan options</span>')
    return " ".join(bits)


def item(p, i, prefix, off=None) -> str:
    maps = f"https://www.openstreetmap.org/?mlat={p['lat']}&mlon={p['lon']}#map=19/{p['lat']}/{p['lon']}"
    site = f' <a href="{esc(p["url"])}">Website</a>' if p.get("url") else ""
    price = f'<span class="place__price">{esc(str(p["price_note"]))}</span>' if p.get("price_note") else ""
    return (f'  <li class="place" id="{prefix}-{i}"><span class="place__num">{i}</span><div>'
            f'<strong>{esc(p["name"])}</strong> <span class="place__kind">{esc(p["kind"])}</span>'
            f'<p>{esc(p["offers"])}</p>{price}{diet(p)}'
            + (f'<span class="place__price">Off the map: about {off} from IPI Academy.</span>' if off else "")
            + f'<p class="place__links">{esc(p.get("address", ""))} <a href="{maps}">Open in maps</a>{site}</p></div></li>')


def block(data, ways, section, show_all) -> str:
    items = [p for p in data[section] if show_all or p.get("approved") is True]
    if not items:
        if section == "eat":
            return ('<p class="ledger-empty">We are still checking which cafés and restaurants near IPI Academy and Freedom Square to recommend, '
                    'and which serve vegetarian or vegan food. The map and the list will be here.</p>')
        return '<p class="ledger-empty">We are still checking places to stay within a walk of IPI Academy. The map and the list will be here.</p>'
    ipi = (data["ipi"]["lat"], data["ipi"]["lon"])
    near = [p for p in items if metres(ipi, (p["lat"], p["lon"])) <= NEAR_M]
    far = [p for p in items if p not in near]
    items = near + far  # numbers on the map first, then the ones further out
    view = View([(p["lat"], p["lon"]) for p in near] + [ipi])
    eat = section == "eat"
    svg = map_svg(view, ways, data, near, section, "#ffd400" if eat else "#0b3d91", "#051d47" if eat else "#ffffff",
                  "Map of places to eat and drink near IPI Academy" if eat else "Map of places to stay near IPI Academy")
    def off(p):
        if p in near:
            return None
        m = metres(ipi, (p["lat"], p["lon"]))
        return f"{round(m / 50) * 50} m {direction(ipi, (p['lat'], p['lon']))}"
    lis = "\n".join(item(p, i, section, off(p)) for i, p in enumerate(items, start=1))
    checked = data["checked"]
    note = ("Ask each place which dishes are vegetarian or vegan. " if eat else "Prices change: check the date, then the place itself. ")
    return (f'<figure class="map-frame">{svg}<figcaption>Map data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors.</figcaption></figure>\n'
            f'<ol class="places">\n{lis}\n</ol>\n<p class="checked">{note}Checked on {checked}.</p>')


def page(show_all=False) -> str:
    data, ways = load()
    text = PAGE.read_text(encoding="utf-8")
    for section in ("eat", "stay"):
        start, end = f"<!-- places:{section} -->", f"<!-- /places:{section} -->"
        pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
        if not pat.search(text):
            raise SystemExit(f"site/travel.html has no {start} block")
        filled = f"{start}\n{block(data, ways, section, show_all)}\n{end}"
        text = pat.sub(lambda _m: filled, text, count=1)
    return text


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--check", action="store_true")
    b.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    want = page(a.all)
    if a.check:
        if PAGE.read_text(encoding="utf-8") != want:
            print("site/travel.html places are out of date: run python3 tools/places.py build")
            return 1
        print("site/travel.html places are current")
        return 0
    PAGE.write_text(want, encoding="utf-8")
    print("wrote site/travel.html" + (" (all places, preview)" if a.all else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
