# CLAUDE Context: `LLM-Wiki/`

## Purpose
`LLM-Wiki/` is the canonical persistent, hash-verified project memory, biomedical evidence ledger, and skill router for `LabOnoM.github.io`, built on Karpathy's LLM Wiki architecture.

## Key Directories & Files
- `index.md`, `STATE.md`, `SCHEMA.md`, `log.md`, `decisions.md`, `contradictions.md`, `open-questions.md`, `lessons-learned.md`
- `experiments/`, `datasets/`, `analyses/`, `figures/`, `results/`: Linked scientific traceability chains with `source_refs` YAML front matter.
- `manifest/`: Deterministic file integrity manifest (`manifest.jsonl`), format/exclusion summary (`manifest.summary.json`), append-only superseded hash ledger (`manifest_history.jsonl`), invalidated summary tracker (`stale_summaries.json`), and Git/worktree snapshot (`git_state.json`).
- `skills/`: Deduplicated multi-tier catalog (`catalog.jsonl`), explicit redundancy omissions (`omissions.jsonl`, `OMISSIONS.md`), pinned repo metadata (`repositories.json`, `REPOSITORIES.md`), and security review gates (`SECURITY_REVIEW.md`).
- `scripts/wiki_cli.py`: Zero-dependency Python 3 stdlib CLI (`scan`, `refresh`, `search`, `build-skills`, `skill-search`, `skill-body`, `route`, `git-state`, `verify`, `fetch-skill-cache`).
- `.cache/` (gitignored): Disposable SQLite FTS5 index (`search_index.sqlite`) and compressed skill-body store (`skill_bodies_v1.jsonl.gz`).

## Rules When Editing `LLM-Wiki/`
1. Preserve YAML front matter (`id`, `type`, `status`, `updated_at`, `source_refs`, `tags`) on every knowledge page so `wiki_cli.py refresh` can automatically invalidate stale summaries when source files change.
2. Never edit `manifest/manifest_history.jsonl` destructively; it is an append-only audit trail of superseded file SHA-256 digests.
3. Run `python3 LLM-Wiki/scripts/wiki_cli.py scan` and `python3 LLM-Wiki/scripts/wiki_cli.py verify` after adding or updating wiki pages.
