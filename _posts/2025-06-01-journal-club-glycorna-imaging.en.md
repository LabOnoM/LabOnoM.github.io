---
title: Spatial Visualization of GlycoRNAs via ARPLA - An Aptamer-Guided RCA Approach
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
tags:
  - JournalClub
  - glycoRNA
  - Aptamer
  - Rolling Circle Amplification
  - Imaging
---
# Spatial Visualization of GlycoRNAs via ARPLA: An Aptamer-Guided RCA Approach

## Background

RNA modifications are well-documented contributors to post-transcriptional regulation. Among them, glycoRNAs—RNAs conjugated with glycans—are a recently described and poorly understood class of biomolecules. Initial evidence for their existence was reported in 2021 by Flynn et al., who detected glycosylated small RNAs (Cell, 2021). However, due to a lack of suitable imaging methods, their precise cellular distribution and potential functional roles remained unclear.

To address this, Ma et al. (Nat Biotechnol, 2024) developed an in situ imaging method termed ARPLA (Aptamer and RNA in situ hybridization-mediated Proximity Ligation Assay). This method aims to detect glycoRNAs with high spatial resolution, selectivity, and sequence specificity.

![Presentation1](https://github.com/user-attachments/assets/7935a319-751e-4d3d-b58d-95019ac5c971)

## Principle of ARPLA

ARPLA combines two molecular recognition strategies:

Aptamer-based glycan recognition: A single-stranded DNA aptamer selectively binds to sialic acid residues commonly found on glycoRNAs.

RNA in situ hybridization (RISH): A DNA probe hybridizes to the target RNA sequence.

When both binding events occur in proximity, they enable ligation of two DNA arms via T4 DNA ligase. The resulting circular DNA serves as a template for rolling circle amplification (RCA), producing repeated DNA sequences that can be visualized by hybridization with fluorophore-labeled oligonucleotides.

This dual-recognition approach helps ensure that only RNAs bearing the specific glycan and matching sequence are amplified and visualized, enhancing both specificity and signal-to-noise ratio.

Experimental Validation
The authors validated ARPLA using HeLa cells as a model. Removal of any key component (aptamer, RISH probe, or ligation connectors) significantly reduced signal intensity. Additionally, enzymatic or pharmacologic degradation of either the glycan (e.g., PNGase-F, neuraminidase, kifunensine) or RNA moiety (RNase A/T1) also abolished signal, supporting the method’s dependence on intact glycoRNA.

The aptamer used (Neu5Ac-binding DNA aptamer) showed a dissociation constant (Kd) of ~91 nM by ITC, supporting its affinity for sialic acid. Control experiments using scrambled aptamers or unrelated glycan aptamers (e.g., Tn antigen, GalNAc) produced negligible signals.

Application to Different GlycoRNAs and Cell Types
ARPLA was applied to detect several glycoRNAs, including:

U1 snRNA: involved in splicing, primarily nuclear

U35a snoRNA: functions in rRNA modification

Y5 RNA: implicated in DNA replication and RNA stability

These targets were selected to represent different RNA classes and subcellular localizations. ARPLA successfully detected their membrane-associated glycoRNA forms in multiple cell lines (HeLa, SH-SY5Y, PANC-1, HEK293T), suggesting method generalizability.

Subcellular Localization and Intracellular Trafficking
Confocal microscopy revealed that glycoRNAs are enriched in lipid raft microdomains, as shown by colocalization with CT-B (cholera toxin B subunit) and ganglioside GM1. Additionally, glycoRNAs colocalized with SNARE proteins (TSNARE1 and VTI1B), suggesting possible involvement in vesicle-mediated exocytosis.

These observations support a model in which certain glycoRNAs are trafficked to the plasma membrane via secretory vesicles.

ARPLA in Cancer and Immune Cell Models
Cancer Progression
The authors applied ARPLA to breast cancer cell lines representing different stages of malignancy:

MCF-10A (non-tumorigenic)

MCF-7 (malignant)

MDA-MB-231 (metastatic)

ARPLA signal intensity for U1, U35a, and Y5 glycoRNAs decreased with increasing malignancy. Notably, this trend contrasts with the observed hypersialylation in cancer cells, suggesting that glycoRNAs and protein glycosylation may be regulated independently.

Immune Differentiation and Activation
In THP-1 monocytes undergoing PMA-induced differentiation to macrophages, glycoRNA levels decreased. However, LPS activation of macrophages led to re-elevation of glycoRNA signal, indicating dynamic regulation during immune response. RNase treatment reduced cell adhesion to endothelial layers, suggesting a possible role for glycoRNAs in immune cell–endothelium interactions.

Limitations
While ARPLA provides valuable spatial and sequence-specific imaging, the method has certain limitations:

Requires prior sequence knowledge: Cannot detect glycoRNAs with unknown RNA sequences.

Moderate signal intensity: Though distinguishable from background, fluorescent signals may be weak for low-abundance targets.

Resolution limit: Estimated at ~300 nm, which may limit visualization of closely spaced molecules.

Semi-quantitative: Signal intensity correlates with glycoRNA presence but does not provide absolute molecule counts.

Conclusion
ARPLA represents a technically sound advancement in glycoRNA imaging by integrating aptamer-based glycan detection and sequence-specific hybridization. It provides new opportunities to investigate glycoRNA distribution in normal and disease contexts, especially in cancer and immunology. Future improvements in probe design and imaging sensitivity could further expand its utility.

<div style="text-align: right; font-style: italic; margin-top: 2em;">
  — Presented in Journal Club by WENG Yao <a href="https://github.com/weng-yao" target="_blank" style="color: #4078c0; text-decoration: none; font-weight: bold;">@weng-yao</a>
</div>
