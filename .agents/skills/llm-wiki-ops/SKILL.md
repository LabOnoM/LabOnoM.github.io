---
name: llm-wiki-ops
description: Manage, query, refresh, route skills, and verify the LabOnoM LLM-Wiki persistent project memory system. Activate at session startup, when checking file integrity or biomedical evidence citations, routing tasks across global/project/external skills, or refreshing manifests before Git checkpoints.
---

# LLM-Wiki Operations (`llm-wiki-ops`)

Canonical workflow skill for maintaining the `LLM-Wiki/` persistent project memory in `LabOnoM.github.io`.

## 1. Startup Check
At the beginning of every session, inspect concise project state and detect drift before editing code or answering scientific questions:

```bash
python3 LLM-Wiki/scripts/wiki_cli.py git-state
python3 LLM-Wiki/scripts/wiki_cli.py refresh --dry-run
```

Read `LLM-Wiki/STATE.md` and `LLM-Wiki/index.md` first, then follow links progressively rather than grepping raw repository files blindly.

## 2. Progressive Retrieval & Evidence Checking
1. Search across wiki summaries, file manifest records, and indexed skills:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py search "<query>"
   ```
2. Read the matched page under `LLM-Wiki/` (`experiments/`, `datasets/`, `analyses/`, `figures/`, `results/`, `contradictions.md`).
3. Verify `source_refs` against primary workspace files (`_posts/PostAttachedFiles/`, `GSE284271/`, `scripts/`) before making substantive scientific or engineering claims. Separate direct observations from interpretations.

## 3. Skill Routing (`global -> project -> external`)
Before improvising specialized bioinformatics, cheminformatics, clinical, or web workflows, query the skill router:

```bash
python3 LLM-Wiki/scripts/wiki_cli.py route "<task description>"
```

- **Priority 1 (`global`)**: Host-installed skills (e.g., Antigravity `science`, `chrome-devtools`, `modern-web-guidance`).
- **Priority 2 (`project`)**: Repository-specific skills in `.agents/skills/`.
- **Priority 3 (`external`)**: Indexed complementary skills from `Yuan1z0825/nature-skills` and `K-Dense-AI` collections. Retrieve only the selected body via:
  ```bash
  python3 LLM-Wiki/scripts/wiki_cli.py skill-body "<skill_id>"
  ```
  Review external instructions and dependency requirements before execution; never bulk-install external packages into global Python.

## 4. Incremental Refresh & Checkpointing
After modifying workspace files or wiki summaries:

```bash
python3 LLM-Wiki/scripts/wiki_cli.py refresh
python3 LLM-Wiki/scripts/wiki_cli.py verify
```

1. Resolve any invalidated summaries listed in `LLM-Wiki/manifest/stale_summaries.json`.
2. Append a timestamped entry to `LLM-Wiki/log.md` (and `LLM-Wiki/decisions.md` for architectural choices) and update `LLM-Wiki/STATE.md`.
3. Stage attributable docs, manifests, and support code only (excluding `LLM-Wiki/.cache/`, secrets, and raw data) for local Git checkpoint commits. Never push or add `.github/workflows/`.
