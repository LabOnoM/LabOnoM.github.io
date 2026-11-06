---
id: open-questions
type: governance
status: active
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/contradictions.md
  - scripts/fetch_bsgou_members.py
  - GSE284271/01.scRNAseq10xVisiumHD.html
  - _posts/PostAttachedFiles/Example_qPCR.xlsx
tags:
  - open-questions
  - follow-up
  - data-governance
---

# Open Scientific & Engineering Questions

1. **External Raw Omics Backup & Archival Location (`OQ-01`)**:
   - Where are the multi-gigabyte primary files for `./240726_VisiumHD/` (`RJ_7_23_24.tif`, `Pax9KO` Space Ranger outputs, `count_area_filtered_adata.h5`) and Stereo-seq chip `A02598A4` (`A02598A4.barcodeToPos.h5`, `E150018299_L01_62_*.fq.gz`) archived and backed up? Current workspace documentation does not record institutional NAS/cloud backup redundancy.
2. **Intended BSGOU Contribution Score Weighting (`OQ-02`, see `CON-05`)**:
   - Should `scripts/fetch_bsgou_members.py#L148` be updated to match the published blog specification (`0.3 * Linear + 0.7 * Poisson`, plus raw event weights), or should `_posts/2025-06-12-BSGOU-Contribution-Score.md` be annotated to reflect the active `0.5 / 0.5` production formula?
3. **Recovery or Removal of Truncated `GSE284271/00.NIH_10xVisiumHD.html` (`OQ-03`, see `CON-03`)**:
   - Does the owner hold the intact upstream NIH Visium HD tutorial/benchmark HTML export intended for `GSE284271/00.NIH_10xVisiumHD.html` (currently a 117-byte truncated fragment)?
4. **qPCR Outlier Well `C6` & Blog Erratum (`OQ-04`, see `CON-04`)**:
   - In `_posts/PostAttachedFiles/Example_qPCR.xlsx`, `KO` well `C6` exhibits a ~2.9-cycle delay in reference gene $C_{T,R}$ (`25.036` vs `19.604–22.376`). Should an addendum be added to `_posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md` clarifying that `F = 1451` in the Prism screenshot is the variance-homogeneity $F$-test on linear $2^{-\Delta\Delta C_T}$ values and showing the log-space $\Delta C_T$ $t$-test (`t = 3.721, P = 0.0098`)?
5. **Cleanup of Tracked Lock & 404 Stub Files (`OQ-05`, see `CON-09`)**:
   - Should `img/gallery/~$Frame_Article.pptx` (`165 B` Office lock file) and the `20` LiteSpeed `404 Not Found` `.html` files in `css/` and `img/` be removed in a dedicated housekeeping PR, or retained for historical stability?
6. **Stale Pipeline Registry Update (`OQ-06`, see `CON-08`)**:
   - Should `00.RawData/PIPELINE_REGISTRY.md` be updated by the owner to replace `.github/workflows/update_members.yml` with manual `scripts/update-members.sh`?
