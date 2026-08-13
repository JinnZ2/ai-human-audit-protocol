"""Unit tests for physics/reference_frame_bridge.py.

Wires reference_frame.assess() as the sensor feeding three downstream modules:
monoculture_collapse_predictor, legacy_trap_detector, substrate_scope_validator.

Tests verify: carrier_state() formula correctness for all four downstream
parameters (reciprocity, maintain_frac, broadcast, envelope_width), clamping
at floors and ceilings, negative narrative_gap clamping, paired-mode
assessment dispatch, dispatch() output shape and key consistency, envelope
symmetry, custom diversity pass-through, and demo scenario quantitative values.

Note: reference_frame_bridge imports `from reference_frame import assess` as a
bare sibling import. conftest.py adds physics/ to sys.path.
"""

import pytest

from physics.reference_frame_bridge import carrier_state, dispatch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _a(located=0.5, narrative_gap=0.2, disposability_ratio=0.5):
    """Minimal assessment dict — only the fields carrier_state reads."""
    return {"frame": {}, "located": located,
            "narrative_gap": narrative_gap,
            "disposability_ratio": disposability_ratio}


def _paired(located=0.5, narrative_gap=0.2, disposability_ratio=0.5):
    """Paired-mode assessment (no top-level 'frame' key)."""
    inner = _a(located, narrative_gap, disposability_ratio)
    return {"self": inner, "external": inner, "self_minus_external": {}}


# ---------------------------------------------------------------------------
# carrier_state() — output shape
# ---------------------------------------------------------------------------

class TestCarrierStateShape:
    def test_returns_dict(self):
        assert isinstance(carrier_state(_a()), dict)

    def test_required_keys(self):
        out = carrier_state(_a())
        for k in ("reciprocity", "maintain_frac", "broadcast",
                  "envelope_width", "disposability_ratio", "located", "narrative_gap"):
            assert k in out

    def test_located_stored(self):
        assert carrier_state(_a(located=0.7))["located"] == pytest.approx(0.7)

    def test_positive_gap_stored(self):
        assert carrier_state(_a(narrative_gap=0.4))["narrative_gap"] == pytest.approx(0.4)

    def test_negative_gap_clamped_to_zero(self):
        # negative narrative_gap = observed > stated; only told-more-than-shown locks
        out = carrier_state(_a(narrative_gap=-0.3))
        assert out["narrative_gap"] == pytest.approx(0.0)

    def test_disposability_ratio_stored(self):
        assert carrier_state(_a(disposability_ratio=0.03))["disposability_ratio"] == pytest.approx(0.03)

    def test_reads_paired_assessment_through_self_key(self):
        out = carrier_state(_paired(located=0.6))
        assert out["located"] == pytest.approx(0.6)

    def test_all_values_rounded_to_4dp(self):
        out = carrier_state(_a(located=1/3, narrative_gap=1/7))
        for k in ("reciprocity", "maintain_frac", "broadcast", "envelope_width"):
            assert out[k] == round(out[k], 4)


# ---------------------------------------------------------------------------
# carrier_state() — reciprocity formula
# ---------------------------------------------------------------------------

