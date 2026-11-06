---
name: spatial-omics-visiumhd-stereoseq
description: Domain workflow and verification checks for 10x Genomics Visium HD single-nucleus binning (GSE284271 StarDist + GeoPandas + Scanpy) and BGI Stereo-seq HDF5 CID barcode decoding (ST_BarcodeMap).
---

# Spatial Omics Workflows: Visium HD & Stereo-seq (`spatial-omics-visiumhd-stereoseq`)

Use this project-local skill when working on `GSE284271/` spatial transcriptomics notebooks, Stereo-seq `.barcodeToPos.h5` / BAM barcode recovery (`_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md`), or downstream Scanpy/Seurat spatial analyses in LabOnoM.

## 1. 10x Visium HD Nuclei Segmentation & Custom Binning (`GSE284271`)
- **Biological Context**: `GSE284271` (PMID `40034445`) profiles FFPE murine embryonic secondary palate (`Pax9-/-` vs `WT`, E12.5/E13.5) with 10x Visium HD (`square_002um` bins, `mm10-2020-A` 19,070-gene matrix). Ignore leftover 10x tutorial markdown in `01.scRNAseq10xVisiumHD.html` that mentions "mouse intestinal cells" or "UMI cutoff of 100" (`CON-01`, `CON-02`).
- **Validated Pipeline (`GSE284271/01.scRNAseq10xVisiumHD.html`)**:
  1. Percentile-normalize full-res H&E TIFF (`[5, 95]`) and segment nuclei via StarDist `2D_versatile_he` (`block_size=4096`, `prob_thresh=0.01`, `nms_thresh=0.001`, `min_overlap=128`, `context=128`).
  2. Convert nuclear polygons and 2 µm bin centers (`pxl_col_in_fullres`, `pxl_row_in_fullres`) into `geopandas.GeoDataFrame` objects and run `gpd.sjoin(..., how='left', predicate='within')`.
  3. **Critical QC Step**: Drop bins overlapping multiple nuclear polygons (`~is_unique` on barcode index) before summing gene counts per nucleus (`groupby('id_right')`), then filter `area < 800` and `total_counts > 200`.
  4.Note that `GSE284271/00.NIH_10xVisiumHD.html` is a truncated 117-byte HTML fragment (`CON-03`), and raw `.tif`/`.h5`/`.parquet` inputs reside outside Git.

## 2. BGI Stereo-seq CID-to-ATGC Barcode Decoding
- **Anti-Hallucination Rule**: Never decode `bpMatrix_1` 64-bit unsigned integers in `*.barcodeToPos.h5` via naive 2-bit base-4 arithmetic (`00=A, 01=C, 10=G, 11=T`). In verified test case `A02598A4` (`Cx=6518, Cy=12274`, integer `100904410303266`), naive base-4 yields `ACCGTTACCGGATGAGACAGTAGAG`, which does not exist in raw FASTQ R1 (`TATAGTACATATGATTCCAGGTCCACGGTCCAACT`).
- **Validated Ground-Truth Workflow**:
  1. Build `STOmics/ST_BarcodeMap` (`v0.0.1`) inside an isolated Conda environment pinned to `boost=1.73`, `hdf5=1.10.7`, `zlib=1.2.11` with `CPATH`, `LIBRARY_PATH`, and `-Wl,-rpath,$CONDA_PREFIX/lib`.
  2. Extract the full `(ATGC_25nt, Cx, Cy)` table using undocumented action mode 3 (`STOmics/ST_BarcodeMap#2`):
     ```bash
     ST_BarcodeMap-0.0.1 --in <chip>.barcodeToPos.h5 --out <chip>.barcodes.txt --action 3
     ```
  3. Cross-check decoded 25-nt CIDs against BAM tags (`Cx:i`, `Cy:i`, `UR:Z`) and R1 FASTQ reads before downstream re-alignment.
