# The Emergent Frame Research Releases

This repository contains the source and compact reproducibility materials for formally archived research releases from [The Emergent Frame](https://theemergentframe.org), an independent fundamental-physics research program led by Xiaodan Wu.

The canonical human-readable records are maintained on the TEF website. Zenodo is the authoritative archive for frozen manuscripts and version-specific DOIs. This repository provides the corresponding technical source, numerical checks, citation metadata, and provenance manifests.

## Releases

| TEF release | Manuscript | Version | Status | Archival record |
| --- | --- | --- | --- | --- |
| [TEF-2026-001](papers/TEF-2026-001/) | A Helical Spacetime Ansatz Linking the Planck Scale and Electroweak Mixing | v5.1 | Preprint; not peer reviewed | [10.5281/zenodo.22101000](https://doi.org/10.5281/zenodo.22101000) |
| [TEF-2026-002](papers/TEF-2026-002/) | From a Gravity-Calibrated Helix to a Conditional Fine-Structure Correspondence | v4.7 | Preprint; not peer reviewed | [10.5281/zenodo.22117153](https://doi.org/10.5281/zenodo.22117153) |
| [TEF-2026-003](papers/TEF-2026-003/) | From a Gravity-Calibrated Helix to Neutrino Oscillation Correspondences | v4.2 | Preprint; not peer reviewed | [10.5281/zenodo.22150998](https://doi.org/10.5281/zenodo.22150998) |

## Verify

The numerical checks use only the Python standard library:

```bash
make verify
```

This command verifies the archived PDF hashes and reruns the calculations reported in each release. It does not validate the physical postulates or supply the field-theoretic dynamics identified as open problems in the manuscripts.

Each paper README also records the LaTeX build command. Recompilation verifies source completeness and rendered content; generated PDFs may not be byte-identical to the archived files because PDF metadata can contain build timestamps and toolchain details.

## Scope

Only formally released material is included. Private working notes, failed directions, internal reviews, unpublished hypotheses, and third-party reference files remain outside this repository.

## Citation

Cite the version-specific Zenodo DOI for the manuscript containing the scientific claim. Paper-specific `CITATION.cff` and BibTeX files are stored under each release's `metadata/` directory. The repository-level [CITATION.cff](CITATION.cff) lists both releases.

## License

Manuscripts, LaTeX source, metadata, and documentation are licensed under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). Verification scripts are licensed under the [MIT License](LICENSES/MIT.txt). See [LICENSE.md](LICENSE.md) for the file-level mapping.
