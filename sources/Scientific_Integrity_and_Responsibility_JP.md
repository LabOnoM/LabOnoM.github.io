---
layout: default
title: Scientific Integrity and Responsibility
---

<!-- Info Row: Visitor count + GitHub profile -->
<div style="margin-top: 10px; margin-bottom: 8px;">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=labonom.github.io/sources/Open_Innovation_JP.html" alt="visitor badge"/>
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

# 科学的誠実性と責任の確保方法

## なぜ科学的誠実性が重要なのか

科学的誠実性は、信頼性と社会的意義のある研究の土台です。透明性・倫理性・再現性のある実践に従うことで、私たちの発見が確実に科学と社会に貢献することを保証します。

## 私たちの基本方針

- すべての研究は査読と内部データ監査を受けています。
- コードやデータは、可能な限り公開されています。
- 著者資格はICMJE（医学雑誌編集者国際委員会）ガイドラインに従っています。
- ヒト・動物を対象とした研究は、国際または地域の倫理基準に準拠しています。
- 出版後のフィードバックや修正も歓迎します。

---

## 実例紹介

### 2025年

---

#### 『Porphyromonas gingivalis』感染マクロファージにおけるPD-L1アイソフォームスイッチを制御するGingipain
*Scientific Reports. 2025. [doi:10.1038/s41598-025-94954-7](https://doi.org/10.1038/s41598-025-94954-7)*

##### 研究概要

歯周病原菌 *P. gingivalis* の毒性プロテアーゼであるGingipainが、ヒトマクロファージにおける免疫チェックポイントタンパク質PD-L1の選択的スプライシング（AS）を制御し、免疫抑制能の高いPD-L1IgV+アイソフォームを選択的に増加させることを明らかにしました。RNA-seq、バイオインフォマティクス、AlphaFold 3を用いた構造予測により、病原体の免疫回避戦略が示されました。

##### 科学的誠実性の実践

- **データとコードの公開：**
  - 生RNA-seqデータ：[NCBI BioProject PRJNA1163056](https://www.ncbi.nlm.nih.gov/sra/?term=PRJNA1163056)
  - 全解析結果：[公開リポジトリ](https://d3dcaz4rv8jgb4.cloudfront.net/)
  - 解析手法、スクリプト、統計処理は論文に完全記載

- **著者情報と資金の透明性：**
  - 著者ごとの貢献内容を記録
  - 資金源（日本学術振興会）を明示
  - 利益相反なし

- **再現性の確保：**
  - 実験設計、感染モデル、解析手法の詳細記載
  - FDR補正、DESeq2・DEXSeqなど信頼性のあるソフトを使用

- **倫理・協働：**
  - 細胞実験は機関の倫理ガイドラインに準拠
  - 外部研究者との協力も明記

- **コミュニティへの共有：**
  - すべてのデータ・補足資料をオンライン公開
  - コレスポンディングオーサー経由で質問受付

---

### 2024年

---

#### O-GlcNAc修飾はミトコンドリア・細胞骨格・小胞体の構造変化を通じて骨芽細胞分化を制御する
*BioFactors. 2024. [doi:10.1002/biof.2131](https://doi.org/10.1002/biof.2131)*

##### 研究概要

翻訳後修飾の一種であるO-GlcNAcylationが、ミトコンドリア、細胞骨格、小胞体構造に影響を与え、骨芽細胞の分化に重要な役割を果たすことを解明。CRISPR/Cas9遺伝子編集、AI支援画像解析、バイオインフォマティクスを組み合わせてOgtノックアウトによる分化阻害の分子機構を明らかにしました。

##### 科学的誠実性の実践

- **データとコードの公開：**
  - すべての実験データ・画像・解析コードを以下で公開：
    - [Mendeley Data](https://data.mendeley.com/datasets/5ybkzhyp8y/1)
    - [Figshare: Time-lapse画像](https://doi.org/10.6084/m9.figshare.25039688.v1)
    - [Figshare: AI訓練用画像](https://doi.org/10.6084/m9.figshare.25039712.v1)
    - [実行環境](https://dndy5us1uro9a.cloudfront.net)
    - [GitHub - AIモデル](https://github.com/wong-ziyi/pytorch_fnet)

- **著者情報と資金の透明性：**
  - 著者の役割と資金提供を明記
  - 利益相反なし

- **再現性の確保：**
  - 実験方法、統計解析、画像処理の詳細を記載

- **倫理と協働：**
  - 機関の倫理規定に準拠
  - 外部貢献者を明記

- **コミュニティへの共有：**
  - すべての資源・ツールをオンラインで公開

---

#### インバースジェネティクスによるヒト軟骨細胞の分化経路追跡
*Osteoarthritis and Cartilage. 2024. [doi:10.1016/j.joca.2024.06.009](https://doi.org/10.1016/j.joca.2024.06.009)*

##### 研究概要

ヒト軟骨細胞がiPS細胞へと再プログラムされる過程を時間経過に沿ってscRNA-seqで解析し、SOX9を抑制する特定の細胞群だけが多能性を獲得できることを解明しました。細胞間コミュニケーションネットワーク（CCNs）の重要性を示し、逆方向から分化制御因子を特定するモデルを構築しました。

##### 科学的誠実性の実践

- **データとソフトウェアの公開：**
  - scRNA-seqデータ：[GEO: GSE261806](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE261806)
  - Webツール：[Shinyアプリ](https://dwll26k42dcbb.cloudfront.net/GEO_Hang2024/)
  - 全コード：[Mendeley Data (DOI:10.17632/t38rw5fg82.1)](https://data.mendeley.com/datasets/t38rw5fg82/1)

- **著者情報と資金の透明性：**
  - CRediT分類に基づいて貢献を記載
  - 科研費（JP21K19603, JP23K17439）による支援、利益相反なし

- **再現性と厳密性：**
  - 複数ドナー使用、独立な生物学的リプリケートあり
  - Seurat、RNA velocity、STREAM等の標準パイプライン使用
  - Wilcoxon検定＋Bonferroni補正、qPCR検証あり

- **倫理と謝辞：**
  - 倫理規定に準拠
  - 技術支援と機関支援を謝辞に記載

- **コミュニティへの共有：**
  - データ・コード・解析ツールをすべて公開
  - リソースリクエストは対応可能

---
