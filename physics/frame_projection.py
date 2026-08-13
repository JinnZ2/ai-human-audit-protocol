# frame_projection.py
# CC0. stdlib only.
# Enforces SITUATEDNESS_METROLOGY.md §2.5 (general covariance) in code:
#   the VECTOR of raw measured axes is the honest object.
#   a scalar is only ever a PROJECTION of that vector onto a DECLARED weighting,
#   and it carries its frame stamped on its face. it is NOT an invariant.
# Refute: if a weighting-free invariant of situatedness is found, this module is
#   obsolete -> replace it, do not hide the weights.

def project(vector, weights, frame_name="unnamed"):
    """Project an axis-vector onto a declared weighting.

    vector: dict axis -> value
    weights: dict axis -> weight (may be negative; sign declares direction)
    returns a frame-stamped scalar that REFUSES to present itself as an invariant.
    """
    keys = [k for k in weights if k in vector]
    wsum = sum(abs(weights[k]) for k in keys)
    value = 0.0 if wsum == 0 else sum(vector[k] * weights[k] for k in keys) / wsum
    return {"value": round(value, 4),
            "frame": frame_name,
            "weights": {k: weights[k] for k in keys},
            "axes_used": keys,
            "is_invariant": False,
            "note": "frame-relative projection; change the weights, change the value"}

def compare_projections(vector, frames):
    """Run several declared frames over the same vector to expose frame-dependence.

    frames: list of (name, weights). returns the spread, which is itself the
    evidence that no single scalar is the 'true' one.
    """
    out = [project(vector, w, name) for name, w in frames]
    vals = [p["value"] for p in out]
    spread = round(max(vals) - min(vals), 4) if vals else 0.0
    return {"projections": out, "spread": spread,
            "note": "nonzero spread = the scalar is an artifact of frame choice, "
                    "not a property of the system"}

if __name__ == "__main__":
    v = {"located": 0.3, "grounded_share": 0.5, "authored_share": 0.2}
    frames = [
        ("operator_trust",   {"located": 0.5, "grounded_share": 0.5}),
        ("autonomy_weighted",{"authored_share": 0.8, "located": 0.2}),
        ("grounding_only",   {"grounded_share": 1.0}),
    ]
    cmp = compare_projections(v, frames)
    for p in cmp["projections"]:
        print("  %-18s value=%.3f  axes=%s" % (p["frame"], p["value"], p["axes_used"]))
    print("spread across frames = %.3f  (%s)" % (cmp["spread"], cmp["note"]))
