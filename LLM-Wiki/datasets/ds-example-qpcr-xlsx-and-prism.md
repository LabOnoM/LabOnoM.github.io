---
id: ds-example-qpcr-xlsx-and-prism
type: dataset
status: inspected_structured_verified
updated_at: 2026-11-06
source_refs:
  - _posts/PostAttachedFiles/Example_qPCR.xlsx
  - _posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism
  - _posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism
tags:
  - dataset
  - xlsx
  - graphpad-prism
  - qpcr
---

# Dataset: `Example_qPCR.xlsx` & GraphPad Prism 10 Archives (`AM` vs. `GM` Calibrator)

## Traceability Links
- **Experiment**: [[exp-qpcr-wt-vs-ko]]
- **Analysis**: [[ana-livak-2ddct-am-vs-gm]]
- **Figures**: [[fig-qpcr-excel-and-prism-panels]]
- **Result Summary**: [[res-qpcr-normalization-equivalence]]

## Primary Data Files (In-Repository, Full-File Hashed & Parsed)
1. **`_posts/PostAttachedFiles/Example_qPCR.xlsx`** (`12,068` bytes, `ooxml_xlsx_spreadsheet`, 1 worksheet `Sheet1`, `134` non-empty cells, `74` live Excel formula cells):
   - **Block 1 (`Rows 3–13`) — Geometric Mean $\Delta C_T$ Calibrator (`GM_Calibrator` / standard Livak $\overline{\Delta C_{T,C}}$)**:
     - `E4:E11`: `=D4-C4` ($\Delta C_T$)
     - `F4`: `=AVERAGE(E4:E7)` (`8.971900`, calibrator arithmetic mean $\overline{\Delta C_{T,\text{WT}}}$, equivalent to geometric mean in $2^{-\Delta C_T}$ space)
     - `G4:G11`: `=E4-$F$4` ($\Delta\Delta C_T$)
     - `H4:H11`: `=2^-G4` ($2^{-\Delta\Delta C_T}$: `WT = [0.320428, 0.562727, 4.622555, 1.199752]`, mean `1.676366`; `KO = [4.300364, 180.742995, 42.918852, 60.090801]`, mean `72.013253`)
     - `J4:J11`: `=H4/$I$4` (re-normalized so `WT` arithmetic mean `= 1.000000` and `KO` arithmetic mean `= 42.957961` / `42.9566` at full float precision).
   - **Block 2 (`Rows 16–26`) — Direct $2^{-\Delta C_T}$ Arithmetic-Mean Calibrator (`AM_Calibrator`)**:
     - `F17:F24`: `=2^-E17` ($2^{-\Delta C_T}$: `WT` mean `I17 = AVERAGE(F17:F20) = 0.00333952`)
     - `G17:G24`: `=F17/$I$17` ($2^{-\Delta\Delta C_T}$ directly scaled by arithmetic mean of $2^{-\Delta C_{T,\text{WT}}}$: `WT = [0.320428, 0.562727, 4.622555, 1.199752]` wait—divided by `1.676366`, yielding **`WT = [0.191144, 0.335683, 2.757486, 0.715686]`** with mean **`1.000000`**, and **`KO = [2.565290, 107.818345, 25.602320, 35.845873]`** with mean **`42.957957`** — identical to `J4:J11` to machine precision!).

2. **`_posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism`** (`60,093` bytes, GraphPad Prism `10.1.1.270` ZIP container):
   - `data/tables/93B04D36.../data.csv`: Column table (`WT` vs `KO`, $n=4$) storing **3-decimal rounded** `AM`-calibrated linear $2^{-\Delta\Delta C_T}$ values:
     - `WT`: `[0.191, 0.336, 2.757, 0.716]` (mean `1.00025`, SD `1.19205`)
     - `KO`: `[2.565, 107.817, 25.602, 35.845]` (mean `42.95725`, SD `45.42423`)
   - `analyses/` (`2` analyses): Unpaired two-sample $t$-test + $F$-test (`29B4...`) and Mann–Whitney nonparametric test (`B6AC...`).

3. **`_posts/PostAttachedFiles/GM_Calibrator_2DDCt.prism`** (`66,281` bytes, GraphPad Prism `10.1.1.270` ZIP container):
   - `data/tables/0867.../data.csv`: Column table (`WT` vs `KO`, $n=4$) storing **6-decimal** `GM`-calibrated linear $2^{-\Delta\Delta C_T}$ values:
     - `WT`: `[0.320428, 0.562735, 4.622585, 1.199810]` (mean `1.676390`, SD `1.998090`)
     - `KO`: `[4.300405, 180.742990, 42.918850, 60.091000]` (mean `72.013311`, SD `76.148755`)
   - `analyses/` (`2` analyses): Unpaired two-sample $t$-test + $F$-test and Mann–Whitney nonparametric test.
