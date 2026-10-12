"""Files for agents: they parse, agree with the program, and hold no stray facts."""

import importlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
agents = importlib.import_module("agents")
program = importlib.import_module("program")


def test_program_json_has_every_day_and_room():
    data = json.loads(agents.program_json())
    assert [d["date"] for d in data["days"]] == ["2027-06-03", "2027-06-04", "2027-06-05"]
    assert len(data["rooms"]) == len(program.ROOMS)
    assert data["days"][1]["welcome"] == program.DAY_PLAN[sorted(program.DAY_PLAN)[1]]["welcome"]


def test_event_data_is_valid_json_and_free():
    block = agents.json_ld()
    data = json.loads(re.search(r'ld\+json">(.*?)</script>', block, re.S).group(1))
    assert data["@type"] == "Event" and data["isAccessibleForFree"] is True
    assert data["offers"]["price"] == 0
    assert data["startDate"].startswith("2027-06-03T")


def test_calendar_lines_are_crlf_and_short():
    text = agents.calendar()
    assert text.startswith("BEGIN:VCALENDAR\r\n") and text.endswith("END:VCALENDAR\r\n")
    assert text.count("BEGIN:VEVENT") == 3
    for line in text.split("\r\n"):
        assert len(line.encode("utf-8")) <= 75


def test_long_lines_fold_without_breaking_letters():
    folded = agents.fold("DESCRIPTION:" + "Džuma " * 40)
    for part in folded.split("\r\n"):
        part.encode("utf-8")
        assert len(part.encode("utf-8")) <= 75
    assert folded.replace("\r\n ", "") == "DESCRIPTION:" + "Džuma " * 40


def test_sitemap_and_llms_list_every_public_page():
    names = [p.name for p in agents.pages()]
    assert names[0] == "index.html" and not any(n.startswith("_") for n in names)
    assert agents.sitemap().count("<url>") == len(names)
    assert "https://goatconf.com/program.json" in agents.llms()
    assert "Sitemap: https://goatconf.com/sitemap.xml" in agents.robots()


def test_public_addresses_have_no_html_extension():
    assert agents.url("index.html") == "https://goatconf.com/"
    assert agents.url("talk.html") == "https://goatconf.com/talk"
    assert agents.url("program.json") == "https://goatconf.com/program.json"
    assert ".html" not in agents.sitemap()
