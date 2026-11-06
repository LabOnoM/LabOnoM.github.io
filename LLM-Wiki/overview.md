---
id: overview
type: overview
status: verified
updated_at: 2026-11-06
source_refs:
  - README.md
  - index.html
  - journalclub.md
  - _config.yml
tags:
  - bsgou
  - labonom
  - overview
  - portfolio
---

# Project Overview: BSGOU (`LabOnoM.github.io`)

## 1. Mission & Institutional Identity
`LabOnoM.github.io` is the multilingual (`EN` / `JP` / `ZH`) web portal, technical blog, community contribution tracker, and open-science dissemination hub for the **Bioinformatics Study Group in Okayama University (`BSGOU`)**, affiliated with **LabOnoM** (Mitsuaki Ono Laboratory, Okayama University Graduate School of Medicine, Dentistry and Pharmaceutical Sciences).

BSGOU unites wet-lab biologists, clinicians/dentists, bioinformaticians, students, and software engineers to bridge high-throughput spatial/single-cell multi-omics with quantitative biological theory (`README.md#L21-L86`, `sources/*.md`).

## 2. Core Functional Pillars in This Repository
1. **Multilingual Community Portal (`index.html`, `README*.md`, `sources/*.md`, `journalclub.md`)**:
   - Presents BSGOU's 9 core values (`sources/`), strategic roadmap (`README.md`, `README_JP.md`, `README_CH.md`), interactive glassmorphic landing page (`js/custom.js`, `css/style.css`), and multilingual journal club archive.
2. **Primary Reproducible Method & Benchmark Case Studies (`GSE284271/`, `_posts/`, `_posts/PostAttachedFiles/`)**:
   - **Visium HD Craniofacial Spatial Transcriptomics** ([[res-gse284271-nuclei-binning]]): StarDist `2D_versatile_he` single-nucleus segmentation and 2 µm bin aggregation on `Pax9-/-` murine embryonic secondary palate (`GSE284271`, PMID `40034445`).
   - **qPCR $2^{-\Delta\Delta C_T}$ Scale-Invariance & Biostatistics** ([[res-qpcr-normalization-equivalence]]): Exact Excel (`Example_qPCR.xlsx`) and GraphPad Prism 10 (`AM`/`GM` `.prism`) demonstration of calibrator proportionality and log-vs-linear statistical testing pitfalls.
   - **BGI Stereo-seq `CID` Barcode Recovery** ([[res-stereoseq-cid-ground-truth]]): Empirical falsification of naive base-4 decoding and verified `ST_BarcodeMap --action 3` HDF5-to-ATGC extraction on `GRCm39/mm39` `Egf` (`Chip A02598A4`).
   - **Literature & Epistemology Reviews**: GlycoRNA single-cell `ARPLA` proximity ligation imaging ([[ana-glycorna-arpla-journal-club]]), zebrafish developmental genetics & `Shenzhou 18` orbital ecosystem ([[ana-zebrafish-model-and-spaceflight]]), and single-cell `UMAP`/`t-SNE` manifold distortion critique ([[ana-elephant-in-the-algorithm]]).
3. **Manual Community Contribution Scoring (`scripts/fetch_bsgou_members.py`, `scripts/update-members.sh`, `members.html`)**:
   - Queries `LabOnoM` GitHub repositories and ranks contributors using a hybrid Linear + Poisson survival-function normalization ([[ana-bsgou-contribution-score]]), run manually by the owner without GitHub Actions (`AGENTS.md#L24-L35`).

## 3. Verified Research Gallery Publications (`index.html#L285-L370`)
The landing-page carousel links LabOnoM's peer-reviewed skeletal, craniofacial, spatial transcriptomic, and regenerative biology studies, including PMIDs `40034445` (`GSE284271` embryonic palate Visium HD), `40140451`, `40080674`, `39990519`, `39710093`, `39405562`, `39086598` (`Mun_2024.jpg` zebrafish `mstnb`/TSGD), `38925474`, `37683603`, and `30413886`.
