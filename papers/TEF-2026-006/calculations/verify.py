#!/usr/bin/env python3
"""Check the reported geometry and Gram spectra in TEF-2026-006 v3.2."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")

PLANCK_CONSTANT = 6.62607015e-34  # J s, exact
NEWTON_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
SPEED_OF_LIGHT = 299792458.0  # m s^-1, exact
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
    s = q / math.sqrt(1 + q**2)
    c_beta = 1 / math.sqrt(1 + q**2)
    chi_f = 1 - c_beta
    k_interface_bound = 2 * math.pi * chi_f

    hbar = PLANCK_CONSTANT / (2 * math.pi)
    planck_length = math.sqrt(
        hbar * NEWTON_CONSTANT / SPEED_OF_LIGHT**3
    )
    one_turn_rollout = math.pi * q * planck_length

    symmetric_spectra = {}
    for branch_count in (2, 3, 4):
        loaded_eigenvalue = branch_count / (branch_count - 1) * s**2
        symmetric_spectra[str(branch_count)] = {
            "zero_eigenvalue_multiplicity": 1,
            "loaded_eigenvalue_over_lambda_squared": loaded_eigenvalue,
            "loaded_eigenvalue_multiplicity": branch_count - 1,
            "rank": branch_count - 1,
            "nullity": 1,
        }

    results = {
        "helix_shape_parameter_q": q,
        "phase_closure_residual": abs(q * math.sqrt(1 + q**2) - 2 / math.pi),
        "sin_beta": s,
        "cos_beta": c_beta,
        "positive_progress_factor_for_unit_radius": (
            2 * math.pi * q**2 / math.sqrt(1 + q**2)
        ),
        "fenchel_deficit": chi_f,
        "additional_curvature_bound_rad": k_interface_bound,
        "additional_curvature_bound_degrees": math.degrees(k_interface_bound),
        "planck_length_m": planck_length,
        "one_turn_rollout_m": one_turn_rollout,
        "one_turn_units_per_fm": FEMTOMETRE / one_turn_rollout,
        "symmetric_minimal_closure_spectra": symmetric_spectra,
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
