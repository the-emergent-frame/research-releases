#!/usr/bin/env python3
"""Check the explicit algebraic bookkeeping in TEF-2026-004 v4.6."""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")


def compare(actual: Any, expected: Any, path: str = "result") -> None:
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise SystemExit(f"{path}: keys differ")
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, (int, float)):
        if not math.isclose(actual, expected, rel_tol=5e-12, abs_tol=5e-12):
            raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")


def complex_parts(value: complex) -> dict[str, float]:
    return {"real": value.real, "imag": value.imag}


def main() -> int:
    zeta = cmath.exp(-2j * math.pi / 3)
    d_lift = -1 / 3
    u_lift = d_lift + 1
    d_phase = cmath.exp(2j * math.pi * d_lift)
    u_phase = cmath.exp(2j * math.pi * u_lift)

    results = {
        "zeta": complex_parts(zeta),
        "zeta_cubed": complex_parts(zeta**3),
        "same_endpoint_phase_distance": abs(d_phase - u_phase),
        "relative_class_difference": 1 - 0,
        "normalized_lifts": {"D": d_lift, "U": u_lift},
        "charge_difference": u_lift - d_lift,
        "three_sector_boundary_distance_from_identity": abs(zeta**3 - 1),
        "quark_antiquark_boundary_distance_from_identity": abs(zeta / zeta - 1),
        "baryon_triality": 3 % 3,
        "meson_triality": (1 - 1) % 3,
        "baryon_charges": {
            "DDD": 0 - 1,
            "UDD": 1 - 1,
            "UUD": 2 - 1,
            "UUU": 3 - 1,
        },
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
