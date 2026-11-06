---
id: OMISSIONS
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/skills/omissions.jsonl
  - LLM-Wiki/scripts/skills_ops.py
tags:
  - skills
  - deduplication
  - omissions
---

# Redundant External Skill Omissions (`273` Omitted Records)

Every excluded skill is preserved with full provenance (`omitted_skill_id`, `source_repo`, `source_commit`, `rel_path`, `capability_key`, `superseded_by_skill_id`, `body_sha256`, and `reason`) in `LLM-Wiki/skills/omissions.jsonl`.

## 1. Deduplication Policy
A lower-priority skill (`priority_rank >= 30`) is omitted **if and only if** its canonical capability (`capability_key` in `LLM-Wiki/scripts/skills_ops.py`) is already provided by a higher-priority active Global (`Tier 1`), Project-Local (`Tier 2`), or canonical upstream (`Tier 3`) skill. Complementary skills—such as `Yuan1z0825/nature-skills` manuscript/citation workflows, `K-Dense-AI/scientific-agent-skills` `scanpy`/`anndata`/`squidpy`, and `K-Dense-AI/science-superpowers` methodology protocols—are **retained**.

## 2. Breakdown of the `273` Omitted Redundant Skills
1. **External Skills Redundant with Active Tier-1 Global `science` Plugin (`11` capabilities across external repos)**:
   - `chembl` $\to$ superseded by `global:antigravity-plugin:science:chembl-database`
   - `pubchem` $\to$ superseded by `global:antigravity-plugin:science:pubchem-database`
   - `uniprot` $\to$ superseded by `global:antigravity-plugin:science:uniprot-database`
   - `pdb` $\to$ superseded by `global:antigravity-plugin:science:pdb-database`
   - `alphafold` $\to$ superseded by `global:antigravity-plugin:science:alphafold-database-fetch-and-analyze`
   - `clinicaltrials` $\to$ superseded by `global:antigravity-plugin:science:clinical-trials-database`
   - `opentargets` $\to$ superseded by `global:antigravity-plugin:science:opentargets-database`
   - `pymol` $\to$ superseded by `global:antigravity-plugin:science:pymol`
   - `rdkit` $\to$ superseded by `global:antigravity-plugin:science:rdkit-general`
   - `autodock-vina` $\to$ superseded by `global:antigravity-plugin:science:cheminformatics-physics`
   - `boltz` $\to$ superseded by `global:antigravity-plugin:science:cheminformatics-cofolding`
2. **Cross-Repository Mirrors Inside `K-Dense-AI` (`105` duplicates)**:
   - `K-Dense-AI/claude-scientific-writer` (`74` omitted): Exact bundled copies of skills already canonical in `K-Dense-AI/scientific-agent-skills` (`scanpy`, `anndata`, `biopython`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, etc.) or Tier-1 `science`.
   - `K-Dense-AI/drug-discovery-agent-skills` (`11` additional mirrors beyond the `10` Tier-1 `science` overlaps above = `21` total): Copies of `datamol`, `deepchem`, `depmap`, `esm`, `medchem`, `molfeat`, etc. already retained from `K-Dense-AI/scientific-agent-skills`.
   - `K-Dense-AI/mimeo` (`20` omitted): `19` early `output/<thinker>/SKILL.md` profiles superseded by the expanded `K-Dense-AI/mimeographs` collection (`80` profiles) + `1` duplicate helper.
3. **Unmounted Local `~/.gemini/skills` Mirrors (`157` duplicates)**:
   - Unversioned local copies in `~/.gemini/skills` duplicating Tier-1 active host skills or version-pinned `K-Dense-AI` canonical skills (`570` unique local-only entries in `~/.gemini/skills` remain retained at lowest fallback priority `global_unmounted_cache`).
