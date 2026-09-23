# TEF Electron-Like Excitation v4.0 - Supplementary Reproducibility Package

This package accompanies:

**Xiaodan Wu (2026), _An Electron-Like Charged-Textured Excitation with Spinorial Configuration Topology in The Emergent Frame_, Version 4.0.**

DOI: [10.5281/zenodo.22923781](https://doi.org/10.5281/zenodo.22923781)

## Version and provenance

The finite-box U1 numerical calculation, parameter set, solver outputs, and diagnostic data in manuscript v4.0 are unchanged from the supplementary package assembled for manuscript v3.2. Version 4.0 revises the title, presentation, organization, and scientific framing of the paper without changing those numerical artifacts.

The original file-level version numbers are intentionally retained for provenance. In particular:

- `TEF_U1_canonical_solver_v2.1.py` is the canonical solver used for the reported U1 calculation;
- `TEF_U1_execution_record_v3.1.txt` is the preserved reference execution record; and
- the remaining filename versions identify the corresponding data or figure revisions.

These historical filename versions do not indicate that this is a v3.2 manuscript package. This archive is the supplementary reproducibility package accompanying manuscript v4.0.

## Reference numerical environment

- Python 3.13.5
- NumPy 2.3.5
- SciPy 1.17.0
- pandas 2.2.3
- matplotlib 3.10.8

## Primary finite-box solver

Run:

```bash
python TEF_U1_canonical_solver_v2.1.py
```

The included reference execution record reports:

```text
status=0
adaptive_nodes=2116
max_rms_residual=9.936912e-07
Q=82.382378960500
E=174.450852921338
degree=0.999999998383
gauss_relative_mismatch=1.547620e-10
```

The solver's historical printed `Q` is denoted by the normalized phase/Noether charge `N` (math symbol `\mathcal N`) in manuscript v4.0.

## Scope of reproducibility

The solver and U1 data reproduce the finite-box stationary calculation only. They support the reported charge, energy, Gauss-law closure, radial degree, convergence checks, and finite-box reference-channel comparison.

They do not numerically construct the smooth full-space representative used in the configuration-space topology argument. That representative is defined analytically by a three-dimensionally smooth inner and outer completion of the finite-box scalar and texture profiles. No equality of its completed electrostatic field, full-space charge, or full-space energy with the finite-box values is claimed.

The U2 files preserve earlier physical-rotation diagnostics used during development of the topology analysis. The v4.0 topology result is stated and justified in the manuscript itself; the U2 diagnostics are included for provenance rather than presented as an independent proof.

## Included materials

- canonical U1 solver;
- raw `R = 40` joint profiles;
- finite-box and origin-cutoff convergence data;
- solver/grid convergence data;
- finite-box reference-channel and binding reaudit data;
- parameter file;
- U1 figures;
- U2 rotation-diagnostic data and figures;
- preserved reference execution record; and
- SHA-256 manifest.

This package documents author-side reproducibility of the finite-box calculation. Independent external replication is not claimed.
