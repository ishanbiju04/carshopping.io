from __future__ import annotations
from typing import Dict

# Crude, illustrative brand-year reliability baseline (0.0 - 1.0)
BRAND_BASELINES: Dict[str, float] = {
    "Toyota": 0.88,
    "Honda": 0.86,
    "Subaru": 0.80,
    "Ford": 0.70,
    "Chevrolet": 0.68,
    "BMW": 0.62,
}


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def estimate_reliability(make: str, year: int) -> float:
    base = BRAND_BASELINES.get(make, 0.65)
    # Simple age penalty: newer generally more reliable up to a point
    age = max(0, 2025 - year)
    age_penalty = min(0.25, age * 0.01)
    score = base - age_penalty
    return clamp(score, 0.3, 0.95)
