# PIPELINE REGISTRY

This registry tracks the computational and laboratory pipelines of the Bioinformatics Study Group Okayama University (BSGOU) workspace.

| Pipeline | Directory / File | Description | Target Workflows / Tools | Status |
|---|---|---|---|---|
| Member Directory Scraper | `scripts/fetch_bsgou_members.py` | Scrapes GitHub contribution data (commits, PRs, issues, repos) for BSGOU members, calculates ranks using Poisson normalization, and generates member lists. | `.github/workflows/update_members.yml` | Active |
| Stereo-seq CID Translation | `ST_BarcodeMap` (compiled locally/CI) | Converts Stereo-seq spatial transcriptomics coordinate IDs (CID) into ATGC genomic sequences. | `ST_BarcodeMap-0.0.1` | Compiled |
| Visium HD Nuclei Segmentation | `GSE284271/01.scRNAseq10xVisiumHD.html` | StarDist-based nuclei segmentation and custom spatial binning pipeline for Visium HD tissue images. | StarDist / Scanpy / AnnData | Complete |
| qPCR Livak calculation | `_posts/PostAttachedFiles/` | $\Delta\Delta C_T$ fold-change calculations and GraphPad Prism templates comparing arithmetic and geometric normalization. | `Example_qPCR.xlsx`, `*.prism` | Complete |
