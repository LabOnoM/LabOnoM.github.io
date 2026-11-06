---
id: fig-qpcr-excel-and-prism-panels
type: figure
status: visually_verified
updated_at: 2026-11-06
source_refs:
  - _posts/PostAttachedFiles/Identical_qPCR_Results.png
  - _posts/PostAttachedFiles/Identical_Statistical_Results_qPCR.png
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
tags:
  - figure
  - qpcr
  - graphpad-prism
  - excel
---

# Figures: qPCR Spreadsheet Normalization & GraphPad Prism Test Output Panels

## Traceability Links
- **Experiment**: [[exp-qpcr-wt-vs-ko]]
- **Dataset**: [[ds-example-qpcr-xlsx-and-prism]]
- **Analysis**: [[ana-livak-2ddct-am-vs-gm]]
- **Result Summary**: [[res-qpcr-normalization-equivalence]]

## Visually Inspected Figures
### 1. `_posts/PostAttachedFiles/Identical_qPCR_Results.png` (`2,482 × 1,568` px, 32-bit RGBA PNG)
- **Direct Visual Observation**:
  - Screenshot of `Example_qPCR.xlsx` comparing the two stacked spreadsheet blocks (`GM`-calibrated $\Delta\Delta C_T$ in upper rows vs. `AM`-calibrated $2^{-\Delta C_T}$ ratio in lower rows) alongside bar charts of relative expression (`WT = 1.00`, `KO = 42.96`).
  - Visually confirms identical normalized replicate values (`WT`: `0.191, 0.336, 2.757, 0.716`; `KO`: `2.565, 107.818, 25.602, 35.846`) when both methods are expressed relative to the `WT` group mean (`1.00`).

### 2. `_posts/PostAttachedFiles/Identical_Statistical_Results_qPCR.png` (`2,928 × 1,532` px, 32-bit RGBA PNG)
- **Direct Visual Observation**:
  - Side-by-side GraphPad Prism 10 tabular output screenshots comparing `AM_Calibrator_2DDCt` (left) and `GM_Calibrator_2DDCt` (right) for both **Unpaired t test** and **Mann-Whitney test**:
    - **Unpaired t test panel**: Displays `P value = 0.1143`, `P value summary = ns`, `Significantly different (P < 0.05)? = No`, `t, df: t=1.847, df=6`, `R squared (eta squared) = 0.3624`, and beneath **`F test to compare variances`**: `F, DFn, DFd = 1451, 3, 3`, `P value < 0.0001`, `P value summary = ****`, `Significantly different (P < 0.05)? = Yes`.
    - **Mann-Whitney test panel**: Displays `P value = 0.0571` (`Exact`), `P value summary = ns`, `Sum of ranks in column A, B = 11, 25`, `Mann-Whitney U = 1`.
- **Observation vs. Caption Interpretation**:
  - Visually confirms that scale-invariant statistics ($t = 1.847$, $R^2 = 0.3624$, variance $F = 1451$, Mann–Whitney $U = 1$) match across both calibrators, while also directly proving that the `F = 1451` row is GraphPad Prism's **variance homogeneity $F$-test** on exponentiated $2^{-\Delta\Delta C_T}$ values rather than an ANOVA $F$-test or a log-space $\Delta C_T$ test (`CON-04`).
