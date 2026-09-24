#!/usr/bin/env python3
"""Audit the stored verification report for TEF-2026-011 v2.1."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads(Path(__file__).with_name("expected-results.json").read_text())
REPORT = json.loads((ROOT / "checks" / "verification_v2.json").read_text())


def main() -> int:
    if REPORT["version"] != EXPECTED["report_version"]:
        raise SystemExit("verification report version mismatch")

    numerical = REPORT["numerical"]
    if numerical["sample_count"] != EXPECTED["sample_count"]:
        raise SystemExit("numerical sample count mismatch")
    if numerical["trajectory_count"] != EXPECTED["trajectory_count"]:
        raise SystemExit("numerical trajectory count mismatch")

    failed_tolerances = {
        name: (numerical["max_errors"][name], tolerance)
        for name, tolerance in numerical["tolerances"].items()
        if numerical["max_errors"][name] > tolerance
    }
    if failed_tolerances:
        raise SystemExit(f"reported numerical tolerances failed: {failed_tolerances}")

    phase = REPORT["independent_phase"]
    if phase["trajectory_count"] != EXPECTED["independent_phase_trajectory_count"]:
        raise SystemExit("independent-phase trajectory count mismatch")
    for name, limit in EXPECTED["independent_phase_error_limits"].items():
        if phase[name] > limit:
            raise SystemExit(f"{name}: expected <= {limit}, got {phase[name]}")

    pass_values = [
        REPORT["symbolic"],
        numerical["fold_and_noninjectivity"],
        numerical["image_rejection"],
        phase["symbolic_phase_and_coframe"],
        phase["rank_and_distinct_kernels"],
        phase["reference_invariance"],
        phase["frenet_bridge"],
        REPORT["graph"],
    ]
    if len(pass_values) != EXPECTED["required_pass_fields"] or not all(
        value.startswith("PASS") for value in pass_values
    ):
        raise SystemExit("one or more stored pass conditions are missing")

    summary = {
        "report_version": REPORT["version"],
        "sample_count": numerical["sample_count"],
        "trajectory_count": numerical["trajectory_count"],
        "independent_phase_trajectory_count": phase["trajectory_count"],
        "largest_numerical_tolerance_ratio": max(
            numerical["max_errors"][name] / tolerance
            for name, tolerance in numerical["tolerances"].items()
        ),
        "pass_fields": len(pass_values),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
