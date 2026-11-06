---
id: manifest-overview
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/scripts/inspectors.py
  - LLM-Wiki/scripts/manifest_ops.py
tags:
  - manifest
  - sha256
  - file-integrity
  - formats
---

# Workspace File Manifest & Format Inspection Overview

Machine-readable ledgers reside alongside this guide:
- `LLM-Wiki/manifest/manifest.jsonl` — Deterministic per-file integrity & format inspection records (sorted by `rel_path`).
- `LLM-Wiki/manifest/manifest.summary.json` — Aggregate counts, format distribution, anomalies, and explicit exclusions.
- `LLM-Wiki/manifest/manifest_history.jsonl` — Append-only ledger retaining superseded `raw_sha256` digests on file modification/deletion.
- `LLM-Wiki/manifest/stale_summaries.json` — Wiki summaries automatically invalidated when cited `source_refs` change.

## 1. Explicit Inspection Status Taxonomy
Every workspace path is classified into an explicit status—never silently skipped:
- `inspected_full`: UTF-8 source code (`.py`, `.js`, `.sh`, `.rb`, `.scss`, `.css`), Markdown (`.md`), configs (`.yml`, `.json`, `.jsonl`, `.xml`, `.svg`), HTML pages, and executed Jupyter HTML notebooks (`GSE284271/01.scRNAseq10xVisiumHD.html`) parsed in full.
- `inspected_visual_and_metadata`: Key scientific figures and screenshots (`9` files, including `IGV_BAM_Screenshot.png`, `Identical_Statistical_Results_qPCR.png`, `Identical_qPCR_Results.png`, `NatureLifeCycleVsLabLifeCycle.png`, `Zebrafish-evolution-and-range.png`, `Software_brief.jpeg`, `Ono_2025.jpg`) both header-parsed and visually examined.
- `inspected_structured`: Binary containers and media whose internal XML/JSON/CSV tables or raster dimensions/frames were parsed (`Example_qPCR.xlsx`, `AM_Calibrator_2DDCt.prism`, `GM_Calibrator_2DDCt.prism`, `Frame_Article.gif`, gallery `.jpg`/`.png`/`.ico` assets).
- `inspected_metadata_only`: Binary font glyph outlines (`.otf`, `.woff`, `.woff2`, `.ttf`, `.eot`) and binary instrument/archive headers (`.RAW`, `.h5`, `.bam`, `.parquet` when present) verified via magic header and full-file SHA-256 without prose extraction.
- `inspected_anomalous`: **`22` workspace files** whose actual byte payload contradicts their file extension (`format_mismatch: true`):
  - `img/gallery/~$Frame_Article.pptx` (`165 B` MS Office owner lock file for `Ziyi Wang`, not a `.pptx` ZIP archive).
  - `GSE284271/00.NIH_10xVisiumHD.html` (`117 B` truncated mid-tag HTML fragment starting with `</script>`).
  - `20` LiteSpeed Web Server `404 Not Found` HTML stubs (`389 B` each) saved under `css/blank.html`, `css/fancy_title_over.html`, `css/fancybox/*.html` (`16`), and `img/glyphicons-halflings*.html` (`2`).
- `unhashed`: `0` | `partial`: `0` | `sampled`: `0` | `unsupported`: `0`.
- `excluded`: Explicitly recorded VCS/cache/symlink/self-referential paths (`.git/`, `Wiki` symlink to `.wiki`, `LLM-Wiki/.cache/`, and `LLM-Wiki/manifest/{manifest.jsonl,manifest.summary.json,manifest_history.jsonl,stale_summaries.json,git_state.json}`).

## 2. Representative Digest Comparison (`raw_sha256` vs. `git_blob_oid`)
| Workspace File | Size (B) | Detected Format | `raw_sha256` (64-hex prefix) | Git Blob SHA-1 (`oid` prefix) |
|---|---:|---|---|---|
| `_posts/PostAttachedFiles/Example_qPCR.xlsx` | `12,068` | `ooxml_xlsx_spreadsheet` | `1da385974f06b6fc...` | `5ecd6ee0877e6a5c...` |
| `_posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism` | `60,093` | `graphpad_prism_zip` | `3b57d3f32af5f8f2...` | `f7e7682e02e1e221...` |
| `_posts/PostAttachedFiles/IGV_BAM_Screenshot.png` | `1,303,246` | `png_image` | `f5fd4acf67f446c1...` | `c6ffdce7ce63b1c8...` |
| `GSE284271/01.scRNAseq10xVisiumHD.html` | `1,412,598` | `jupyter_html_notebook` | `66a77eda32e339df...` | `697eb65a185d7681...` |
| `GSE284271/00.NIH_10xVisiumHD.html` | `117` | `html_truncated_fragment` | `c8ed3597d3a7bade...` | `ae1a383ed11076a0...` |
| `img/gallery/~$Frame_Article.pptx` | `165` | `ms_office_owner_lock` | `8562ed134d9c32e4...` | `16bfa00a3745caa1...` |
| `scripts/fetch_bsgou_members.py` | `6,808` | `python_source` | `6b2eee60b852785a...` | `87cc7180611d841b...` |

> **Epistemic Reminder**: Computing SHA-256 digests and indexing format headers establishes file provenance and tamper/drift detection; it never substitutes for biological, statistical, or experimental validation.
