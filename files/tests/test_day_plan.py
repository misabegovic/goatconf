"""The core days' times live once, in the program's day plan, and every page that gives them follows it."""
import copy
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def test_a_changed_day_reaches_every_place(monkeypatch):
    program = importlib.reload(importlib.import_module("program"))
    plan = copy.deepcopy(program.DAY_PLAN)
    thursday = next(iter(program.CORE_DAYS))
    plan[thursday].update(welcome="08:45", end="18:30", slots=("09:00", "11:00", "13:00", "15:00"))
    monkeypatch.setattr(program, "DAY_PLAN", plan)
    assert program.day_hours(thursday) == "09:00 to 18:30"
    assert "talks, 09:00 to 18:30" in program.register_days() and "Welcome at 08:45." in program.register_days()
    assert "Thursday 3rd June 2027: 09:00, 11:00, 13:00 or 15:00." in program.slot_times()
    assert program.day_note(plan[thursday]).endswith("Welcome at 08:45.")
    assert "Thursday runs from 09:00 to 18:30." in program.page()
