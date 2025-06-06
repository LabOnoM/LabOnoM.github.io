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
### Define notations
Let's denote the following terms:
 - The PCR Cycles: $C$
 - The PCR Efficiency: $E$
 - The PCR Cycles at the threshold: subscript $T$
 - The Reference gene (*i.e.*, hosekeeping gene): subscript $R$
 - The target interested **unknown** gene: subscript $X$
 - The target interested **unknown** gene ($X$) in query group: subscript $q$
 - The target interested **unknown** gene ($X$) in control group: subscript $c$
 - The sample index: $i$
 
 > **note:**  Each sample contains both the target gene $X$ and the reference gene $R$, hence they are considered paired within each sample.

Then, we make the following assumptions and definitions:
 - $(1 + E)$ is the PCR amplification base (often $\approx2$). For simplicity, we assume ideal efficiency, i.e., $E_X = E_R = E = 1$.
 - $C_{T,R}$ is the **Threshold Cycle** ($C_{T}$) for the **reference ($R$)** gene in all samples (e.g., GAPDH, 18s, Beta-actin, etc.).
 - $C_{T,X}$ is the **Threshold Cycle** ($C_{T}$) for our interested **unknown** gene $X$ in all samples.
 - The $\Delta C_T$ for the query sample $i$ is defined as: $\Delta C_{T,Q_{i}} = C_{T,X_{Q,i}} - C_{T,R_{Q,i}}$
 - The $\Delta C_T$ for the control sample $i$ is defined as: $\Delta C_{T,C_{i}} = C_{T,X_{C,i}} - C_{T,R_{C,i}}$ 
 
According to [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/), the calibrator was estimated by the mean $\Delta C_{T,X_c}$ of the **control ($c$)** group: 
 $$\overline{\Delta C_{T,C}} = \frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i} \tag{1}$$
Then, we can define:
 - $\Delta\Delta C_{T,X_i} = \Delta C_{T,X_i} - \overline{\Delta C_{T,C}} \tag{2}$
 - $\Delta\Delta C_{T,Q_i} = \Delta C_{T,Q_i} - \overline{\Delta C_{T,C}}$
 - $\Delta\Delta C_{T,C_i} = \Delta C_{T,C_i} - \overline{\Delta C_{T,C}}$

Then, we can express the observation from the previous electric spreadsheet using the following equation:
$$2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = 2^{-\Delta\Delta C_{T,X_i}}\div \overline{2^{-\Delta\Delta C_{T,C}}}\tag{2}$$
Where:
 - $\overline{2^{-\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}$
 - $\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,C_i}}$

The **left-hand side** of Equation (2) describes a normalization process: first, the target gene expression ($X$) is normalized to the reference gene ($R$) within each sample; second, these normalized values are further normalized by the arithmetic mean of the control group’s $X/R$ values.

The **right-hand side** of Equation (2) describes an additional normalization on the original $2^{-\Delta\Delta C_T}$ method: each $2^{-\Delta\Delta C_T}$​ value is additionally normalized by the mean of the control group’s $2^{-\Delta\Delta C_T}$​​ values.

What we found in our calculation inside the electric spreadsheet is that these two normalization methods yield exactly the same results. In the following section, we will demonstrate that these two approaches are mathematically equivalent.
### Derivation of Eq.(2)

Let's first expand the upper part (numerator) of the right side of eq.(2):
  - From the definition of $\Delta\Delta C_{T,X_i} = \Delta C_{T,X_i} - \overline{\Delta C_{T,C}} \tag{2}$ , we get:
$$2^{-\Delta\Delta C_{T,X_i}} = 2^{-(\Delta C_{T,X_i} - \overline{\Delta C_{T,C}})} = \frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}}$$
 
 Then, let's expand the lower part (denominator) of the right side of eq.(1):
  - Because of $\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,Ci}}$ and $\Delta\Delta C_{T,C_i} = \Delta C_{T,C_i} - \overline{\Delta C_{T,C}}$:
$$\overline{2^{-\Delta\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta\Delta C_{T,Ci}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-(\Delta C_{T,C_i} - \overline{\Delta C_{T,C}})} = \frac{1}{n}\sum_{i=1}^{n} \frac{2^{-\Delta C_{T,C_i}}}{2^{-\overline{\Delta C_{T,C}}}} $$
 - Therefore:
$$\frac{1}{n}\sum_{i=1}^{n} \frac{2^{-\Delta C_{T,C_i}}}{2^{-\overline{\Delta C_{T,C}}}} = \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot 2^{-\overline{\Delta C_{T,C}}}}$$

So the full expression becomes: 

$$\frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}} \div \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot 2^{-\overline{\Delta C_{T,C}}}} = \frac{2^{-\Delta C_{T,X_i}}}{\cancel{2^{-\overline{\Delta C_{T,C}}}}} \div \frac{\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}{n\cdot \cancel{2^{-\overline{\Delta C_{T,C}}}}} = \frac{2^{-\Delta C_{T,X_i}}}{\frac{1}{n} \sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}}$$

Because of $\overline{2^{-\Delta C_{T,C}}} = \frac{1}{n}\sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}$ , we get:
$$\frac{2^{-\Delta C_{T,X_i}}}{\frac{1}{n} \sum_{i=1}^{n} 2^{-\Delta C_{T,C_i}}} = \frac{2^{-\Delta C_{T,X_i}}}{\overline{2^{-\Delta C_{T,C}}}} = 2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = left\ side\ of\ eq.(2)$$


Hence, the **left-hand side of equation (2)** is algebraically equal to its **right-hand side**, even though they originate from different forms. ooks wired, right? Then what happened in here? Why do we divide the $2^{-\Delta\Delta C_{T,X_i}}$ by the averaged $2^{-\Delta\Delta C_{T,C}}$ of control group results in the exact value as the same as when we divide the $2^{-\Delta C_{T,X_i}}$ by the average $2^{-\Delta C_{T,C}}$ ?

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

## References
 - [https://www.gene-quantification.de/](https://www.gene-quantification.de/)
 - [Karlen Y, McNair A, Perseguers S, Mazza C, Mermod N. Statistical significance of quantitative PCR. BMC bioinformatics. 2007 Dec;8:1-6.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-131#Sec14)
 - [Vandesompele J, De Preter K, Pattyn F, Poppe B, Van Roy N, De Paepe A, Speleman F. Accurate normalization of real-time quantitative RT-PCR data by geometric averaging of multiple internal control genes. Genome biology. 2002 Jun;3:1-2.](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2002-3-7-research0034#Abs1)
 - [Nolan T, Hands RE, Bustin SA. Quantification of mRNA using real-time RT-PCR. Nature protocols. 2006 Aug;1(3):1559-82.](http://gene-quantification.org/nolan-hands-bustin-2006.pdf)
 - [Pfaffl MW. A new mathematical model for relative quantification in real-time RT–PCR. Nucleic acids research. 2001 May 1;29(9):e45-.](https://academic.oup.com/nar/article/29/9/e45/2384081)
 - [Yuan JS, Reed A, Chen F, Stewart CN. Statistical analysis of real-time PCR data. BMC bioinformatics. 2006 Dec;7:1-2.](https://link.springer.com/article/10.1186/1471-2105-7-85)
 - [Rao X, Huang X, Zhou Z, Lin X. An improvement of the 2ˆ (–delta delta CT) method for quantitative real-time polymerase chain reaction data analysis. Biostatistics, bioinformatics and biomathematics. 2013 Aug;3(3):71.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4280562/?utm_source=chatgpt.com)