class TestReciprocity:
    def test_formula(self):
        # max(0, 0.6 * (1 - 0.2)) = 0.6 * 0.8 = 0.48
        assert carrier_state(_a(located=0.6, narrative_gap=0.2))["reciprocity"] == pytest.approx(0.48, abs=1e-4)

    def test_zero_located_gives_zero(self):
        assert carrier_state(_a(located=0.0, narrative_gap=0.0))["reciprocity"] == pytest.approx(0.0)

    def test_zero_gap_gives_located(self):
        # max(0, 0.7*(1-0)) = 0.7
        assert carrier_state(_a(located=0.7, narrative_gap=0.0))["reciprocity"] == pytest.approx(0.7)

    def test_gap_one_gives_zero(self):
        # max(0, 0.8*(1-1.0)) = 0.0
        assert carrier_state(_a(located=0.8, narrative_gap=1.0))["reciprocity"] == pytest.approx(0.0)

    def test_fully_located_zero_gap_gives_one(self):
        assert carrier_state(_a(located=1.0, narrative_gap=0.0))["reciprocity"] == pytest.approx(1.0)

    def test_negative_gap_uses_zero_not_negative(self):
        # gap clamped to 0, so reciprocity = located * 1.0
        out = carrier_state(_a(located=0.5, narrative_gap=-0.5))
        assert out["reciprocity"] == pytest.approx(0.5)

    def test_nonnegative(self):
        for gap in (0.0, 0.5, 1.0, 1.5):
            val = carrier_state(_a(located=0.3, narrative_gap=gap))["reciprocity"]
            assert val >= 0.0


# ---------------------------------------------------------------------------
# carrier_state() — maintain_frac formula
# ---------------------------------------------------------------------------

class TestMaintainFrac:
    def test_formula(self):
        # min(1.0, (1-0.3)*0.5 + 0.4*0.5) = min(1.0, 0.35+0.2) = 0.55
        assert carrier_state(_a(located=0.3, narrative_gap=0.4))["maintain_frac"] == pytest.approx(0.55, abs=1e-4)

    def test_fully_located_zero_gap_gives_zero(self):
        # min(1.0, 0*0.5 + 0*0.5) = 0.0
        assert carrier_state(_a(located=1.0, narrative_gap=0.0))["maintain_frac"] == pytest.approx(0.0)

    def test_zero_located_unit_gap_gives_one(self):
        # min(1.0, 1*0.5 + 1*0.5) = min(1.0, 1.0) = 1.0
        assert carrier_state(_a(located=0.0, narrative_gap=1.0))["maintain_frac"] == pytest.approx(1.0)

    def test_clamped_to_one(self):
        # located=0, gap=1 → 0.5+0.5=1.0 → min clips to 1.0
        val = carrier_state(_a(located=0.0, narrative_gap=1.0))["maintain_frac"]
        assert val <= 1.0

    def test_increases_with_gap(self):
        lo = carrier_state(_a(located=0.5, narrative_gap=0.1))["maintain_frac"]
        hi = carrier_state(_a(located=0.5, narrative_gap=0.8))["maintain_frac"]
        assert hi > lo

    def test_increases_as_location_drops(self):
        lo = carrier_state(_a(located=0.8, narrative_gap=0.3))["maintain_frac"]
        hi = carrier_state(_a(located=0.2, narrative_gap=0.3))["maintain_frac"]
        assert hi > lo


# ---------------------------------------------------------------------------
# carrier_state() — broadcast formula
# ---------------------------------------------------------------------------

class TestBroadcast:
    def test_formula(self):
        # min(2.0, 0.5 + 0.4*1.5) = min(2.0, 1.1) = 1.1
        assert carrier_state(_a(narrative_gap=0.4))["broadcast"] == pytest.approx(1.1, abs=1e-4)

    def test_zero_gap_gives_half(self):
        # min(2.0, 0.5 + 0) = 0.5
        assert carrier_state(_a(narrative_gap=0.0))["broadcast"] == pytest.approx(0.5)

    def test_unit_gap_hits_ceiling(self):
        # min(2.0, 0.5 + 1.0*1.5) = min(2.0, 2.0) = 2.0
        assert carrier_state(_a(narrative_gap=1.0))["broadcast"] == pytest.approx(2.0)

    def test_capped_at_two(self):
        # gap > 1.0 would push beyond 2.0 → capped
        val = carrier_state(_a(narrative_gap=1.5))["broadcast"]
        assert val <= 2.0

    def test_independent_of_located(self):
        # broadcast formula does not use located
        b1 = carrier_state(_a(located=0.1, narrative_gap=0.3))["broadcast"]
        b2 = carrier_state(_a(located=0.9, narrative_gap=0.3))["broadcast"]
        assert b1 == pytest.approx(b2)

    def test_increases_with_gap(self):
        lo = carrier_state(_a(narrative_gap=0.1))["broadcast"]
        hi = carrier_state(_a(narrative_gap=0.7))["broadcast"]
        assert hi > lo


