# TEF-2026-001

## A Helical Spacetime Ansatz Linking the Planck Scale and Electroweak Mixing

- Version: v5.1
- Release date: 2026-08-21
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22101000](https://doi.org/10.5281/zenodo.22101000)
- Concept DOI: [10.5281/zenodo.22100999](https://doi.org/10.5281/zenodo.22100999)
- Canonical page: [theemergentframe.org/papers/helical-spacetime-weak-mixing](https://theemergentframe.org/papers/helical-spacetime-weak-mixing/)

The manuscript studies a gravity-calibrated helical ansatz whose one-cycle phase closure fixes a dimensionless pitch ratio and a candidate primitive geometric reference angle for weak mixing. It is a kinematic ansatz and numerical correspondence, not a derivation of electroweak dynamics.

## Reproduce the reported geometry

```bash
python3 calculations/verify.py
```

The script independently evaluates the closed-form solution of

```text
q * sqrt(1 + q^2) = 2 / pi
```

and checks the reported values of `q`, the helix angle, and `sin^2(beta)`.

## Build the manuscript

A TeX Live installation containing REVTeX 4.2, TikZ, `siunitx`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps or TeX toolchain versions.

## Source provenance

The archived v5.1 PDF is byte-for-byte the file published by Zenodo. The v5.1 LaTeX source is reconstructed from the retained v5 source by adding the DOI to the author note. Full-text extraction of the v5 and v5.1 PDFs found no other textual difference. The scientific content is unchanged from v5; v5.1 records the DOI-bearing archival copy.
