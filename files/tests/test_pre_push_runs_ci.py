"""tools/git-hooks/pre-push holds every push behind tools/ci-local.sh."""

import shutil
import subprocess
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "tools" / "git-hooks" / "pre-push"
ZERO = "0" * 40
SHA = "a" * 40


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", "-b", "work"], cwd=tmp_path, check=True)
    (tmp_path / "files" / "tools" / "git-hooks").mkdir(parents=True)
    shutil.copy(HOOK, tmp_path / "files" / "tools" / "git-hooks" / "pre-push")
    return tmp_path


def stub_ci(repo, exit_code):
    (repo / "files" / "tools" / "ci-local.sh").write_text(f"echo stub-ci-ran\nexit {exit_code}\n")


def push(repo, ref_line):
    return subprocess.run(
        ["bash", "files/tools/git-hooks/pre-push", "origin", "url"],
        cwd=repo, input=ref_line + "\n", capture_output=True, text=True,
    )


def test_a_push_runs_ci_and_passes_when_it_passes(repo):
    stub_ci(repo, 0)
    r = push(repo, f"refs/heads/work {SHA} refs/heads/work {ZERO}")
    assert r.returncode == 0 and "stub-ci-ran" in r.stderr


def test_a_push_is_refused_when_ci_fails(repo):
    stub_ci(repo, 1)
    r = push(repo, f"refs/heads/work {SHA} refs/heads/work {ZERO}")
    assert r.returncode == 1 and "files/tools/ci-local.sh failed" in r.stderr


def test_deleting_a_branch_skips_ci(repo):
    stub_ci(repo, 1)
    r = push(repo, f"(delete) {ZERO} refs/heads/old {SHA}")
    assert r.returncode == 0 and "stub-ci-ran" not in r.stderr


def test_main_is_refused_before_ci_runs(repo):
    stub_ci(repo, 0)
    r = push(repo, f"refs/heads/main {SHA} refs/heads/main {ZERO}")
    assert r.returncode == 1 and "stub-ci-ran" not in r.stderr


@pytest.mark.parametrize("line", ["LOCAL_FIRST=true", 'LOCAL_FIRST="true"', "LOCAL_FIRST='true'"])
def test_local_first_refuses_a_push_quoted_or_not(repo, line):
    stub_ci(repo, 0)
    (repo / ".env").write_text(line + "\n")
    r = push(repo, f"refs/heads/work {SHA} refs/heads/work {ZERO}")
    assert r.returncode == 1 and "LOCAL_FIRST=true" in r.stderr and "stub-ci-ran" not in r.stderr


def test_local_first_false_lets_a_push_through_ci(repo):
    stub_ci(repo, 0)
    (repo / ".env").write_text('LOCAL_FIRST="false"\n')
    r = push(repo, f"refs/heads/work {SHA} refs/heads/work {ZERO}")
    assert r.returncode == 0 and "stub-ci-ran" in r.stderr