# ---------------------------------------------------------------------------
# carrier_state() — envelope_width formula
# ---------------------------------------------------------------------------

class TestEnvelopeWidth:
    def test_formula(self):
        # max(0.05, 0.6*(1-0.2)) = max(0.05, 0.48) = 0.48
        assert carrier_state(_a(located=0.6, narrative_gap=0.2))["envelope_width"] == pytest.approx(0.48, abs=1e-4)

    def test_floor_at_zero_located(self):
        # max(0.05, 0) = 0.05
        assert carrier_state(_a(located=0.0, narrative_gap=0.0))["envelope_width"] == pytest.approx(0.05)

    def test_floor_when_product_small(self):
        # located=0.04, gap=0 → 0.04*(1-0) = 0.04 < 0.05 → floor
        val = carrier_state(_a(located=0.04, narrative_gap=0.0))["envelope_width"]
        assert val == pytest.approx(0.05)

    def test_floor_when_gap_is_one(self):
        # located*(1-1)=0 → floor
        val = carrier_state(_a(located=0.8, narrative_gap=1.0))["envelope_width"]
        assert val == pytest.approx(0.05)

    def test_never_below_floor(self):
        for located in (0.0, 0.1, 0.5, 1.0):
            for gap in (0.0, 0.5, 1.0):
                val = carrier_state(_a(located=located, narrative_gap=gap))["envelope_width"]
                assert val >= 0.05

    def test_shrinks_with_higher_gap(self):
        lo = carrier_state(_a(located=0.5, narrative_gap=0.1))["envelope_width"]
        hi = carrier_state(_a(located=0.5, narrative_gap=0.9))["envelope_width"]
        assert hi < lo


# ---------------------------------------------------------------------------
# dispatch() — shape and structural contracts
# ---------------------------------------------------------------------------

class TestDispatchShape:
    def _d(self, **kw):
        return dispatch(_a(**kw))

    def test_returns_dict(self):
        assert isinstance(self._d(), dict)

    def test_carrier_state_key_present(self):
        assert "carrier_state" in self._d()

    def test_monoculture_key_present(self):
        assert "monoculture_collapse_predictor.sweep" in self._d()

    def test_legacy_key_present(self):
        assert "legacy_trap_detector.run" in self._d()

    def test_substrate_key_present(self):
        assert "substrate_scope_validator.envelope" in self._d()

    def test_sweep_has_diversity_broadcast_reciprocity(self):
        sweep = self._d()["monoculture_collapse_predictor.sweep"]
        for k in ("diversity", "broadcast", "reciprocity"):
            assert k in sweep

    def test_legacy_has_maintain_frac(self):
        assert "maintain_frac" in self._d()["legacy_trap_detector.run"]

    def test_envelope_has_heat_and_load(self):
        env = self._d()["substrate_scope_validator.envelope"]
        assert "heat" in env and "load" in env

    def test_carrier_state_values_match(self):
        a = _a(located=0.4, narrative_gap=0.3)
        d = dispatch(a)
        cs_direct = carrier_state(a)
        cs_dispatch = d["carrier_state"]
        for k in ("reciprocity", "maintain_frac", "broadcast", "envelope_width"):
            assert cs_dispatch[k] == pytest.approx(cs_direct[k])


# ---------------------------------------------------------------------------
# dispatch() — downstream parameter correctness
# ---------------------------------------------------------------------------

