---
title: Everything you shall know when using ΔΔCt method in qPCR
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

<img src="https://visitor-badge.laobi.icu/badge?page_id=https://labonom.github.io/2025/06/15/shall-we-use-geometric-mean.html" alt="visitor badge"/> [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/LabOnoM)

Have you ever run into this situation while using the ΔΔCt method for qPCR analysis—your control group’s mean expression value _isn’t_ exactly 1? What did you do? Did you quietly normalize the ΔΔCt results **again** just to force the control group’s mean back to 1? And have you ever wondered whether this “sneaky extra normalization” is actually valid, or if you've been doing something questionable all along?

Well, in this blog post, we’re going to get to the bottom of it—**is this secondary normalization mathematically justified, or is it just a placebo for our inner perfectionist?** Let’s find out.
<!--more-->
## Background of qPCR

Quantitative PCR (qPCR), also known as real-time PCR, is a molecular biology technique used to **amplify and quantify DNA** simultaneously. It builds upon traditional PCR (polymerase chain reaction) but adds the ability to monitor DNA amplification in real time.

### 🔬 Core Principle

qPCR uses **fluorescent dyes** (e.g., SYBR Green) or **fluorescent-labeled probes** (e.g., TaqMan) that emit fluorescence proportional to the amount of DNA produced during each PCR cycle. The fluorescence is measured at each cycle, enabling quantification of the target DNA.

### 🧪 Applications

- **Gene expression analysis** (using cDNA from reverse-transcribed RNA)
- **Pathogen detection** (e.g., viruses, bacteria)
- **Genotyping and mutation analysis**
- **Validation of RNA-seq and microarray results**

### 📈 Key Metric: Ct Value

The **cycle threshold (Ct)** is the number of cycles required for the fluorescent signal to **_exceed background_**. It inversely correlates with the amount of starting template: **the lower the Ct, the higher the initial DNA quantity.**

## The $2^{-\Delta\Delta{C_{T}}}$ Method

The method was introduced by **Kenneth J. Livak and Thomas D. Schmittgen** in December 2001, in their pivotal paper titled [_“Analysis of relative gene expression data using real-time quantitative PCR and the 2(–ΔΔCT) Method”_](https://pubmed.ncbi.nlm.nih.gov/11846609/).

Developed at **Applied Biosystems (Foster City, CA)**, it offers a streamlined approach for relative gene expression analysis using real-time PCR, eliminating the need for standard curves when amplification efficiencies are assumed to be identical ([Guide to Performing Relative Quantitation of Gene Expression Using Real-Time Quantitative PCR](https://assets.thermofisher.com/TFS-Assets/LSG/manuals/cms_042380.pdf)).

## An interesting finding

An additional normalization on the original $2^{-\Delta\Delta C_T}$ method (divide the $2^{-\Delta\Delta C_T}$ by mean of $2^{-\Delta\Delta C_T}$ in control group) is qual to dividing the $2^{-\Delta C_T}$ by mean of $2^{-\Delta C_T}$ in control group. As shown in a screenshot of a MS Excel file:


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
 - The $\Delta C_T$ for the **query** sample $i$ is defined as: $\Delta C_{T,Q_{i}} = C_{T,X_{Q,i}} - C_{T,R_{Q,i}}$
 - The $\Delta C_T$ for the **control** sample $i$ is defined as: $\Delta C_{T,C_{i}} = C_{T,X_{C,i}} - C_{T,R_{C,i}}$ 
 
According to [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/), the calibrator was estimated by the mean $\Delta C_{T,X_c}$ of the **control ($c$)** group: 
 $$\overline{\Delta C_{T,C}} = \frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i} \tag{1}$$
Then, we can define:
 - $\Delta\Delta C_{T,X_i} = \Delta C_{T,X_i} - \overline{\Delta C_{T,C}}$
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

Hence, the **left-hand side of equation (2)** is algebraically equal to its **right-hand side**, even though they originate from different forms. looks wired, right? Then what happened in here? Why do we divide the $2^{-\Delta\Delta C_{T,X_i}}$ by the averaged $2^{-\Delta\Delta C_{T,C}}$ of control group results in the exact value as the same as when we divide the $2^{-\Delta C_{T,X_i}}$ by the average $2^{-\Delta C_{T,C}}$ ?

 OK, let's go back to the paper of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/) and check the its ref\[[Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/)\].eq.(8):
 $$\frac{X_{N,q}}{X_{N,cb}}=\frac{K\times(1+E)^{-\Delta C_{T,q}}}{K\times(1+E)^{-\Delta C_{T,cb}}}=(1+E)^{-\Delta\Delta C_T}$$
According to the FIG.2 of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/), the $\Delta C_{T,cb}$ is the arithmetic mean of the $\Delta C_{T}$ in the control group. Therefore, the above ref\[[Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/)\].eq.(8) can be re-written as the below equation in the context of this blog:

$$ 2^{-\Delta\Delta C_{T,X_i}} = \frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}} = {2^{-\Delta C_{T,X_i}}}\div{2^{-\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}} \tag{3}$$

