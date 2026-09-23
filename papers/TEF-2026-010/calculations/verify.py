#!/usr/bin/env python3
"""Audit the published numerical artifacts for TEF-2026-010 v4.0."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENTARY = ROOT / "supplementary"
EXPECTED = json.loads(Path(__file__).with_name("expected-results.json").read_text())


def compare(actual: Any, expected: Any, path: str = "result", rel_tol: float = 5e-7) -> None:
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise SystemExit(f"{path}: keys differ")
        for key in expected:
            compare(actual[key], expected[key], f"{path}.{key}", rel_tol)
        return
    if isinstance(expected, (int, float)):
        if not math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=5e-12):
            raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise SystemExit(f"{path}: expected {expected!r}, got {actual!r}")


def verify_manifest() -> int:
    count = 0
    manifest = SUPPLEMENTARY / "MANIFEST_SHA256.txt"
    for line in manifest.read_text().splitlines():
        digest, filename = line.split(maxsplit=1)
        path = SUPPLEMENTARY / filename
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise SystemExit(f"supplementary/{filename}: SHA-256 mismatch")
        count += 1
    return count


def parse_execution_record() -> dict[str, float | int]:
    text = (SUPPLEMENTARY / "TEF_U1_execution_record_v3.1.txt").read_text()
    values = dict(re.findall(r"^([A-Za-z_]+)=([^\n]+)$", text, flags=re.MULTILINE))
    return {
        "status": int(values["status"]),
        "adaptive_nodes": int(values["adaptive_nodes"]),
        "max_rms_residual": float(values["max_rms_residual"]),
        "normalized_phase_charge": float(values["Q"]),
        "energy": float(values["E"]),
        "texture_degree": float(values["degree"]),
        "gauss_relative_mismatch": float(values["gauss_relative_mismatch"]),
    }


def read_rows(filename: str) -> list[dict[str, str]]:
    with (SUPPLEMENTARY / filename).open(newline="") as stream:
        return list(csv.DictReader(stream))


def linear_intercept(xs: list[float], ys: list[float]) -> float:
    count = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    denominator = count * sum(x * x for x in xs) - sum_x * sum_x
    slope = (count * sum(x * y for x, y in zip(xs, ys)) - sum_x * sum_y) / denominator
    return (sum_y - slope * sum_x) / count


def main() -> int:
    manifest_files = verify_manifest()
    canonical = parse_execution_record()

    binding = read_rows("TEF_U1_binding_reaudit_v2.1.csv")[0]
    reference = {
        "radius": float(binding["Rmax"]),
        "joint_energy": float(binding["joint_E"]),
        "isolated_core_energy": float(binding["matched_isolated_core_E"]),
        "isolated_texture_energy": float(binding["isolated_texture_E"]),
        "reference_energy": float(binding["separated_energy"]),
        "reference_gap": float(binding["binding_difference"]),
    }
    closure = reference["isolated_core_energy"] + reference["isolated_texture_energy"]
    if not math.isclose(closure, reference["reference_energy"], rel_tol=1e-12):
        raise SystemExit("primary reference energy does not close")
    if not math.isclose(
        reference["reference_energy"] - reference["joint_energy"],
        reference["reference_gap"],
        rel_tol=1e-12,
    ):
        raise SystemExit("primary reference gap does not close")

    finite_box = read_rows("TEF_U1_finite_box_reference_channel_v2.9.csv")
    inverse_r = [1.0 / float(row["Rmax"]) for row in finite_box]
    extrapolation = {
        "joint_energy": linear_intercept(inverse_r, [float(row["joint_E"]) for row in finite_box]),
        "reference_energy": linear_intercept(
            inverse_r, [float(row["finite_box_reference_E"]) for row in finite_box]
        ),
        "reference_gap": linear_intercept(
            inverse_r, [float(row["reference_gap"]) for row in finite_box]
        ),
    }

    cutoff = read_rows("TEF_U1_origin_cutoff_convergence_v2.8.csv")
    cutoff_energies = [float(row["E_total"]) for row in cutoff]
    cutoff_span = max(cutoff_energies) - min(cutoff_energies)

    parity = read_rows("TEF_U2_physical_rotation_parity_v0.5.csv")
    odd_rows = sum(
        int(row["texture_degree_nu"]) % 2 == 1
        and row["2pi_spatial_rotation_Z2_class"] == "1"
        and row["4pi_spatial_rotation_Z2_class"] == "0"
        and row["spinorial_FR_sector_available_if_nontrivial_rep_selected"] == "True"
        for row in parity
    )

    results = {
        "canonical_run": canonical,
        "primary_reference_channel": reference,
        "inverse_radius_extrapolation": extrapolation,
        "origin_cutoff_energy_span": cutoff_span,
        "odd_degree_spinorial_rows": odd_rows,
    }
    compare(results, EXPECTED)
    print(json.dumps({"manifest_files": manifest_files, **results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
