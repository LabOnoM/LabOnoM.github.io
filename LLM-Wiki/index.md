---
id: index
type: governance
status: canonical
updated_at: 2026-11-15
source_refs:
  - LLM-Wiki/SCHEMA.md
  - LLM-Wiki/STATE.md
tags:
  - index
  - navigation
  - karpathy-llm-wiki
---

# `LLM-Wiki` Master Knowledge Index (`LabOnoM.github.io`)

Canonical entry catalog for the BSGOU / LabOnoM persistent project memory system. Read [[STATE]] first on startup, then follow links below or run `python3 LLM-Wiki/scripts/wiki_cli.py search "<query>"`.

## 1. Core Orientation & Durable Memory
- [README.md](README.md) — Quick-start guide, workflow architecture diagram, setup, and verified CLI commands.
- [STATE.md](STATE.md) — Concise live dashboard: active branch/commit, manifest integrity counts, flagged contradictions, and next actions.
- [SCHEMA.md](SCHEMA.md) — Three-layer LLM-Wiki conventions, `source_refs` invalidation schema, and observation-vs-interpretation rules.
- [overview.md](overview.md) — BSGOU & LabOnoM mission, multilingual web portal, and research gallery PMIDs.
- [code-map.md](code-map.md) — Verified repository directory topology, Jekyll pipeline, Python scripts, and `wiki_cli.py` modules.
- [git-state.md](git-state.md) — Repository/worktree identity, `raw_sha256` vs. Git blob SHA-1 vs. Commit SHA separation, and untracked data backup status.
- [log.md](log.md) — Append-only chronological activity and validation ledger.

## 2. Linked Scientific Traceability Chains (`Experiment -> Dataset -> Analysis -> Figure -> Result`)

### Chain A — Murine Embryonic Palate 10x Visium HD (`GSE284271` / `Pax9KO`, PMID `40034445`)
- **Experiment**: [exp-gse284271-visiumhd-palate](experiments/exp-gse284271-visiumhd-palate.md) — E12.5/E13.5 `Pax9-/-` vs `WT` FFPE secondary palate (`mm10-2020-A`, `19,070` genes).
- **Dataset**: [ds-gse284271-pax9ko-2um](datasets/ds-gse284271-pax9ko-2um.md) — Executed 29-cell notebook (`1.41 MB`), 117 B truncated `00.NIH` fragment, and external 2 µm Space Ranger / H&E inputs.
- **Analysis**: [ana-stardist-visiumhd-binning](analyses/ana-stardist-visiumhd-binning.md) — StarDist `2D_versatile_he` segmentation, `geopandas.sjoin` overlap filtering, `area < 800` & `total_counts > 200` QC, and Scanpy Leiden clustering.
- **Figures**: [fig-gse284271-segmentation-and-clustering](figures/fig-gse284271-segmentation-and-clustering.md) — Visually verified ROI 1 masks, ~120k-nucleus area histograms, UMI boxplots, and 11 spatial clusters.
- **Result**: [res-gse284271-nuclei-binning](results/res-gse284271-nuclei-binning.md) — Single-nucleus resolution at palatal mesenchymal boundaries and Seurat v5 export.

### Chain B — Comparative RT-qPCR $2^{-\Delta\Delta C_T}$ Scale-Invariance & Biostatistics (`WT` vs `KO`, $n=4$)
- **Experiment**: [exp-qpcr-wt-vs-ko](experiments/exp-qpcr-wt-vs-ko.md) — Well-level `Ref` and `Target` $C_T$ measurements across `WT` (`A1–A4`) and `KO` (`C5–C8`), highlighting `C6` reference delay.
- **Dataset**: [ds-example-qpcr-xlsx-and-prism](datasets/ds-example-qpcr-xlsx-and-prism.md) — `Example_qPCR.xlsx` (`74` formulas) and GraphPad Prism 10.1.1.270 ZIP containers (`AM` vs `GM`).
- **Analysis**: [ana-livak-2ddct-am-vs-gm](analyses/ana-livak-2ddct-am-vs-gm.md) — Exact proportionality proof ($c = 1.676390$), variance-homogeneity $F(3,3)=1451$ audit, and log-space $\Delta C_T$ test ($t=3.721, P=0.0098$).
- **Figures**: [fig-qpcr-excel-and-prism-panels](figures/fig-qpcr-excel-and-prism-panels.md) — Visually verified Excel comparison and Prism Unpaired $t$ / Mann–Whitney output screenshots.
- **Result**: [res-qpcr-normalization-equivalence](results/res-qpcr-normalization-equivalence.md) — Calibrator invariance (`42.96x` arithmetic / `37.63x` geometric) and mandatory cycle-space testing rule.

