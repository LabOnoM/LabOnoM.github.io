---
title: "'Shall we use geometric mean for reporting qPCR results?'"
lang: en
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
tags:
  - qPCR
  - Math
  - Statistics
---

Let's denote the below notations:
 - The PCR Cycles: $C$
 - The PCR Efficiency: $E$
 - The PCR Cycles at the threshold: subscript $T$
 - The Reference gene (*i.e.*, hosekeeping gene): subscript $R$
 - The target interested **unknown** gene: subscript $X$
 - The target interested **unknown** gene ($X$) in query group: subscript $q$
 - The target interested **unknown** gene ($X$) in control group: subscript $c$
 - The sample index: $i$
 
 > **note:**  $X$ and $R$ are paired for each sample, as every sample includes both the target gene $X$ and the reference gene $R$.

Then, we make the following assumptions and definitions:
 - $(1 + E)$ is the PCR amplification base (often $\approx2$). For simplification, let's just use base of 2 for the PCR amplification based on the assumption that $E_X = E_R = E = 1$.
 - $C_{T,R}$ is the **Threshold Cycle** ($C_{T}$) for the **reference ($R$)** gene in all samples (e.g., GAPDH, 18s, Beta-actin, etc.).
 - $C_{T,X}$ is the **Threshold Cycle** ($C_{T}$) for our interested **unknown** gene $X$ in all samples.
 - $\Delta C_{T,Q_{i}} = C_{T,X_{Q,i}} - C_{T,R_{Q,i}}$ in each **query ($Q$)** sample.
 - $\Delta C_{T,C_{i}} = C_{T,X_{C,i}} - C_{T,R_{C,i}}$ in each **control ($C$)** sample.
 
 In the paper of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/), the calibrator was estimated by the mean $\Delta C_{T,X_c}$ of the **control ($c$)** group: 
 $$\overline{\Delta C_{T,C}} = \frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i} \tag{1}$$
Then, we can define:
 - $\Delta\Delta C_{T,X_i} = \Delta C_{T,X_i} - \overline{\Delta C_{T,C}} \tag{2}$
 - $\Delta\Delta C_{T,Q_i} = \Delta C_{T,Q_i} - \overline{\Delta C_{T,C}}$
 - $\Delta\Delta C_{T,C_i} = \Delta C_{T,C_i} - \overline{\Delta C_{T,C}}$

Then, we can have the below equation:
$$2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = 2^{-\Delta\Delta C_{T,X_i}}\div \overline{2^{-\Delta\Delta C_{T,C}}}\tag{2}$$
Where:
 - $\overline{2^{-\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}$
 - $\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,C_i}}$

Let's first expand the upper part of the right side of eq.(2):
  - Because of $\Delta\Delta C_{T,X_i} = \Delta C_{T,X_i} - \overline{\Delta C_{T,C}} \tag{2}$ :
$$2^{-\Delta\Delta C_{T,X_i}} = 2^{-(\Delta C_{T,X_i} - \overline{\Delta C_{T,C}})} = \frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}}$$
 
 Then, let's expand the lower part the right side of eq.(1):
  - Because of $\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,Ci}}$ and $\Delta\Delta C_{T,C_i} = \Delta C_{T,C_i} - \overline{\Delta C_{T,C}}$:
$$\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,Ci}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-(\Delta C_{T,C_i} - \overline{\Delta C_{T,C}})} = \frac{1}{n}\sum_{i=1}^{n} \frac{2^{-\Delta C_{T,C_i}}}{2^{-\overline{\Delta C_{T,C}}}} $$
 - Therefore:
$$\frac{1}{n}\sum_{i=1}^{n} \frac{2^{-\Delta C_{T,C_i}}}{2^{-\overline{\Delta C_{T,C}}}} = \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot 2^{-\overline{\Delta C_{T,C}}}}$$

Finally, 

