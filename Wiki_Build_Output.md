# BSGOU Project Report & Workspace Documentation

This document compiles the structured knowledge base from the BSGOU LLM-Wiki, representing a complete overview of the Bioinformatics Study Group Okayama University (BSGOU) workspace, codebase, and scientific methodologies.

---

## 1. Executive Summary & BSGOU Overview

**BSGOU (Bioinformatics Study Group Okayama University)** is an international community of students, researchers, clinicians, engineers, and industry professionals. The organization is based at Okayama University and focuses on bridging biological data with theoretical models of living systems.

### Mission
BSGOU's mission is to collaboratively tackle complex biological problems, develop open-source tools, and train the next generation of bioinformaticians. It promotes open, reproducible science to turn big data into meaningful, actionable insights.

### Strategic Goals
1. **Foster Interdisciplinary Collaboration**: Uniting clinical knowledge with engineering optimization.
2. **Embrace Systems Biology**: Building multi-scale models of complex biological systems.
3. **Upskill Members**: Providing hands-on tutorials for both computational and wet-lab techniques.
4. **Outreach & Leadership**: Contributing to global standards and ethics in bioinformatics.

---

## 2. Core Values

BSGOU operates under 9 core values, which guide all community, research, and coding contributions:
- **Serve the People**: Prioritizing community needs and public health impact.
- **Theory-Driven Understanding**: Championing mathematical frameworks over simple data accumulation.
- **Transdisciplinary Collaboration**: Breaking silos between wet-lab biology and engineering.
- **Education for Empowerment**: Upskilling members at all levels.
- **Scientific Integrity**: Ensuring strict verification, quality control, and reproducible pipelines.
- **Global Inclusivity**: Maintaining a diverse international network.
- **Open Innovation**: Promoting open source, open data (FAIR principles), and shared repositories.
- **Visionary Leadership**: Preparing the next generation of bioinformatics pioneers.
- **Everyone Can Contribute**: Supporting a culture where all corrections, comments, and pull requests are verified, tracked, and rewarded.

---

## 3. Reconstructed Historical Timeline

Below is the verified timeline of milestones for the BSGOU codebase and public blog releases:
- **2025-05-30** `[verified]`: Launch of the BSGOU public website and publishing of the "About Our Logo" post.
- **2025-06-01** `[verified]`: Publication of the GlycoRNA cell-surface imaging journal club summaries across English, Japanese, and Chinese translations.
- **2025-06-08** `[verified]`: Stereo-seq CID coordinates to ATGC barcode mapping guide published ("From CID to ATGC").
- **2025-06-10** `[verified]`: Publication of the Zebrafish genomic history article detailing duplication events.
- **2025-06-12** `[verified]`: Launch of the Contribution Score Poisson normalization method.
- **2025-06-15** `[verified]`: Mathematical proof of qPCR relative quantitation normalization published, accompanied by Excel and GraphPad Prism templates.
- **2026-06-08** `[verified]`: Repository onboarded to AROS governance, initializing `re_gent` and seeding the LLM-Wiki.

---

## 4. Codebase Components and Workflows

### 4.1 Member Directory Scraper
The directory ranking pipeline consists of a cron workflow and a Python parsing script:
- **GitHub Workflow (`.github/workflows/update_members.yml`)**: Runs daily at 3 AM UTC. Automatically executes the scraper script, commits the updated HTML roster, and uploads build artifacts.
- **Scraper Script (`scripts/fetch_bsgou_members.py`)**:
  - Searches the GitHub API for users with files containing the BSGOU member verification tag.
  - Pulls member contribution counts (Commits, Pull Requests, Issues, Repos) inside the `LabOnoM` organization.
  - Standardizes contributions to a **Contribution Score** using Poisson distribution normalization:
    $$\text{Raw Score} = 5 \times \text{PRs} + 3 \times \text{Issues} + 2 \times \text{Commits} + \text{Repos}$$
    $$\text{Final Score} = 0.5 \times \left(\frac{\text{Raw}}{\text{Max Raw}} \times 100\right) + 0.5 \times \left(100 - \text{Poisson.sf}(\text{Raw}-1, \mu) \times 100\right)$$
  - Renders output to `members.html` and saves raw tables to `members.xlsx`.

### 4.2 Utility Tools
- **`tools/dir-tree.sh`**: Directory tree printer excluding node and site packages.
- **`tools/diff.sh`**: Configurations comparator across development and production environments.
- **`tools/assert-url.js`**: Node.js script that dynamically updates relative image pathways in markdown files to point to raw GitHub URLs, preventing rendering errors.

---

## 5. Scientific Analyses & Cases

### 5.1 Visium HD Nuclei Segmentation (GSE284271)
The data folder `GSE284271/` documents spatial transcriptomics segmentation workflows:
- **Segmentation**: Processes high-resolution H&E stained intestinal tissue using StarDist2D neural network models to segment cell nuclei.
- **Binned Barcode Sorting**: Custom python algorithms map sub-micron Visium HD bins to their nearest nuclei centroids.
- **UMI Summation**: Gene expression matrices are summed within cell boundaries and exported as Seurat/AnnData HDF5 formats for clustering using Scanpy.

### 5.2 qPCR Livak Normalization Proof
We mathematically verify that relative fold-changes under Kenneth Livak's $2^{-\Delta\Delta C_T}$ method are scale-invariant. 

Performing secondary normalization (dividing individual fold-changes by the arithmetic mean of the control group's $2^{-\Delta\Delta C_T}$) yields identical relative fold-changes as dividing raw $2^{-\Delta C_T}$ expression by the control group's mean:

$$ \frac{2^{-\Delta C_{T, X_i}}}{\frac{1}{n} \sum 2^{-\Delta C_{T, C_i}}} = \frac{2^{-\Delta\Delta C_{T, X_i}}}{\frac{1}{n} \sum 2^{-\Delta\Delta C_{T, C_i}}} $$

As a result, statistical parameters ($P$-values, $t$-statistics, and ANOVA $F$-ratios) remain exactly the same, which is verified using the GraphPad Prism sheets (`AM_Calibrator_2DDCt.prism` / `GM_Calibrator_2DDCt.prism`).

### 5.3 Stereo-seq CID Barcode Translation
- **Barcoding Issue**: AI models often suggest simple base-4 modular math conversions for Stereo-seq coordinates, which fail against BAM file sequence reads.
- **Resolution**: Actual sequence mapping requires loading MGI's `saw` mask coordinates (`A02598A4.barcodeToPos.h5`) using `ST_BarcodeMap` tool (action 3).
- **Compilation Lesson**: Compiling `ST_BarcodeMap` requires Boost exactly at version 1.73.0. The workspace makefile was adjusted to link local conda include/lib directories correctly:
  ```makefile
  INCLUDE_DIRS = -I$(DIR_INC) -I$(CONDA_PREFIX)/include -I/usr/include/hdf5/serial
  LIBRARY_DIRS = -L$(CONDA_PREFIX)/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial
  ```

---

## 6. System Engineering and Lessons Learned

- **Jekyll Setup**: Ruby and bundle environments are managed in `codex.yaml` for clean static site previews.
- **Git Push Bypass**: The IDE wrapper dummy token is bypassed during pushes by running `env -u GITHUB_TOKEN git push origin main` to let native system authentication take over.
