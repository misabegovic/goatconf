"""Photos for the site: every shown JPG is wrapped for its WebP copies, the same way twice."""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def test_wrap_lists_the_copies_and_is_stable():
    images = importlib.reload(importlib.import_module("images"))
    src = sorted(images.shown())[0]
    widths = [w for w, _ in images.copies(src)]
    page = f'<p><img class="page-head__photo" src="{src}" alt=""></p>'
    once = images.wrap(page)
    assert once.startswith('<p><picture><source type="image/webp" srcset="')
    assert all(f"-{w}.webp {w}w" in once for w in widths)
    assert images.SIZES["page-head__photo"] in once
    assert images.wrap(once) == once


def test_a_jpg_without_copies_stays_as_it_is():
    images = importlib.reload(importlib.import_module("images"))
    page = '<img src="img/no-such-photo.jpg" alt="">'
    assert images.wrap(page) == page
