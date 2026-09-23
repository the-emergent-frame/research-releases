# TEF-2026-010

## An Electron-Like Charged-Textured Excitation with Spinorial Configuration Topology in The Emergent Frame

- Version: v4.0
- Release date: 2026-09-24
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22923781](https://doi.org/10.5281/zenodo.22923781)
- Concept DOI: [10.5281/zenodo.22923780](https://doi.org/10.5281/zenodo.22923780)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper develops an electron-like matter candidate on the already-realized TEF rollout substrate. The candidate is a localized coherent charged resonance distributed across neighboring helices and coupled to an independent degree-one rollout-frame texture. A single effective action combines the charged collective field, a canonically normalized electromagnetic connection, and the frame texture.

On the flat finite numerical domain, the coupled radial equations admit a stationary charged-textured solution with mutual backreaction. The primary `R = 40` calculation gives normalized phase/Noether charge `N ~= 82.382379` and energy `E ~= 174.450853`; the joint state lies approximately `7.887096` below the specified matched-charge finite-box reference sum. A separately constructed smooth full-space representative has the standard odd mapping-space rotation class: its `2 pi` loop is noncontractible and its twice-traversed `4 pi` loop is contractible.

The two constructions are linked but distinct. The work does not prove nonlinear stability or a general binding theorem, select a Finkelstein--Rubinstein representation, establish `j = 1/2`, derive the observed electron charge or mass, construct exchange statistics, or obtain Dirac and QED-like low-energy closure.

## Reproduce and audit

```bash
python3 calculations/verify.py
```

The repository check uses only the Python standard library. It validates the published supplementary manifest, the preserved canonical execution record, the reported finite-box observables, the reference-channel energy gap, the `1/R` diagnostic extrapolation, cutoff stability, and the degree-parity table. It does not rerun the nonlinear boundary-value solver or validate the physical assumptions.

The complete published supplementary package is unpacked under [`supplementary/`](supplementary/). Rerunning its canonical solver requires the numerical environment documented there: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3, and matplotlib 3.10.8.

## Build the manuscript

A TeX Live installation containing `amsmath`, `mathtools`, `amsthm`, `mathrsfs`, `microtype`, `setspace`, `caption`, `balance`, `titlesec`, `enumitem`, `booktabs`, `hyperref`, `graphicx`, TikZ, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The PDF is byte-for-byte the file published by Zenodo. The LaTeX source was supplied by the author for Version 4.0, and the required profile figure is included beside it. The source independently compiles to the 16-page manuscript matching the archived document in content and layout. The unpacked supplementary files are byte-for-byte the contents of the reproducibility ZIP published with the Zenodo record.