$$\frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}} \div \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot 2^{-\overline{\Delta C_{T,C}}}} = \frac{2^{-\Delta C_{T,X_i}}}{\cancel{2^{-\overline{\Delta C_{T,C}}}}} \div \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot \cancel{2^{-\overline{\Delta C_{T,C}}}}} = \frac{2^{-\Delta C_{T,X_i}}}{\frac{1}{n} \sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}$$

Because of $\overline{2^{-\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}$ :
$$\frac{2^{-\Delta C_{T,X_i}}}{\frac{1}{n} \sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}} = \frac{2^{-\Delta C_{T,X_i}}}{\overline{2^{-\Delta C_{T,C}}}} = 2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = left\ side\ of\ eq.(2)$$


Looks wired, right? Then what happened in here? Why do we divide the $2^{-\Delta\Delta C_{T,X_i}}$ by the averaged $2^{-\Delta\Delta C_{T,C}}$ of control group results in the exact value as the same as when we divide the $2^{-\Delta C_{T,X_i}}$ by the average $2^{-\Delta C_{T,C}}$ ?

 OK, let's go back to the paper of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/) and check the its ref\[[Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/)\].eq.(8):
 $$\frac{X_{N,q}}{X_{N,cb}}=\frac{K\times(1+E)^{-\Delta C_{T,q}}}{K\times(1+E)^{-\Delta C_{T,cb}}}=(1+E)^{-\Delta\Delta C_T}$$
According to the FIG.2 of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/), the $\Delta C_{T,cb}$ is the arithmetic mean of the $\Delta C_{T}$ in the control group. Therefore, the above ref\[[Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/)\].eq.(8) can be re-written as the below equation in the context of this blog:

$$ 2^{-\Delta\Delta C_{T,X_i}} = \frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}} = {2^{-\Delta C_{T,X_i}}}\div{2^{-\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}} \tag{3}$$

Have you noticed this part, ${2^{-\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}}$ ? This is the geometric mean of $2^{-\Delta C_{T,C_i}}$, because:

$$ {2^{-\frac{1}{n}\sum_{i=1}^{n}{\Delta C_{T,C_i}}}} = \sqrt[n]{2^{-\sum_{i=1}^{n}{\Delta C_{T,Ci}}}} = \sqrt[n]{2^{-\Delta C_{T, C_1}}\cdot2^{-\Delta C_{T, C_2}}\cdot 2^{-\Delta C_{T, C_3}}...2^{-\Delta C_{T, C_n}}} = (\prod^n_{i=1}{2^{-\Delta C_{T,C_i}}})^\frac{1}{n} $$


Therefore, the left side of eq.(2) is actually equal to:
$$ 2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = 2^{-\Delta C_{T,X_i}}\div\frac{1}{n}\sum_{i=1}^{n}{2^{-\Delta C_{T,C_i}}} $$

Now, the story is totally clear, the left side of eq.(2) is the Arithmetic Mean version of $2^{-\Delta\Delta C_T}$. Let's denote it as:
$$ 2^{-\Delta\Delta{C_{T,X_i}}AM} = \frac{2^{-\Delta C_{T,X_i}}}{\overline{2^{-\Delta C_{T,C}}}} = 2^{-\Delta C_{T,X_i}}\div\frac{1}{n}\sum_{i=1}^{n}{2^{-\Delta C_{T,C_i}}} \tag{4}$$
Now, we can take the eq.(3) as the Geometric Mean of $2^{-\Delta\Delta C_T}$, which is the original in the paper of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/). For distinguish and convenience in this blog, let's denote it as $2^{-\Delta\Delta{C_{T,X_i}}GM}$.



This is interesting, because 


$$\frac{\cancel{Geometric\_Mean}[Sample]}{Arithmetic\_Mean[\cancel{Geometric\_Mean}[Sample]]} = \frac{Sample}{Arithmetic\_Mean[Sample]}$$







  - Because of eq.(1):
$$2^{-(\Delta C_{T,X_i} - \overline{\Delta C_{T,C}})} = 2^{-(\Delta C_{T,X_i} - \frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i})} = 2^{-\Delta C_{T,X_i}} \div 2^{\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}$$
