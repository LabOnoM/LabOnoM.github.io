---
id: contradictions
type: governance
status: active_verified_ledger
updated_at: 2026-11-06
source_refs:
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - GSE284271/00.NIH_10xVisiumHD.html
  - GSE284271/CLAUDE.md
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
  - _posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism
  - _posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism
  - _posts/2025-06-12-BSGOU-Contribution-Score.md
  - scripts/fetch_bsgou_members.py
  - .wiki/entities/glycorna-imaging.md
  - .wiki/entities/zebrafish-history.md
  - 00.RawData/PIPELINE_REGISTRY.md
  - CODE_MAP.md
tags:
  - contradictions
  - audit
  - missing-evidence
  - format-anomalies
---

# Contradictions, Discrepancies, & Missing-Evidence Ledger

All discrepancies below were identified by cross-checking prose claims and legacy `.wiki/` summaries directly against executed code, spreadsheet formulas, `.prism` JSON archives, and raw image/binary headers. Originals have been preserved untouched per repository rules.

## 1. Scientific & Analytical Contradictions

### `CON-01` — `GSE284271` Tissue Misattributed to "Mouse Intestine" Instead of Murine Embryonic Secondary Palate
- **Conflicting Claims**:
  - Legacy `.wiki/entities/gse284271.md`, `GSE284271/CLAUDE.md#L9`, `Wiki_Build_Output.md#L74`, and unedited 10x tutorial boilerplate in `GSE284271/01.scRNAseq10xVisiumHD.html` state the dataset profiles **mouse intestinal tissue**.
- **Primary Evidence**:
  - Executed Python cells in `GSE284271/01.scRNAseq10xVisiumHD.html` (Cells 2 & 9) load `./240726_VisiumHD/RJ_7_23_24.tif` and `./240726_VisiumHD/analysis/Pax9KO/outs/binned_outputs/square_002um/filtered_feature_bc_matrix.h5`.
  - Public NCBI GEO record `GSE284271` (PMID `40034445`) confirms these samples are **FFPE embryonic murine secondary palate (`Pax9-/-` vs `WT`, E12.5/E13.5)**, not intestine.
  - See [[exp-gse284271-visiumhd-palate]].

### `CON-02` — `GSE284271` Total UMI Cutoff (`100` in Prose vs. `> 200` in Executed Code)
- **Conflicting Claims**:
  - Markdown narrative above Cell 21 in `GSE284271/01.scRNAseq10xVisiumHD.html` states: *"In this example, a total UMI cutoff of 100 was chosen."*
- **Primary Evidence**:
  - Executed Cell 21 code and Embedded Figure 3 (`Total Counts > 200`) filter strictly with `adata_area_filtered[adata_area_filtered.obs['total_counts'] > 200, :]`.
  - See [[ana-stardist-visiumhd-binning]].

### `CON-03` — `GSE284271/00.NIH_10xVisiumHD.html` Is a 117-Byte Truncated HTML Fragment
- **Conflicting Claims**:
  - `GSE284271/CLAUDE.md#L14` describes `00.NIH_10xVisiumHD.html` as a primary NIH Visium HD reference report.
- **Primary Evidence**:
  - `GSE284271/00.NIH_10xVisiumHD.html` is exactly **`117` bytes** (`raw_sha256: 294fd9cc...`) beginning mid-tag with `</script><meta name="viewport" content="user-scalable=no, initial-scale=1.0">` and containing zero code, text, or figures.

### `CON-04` — qPCR GraphPad Prism Variance $F$-Test Misdescribed as ANOVA & Linear-vs-Log Testing Mismatch
- **Conflicting Claims**:
  - `_posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md#L221-L240` and `Wiki_Build_Output.md#L85` claim `AM_Calibrator_2DDCt.prism` and `GM_Calibrator_2DDCt.prism` verify **ANOVA $F$-ratios** and recommend testing in $\Delta C_T$ / $\Delta\Delta C_T$ log space before $2^{-x}$ transformation.
- **Primary Evidence**:
  - Parsing `analyses/*/results.json` inside both `.prism` ZIP containers proves **no ANOVA sheet exists**. Both files run two-group Unpaired $t$-test (`t = 1.847`, `df = 6`, `P = 0.1143`) + **Snedecor's variance-homogeneity $F$-test (`F(3,3) = 1451`, `P = 0.0000614`)** + Mann–Whitney (`U = 1`, `P = 0.0571`) on **linear exponentiated $2^{-\Delta\Delta C_T}$ values**, where outlier well `C6` (`180.74x`) causes 1,451-fold variance inflation. Testing directly on $\Delta C_T$ gives `t = 3.721`, `df = 6`, `P = 0.00984` with homogeneous variance (`F(3,3) = 1.85`).
  - See [[ana-livak-2ddct-am-vs-gm]].

