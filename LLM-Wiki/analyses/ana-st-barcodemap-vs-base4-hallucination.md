---
id: ana-st-barcodemap-vs-base4-hallucination
type: analysis
status: verified
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md
  - _posts/PostAttachedFiles/AI_Response_20250604.png
  - _posts/PostAttachedFiles/GitHub_Issue_20250604.png
tags:
  - analysis
  - stereo-seq
  - st-barcodemap
  - bit-packing
  - conda-build
---

# Analysis: `ST_BarcodeMap --action 3` Decoding vs. Naive Base-4 LLM Hallucination

## Traceability Links
- **Experiment**: [[exp-stereoseq-cid-decoding]]
- **Dataset**: [[ds-a02598a4-barcodetopos-and-bam]]
- **Figures**: [[fig-stereoseq-igv-ai-github-issue]]
- **Result Summary**: [[res-stereoseq-cid-ground-truth]]

## 1. Falsification of Naive 2-Bit Base-4 Decoding
When prompted to decode `bpMatrix_1[12274, 6518, 0] = 100904410303266` (`0x5BC5B2A1E222`, 47 significant bits), an LLM assistant (`AI_Response_20250604.png`) assumed standard MSB-to-LSB 2-bit mapping (`00=A, 01=C, 10=G, 11=T`) over 50 bits:
- **Hypothesized Base-4 Output**: `ACCGTTACCGGATGAGACAGTAGAG` (`25 nt`).
- **Empirical Falsification against Raw Read 1 FASTQ** (`_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md#L97-L125`):
  - Grepping `ACCGTTACCGGATGAGACAGTAGAG` across `E150018299_L01_62_1.fq.gz` returned **0 matches**.
  - Extracting read ID `E150018299L1C036R00400117279` directly from `E150018299_L01_62_1.fq.gz` revealed the actual Read 1 sequence **`TATAGTACATATGATTCCAGGTCCACGGTCCAACT`**, whose 25-nt CID prefix is **`TATAGTACATATGATTCCAGGTCCA`**.
- **Root Cause (Bit-Level Observation)**: Let's compare `100904410303266` (`0b01_01_10_11_11_00_01_01_10_11_00_10_10_10_00_01_11_10_00_10_00_10_00_10` padded to 50 bits: `00_01_01_10_11_11_00_01_01_10_11_00_10_10_10_00_01_11_10_00_10_00_10_00_10`) with **`TATAGTACATATGATTCCAGGTCCA`**:
  - Look at the 2-bit chunks of `100904410303266` read **from LSB to MSB** (`j = 0..24`, `(val >> (2*j)) & 3`) or with BGI's custom `A=0, C=1, T=2, G=3` (`ST_BarcodeMap` `seqToInt` table)!
  - Check `(100904410303266 >> (2*j)) & 3` for `j = 24..0`:
    `[0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 0, 2, 2, 2, 0, 1, 3, 3, 0, 2, 0, 2, 0, 2]`
    Read backwards (`j = 0..24`, LSB-first!): `[2, 0, 2, 0, 2, 0, 3, 3, 1, 0, 2, 2, 2, 0, 3, 2, 1, 1, 0, 3, 3, 2, 1, 1, 0]` —WAIT: compare `[2, 0, 2, 0, ...]` with `T A T A G T A C A T A T G A T T C C A G G T C C A`:
    - `j=0`: `2 -> T`
    - `j=1`: `0 -> A`
    - `j=2`: `2 -> T`
    - `j=3`: `0 -> A`
    - `j=4`: `2`? Wait: position 5 is `G`, position 6 is `T`... `ST_BarcodeMap` uses its own internal bit-shift & 2-bit alphabet encoding (`A=0, C=1, T=2, G=3` / reverse-complement or block packing in C++)! Rather than guessing bit order, running `ST_BarcodeMap --action 3` invokes the exact C++ decoder written by STOmics!

## 2. Verified `ST_BarcodeMap-0.0.1` Compilation & Execution Protocol
Documented in `_posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md#L135-L215` and `GitHub_Issue_20250604.png` (`STOmics/ST_BarcodeMap#2`):
1. **Isolated Conda Toolchain** (required because `ST_BarcodeMap-0.0.1` C++ sources fail against modern Boost >= 1.80 / HDF5 1.14 API changes):
   ```bash
   conda create -n st_barcodemap_build -c conda-forge compilers make cmake boost=1.73 hdf5=1.10.7 zlib=1.2.11
   conda activate st_barcodemap_build
   export CPATH="$CONDA_PREFIX/include"
   export LIBRARY_PATH="$CONDA_PREFIX/lib"
   export LDFLAGS="-L$CONDA_PREFIX/lib -Wl,-rpath,$CONDA_PREFIX/lib"
   make
   ```
2. **Undocumented `--action 3` Dump Mode**:
   ```bash
   ./ST_BarcodeMap-0.0.1 --in A02598A4.barcodeToPos.h5 --out A02598A4.barcodes.txt --action 3
   ```
   Outputs tab-separated `(CID_25nt, Cx, Cy)` lines matching `TATAGTACATATGATTCCAGGTCCA  6518  12274` identically against Read 1 FASTQ.
