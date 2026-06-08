# Entity: Stereo-seq Barcoding

This page documents the translation of Stereo-seq coordinate identifiers (CID) to genomic DNA barcodes (ATGC).

## The AI Hallucination Warning
- **The Issue**: AI assistants often explain that CID numbers are base-4 encodings ($A=0, C=1, G=2, T=3$) of DNA sequences and provide simple modulo-4 python scripts.
- **The Reality**: This base-4 conversion does not match actual reads from the BAM files.
- **The Correction**: The official conversion requires MGI's `saw` software mask mapping files (`A02598A4.barcodeToPos.h5`) processed via `ST_BarcodeMap` tool (action 3).

## Compilation Walkthrough
Compiling the C++ barcode mapper `ST_BarcodeMap` requires setting up specific system library versions:
- `gcc`
- `boost == 1.73.0` (Note: version must be exactly 1.73.0, newer versions introduce syntax incompatibilities)
- `hdf5 >= 1.10.7`
- `zlib >= 1.2.11`

### Custom Makefile Pattern
Since local compilation fails to resolve conda prefixes automatically, the makefile was adjusted to link dependencies via the active conda environment variables:
```makefile
INCLUDE_DIRS = -I$(DIR_INC) -I$(CONDA_PREFIX)/include -I/usr/include/hdf5/serial
LIBRARY_DIRS = -L$(CONDA_PREFIX)/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial
```
This is fully detailed in [[lessons-learned]].
