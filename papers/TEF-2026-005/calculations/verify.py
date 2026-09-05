#!/usr/bin/env python3
"""Check the reported numerical relations in TEF-2026-005 v4.1."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")

# Exact defining constants where applicable; G carries its measured uncertainty.
PLANCK_CONSTANT = 6.62607015e-34  # J s
NEWTON_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
SPEED_OF_LIGHT = 299792458.0  # m s^-1
HBAR_C_GEV_FM = 0.1973269804  # GeV fm
FEMTOMETRE = 1e-15  # m


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


def main() -> int:
    q = math.sqrt((-1 + math.sqrt(1 + 16 / math.pi**2)) / 2)
    r_g = math.sqrt(
        PLANCK_CONSTANT * NEWTON_CONSTANT
        / (8 * math.pi * SPEED_OF_LIGHT**3)
    )
    p_1 = 2 * math.pi * q * r_g
    p_2 = 2 * p_1

    sqrt_sigma_gev = 0.445
    sigma_gev2 = sqrt_sigma_gev**2
    sigma_gev_per_fm = sigma_gev2 / HBAR_C_GEV_FM
    delta_e_2_ev = sigma_gev_per_fm * (p_2 / FEMTOMETRE) * 1e9

    # If n only groups identical cells, Delta E_n = n Delta E_1 makes sigma invariant.
    delta_e_1_test = 1.0
    sigma_1_test = delta_e_1_test / p_1
    sigma_2_test = (2 * delta_e_1_test) / p_2

    results = {
        "helix_shape_parameter_q": q,
        "phase_closure_residual": abs(q * math.sqrt(1 + q**2) - 2 / math.pi),
        "gravity_calibrated_radius_m": r_g,
        "one_turn_rollout_m": p_1,
        "two_turn_rollout_m": p_2,
        "two_turn_units_per_fm": FEMTOMETRE / p_2,
        "reference_string_tension": {
            "sqrt_sigma_gev": sqrt_sigma_gev,
            "sigma_gev2": sigma_gev2,
            "sigma_gev_per_fm": sigma_gev_per_fm,
        },
        "diagnostic_two_turn_gap_ev": delta_e_2_ev,
        "partition_invariance_ratio": sigma_2_test / sigma_1_test,
        "force_scheme_linear_coefficient": 1 / (4 / 3),
        "momentum_scheme_linear_coefficient": 2 / (4 / 3),
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