Have you noticed this part, ${2^{-\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}}$ ? This is the geometric mean of $2^{-\Delta C_{T,C_i}}$, because:

$$ {2^{-\frac{1}{n}\sum_{i=1}^{n}{\Delta C_{T,C_i}}}} = \sqrt[n]{2^{-\sum_{i=1}^{n}{\Delta C_{T,Ci}}}} = \sqrt[n]{2^{-\Delta C_{T, C_1}}\cdot2^{-\Delta C_{T, C_2}}\cdot 2^{-\Delta C_{T, C_3}}...2^{-\Delta C_{T, C_n}}} = (\prod^n_{i=1}{2^{-\Delta C_{T,C_i}}})^\frac{1}{n} \tag{4}$$


Therefore, the left side of eq.(2) is actually equal to:
$$ 2^{-\Delta C_{T,X_i}}\div\overline{2^{-\Delta C_{T,C}}} = 2^{-\Delta C_{T,X_i}}\div\frac{1}{n}\sum_{i=1}^{n}{2^{-\Delta C_{T,C_i}}} $$

Now, the story is totally clear, the left side of eq.(2) is the Arithmetic Mean version of $2^{-\Delta\Delta C_T}$. Let's denote it as:
$$ 2^{-\Delta\Delta{C_{T,X_i}}AM} = \frac{2^{-\Delta C_{T,X_i}}}{\overline{2^{-\Delta C_{T,C}}}} = 2^{-\Delta C_{T,X_i}}\div\frac{1}{n}\sum_{i=1}^{n}{2^{-\Delta C_{T,C_i}}} \tag{5}$$
Now, we can take the eq.(3) as the Geometric Mean of $2^{-\Delta\Delta C_T}$, which is the original in the paper of [Livak & Schmittgen, 2001](https://pubmed.ncbi.nlm.nih.gov/11846609/). For distinguish and convenience in this blog, let's denote it as $2^{-\Delta\Delta{C_{T,X_i}}GM}$.

This is interesting, because our above steps show something like below:
$$\frac{\cancel{Geometric\_Mean}[Sample]}{Arithmetic\_Mean[\cancel{Geometric\_Mean}[Sample]]} = \frac{Sample}{Arithmetic\_Mean[Sample]} \tag{6}$$
## Geometric mean vs Arithmetic mean

### Reason for using geometric mean normalization

Many tutorials and textbooks state that qPCR results often follow a **log-normal distribution**, and therefore recommend applying a log₂ transformation (e.g., for t-tests or ANOVA). However, when using the ΔΔCt method, the log₂ transformation is already embedded in the calculation:

$$\log_2(2^{-\Delta\Delta C_T}) = -\Delta\Delta C_T$$

In other words, we are essentially analyzing **ΔΔCt values directly** in the log space.

This raises a key question: **If our analysis is done in log space, shouldn't the summary statistics also respect the log scale?** Specifically, when we report mean fold changes, **shouldn't we use the geometric mean and geometric standard deviation**, rather than the arithmetic ones?

In fact, as shown in our derivation earlier, the original Livak & Schmittgen (2001) paper used the **arithmetic mean of ΔCₜ values** in the control group to compute the calibrator ΔCₜ. Mathematically, this is equivalent to computing the **geometric mean of the normalized expression values** ($2^{-\Delta C_T}$) (see **eq.4** in this post). Therefore, the fold change of expression in the control group is **implicitly defined via geometric averaging**.

Following the same logic, we should also apply **geometric averaging** to estimate the fold change of the treatment (experimental) group. That is, we calculate the arithmetic mean of the ΔCₜ values in that group, then back-transform using $2^{-\text{Mean}(\Delta C_T)}$(see **eq.4** in this post), which gives us the **geometric mean fold change**. This is **not** the same as taking the arithmetic mean of each sample’s $2^{-\Delta\Delta C_T}$ value.

So, the conclusion is:

> **Since the ΔΔCt method operates in log space, our statistical analysis should remain in log space, and fold changes should be reported as geometric means to preserve mathematical consistency and avoid distortion caused by skewed data distributions.**

### ### Reason for using the arithmetic mean normalization

There’s also a **valid statistical justification** for using the arithmetic mean—especially when the linearized expression values ($2^{-\Delta C_T}$ or $2^{-\Delta\Delta C_T}$) are themselves approximately **normally distributed**.

Let’s say your data (e.g., $2^{-\Delta C_T}$) follows a normal distribution. In this case, the **arithmetic mean** is the best unbiased estimator of central tendency, and standard parametric tests (like t-tests or ANOVA) are valid directly on these values. Then it makes perfect sense to define your calibrator using the **arithmetic mean of $2^{-\Delta C_T}$**, which leads naturally to computing $2^{-\Delta\Delta{C_{T,X_i}}AM}$ as we derived earlier in Eq.(5).

But here comes a subtle contradiction:

> In the original paper, Livak & Schmittgen defined the calibrator by taking the **arithmetic mean of ΔCₜ** values in the control group—not of the $2^{-\Delta C_T}$ values. However, in **Section 3**, they also demonstrated that **calculating variation directly on ΔCₜ underestimates variability**, while $2^{-C_T}$ better reflects technical variance.

So the question arises:  
**If we believe $2^{-\Delta C_T}$ better reflects variation, why don’t we define the calibrator using its arithmetic mean in the first place?**

The answer lies in the **mathematical structure of the ΔΔCt method itself**.

The ΔΔCt equation:
$$2^{-(\Delta C_{T,X_i} - \overline{\Delta C_{T,C}})} = \frac{2^{-\Delta C_{T,X_i}}}{2^{-\overline{\Delta C_{T,C}}}}$$
implicitly treats the calibrator as:
$$2^{-\overline{\Delta C_{T,C}}} = 2^{-\frac{1}{n} \sum_{i=1}^n \Delta C_{T,C_i}}$$  
which is the **geometric mean** of $2^{-\Delta C_T}$ (see **eq.4** in this post).

This creates a situation where:
- You’re computing your calibrator in **log space** (via mean ΔCₜ),
- But then reporting your results in **linear space** (fold change),
- While calculating group statistics using **arithmetic operations in linear space**.

This mathematical inconsistency may go unnoticed when the data are symmetrical and low-variance. However, in skewed or noisy data, it can lead to biased central tendencies.

> In short: If you prefer to use arithmetic mean for group-level fold change summaries, you should **also define your calibrator in linear space**, using the arithmetic mean of $2^{-\Delta C_T}$—not the mean of ΔCₜ. Otherwise, you mix geometric and arithmetic frameworks, which subtly breaks the consistency of the ΔΔCt model.

### My opinion?

Either is fine—**as long as you stay consistent**.

But here’s the real-world twist:

In practice, the **ΔΔCt method is rarely used for precise quantification**. What most researchers care about is not the exact fold-change number (e.g., 3.4× vs. 3.7×), but rather the **direction and significance** of the change. In this sense, the method has always been **more qualitative than quantitative** in application.

Since the original 2001 paper, **thousands of studies—including clinical trials and drug discovery pipelines—have mixed arithmetic and geometric normalizations** in fold-change reporting and statistics. And guess what? **It didn’t really matter**. Our biological conclusions still held. Drug candidates still moved forward. Misinterpretation due to this averaging mismatch was **statistically negligible**.

Why? Because of that when you perform **statistical hypothesis tests** (t-test, ANOVA, or even non-parametric tests like Wilcoxon),  your test statistic is calculated from the **ΔCt or ΔΔCt values**, and **any post hoc normalization of fold change values (whether via geometric or arithmetic mean)** has **no effect on the p-value**.

#### Quick examples:

- **t-test** compares group means:
	- Original t-test:
  $$ t = \frac{\overline{x}_1 - \overline{x}_2}{s_p \cdot \sqrt{\frac{1}{n_1}+\frac{1}{n_2}}} $$
	- After dividing all data by $c$:
$$
\text{New}\ t=\frac{\frac{\bar{x_1}}{c}-\frac{\bar{x_2}}{c}}{\frac{s_p}{c}\cdot\sqrt{\frac{1}{n_1}+\frac{1}{n_2}}}= \frac{\frac{\bar{x}_1}{c} - \frac{\bar{x}_2}{c}}{\frac{s_p}{c} \cdot \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}} = \frac{1}{c} \cdot \text{Numerator} \div \frac{1}{c} \cdot \text{Denominator} = \text{Same}\ t
$$
  where $x$ is ΔΔCt or any transformed version. Scaling or shifting the values (like subtracting a group mean) cancels out in the numerator and denominator. For example, let's say $x$ is $2^{-\Delta\Delta C_T}$ and $c$ is the arithmetic mean of  $2^{-\Delta\Delta C_T}$ in control group. Then, the New $t$ in the above is actually calculated from the Arithmetic Mean version of $2^{-\Delta\Delta C_T}$, the $t$ is finally the same, therefore the $P$-value is also the same.
