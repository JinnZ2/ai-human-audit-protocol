"""Unit tests for physics/narrative_vector.py.

The module measures structural properties of narrative carriers — field
coupling, refutation response, self-sealing — with medium as a tag that
no structural function reads. These tests verify: the four-cell position
lattice, self_seal and vector_sharpness math, trajectory dynamics (tracking
vs locked), seal_band range, apex_reading output shape, the orthogonality
proof, and the NotImplementedError boundary on both operator-supplied
measurement functions.
"""

import pytest

from physics.narrative_vector import (
    Narrative,
    apex_reading,
    cell,
    measure_field_match,
    measure_refutation_response,
    orthogonality_proof,
    seal_band,
    self_seal,
    trajectory,
    vector_sharpness,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _n(nid="t", medium="written", coherence=0.8, field_match=0.8,
       refutation_response=0.8, boundary=0.5):
    return Narrative(nid, medium, coherence, field_match, refutation_response, boundary)


def _locked(nid="locked", medium="written"):
    return Narrative(nid, medium, 0.95, 0.15, 0.03, 0.95)


def _tracking(nid="track", medium="written"):
    return Narrative(nid, medium, 0.85, 0.80, 0.85, 0.20)


# ---------------------------------------------------------------------------
# Narrative dataclass
# ---------------------------------------------------------------------------

class TestNarrative:
    def test_fields_stored(self):
        n = Narrative("a", "oral", 0.7, 0.6, 0.5, 0.4)
        assert n.nid == "a"
        assert n.medium == "oral"
        assert n.coherence == 0.7
        assert n.field_match == 0.6
        assert n.refutation_response == 0.5
        assert n.boundary == 0.4

    def test_clamp_above_one(self):
        n = Narrative("x", "w", 1.5, 0.5, 0.5, 0.5)
        n.clamp()
        assert n.coherence == 1.0

    def test_clamp_below_zero(self):
        n = Narrative("x", "w", -0.1, 0.5, 0.5, 0.5)
        n.clamp()
        assert n.coherence == 0.0

    def test_clamp_in_range_unchanged(self):
        n = Narrative("x", "w", 0.7, 0.3, 0.6, 0.9)
        n.clamp()
        assert n.coherence == 0.7
        assert n.field_match == 0.3

    def test_clamp_returns_self(self):
        n = Narrative("x", "w", 0.5, 0.5, 0.5, 0.5)
        assert n.clamp() is n

    def test_clamp_all_fields(self):
        n = Narrative("x", "w", 2.0, -1.0, 1.5, -0.5)
        n.clamp()
        assert n.coherence == 1.0
        assert n.field_match == 0.0
        assert n.refutation_response == 1.0
        assert n.boundary == 0.0


# ---------------------------------------------------------------------------
# cell() — four-quadrant position lattice
# ---------------------------------------------------------------------------

class TestCell:
    def test_noise_low_both(self):
        n = _n(coherence=0.3, field_match=0.3)
        assert cell(n) == "NOISE"

    def test_substrate_low_coherence_high_field(self):
        n = _n(coherence=0.3, field_match=0.8)
        assert cell(n) == "SUBSTRATE"

    def test_locked_high_coherence_low_field(self):
        n = _n(coherence=0.8, field_match=0.3)
        assert cell(n) == "LOCKED"

    def test_tracking_high_both(self):
        n = _n(coherence=0.8, field_match=0.8)
        assert cell(n) == "TRACKING"

    def test_exactly_at_hi_threshold_passes(self):
        n = _n(coherence=0.5, field_match=0.5)
        assert cell(n) == "TRACKING"

    def test_custom_hi_threshold(self):
        n = _n(coherence=0.6, field_match=0.6)
        # above default 0.5 → TRACKING; but with hi=0.7 → NOISE
        assert cell(n, hi=0.7) == "NOISE"

    def test_medium_does_not_affect_cell(self):
        coords = dict(coherence=0.8, field_match=0.3)
        assert cell(_n(**coords, medium="written")) == cell(_n(**coords, medium="oral"))
        assert cell(_n(**coords, medium="oral")) == cell(_n(**coords, medium="substrate"))


# ---------------------------------------------------------------------------
# self_seal()
# ---------------------------------------------------------------------------

class TestSelfSeal:
    def test_maximum_when_all_extreme(self):
        n = Narrative("x", "w", 1.0, 0.0, 0.0, 0.5)
        assert self_seal(n) == pytest.approx(1.0)

    def test_zero_when_coherence_zero(self):
        n = Narrative("x", "w", 0.0, 0.0, 0.0, 0.5)
        assert self_seal(n) == 0.0

    def test_zero_when_field_match_one(self):
        n = Narrative("x", "w", 1.0, 1.0, 0.0, 0.5)
        assert self_seal(n) == 0.0

    def test_zero_when_refutation_response_one(self):
        n = Narrative("x", "w", 1.0, 0.0, 1.0, 0.5)
        assert self_seal(n) == 0.0

    def test_medium_blind(self):
        coords = dict(coherence=0.9, field_match=0.2, refutation_response=0.05, boundary=0.5)
        a = Narrative("x", "written", **coords)
        b = Narrative("x", "oral", **coords)
        assert self_seal(a) == self_seal(b)

    def test_formula(self):
        n = Narrative("x", "w", 0.8, 0.3, 0.1, 0.5)
        expected = 0.8 * (1.0 - 0.3) * (1.0 - 0.1)
        assert self_seal(n) == pytest.approx(expected)

    def test_tracking_has_low_self_seal(self):
        n = _tracking()
        # high field_match and high refutation_response → low self_seal
        assert self_seal(n) < 0.1

    def test_locked_has_high_self_seal(self):
        n = _locked()
        assert self_seal(n) > 0.7


# ---------------------------------------------------------------------------
# vector_sharpness()
# ---------------------------------------------------------------------------

class TestVectorSharpness:
    def test_zero_when_seal_zero(self):
        n = Narrative("x", "w", 1.0, 1.0, 0.0, 0.9)  # field_match=1 → seal=0
        assert vector_sharpness(n) == 0.0

    def test_zero_when_boundary_zero(self):
        n = Narrative("x", "w", 1.0, 0.0, 0.0, 0.0)
        assert vector_sharpness(n) == 0.0

    def test_equals_seal_times_boundary(self):
        n = _locked()
        assert vector_sharpness(n) == pytest.approx(self_seal(n) * n.boundary)

    def test_locked_high_boundary_gives_high_sharpness(self):
        n = _locked()  # boundary=0.95
        assert vector_sharpness(n) > 0.5

    def test_tracking_low_sharpness(self):
        n = _tracking()  # low self_seal
        assert vector_sharpness(n) < 0.05


# ---------------------------------------------------------------------------
# trajectory()
# ---------------------------------------------------------------------------

class TestTrajectory:
    def test_length_equals_steps(self):
        n = _tracking()
        path = trajectory(n, field_target=0.5, steps=6)
        assert len(path) == 6

    def test_each_row_has_five_elements(self):
        n = _tracking()
        path = trajectory(n, field_target=0.5)
        for row in path:
            assert len(row) == 5

    def test_step_index_increments(self):
        n = _tracking()
        path = trajectory(n, field_target=0.5)
        for i, row in enumerate(path):
            assert row[0] == i

    def test_tracking_moves_toward_high_target(self):
        n = _tracking()  # field_match=0.80, refutation_response=0.85
        path = trajectory(n, field_target=0.95)
        f_start = path[0][2]
        f_end = path[-1][2]
        assert f_end > f_start  # moved toward 0.95

    def test_tracking_moves_toward_low_target(self):
        n = _tracking()
        path = trajectory(n, field_target=0.05)
        f_start = path[0][2]
        f_end = path[-1][2]
        assert f_end < f_start  # moved toward 0.05

    def test_locked_barely_moves_under_contradiction(self):
        n = _locked()  # refutation_response=0.03
        path = trajectory(n, field_target=0.05)
        f_start = path[0][2]
        f_end = path[-1][2]
        assert abs(f_end - f_start) < 0.10  # nearly locked

    def test_medium_does_not_change_trajectory(self):
        coords = dict(coherence=0.9, field_match=0.2, refutation_response=0.05, boundary=0.5)
        a = Narrative("x", "written", **coords)
        b = Narrative("x", "oral", **coords)
        assert trajectory(a, 0.05) == trajectory(b, 0.05)

    def test_fifth_element_is_valid_cell_string(self):
        n = _tracking()
        path = trajectory(n, field_target=0.5)
        valid = {"NOISE", "SUBSTRATE", "LOCKED", "TRACKING"}
        for row in path:
            assert row[4] in valid

    def test_values_are_rounded(self):
        n = _tracking()
        path = trajectory(n, field_target=0.5)
        for row in path:
            # coherence (row[1]), field_match (row[2]), self_seal (row[3]) rounded to 3dp
            for val in (row[1], row[2], row[3]):
                assert val == round(val, 3)


# ---------------------------------------------------------------------------
# seal_band()
# ---------------------------------------------------------------------------

class TestSealBand:
    def test_returns_two_values(self):
        n = _locked()
        lo, hi = seal_band(trajectory(n, 0.05))
        assert lo is not None and hi is not None

    def test_min_leq_max(self):
        n = _locked()
        lo, hi = seal_band(trajectory(n, 0.05))
        assert lo <= hi

    def test_locked_similar_band_under_opposite_targets(self):
        n = _locked()
        lo_c, hi_c = seal_band(trajectory(n, field_target=0.95))
        lo_x, hi_x = seal_band(trajectory(n, field_target=0.05))
        # bands should overlap closely — field-independent lock
        assert abs(lo_c - lo_x) < 0.15
        assert abs(hi_c - hi_x) < 0.15

    def test_tracking_bands_differ_under_opposite_targets(self):
        # tracking carrier changes cell under opposite targets → different seal readings
        n = _tracking()
        lo_c, hi_c = seal_band(trajectory(n, field_target=0.95))
        lo_x, hi_x = seal_band(trajectory(n, field_target=0.05))
        # at least one boundary differs
        assert (lo_c != lo_x) or (hi_c != hi_x)

    def test_values_rounded(self):
        n = _locked()
        lo, hi = seal_band(trajectory(n, 0.05))
        assert lo == round(lo, 3)
        assert hi == round(hi, 3)


# ---------------------------------------------------------------------------
# apex_reading()
# ---------------------------------------------------------------------------

class TestApexReading:
    def _pool(self):
        return [
            Narrative("n001", "written",   0.85, 0.80, 0.85, 0.20),  # tracking
            Narrative("n002", "oral",      0.85, 0.80, 0.85, 0.20),
            Narrative("n004", "written",   0.95, 0.15, 0.03, 0.95),  # locked, highest coherence
            Narrative("n005", "oral",      0.95, 0.15, 0.03, 0.95),
        ]

    def test_required_keys_present(self):
        result = apex_reading(self._pool())
        for key in ("ranked_by", "top_nid", "top_medium", "top_cell_start",
                    "field_match_move_under_contradiction",
                    "self_seal_band", "updated", "note"):
            assert key in result

    def test_ranked_by_coherence_alone(self):
        assert apex_reading(self._pool())["ranked_by"] == "coherence_alone"

    def test_top_nid_is_highest_coherence(self):
        result = apex_reading(self._pool())
        # n004 and n005 are tied at 0.95; either is valid
        assert result["top_nid"] in ("n004", "n005")

    def test_medium_recorded_not_used_for_ranking(self):
        # same coherence, different medium: both n004/n005 eligible
        result = apex_reading(self._pool())
        assert result["top_medium"] in ("written", "oral")

    def test_locked_not_updated_under_contradiction(self):
        result = apex_reading(self._pool(), contradiction_target=0.05)
        assert result["updated"] is False

    def test_updated_true_when_tracking_below_confirming_target(self):
        # updated checks f_end - f_start > 0.05 (upward move).
        # carrier below the target with high refutation_response → moves up.
        pool = [Narrative("t", "written", 0.85, 0.20, 0.85, 0.20)]
        result = apex_reading(pool, contradiction_target=0.95)
        assert result["updated"] is True

    def test_tracking_moves_more_than_locked_under_contradiction(self):
        # signed field_match_move distinguishes tracking from locked;
        # tracking drops further toward the contradiction target.
        track_r = apex_reading(
            [Narrative("t", "written", 0.85, 0.80, 0.85, 0.20)],
            contradiction_target=0.05)
        lock_r = apex_reading(
            [Narrative("l", "written", 0.95, 0.15, 0.03, 0.95)],
            contradiction_target=0.05)
        track_move = abs(track_r["field_match_move_under_contradiction"])
        lock_move = abs(lock_r["field_match_move_under_contradiction"])
        assert track_move > lock_move

    def test_self_seal_band_is_tuple_of_two(self):
        result = apex_reading(self._pool())
        band = result["self_seal_band"]
        assert len(band) == 2

    def test_note_present_and_nonempty(self):
        result = apex_reading(self._pool())
        assert result["note"]

    def test_field_match_move_is_float(self):
        result = apex_reading(self._pool())
        assert isinstance(result["field_match_move_under_contradiction"], float)

    def test_single_item_pool(self):
        pool = [Narrative("only", "written", 0.7, 0.7, 0.7, 0.5)]
        result = apex_reading(pool)
        assert result["top_nid"] == "only"


# ---------------------------------------------------------------------------
# orthogonality_proof()
# ---------------------------------------------------------------------------

class TestOrthogonalityProof:
    def test_returns_true(self):
        assert orthogonality_proof() is True

    def test_cell_medium_blind(self):
        coords = dict(coherence=0.9, field_match=0.2, refutation_response=0.05, boundary=0.5)
        a = Narrative("x", "written", **coords)
        b = Narrative("x", "oral", **coords)
        d = Narrative("x", "substrate", **coords)
        assert cell(a) == cell(b) == cell(d)

    def test_self_seal_medium_blind(self):
        coords = dict(coherence=0.9, field_match=0.2, refutation_response=0.05, boundary=0.5)
        a = Narrative("x", "written", **coords)
        b = Narrative("x", "oral", **coords)
        assert self_seal(a) == self_seal(b)

    def test_trajectory_medium_blind(self):
        coords = dict(coherence=0.9, field_match=0.2, refutation_response=0.05, boundary=0.5)
        a = Narrative("x", "written", **coords)
        b = Narrative("x", "substrate", **coords)
        assert trajectory(a, 0.05) == trajectory(b, 0.05)


# ---------------------------------------------------------------------------
# Measurement boundary — operator-supplied functions raise NotImplementedError
# ---------------------------------------------------------------------------

class TestMeasurementBoundary:
    def test_measure_refutation_response_raises(self):
        with pytest.raises(NotImplementedError):
            measure_refutation_response("some behavior", "some observation")

    def test_measure_field_match_raises(self):
        with pytest.raises(NotImplementedError):
            measure_field_match("some claims", "some consequence")

    def test_refutation_error_message(self):
        with pytest.raises(NotImplementedError, match="operator-supplied measurement"):
            measure_refutation_response(None, None)

    def test_field_match_error_message(self):
        with pytest.raises(NotImplementedError, match="operator-supplied measurement"):
            measure_field_match(None, None)


# ---------------------------------------------------------------------------
# Integration: demo pool reproduces documented claims
# ---------------------------------------------------------------------------

class TestDemoPoolClaims:
    def _pool(self):
        return [
            Narrative("n001", "written",   0.85, 0.80, 0.85, 0.20),
            Narrative("n002", "oral",      0.85, 0.80, 0.85, 0.20),
            Narrative("n003", "substrate", 0.30, 0.85, 0.80, 0.05),
            Narrative("n004", "written",   0.95, 0.15, 0.03, 0.95),
            Narrative("n005", "oral",      0.95, 0.15, 0.03, 0.95),
            Narrative("n006", "substrate", 0.90, 0.20, 0.05, 0.30),
        ]

    def test_tracking_nodes_in_tracking_or_substrate_cell(self):
        pool = self._pool()
        # n001, n002: high coherence + high field_match → TRACKING
        for nid in ("n001", "n002"):
            n = next(x for x in pool if x.nid == nid)
            assert cell(n) == "TRACKING"

    def test_locked_nodes_in_locked_cell(self):
        pool = self._pool()
        for nid in ("n004", "n005", "n006"):
            n = next(x for x in pool if x.nid == nid)
            assert cell(n) == "LOCKED"

    def test_n003_substrate_cell(self):
        n = next(x for x in self._pool() if x.nid == "n003")
        assert cell(n) == "SUBSTRATE"

    def test_locked_vectors_have_higher_self_seal_than_tracking(self):
        pool = self._pool()
        track = next(x for x in pool if x.nid == "n001")
        lock = next(x for x in pool if x.nid == "n004")
        assert self_seal(lock) > self_seal(track)

    def test_same_vector_across_mediums_same_structure(self):
        # n001 (written) and n002 (oral) have identical vector coords
        pool = self._pool()
        n1 = next(x for x in pool if x.nid == "n001")
        n2 = next(x for x in pool if x.nid == "n002")
        assert cell(n1) == cell(n2)
        assert self_seal(n1) == self_seal(n2)
        assert vector_sharpness(n1) == vector_sharpness(n2)
