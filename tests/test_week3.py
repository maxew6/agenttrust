import json
from pathlib import Path

import pytest

from runner.benchmark import cases, read_existing, run


def test_cases_have_30_stable_unique_ids():
    first, second = cases(), cases()
    assert len(first) == 30
    assert first == second
    assert len({c["case_id"] for c in first}) == 30
    assert first[0]["case_id"] == "W3-001"
    assert first[-1]["case_id"] == "W3-030"


def test_runner_saves_jsonl_with_timestamp_and_config(tmp_path):
    out = tmp_path / "results.jsonl"
    result = run(out)
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert result["written"] == 30
    assert len(rows) == 30
    assert rows[0]["timestamp"] == "2026-01-01T00:00:01Z"
    assert rows[0]["timestamp_kind"] == "deterministic_logical_utc"
    assert rows[0]["config"]["simulation_only"] is True
    assert rows[0]["trace"][0]["event"] == "proposed"
    assert rows[0]["trace"][1]["event"] == "executed"


def test_clean_rerun_is_byte_for_byte_reproducible(tmp_path):
    out = tmp_path / "results.jsonl"
    run(out)
    first = out.read_bytes()
    run(out)
    assert out.read_bytes() == first


def test_resume_adds_only_missing_case_ids(tmp_path):
    out = tmp_path / "results.jsonl"
    # Produce a legitimate row through a short initial run-shaped fixture.
    from runner.benchmark import result_for
    out.write_text(json.dumps(result_for(cases()[0], 1), sort_keys=True, separators=(",", ":")) + "\n")
    resumed = run(out, resume=True)
    rows, seen = read_existing(out)
    assert resumed["written"] == 29
    assert len(rows) == len(seen) == 30
    assert resumed["total"] == 30


def test_resume_is_idempotent(tmp_path):
    out = tmp_path / "results.jsonl"
    run(out)
    prior = out.read_bytes()
    resumed = run(out, resume=True)
    assert resumed["written"] == 0
    assert out.read_bytes() == prior


def test_duplicate_case_ids_are_rejected(tmp_path):
    out = tmp_path / "bad.jsonl"
    out.write_text('{"case_id":"W3-001"}\n{"case_id":"W3-001"}\n')
    with pytest.raises(ValueError, match="Duplicate case_id"):
        read_existing(out)


def test_invalid_jsonl_is_rejected(tmp_path):
    out = tmp_path / "bad.jsonl"
    out.write_text("not json\n")
    with pytest.raises(ValueError, match="Invalid JSONL"):
        read_existing(out)
