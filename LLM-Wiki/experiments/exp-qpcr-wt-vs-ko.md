---
id: exp-qpcr-wt-vs-ko
type: experiment
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md
  - _posts/PostAttachedFiles/Example_qPCR.xlsx
  - _posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism
  - _posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism
tags:
  - experiment
  - qpcr
  - livak-2ddct
  - statistics
---

# Experiment: Comparative RT-qPCR Assay (`WT` vs. `KO`, $n=4$ Biological Replicates)

## Traceability Links
- **Dataset**: [[ds-example-qpcr-xlsx-and-prism]]
- **Analysis**: [[ana-livak-2ddct-am-vs-gm]]
- **Figures**: [[fig-qpcr-excel-and-prism-panels]]
- **Result Summary**: [[res-qpcr-normalization-equivalence]]
- **Flagged Contradictions**: [[contradictions]] (`CON-04`)

## Experimental Design & Sample Identities (Direct Observations)
- **Groups & Sample Sizes**: Two genotype groups with **$n = 4$ independent wells/replicates per group** (`8` total wells recorded in `_posts/PostAttachedFiles/Example_qPCR.xlsx`, `Sheet1`, cells `A4:D11` and `A17:D24`):
  - **Control / Calibrator Group (`WT`)**: Wells `A1`, `A2`, `A3`, `A4`.
  - **Treatment / Perturbation Group (`KO`)**: Wells `C5`, `C6`, `C7`, `C8`.
- **Measured Channels & Units**:
  - **Reference (Housekeeping) Gene (`Ref`, $C_{T,R}$)**: Fractional PCR threshold cycle (unitless cycle number $C_T$).
  - **Target Gene of Interest (`Target`, $C_{T,X}$)**: Fractional PCR threshold cycle ($C_T$).
- **Amplification Assumption**: Idealized doubling efficiency per thermal cycle ($E_X = E_R = 1$, i.e., base $1 + E = 2.00$, derived in `_posts/2025-06-15-Everything-you-shall-know-when-using-ΔΔCt-method-in-qPCR.md#L33-L79`).

## Observed Well-Level Measurements (`Example_qPCR.xlsx`, `Sheet1`)
| Group | Well ID | $C_{T,R}$ (`Ref`) | $C_{T,X}$ (`Target`) | $\Delta C_T = C_{T,X} - C_{T,R}$ | Quality Note |
|---|---|---:|---:|---:|---|
| `WT` | `A1` | `21.163004` | `31.776840` | `10.613836` | Normal `WT` replicate |
| `WT` | `A2` | `20.941521` | `30.742912` | `9.801392` | Normal `WT` replicate |
| `WT` | `A3` | `22.998070` | `29.761280` | `6.763210` | Lower $\Delta C_T$ (`WT` high-expressor) |
| `WT` | `A4` | `22.839317` | `31.548481` | `8.709164` | Normal `WT` replicate |
| `KO` | `C5` | `19.604200` | `26.471642` | `6.867441` | Higher $C_{T}$ separation than `C6–C8` |
| `KO` | `C6` | `25.036123` | `26.510185` | `1.474062` | **Reference $C_{T,R}$ delayed by ~2.9 cycles** (`25.04` vs `19.60–22.38`), driving extreme linear fold-change (`180.74x`) |
| `KO` | `C7` | `22.376087` | `25.924448` | `3.548361` | Normal `KO` replicate |
| `KO` | `C8` | `22.175276` | `25.238119` | `3.062843` | Normal `KO` replicate |

## Summary Group Statistics ($\Delta C_T$ Domain)
- **`WT` ($n=4$)**: Arithmetic mean $\overline{\Delta C_{T,\text{WT}}} = 8.971900\text{ cycles}$, sample SD $= 1.666544\text{ cycles}$.
- **`KO` ($n=4$)**: Arithmetic mean $\overline{\Delta C_{T,\text{KO}}} = 3.738177\text{ cycles}$, sample SD $= 2.266364\text{ cycles}$.
- **Mean $\Delta C_T$ Shift ($\overline{\Delta C_{T,\text{KO}}} - \overline{\Delta C_{T,\text{WT}}}$)**: $-5.233724\text{ cycles}$ (corresponding to a $2^{5.233724} = 37.6273\text{-fold}$ geometric increase in `KO` relative to `WT`).
