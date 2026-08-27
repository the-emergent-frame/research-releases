# TEF-2026-002

## From a Gravity-Calibrated Helix to a Conditional Fine-Structure Correspondence

- Version: v4.7
- Release date: 2026-08-26
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22117153](https://doi.org/10.5281/zenodo.22117153)
- Concept DOI: [10.5281/zenodo.22117152](https://doi.org/10.5281/zenodo.22117152)
- Canonical page: [theemergentframe.org/papers/helical-geometry-fine-structure-constant](https://theemergentframe.org/papers/helical-geometry-fine-structure-constant/)

The manuscript inherits the frozen helix parameter from TEF-2026-001 and examines an explicitly conditional map to a fine-structure candidate. The factor `1 / (2*pi^2)` and its physical coupling interpretation are postulates whose dynamical justification remains open.

## Reproduce the reported correspondence

```bash
python3 calculations/verify.py
```

The script checks the inherited `q`, helical path excess, conditional fine-structure candidate, inverse value, and relative difference from the cited 2022 CODATA low-energy value.

## Build the manuscript

A TeX Live installation containing TikZ, `geometry`, `microtype`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps or TeX toolchain versions.

## Source provenance

The LaTeX source and PDF are the retained v4.7 release pair. The PDF is byte-for-byte the file published by Zenodo.
