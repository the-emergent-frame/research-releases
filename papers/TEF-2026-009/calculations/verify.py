#!/usr/bin/env python3
"""Check algebraic consequences reported in TEF-2026-009 v3.3."""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Any


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [dot(row, vector) for row in matrix]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def matmul(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matsub(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    return [
        [a - b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def inverse_2x2(matrix: list[list[float]]) -> list[list[float]]:
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def cross(left: list[float], right: list[float]) -> list[float]:
    return [
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    ]


def compare(actual: Any, expected: Any, path: str = "result") -> None:
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise SystemExit(f"{path}: keys differ")
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if len(actual) != len(expected):
            raise SystemExit(f"{path}: lengths differ")
        for index, value in enumerate(expected):
            compare(actual[index], value, f"{path}[{index}]")
        return
    if isinstance(expected, (int, float)):
        if not math.isclose(actual, expected, rel_tol=5e-12, abs_tol=5e-15):
            raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")


def main() -> int:
    electric_block = [[2.0, 0.3], [0.3, 1.5]]
    mixed_block = [[0.2, -0.1], [0.05, 0.15]]
    magnetic_block = [[1.2, 0.1], [0.1, 1.0]]
    temporal_rate = [0.7, -0.4]
    curvature = [0.3, -0.2]

    electric_inverse = inverse_2x2(electric_block)
    effective_magnetic_block = matsub(
        magnetic_block,
        matmul(
            matmul(transpose(mixed_block), electric_inverse),
            mixed_block,
        ),
    )
    trace = effective_magnetic_block[0][0] + effective_magnetic_block[1][1]
    determinant = (
        effective_magnetic_block[0][0] * effective_magnetic_block[1][1]
        - effective_magnetic_block[0][1] * effective_magnetic_block[1][0]
    )
    discriminant = math.sqrt(trace**2 - 4 * determinant)
    eigenvalues = [(trace - discriminant) / 2, (trace + discriminant) / 2]

    shifted_rate = [
        rate - mixing
        for rate, mixing in zip(
            temporal_rate, matvec(mixed_block, curvature)
        )
    ]
    stationary_flux = matvec(electric_inverse, shifted_rate)
    original_lagrangian = (
        dot(stationary_flux, temporal_rate)
        - 0.5 * dot(stationary_flux, matvec(electric_block, stationary_flux))
        - dot(stationary_flux, matvec(mixed_block, curvature))
        - 0.5 * dot(curvature, matvec(magnetic_block, curvature))
    )
    effective_lagrangian = (
        0.5 * dot(shifted_rate, matvec(electric_inverse, shifted_rate))
        - 0.5 * dot(curvature, matvec(magnetic_block, curvature))
    )

    edges = ((0, 1), (1, 2), (2, 0))
    link_angles = (0.2, -0.3, 0.7)
    frame_angles = (0.4, -0.2, 0.1)
    transformed_links = tuple(
        angle + frame_angles[target] - frame_angles[source]
        for angle, (source, target) in zip(link_angles, edges)
    )
    plaquette_flux = sum(link_angles)
    transformed_flux = sum(transformed_links)
    holonomy = cmath.exp(-1j * plaquette_flux)

    def periodic_potential(angle: float) -> float:
        return (
            1.2
            + 0.7 * math.cos(angle)
            - 0.3 * math.sin(2 * angle)
            + 0.11 * math.cos(3 * angle)
        )

    electric_stiffness = 9.0
    magnetic_stiffness = 4.0
    epsilon = 1 / electric_stiffness
    mu = 1 / magnetic_stiffness
    speed = math.sqrt(electric_stiffness * magnetic_stiffness)
    impedance = math.sqrt(electric_stiffness / magnetic_stiffness)

    wavevector = [3.0, 4.0, 0.0]
    electric_field = [4.0, -3.0, 0.0]
    wavenumber = math.sqrt(dot(wavevector, wavevector))
    omega = speed * wavenumber
    magnetic_field = [
        component / omega
        for component in cross(wavevector, electric_field)
    ]
    energy_density = (
        0.5 * epsilon * dot(electric_field, electric_field)
        + 0.5 / mu * dot(magnetic_field, magnetic_field)
    )
    poynting = [
        component / mu for component in cross(electric_field, magnetic_field)
    ]
    poynting_magnitude = math.sqrt(dot(poynting, poynting))

    charge = 2.0
    velocity = [0.3, 0.4, -0.2]
    external_electric = [1.0, -2.0, 0.5]
    external_magnetic = [-0.5, 0.25, 1.0]
    lorentz_force = [
        charge * (electric_component + magnetic_component)
        for electric_component, magnetic_component in zip(
            external_electric, cross(velocity, external_magnetic)
        )
    ]

    charge_scale = 2.4
    action_scale = 3.1
    reference_impedance = 1.7
    field_rescaling = 2.5
    alpha = (
        charge_scale**2 * reference_impedance
        / (4 * math.pi * action_scale)
    )
    rescaled_alpha = (
        (charge_scale / field_rescaling) ** 2
        * (field_rescaling**2 * reference_impedance)
        / (4 * math.pi * action_scale)
    )

    results = {
        "quadratic_response": {
            "effective_magnetic_block": effective_magnetic_block,
            "effective_block_eigenvalues": eigenvalues,
            "stationary_flux": stationary_flux,
            "original_lagrangian": original_lagrangian,
            "effective_lagrangian": effective_lagrangian,
            "elimination_residual": abs(
                original_lagrangian - effective_lagrangian
            ),
        },
        "compact_gauge": {
            "plaquette_flux": plaquette_flux,
            "transformed_plaquette_flux": transformed_flux,
            "flux_residual": abs(plaquette_flux - transformed_flux),
            "holonomy_real": holonomy.real,
            "holonomy_imag": holonomy.imag,
            "periodicity_residual": abs(
                periodic_potential(0.37 + 2 * math.pi)
                - periodic_potential(0.37)
            ),
        },
        "maxwell_representative": {
            "electric_stiffness": electric_stiffness,
            "magnetic_stiffness": magnetic_stiffness,
            "epsilon": epsilon,
            "mu": mu,
            "speed": speed,
            "impedance": impedance,
            "epsilon_mu_product": epsilon * mu,
            "plane_wave_omega": omega,
            "wavevector_dot_electric": dot(wavevector, electric_field),
            "magnetic_field": magnetic_field,
            "energy_density": energy_density,
            "poynting": poynting,
            "poynting_magnitude": poynting_magnitude,
            "speed_times_energy_density": speed * energy_density,
        },
        "lorentz_force": lorentz_force,
        "normalization": {
            "dimensionless_coupling": alpha,
            "rescaled_dimensionless_coupling": rescaled_alpha,
            "rescaling_residual": abs(alpha - rescaled_alpha),
        },
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    compare(results, expected)
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
