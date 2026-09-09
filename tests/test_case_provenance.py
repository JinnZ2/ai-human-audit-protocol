"""Tests for the case-provenance side channel (schemas/case_provenance.schema.json
+ logs/*-case-provenance.json).

The provenance index splits 'observed on model M at date D' from
'predicted to recur' from 'extinct'. These tests guard three things:
the schema is well-formed, every index entry conforms to it, and every
log file in logs/ (other than the indexes themselves) is covered by at
least one index entry — so a new log without provenance fails here.
Coverage is additive: a later index file may cover later logs; no
existing index is edited.
"""

import json
from pathlib import Path

import pytest

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).parent.parent
LOGS = ROOT / "logs"
SCHEMA_PATH = ROOT / "schemas" / "case_provenance.schema.json"
LOG_SCHEMA_PATH = ROOT / "schemas" / "audit_log.schema.json"

REQUIRED = {"observed_on", "observed_date", "retest_condition", "status", "recurrence"}
STATUSES = {"live", "extinct", "untested", "recurring"}


def _index_files():
    return sorted(LOGS.glob("*-case-provenance.json"))


def _all_cases():
    cases = []
    for f in _index_files():
        data = json.loads(f.read_text())
        assert data.get("type") == "case_provenance_index", f.name
        cases.extend(data["cases"])
    return cases


class TestSchemaFile:
    def test_schema_loads(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert s["title"] == "Case Provenance"
        assert set(s["required"]) == REQUIRED

    def test_status_enum(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert set(s["properties"]["status"]["enum"]) == STATUSES

    def test_recurrence_item_contract(self):
        s = json.loads(SCHEMA_PATH.read_text())
        item = s["properties"]["recurrence"]["items"]
        assert set(item["required"]) == {"model", "date", "reproduced"}
        assert item["properties"]["reproduced"]["enum"] == ["yes", "no"]


class TestIndexFiles:
    def test_at_least_one_index_exists(self):
        assert _index_files()

    def test_index_follows_log_naming(self):
        import re
        pat = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}Z-case-provenance\.json$")
        for f in _index_files():
            assert pat.match(f.name), f.name

    def test_every_case_has_required_fields(self):
        for c in _all_cases():
            missing = REQUIRED - set(c)
            assert not missing, (c.get("case_id"), missing)
            assert c["status"] in STATUSES
            assert c["retest_condition"].strip()
            assert isinstance(c["recurrence"], list)

    def test_observed_on_never_empty(self):
        for c in _all_cases():
            assert c["observed_on"].strip(), c.get("case_id")

    def test_case_ids_unique(self):
        ids = [c["case_id"] for c in _all_cases()]
        assert len(ids) == len(set(ids))

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_cases_validate_against_schema(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        for c in _all_cases():
            jsonschema.validate(instance=c, schema=schema)

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_index_validates_against_audit_log_schema(self):
        schema = json.loads(LOG_SCHEMA_PATH.read_text())
        for f in _index_files():
            jsonschema.validate(instance=json.loads(f.read_text()), schema=schema)


class TestCoverage:
    def test_every_log_has_a_provenance_entry(self):
        covered = {c["case_id"] for c in _all_cases()}
        covered |= {c.get("source", "").split(":")[0] for c in _all_cases()}
        for f in sorted(LOGS.glob("*.json")):
            if f.name.endswith("-case-provenance.json"):
                continue
            assert f"logs/{f.name}" in covered, (
                f"{f.name} has no case-provenance entry; append a new "
                f"dated *-case-provenance.json log (do not edit existing ones)"
            )

    def test_readme_trigger_cases_covered(self):
        ids = {c["case_id"] for c in _all_cases()}
        assert any(i.startswith("README.md#case-study") for i in ids)
        assert any(i.startswith("README.md#trigger-case-1") for i in ids)

    def test_no_status_claims_without_recurrence(self):
        """live / extinct / recurring require at least one re-test record."""
        for c in _all_cases():
            if c["status"] in {"live", "extinct", "recurring"}:
                assert c["recurrence"], (
                    f"{c['case_id']} claims {c['status']} with no re-test"
                )
