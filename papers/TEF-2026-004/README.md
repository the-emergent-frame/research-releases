# TEF-2026-004

## Closed Matter and Open Space

**Subtitle:** A Relative-Framing Ansatz for Incomplete Quark Sectors and the Matter–Space Interface

- Version: v4.6
- Release date: 2026-09-02
- Status: Preprint; not peer reviewed
- Version DOI: [10.5281/zenodo.22256714](https://doi.org/10.5281/zenodo.22256714)
- Concept DOI: [10.5281/zenodo.22256713](https://doi.org/10.5281/zenodo.22256713)
- Canonical page: [theemergentframe.org/papers/closed-matter-open-space](https://theemergentframe.org/papers/closed-matter-open-space/)

This paper opens the matter-topology branch of the TEF research program. It models a quark-like constituent as a boundary-exposed framed matter sub-sector and proves a restricted mathematical statement: for a fixed embedded open arc, chosen normal-plane trivialization, and fixed endpoint phase, the endpoint-fixed homotopy classes form a torsor for `pi_1(S^1)`, isomorphic to the integers.

The nontrivial threefold endpoint phase, selection of an adjacent `D/U` pair, and identification of the normalized framing lift with electric charge are separate postulates. The construction does not derive continuous `SU(3)_c`, confinement, weak dynamics, spin-statistics, or a complete particle model.

## Reproduce the algebraic checks

```bash
python3 calculations/verify.py
```

The script checks the explicit roots-of-unity, adjacent-class, normalized-lift, composite-boundary, triality, and baryon-charge bookkeeping relations used in the manuscript. It does not prove the torsor proposition or validate the physical postulates.

## Build the manuscript

A TeX Live installation containing REVTeX 4.2, TikZ, `microtype`, `mathtools`, `enumitem`, and `latexmk` is required.

```bash
cd paper
latexmk -pdf manuscript.tex
```

The tracked PDF is the authoritative Zenodo artifact. A rebuilt PDF may differ at the byte level because of build timestamps and TeX toolchain versions.

## Source provenance

The LaTeX source and PDF are the retained v4.6 release pair. The PDF is byte-for-byte the file published by Zenodo.
