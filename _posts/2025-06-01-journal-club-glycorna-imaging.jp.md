---
title: 'ARPLAによるGlycoRNAの空間可視化：アプタマー誘導型RCAアプローチ'
lang: jp
hidden: true
license: true
aside:
  toc: true
show_edit_on_github: true
pageview: true
tags: 日本語
---

<img src="https://visitor-badge.laobi.icu/badge?page_id=https://labonom.github.io/journalclub/2025/06/01/journal-club-glycorna-imaging.jp.html" alt="visitor badge"/> [![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/LabOnoM)

🌐 Other languages: [English](https://labonom.github.io/journalclub/2025/06/01/journal-club-glycorna-imaging.en.html){:.button.button--primary.button--rounded.button--xs} [日本語](https://labonom.github.io/2025/06/01/journal-club-glycorna-imaging.jp.html){:.button.button--primary.button--rounded.button--xs} [中文](https://labonom.github.io/2025/06/01/journal-club-glycorna-imaging.zh.html){:.button.button--primary.button--rounded.button--xs}

> 以下の内容は、英語の原文をもとに ChatGPT により自動翻訳されたものです。専門用語の正確さと表現の明瞭さに配慮しておりますが、参考用としてご利用ください。

## 1. 背景
RNA修飾は、転写後調節において重要な役割を果たしています。その中でも、**glycoRNA（糖修飾RNA）**は糖鎖が共有結合したRNAで、最近報告されたばかりで、未解明な点が多い生体分子クラスです。2021年、Flynnらにより初めてその存在が報告され、小型の糖修飾RNAが検出されました([Ryan, et al., Cell, 2021](https://pubmed.ncbi.nlm.nih.gov/34004145/))。しかし、適切なイメージング手法がなかったため、その細胞内分布や機能的役割の解明は困難でした。

この課題に対し、Maらは**ARPLA（Aptamer and RNA in situ hybridization-mediated Proximity Ligation Assay：アプタマーおよびRNA in situハイブリダイゼーションを用いた近接連結アッセイ）**と名付けた新しいin situイメージング法を開発しました。本手法は、高い空間分解能、選択性、配列特異性をもってglycoRNAを検出することを目的としています([Yuan Ma, et al., Nat Biotechnol, 2024](https://pubmed.ncbi.nlm.nih.gov/37217750/))。

![Presentation1](https://github.com/user-attachments/assets/7935a319-751e-4d3d-b58d-95019ac5c971)

<!--more-->

## 2. ARPLAの原理

ARPLAは2つの分子認識戦略を統合しています：
 - アプタマーによる糖鎖認識：一本鎖DNAアプタマーが、glycoRNA上に存在する唾液酸残基を特異的に認識します。
 - RNA in situハイブリダイゼーション（RISH）：DNAプローブが標的RNA配列にハイブリダイズします。

 ![Screenshot 2025-06-01 at 23 34 49](https://github.com/user-attachments/assets/83ad3ab8-35e0-458e-aaef-8b1a750c0cc8)

 両者の結合が近接して起こると、T4 DNAリガーゼにより2つのDNAアームが連結され、円形DNAが形成されます。これがテンプレートとなって**ローリングサークル増幅（RCA）**が進行し、繰り返し配列を持つ長鎖DNAが生成されます。その後、蛍光標識オリゴヌクレオチドとのハイブリダイゼーションによって可視化されます。

この二重認識機構により、特定の糖鎖とRNA配列の両方を有するRNAのみが選択的に可視化され、**特異性**と**シグナル対ノイズ比**が大幅に向上します。

### 2.1. アプタマーの背景

**アプタマー（aptamer）**は、特異的な三次構造を形成して標的分子（タンパク質、小分子、細胞など）に高い親和性と特異性で結合する短鎖の一本鎖DNAまたはRNA分子であり、抗体と類似の機能を果たします。

#### 2.1.1 技術的起源

アプタマーの概念は1990年に、2つの独立した研究により確立されました：
 - **Craig Tuerk** と **Larry Gold** は、SELEX（Systematic Evolution of Ligands by EXponential enrichment）法を開発し、T4 DNAポリメラーゼに結合するRNA配列の選別に成功しました（([C Tuerk, et al., Science, 1990](https://pubmed.ncbi.nlm.nih.gov/2200121/))。
 - **Andrew D. Ellington** と **Jack W. Szostak** は、有機色素に結合するRNA分子を選択するために類似のアプローチを用いました。彼らはこのような核酸リガンドを表すために、「適合する」を意味するラテン語の aptus と「部分」を意味するギリシャ語の meros に由来する「aptamer（アプタマー）」という用語を作り出しました([A D Ellington, et al., Nature, 1990](https://pubmed.ncbi.nlm.nih.gov/1697402/))。

 これらの研究により、SELEX法はアプタマー開発の基礎技術として定着しました。

#### 2.1.2 自然界における起源

自然界にもアプタマーに類似した構造が存在します。たとえばリボスイッチは、バクテリアmRNAの非翻訳領域に存在する構造化RNAで、代謝物に結合し、遺伝子発現を調節します。リガンド結合を担うのがアプタマー領域であり、遺伝子発現調節は発現プラットフォームが担います([Leurin Flemmich, et al., Nat Commun, 2021](https://pubmed.ncbi.nlm.nih.gov/34162884/))。

リボスイッチの存在は、RNAが遺伝情報の保存と酵素活性の両方を担っていたとされるRNAワールド仮説を支持する証拠でもあります([Kumari Kavita, et al., Trends Biochem Sci, 2022](https://pubmed.ncbi.nlm.nih.gov/36150954/))。

### 2.2. RCA（ローリングサークル増幅）の背景

**RCA（ローリングサークル増幅）**は、円形DNAテンプレートと鎖置換活性を持つDNAポリメラーゼを用いた、等温核酸増幅技術です。

#### 2.2.1 技術的起源
RCAは1990年代中頃に開発された技術で、円形DNAの増幅を目的としています。中核となる酵素は、バチルス・サブチリス由来ファージphi29のphi29 DNAポリメラーゼであり、高いプロセシビティと鎖置換能力を持っています([Wikipeida](https://en.wikipedia.org/wiki/Rolling_circle_replication); [M Monsur Ali, et al., Chem Soc Rev, 2014](https://pubmed.ncbi.nlm.nih.gov/24643375/))。

RCAは以下のような応用に利用されています：([phi29 DNA Polymerase, product webpage, Thermo Fisher](https://www.thermofisher.com/order/catalog/product/jp/en/EP0091))
 - DNAバイオセンサー
 - 近接連結アッセイ
 - in situハイブリダイゼーション

熱変性を必要としない等温性により、複雑な装置を必要とせず実施可能です。

#### 2.2.2 自然界における起源

RCAは、自然界で見られる**ローリングサークル複製（RCR）**に着想を得ています。これはファージ（例：φX174、M13）、プラスミド、ウイロイド、および一部の真核ウイルスが遺伝子複製に用いるメカニズムです。環状DNAに切れ目が入ることで一方向性の複製が始まり、連続的にコピーが生成されます([Shuzhen Yue, et al., Trends Biotechnol, 2021](https://pubmed.ncbi.nlm.nih.gov/33715868/))。

## 3. 実験的検証

著者らは、HeLa細胞を用いてARPLA法を検証しました。アプタマー、RISHプローブ、DNAアームのいずれかを欠くと、シグナル強度が著しく低下しました。また、糖鎖（PNGase-F、ノイラミニダーゼ、kifunensine）やRNA部分（RNase A/T1）を酵素処理または薬理学的に分解すると、シグナルが消失し、glycoRNAの存在が検出に不可欠であることが示されました。

使用されたアプタマー（Neu5Ac結合DNAアプタマー）は、ITCにより解離定数（Kd）約91 nMが測定され、唾液酸との高い親和性を示しました。無作為配列や非関連の糖鎖アプタマー（Tn抗原、GalNAc）ではシグナルが検出されませんでした。

### 3.1. 多様なglycoRNAと細胞タイプへの応用

ARPLAは、以下のglycoRNAの検出に適用されました：
 - **U1 snRNA**：スプライシングに関与、主に核内に局在
 - **U35a snoRNA**：rRNA修飾に関与
 - **Y5 RNA**：DNA複製やRNA安定性に関与

異なるクラス・局在を持つglycoRNAを対象に選定し、HeLa、SH-SY5Y、PANC-1、HEK293Tなど複数の細胞株において膜局在型glycoRNAが検出され、方法の汎用性が示されました。

### 3.2. 細胞内局在と輸送経路
共焦点顕微鏡観察により、glycoRNAは**リピッドラフト（脂質ラフト）**領域に富み、CT-B（コレラ毒素Bサブユニット）やGM1神経節糖脂質との共局在が確認されました。また、SNAREタンパク質（TSNARE1、VTI1B）との共局在も観察され、**小胞輸送**に関与している可能性が示唆されました。

これらの結果は、glycoRNAが分泌小胞を介して細胞膜に輸送されるモデルを支持しています。

### 3.3. がんおよび免疫細胞モデルへの応用

#### 3.3.1 がん進行

ARPLAは乳がんの3つの段階を示す細胞株で使用されました：
 - MCF-10A（非腫瘍性）
 - MCF-7（悪性）
 - MDA-MB-231（転移性）

U1、U35a、Y5 glycoRNAのシグナルは、悪性度の上昇に伴い減少しました。これは、がん細胞で一般的に観察される**過剰シアル化（hypersialylation）**とは逆の傾向であり、glycoRNAとタンパク質の糖修飾が独立して調節されている可能性を示唆します。

#### 3.3.2 免疫応答

THP-1単球をPMAでマクロファージに分化させると、glycoRNA量は低下しましたが、LPSで活性化されたマクロファージでは再びシグナルが上昇しました。これは、免疫応答においてglycoRNAが動的に制御されていることを示します。さらに、RNase処理により、細胞の内皮細胞への接着が低下し、glycoRNAが**免疫細胞と血管内皮**の相互作用に関与している可能性が示されました。

## 5. 限界

ARPLAは空間的・配列特異的なイメージングを提供しますが、いくつかの限界があります：
 - 配列情報が必須：未知のRNA配列を持つglycoRNAは検出不可
 - シグナル強度は中程度：低発現ターゲットでは検出が難しい
 - 分解能の制約：～300 nmで、近接分子の区別が困難
 - 半定量的：シグナルはglycoRNAの存在と相関するが、絶対分子数は測定不可

## 結論

ARPLAは、糖鎖認識のアプタマーとRNA配列特異的ハイブリダイゼーションを組み合わせた技術的に洗練された方法であり、glycoRNAの細胞内分布を明らかにするための強力な手段です。特にがんや免疫分野において有望です。今後は、プローブ設計やイメージング感度の向上によって、さらなる応用が期待されます。

<div style="text-align: right; font-style: italic; margin-top: 2em;">
    —— 抄読会にて翁瑶が発表 <a href="https://github.com/weng-yao" target="_blank" style="color: #4078c0; text-decoration: none; font-weight: bold;">@weng-yao</a>
</div>

---

この記事が参考になりましたら、ぜひコメント・共有・フォローをお願いいたします。皆さまの応援が、今後の質の高いコンテンツ制作の励みになります。