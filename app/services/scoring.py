from __future__ import annotations
from typing import List, Tuple
from math import sqrt
from ..models import CarListing, TrianglePoint, NormalizationInfo


def _safe(vals: List[float]) -> Tuple[float, float]:
    finite = [v for v in vals if v is not None]
    if not finite:
        return 0.0, 1.0
    lo = min(finite)
    hi = max(finite)
    if lo == hi:
        hi = lo + 1.0
    return float(lo), float(hi)


def compute_normalization(listings: List[CarListing]) -> NormalizationInfo:
    prices = [l.price for l in listings if l.price is not None]
    horses = [l.horsepower for l in listings if l.horsepower is not None]
    pmin, pmax = _safe(prices)
    hmin, hmax = _safe(horses)
    return NormalizationInfo(price_min=pmin, price_max=pmax, horsepower_min=int(hmin), horsepower_max=int(hmax))


def _norm(value: float | None, lo: float, hi: float) -> float:
    if value is None:
        return 0.0
    if hi == lo:
        return 0.0
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def listing_to_barycentric(listing: CarListing, norm: NormalizationInfo) -> TrianglePoint:
    # cost component increases with price ("more costly closer to cost side")
    cost = _norm(listing.price, norm.price_min or 0.0, (norm.price_max or 1.0))

    # performance increases with horsepower
    performance = _norm(listing.horsepower, float(norm.horsepower_min or 0), float(norm.horsepower_max or 1))

    # reliability provided as 0-1 already (fallback 0.5)
    reliability = listing.reliability_score if listing.reliability_score is not None else 0.5

    # Normalize to sum to 1 (barycentric)
    total = cost + performance + reliability
    if total <= 0:
        return TrianglePoint(cost=1/3, performance=1/3, reliability=1/3)
    return TrianglePoint(cost=cost / total, performance=performance / total, reliability=reliability / total)


def score_against_preference(placement: TrianglePoint, desired: TrianglePoint) -> float:
    # Use Euclidean distance in 3D simplex then invert
    dx = placement.cost - desired.cost
    dy = placement.performance - desired.performance
    dz = placement.reliability - desired.reliability
    dist = sqrt(dx*dx + dy*dy + dz*dz)
    # Max distance in 3-simplex corners is sqrt( (1-0)^2 * 2 ) ~= 1.41; normalize roughly
    score = max(0.0, 1.0 - (dist / 1.5))
    return score
