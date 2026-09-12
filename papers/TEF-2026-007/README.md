# TEF-2026-007

## The Emergent Frame: A Minimal Framework for Spacetime Rollout, Interaction, and Excitation

- Version: v2.5
- Release date: 2026-09-12
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22723329](https://doi.org/10.5281/zenodo.22723329)
- Concept DOI: [10.5281/zenodo.22723328](https://doi.org/10.5281/zenodo.22723328)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper consolidates the current TEF research programme into a minimal working framework. It distinguishes persistent closed matter topology, matter-associated spacetime rollout, and excitations supported by the resulting structure. Complete closures are provisionally assigned independent rollout-source identity; excitations are not, although all energy, momentum, stress, motion, and interaction energy must still enter effective gravitational backreaction.

The inherited helix supplies local phase-bearing geometry with transverse closure and axial advance, but not a wave equation. The proposed strong, weak, electromagnetic, and gravitational correspondences remain research directions rather than derived interaction laws. The separate `444.56 MeV` closure-scale relation is explicitly a retrospective, replaceable calibration conjecture, not an independent prediction or a consequence of the rollout ontology.

## Reproduce the numerical checks

```bash
python3 calculations/verify.py
```

The script checks the frozen helix geometry, the electroweak scale inferred from the stated Fermi constant, the candidate closure scale, its comparison with the frozen `445 MeV` lattice benchmark, and the global rollout bookkeeping scale. It validates reported algebra and arithmetic only; it does not validate the framework's ontology, interaction proposals, or physical interpretation.

## Build the manuscript

A TeX Live installation containing `amsmath`, `mathtools`, `booktabs`, `microtype`, `enumitem`, `hyperref`, `siunitx`, `caption`, `balance`, `tikz`, `pgfplots`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source was supplied by the author for Version 2.5. The PDF is byte-for-byte the file published by Zenodo. The supplied source independently compiles to an 11-page manuscript matching the archived document in content and layout.
