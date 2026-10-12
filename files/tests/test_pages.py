"""The publish workflow: exactly one, unchanged, and nothing else allowed."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
pages = importlib.import_module("pages")


def _point_at(tmp_path, monkeypatch):
    monkeypatch.setattr(pages, "WORKFLOWS", tmp_path / ".github" / "workflows")
    return pages.WORKFLOWS


def test_missing_workflow_fails(tmp_path, monkeypatch):
    _point_at(tmp_path, monkeypatch)
    assert any("missing" in p for p in pages.problems())


def test_built_workflow_passes(tmp_path, monkeypatch):
    _point_at(tmp_path, monkeypatch)
    assert pages.main(["build"]) == 0
    assert pages.problems() == []


def test_edited_workflow_fails(tmp_path, monkeypatch):
    wf = _point_at(tmp_path, monkeypatch)
    pages.main(["build"])
    (wf / pages.NAME).write_text(pages.WORKFLOW + "      - run: make deploy\n")
    assert any("differs" in p for p in pages.problems())


def test_any_other_workflow_fails(tmp_path, monkeypatch):
    wf = _point_at(tmp_path, monkeypatch)
    pages.main(["build"])
    (wf / "ci.yml").write_text("name: ci\n")
    assert any("ci.yml" in p for p in pages.problems())


def test_workflow_only_uploads_the_site():
    assert "path: files/site" in pages.WORKFLOW
    assert "run:" not in pages.WORKFLOW
    for action in ("checkout", "configure-pages", "upload-pages-artifact", "deploy-pages"):
        assert f"actions/{action}@" in pages.WORKFLOW
