"""The shell's own invariants: what must stay true of this brain whatever its content."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BRAIN = [sys.executable, str(ROOT / "tools" / "brain.py")]
LOG_LINE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2} (?P<keyword>[a-z][a-z+-]*) — (?P<summary>.*)$")


def run(*args):
    env = {k: v for k, v in os.environ.items() if k != "BRAIN_DIR"}
    return subprocess.run([*BRAIN, *args], cwd=ROOT, capture_output=True, text=True, env=env)


def test_validate_passes():
    r = run("validate")
    assert r.returncode == 0, r.stdout + r.stderr


def test_citations_resolve():
    r = run("check", "--no-net")
    assert r.returncode == 0, r.stdout + r.stderr


def test_notion_writes_denied():
    r = run("check-no-notion-writes")
    assert r.returncode == 0, r.stdout + r.stderr


def test_claude_md_is_agents_md():
    claude = ROOT / "CLAUDE.md"
    assert claude.is_symlink() and os.readlink(claude) == "AGENTS.md"


def test_dated_log_lines_follow_the_published_shape():
    dated = [l for l in (ROOT / "log" / "log.md").read_text().splitlines() if re.match(r"^[0-9]{4}-", l)]
    assert dated, "the log has no dated line"
    bad = [l for l in dated if not LOG_LINE.match(l)]
    assert not bad, bad


def test_settings_carry_no_machine_paths():
    text = (ROOT / ".claude" / "settings.json").read_text()
    json.loads(text)
    assert "/home/" not in text, "settings.json must stay portable: use ${CLAUDE_PROJECT_DIR} or a PATH lookup"


def test_every_skill_has_its_protocol():
    skills = [d for d in (ROOT / ".claude" / "skills").iterdir() if d.is_dir()]
    assert skills
    missing = [d.name for d in skills if not (d / "SKILL.md").exists()]
    assert not missing, missing


def test_scope_tiers_are_lists():
    cfg = yaml.safe_load((ROOT / "tabula.config.yml").read_text()) or {}
    for tier in ("active", "reference", "frozen", "archived"):
        assert isinstance(cfg.get(f"{tier}_repos", []), list), tier
