---
id: ana-stardist-visiumhd-binning
type: analysis
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
tags:
  - analysis
  - stardist
  - geopandas
  - scanpy
  - visium-hd
  - leiden
---

# Analysis: StarDist `2D_versatile_he` Segmentation & 2 µm Barcode-to-Nucleus Binning

## Traceability Links
- **Experiment**: [[exp-gse284271-visiumhd-palate]]
- **Dataset**: [[ds-gse284271-pax9ko-2um]]
- **Figures**: [[fig-gse284271-segmentation-and-clustering]]
- **Result Summary**: [[res-gse284271-nuclei-binning]]
- **Flagged Contradictions**: [[contradictions]] (`CON-01`, `CON-02`, `CON-03`)

## Computational Environment & Parameters (Observed from Executed Notebook)
- **Hardware & Runtime**: Executed `2024-10-08 10:57` on Linux with an **NVIDIA GeForce RTX 3090** (22,163 MB usable VRAM via TensorFlow CUDA device `/device:GPU:0`).
- **Python Stack**: `stardist` (`StarDist2D.from_pretrained('2D_versatile_he')`), `csbdeep.utils.normalize`, `tifffile`, `shapely.geometry` (`Polygon`, `Point`, `box`), `geopandas`, `scanpy`, `anndata`, `pandas`, `numpy`.

## Step-by-Step Pipeline Verification
1. **Image Percentile Normalization** (`01.scRNAseq10xVisiumHD.html`, Cell 3):
   - Loads `./240726_VisiumHD/RJ_7_23_24.tif` and scales intensities using `normalize(img, 5, 95)` (5th to 95th percentile).
2. **Tiled StarDist Inference** (Cell 4):
   - Runs `model.predict_instances_big` with `axes='YXC'`, `block_size=4096`, `prob_thresh=0.01`, `nms_thresh=0.001`, `min_overlap=128`, `context=128`, `normalizer=None`, `n_tiles=(4, 4, 1)`.
   - Converts predicted nuclear contours `polys['coord']` into `shapely.geometry.Polygon` instances (`gdf`, indexed `ID_0`, `ID_1`, …; ~120,000+ segmented nuclei across the tissue section).
3. **Spatial Point-in-Polygon Join & Overlap Exclusion** (Cells 9–14):
   - Builds `Point(pxl_col_in_fullres, pxl_row_in_fullres)` geometries for every 2 µm Visium HD capture square (`square_002um`).
   - Executes `gpd.sjoin(gdf_coordinates, gdf, how='left', predicate='within')`.
   - Identifies barcodes falling inside more than one overlapping nuclear polygon (`is_within_polygon['is_overlapping'] = ~is_within_polygon.index.is_unique`) and filters strictly to `~is_overlapping` and `id_right.notnull()`.
4. **Single-Nucleus Count Aggregation & Quality Control Filtering** (Cells 15–21):
   - Sums sparse UMI counts across all uniquely assigned 2 µm bins per nucleus (`groupby('id_right', observed=True)`) to form a nucleus-by-gene `AnnData` object (`19,070` genes) and runs `sc.pp.calculate_qc_metrics(grouped_adata, inplace=True)`.
   - **Observed QC Thresholds**:
     - Nuclear polygon area filter: `adata_area_filtered = grouped_adata[grouped_adata.obs['area'] < 800, :]` (removes large segmentation artifacts/merged clumps extending past 6,000 px²).
     - Total UMI filter: `count_area_filtered_adata = adata_area_filtered[adata_area_filtered.obs['total_counts'] > 200, :]`.
   - **Contradiction Flagged (`CON-02`)**: Markdown prose above Cell 21 states *"In this example, a total UMI cutoff of 100 was chosen"*, whereas Cell 21 code and plot title explicitly enforce **`total_counts > 200`**.
5. **Normalization, Dimensionality Reduction, & Leiden Clustering** (Cells 22–24):
   - `sc.pp.normalize_total(count_area_filtered_adata, inplace=True)`
   - `sc.pp.log1p(count_area_filtered_adata)`
   - `sc.pp.highly_variable_genes(..., flavor="seurat", n_top_genes=2000)`
   - `sc.pp.pca(count_area_filtered_adata)` -> `sc.pp.neighbors(count_area_filtered_adata)` -> `sc.tl.leiden(..., key_added="clusters")` (producing **11 Leiden clusters**, labeled `0` through `10`) and plots spatial cluster assignments over Region of Interest 1 `bbox=(5758, 2664, 6129, 2898)`.
6. **Seurat Spatial Export** (Cells 25–29):
   - Exports nuclear centroids (`centroid_df.txt`), polygon boundary vertices (`boundary_df.txt`), cluster metadata (`merged_df.txt`), and filtered HDF5 (`count_area_filtered_adata.h5`) for downstream R/Seurat v5 spatial visualization.
