---
id: skills-readme
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/scripts/skills_ops.py
  - LLM-Wiki/skills/repositories.json
tags:
  - skills
  - router
  - nature-skills
  - k-dense-ai
---

# Multi-Tier Skills Catalog & Priority Router (`LLM-Wiki/skills/`)

## 1. Inventory Summary (`1,812` Discovered $\to$ `1,539` Retained + `273` Redundant Omitted)
| Routing Priority | Tier | Source Collection(s) | Discovered `SKILL.md` | Retained | Omitted (Redundant) | Availability |
|---:|---|---|---:|---:|---:|---|
| **1 (Highest)** | `global` | Antigravity Built-in (`9`) + Active Plugins (`116`: `science` `48`, `data-agent-kit` `40`, `firebase` `13`, `chrome-devtools` `6`, `android-cli` `3`, `gemini-api` `3`, `modern-web` `2`, `agy-sdk` `1`) + Codex (`2`) + Claude Marketplace (`15`) | `142` | **`142`** | `0` | `active_host_global` / `host_installed_*` |
| **2** | `project` | `.agents/skills/` (`llm-wiki-ops`, `bsgou-jekyll-site-ops`, `bsgou-member-scoring`, `spatial-omics-visiumhd-stereoseq`) | `4` | **`4`** | `0` | `active_project_local` |
| **3** | `external` | [`Yuan1z0825/nature-skills`](https://github.com/Yuan1z0825/nature-skills) (`24`) + [`K-Dense-AI`](https://github.com/K-Dense-AI) (`915` across `8` skill repos; `16` total org repos audited) | `939` | **`823`** | `116` | `indexed_external_cached` |
| **4 (Fallback)** | `global_unmounted_cache` | Local disk `~/.gemini/skills` (unmounted skill pack) | `727` | **`570`** | `157` | `local_disk_unmounted` |
| **Total** | — | All Inventoried Sources | **`1,812`** | **`1,539`** | **`273`** | — |

## 2. Discoverable Router & Progressive Instruction Loading
Never bulk-load all skills into context or bulk-install external dependencies. Follow the 3-step progressive protocol:

1. **Route Task by Capability (`global -> project -> external`)**:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py route "Segment H&E nuclei and bin 10x Visium HD spatial transcriptomics"
   ```
2. **Search Full Skill Bodies Locally (SQLite FTS5 + Versioned `.jsonl.gz` Cache)**:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py skill-search "StarDist Scanpy spatial join"
   ```
3. **Load Only the Selected `SKILL.md` Body & Review Before Execution**:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py skill-body "project:LabOnoM.github.io:spatial-omics-visiumhd-stereoseq"
   ```
   If `LLM-Wiki/.cache/skill_bodies_v1.jsonl.gz` is cold on a fresh checkout, rebuild it at the exact pinned GitHub commit SHAs via:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py fetch-skill-cache
   ```

## 3. Related Catalog Documents
- [[REPOSITORIES]] (`LLM-Wiki/skills/REPOSITORIES.md`) — Exact commit SHAs, scopes, and counts across `Yuan1z0825/nature-skills` and all `16` `K-Dense-AI` repositories.
- [[OMISSIONS]] (`LLM-Wiki/skills/OMISSIONS.md`) — Capability deduplication policy and summary of the `273` omitted redundant skills (`omissions.jsonl`).
- [[SECURITY_REVIEW]] (`LLM-Wiki/skills/SECURITY_REVIEW.md`) — Host instruction precedence and mandatory pre-execution review rules for external skills.
