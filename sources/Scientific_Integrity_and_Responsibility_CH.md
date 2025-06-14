---
layout: default
title: Scientific Integrity and Responsibility
---

<!-- Info Row: Visitor count + GitHub profile -->
<div style="margin-top: 10px; margin-bottom: 8px;">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=labonom.github.io/sources/Open_Innovation.html" alt="visitor badge"/>
  <a href="https://github.com/LabOnoM">
    <img src="https://img.shields.io/badge/GitHub-Profile-black?logo=github" alt="GitHub badge"/>
  </a>
</div>

<!-- Language Switch Row -->
<div>
  <a href="/sources/Scientific_Integrity_and_Responsibility.html" style="padding: 6px 12px; border: 1px solid #ccc; background-color: #f0f0f0; text-decoration: none; border-radius: 4px; margin-right: 8px;">English</a>
  <a href="/sources/Scientific_Integrity_and_Responsibility_JP.html" style="padding: 6px 12px; border: 1px solid #ccc; background-color: #f0f0f0; text-decoration: none; border-radius: 4px; margin-right: 8px;">日本語</a>
  <a href="/sources/Scientific_Integrity_and_Responsibility_CH.html" style="padding: 6px 12px; border: 1px solid #ccc; background-color: #f0f0f0; text-decoration: none; border-radius: 4px;">中文</a>
</div>

# 我们如何践行科学诚信与责任

## 为什么科学诚信至关重要

科学诚信是可信与有影响力研究的基石。通过坚持透明、伦理和可重复的实践，我们确保我们的研究发现能够可靠地服务于科学与社会。

## 我们的基本原则

- 所有研究都接受同行评审和内部数据审核。
- 所有代码与数据在可行的情况下都会公开。
- 作者署名遵循 ICMJE（国际医学期刊编辑委员会）标准。
- 所有人体/动物实验均遵守国际或本地伦理规范。
- 我们欢迎发表后的评审与修正。

---

## 实例研究

### 2025年

---

#### Gingipain调控被*Porphyromonas gingivalis*感染的巨噬细胞中PD-L1的可变剪接
*Scientific Reports. 2025. [doi:10.1038/s41598-025-94954-7](https://doi.org/10.1038/s41598-025-94954-7)*

##### 研究摘要

本研究揭示了牙周病菌 *P. gingivalis* 的毒性蛋白酶Gingipain如何通过调控免疫检查点蛋白PD-L1的可变剪接（AS），在巨噬细胞中促进特定PD-L1亚型（PD-L1IgV+）的表达，从而增强其与PD-1结合并抑制免疫反应。研究结合了RNA测序、高级生物信息学和AlphaFold 3结构预测技术，揭示了该病原体逃避免疫监测的机制。

##### 本研究如何践行科学诚信

- **数据与代码公开：**
  - 原始RNA-seq数据已上传至 [NCBI BioProject PRJNA1163056](https://www.ncbi.nlm.nih.gov/sra/?term=PRJNA1163056)
  - 所有数据分析结果可访问：[公共数据仓库](https://d3dcaz4rv8jgb4.cloudfront.net/)
  - 论文中详细描述了方法、定制脚本和统计方案

- **作者与资助信息透明：**
  - 明确列出各作者的贡献
  - 所有资助来源（日本学术振兴会）均有披露
  - 无利益冲突声明

- **可重复性保障：**
  - 提供了实验设计、感染模型、RNA-seq、蛋白验证和计算分析（含AlphaFold 3）的完整细节
  - 采用FDR校正，报告所有原始及标准化数据，使用DESeq2、DEXSeq、IsoformSwitchAnalyzeR等标准软件

- **伦理与协作：**
  - 所有细胞实验均遵守机构伦理指南
  - 明确列出外部合作者（如菌株与分析专家）

- **共享与社区参与：**
  - 所有原始数据、分析结果和补充资料均在线共享
  - 通讯作者接受材料请求与提问

---

### 2024年

---

#### O-GlcNAc糖基化通过影响线粒体、细胞骨架和内质网形态调控成骨细胞分化
*BioFactors. 2024. [doi:10.1002/biof.2131](https://doi.org/10.1002/biof.2131)*

##### 研究摘要

本研究揭示了翻译后修饰O-GlcNAcylation在成骨细胞分化中的核心作用。研究结合生物信息学、CRISPR/Cas9基因编辑、AI辅助影像分析等手段，表明Ogt缺失会导致分化受阻，并绘制出糖基化与线粒体和细胞骨架调控之间的网络。

##### 本研究如何践行科学诚信

- **数据与代码公开：**
  所有原始数据（免疫荧光图像、延时成像、Western blot等）及图像处理与分析代码全部公开：
  - [Mendeley 数据库](https://data.mendeley.com/datasets/5ybkzhyp8y/1)
  - [Figshare 时间序列图像](https://doi.org/10.6084/m9.figshare.25039688.v1)
  - [Figshare AI训练图像](https://doi.org/10.6084/m9.figshare.25039712.v1)
  - [代码网页](https://dndy5us1uro9a.cloudfront.net)
  - [GitHub 模型代码](https://github.com/wong-ziyi/pytorch_fnet)

- **作者与资助信息透明：**
  - 明确列出作者分工
  - 全部资助信息公开，无利益冲突

- **可重复性保障：**
  - 提供完整的实验、统计与分析流程

- **伦理与协作：**
  - 遵循机构伦理规范，技术人员与合作者获得致谢

- **共享与社区参与：**
  - 所有数据与交互式工具开放共享，欢迎提问交流

---

#### 逆遗传学追踪人软骨细胞的分化路径
*Osteoarthritis and Cartilage. 2024. [doi:10.1016/j.joca.2024.06.009](https://doi.org/10.1016/j.joca.2024.06.009)*

##### 研究摘要

本研究提出“逆遗传学”策略，通过时间分辨单细胞转录组（scRNA-seq）技术，追踪人软骨细胞如何向iPS细胞重编程。结果显示，只有特定SOX9沉默的细胞群体可实现多能性，其他群体则走向不同命运。同时指出了CCN（细胞通信网络）因子的关键作用，并建立了识别主调控基因的模型。

##### 本研究如何践行科学诚信

- **数据与软件公开：**
  - 所有scRNA-seq数据：[GEO: GSE261806](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261806)
  - 交互式Web工具：[Shiny Demo](https://dwll26k42dcbb.cloudfront.net/GEO_Hang2024/)
  - 全部分析代码：[Mendeley DOI: 10.17632/t38rw5fg82.1](https://data.mendeley.com/datasets/t38rw5fg82/1)
  - 实验步骤与试剂信息详列于补充材料

- **作者与资助信息透明：**
  - 作者贡献遵循CRediT分类标准：概念、方法、数据处理、分析、写作、监督、资金等
  - 日本科研基金JSPS资助（JP21K19603, JP23K17439），无利益冲突

- **可重复性与严谨性：**
  - 实验包括多个供体与独立重复组
  - 生信流程标准化：CellRanger, Seurat, SCTransform, RNA velocity, STREAM等
  - DEG分析采用Wilcoxon秩和检验并进行Bonferroni校正；RT-qPCR验证与引物序列提供

- **伦理与致谢：**
  - 所有人体细胞实验符合伦理标准
  - 技术和机构支持均在文中致谢

- **共享与社区参与：**
  - 数据、代码与可视化工具完全开放
  - 额外资源和实验材料可通过通讯作者请求获取

---