- **ANOVA** partitions total variance and compares group means. The F-statistic is scale-invariant under uniform normalization. The F-statistic in ANOVA is a **ratio of variances**, so scaling all data by a constant ccc **scales both the numerator and denominator of the F-statistic by $c^2$**, which cancels out:
$$
F = \frac{\text{Between-group variance}}{\text{Within-group variance}} \rightarrow \text{unchanged}  
]
$$
- **Wilcoxon/Mann–Whitney** tests are based on **rank order**, and are **invariant under monotonic transformations**, including normalization by any mean.

> So whether you normalize using a geometric mean or an arithmetic one: **your statistical test results don’t change**, and your biological interpretation likely doesn’t either.

That said, being mathematically aware of what you’re doing is still important. If you mix geometric and arithmetic elements in your reporting, just **be transparent**. In 90% of use cases, it won’t mislead your readers—but in the 10% of cases where precision matters (e.g., modeling dose-response relationships), it’s good to be exact.

## 🧾 Final Summary: So... Should We Use Geometric Mean or Arithmetic Mean?

The ΔΔCt method, by design, operates in **logarithmic space**—you calculate Ct differences (ΔCt), then subtract a calibrator group’s mean ΔCt to get ΔΔCt, and finally back-transform via $2^{-\Delta\Delta C_T}$ to get fold change. Mathematically, this structure implies that the **calibrator is defined via a geometric mean**, and fold changes should logically also be summarized using **geometric averages**.

