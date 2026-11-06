---
id: REPOSITORIES
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/skills/repositories.json
  - LLM-Wiki/scripts/skills_ops.py
tags:
  - skills
  - repositories
  - nature-skills
  - k-dense-ai
---

# Audited Skill Repositories & Pinned Source Versions

All `17` external repositories (`Yuan1z0825/nature-skills` + all `16` public repositories under the `K-Dense-AI` GitHub organization) were inspected on `2026-11-06` and pinned by exact `main` commit/tree SHA in `LLM-Wiki/skills/repositories.json`.

## 1. Skill-Bearing External Repositories (`9` Repos, `939` `SKILL.md` Files)
| Repository | Pinned `main` Commit / Tree SHA | `SKILL.md` Found | Retained | Omitted | Scope & Complementary Value |
|---|---|---:|---:|---:|---|
| [`Yuan1z0825/nature-skills`](https://github.com/Yuan1z0825/nature-skills) | `d774add241c65e89ed17a4da573b472b0972fd42` | `24` | `24` | `0` | Multi-source academic search (`Scopus`/`ScienceDirect`/`CrossRef`/`PubMed`), strict citation verification, Nature-style figure formatting, manuscript drafting, peer review, and rebuttal workflows. |
| [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills) | `a25cf9ec00e2745d03f8704acf6f6919694ccd9a` | `177` | `176` | `1` | Core bioinformatics (`scanpy`, `anndata`, `squidpy`, `scvi-tools`, `biopython`), statistics (`statsmodels`, `pymc`), ML, plotting, and lab formats (`pymol` omitted as covered by Tier-1 `science`). |
| [`K-Dense-AI/claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer) | `529b9f73ab4b48925027145800d7b49e96ccfd3c` | `78` | `4` | `74` | Retains unique writing/formatting skills not duplicated in `scientific-agent-skills`; `74` bundled mirrors of `scientific-agent-skills` omitted. |
| [`K-Dense-AI/drug-discovery-agent-skills`](https://github.com/K-Dense-AI/drug-discovery-agent-skills) | `ee7655f065e4bb1a5a4d4898154b61c0e45918e2` | `37` | `16` | `21` | Retains `16` complementary drug-design workflows (`adaptyv`, `admet-prediction`, `antibody-engineering`, `binding-site-analysis`, `chemical-space`, `degraders`, `diffdock`, `lead-optimization`, etc.); omits `21` skills redundant with Tier-1 `science` (`chembl`, `pubchem`, `uniprot`, `pdb`, `alphafold`, `clinicaltrials`, `opentargets`, `rdkit`, `autodock-vina`, `boltz`) or `scientific-agent-skills`. |
| [`K-Dense-AI/science-superpowers`](https://github.com/K-Dense-AI/science-superpowers) | `0374bdf82c2372bdf1667e3c762146c3a29215f5` | `16` | `16` | `0` | Preregistration, feasibility checks, red-team review, anomalous-result investigation, and reproducible analysis orchestration. |
| [`K-Dense-AI/scientific-agents`](https://github.com/K-Dense-AI/scientific-agents) | `98c7fae46648724e1a43a1f2b207b0c82fcc462e` | `503` | `503` | `0` | `503` domain-specialist scientific agent profiles (demoted behind tool skills during technical routing unless specialist/persona framing is requested). |
| [`K-Dense-AI/mimeographs`](https://github.com/K-Dense-AI/mimeographs) | `a38f5fcad0853be3e98a6cd95d8e6bf8c66f7c7b` | `80` | `80` | `0` | `80` reasoning/writing style guides (including `andrej-karpathy`, `richard-feynman`, `claude-shannon`, `edward-tufte`). |
| [`K-Dense-AI/mimeo`](https://github.com/K-Dense-AI/mimeo) | `a4cea1842a24515cda354a3aa9eb9763677a3cdd` | `22` | `2` | `20` | Retains corpus/style synthesis skills; omits `19` `output/*` thinker profiles superseded by `mimeographs` plus `1` duplicate helper. |
| [`K-Dense-AI/skill-101-webinar`](https://github.com/K-Dense-AI/skill-101-webinar) | `f51b0a70c820784d8dbc9590bb48e01a54d93bbf` | `2` | `2` | `0` | `plain-language-summary` and `paper-draft-SKILL` authoring template. |

## 2. Non-Skill `K-Dense-AI` Repositories Audited (`7` Repos, `0` `SKILL.md` Files)
Recorded in `repositories.json` so future audits know every repository in `K-Dense-AI` was accounted for:
- `K-Dense-AI/agentic-data-scientist` (`702dee9dfb`) — Standalone agentic data-science app (`0` `SKILL.md`).
- `K-Dense-AI/claude-skills-mcp` (`72a7b50223`) — MCP server wrapper over scientific skills (`0` standalone `SKILL.md`).
- `K-Dense-AI/lab-instrument-mcps` (`46545ea7eb`) — Laboratory hardware MCP servers (`0` `SKILL.md`).
- `K-Dense-AI/rowan-autosearch` (`faebbb2aaa`) — Rowan quantum chemistry autosearch (`1` `AGENTS.md`, `0` `SKILL.md`).
- `K-Dense-AI/k-dense-byok` (`6a55f5ce6f`) — Web BYOK client/backend (`1` `AGENTS.md`, `0` `SKILL.md`).
- `K-Dense-AI/karpathy` (`f92b680a48`) — Standalone precursor superseded by `K-Dense-AI/mimeographs` (`0` `SKILL.md`).
- `K-Dense-AI/hf-mva-hackathon-2026` (`1fc4279131`) — Hackathon project (`0` `SKILL.md`).
