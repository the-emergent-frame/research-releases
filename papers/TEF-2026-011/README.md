# TEF-2026-011

## Spatial Dimension, Internal Phase, and Kinematics of Helical Line Families

- Version: v2.1
- Release date: 2026-09-25
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22945612](https://doi.org/10.5281/zenodo.22945612)
- Concept DOI: [10.5281/zenodo.22945611](https://doi.org/10.5281/zenodo.22945611)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper develops differential-geometric tools for families of helical lines. It distinguishes the intrinsic one-dimensionality of an individual helix from a selected rank-three effective position map and from the four-dimensional position-phase state space carried over that image. On a regular local chart, the construction is a circle bundle over a three-dimensional effective position space.

The paper gives covariant phase comparison, loop-compatibility conditions, and moving-frame velocity and acceleration formulas for arbitrary position-phase paths. For a selected common initial phase, it derives an explicit helical coordinate chart on a proven injective domain, including a closed-form inverse, Jacobian, second derivatives, and a flat Euclidean pullback metric. It also separates small position offsets from tangent, arc-length, and finite-resolution effects.

The three-dimensional effective position is conditional on the chosen projection; it is not derived from the helicity of one curve. The construction does not add a fourth spatial translation or time coordinate, derive physical dynamics, identify the internal phase with a quantum state, or establish a continuous-discrete correspondence with TEF rollout complexes.

## Audit the published checks

```bash
python3 calculations/verify.py
```

This standard-library audit validates the stored verification report, fixed sample counts, pass conditions, and all reported numerical tolerances. It does not rerun the symbolic and numerical experiment suite.

## Rerun the full verification and figures

The complete author-supplied script requires Python with NumPy, SymPy, and matplotlib:

```bash
python3 calculations/verify_and_plot_v2.py
```

The script uses fixed random seeds, reruns the symbolic identities and numerical tests, regenerates the two figure pairs under `figures/`, and rewrites `checks/verification_v2.json`.

## Build the manuscript

A TeX Live installation containing `amsmath`, `amsthm`, `mathtools`, `microtype`, `setspace`, `caption`, `titlesec`, `enumitem`, `booktabs`, `array`, `graphicx`, `tikz-cd`, `hyperref`, `balance`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

Zenodo Version 2.1 contains the manuscript PDF, reproduced here byte-for-byte. The LaTeX source, vector figures, plotting/verification script, and stored check report were supplied by the author from the local Version 2.1 release workspace. The source independently compiles to an 11-page manuscript matching the archived document in content and layout.