This view is consistent with:
- The **original 2001 Livak & Schmittgen paper**, which uses arithmetic mean ΔCt (→ geometric mean in fold-change space)
- The fact that **fold changes are multiplicative**, and thus best represented by geometric statistics

So if you’re aiming for mathematical consistency and statistical clarity—especially when reporting group-level averages—**geometric mean is the better choice**.

However, there are also valid **practical reasons** to use the **arithmetic mean**, particularly when:
- Your $2^{-\Delta C_T}$ or $2^{-\Delta\Delta C_T}$ values are approximately **normally distributed**
- You’re comparing **technical replicates**, where variation in linear space is of interest
- You want to maintain consistency with how many researchers have traditionally reported qPCR data

But here’s the key takeaway:

> ✅ **Either mean is fine**—**as long as you're consistent** between how you define your calibrator and how you summarize your group statistics.  
> ❌ **What’s not okay** is mixing spaces—e.g., computing ΔΔCt using log-space (ΔCt), but reporting arithmetic means of linear fold changes.

And most importantly—don’t stress too much:

In real-world applications, **ΔΔCt is used more for qualitative interpretation than for precise quantification**. Whether your normalization is based on the geometric or arithmetic mean of control group **has minimal or no effect** on statistical outcomes like *p-values*.

So be aware of the math. Respect the logic. But also remember:

> **This is biology—not a math exam. Context, consistency, and clarity matter more than strict formality.**

Whether you're writing a paper, presenting data, or building a pipeline—just choose a method that fits your goal, and stick with it transparently.
<div style="text-align: right; font-style: italic; margin-top: 2em;">
  — by WANG Ziyi <a href="https://github.com/wong-ziyi" target="_blank" style="color: #4078c0; text-decoration: none; font-weight: bold;">GitHub Profile</a>
</div>

## References
 - [https://www.gene-quantification.de/](https://www.gene-quantification.de/)
 - [Karlen Y, McNair A, Perseguers S, Mazza C, Mermod N. Statistical significance of quantitative PCR. BMC bioinformatics. 2007 Dec;8:1-6.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-131#Sec14)
 - [Vandesompele J, De Preter K, Pattyn F, Poppe B, Van Roy N, De Paepe A, Speleman F. Accurate normalization of real-time quantitative RT-PCR data by geometric averaging of multiple internal control genes. Genome biology. 2002 Jun;3:1-2.](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2002-3-7-research0034#Abs1)
 - [Nolan T, Hands RE, Bustin SA. Quantification of mRNA using real-time RT-PCR. Nature protocols. 2006 Aug;1(3):1559-82.](http://gene-quantification.org/nolan-hands-bustin-2006.pdf)
 - [Pfaffl MW. A new mathematical model for relative quantification in real-time RT–PCR. Nucleic acids research. 2001 May 1;29(9):e45-.](https://academic.oup.com/nar/article/29/9/e45/2384081)
 - [Yuan JS, Reed A, Chen F, Stewart CN. Statistical analysis of real-time PCR data. BMC bioinformatics. 2006 Dec;7:1-2.](https://link.springer.com/article/10.1186/1471-2105-7-85)
 - [Rao X, Huang X, Zhou Z, Lin X. An improvement of the 2ˆ (–delta delta CT) method for quantitative real-time polymerase chain reaction data analysis. Biostatistics, bioinformatics and biomathematics. 2013 Aug;3(3):71.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4280562/?utm_source=chatgpt.com)


---

If you found this helpful, feel free to comment, share, and follow for more. Your support encourages us to keep creating quality content.