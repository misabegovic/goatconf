"""Goatchi, the goat game on its own page: which goats can be kept, and a speaker's goat only with their yes."""

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import goat_atlas  # noqa: E402
import goatchi  # noqa: E402
import speakers  # noqa: E402


def test_the_plain_goat_and_the_role_goats_can_be_kept():
    poses = [g["pose"] for g in goatchi.goats([])]
    assert poses[0] == "sitting"
    for role in ("sticker-host", "sticker-coder", "sticker-speaker", "sticker-cook", "sticker-pirate", "sticker-hidden"):
        assert role in poses


def test_a_speakers_goat_can_be_kept_only_once_they_said_yes():
    asked = [("amar-mahmutbegovic", {"name": "Amar Mahmutbegović"}),
             ("dejan-menges", {"name": "Dejan Menges", "goat_keep": True})]
    poses = [g["pose"] for g in goatchi.goats(asked)]
    assert "speaker-dejan-menges-sitting" in poses
    assert "speaker-amar-mahmutbegovic-sitting" not in poses
    dejan = next(g for g in goatchi.goats(asked) if g["pose"] == "speaker-dejan-menges-sitting")
    # A speaker's goat links to its speaker's page, which cheers it up.
    assert dejan["speaker"] == "speaker-dejan-menges.html"


def test_every_goat_and_its_food_and_sleep_are_single_images_on_the_site():
    names = set(goat_atlas.singles())
    for g in goatchi.goats([]):
        assert g["pose"] in names
    for pose in goatchi.FOOD + ("asleep",):
        assert pose in names


def test_the_page_carries_the_goats_and_loads_its_own_script():
    html = goatchi.page()
    assert 'data-pose="sitting"' in html
    assert '<script src="goatchi.js" defer></script>' in html
    # The companion goat stays away: no goat on this page is one of its places.
    assert 'class="goat ' not in html


def test_a_speakers_yes_to_goatchi_must_be_yes(tmp_path):
    record = tmp_path / "jane-doe.md"
    record.write_text("---\nname: Jane Doe\npublish: yes\ngoat_keep: maybe\n---\nJane builds things.\n", encoding="utf-8")
    problems, _, _ = speakers.check_speaker(record, set())
    assert any("goat_keep" in p for p in problems)
