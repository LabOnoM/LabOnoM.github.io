---
id: fig-gse284271-segmentation-and-clustering
type: figure
status: visually_verified
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
tags:
  - figure
  - visium-hd
  - stardist
  - leiden-clusters
  - histology
---

# Figures: `GSE284271` StarDist Segmentation, QC Distributions, & Spatial Clusters

## Traceability Links
- **Experiment**: [[exp-gse284271-visiumhd-palate]]
- **Dataset**: [[ds-gse284271-pax9ko-2um]]
- **Analysis**: [[ana-stardist-visiumhd-binning]]
- **Result Summary**: [[res-gse284271-nuclei-binning]]

## Embedded Figure Inventory (`GSE284271/01.scRNAseq10xVisiumHD.html`)
All four base64-encoded PNG figures embedded in `01.scRNAseq10xVisiumHD.html` were extracted and visually inspected.

### 1. Embedded Figure 1 (`989 × 320` px, Cell 8): ROI 1 H&E vs. StarDist Masks
- **Direct Visual Observation**:
  - **Left panel (`Region of Interest 1`)**: Cropped H&E brightfield subfield `bbox=(5758, 2664, 6129, 2898)` (`371 × 234` px extent) showing tightly packed hematoxylin-stained (dark purple) embryonic nuclei interspersed with pale circular/ovoid luminal or vacuolar structures and a denser basal/perichondrial layer along the lower-left margin.
  - **Right panel**: Corresponding grey filled polygon masks (~165–180 discrete polygons) predicted by `StarDist2D('2D_versatile_he')`. Individual closely apposed mesenchymal nuclei are cleanly separated into convex polygons, while unstained circular lumens remain unsegmented whitespace.

### 2. Embedded Figure 2 (`1489 × 390` px, Cell 19): Nuclear Area Histograms (`< 800` Cutoff)
- **Direct Visual Observation**:
  - **Left panel (`Nuclei Area`)**: Unfiltered distribution spanning `0` to `>6,000` px². The first two narrow bins (`~0–300` px²) contain `~49,500` and `~46,500` nuclei, followed by `~14,500`, `~5,500`, and `~2,500` nuclei, indicating `~120,000` total segmented nuclear instances across the whole slide with a sparse extreme outlier tail up to `~6,500` px².
  - **Right panel (`Nuclei Area Filtered:800`)**: Zoomed 40-bin histogram post-filtering (`area < 800` px²), showing a smooth unimodal right-skewed nuclear size distribution rising from `~30` px², peaking at **`120–160` px²** (`~9,400` nuclei in the modal bin), and tapering gradually to `<150` nuclei/bin at `800` px².

### 3. Embedded Figure 3 (`1189 × 390` px, Cell 21): Total UMI Boxplots (`> 200` Cutoff)
- **Direct Visual Observation**:
  - **Left panel (`Total Counts`)**: Horizontal boxplot of summed 2 µm bin UMI counts per area-filtered nucleus (`< 800` px²). The interquartile box sits near `~400–2,000` UMIs (median `~1,000–1,200` UMIs, upper whisker `~4,000` UMIs), with high-UMI outlier nuclei extending past `40,000`, `58,000`, `81,500`, and `85,000` UMIs.
  - **Right panel (`Total Counts > 200`)**: Post-filter horizontal boxplot confirming truncation of the low-count tail (`<= 200` UMIs) while preserving the median/IQR body and upper dynamic range (`max ~85,000` UMIs). Confirms the executed threshold is `200`, not `100` (`CON-02`).

### 4. Embedded Figure 4 (`1048 × 333` px, Cell 24): ROI 1 Spatial Leiden Clusters (`0–10`)
- **Direct Visual Observation**:
  - Maps the **11 Leiden transcriptomic clusters (`0`–`10`)** onto the QC-passing nuclear polygons within ROI 1 (`5758:6129, 2664:2898`).
  - **Spatial Organization**: The bulk mesenchymal interior of ROI 1 is overwhelmingly assigned to **Cluster `1`** (olive green, >90% of ROI 1 nuclei). Along the lower-left anatomical boundary (corresponding to the elongated, darker-staining border layer in the H&E panel), **Cluster `0`** (dark red, 5 contiguous elongated nuclei at bottom-left plus 2 scattered upper-right nuclei) and **Cluster `6`** (steel blue, 2 adjacent boundary nuclei at bottom-left) form a spatially coherent lining, while **Cluster `5`** (teal) marks 2 small isolated nuclei.
- **Interpretation**: Custom StarDist nuclear binning preserves sharp single-cell anatomical boundaries at the mesenchymal/epithelial or vascular interface that standard 8 µm or 16 µm square Visium HD grids would blur across neighboring cell types.
