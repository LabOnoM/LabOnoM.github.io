---
id: exp-gse284271-visiumhd-palate
type: experiment
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - GSE284271/00.NIH_10xVisiumHD.html
  - GSE284271/CLAUDE.md
tags:
  - spatial-transcriptomics
  - visium-hd
  - pax9
  - murine-palate
  - gse284271
---

# Experiment: Murine Embryonic Palate 10x Visium HD Spatial Transcriptomics (`GSE284271`)

## Traceability Links
- **Dataset**: [[ds-gse284271-pax9ko-2um]]
- **Analysis**: [[ana-stardist-visiumhd-binning]]
- **Figures**: [[fig-gse284271-segmentation-and-clustering]]
- **Result Summary**: [[res-gse284271-nuclei-binning]]
- **Flagged Contradictions**: [[contradictions]] (`CON-01`, `CON-02`, `CON-03`)

## Biological & Experimental Design (Direct Observations)
- **GEO Accession & Publication**: `GSE284271` (PMID `40034445`, *"Single Cell Spatial Transcriptomics of the Murine Embryonic Palate Links Pax9 to Patterning and Organization of Extracellular Matrix Components"*, NIH/NIDCR Piña, Raju, D'Souza in collaboration with Okayama University Ziyi Wang and Mitsuaki Ono).
- **Organism & Genome Build**: *Mus musculus*, `mm10-2020-A` reference transcriptome (`10x Visium Mouse Transcriptome Probe Set v2.0`, 19,405 targeted probes; `19,070` detected gene features loaded in `GSE284271/01.scRNAseq10xVisiumHD.html`, starting with `Xkr4` / `ENSMUSG00000051951`).
- **Tissue & Developmental Stages**: Formalin-fixed paraffin-embedded (FFPE) coronal sections of the murine embryonic secondary palate at embryonic days **E12.5** and **E13.5**.
- **Genotypes**: `Pax9-/-` knockout (`Pax9KO`) vs wild-type (`WT`) littermate controls. The notebook executed in this repository specifically processes sample directory `./240726_VisiumHD/analysis/Pax9KO/outs/` paired with full-resolution H&E brightfield micrograph `./240726_VisiumHD/RJ_7_23_24.tif`.
- **Assay Resolution**: 10x Genomics Visium HD spatial gene expression binned at native **2 µm × 2 µm** grid resolution (`binned_outputs/square_002um/`), aggregated computationally into custom single-nucleus polygons segmented from the co-registered H&E image.

## Separation of Observation vs. Legacy Documentation Errors
- **Observed Ground Truth**: Executed code cells in `GSE284271/01.scRNAseq10xVisiumHD.html` (timestamped `2024-10-08 10:57` on an NVIDIA GeForce RTX 3090 24 GB GPU) load `Pax9KO` murine palate paths (`./240726_VisiumHD/RJ_7_23_24.tif` and `./240726_VisiumHD/analysis/Pax9KO/outs/binned_outputs/square_002um/filtered_feature_bc_matrix.h5`).
- **Contradiction Flagged (`CON-01`)**: Unedited 10x Genomics tutorial boilerplate in the introductory Markdown cell of `01.scRNAseq10xVisiumHD.html` mentions *"mouse intestinal cells"*, which caused legacy `.wiki/entities/gse284271.md`, `GSE284271/CLAUDE.md:9`, and `Wiki_Build_Output.md:74` to misattribute this study to mouse intestine rather than embryonic secondary palate.
- **Missing / External Evidence**: Raw TIFF imagery (`RJ_7_23_24.tif`), Space Ranger HDF5 count matrices (`filtered_feature_bc_matrix.h5`), `tissue_positions.parquet`, and downstream exported tables (`centroid_df.txt`, `boundary_df.txt`, `merged_df.txt`, `count_area_filtered_adata.h5`) are external to Git; backup arrangements for `./240726_VisiumHD/` are **unknown** (not recorded in workspace documentation).