class TestDispatchParams:
    def test_sweep_reciprocity_matches_carrier_state(self):
        a = _a(located=0.5, narrative_gap=0.3)
        d = dispatch(a)
        assert d["monoculture_collapse_predictor.sweep"]["reciprocity"] == \
               d["carrier_state"]["reciprocity"]

    def test_sweep_broadcast_matches_carrier_state(self):
        a = _a(narrative_gap=0.4)
        d = dispatch(a)
        assert d["monoculture_collapse_predictor.sweep"]["broadcast"] == \
               d["carrier_state"]["broadcast"]

    def test_legacy_maintain_frac_matches_carrier_state(self):
        a = _a(located=0.3, narrative_gap=0.6)
        d = dispatch(a)
        assert d["legacy_trap_detector.run"]["maintain_frac"] == \
               d["carrier_state"]["maintain_frac"]

    def test_envelope_symmetric_around_half(self):
        d = dispatch(_a())
        env = d["substrate_scope_validator.envelope"]
        for ax in ("heat", "load"):
            lo, hi = env[ax]
            assert (lo + hi) / 2 == pytest.approx(0.5, abs=1e-6)

    def test_envelope_width_equals_carrier_state_width(self):
        a = _a(located=0.6, narrative_gap=0.2)
        d = dispatch(a)
        cs = d["carrier_state"]
        env = d["substrate_scope_validator.envelope"]
        lo, hi = env["heat"]
        assert hi - lo == pytest.approx(cs["envelope_width"], abs=1e-6)

    def test_heat_and_load_envelopes_equal(self):
        d = dispatch(_a())
        env = d["substrate_scope_validator.envelope"]
        assert env["heat"] == env["load"]

    def test_custom_diversity_passed_to_sweep(self):
        d = dispatch(_a(), diversity=2.5)
        assert d["monoculture_collapse_predictor.sweep"]["diversity"] == pytest.approx(2.5)

    def test_default_diversity_is_one(self):
        d = dispatch(_a())
        assert d["monoculture_collapse_predictor.sweep"]["diversity"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Demo scenario — quantitative predictions
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _cs(self):
        # told_high scenario: located=0.26, narrative_gap=0.55
        return carrier_state(_a(located=0.26, narrative_gap=0.55,
                                disposability_ratio=0.025))

    def test_reciprocity(self):
        # max(0, 0.26*(1-0.55)) = 0.26*0.45 = 0.117
        assert self._cs()["reciprocity"] == pytest.approx(0.117, abs=1e-4)

    def test_maintain_frac(self):
        # min(1.0, (1-0.26)*0.5 + 0.55*0.5) = 0.37+0.275 = 0.645
        assert self._cs()["maintain_frac"] == pytest.approx(0.645, abs=1e-4)

    def test_broadcast(self):
        # min(2.0, 0.5 + 0.55*1.5) = 0.5+0.825 = 1.325
        assert self._cs()["broadcast"] == pytest.approx(1.325, abs=1e-4)

    def test_envelope_width(self):
        # max(0.05, 0.26*0.45) = max(0.05, 0.117) = 0.117
        assert self._cs()["envelope_width"] == pytest.approx(0.117, abs=1e-4)

    def test_envelope_bounds(self):
        d = dispatch(_a(located=0.26, narrative_gap=0.55, disposability_ratio=0.025))
        env = d["substrate_scope_validator.envelope"]
        lo, hi = env["heat"]
        assert lo == pytest.approx(0.5 - 0.117/2, abs=1e-4)
        assert hi == pytest.approx(0.5 + 0.117/2, abs=1e-4)

    def test_low_location_high_gap_means_low_reciprocity(self):
        # the fundamental claim: unlocated + gap → locked carrier
        cs = self._cs()
        assert cs["reciprocity"] < 0.2

    def test_low_location_high_gap_means_high_maintain_frac(self):
        assert self._cs()["maintain_frac"] > 0.5

    def test_high_gap_means_high_broadcast(self):
        assert self._cs()["broadcast"] > 1.0

    def test_narrow_envelope_when_gap_high(self):
        assert self._cs()["envelope_width"] < 0.2
