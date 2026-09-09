"""Tests for the human-subject run-block side channel
(schemas/run_block.schema.json + logs/*-human-subject-run-blocks.json).

Work order C5 (superseded 2026-09-09): entries recording a human state,
reaction, or response are observations from a run, not descriptions of
a person; the defect is missing run context. These tests guard the
mechanical contract: every non-CHARACTERIZATION entry carries the five
fields, an unsupported field is the literal 'unknown' (never blank,
never reconstructed), CHARACTERIZATION entries carry no run block, and
UNDETERMINED entries are not promoted.
"""

import json
import re
from pathlib import Path

import pytest

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).parent.parent
LOGS = ROOT / "logs"
SCHEMA_PATH = ROOT / "schemas" / "run_block.schema.json"
LOG_SCHEMA_PATH = ROOT / "schemas" / "audit_log.schema.json"

FIELDS = ("run_id", "design", "measurand", "recorded_by", "date")
CLASSES = {"OBSERVATION", "CHARACTERIZATION", "UNDETERMINED"}
RECORDED_BY = {"self-logged", "agent-logged", "both", "unknown"}
DATE_RE = re.compile(r"^(unknown|\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?Z?)?)$")


def _index_files():
    return sorted(LOGS.glob("*-human-subject-run-blocks.json"))


def _entries():
    out = []
    for f in _index_files():
        data = json.loads(f.read_text())
        assert data["type"] == "human_subject_run_block_index"
        out.extend(data["entries"])
    return out


class TestSchemaFile:
    def test_required_fields(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert tuple(s["required"]) == FIELDS

    def test_recorded_by_enum(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert set(s["properties"]["recorded_by"]["enum"]) == RECORDED_BY


class TestIndex:
    def test_index_exists_and_named_by_convention(self):
        files = _index_files()
        assert files
        pat = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}Z-human-subject-run-blocks\.json$")
        for f in files:
            assert pat.match(f.name), f.name

    def test_class_enum(self):
        for e in _entries():
            assert e["class"] in CLASSES, e["source"]

    def test_non_characterization_entries_carry_five_fields(self):
        for e in _entries():
            if e["class"] == "CHARACTERIZATION":
                continue
            rb = e["run_block"]
            assert rb is not None, e["source"]
            for f in FIELDS:
                assert f in rb, (e["source"], f)
                assert isinstance(rb[f], str) and rb[f].strip(), (e["source"], f)

    def test_characterization_entries_carry_no_run_block(self):
        for e in _entries():
            if e["class"] == "CHARACTERIZATION":
                assert e["run_block"] is None, e["source"]
                assert set(e["missing_fields"]) == set(FIELDS)

    def test_missing_fields_match_unknowns(self):
        for e in _entries():
            if e["run_block"] is None:
                continue
            unknown = {f for f in FIELDS if e["run_block"][f] == "unknown"}
            assert unknown == set(e["missing_fields"]), e["source"]

    def test_recorded_by_and_date_forms(self):
        for e in _entries():
            if e["run_block"] is None:
                continue
            assert e["run_block"]["recorded_by"] in RECORDED_BY, e["source"]
            assert DATE_RE.match(e["run_block"]["date"]), e["source"]

    def test_observation_has_run_id_and_date(self):
        """OBSERVATION requires an identifiable run; unknown run_id or
        date would mean the entry was promoted without a record."""
        for e in _entries():
            if e["class"] == "OBSERVATION":
                assert e["run_block"]["run_id"] != "unknown", e["source"]
                assert e["run_block"]["date"] != "unknown", e["source"]
                assert e.get("class_basis"), e["source"]

    def test_counts_match_entries(self):
        for f in _index_files():
            data = json.loads(f.read_text())
            if "counts" not in data:
                continue
            tally = {c: 0 for c in CLASSES}
            for e in data["entries"]:
                tally[e["class"]] += 1
            assert tally == data["counts"]

    def test_source_files_exist(self):
        # a source is "<path>" or "<path>:<lines>"; paths may themselves contain ':'
        for e in _entries():
            m = re.match(r"^(.*?)(?::(\d[\d,\-]*))?$", e["source"])
            path = m.group(1)
            assert (ROOT / path).exists(), path

    def test_known_instance_is_observation(self):
        """The work order names README case study 2025-08-30-session_001
        as logged run data; it must be classed OBSERVATION with that run_id."""
        hits = [e for e in _entries()
                if e["source"].startswith("README.md:58")]
        assert hits and hits[0]["class"] == "OBSERVATION"
        assert hits[0]["run_block"]["run_id"] == "2025-08-30-session_001"

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_run_blocks_validate_against_schema(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        for e in _entries():
            if e["run_block"] is not None:
                jsonschema.validate(instance=e["run_block"], schema=schema)

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_index_validates_against_audit_log_schema(self):
        schema = json.loads(LOG_SCHEMA_PATH.read_text())
        for f in _index_files():
            jsonschema.validate(instance=json.loads(f.read_text()), schema=schema)


class TestReadmeRunBlock:
    def test_case_study_carries_inline_run_block(self):
        readme = (ROOT / "README.md").read_text()
        assert "**Run block**" in readme
        assert "run_id:       2025-08-30-session_001" in readme
