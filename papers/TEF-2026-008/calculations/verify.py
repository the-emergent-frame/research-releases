#!/usr/bin/env python3
"""Check finite algebraic consequences reported in TEF-2026-008 v3.12."""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")
REFERENCE_RADIUS = 100


def compare(actual: Any, expected: Any, path: str = "result") -> None:
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise SystemExit(f"{path}: keys differ")
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, (int, float)):
        if not math.isclose(actual, expected, rel_tol=5e-12, abs_tol=5e-15):
            raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")


def main() -> int:
    r = REFERENCE_RADIUS
    ideal_shell_sum = sum((r - abs(m)) ** 2 for m in range(-r, r + 1))
    ideal_closed_form = (2 * r**3 + r) // 3
    if ideal_shell_sum != ideal_closed_form:
        raise SystemExit("the shell sum does not match its closed form")

    endpoint_corrected_sum = sum(
        (1 + r - abs(m)) ** 2 for m in range(-r, r + 1)
    )

    transverse_volume_dimension = 2
    longitudinal_volume_dimension = 1
    volume_dimension = (
        transverse_volume_dimension + longitudinal_volume_dimension
    )
    walk_dimension = 2

    potential_exponent = 1.0
    hydrogen_binding_exponent = (
        -2 * potential_exponent / (2 - potential_exponent)
    )

    phase_alpha = 0.37
    phase_beta = -1.12
    link_phase = 0.83
    frame_alpha = 0.44
    frame_beta = -0.71

    psi_alpha = cmath.exp(1j * phase_alpha)
    psi_beta = cmath.exp(1j * phase_beta)
    link = cmath.exp(-1j * link_phase)
    link_observable = psi_alpha.conjugate() * link * psi_beta

    transformed_psi_alpha = cmath.exp(-1j * frame_alpha) * psi_alpha
    transformed_psi_beta = cmath.exp(-1j * frame_beta) * psi_beta
    transformed_link = (
        cmath.exp(-1j * frame_alpha)
        * link
        * cmath.exp(1j * frame_beta)
    )
    transformed_observable = (
        transformed_psi_alpha.conjugate()
        * transformed_link
        * transformed_psi_beta
    )

    phases = (0.1, -0.2, 0.5)
    link_phases = (0.2, -0.4, 0.7)
    weights = (1.0, 2.0, 0.5)
    edges = ((0, 1), (1, 2), (2, 0))
    covariant_differences = tuple(
        phases[j] - phases[i] - edge_phase
        for (i, j), edge_phase in zip(edges, link_phases)
    )
    coherence = sum(
        weight * math.cos(delta)
        for weight, delta in zip(weights, covariant_differences)
    ) / sum(weights)

    results = {
        "volume_growth": {
            "reference_radius": r,
            "ideal_shell_sum": ideal_shell_sum,
            "ideal_closed_form": ideal_closed_form,
            "endpoint_corrected_shell_sum": endpoint_corrected_sum,
            "transverse_volume_dimension": transverse_volume_dimension,
            "longitudinal_volume_dimension": longitudinal_volume_dimension,
            "product_volume_dimension": volume_dimension,
        },
        "bulk_scaling": {
            "walk_dimension": walk_dimension,
            "heat_kernel_time_exponent": -volume_dimension / walk_dimension,
            "green_distance_exponent": walk_dimension - volume_dimension,
        },
        "hydrogen_consistency": {
            "potential_exponent": potential_exponent,
            "binding_n_exponent": hydrogen_binding_exponent,
        },
        "gauge_covariance": {
            "link_observable_real": link_observable.real,
            "link_observable_imag": link_observable.imag,
            "frame_transformation_residual": abs(
                link_observable - transformed_observable
            ),
            "loop_covariant_phase_sum": sum(covariant_differences),
            "negative_link_phase_sum": -sum(link_phases),
            "weighted_coherence": coherence,
        },
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
