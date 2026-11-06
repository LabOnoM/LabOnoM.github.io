---
id: ana-zebrafish-model-and-spaceflight
type: analysis
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-10-zebrafish-history.md
  - _posts/PostAttachedFiles/NatureLifeCycleVsLabLifeCycle.png
  - _posts/PostAttachedFiles/Zebrafish-evolution-and-range.png
  - index.html
  - .wiki/entities/zebrafish-history.md
tags:
  - analysis
  - zebrafish
  - danio-rerio
  - developmental-biology
  - spaceflight
---

# Domain Review: Zebrafish (*Danio rerio*) History, Husbandry, & LabOnoM Craniofacial Models

## Cross-Links
- **Figures**: [[fig-zebrafish-and-software-panels]]
- **Flagged Contradiction**: [[contradictions]] (`CON-07`)
- **Project Overview**: [[overview]]

## 1. Historical & Experimental Synthesis (`_posts/2025-06-10-zebrafish-history.md`)
- **Taxonomy & Biogeography**: Described by Francis Hamilton (`1822`) from the Kosi/Ganges basin in northeastern India (*Danio rerio*, sister to *D. aesculapii* in the *Danio* clade; `Zebrafish-evolution-and-range.png`).
- **Husbandry & Genetic Standardization**:
  - `1851`: Early glass aquarium maintenance; `1934`: Charles W. Creaser introduced zebrafish embryology to US teaching/research laboratories.
  - `1968–1981`: **George Streisinger** (University of Oregon) established the **`AB` line**, isolated the recessive `golden` pigmentation locus, and pioneered **homozygous diploid clonal zebrafish** via heat-shock / hydrostatic-pressure suppression of first cleavage (*Nature* 1981).
  - `1990s`: **Wolfgang Driever** (Boston) and **Christiane Nüsslein-Volhard** (Tübingen, **`TU` strain**) conducted large-scale ENU forward-genetic screens (*Development* 1996 special issue), isolating **`>6,000` embryonic developmental mutants**.
  - `2013`: Howe *et al.* (*Nature* 2013) published the `GRCz` reference genome demonstrating that **~70% of human protein-coding genes** (`>80%` of human disease-associated genes) have at least one zebrafish ortholog.
- **Neuroethology & Live Optical Readouts**:
  - Transparent embryos hatch at `~3 dpf` (`28°C`) and initiate free-swimming exogenous feeding at `5 dpf`, maturing in `~90 dpf` under constant laboratory conditions versus `~10 months` under wild Indian monsoon seasonality (`NatureLifeCycleVsLabLifeCycle.png`).
  - Supports whole-brain `GCaMP` two-photon calcium imaging, optogenetics, looming-shadow Mauthner-cell escape circuit mapping, and CRISPR-Cas9 F0 crispant screening.
- **Orbital Microgravity Milestones**:
  - `1976`: Soviet **`Soyuz 21` / `Salyut 5`** carried early zebrafish developmental experiments.
  - `2024-04`: China's **`Shenzhou 18`** (`Tiangong` space station) maintained **`4` adult zebrafish (`2` male, `2` female) + hornwort (*Ceratophyllum demersum*)** inside a **`1.2 L` closed aquatic ecosystem** for **`43` days** (exceeding the planned 30-day mission and achieving orbital oviposition despite microgravity spatial disorientation/looping behavior).

## 2. Zebrafish Models in LabOnoM Primary Publications (`index.html#L320-L360`)
- **Myostatin (`mstnb`) Craniofacial & Tendon Phenotyping**: Ono *et al.* (`Ono_2025.jpg`, *Journal of Bone and Mineral Research* / skeletal regeneration portfolio) and Mun *et al.* (`Mun_2024.jpg`, PMID `39086598`, `index.html#L348`) investigate **teleost-specific genome duplication (`TSGD`)** paralogs (`mstna`/`mstnb`) in zebrafish craniofacial bone/jaw morphogenesis.

## 3. Legacy `.wiki/` Misattribution Flagged (`CON-07`)
- `.wiki/entities/zebrafish-history.md` falsely states that `_posts/2025-06-10-zebrafish-history.md` analyzes **teleost-specific whole-genome duplication (`TSGD`)** and **Stereo-seq / Visium spatial transcriptomics**. Neither `TSGD` nor `Stereo-seq` nor `Visium` appears anywhere in `_posts/2025-06-10-zebrafish-history.md`; `TSGD` is actually discussed in the `index.html#L348` gallery caption for `Mun_2024.jpg` (PMID `39086598`).
