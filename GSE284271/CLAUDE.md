# CLAUDE (GSE284271 Analysis Context)

This package contains HTML reports and spatial transcriptomics analysis outputs for Visium HD datasets.

## 1. Analysis Pipeline Context

- **Workflow**:
  - Segment cell nuclei using StarDist2D on H&E stained intestinal tissue images.
  - Nearest-centroid spatial mapping to associate sub-micron Visium HD bins with individual segmented nuclei.
  - Sum gene expressions within cell borders, exporting as HDF5 formats compatible with Scanpy or AnnData.
- **Key Files**:
  - `00.NIH_10xVisiumHD.html`: Preliminary summary and data specifications.
  - `01.scRNAseq10xVisiumHD.html`: Full StarDist segmentation workflow details and Jupyter-rendered analysis.

---

## 2. Standards for Data Reports

- Do not modify raw data matrices or output HTML summaries directly unless replicating the complete Jupyter execution.
- Maintain consistency with downstream single-cell pipelines (Scanpy clustering and visualization).
