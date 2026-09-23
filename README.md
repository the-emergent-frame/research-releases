# The Emergent Frame Research Releases

This repository contains the source and compact reproducibility materials for formally archived research releases from [The Emergent Frame](https://theemergentframe.org), an independent fundamental-physics research program led by Xiaodan Wu.

The canonical human-readable records are maintained on the TEF website. Zenodo is the authoritative archive for frozen manuscripts and version-specific DOIs. This repository provides the corresponding technical source, numerical checks, citation metadata, and provenance manifests.

## Releases

| TEF release | Manuscript | Version | Status | Archival record |
| --- | --- | --- | --- | --- |
| [TEF-2026-001](papers/TEF-2026-001/) | A Helical Spacetime Ansatz Linking the Planck Scale and Electroweak Mixing | v5.1 | Preprint; not peer reviewed | [10.5281/zenodo.22101000](https://doi.org/10.5281/zenodo.22101000) |
| [TEF-2026-002](papers/TEF-2026-002/) | From a Gravity-Calibrated Helix to a Conditional Fine-Structure Correspondence | v4.7 | Preprint; not peer reviewed | [10.5281/zenodo.22117153](https://doi.org/10.5281/zenodo.22117153) |
| [TEF-2026-003](papers/TEF-2026-003/) | From a Gravity-Calibrated Helix to Neutrino Oscillation Correspondences | v4.2 | Preprint; not peer reviewed | [10.5281/zenodo.22150998](https://doi.org/10.5281/zenodo.22150998) |
| [TEF-2026-004](papers/TEF-2026-004/) | Closed Matter and Open Space: A Relative-Framing Ansatz for Incomplete Quark Sectors and the Matter–Space Interface | v4.6 | Preprint; not peer reviewed | [10.5281/zenodo.22256714](https://doi.org/10.5281/zenodo.22256714) |
| [TEF-2026-005](papers/TEF-2026-005/) | From a Gravity-Calibrated Helix to a Strong-Interaction Confinement Correspondence | v4.1 | Preprint; not peer reviewed | [10.5281/zenodo.22412464](https://doi.org/10.5281/zenodo.22412464) |
| [TEF-2026-006](papers/TEF-2026-006/) | From a Gravity-Calibrated Helix to a Matter–Spacetime Interface: Closure Obstruction and a Factorized Mass-Squared Ansatz | v3.2 | Preprint; not peer reviewed | [10.5281/zenodo.22649267](https://doi.org/10.5281/zenodo.22649267) |
| [TEF-2026-007](papers/TEF-2026-007/) | The Emergent Frame: A Minimal Framework for Spacetime Rollout, Interaction, and Excitation | v2.5 | Preprint; not peer reviewed | [10.5281/zenodo.22723329](https://doi.org/10.5281/zenodo.22723329) |
| [TEF-2026-008](papers/TEF-2026-008/) | Spacetime as Source-Local Rollout and the Conditional Emergence of Three-Dimensional Effective Geometry in The Emergent Frame | v3.12 | Preprint; not peer reviewed | [10.5281/zenodo.22776137](https://doi.org/10.5281/zenodo.22776137) |
| [TEF-2026-009](papers/TEF-2026-009/) | Rollout Connection Dynamics and a Maxwell–Lorentz-Compatible Low-Energy Electromagnetic Sector in The Emergent Frame | v3.3 | Preprint; not peer reviewed | [10.5281/zenodo.22849547](https://doi.org/10.5281/zenodo.22849547) |
| [TEF-2026-010](papers/TEF-2026-010/) | An Electron-Like Charged-Textured Excitation with Spinorial Configuration Topology in The Emergent Frame | v4.0 | Preprint; not peer reviewed | [10.5281/zenodo.22923781](https://doi.org/10.5281/zenodo.22923781) |

## Verify

The numerical checks use only the Python standard library:

```bash
make verify
```

This command verifies the archived PDF hashes and runs each release's standard-library checks. Depending on the release, those checks either recompute reported relations or audit the published numerical outputs and manifests. They do not validate the physical postulates or supply the field-theoretic dynamics identified as open problems in the manuscripts.

Each paper README also records the LaTeX build command. Recompilation verifies source completeness and rendered content; generated PDFs may not be byte-identical to the archived files because PDF metadata can contain build timestamps and toolchain details.

## Scope

Only formally released material is included. Private working notes, failed directions, internal reviews, unpublished hypotheses, and third-party reference files remain outside this repository.

## Citation

Cite the version-specific Zenodo DOI for the manuscript containing the scientific claim. Paper-specific `CITATION.cff` and BibTeX files are stored under each release's `metadata/` directory. The repository-level [CITATION.cff](CITATION.cff) lists all releases.

## License

Manuscripts, LaTeX source, metadata, and documentation are licensed under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Verification scripts are licensed under the [MIT License](LICENSES/MIT.txt). See [LICENSE.md](LICENSE.md) for the file-level mapping.
