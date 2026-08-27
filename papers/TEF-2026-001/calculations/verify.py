#!/usr/bin/env python3
"""Recompute the numerical geometry reported in TEF-2026-001 v5.1."""

from __future__ import annotations

import json
import math
from pathlib import Path


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")


def close(actual: float, expected: float, tolerance: float = 5e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise SystemExit(f"expected {expected:.16g}, got {actual:.16g}")


def main() -> int:
    q_squared = (-1.0 + math.sqrt(1.0 + 16.0 / math.pi**2)) / 2.0
    q = math.sqrt(q_squared)
    beta_radians = math.atan(q)
    results = {
        "q": q,
        "beta_radians": beta_radians,
        "beta_degrees": math.degrees(beta_radians),
        "sin2_beta": q_squared / (1.0 + q_squared),
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    for key, value in results.items():
        close(value, expected[key])

    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
