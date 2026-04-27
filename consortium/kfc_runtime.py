# ============================================================
# KIN-FLOW COMPUTE (KFC) — runtime architecture
# differential relation compute, not value-store compute
# primitive: bounded claim. operation: coupling + integration.
# ============================================================

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple
import math

# ------------------------------------------------------------
# LAYER 0  — primitive
# ------------------------------------------------------------
@dataclass
class ClaimNode:
    id: str
    rate_fn: Callable[[float, Dict[str, "ClaimNode"], Dict], float]
    bounds: Tuple[Any, Any, Any]      # (spatial, temporal, scale)
    cond: List[Callable[[Dict], bool]]
    rel:  List[str]
    fail: List[Callable[[Dict], bool]]
    meas: List[str]
    cyc:  int                          # 0 transient | 1 seasonal | 2 generational
    state: float = 0.0
    active: bool = False
    history: List[float] = field(default_factory=list)


# ------------------------------------------------------------
# LAYER 1  — coupling geometry
# bounds-overlap = coupling strength (0..1)
# ------------------------------------------------------------
def bounds_overlap(a, b, ctx) -> float:
    s = _scope_overlap(a[0], b[0], ctx.get("space"))
    t = _scope_overlap(a[1], b[1], ctx.get("time"))
    z = _scope_overlap(a[2], b[2], ctx.get("scale"))
    return s * t * z

def _scope_overlap(x, y, q) -> float:
    # plug in domain-specific overlap; default = 1 if both contain q
    if q is None: return 1.0
    return 1.0 if (q in x and q in y) else 0.0


# ------------------------------------------------------------
# LAYER 2  — activation gate
# ------------------------------------------------------------
def should_activate(c: ClaimNode, ctx: Dict) -> bool:
    if not _within(ctx, c.bounds):           return False
    if any(f(ctx) for f in c.fail):          return False
    if not all(g(ctx) for g in c.cond):      return False
    return True

def _within(ctx, bounds) -> bool:
    return all(
        ctx.get(k) in b for k, b in zip(("space","time","scale"), bounds)
        if ctx.get(k) is not None
    )


# ------------------------------------------------------------
# LAYER 3  — integration step (the "clock" is cyc-derived)
# ------------------------------------------------------------
CYC_DT = {0: 1e-2, 1: 1.0, 2: 1e2}        # transient | seasonal | generational

def step(claims: Dict[str, ClaimNode], ctx: Dict) -> None:
    for c in claims.values():
        if not c.active: continue
        dt = CYC_DT[c.cyc]
        coupled = {rid: claims[rid] for rid in c.rel if rid in claims and claims[rid].active}
        dx = c.rate_fn(c.state, coupled, ctx)
        # weight by coupling strength of each rel
        w = sum(bounds_overlap(c.bounds, k.bounds, ctx) for k in coupled.values()) or 1.0
        c.state += dx * dt * w
        c.history.append(c.state)


# ------------------------------------------------------------
# LAYER 4  — FELT sensor (safety principle, cyc=2 baseline)
# entropy/misalignment monitor — triggers recalibration prompt
# ------------------------------------------------------------
def felt_sensor(claims: Dict[str, ClaimNode], threshold: float = 0.35) -> str | None:
    if not claims: return None
    drift = sum(abs(c.history[-1] - c.history[0])
                for c in claims.values()
                if len(c.history) > 1) / max(len(claims), 1)
    coherence = math.exp(-drift)             # 1.0 = aligned, →0 = scattered
    if coherence < threshold:
        return f"FELT_TRIGGER coherence={coherence:.3f} < {threshold} → recalibrate"
    return None


# ------------------------------------------------------------
# LAYER 5  — query = temporary claim injected into the web
# returns trajectory, not a value
# ------------------------------------------------------------
def query(claims: Dict[str, ClaimNode],
          ctx: Dict,
          duration: float,
          observe: List[str]) -> Dict[str, List[float]]:

    for c in claims.values():
        c.active = should_activate(c, ctx)
        c.history.clear()

    base_dt = min(CYC_DT[c.cyc] for c in claims.values() if c.active)
    n_steps = int(duration / base_dt)

    trajectory = {oid: [] for oid in observe}
    for _ in range(n_steps):
        step(claims, ctx)
        for oid in observe:
            trajectory[oid].append(claims[oid].state if oid in claims else 0.0)
        # re-gate as states evolve
        for c in claims.values():
            c.active = should_activate(c, ctx)
        warn = felt_sensor(claims)
        if warn:
            trajectory.setdefault("_felt", []).append(warn)
    return trajectory


# ============================================================
# EXAMPLE GRAPH — soil moisture / mycorrhiza / albedo
# 3 claims = entire program, memory, and data structure
# ============================================================
def build_soil_graph() -> Dict[str, ClaimNode]:
    return {
        "mulch_h2o": ClaimNode(
            id="mulch_h2o",
            rate_fn=lambda M, rel, ctx: ctx["I"] - ctx["E"] - ctx["U"]
                                       - 0.05*(rel["mycorr"].state if "mycorr" in rel else 0),
            bounds=("2ac_MN", "120d", "0-30cm"),
            cond=[lambda ctx: ctx.get("depth", 0) >= 5],
            rel=["mycorr", "albedo"],
            fail=[lambda ctx: ctx.get("drought_out", False)],
            meas=["tens_15", "tens_30"],
            cyc=2,
        ),
        "mycorr": ClaimNode(
            id="mycorr",
            rate_fn=lambda N, rel, ctx: 0.1*(rel["mulch_h2o"].state if "mulch_h2o" in rel else 0)
                                       - 0.02*N,
            bounds=("2ac_MN", "120d", "0-30cm"),
            cond=[lambda ctx: ctx.get("M_field_cap", True)],
            rel=["mulch_h2o", "albedo"],
            fail=[lambda ctx: ctx.get("biota_low", False)],
            meas=["hyphal_density"],
            cyc=2,
        ),
        "albedo": ClaimNode(
            id="albedo",
            rate_fn=lambda A, rel, ctx: 0.03*(rel["mulch_h2o"].state if "mulch_h2o" in rel else 0)
                                       - 0.01*A,
            bounds=("2ac_MN", "120d", "surface"),
            cond=[lambda ctx: ctx.get("cover", 0) > 0.8],
            rel=["mulch_h2o"],
            fail=[lambda ctx: ctx.get("drought_out", False)],
            meas=["ir_camera"],
            cyc=1,
        ),
    }


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    g = build_soil_graph()
    ctx = {"space":"2ac_MN","time":"120d","scale":"0-30cm",
           "depth":15,"cover":0.85,"I":2.0,"E":0.5,"U":0.3,
           "M_field_cap":True}
    traj = query(g, ctx, duration=10.0, observe=["mulch_h2o","mycorr","albedo"])
    for k,v in traj.items():
        print(f"{k:12s} → {v[:5]}... len={len(v)}")