### `CON-05` — BSGOU Contribution Score Weights (`0.3 / 0.7` in Post vs. `0.5 / 0.5` in Production Code)
- **Conflicting Claims**:
  - `_posts/2025-06-12-BSGOU-Contribution-Score.md#L395` defines `Final Score = 0.3 * Linear + 0.7 * Poisson`.
- **Primary Evidence**:
  - `scripts/fetch_bsgou_members.py#L143-L148` computes `Raw = 5*PRs + 3*Issues + 2*Commits + Repos`, `Poisson = 100 - stats.poisson.sf(Raw - 1, mu=lambda_) * 100`, and `Final = 0.5 * Linear + 0.5 * Poisson`, which exactly reproduces `wong-ziyi`'s live score (`0.5*100 + 0.5*49.8117 = 74.91`) in `members.html` (whereas `0.3 / 0.7` would yield `64.87`). Also note `/repos/.../issues` (`L127`) double-counts PRs unless filtered.
  - See [[ana-bsgou-contribution-score]].

### `CON-06` — Legacy `.wiki/entities/glycorna-imaging.md` Hallucinates Metabolic Azide Click-Chemistry
- **Conflicting Claims**:
  - `.wiki/entities/glycorna-imaging.md` claims the 2025-06-01 journal club reviews metabolic labeling with clickable azide sugars (`Ac4ManNAz`) and copper-free click chemistry.
- **Primary Evidence**:
  - `_posts/2025-06-01-journal-club-glycorna-imaging.{en,jp,zh}.md` reviews **ARPLA** (Ma *et al.*, *Nat Biotechnol* 2024, PMID `37217750`), which uses a **label-free Neu5Ac DNA aptamer + sequence-specific RISH probe + T4 DNA ligase + phi29 RCA**, explicitly citing metabolic azide/click labeling as the *prior limitation* ARPLA replaces.
  - See [[ana-glycorna-arpla-journal-club]].

### `CON-07` — Legacy `.wiki/entities/zebrafish-history.md` Hallucinates TSGD & Spatial Omics Content in History Post
- **Conflicting Claims**:
  - `.wiki/entities/zebrafish-history.md` attributes teleost-specific genome duplication (`TSGD`) and Stereo-seq/Visium profiling to `_posts/2025-06-10-zebrafish-history.md`.
- **Primary Evidence**:
  - `_posts/2025-06-10-zebrafish-history.md` covers 1822 taxonomy, Streisinger `AB` cloning, Driever/Nüsslein-Volhard ENU screens, optical neurobiology, and `Soyuz 21` / `Shenzhou 18` spaceflight (`4` zebrafish, `43` days, `1.2 L`), with zero mention of `TSGD` or spatial transcriptomics (`TSGD` appears instead in `index.html#L348` for `Mun_2024.jpg`).
  - See [[ana-zebrafish-model-and-spaceflight]].

---

## 2. Infrastructure, Governance, & File-Format Anomalies

### `CON-08` — Stale GitHub Actions References After `2026-10-13` Manual-CI Policy
- **Conflicting Claims**:
  - `00.RawData/PIPELINE_REGISTRY.md#L7` lists `.github/workflows/update_members.yml` as `Active`, and `sources/Global_Inclusivity.md` references developing GitHub Actions workflows.
- **Primary Evidence**:
  - Commit `b5eedef631ca7b102cccf9a32896468ded9b3501` (`2026-10-13`) deleted `.github/workflows/update_members.yml` and established the strict no-GitHub-Actions rule in `AGENTS.md#L24-L35`, `CLAUDE.md#L39-L50`, and `README.md#L127-L133`.

### `CON-09` — Format Mismatches, Stale `/home/ubuntu4/` Paths, & Theme Leftovers
1. **`img/gallery/~$Frame_Article.pptx` (`165` bytes)**: Tracked MS Office temporary owner lock file (`Ziyi Wang`), **not** a valid OOXML `.pptx` ZIP presentation (`Frame_Article.pptx` itself is absent; animated `img/gallery/Frame_Article.gif` is tracked).
2. **`20` LiteSpeed `404 Not Found` HTML Stubs (`389` bytes each)**: `css/blank.html`, `css/fancy_title_over.html`, `css/fancybox/*.html` (`16` files), and `img/glyphicons-halflings*.html` (`2` files) are scraped LiteSpeed Web Server 404 error pages rather than valid UI assets.
3. **Legacy `tools/` & `CODE_MAP.md` Paths**: `tools/assert-url.js` and `tools/diff.sh` hardcode upstream `jekyll-TeXt-theme` directories (`./test/_posts`, `./docs/en`) absent from this repository; `CODE_MAP.md` previously contained hardcoded `/home/ubuntu4/GitHub/...` links (remediated in `CODE_MAP.md` and `LLM-Wiki/code-map.md`).
