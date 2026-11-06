---
id: schema
type: governance
status: canonical
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/scripts/wiki_cli.py
  - AGENTS.md
  - CLAUDE.md
tags:
  - schema
  - karpathy-llm-wiki
  - governance
---

# `LLM-Wiki` Architecture & Maintenance Schema

Inspired by Andrej Karpathy's [LLM Wiki design](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), `LLM-Wiki/` separates **immutable primary evidence** (repository code, spreadsheets, `.prism` archives, notebooks, and microscopy/sequencing screenshots) from **curated, cross-linked Markdown memory** and **deterministic integrity manifests**.

## 1. Three-Layer Architecture
1. **Immutable Source Layer (Workspace Root)**:
   - `_posts/PostAttachedFiles/*`, `GSE284271/*`, `scripts/*`, `sources/*`, `img/*`, `css/*`, `js/*`, and legacy `.wiki/*` remain untouched in place. Never edit or overwrite research data artifacts.
2. **Compiled Knowledge & Traceability Layer (`LLM-Wiki/`)**:
   - `index.md` (categorized master catalog), `STATE.md` (concise startup dashboard), `log.md` (append-only activity record), `decisions.md`, `contradictions.md`, `lessons-learned.md`, `open-questions.md`.
   - Scientific traceability chains: `experiments/exp-*.md` $\to$ `datasets/ds-*.md` $\to$ `analyses/ana-*.md` $\to$ `figures/fig-*.md` $\to$ `results/res-*.md`.
3. **Deterministic Integrity & Routing Layer (`LLM-Wiki/manifest/`, `LLM-Wiki/skills/`, `LLM-Wiki/scripts/`)**:
   - `manifest/manifest.jsonl`: Full-file `raw_sha256` (64-hex), `working_git_blob_oid` (40-hex SHA-1), `git_index_blob_oid`, `size_bytes`, `mtime_utc`, `detected_format`, and `inspection_status`.
   - `manifest/manifest_history.jsonl`: Append-only superseded SHA-256 history whenever a tracked file changes or is deleted.
   - `manifest/stale_summaries.json`: Automatic summary invalidation map computed from YAML `source_refs`.
   - `skills/catalog.jsonl` & `skills/omissions.jsonl`: Multi-tier (`global -> project -> external`) capability-deduplicated skill index.
   - `.cache/` (gitignored): Disposable SQLite FTS5 search index (`search_index.sqlite`) and compressed skill-body archive (`skill_bodies_v1.jsonl.gz`).

## 2. Page Front Matter & Citation Rules
Every `LLM-Wiki/` page MUST begin with YAML front matter:
```yaml
---
id: <kebab-case-unique-id>
type: experiment | dataset | analysis | figure | result | governance | overview
status: verified | verified_with_flagged_contradictions | active
updated_at: YYYY-MM-DD
source_refs:
  - relative/path/to/source#L10-L45
tags:
  - tag1
---
```
- **Epistemic Discipline**: Separate **Direct Observations** (exact numbers, sample IDs, units, $n$ replicates, test statistics, line/cell/archive paths) from **Interpretations**. Never equate file hashing/indexing with scientific validation. Never infer historical intent or AI authorship from prose style.

## 3. Append-Only Log Entry Format (`LLM-Wiki/log.md`)
```markdown
## [YYYY-MM-DDTHH:MM:SS+09:00] <ingest|refresh|audit|checkpoint> | <Concise Title>
- **What Changed**: ...
- **Why**: ...
- **Evidence**: ...
- **Validation**: ...
- **Next Actions**: ...
```
