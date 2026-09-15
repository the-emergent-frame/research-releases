# TEF-2026-008

## Spacetime as Source-Local Rollout and the Conditional Emergence of Three-Dimensional Effective Geometry in The Emergent Frame

- Version: v3.12
- Release date: 2026-09-16
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22776137](https://doi.org/10.5281/zenodo.22776137)
- Concept DOI: [10.5281/zenodo.22776136](https://doi.org/10.5281/zenodo.22776136)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper gives a conditional mathematical realization of source-local spacetime rollout. It models the rollout object as an ensemble of helical trajectories with a weighted transverse relational cell complex. For homogeneous, cell-isomorphic transport, intrinsic relabeling produces a product complex. A transverse quadratic-growth class then yields cubic volume growth with `d_f = 3`; additional long-scale graph-analytic assumptions yield normal diffusion with `d_w = 2` and an infinite-bulk Green scale proportional to `1/r` up to two-sided constants.

The transverse quadratic-growth class is a TEF structural postulate, not a consequence of one isolated helix. The Green result applies to an infinite homogeneous bulk and may be modified by the core, rollout front, or other finite boundaries. Hydrogenic `1/n^2` gross scaling is only a conditional low-energy consistency check. The paper does not derive `J_0 = hbar`, electromagnetic normalization, a full excitation dynamics, multi-source composition, or quantitative cosmology.

## Reproduce the mathematical checks

```bash
python3 calculations/verify.py
```

The script checks the exact shell-sum identity used in the cubic-growth argument, the reported volume, walk, heat-kernel, Green, and hydrogenic scaling exponents, and gauge invariance of a sample link observable and coherence diagnostic. It verifies finite algebraic consequences of the stated construction only; it does not prove the structural postulates or the graph-analytic hypotheses.

## Build the manuscript

A TeX Live installation containing `amsmath`, `amsthm`, `mathtools`, `microtype`, `caption`, `balance`, `titlesec`, `enumitem`, `booktabs`, `hyperref`, `graphicx`, `tikz`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source was supplied by the author for Version 3.12. The PDF is byte-for-byte the file published by Zenodo. The supplied source independently compiles to a 15-page manuscript matching the archived document in content and layout.
