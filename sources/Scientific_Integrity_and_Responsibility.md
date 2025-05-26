---
layout: default
title: Scientific Integrity and Responsibility
---

<img src="https://visitor-badge.laobi.icu/badge?page_id=labonom.github.io/sources/Scientific_Integrity_and_Responsibility.html" alt="visitor badge"/>

# How We Uphold Scientific Integrity & Responsibility

## Why Scientific Integrity Matters

Scientific integrity is the foundation of credible and impactful research. By adhering to transparent, ethical, and reproducible practices, we ensure our discoveries contribute reliably to science and society.

## Our Principles

 - All studies undergo peer review and internal data audits.
 - All code and data are, where possible, made public.
 - Authorship follows ICMJE guidelines.
 - All human/animal studies comply with international or local ethics standards.
 - We welcome post-publication review and corrections.

---

## Real Case Studies

### 2025

---

#### Gingipain Regulates Isoform Switches of PD-L1 in Macrophages Infected with *Porphyromonas gingivalis*  
*Scientific Reports. 2025. [doi:10.1038/s41598-025-94954-7](https://doi.org/10.1038/s41598-025-94954-7)*  
**Authors:** Yilin Zheng, Ziyi Wang, Yao Weng, Heriati Sitosari, Yuhan He, Xiu Zhang, Noriko Shiotsu, Yoko Fukuhara, Mika Ikegame, Hirohiko Okamura

##### Summary of the Study

This study uncovered how gingipain, a toxic protease from the periodontal pathogen *P. gingivalis*, modulates the alternative splicing (AS) of the immune checkpoint protein PD-L1 in human macrophages, leading to the upregulation of a specific PD-L1 isoform that more effectively binds to PD-1 and inhibits immune function. Using RNA-sequencing, advanced bioinformatics, and AlphaFold 3 protein modeling, the team demonstrated that gingipain selectively increases the functional PD-L1IgV+ isoform, thus promoting immune evasion by the pathogen.

##### **How We Achieve Scientific Integrity in this study**

- **Open Data & Code:**  
  - All raw RNA-seq data is publicly available in [NCBI BioProject PRJNA1163056](https://www.ncbi.nlm.nih.gov/sra/?term=PRJNA1163056).
  - All data analysis results are accessible at [public repository](https://d3dcaz4rv8jgb4.cloudfront.net/).
  - Methods, custom bioinformatics scripts, and statistical protocols are fully described in the publication.

- **Transparent Authorship & Funding:**  
  - Each author’s contributions are clearly documented.
  - All funding sources (Japan JSPS grants) are disclosed.
  - The authors declare no competing interests.

- **Reproducibility:**  
  - Full details of experimental design, infection models, RNA-seq, protein validation, and computational analysis (including AlphaFold 3) are provided for independent replication.
  - Statistical rigor: FDR correction, reporting of all raw and normalized values, and use of established software (DESeq2, DEXSeq, IsoformSwitchAnalyzeR, etc.).

- **Ethical & Collaborative:**  
  - All cell line work was conducted following institutional guidelines.
  - Collaboration with external experts (e.g., for bacterial strains and advanced analytics) is fully acknowledged.

- **Community Sharing:**  
  - Raw data, analysis results, and all supplementary materials are shared online.
  - The group welcomes questions and requests for materials via the corresponding author.

[Read the full article](https://doi.org/10.1038/s41598-025-94954-7)

---

### 2024

---

#### O‐GlcNAcylation Regulates Osteoblast Differentiation Through Morphological Changes in Mitochondria, Cytoskeleton, and Endoplasmic Reticulum  
*BioFactors. 2024. [doi:10.1002/biof.2131](https://doi.org/10.1002/biof.2131)*  
**Authors:** Yao Weng, Ziyi Wang, Heriati Sitosari, Mitsuaki Ono, Hirohiko Okamura, Toshitaka Oohashi

##### Summary of the Study

This research uncovered the crucial role of O-GlcNAcylation—a post-translational modification—in regulating osteoblast differentiation via changes in mitochondria, cytoskeleton, and endoplasmic reticulum structure. Using a combination of bioinformatics, CRISPR/Cas9 gene editing, AI-assisted imaging, and rigorous validation, the team identified how Ogt knockout impairs osteoblast differentiation and mapped the regulatory network linking O-GlcNAcylation to mitochondrial and cytoskeletal function.

##### **How We Achieve Scientific Integrity in this study**

- **Open Data & Code:**  
  All primary data (immunofluorescence images, time-lapse imaging, Western blots, and more) as well as custom code and macros for image processing and bioinformatics are publicly available:  
   - [Mendeley Data (all original biomedical results and their corresponding processing and analysis steps)](https://data.mendeley.com/datasets/5ybkzhyp8y/1),
   - [Figshare repository 1: raw time lapse images of MC3T3-E1 osteoblastic-like cells with Ogt knock out](https://doi.org/10.6084/m9.figshare.25039688.v1),
   - [Figshare repository 2: raw AI training images](https://doi.org/10.6084/m9.figshare.25039712.v1),
   - [Interactive webpage to host all code script](https://dndy5us1uro9a.cloudfront.net),
   - [GitHub - modified AI Model](https://github.com/wong-ziyi/pytorch_fnet).

- **Transparent Authorship & Funding:**  
  Roles and contributions are clearly stated; all funding sources are disclosed, and there are no conflicts of interest.

- **Reproducibility:**  
  Full experimental methods, statistical analyses, and protocols are described in detail.

- **Ethical & Collaborative:**  
  Institutional standards followed; technical contributors and collaborators acknowledged.

- **Community Sharing:**  
  All resources and interactive tools are shared online; you'll be more than welcome any questions.

[Read the full article](https://doi.org/10.1002/biof.2131)

---

#### Inverse Genetics Tracing the Differentiation Pathway of Human Chondrocytes  
*Osteoarthritis and Cartilage. 2024. [doi:10.1016/j.joca.2024.06.009](https://doi.org/10.1016/j.joca.2024.06.009)*  
**Authors:** H.T. Do, M. Ono, Z. Wang, W. Kitagawa, A.T. Dang, T. Yonezawa, T. Kuboki, T. Oohashi, S. Kubota

##### Summary of the Study

This study established an "inverse genetics" approach to map how human chondrocytes are reprogrammed toward induced pluripotent stem cells (iPSCs). Using time-course single-cell RNA sequencing, the research tracked the transcriptomic transitions of chondrocytes, demonstrating that only a specific subpopulation silencing SOX9 along a proper pathway can achieve pluripotency, while others take alternative fates. The work highlights the role of cellular communication network factors (CCNs) and provides a model for tracing differentiation pathways backward to discover master regulatory genes.

##### **How We Achieve Scientific Integrity in this study**

- **Open Data & Software:**  
  - **All scRNA-seq data** are deposited in [NCBI GEO: GSE261806](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261806), enabling independent verification and re-use.
  - An **interactive R Shiny web tool** to explore gene expression, clustering, DEGs, and trajectory analyses is available online ([demo app](https://dwll26k42dcbb.cloudfront.net/GEO_Hang2024/)).
  - **Full source code** for the analysis (R Shiny/Seurat workflow) is deposited at [Mendeley Data (DOI: 10.17632/t38rw5fg82.1)](https://data.mendeley.com/datasets/t38rw5fg82/1).
  - All experimental protocols (vector construction, cell culture, reprogramming, scRNA-seq, and data processing) are described in detail in supplementary materials.

- **Transparent Authorship & Funding:**  
  - Author contributions are fully specified (CRediT taxonomy), covering conceptualization, methodology, data curation, analysis, writing, supervision, and funding acquisition.
  - Supported by JSPS KAKENHI (JP21K19603, JP23K17439); all funding and potential conflicts are disclosed (none declared).

- **Reproducibility & Rigor:**  
  - Experiments included multiple human donors and independent biological replicates.
  - Bioinformatics: Standardized pipelines for scRNA-seq analysis (CellRanger, Seurat, SCTransform, RNA velocity with scVelo, STREAM for trajectory).
  - Statistical methods: DEGs identified via Wilcoxon rank-sum test with Bonferroni correction; protocols for RT-qPCR validation are described and primer sequences provided.

- **Ethics & Acknowledgments:**  
  - All human cell work performed in compliance with institutional and ethical guidelines.
  - Technical and institutional support are acknowledged in the manuscript and supplementary materials.

- **Community Sharing:**  
  - Data, code, and online exploration tools are open to the community.
  - Additional resources, protocols, and reagents available upon reasonable request to the corresponding author.

[Read the full article](https://doi.org/10.1016/j.joca.2024.06.009)

---
