---
id: ds-gse284271-pax9ko-2um
type: dataset
status: metadata_and_notebook_verified_raw_external
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - GSE284271/00.NIH_10xVisiumHD.html
tags:
  - dataset
  - visium-hd
  - pax9ko
  - stardist
  - gse284271
---

# Dataset: `GSE284271` `Pax9KO` 2 µm Visium HD & H&E Artifacts

## Traceability Links
- **Experiment**: [[exp-gse284271-visiumhd-palate]]
- **Analysis**: [[ana-stardist-visiumhd-binning]]
- **Figures**: [[fig-gse284271-segmentation-and-clustering]]
- **Result Summary**: [[res-gse284271-nuclei-binning]]

## In-Repository Artifacts (Full-File Inspected & Hashed)
| Workspace Path | Size | Format Inspection | Status & Findings |
|---|---:|---|---|
| `GSE284271/01.scRNAseq10xVisiumHD.html` | 1,412,598 B | `jupyter_html_notebook` (29 code cells, 4 embedded base64 PNGs) | `inspected_full` — Complete executed Python/Scanpy/StarDist report (`2024-10-08`). |
| `GSE284271/00.NIH_10xVisiumHD.html` | 117 B | `html_truncated_fragment` (`</script><meta name="viewport"...`) | `inspected_anomalous` — Truncated mid-tag HTML fragment lacking code or data (`CON-03`). |
| `GSE284271/CLAUDE.md` | 917 B | `markdown_document` | `inspected_full` — Local context guide (contains inherited intestinal tissue & `00.NIH` errors). |

## External Input & Output Files Referenced by Executed Code
The following files were read or written during the `2024-10-08` execution recorded in `GSE284271/01.scRNAseq10xVisiumHD.html` (Cells 2, 5, 9, 25–29) and are **not tracked in Git**:

1. **Brightfield Histology Input**:
   - `./240726_VisiumHD/RJ_7_23_24.tif` — High-resolution H&E whole-slide TIFF image normalized across percentiles `[5, 95]` (`min_percentile=5`, `max_percentile=95`) prior to StarDist inference.
2. **Space Ranger 2 µm Spatial Count Inputs**:
   - `./240726_VisiumHD/analysis/Pax9KO/outs/binned_outputs/square_002um/filtered_feature_bc_matrix.h5` — 10x HDF5 count matrix containing **`19,070` mouse genes** (`var_names` starting with `Xkr4` / `ENSMUSG00000051951`, `Gm1992`, `Gm19938`, `Rp1`, `Sox17`; `genome = mm10`).
   - `./240726_VisiumHD/analysis/Pax9KO/outs/binned_outputs/square_002um/spatial/tissue_positions.parquet` — Spatial barcode coordinates (`in_tissue`, `array_row`, `array_col`, `pxl_row_in_fullres`, `pxl_col_in_fullres`; first barcode `s_002um_00000_00000-1` at pixel `(2381.95, 19572.64)`).
3. **Intermediate & Seurat Interop Outputs**:
   - `./240726_VisiumHD/stardist/nuclei_polys.pkl` — Pickled StarDist polygon coordinates.
   - `./240726_VisiumHD/Pax9KO_241007/centroid_df.txt` — Per-nucleus centroid coordinates (`cell`, `x`, `y`) for `Seurat::ReadVizgen` / `LoadXenium`-style FOV construction.
   - `./240726_VisiumHD/Pax9KO_241007/boundary_df.txt` — Per-nucleus polygon vertices (`cell`, `x`, `y`) for Seurat segmentation boundaries.
   - `./240726_VisiumHD/Pax9KO_241007/merged_df.txt` — Combined nucleus metadata and Leiden cluster assignments.
   - `./240726_VisiumHD/Pax9KO_241007/count_area_filtered_adata.h5` — Filtered single-nucleus AnnData HDF5 matrix (`area < 800` px² and `total_counts > 200` UMIs).
