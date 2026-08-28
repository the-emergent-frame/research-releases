# TEF-2026-003

## From a Gravity-Calibrated Helix to Neutrino Oscillation Correspondences

**Subtitle:** A Third Cross-Sector Comparison of the Frozen TEF Shape Parameter

- Version: v4.2
- Release date: 2026-08-29
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22150998](https://doi.org/10.5281/zenodo.22150998)
- Concept DOI: [10.5281/zenodo.22150997](https://doi.org/10.5281/zenodo.22150997)
- Canonical page: [theemergentframe.org/papers/cross-sector-neutrino-correspondences](https://theemergentframe.org/papers/cross-sector-neutrino-correspondences/)

The manuscript carries the publicly frozen helical parameter from TEF-2026-001 and TEF-2026-002 into neutrino oscillation phenomenology without refitting it. It records the post-hoc, coefficient-free correspondences `q^2` with the solar mixing quantity and `q^6` with the ratio of the solar and atmospheric mass-squared splittings.

These correspondences are empirical targets, not a derivation of neutrino mixing or a preregistered prediction. The paper freezes the mappings for prospective comparison and identifies a common relativistic spectral operator as the missing dynamical construction.

## Reproduce the reported comparisons

```bash
python3 calculations/verify.py
```

The script recomputes the inherited `q`, its relevant powers, the quoted central-value ratios, the two conditional mass-squared restatements, and the parameter-eliminated JUNO comparison.

## Build the manuscript

A TeX Live installation containing TikZ, `geometry`, `microtype`, `mathtools`, `multirow`, `siunitx`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source and PDF are the retained v4.2 release pair. The PDF is byte-for-byte the file published by Zenodo.
