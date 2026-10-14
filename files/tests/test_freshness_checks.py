"""check-home-fresh and check-readme-fresh look only at the brain under files/.

The repository root is a pi-brain layer with its own wiki/ and .claude/;
its changes must neither trigger nor satisfy the goatconf brain's checks.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

BRAIN = Path(__file__).resolve().parent.parent / "tools" / "brain.py"


def sh(repo, *args):
    subprocess.run(args, cwd=repo, capture_output=True, text=True, check=True)


def write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def commit(repo):
    sh(repo, "git", "add", "-A")
    sh(repo, "git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "change")


@pytest.fixture
def repo(tmp_path):
    for rel in ("wiki/index.md", "wiki/org/state.md", "files/wiki/index.md",
                "files/wiki/org/page.md", "files/README.md", "files/AGENTS.md"):
        write(tmp_path, rel, "# start\n")
    sh(tmp_path, "git", "init", "-q", "-b", "main")
    commit(tmp_path)
    sh(tmp_path, "git", "checkout", "-q", "-b", "work")
    return tmp_path


def check(repo, name):
    env = {**os.environ, "BRAIN_DIR": str(repo / "files")}
    # Run from the repository root on purpose: the checks must not depend on the caller's directory.
    return subprocess.run([sys.executable, str(BRAIN), name, "--base", "main"],
                          cwd=repo, capture_output=True, text=True, env=env)


def test_a_root_wiki_edit_does_not_need_this_home_page(repo):
    write(repo, "wiki/org/state.md", "# changed\n")
    commit(repo)
    assert check(repo, "check-home-fresh").returncode == 0


def test_a_brain_wiki_edit_without_the_home_page_fails(repo):
    write(repo, "files/wiki/org/page.md", "# changed\n")
    commit(repo)
    r = check(repo, "check-home-fresh")
    assert r.returncode == 1 and "wiki/org/page.md" in r.stderr


def test_a_root_home_page_edit_does_not_satisfy_the_brain(repo):
    write(repo, "files/wiki/org/page.md", "# changed\n")
    write(repo, "wiki/index.md", "# root home changed\n")
    commit(repo)
    assert check(repo, "check-home-fresh").returncode == 1


def test_a_brain_wiki_edit_with_a_visible_home_change_passes(repo):
    write(repo, "files/wiki/org/page.md", "# changed\n")
    write(repo, "files/wiki/index.md", "# start\n\n- a new entry\n")
    commit(repo)
    r = check(repo, "check-home-fresh")
    assert r.returncode == 0, r.stderr


def test_root_settings_are_not_a_readme_trigger(repo):
    write(repo, ".claude/settings.json", "{}\n")
    commit(repo)
    assert check(repo, "check-readme-fresh").returncode == 0


def test_an_agents_md_change_needs_the_brain_readme(repo):
    write(repo, "files/AGENTS.md", "# changed\n")
    commit(repo)
    r = check(repo, "check-readme-fresh")
    assert r.returncode == 1 and "AGENTS.md" in r.stderr
    write(repo, "files/README.md", "# also changed\n")
    commit(repo)
    assert check(repo, "check-readme-fresh").returncode == 0
