---
id: res-qpcr-normalization-equivalence
type: result
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
  - _posts/PostAttachedFiles/Example_qPCR.xlsx
  - _posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism
  - _posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism
tags:
  - result
  - qpcr
  - livak-2ddct
  - biostatistics
---

# Result Summary: Scale-Invariance of qPCR Calibrators & Mandatory Log-Space Testing

## Complete Traceability Chain
- **Experiment**: [[exp-qpcr-wt-vs-ko]]
- **Dataset**: [[ds-example-qpcr-xlsx-and-prism]]
- **Analysis**: [[ana-livak-2ddct-am-vs-gm]]
- **Figures**: [[fig-qpcr-excel-and-prism-panels]]
- **Contradictions**: [[contradictions]] (`CON-04`)

## Verified Results (Observations)
1. **Exact Positive Proportionality of Calibrators**: Across `WT` ($n=4$) and `KO` ($n=4$) wells in `Example_qPCR.xlsx`, normalizing $2^{-\Delta C_T}$ by the control group's arithmetic mean ($k_{\text{AM}} = 0.003340$) versus Livak's control mean $\Delta C_T$ ($k_{\text{GM}} = 2^{-8.9719} = 0.001992$) scales all replicate fold-changes by exact constant $c = 1.676390$. Re-normalizing to `WT = 1.0000` yields identical arithmetic fold-change **`42.9580x`** (`KO/WT`) in both pipelines (whereas the geometric fold-change $2^{-\overline{\Delta\Delta C_T}}$ is **`37.6273x`**).
2. **Invariance of Dimensionless Test Statistics**: In GraphPad Prism 10.1.1.270 (`AM_Calibrator_2DDCt.prism` vs. `GM_Calibrator_2DDCt.prism`), unpaired Student's $t$ (`1.847`, $\text{df}=6$, $P=0.1143$), $R^2$ (`0.3624`), variance-ratio $F_{3,3}$ (`1451`, $P=6.14\times 10^{-5}$), and Mann–Whitney $U$ (`1`, two-tailed exact $P=0.0571$) are invariant to the choice of calibrator constant (differing only in the 5th significant digit due to 3-decimal CSV rounding in `AM_Calibrator_2DDCt.prism`).

## Methodological & Biological Takeaway (Interpretation)
- While calibrator choice (`AM` vs. `GM`) does **not** alter scale-invariant test statistics within linear $2^{-\Delta\Delta C_T}$ space, **performing parametric $t$-tests or ANOVA on exponentiated $2^{-\Delta\Delta C_T}$ values is statistically invalid** because $2^{-x}$ transforms additive Gaussian cycle noise into severely right-skewed log-normal heteroscedasticity ($F_{3,3} = 1451$ driven by well `C6` reference shift $C_{T,R} = 25.04$).
- Hypothesis testing for qPCR should be executed in **log/cycle space ($\Delta C_T$)** ($t = 3.721$, $\text{df} = 6$, $P = 0.0098$, variance $F_{3,3} = 1.85$), reporting geometric fold-change $2^{-\Delta\Delta C_T} = 37.63$ with asymmetric $95\%$ confidence intervals mapped from $\Delta C_T$, and inspecting outlier well `C6` for RNA loading/amplification failure.
