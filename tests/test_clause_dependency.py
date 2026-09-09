"""Tests for the PER CLAUSE inventory (schemas/clause_dependency.schema.json
+ protocols/clause_dependency_inventory.json).

The inventory says what each protocol clause depends on. These tests
guard the mechanical contract: bucket-specific fields are present,
still_true=no cannot appear without VESTIGIAL + replaced_by, PHYSICS
clauses carry no expiry fields, every MODEL_PROPERTY clause points at a
declared property with a test, and every source path exists.
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
SCHEMA_PATH = ROOT / "schemas" / "clause_dependency.schema.json"
INVENTORY_PATH = ROOT / "protocols" / "clause_dependency_inventory.json"
BUCKETS = {"MODEL_PROPERTY", "GUIDELINE_TEXT", "PHYSICS"}


def _inv():
    return json.loads(INVENTORY_PATH.read_text())


class TestSchema:
    def test_bucket_enum(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert set(s["properties"]["depends_on"]["enum"]) == BUCKETS

    def test_still_true_enum(self):
        s = json.loads(SCHEMA_PATH.read_text())
        assert set(s["properties"]["still_true"]["enum"]) == {"yes", "no", "untested"}


class TestInventory:
    def test_every_clause_has_basis_and_bucket(self):
        for c in _inv()["clauses"]:
            assert c["depends_on"] in BUCKETS, c["clause_id"]
            assert c["classification_basis"].strip(), c["clause_id"]

    def test_clause_ids_unique(self):
        ids = [c["clause_id"] for c in _inv()["clauses"]]
        assert len(ids) == len(set(ids))

    def test_model_property_fields(self):
        props = _inv()["model_properties"]
        for c in _inv()["clauses"]:
            if c["depends_on"] != "MODEL_PROPERTY":
                continue
            assert c["property"].strip() and c["test"].strip(), c["clause_id"]
            assert c["still_true"] in {"yes", "no", "untested"}, c["clause_id"]
            assert c["property_id"] in props, c["clause_id"]

    def test_no_requires_vestigial_and_replacement(self):
        for c in _inv()["clauses"]:
            if c.get("still_true") == "no":
                assert c.get("status") == "VESTIGIAL", c["clause_id"]
                assert c.get("replaced_by", "").strip(), c["clause_id"]

    def test_guideline_fields(self):
        for c in _inv()["clauses"]:
            if c["depends_on"] != "GUIDELINE_TEXT":
                continue
            assert c["tracks"].strip(), c["clause_id"]
            assert re.match(r"^(yes|no|superseded_by:.+)$", c["current"]), c["clause_id"]
            if c["current"] == "no":
                assert c.get("repair") in {"legible_to", "constrain", "unknown"}

    def test_physics_has_no_expiry_fields(self):
        for c in _inv()["clauses"]:
            if c["depends_on"] != "PHYSICS":
                continue
            assert c["review"] == "none", c["clause_id"]
            assert c["axiom"].strip(), c["clause_id"]
            for forbidden in ("still_true", "test", "current", "status"):
                assert forbidden not in c, (c["clause_id"], forbidden)

    def test_all_seven_axioms_present(self):
        ids = {c["clause_id"] for c in _inv()["clauses"] if c["depends_on"] == "PHYSICS"}
        assert ids == {f"A{i}" for i in range(1, 8)}

    def test_declared_properties_each_have_test_and_status(self):
        for pid, p in _inv()["model_properties"].items():
            assert p["property"].strip() and p["test"].strip(), pid
            assert p["still_true"] in {"yes", "no", "untested"}, pid

    def test_every_declared_property_is_used(self):
        used = {c.get("property_id") for c in _inv()["clauses"]}
        assert set(_inv()["model_properties"]) <= used

    def test_first_pass_marks_nothing_vestigial(self):
        """Holds for the first pass only; a later pass that runs a test may
        legitimately flip this — update the test with the CHANGELOG entry."""
        assert not any(c.get("status") == "VESTIGIAL" for c in _inv()["clauses"])

    def test_source_paths_exist(self):
        for c in _inv()["clauses"]:
            path = re.split(r"[: (]", c["source"], maxsplit=1)[0]
            assert (ROOT / path).exists(), (c["clause_id"], path)

    def test_threshold_values_agree_across_tracked_files(self):
        """SW-1 / SP-5 claim the thresholds agree; check it."""
        cfg = json.loads((ROOT / "swarm_config.json").read_text())
        sym = json.loads((ROOT / "symbols" / "symbolic_protocol_v1.0.json").read_text())
        assert cfg["clarity_threshold"] == sym["thresholds"]["clarity_minimum"] == 0.9
        assert cfg["trust_threshold"] == sym["thresholds"]["trust_floor"] == 0.85

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_validates_against_schema(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        for c in _inv()["clauses"]:
            jsonschema.validate(instance=c, schema=schema)

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_schema_rejects_no_without_vestigial(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        bad = {"clause_id": "x", "source": "README.md", "text": "t",
               "depends_on": "MODEL_PROPERTY", "classification_basis": "b",
               "property": "p", "still_true": "no", "test": "t"}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=bad, schema=schema)

    @pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
    def test_schema_rejects_physics_with_still_true(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        bad = {"clause_id": "x", "source": "README.md", "text": "t",
               "depends_on": "PHYSICS", "classification_basis": "b",
               "axiom": "A1", "review": "none", "still_true": "yes"}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=bad, schema=schema)
