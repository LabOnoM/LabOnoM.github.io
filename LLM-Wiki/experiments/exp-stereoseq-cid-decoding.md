---
id: exp-stereoseq-cid-decoding
type: experiment
status: verified_primary_screenshots_raw_external
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-08-how-to-encode-barcode-in-stereo-seq.md
  - _posts/PostAttachedFiles/IGV_BAM_Screenshot.png
tags:
  - experiment
  - stereo-seq
  - spatial-transcriptomics
  - cid-barcode
  - mm39
---

# Experiment: BGI Stereo-seq Spatial Coordinate ID (`CID`) Barcode Recovery (`Chip A02598A4`)

## Traceability Links
- **Dataset**: [[ds-a02598a4-barcodetopos-and-bam]]
- **Analysis**: [[ana-st-barcodemap-vs-base4-hallucination]]
- **Figures**: [[fig-stereoseq-igv-ai-github-issue]]
- **Result Summary**: [[res-stereoseq-cid-ground-truth]]

## Experimental & Sequencing Context (Direct Observations)
- **Assay Platform**: BGI STOmics Stereo-seq DNA nanoball (DNB) patterned array (`Chip ID: A02598A4`), processed initially via `SAW` (Stereo-seq Analysis Workflow) to aligned BAM + spatial mask HDF5 (`A02598A4.barcodeToPos.h5`), with paired raw sequencing FASTQs (`E150018299_L01_62_1.fq.gz` / `_2.fq.gz`).
- **Organism, Reference Genome, & Genomic Locus** (established directly from visual inspection of `_posts/PostAttachedFiles/IGV_BAM_Screenshot.png`, not stated in blog prose):
  - **Reference Genome**: **Mouse `mm39` (`GRCm39`)**.
  - **Target Window**: **`chr3:129,503,811-129,504,562`** (`752 bp` window overlapping an exon of **`Egf`**, Epidermal growth factor).
- **Scientific Motivation**: Standard `SAW` BAM files store integer DNB grid coordinates (`Cx:i`, `Cy:i`) and UMI (`UR:Z`) tags on aligned cDNA reads (Read 2) while stripping the original **25-nt ATGC spatial barcode (`CID`)** sequenced on Read 1. Re-running custom alignment or splice-isoform pipelines from raw FASTQ or subsetted BAM regions requires exact bijective mapping between `(Cx, Cy)` integer coordinates in `.barcodeToPos.h5` and 25-nt `ATGC` sequences in Read 1 FASTQ.
