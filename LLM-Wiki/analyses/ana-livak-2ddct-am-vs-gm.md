---
id: ana-livak-2ddct-am-vs-gm
type: analysis
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
  - _posts/PostAttachedFiles/Example_qPCR.xlsx
  - _posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism
  - _posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism
tags:
  - analysis
  - qpcr
  - scale-invariance
  - t-test
  - mann-whitney
  - log-transformation
---

# Analysis: Scale-Invariance of $2^{-\Delta\Delta C_T}$ Calibrators & Linear-vs-Log Statistical Testing

## Traceability Links
- **Experiment**: [[exp-qpcr-wt-vs-ko]]
- **Dataset**: [[ds-example-qpcr-xlsx-and-prism]]
- **Figures**: [[fig-qpcr-excel-and-prism-panels]]
- **Result Summary**: [[res-qpcr-normalization-equivalence]]
- **Flagged Contradictions**: [[contradictions]] (`CON-04`)

## 1. Mathematical Proof Verification (Scale Invariance)
In `_posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md#L121-L246`, two common laboratory calibrator definitions are compared for sample $i$:
- **Method A (Arithmetic Mean Calibrator in $2^{-\Delta C_T}$ space, `AM`)**:
  $$R_i^{\text{AM}} = \frac{2^{-\Delta C_{T,i}}}{\frac{1}{n_C}\sum_{j \in C} 2^{-\Delta C_{T,j}}}$$
- **Method B (Livak Mean $\Delta C_T$ / Geometric Mean Calibrator, `GM`)**:
  $$R_i^{\text{GM}} = 2^{-(\Delta C_{T,i} - \overline{\Delta C_{T,C}})} = \frac{2^{-\Delta C_{T,i}}}{2^{-\overline{\Delta C_{T,C}}}}$$

Because both calibrators divide every replicate $2^{-\Delta C_{T,i}}$ across **all** experimental groups by a single positive constant ($k_{\text{AM}} = 0.00333952$ vs. $k_{\text{GM}} = 2^{-8.971900} = 0.00199220$), the two vectors satisfy exact positive proportionality:
$$R_i^{\text{GM}} = c \cdot R_i^{\text{AM}}, \quad c = \frac{k_{\text{AM}}}{k_{\text{GM}}} = 1.676390 > 0$$
Consequently, **any scale-invariant test statistic**—specifically Student's $t$, Welch's $t$, one-way ANOVA $F$, variance-ratio $F$, Pearson $R^2$, and rank-based Mann–Whitney $U$—is mathematically invariant between `AM` and `GM`.

## 2. Exact Verification in GraphPad Prism 10.1.1.270 (`*.prism` `results.json`)
| Statistic / Metric | `AM_Calibrator_2DDCt.prism` (3-dec input) | `GM_Calibrator_2DDCt.prism` (6-dec input) | Discrepancy Cause |
|---|---:|---:|---|
| Control (`WT`) Mean $\pm$ SD | `1.00025 ± 1.19205` | `1.67639 ± 1.99809` | Scaled by $c = 1.67639$ |
| Treatment (`KO`) Mean $\pm$ SD | `42.95725 ± 45.42423` | `72.01331 ± 76.14876` | Scaled by $c = 1.67639$ |
| Ratio $\overline{\text{KO}} / \overline{\text{WT}}$ | `42.9465` (`42.9580` unrounded) | `42.9574` (`42.9580` unrounded) | 3-decimal input truncation in `AM` |
| Unpaired Student's $t$ ($\text{df}=6$) | **`t = 1.846725`**, **`P = 0.1143`** (`ns`) | **`t = 1.846736`**, **`P = 0.1143`** (`ns`) | Identical to 4 sig figs |
| Effect Size $R^2$ | `0.36236` | `0.36236` | Exact match |
| Variance Homogeneity $F$-test ($F_{3,3}$) | **`F = 1450.74`**, **`P = 0.0000614`** (`****`) | **`F = 1451.18`**, **`P = 0.0000614`** (`****`) | **Variance ratio test, NOT ANOVA!** |
| Exact Mann–Whitney $U$ (two-tailed) | **`U = 1`**, ranks `(11, 25)`, **`P = 0.0571`** (`ns`) | **`U = 1`**, ranks `(11, 25)`, **`P = 0.0571`** (`ns`) | Exact rank invariance |

## 3. Critical Statistical Contradictions Flagged (`CON-04`)
1. **Variance $F$-test Misdescribed as ANOVA**: `_posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md#L221-L240` and `Wiki_Build_Output.md#L85` refer to ANOVA $F$-ratios in the Prism verification; however, neither `.prism` archive contains an ANOVA analysis. With $k=2$ groups, Prism ran an Unpaired $t$-test whose companion $F(3,3) = 1451$ (`P < 0.0001`) is **Snedecor's $F$-test for equality of variances** ($s_{\text{KO}}^2 / s_{\text{WT}}^2 = 76.15^2 / 2.00^2 \approx 1451$), proving severe heteroscedasticity in $2^{-\Delta\Delta C_T}$ space! (Had one-way ANOVA been run on these two groups, $F_{1,6} = t^2 = 1.8467^2 = 3.4104$, $P = 0.1143$.)
2. **Linear Fold-Change (`P = 0.1143`) vs. Log $\Delta C_T$ (`P = 0.0098`) Statistical Domain**: Post line 239 warns users to run parametric tests in $\Delta C_T$ / $\Delta\Delta C_T$ log space before exponentiation, yet the attached `.prism` files run Student's $t$-test **after** $2^{-x}$ exponentiation. Because well `C6` has $\Delta C_T = 1.474$ (`180.74x` linear fold-change), exponentiation inflates `KO` standard deviation 38-fold and masks significance ($P = 0.1143$). Running the unpaired two-sample $t$-test directly on $\Delta C_T$ (`WT` $8.972 \pm 1.667$ vs `KO` $3.738 \pm 2.266$) yields homogeneous variances ($F_{3,3} = 1.85$, $P = 0.626$) and a statistically significant difference (**$t = 3.7208$, $\text{df} = 6$, $P = 0.00984$**; Welch's $t = 3.7208$, $\text{df} = 5.51$, $P = 0.0114$).