### Chain C — BGI Stereo-seq Spatial `CID` Barcode Decoding (`Chip A02598A4`, `GRCm39/mm39` `Egf`)
- **Experiment**: [exp-stereoseq-cid-decoding](experiments/exp-stereoseq-cid-decoding.md) — `mm39` `chr3:129,503,811-129,504,562` (`Egf`) spatial BAM-to-FASTQ barcode recovery.
- **Dataset**: [ds-a02598a4-barcodetopos-and-bam](datasets/ds-a02598a4-barcodetopos-and-bam.md) — `bpMatrix_1[12274, 6518, 0] = 100904410303266` and read `E150018299L1C036R00400117279`.
- **Analysis**: [ana-st-barcodemap-vs-base4-hallucination](analyses/ana-st-barcodemap-vs-base4-hallucination.md) — Falsification of naive base-4 output and pinned `ST_BarcodeMap-0.0.1 --action 3` build (`boost=1.73`, `hdf5=1.10.7`).
- **Figures**: [fig-stereoseq-igv-ai-github-issue](figures/fig-stereoseq-igv-ai-github-issue.md) — Visually verified IGV alignment tooltip, LLM hallucination screenshot, and GitHub issue `#2`.
- **Result**: [res-stereoseq-cid-ground-truth](results/res-stereoseq-cid-ground-truth.md) — Exact 25-nt CID match (`TATAGTACATATGATTCCAGGTCCA`) against raw Read 1 FASTQ.

### Additional Domain, Community, & Epistemology Reviews
- [ana-glycorna-arpla-journal-club](analyses/ana-glycorna-arpla-journal-club.md) — Single-cell glycoRNA `ARPLA` aptamer + RISH + phi29 RCA imaging (PMID `37217750`; corrects `.wiki/` click-chemistry error).
- [ana-zebrafish-model-and-spaceflight](analyses/ana-zebrafish-model-and-spaceflight.md) — *Danio rerio* genetics (`AB`/`TU`), `Shenzhou 18` 43-day closed orbital tank, and LabOnoM `mstnb`/TSGD studies.
- [ana-bsgou-contribution-score](analyses/ana-bsgou-contribution-score.md) — GitHub API contribution scraper and `0.5/0.5` vs `0.3/0.7` Linear+Poisson formula audit.
- [ana-elephant-in-the-algorithm](analyses/ana-elephant-in-the-algorithm.md) — Single-cell `UMAP`/`t-SNE` distortion (Chari & Pachter 2023) and preclinical replication benchmarks.
- [ana-beyond-the-silicon-mirage](analyses/ana-beyond-the-silicon-mirage.md) — Epistemic & biophysical limits of compute-only biology (`64 h` GPU vs `60 d` SPR latency, `49%` ranking score, IDPs, cavity hydration, and DBTL bottlenecks).
- [ana-after-proof-scarcity](analyses/ana-after-proof-scarcity.md) — Post-scarcity mathematical synthesis (`Math 1.0` -> `Math 2.0`, `722`/`719` Oct 2026 preprints, `Palomar` alignment, `PNAS` `63%` -> `88%` novelty) and quantitative biology rigor (`UMAP`, `$2^{-\Delta\Delta C_T}$`, identifiability).
- [fig-zebrafish-and-software-panels](figures/fig-zebrafish-and-software-panels.md) — Visually verified zebrafish lifecycle, biogeography/phylogeny, BSGOU software schematic, and `Ono_2025.jpg` gallery figure.

## 3. Governance, Integrity Manifest, & Skills Router
- [contradictions.md](contradictions.md) — `9` verified contradictions and format anomalies (`CON-01`–`CON-09`) with exact `path:line` citations.
- [decisions.md](decisions.md) — Historical Git-provenanced decisions and `2026-11-06` architecture records (`DEC-01`–`DEC-05`).
- [lessons-learned.md](lessons-learned.md) — Verified biomedical and engineering lessons.
- [open-questions.md](open-questions.md) — `6` concrete follow-up questions (`OQ-01`–`OQ-06`) awaiting owner decision.
- [manifest/OVERVIEW.md](manifest/OVERVIEW.md) — Format-aware SHA-256 file manifest guide and anomaly breakdown.
- [skills/README.md](skills/README.md) — Multi-tier skills catalog (`1,539` retained, `273` omitted) and `global -> project -> external` router.
  - [skills/REPOSITORIES.md](skills/REPOSITORIES.md) | [skills/OMISSIONS.md](skills/OMISSIONS.md) | [skills/SECURITY_REVIEW.md](skills/SECURITY_REVIEW.md)
- [worktrees/README.md](worktrees/README.md) — Staging protocol for isolated `git worktree` findings prior to consolidation.
