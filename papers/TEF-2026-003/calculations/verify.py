#!/usr/bin/env python3
"""Recompute the numerical comparisons reported in TEF-2026-003 v4.2."""

from __future__ import annotations

import json
import math
from pathlib import Path


EXPECTED_PATH = Path(__file__).with_name("expected-results.json")
JUNO_SIN2_THETA12 = 0.3092
JUNO_DM21 = 7.50e-5
NUFIT_DM31_NO = 2.521e-3
NUFIT_DM32_IO_ABS = 2.510e-3


def close(actual: float, expected: float, tolerance: float = 5e-12) -> None:
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise SystemExit(f"expected {expected:.16g}, got {actual:.16g}")


def main() -> int:
    q_squared = (-1.0 + math.sqrt(1.0 + 16.0 / math.pi**2)) / 2.0
    q = math.sqrt(q_squared)
    q_cubed = q**3
    q_sixth = q_cubed**2
    results = {
        "q": q,
        "q_squared": q_squared,
        "q_cubed": q_cubed,
        "q_sixth": q_sixth,
        "r_nu_no": JUNO_DM21 / NUFIT_DM31_NO,
        "r_nu_io": JUNO_DM21 / NUFIT_DM32_IO_ABS,
        "conditional_dm31_no": JUNO_DM21 / q_sixth,
        "conditional_dm21_no": q_sixth * NUFIT_DM31_NO,
        "sin2_theta12_cubed": JUNO_SIN2_THETA12**3,
    }

    expected = json.loads(EXPECTED_PATH.read_text())
    for key, value in results.items():
        close(value, expected[key])

    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
