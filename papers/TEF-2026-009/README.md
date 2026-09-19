# TEF-2026-009

## Rollout Connection Dynamics and a Maxwell–Lorentz-Compatible Low-Energy Electromagnetic Sector in The Emergent Frame

- Version: v3.3
- Release date: 2026-09-19
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22849547](https://doi.org/10.5281/zenodo.22849547)
- Concept DOI: [10.5281/zenodo.22849546](https://doi.org/10.5281/zenodo.22849546)
- Project: [theemergentframe.org](https://theemergentframe.org)

This paper constructs a conditional low-energy electromagnetic sector on the source-local rollout geometry. Adopted transverse-frame comparison supplies a compact `U(1)` connection, while an assumed local Hamiltonian with a positive physical quadratic Hessian supplies connection dynamics. Under explicit smooth-interpolation, constitutive, boundary, and defect-free assumptions, the continuum representatives have Maxwell form. Wave-speed matching yields two transverse modes with `omega = c k`, and an additionally assumed electric-monopole coupling gives the external Lorentz force and compatible field energy and momentum exchange.

The result establishes classical effective compatibility, not a microscopic derivation of electromagnetism. The paper does not prove continuum convergence, a quantum or statistical Coulomb phase, microscopic Lorentz invariance, or the existence of a finite-energy charged resonance. Compactness classifies allowed charge representations but does not populate them. The electron candidate, `J_0 = hbar`, the measured charge, electromagnetic impedance, fine-structure normalization, quantization, and QED comparison remain open.

## Reproduce the algebraic checks

```bash
python3 calculations/verify.py
```

The script checks a representative positive quadratic Hessian and Schur-complement elimination, compact plaquette gauge invariance and potential periodicity, propagation-speed and impedance identities, transverse-wave energy transport, a sample Lorentz force, and invariance of the dimensionless coupling under field normalization changes. It verifies algebraic consequences of the stated effective construction only; it does not validate the microscopic assumptions or establish the existence of the proposed charged modes.

## Build the manuscript

A TeX Live installation containing `amsmath`, `amsthm`, `mathtools`, `microtype`, `caption`, `balance`, `titlesec`, `enumitem`, `booktabs`, `hyperref`, `graphicx`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source was supplied by the author for Version 3.3. The PDF is byte-for-byte the file published by Zenodo. The supplied source independently compiles to a 16-page manuscript matching the archived document in content and layout.
