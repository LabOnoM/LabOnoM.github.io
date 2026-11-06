---
id: ds-a02598a4-barcodetopos-and-bam
type: dataset
status: metadata_and_screenshots_verified_raw_external
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md
  - _posts/PostAttachedFiles/IGV_BAM_Screenshot.png
tags:
  - dataset
  - stereo-seq
  - hdf5
  - bam
  - fastq
---

# Dataset: Stereo-seq Chip `A02598A4` HDF5 Mask, Aligned BAM, & Paired FASTQ

## Traceability Links
- **Experiment**: [[exp-stereoseq-cid-decoding]]
- **Analysis**: [[ana-st-barcodemap-vs-base4-hallucination]]
- **Figures**: [[fig-stereoseq-igv-ai-github-issue]]
- **Result Summary**: [[res-stereoseq-cid-ground-truth]]

## Verified Specimen & Read-Level Identifiers
Raw sequencing and HDF5 files are external to Git (multi-gigabyte omics files); exact file names, HDF5 tensor shapes, integer values, and read sequences are preserved in `_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md` and `_posts/PostAttachedFiles/IGV_BAM_Screenshot.png`:

1. **Spatial Barcode Mask HDF5**: `A02598A4.barcodeToPos.h5`
   - Contains dataset `/bpMatrix_1` of `uint64` encoded spatial barcodes indexed by `[Cy, Cx, slot]` (or `[y, x, 0]`).
   - Verified coordinate lookup (`_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md#L68-L78`):
     - `bpMatrix_1[12274, 6518, 0] = 100904410303266` (`uint64`).
2. **Aligned Target BAM**: `A02598A4.Aligned.sortedByCoord.out.merge.q10.dedup.target.bam`
   - Verified read from `IGV_BAM_Screenshot.png` at `mm39` `chr3:129,503,811-129,504,562` (`Egf`):
     - **Read Name**: `E150018299L1C036R00400117279`
     - **Alignment**: `chr3:129,504,225-129,504,324` (`100M`, negative strand, `MAPQ = 255`, `NH = 1`)
     - **Spatial & UMI BAM Tags**: `Cx:i:6518`, `Cy:i:12274`, `UR:Z:6B507` (encoded 10-nt UMI).
3. **Paired Raw Read 1 FASTQ**: `E150018299_L01_62_1.fq.gz`
   - Verified raw Read 1 sequence for `E150018299L1C036R00400117279` (`_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md#L114-L120`):
     - Full 35-nt Read 1 (`25-nt CID` + `10-nt UMI`): **`TATAGTACATATGATTCCAGGTCCACGGTCCAACT`**
     - True 25-nt CID prefix (`pos 1–25`): **`TATAGTACATATGATTCCAGGTCCA`**
     - True 10-nt UMI suffix (`pos 26–35`): **`CGGTCCAACT`**.
4. **Backup Status**: External storage location and backup redundancy for `A02598A4.*` and `E150018299_L01_62_*.fq.gz` are **unknown** (not documented in repository).
