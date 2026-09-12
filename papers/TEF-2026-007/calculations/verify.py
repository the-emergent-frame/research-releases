#!/usr/bin/env python3
"""Check the reported geometry and energy scales in TEF-2026-007 v2.5."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")

PLANCK_CONSTANT = 6.62607015e-34  # J s, exact
NEWTON_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
SPEED_OF_LIGHT = 299792458.0  # m s^-1, exact
ELECTRONVOLT_JOULES = 1.602176634e-19  # J, exact
ELECTRON_REST_ENERGY_MEV = 0.51099895069
FERMI_CONSTANT_GEV_MINUS_2 = 1.1663787e-5
LATTICE_BENCHMARK_MEV = 445.0


def compare(actual: Any, expected: Any, path: str = "result") -> None:
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise SystemExit(f"{path}: keys differ")
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, (int, float)):
        if not math.isclose(actual, expected, rel_tol=5e-12, abs_tol=1e-45):
            raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")


def main() -> int:
    q = math.sqrt((-1 + math.sqrt(1 + 16 / math.pi**2)) / 2)

    hbar = PLANCK_CONSTANT / (2 * math.pi)
    planck_length = math.sqrt(
        hbar * NEWTON_CONSTANT / SPEED_OF_LIGHT**3
    )
    primitive_radius = planck_length / 2
    helix_pitch_parameter = q * primitive_radius
    one_turn_rollout = 2 * math.pi * helix_pitch_parameter

    interaction_scale_gev = (
        math.sqrt(2) * FERMI_CONSTANT_GEV_MINUS_2
    ) ** -0.5
    closure_scale_mev = math.sqrt(
        math.pi
        / 2
        * ELECTRON_REST_ENERGY_MEV
        * interaction_scale_gev
        * 1000
    )

    planck_energy_gev = (
        math.sqrt(hbar * SPEED_OF_LIGHT**5 / NEWTON_CONSTANT)
        / ELECTRONVOLT_JOULES
        / 1e9
    )
    global_rollout_scale_gev = math.pi * q * planck_energy_gev

    results = {
        "helix": {
            "shape_parameter_q": q,
            "phase_closure_residual": abs(
                q * math.sqrt(1 + q**2) - 2 / math.pi
            ),
            "planck_length_m": planck_length,
            "primitive_radius_m": primitive_radius,
            "pitch_parameter_m": helix_pitch_parameter,
            "one_turn_axial_advance_m": one_turn_rollout,
        },
        "closure_calibration": {
            "interaction_scale_gev": interaction_scale_gev,
            "closure_scale_mev": closure_scale_mev,
            "lattice_benchmark_mev": LATTICE_BENCHMARK_MEV,
            "relative_difference_percent": (
                (closure_scale_mev - LATTICE_BENCHMARK_MEV)
                / LATTICE_BENCHMARK_MEV
                * 100
            ),
        },
        "global_rollout_bookkeeping": {
            "planck_energy_gev": planck_energy_gev,
            "rollout_scale_gev": global_rollout_scale_gev,
        },
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
