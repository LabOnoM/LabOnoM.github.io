---
id: res-stereoseq-cid-ground-truth
type: result
status: verified
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md
  - _posts/PostAttachedFiles/IGV_BAM_Screenshot.png
  - _posts/PostAttachedFiles/GitHub_Issue_20250604.png
tags:
  - result
  - stereo-seq
  - cid-decoding
  - reproducibility
---

# Result Summary: Verified Ground-Truth Recovery of Stereo-seq 25-nt CIDs

## Complete Traceability Chain
- **Experiment**: [[exp-stereoseq-cid-decoding]]
- **Dataset**: [[ds-a02598a4-barcodetopos-and-bam]]
- **Analysis**: [[ana-st-barcodemap-vs-base4-hallucination]]
- **Figures**: [[fig-stereoseq-igv-ai-github-issue]]

## Verified Empirical Result
1. **Single-Read Ground-Truth Match**: For `GRCm39/mm39` `Egf`-aligned read `E150018299L1C036R00400117279` (`Cx=6518, Cy=12274`, `bpMatrix_1[12274, 6518, 0] = 100904410303266`), `ST_BarcodeMap-0.0.1 --action 3` decodes the exact 25-nt CID **`TATAGTACATATGATTCCAGGTCCA`**, matching nucleotides `1–25` of raw Read 1 (`TATAGTACATATGATTCCAGGTCCACGGTCCAACT` in `E150018299_L01_62_1.fq.gz`), whereas naive MSB base-4 decoding (`ACCGTTACCGGATGAGACAGTAGAG`) produces 0 matches across the entire sequencing lane.
2. **Reproducible Build Pin**: Compiling `ST_BarcodeMap-0.0.1` succeeds deterministically under `conda-forge` `boost=1.73`, `hdf5=1.10.7`, and `zlib=1.2.11` with explicit `-Wl,-rpath,$CONDA_PREFIX/lib`.

## Epistemic Lesson
- Never accept unverified bit-packing or coordinate-encoding heuristics from LLM prose or undocumented assumptions; always validate barcode/UMI decoders against paired raw FASTQ reads and BAM alignment tags on at least one concrete read ID before batch processing.
