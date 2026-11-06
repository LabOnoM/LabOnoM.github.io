---
id: fig-stereoseq-igv-ai-github-issue
type: figure
status: visually_verified
updated_at: 2026-11-06
source_refs:
  - _posts/PostAttachedFiles/IGV_BAM_Screenshot.png
  - _posts/PostAttachedFiles/AI_Response_20250604.png
  - _posts/PostAttachedFiles/GitHub_Issue_20250604.png
tags:
  - figure
  - stereo-seq
  - igv
  - mm39
  - egf
---

# Figures: Stereo-seq IGV Alignment (`mm39` `Egf`), LLM Base-4 Output, & `ST_BarcodeMap` Issue `#2`

## Traceability Links
- **Experiment**: [[exp-stereoseq-cid-decoding]]
- **Dataset**: [[ds-a02598a4-barcodetopos-and-bam]]
- **Analysis**: [[ana-st-barcodemap-vs-base4-hallucination]]
- **Result Summary**: [[res-stereoseq-cid-ground-truth]]

## Visually Inspected Evidence Images
### 1. `_posts/PostAttachedFiles/IGV_BAM_Screenshot.png` (`2,866 × 1,558` px, 32-bit RGBA PNG)
- **Direct Visual Observation**:
  - Desktop Integrative Genomics Viewer (IGV) screenshot loaded with genome **`Mouse (GRCm39/mm39)`** at **`chr3:129,503,811-129,504,562`** (`752 bp`), spanning an exon of RefSeq gene **`Egf`**.
  - Track `A02598A4.Aligned.sortedByCoord.out.merge.q10.dedup.target.bam` displays spliced/exonic RNA-seq coverage and individual reads.
  - Hover tooltip on highlighted read **`E150018299L1C036R00400117279`** explicitly shows:
    - Location: `chr3:129,504,225 - 129,504,324 (-)` (`100M`, `Mapping quality = 255`)
    - Tags: `NH = 1`, `HI = 1`, `AS = 98`, `nM = 0`, **`Cx = 6518`**, **`Cy = 12274`**, **`UR = 6B507`**.
- **Value Added Over Text**: Supplies the exact genome assembly (`GRCm39/mm39`), chromosome interval, target gene (`Egf`), alignment CIGAR (`100M`), and UMI tag (`UR=6B507`), none of which were transcribed into the Markdown text of the blog post.

### 2. `_posts/PostAttachedFiles/AI_Response_20250604.png` (`1,528 × 1,354` px, 32-bit RGBA PNG)
- **Direct Visual Observation**:
  - Screenshot (`2025-06-04`) of an LLM chat response confidently presenting a Python function converting integer `100904410303266` into `ACCGTTACCGGATGAGACAGTAGAG` via `00=A, 01=C, 10=G, 11=T`. Documented as primary evidence of plausible-looking bioinformatics code hallucination when proprietary binary encodings are unverified against raw sequencing reads.

### 3. `_posts/PostAttachedFiles/GitHub_Issue_20250604.png` (`2,248 × 1,334` px, 32-bit RGBA PNG)
- **Direct Visual Observation**:
  - Screenshot of GitHub issue `STOmics/ST_BarcodeMap#2` revealing the `--action 3` CLI flag in `ST_BarcodeMap-0.0.1` for exporting HDF5 `.barcodeToPos.h5` binary matrices directly to text `(barcode, x, y)` tuples.
