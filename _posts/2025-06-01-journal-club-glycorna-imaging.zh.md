---
title: '通过ARPLA实现GlycoRNA的空间可视化：一种由适配体引导的RCA方法'
lang: zh
hidden: true
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
tags: 中文
---

<img src="https://visitor-badge.laobi.icu/badge?page_id=https://labonom.github.io/journalclub/2025/06/01/journal-club-glycorna-imaging.zh.html" alt="visitor badge"/> [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/LabOnoM)

🌐 Other languages: [English](https://labonom.github.io/journalclub/2025/06/01/journal-club-glycorna-imaging.en.html){:.button.button--primary.button--rounded.button--xs} [日本語](https://labonom.github.io/2025/06/01/journal-club-glycorna-imaging.jp.html){:.button.button--primary.button--rounded.button--xs} [中文](https://labonom.github.io/2025/06/01/journal-club-glycorna-imaging.zh.html){:.button.button--primary.button--rounded.button--xs}

> 以下内容由 ChatGPT 根据英文原文自动翻译，已尽量保持术语准确性和表达清晰度，供参考。

# 背景

RNA修饰在转录后调控中发挥着重要作用。其中，**glycoRNA（糖化RNA）**，即与糖链共轭的RNA，是近年来被发现但仍未被充分理解的一类新型生物分子。Flynn 等人于2021年首次报道了其存在，并检测到糖基化的小RNA([Ryan, et al., Cell, 2021](https://pubmed.ncbi.nlm.nih.gov/34004145/))。然而，由于缺乏合适的成像方法，其在细胞中的具体分布和潜在功能仍不清楚。

为了解决这一问题，Ma 等人开发了一种原位成像新技术，命名为 ARPLA（Aptamer and RNA in situ hybridization-mediated Proximity Ligation Assay，适配体与RNA原位杂交介导的近邻连接反应）。该方法旨在实现对glycoRNA的高空间分辨率、高选择性及序列特异性检测 ([Yuan Ma, et al., Nat Biotechnol, 2024](https://pubmed.ncbi.nlm.nih.gov/37217750/))。

![Presentation1](https://github.com/user-attachments/assets/7935a319-751e-4d3d-b58d-95019ac5c971)

<!--more-->

## ARPLA 原理

ARPLA整合了两种分子识别策略：
 - **基于核算适配体的糖链识别**：一种单链DNA适配体可选择性结合glycoRNA上常见的唾液酸残基；
 - **RNA原位杂交（RISH）**：DNA探针与目标RNA序列发生杂交。

 ![Screenshot 2025-06-01 at 23 34 49](https://github.com/user-attachments/assets/83ad3ab8-35e0-458e-aaef-8b1a750c0cc8)


当这两个识别事件在空间上接近时，它们能借助T4 DNA连接酶实现连接，从而形成闭合的DNA环结构。此闭环DNA可作为**滚环扩增（RCA）**的模板，通过聚合酶反应产生大量重复序列，随后使用荧光标记的寡核苷酸进行可视化检测。

这一双重识别策略可确保仅有同时具有特定糖链和序列的RNA才被扩增和成像，从而提高检测的**特异性**与**信噪比**。

### 背景介绍：核算适配体

**核算适配体（Aptamer）**是短的单链DNA或RNA分子，能够折叠形成特定的三维结构，从而以高亲和力和高特异性结合目标分子，如蛋白质、小分子，甚至是细胞。功能上类似于抗体。

#### 技术来源

核算适配体的概念始于1990年，两项独立研究奠定了其基础：
- **Craig Tuerk** 和 **Larry Gold** 首次提出了SELEX（系统进化筛选）技术，展示了可选择与噬菌体T4 DNA聚合酶结合的RNA序列 ([C Tuerk, et al., Science, 1990](https://pubmed.ncbi.nlm.nih.gov/2200121/))；
 - **Andrew D. Ellington** 和 **Jack W. Szostak** 采用类似的方法筛选能够与有机染料结合的RNA分子。他们创造了“aptamer（适配体）”这一术语，来源于拉丁语“aptus”（适合）和希腊语“meros”（部分），用以描述这类核酸适配体 ([A D Ellington, et al., Nature, 1990](https://pubmed.ncbi.nlm.nih.gov/1697402/))。

这两项开创性研究奠定了适配体筛选的基础技术——SELEX。

#### 自然来源

自然界中也存在类似核算适配体结构的RNA，称为核糖开关（Riboswitch）。它们通常存在于细菌mRNA的非翻译区，可结合小分子代谢物，并根据其浓度调控基因表达。其中，核算适配体结构域负责识别配体，而表达平台则调控下游基因表达 ([Leurin Flemmich, et al., Nat Commun, 2021](https://pubmed.ncbi.nlm.nih.gov/34162884/))。

核糖开关的存在也支持“RNA世界假说”（RNA World Hypothesis），即生命早期可能完全依赖RNA进行遗传信息的储存和催化功能 ([Kumari Kavita, et al., Trends Biochem Sci, 2022](https://pubmed.ncbi.nlm.nih.gov/36150954/))。

### 背景介绍：滚环扩增（RCA）

**滚环扩增（RCA）**是一种等温核酸扩增技术，利用圆形DNA模板和具备链置换能力的DNA聚合酶，合成长链单链DNA或RNA。

#### 技术来源

RCA技术始于1990年代中期，用于扩增圆形DNA模板。核心酶为phi29 DNA聚合酶，源自枯草芽孢杆菌噬菌体phi29。该酶具有高过程性和强链置换活性，非常适合RCA使用 ([Wikipeida](https://en.wikipedia.org/wiki/Rolling_circle_replication); [M Monsur Ali, et al., Chem Soc Rev, 2014](https://pubmed.ncbi.nlm.nih.gov/24643375/))。

RCA的应用包括但不限于：([phi29 DNA Polymerase, product webpage, Thermo Fisher](https://www.thermofisher.com/order/catalog/product/jp/en/EP0091))
 - DNA生物传感器
 - 近邻连接反应
 - 原位杂交成像

其等温性质无需热循环设备，简化了实验平台。

#### 自然来源

RCA技术的灵感来自于自然界中的滚环复制（RCR），被用于复制各种圆形DNA或RNA。其天然实例包括：噬菌体（如φX174、M13）、质粒、类病毒及部分真核病毒。在RCR中，DNA上的切口引发单向复制，从而连续产生多个拷贝 ([Shuzhen Yue, et al., Trends Biotechnol, 2021](https://pubmed.ncbi.nlm.nih.gov/33715868/))。

## 实验验证

作者使用HeLa细胞模型验证了ARPLA方法。若缺失任一关键组分（核算适配体、RISH探针、连接臂），信号强度显著下降。此外，酶解或药物处理去除糖链（如PNGase-F、神经氨酸酶、kifunensine）或RNA片段（RNase A/T1）均可导致信号丧失，证明该方法对完整glycoRNA的依赖性。

所用核算适配体为Neu5Ac结合型DNA适配体，通过等温滴定量热法（ITC）测得其解离常数Kd约为91 nM，表明其具有良好的结合亲和力。使用无序适配体或识别不同糖链（如Tn抗原、GalNAc）的适配体均未产生明显信号。

### 不同GlycoRNA与细胞类型中的应用

ARPLA成功检测了几种glycoRNA，包括：
 - **U1 snRNA**：参与剪接，主要定位于细胞核；
 - **U35a snoRNA**：功能为rRNA修饰；
 - **Y5 RNA**：与DNA复制和RNA稳定性相关。

这些RNA代表了不同类别及亚细胞定位。ARPLA在多种细胞系（HeLa, SH-SY5Y, PANC-1, HEK293T）中均能成功检测其膜相关形式，表明该方法具有较强的普适性。

### 亚细胞定位与胞内转运

共聚焦显微成像显示glycoRNA富集于**脂筏微区**，表现为与CT-B（霍乱毒素B亚基）和GM1神经节苷脂共定位。此外，其还与SNARE蛋白（TSNARE1和VTI1B）共定位，提示其可能参与**囊泡介导的分泌过程**。

这些结果支持一种模型：特定glycoRNA可通过分泌囊泡被转运至质膜。

### 在癌症与免疫细胞模型中的应用

#### 癌症进展

作者使用ARPLA检测乳腺癌细胞中glycoRNA表达，覆盖不同恶性程度的细胞系：
 - MCF-10A（非肿瘤性）
 - MCF-7（恶性）
 - MDA-MB-231（转移性）

结果显示，U1、U35a和Y5 glycoRNA的ARPLA信号随恶性程度升高而下降。这一趋势与癌细胞中常见的**高唾液酸化（hypersialylation）**相反，提示glycoRNA与蛋白糖基化可能存在独立调控机制。

#### 免疫激活

在PMA诱导THP-1单核细胞向巨噬细胞分化过程中，glycoRNA水平下降。而经LPS刺激激活的巨噬细胞，其glycoRNA信号重新上升，提示在免疫应答过程中glycoRNA呈动态调控状态。RNase处理还显著降低细胞与内皮层的黏附能力，表明glycoRNA可能参与**免疫细胞与内皮细胞的相互作用**。

## 方法局限性

尽管ARPLA在空间定位和序列特异性方面具有优势，但仍存在以下限制：
 - 需已知序列信息：无法检测未知序列的glycoRNA；
 - 信号强度有限：对于低丰度目标，荧光信号可能较弱；
 - 分辨率受限：约为300纳米，难以区分彼此靠近的分子；
 - 半定量性质：信号强度与glycoRNA丰度相关，但无法提供绝对分子数。

## 总结

ARPLA结合了适配体识别糖链与RNA序列杂交，技术路线严谨，为glycoRNA的成像分析提供了新工具，尤其在肿瘤与免疫研究中具有广泛前景。未来可通过优化探针设计与成像灵敏度进一步提升其应用价值。

<div style="text-align: right; font-style: italic; margin-top: 2em;">
     —— 由翁瑶于文献研讨会中介绍 <a href="https://github.com/weng-yao" target="_blank" style="color: #4078c0; text-decoration: none; font-weight: bold;">@weng-yao</a>
</div>

---

如果你觉得这篇文章有帮助，欢迎点赞评论、分享转发，并关注我们获取更多优质内容。你的支持是我们持续创作的最大动力。



 