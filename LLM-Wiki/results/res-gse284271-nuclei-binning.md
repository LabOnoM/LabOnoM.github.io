---
id: res-gse284271-nuclei-binning
type: result
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - GSE284271/00.NIH_10xVisiumHD.html
tags:
  - result
  - visium-hd
  - stardist
  - pax9ko
  - gse284271
---

# Result Summary: Single-Nucleus Spatial Transcriptomic Resolution in `Pax9KO` Palate (`GSE284271`)

## Complete Traceability Chain
- **Experiment**: [[exp-gse284271-visiumhd-palate]]
- **Dataset**: [[ds-gse284271-pax9ko-2um]]
- **Analysis**: [[ana-stardist-visiumhd-binning]]
- **Figures**: [[fig-gse284271-segmentation-and-clustering]]
- **Contradictions**: [[contradictions]] (`CON-01`, `CON-02`, `CON-03`)

## Verified Quantitative Findings (Observations)
1. **Whole-Slide Nuclear Segmentation Scale**: Pretrained `StarDist2D('2D_versatile_he')` (`prob_thresh=0.01`, `nms_thresh=0.001`, `block_size=4096`) segments `~120,000` candidate nuclear polygons from the percentile-normalized (`[5, 95]`) H&E whole-slide image (`RJ_7_23_24.tif`), with a modal nuclear cross-sectional area of **`120–160` px²** (`GSE284271/01.scRNAseq10xVisiumHD.html`, Cells 4 & 19).
2. **Unambiguous 2 µm Barcode-to-Nucleus Aggregation**: Point-in-polygon spatial joining (`geopandas.sjoin(..., predicate='within')`) followed by strict removal of multi-nucleus overlapping 2 µm barcodes (`~is_overlapping`) and dual QC filtering (**`area < 800` px²** and **`total_counts > 200` UMIs**) produces single-nucleus gene expression profiles across **`19,070` mouse genes** (`mm10-2020-A`) with median nuclear depth around `~1,000–1,200` UMIs (Cells 9–21).
3. **Transcriptomic Cluster Recovery (`11` Leiden Clusters)**: Standard Scanpy log-normalization, 2,000-HVG selection, PCA, neighborhood graph construction, and Leiden clustering resolve **11 clusters (`0`–`10`)** across the `Pax9KO` section. In ROI 1 (`bbox=(5758, 2664, 6129, 2898)`), Cluster `1` dominates the mesenchymal core whereas Clusters `0` and `6` co-localize precisely along the lower-left histological boundary (Cell 24).
4. **Python-to-Seurat Interoperability**: Exporting `centroid_df.txt`, `boundary_df.txt`, `merged_df.txt`, and `count_area_filtered_adata.h5` bridges StarDist/Scanpy custom nuclear binning to R/Seurat spatial polygon visualization (Cells 25–29).

## Scientific Interpretation vs. Limitations
- **Interpretation**: Aggregating 2 µm Visium HD bins inside H&E-derived nuclear polygons avoids chimeric multi-cell square bins in densely packed embryonic craniofacial mesenchyme, enabling cell-resolved spatial clustering in `Pax9-/-` palatal shelves (consistent with published study PMID `40034445`).
- **Limitations & Unresolved Gaps**:
  1. Only cytoplasmic/intranuclear 2 µm bins strictly `within` segmented nuclear masks are summed; extranuclear cytoplasmic transcripts outside nuclear polygons are excluded unless morphological mask expansion is applied.
  2. The exact post-QC cell count (`grouped_adata.n_obs` and `count_area_filtered_adata.n_obs`) was not printed to stdout in `01.scRNAseq10xVisiumHD.html`, and `count_area_filtered_adata.h5` is external to Git.
  3. `GSE284271/00.NIH_10xVisiumHD.html` is a truncated 117-byte file (`CON-03`) and cannot be used as an evidence source.
