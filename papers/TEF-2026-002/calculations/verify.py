#!/usr/bin/env python3
"""Recompute the numerical correspondence reported in TEF-2026-002 v4.7."""

from __future__ import annotations

import json
import math
from pathlib import Path


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")
CODATA_ALPHA_INVERSE = 137.035999177


def close(actual: float, expected: float, tolerance: float = 5e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise SystemExit(f"expected {expected:.16g}, got {actual:.16g}")


def main() -> int:
    q_squared = (-1.0 + math.sqrt(1.0 + 16.0 / math.pi**2)) / 2.0
    q = math.sqrt(q_squared)
    delta_h = math.sqrt(1.0 + q_squared) - 1.0
    alpha_tef = delta_h / (2.0 * math.pi**2)
    alpha_experiment = 1.0 / CODATA_ALPHA_INVERSE
    results = {
        "q": q,
        "delta_h": delta_h,
        "alpha_tef": alpha_tef,
        "alpha_tef_inverse": 1.0 / alpha_tef,
        "relative_difference_percent": (alpha_tef - alpha_experiment) / alpha_experiment * 100.0,
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    for key, value in results.items():
        close(value, expected[key])

    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
