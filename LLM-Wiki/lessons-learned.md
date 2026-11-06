---
id: lessons-learned
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - AGENTS.md
tags:
  - lessons-learned
  - reproducibility
  - bioinformatics
  - engineering
---

# Lessons Learned (Verified Engineering & Scientific Practice)

## 1. Biomedical & Bioinformatics Verification Lessons
1. **Verify Executed Code Over Inherited Notebook Prose (`GSE284271`)**:
   - Research notebooks adapted from vendor tutorials frequently retain stale markdown descriptions (e.g., *"mouse intestinal cells"* and *"UMI cutoff of 100"* in `GSE284271/01.scRNAseq10xVisiumHD.html` when actual code runs `Pax9KO` embryonic palate with `total_counts > 200`). Always audit executed code cells, file paths, and plot axes rather than prose cells alone.
2. **Validate Binary Omics Encodings Against Raw Sequencing Reads (`Stereo-seq`)**:
   - Proprietary spatial barcode masks (`*.barcodeToPos.h5` `bpMatrix_1`) do not necessarily follow textbook MSB-first 2-bit base-4 encoding. Always verify at least one concrete read (`Cx, Cy, UR` in BAM vs. Read 1 FASTQ) using the vendor's reference C++ decoder (`ST_BarcodeMap --action 3`).
3. **Test qPCR Hypotheses in Log/Cycle Space ($\Delta C_T$), Not Linear $2^{-\Delta\Delta C_T}$ Space**:
   - While arithmetic-mean (`AM`) and Livak (`GM`) calibrators differ only by a positive scalar $c > 0$ (leaving $t$, $F$, $R^2$, and Mann–Whitney $U$ unchanged), exponentiation turns additive cycle variance into extreme log-normal heteroscedasticity (`F(3,3) = 1451` in `Example_qPCR.xlsx`), masking true biological effects (`P = 0.1143` linear vs. `P = 0.0098` on $\Delta C_T$).
4. **Inspect Container Internals & Magic Bytes**:
   - File extensions can mislead: `~$Frame_Article.pptx` (`165 B`) is an MS Office lock file, `00.NIH_10xVisiumHD.html` (`117 B`) is a truncated HTML fragment, `css/fancybox/*.html` (`389 B`) are LiteSpeed 404 stubs, and `.prism` files (Prism >= 9.4 / 10) are structured ZIP archives containing `document.json`, `data.csv`, and `results.json`.

## 2. Repository & Agent Engineering Lessons
5. **Isolate Ruby/Jekyll Toolchains on macOS**:
   - macOS system Ruby (`2.6.10`) cannot install `ffi >= 1.17` required by current `Gemfile` gems (`ruby >= 3.0`). Provisioning an isolated `conda-forge` `ruby=3.2` + local scratch `BUNDLE_PATH` builds `Jekyll 4.2.2` cleanly in ~2.2 s without touching system gems or polluting the repository root.
6. **Prevent Self-Referential Manifest Loops**:
   - Any file-integrity manifest (`manifest.jsonl`) must explicitly exclude itself and disposable index caches (`LLM-Wiki/.cache/`) so repeated verification runs remain strictly idempotent (`zero_diff: true`).
7. **Respect Root `README.md` Dual Routing in Jekyll**:
   - In `LabOnoM.github.io`, `README.md` has YAML front matter (`layout: default`) and serves `/README.html`. Edits to `README.md` must remain valid Kramdown/HTML and preserve existing strategic plan content.
