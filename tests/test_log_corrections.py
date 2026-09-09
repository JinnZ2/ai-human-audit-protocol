"""Tests for the logs/ correction mechanism.

logs/ is append-only. A missing run block on an earlier entry is fixed by
APPENDING a correction entry that supersedes the original by content
hash; the original stays readable and unmodified. These tests guard:
every correction points at a file that exists and whose bytes still
hash to the recorded sha256 (so an edit to an original breaks the
suite), the five added fields are present with `unknown` literal where
unsupported, UNDETERMINED entries are present rather than skipped, and
every log that has a run-block index entry has a correction.
"""

import hashlib
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
FIELDS = ("run_id", "design", "measurand", "recorded_by", "date")


def _corrections():
    out = []
    for f in sorted(LOGS.glob("*-correction-*.json")):
        d = json.loads(f.read_text())
        assert d["type"] == "correction", f.name
        out.append((f, d))
    return out


def _indexed_logs():
    paths = set()
    for f in LOGS.glob("*-human-subject-run-blocks.json"):
        for e in json.loads(f.read_text())["entries"]:
            src = e["source"].split(":")[0]
            if src.startswith("logs/"):
                paths.add(src)
    return paths


class TestCorrections:
    def test_corrections_exist(self):
        assert _corrections()

    def test_naming_convention(self):
        pat = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}Z-correction-.+\.json$")
        for f, _ in _corrections():
            assert pat.match(f.name), f.name

    def test_original_exists_and_is_unmodified(self):
        for f, d in _corrections():
            orig = ROOT / d["supersedes"]["path"]
            assert orig.exists(), d["supersedes"]["path"]
            sha = hashlib.sha256(orig.read_bytes()).hexdigest()
            assert sha == d["supersedes"]["sha256"], (
                f"{orig.name} bytes no longer match the hash recorded in {f.name}; "
                f"originals are append-only — append a new correction, do not edit"
            )

    def test_original_field_is_literal(self):
        for _, d in _corrections():
            assert d["original"] == "retained, unmodified"

    def test_added_fields_complete_and_unknown_is_literal(self):
        for f, d in _corrections():
            for k in FIELDS:
                v = d["added_fields"][k]
                assert isinstance(v, str) and v.strip(), (f.name, k)
            unknown = {k for k in FIELDS if d["added_fields"][k] == "unknown"}
            assert unknown == set(d["missing_fields"]), f.name

    def test_undetermined_entries_are_present_not_skipped(self):
        classes = {d["class"] for _, d in _corrections()}
        assert "UNDETERMINED" in classes

    def test_reason_enum(self):
        for _, d in _corrections():
            assert d["reason"] in {"missing run block", "class correction"}

    def test_every_indexed_log_has_a_correction(self):
        superseded = {d["supersedes"]["path"] for _, d in _corrections()}
        missing = _indexed_logs() - superseded
        assert not missing, missing

    def test_correction_does_not_supersede_itself_or_an_index(self):
        for f, d in _corrections():
            target = json.loads((ROOT / d["supersedes"]["path"]).read_text())
            assert target.get("type") not in {"correction"}, f.name
            assert not str(target.get("type", "")).endswith("_index"), f.name

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_validates_against_audit_log_schema(self):
        schema = json.loads((ROOT / "schemas" / "audit_log.schema.json").read_text())
        for _, d in _corrections():
            jsonschema.validate(instance=d, schema=schema)
