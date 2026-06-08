# Entity: qPCR Livak Analysis Proof

This page documents the mathematical verification of relative qPCR quantification using the Livak $2^{-\Delta\Delta C_T}$ method.

## The Normalization Equivalence
In relative quantification, researchers often perform a secondary normalization on the Livak fold-changes to force the control group's mean to exactly 1. 

We prove that dividing the individual $2^{-\Delta\Delta C_T}$ values by the **arithmetic mean (AM)** of the control group's $2^{-\Delta\Delta C_T}$ is mathematically identical to dividing the raw relative expression values $2^{-\Delta C_T}$ by the **arithmetic mean** of the control group's $2^{-\Delta C_T}$:

$$ \frac{2^{-\Delta C_{T, X_i}}}{\overline{2^{-\Delta C_{T, C}}}} = \frac{2^{-\Delta\Delta C_{T, X_i}}}{\overline{2^{-\Delta\Delta C_{T, C}}}} $$

### Mathematical Proof
1. Expand $2^{-\Delta\Delta C_{T, X_i}}$ where $\Delta\Delta C_{T, X_i} = \Delta C_{T, X_i} - \overline{\Delta C_{T, C}}$:
   $$ 2^{-\Delta\Delta C_{T, X_i}} = \frac{2^{-\Delta C_{T, X_i}}}{2^{-\overline{\Delta C_{T, C}}}} $$
2. Expand the control group mean:
   $$ \overline{2^{-\Delta\Delta C_{T, C}}} = \frac{\sum 2^{-\Delta C_{T, C_i}}}{n \cdot 2^{-\overline{\Delta C_{T, C}}}} $$
3. Divide the two terms:
   $$ \frac{2^{-\Delta\Delta C_{T, X_i}}}{\overline{2^{-\Delta\Delta C_{T, C}}}} = \frac{2^{-\Delta C_{T, X_i}}}{2^{-\overline{\Delta C_{T, C}}}} \div \frac{\sum 2^{-\Delta C_{T, C_i}}}{n \cdot 2^{-\overline{\Delta C_{T, C}}}} = \frac{2^{-\Delta C_{T, X_i}}}{\frac{1}{n}\sum 2^{-\Delta C_{T, C_i}}} = \frac{2^{-\Delta C_{T, X_i}}}{\overline{2^{-\Delta C_{T, C}}}} $$

## Statistical Scale Invariance
Since relative quantification scales data by a linear constant, statistical parameters (such as $P$-values, $t$-statistics, and ANOVA $F$-ratios) remain **identical** across both normalization strategies.

## Related Files
- `_posts/PostAttachedFiles/Example_qPCR.xlsx`: Spreadsheet proving identity of both methods.
- `_posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism` / `GM_Calibrator_2DDCt.prism`: GraphPad Prism files verifying identical statistics.
