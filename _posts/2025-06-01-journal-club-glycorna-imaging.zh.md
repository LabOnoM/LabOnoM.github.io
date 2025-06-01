---
title: '通过ARPLA实现GlycoRNA的空间可视化：一种由适配体引导的RCA方法'
lang: en
categories: journalclub
hidden: true
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
---

<img src="https://visitor-badge.laobi.icu/badge?page_id=https://labonom.github.io/journalclub/2025/06/01/journal-club-glycorna-imaging.zh.html" alt="visitor badge"/> [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/LabOnoM)

🌐 Other languages: [English]({{ "/2025/06/01/journal-club-glycorna-imaging.en.html" | relative_url }}) |

# 背景

RNA修饰在转录后调控中发挥着重要作用。其中，**glycoRNA（糖化RNA）**，即与糖链共轭的RNA，是近年来被发现但仍未被充分理解的一类新型生物分子。Flynn 等人于2021年首次报道了其存在，并检测到糖基化的小RNA([Ryan, et al., Cell, 2021](https://pubmed.ncbi.nlm.nih.gov/34004145/))。然而，由于缺乏合适的成像方法，其在细胞中的具体分布和潜在功能仍不清楚。

为了解决这一问题，Ma 等人开发了一种原位成像新技术，命名为 ARPLA（Aptamer and RNA in situ hybridization-mediated Proximity Ligation Assay，适配体与RNA原位杂交介导的近邻连接反应）。该方法旨在实现对glycoRNA的高空间分辨率、高选择性及序列特异性检测 ([Yuan Ma, et al., Nat Biotechnol, 2024](https://pubmed.ncbi.nlm.nih.gov/37217750/))。

![Presentation1](https://github.com/user-attachments/assets/7935a319-751e-4d3d-b58d-95019ac5c971)

<!--more-->

## ARPLA 原理

ARPLA整合了两种分子识别策略：
 - 基于适配体的糖链识别：一种单链DNA适配体可选择性结合glycoRNA上常见的唾液酸残基；
 - RNA原位杂交（RISH）：DNA探针与目标RNA序列发生杂交。