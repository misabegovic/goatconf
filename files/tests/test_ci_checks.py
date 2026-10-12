"""tools/ci_checks.py, run for real in a throwaway repository with a base branch."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "tools" / "ci_checks.py"
DASH = "\u2014"


def sh(repo, *args):
    return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "files" / "tools").mkdir(parents=True)
    shutil.copy(SCRIPT, tmp_path / "files" / "tools" / "ci_checks.py")
    for d in ("sources", "wiki", "log"):
        (tmp_path / "files" / d).mkdir()
    (tmp_path / "files" / "sources" / "a.md").write_text("verbatim " + DASH + " text\n")
    (tmp_path / "files" / "wiki" / "page.md").write_text("---\ntitle: p\nconfidence: low\n---\nOld line " + DASH + " kept.\n")
    (tmp_path / "files" / "log" / "log.md").write_text("# log\n")
    sh(tmp_path, "git", "init", "-q", "-b", "main")
    sh(tmp_path, "git", "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    sh(tmp_path, "git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "base")
    sh(tmp_path, "git", "checkout", "-q", "-b", "work")
    return tmp_path


def run(repo, check):
    return subprocess.run(
        [sys.executable, "files/tools/ci_checks.py", check, "--base", "main"],
        cwd=repo, capture_output=True, text=True,
    )


def commit(repo, message="change"):
    sh(repo, "git", "add", "-A")
    sh(repo, "git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", message)


def test_clean_branch_passes_every_check(repo):
    assert run(repo, "all").returncode == 0


def test_a_new_source_is_fine(repo):
    (repo / "files" / "sources" / "b.md").write_text("new\n")
    commit(repo)
    assert run(repo, "sources-additive").returncode == 0


def test_a_modified_source_fails_even_once_committed(repo):
    (repo / "files" / "sources" / "a.md").write_text("rewritten\n")
    commit(repo)
    r = run(repo, "sources-additive")
    assert r.returncode == 1 and "files/sources/a.md is modified" in r.stdout


def test_a_deleted_source_fails(repo):
    (repo / "files" / "sources" / "a.md").unlink()
    r = run(repo, "sources-additive")
    assert r.returncode == 1 and "deleted" in r.stdout

def test_a_source_renamed_within_files_fails(repo):
    sh(repo, "git", "mv", "files/sources/a.md", "files/sources/b.md")
    commit(repo)
    r = run(repo, "sources-additive")
    assert r.returncode == 1 and "files/sources/b.md is renamed" in r.stdout


def test_promoting_to_high_fails(repo):
    page = repo / "files" / "wiki" / "page.md"
    page.write_text(page.read_text().replace("confidence: low", "confidence: high"))
    r = run(repo, "confidence-floor")
    assert r.returncode == 1 and "files/wiki/page.md" in r.stdout


def test_a_new_page_at_high_fails(repo):
    (repo / "files" / "wiki" / "new.md").write_text("---\ntitle: n\nconfidence: high\n---\n")
    assert run(repo, "confidence-floor").returncode == 1


def test_generated_views_at_high_pass(repo):
    (repo / "files" / "wiki" / "_views").mkdir()
    (repo / "files" / "wiki" / "_views" / "by-kind.md").write_text("---\ntitle: v\nconfidence: high\n---\n")
    assert run(repo, "confidence-floor").returncode == 0


def test_a_recorded_human_promotion_passes(repo):
    page = repo / "files" / "wiki" / "page.md"
    page.write_text(page.read_text().replace("confidence: low", "confidence: high"))
    (repo / "files" / "wiki" / "_state").mkdir()
    (repo / "files" / "wiki" / "_state" / "confidence-promotions.yml").write_text(
        "- page: files/wiki/page.md\n  by: the organiser\n  date: 2026-10-07\n"
    )
    assert run(repo, "confidence-floor").returncode == 0


def test_an_added_em_dash_fails(repo):
    page = repo / "files" / "wiki" / "page.md"
    page.write_text(page.read_text() + "New line " + DASH + " not allowed.\n")
    commit(repo)
    r = run(repo, "no-em-dashes")
    assert r.returncode == 1 and "files/wiki/page.md" in r.stdout and "Old line" not in r.stdout


def test_an_em_dash_in_a_new_untracked_file_fails(repo):
    (repo / "files" / "wiki" / "draft.md").write_text("A draft " + DASH + " here.\n")
    assert run(repo, "no-em-dashes").returncode == 1


def test_em_dashes_in_sources_and_the_log_separator_pass(repo):
    (repo / "files" / "sources" / "c.md").write_text("quoted " + DASH + " verbatim\n")
    (repo / "files" / "log" / "log.md").write_text("# log\n2026-10-07 shape " + DASH + " a summary\n")
    commit(repo)
    assert run(repo, "no-em-dashes").returncode == 0


def test_a_second_em_dash_in_a_log_line_fails(repo):
    (repo / "files" / "log" / "log.md").write_text("# log\n2026-10-07 shape " + DASH + " one " + DASH + " two\n")
    assert run(repo, "no-em-dashes").returncode == 1


def test_a_source_arriving_by_rename_from_outside_files_passes(repo):
    # Faithful conversion shape: the base holds the source at the old root
    # layout; the branch moves it under files/ with a tweak. Rebuild the
    # base so the source starts outside files/.
    sh(repo, "git", "rm", "-q", "files/sources/a.md")
    (repo / "sources").mkdir()
    (repo / "sources" / "a.md").write_text("verbatim " + DASH + " text\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "base: old root layout")
    sh(repo, "git", "branch", "-f", "main", "HEAD")
    (repo / "files" / "sources").mkdir(exist_ok=True)
    (repo / "files" / "sources" / "a.md").write_text("verbatim " + DASH + " text tweaked\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "conversion")
    assert run(repo, "sources-additive").returncode == 0


@pytest.mark.parametrize("trailer", [
    "Co-Authored-By: Claude <noreply@anthropic.com>",
    "Claude-Session: https://claude.ai/code/session_x",
    "\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)",
])
def test_ai_attribution_in_a_commit_fails(repo, trailer):
    (repo / "files" / "wiki" / "x.md").write_text("x\n")
    commit(repo, "A change\n\n" + trailer)
    r = run(repo, "no-ai-attribution")
    assert r.returncode == 1 and "no-ai-attribution" in r.stdout


def test_a_human_co_author_passes(repo):
    (repo / "files" / "wiki" / "x.md").write_text("x\n")
    commit(repo, "A change\n\nCo-Authored-By: A Person <a@example.com>")
    assert run(repo, "no-ai-attribution").returncode == 0


def test_an_edit_to_a_moved_file_is_scoped_to_its_own_diff(repo):
    # The conversion moved files under files/ and edited some of them;
    # the em-dash rule must see only the lines the branch actually wrote.
    page = repo / "files" / "wiki" / "moved.md"
    page.write_text("---\ntitle: m\n---\nkept line\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "add page at new layout")
    sh(repo, "git", "rm", "-q", "files/wiki/moved.md")
    (repo / "wiki").mkdir()
    (repo / "wiki" / "moved.md").write_text("---\ntitle: m\n---\nkept line\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "base: old root layout")
    sh(repo, "git", "branch", "-f", "main", "HEAD")
    (repo / "files" / "wiki").mkdir(exist_ok=True)
    page.write_text("---\ntitle: m\n---\nkept line\nnew line " + DASH + " flagged\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "conversion with an edit")
    r = run(repo, "no-em-dashes")
    assert r.returncode == 1 and "files/wiki/moved.md" in r.stdout and "kept line" not in r.stdout


def test_a_move_with_an_edit_free_of_em_dashes_passes(repo):
    page = repo / "files" / "wiki" / "moved.md"
    page.write_text("---\ntitle: m\n---\nkept line\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "add page at new layout")
    sh(repo, "git", "rm", "-q", "files/wiki/moved.md")
    (repo / "wiki").mkdir()
    (repo / "wiki" / "moved.md").write_text("---\ntitle: m\n---\nkept line\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "base: old root layout")
    sh(repo, "git", "branch", "-f", "main", "HEAD")
    (repo / "files" / "wiki").mkdir(exist_ok=True)
    page.write_text("---\ntitle: m\n---\nkept line\nnew line, no dash here\n")
    sh(repo, "git", "add", "-A")
    commit(repo, "conversion with a clean edit")
    assert run(repo, "no-em-dashes").returncode == 0


def test_an_unknown_base_is_refused_by_name(repo):
    r = subprocess.run(
        [sys.executable, "files/tools/ci_checks.py", "all", "--base", "nope"],
        cwd=repo, capture_output=True, text=True,
    )
    assert r.returncode == 2 and "not found" in r.stderr
