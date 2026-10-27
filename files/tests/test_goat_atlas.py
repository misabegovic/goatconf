"""The goat's sprite sheets: the layout, the markup the companion reads, and the check without Pillow."""

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import goat_atlas  # noqa: E402


def test_the_sheets_on_the_site_match_the_manifest():
    # The check reads image sizes from the WebP headers, so it needs no Pillow and no masters.
    assert goat_atlas.check() == 0


def test_every_peeking_goat_is_placed_with_its_edge_and_its_blink():
    man = goat_atlas.manifest()
    for name in ("roles", "speakers"):
        L = goat_atlas.layout(name)
        for pose, cell in L["cells"].items():
            m = man[pose]
            # The edge line is the same in every cell, so every goat stands on the slot's edge.
            assert cell["y"] + round(m["edge"] * L["scale"]) == L["edge"], pose
            assert 0 <= cell["x"] and cell["x"] + cell["w"] <= L["cell_w"], pose
            if m["eyes"]:
                assert cell["eyes"]["sx"] >= L["cell_w"], pose  # the eye patches sit beside the goats


def test_a_goat_that_turns_carries_its_head_band_and_its_cut_line():
    man = goat_atlas.manifest()
    turning = [p for p in goat_atlas.sets()["roles"][0] if man[p].get("turn")]
    assert turning, "no role goat turns"
    html = goat_atlas.goat(turning[0], "peek peek--art")
    parts = html.split('data-turn="')[1].split('"')[0].split("|")
    assert parts[0].endswith("-turns.webp") and len(parts) == 9
    # The cut line, where the turned head band ends and the goat's own body begins, lies inside the goat.
    assert 0 < float(parts[8].rstrip("%")) < 100
    still = [p for p in goat_atlas.sets()["roles"][0] if not man[p].get("turn")]
    for p in still:
        assert "data-turn" not in goat_atlas.goat(p, "peek")


def test_webp_size_reads_all_three_kinds_of_header(tmp_path):
    lossy = b"RIFF\x00\x00\x00\x00WEBPVP8 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" + (300).to_bytes(2, "little") + (200).to_bytes(2, "little")
    (tmp_path / "a.webp").write_bytes(lossy)
    assert goat_atlas.webp_size(tmp_path / "a.webp") == (300, 200)
    ext = b"RIFF\x00\x00\x00\x00WEBPVP8X" + bytes(8) + (299).to_bytes(3, "little") + (199).to_bytes(3, "little")
    (tmp_path / "b.webp").write_bytes(ext)
    assert goat_atlas.webp_size(tmp_path / "b.webp") == (300, 200)
    bits = (300 - 1) | ((200 - 1) << 14)
    lossless = b"RIFF\x00\x00\x00\x00WEBPVP8L" + bytes(4) + b"\x2f" + bits.to_bytes(4, "little")
    (tmp_path / "c.webp").write_bytes(lossless)
    assert goat_atlas.webp_size(tmp_path / "c.webp") == (300, 200)
