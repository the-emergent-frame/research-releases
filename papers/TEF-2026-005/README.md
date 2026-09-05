# TEF-2026-005

## From a Gravity-Calibrated Helix to a Strong-Interaction Confinement Correspondence

- Version: v4.1
- Release date: 2026-09-06
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22412464](https://doi.org/10.5281/zenodo.22412464)
- Concept DOI: [10.5281/zenodo.22412463](https://doi.org/10.5281/zenodo.22412463)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper formulates a conditional closure-energy framework for a restricted connected static-source channel. Along a discrete branch with fixed rollout increment `P`, its assumptions imply that the averaged static-energy slope tends to `Delta E / P`. The TEF specialization uses `P_n = 2 pi n q R_G`, where `R_G` and `q` are inherited from Paper I.

The result is not a microscopic derivation of QCD confinement. The closure sectors, no-shortcut condition, reducing static quadratic form, and subextensive optimized residual envelope are assumptions awaiting microscopic justification. The turn multiplicity `n`, positive energy increment `Delta E`, continuous-separation behavior, `SU(3)_c` dynamics, string breaking, flux-tube fluctuations, and ultraviolet running are not derived.

## Reproduce the numerical checks

```bash
python3 calculations/verify.py
```

The script checks the inherited helix parameter and gravity-calibrated radius, the one- and two-turn rollout lengths, the number of two-turn units per femtometre, the optional string-tension diagnostic, and the partition-invariance identity. These checks validate reported arithmetic only; they do not validate the physical assumptions or establish confinement.

## Build the manuscript

A TeX Live installation containing TikZ, `microtype`, `mathtools`, `booktabs`, `siunitx`, `caption`, `enumitem`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source was supplied by the author for Version 4.1. The PDF is byte-for-byte the file published by Zenodo. The supplied source independently compiles to an 11-page manuscript matching the archived document in content and layout.
