# TEF-2026-006

## From a Gravity-Calibrated Helix to a Matter-Spacetime Interface

**Subtitle:** Closure Obstruction and a Factorized Mass-Squared Ansatz

- Version: v3.2
- Release date: 2026-09-08
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22649267](https://doi.org/10.5281/zenodo.22649267)
- Concept DOI: [10.5281/zenodo.22649266](https://doi.org/10.5281/zenodo.22649266)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper proves a conditional geometric obstruction: a finite sequence of oriented, complete, nonzero-pitch circular helix turns cannot be joined directly with `C^1` tangent continuity into a closed oriented curve. It also gives a necessary additional-curvature bound when one frozen native turn is retained in a smooth closed completion.

After relaxing direct gluing, the paper separately constructs a linear interface map `C_N` from prescribed post-rerouting closure data and studies the positive Gram operator `G_N = C_N^dagger C_N`. Its rank and kernel follow from the chosen geometry. Identifying this operator with a physical mass-squared contribution remains an ansatz; particle masses, QCD dynamics, a unique completion geometry, and a fundamental TEF energy law are not derived.

## Reproduce the numerical checks

```bash
python3 calculations/verify.py
```

The script checks the frozen helix quantities, the positive endpoint-progress factor used in the closure obstruction, the Fenchel deficit and curvature bound, the primitive-to-hadronic scale ratio, and the symmetric minimal-closure Gram spectra for `N = 2, 3, 4`. It validates reported algebra and arithmetic only; it does not validate the physical interface or mass-squared ansatz.

## Build the manuscript

A TeX Live installation containing `microtype`, `mathtools`, `booktabs`, `siunitx`, `caption`, `enumitem`, `flushend`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source was supplied by the author for Version 3.2. The PDF is byte-for-byte the file published by Zenodo. The supplied source independently compiles to a 12-page manuscript matching the archived document in content and layout.
