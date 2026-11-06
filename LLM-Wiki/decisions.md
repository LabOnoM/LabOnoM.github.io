---
id: decisions
type: governance
status: append_only_ledger
updated_at: 2026-11-06
source_refs:
  - AGENTS.md
  - CLAUDE.md
  - README.md
  - _config.yml
tags:
  - decisions
  - governance
  - architecture
---

# Architectural & Governance Decision Log

Historical entries prior to `2026-11-06` cite only verified Git commits and repository policy documents (no historical intent or AI authorship is inferred from style). Entries from `2026-11-06` onward form an append-only decision record.

## Verified Historical Repository Decisions

### `[2026-10-13] HIST-01 | Manual CI/CD & Removal of GitHub Actions`
- **Source Provenance**: Git commit `b5eedef631ca7b102cccf9a32896468ded9b3501`, `AGENTS.md#L24-L35`, `CLAUDE.md#L39-L50`, `README.md#L127-L133`.
- **Decision**: Removed `.github/workflows/update_members.yml`; prohibited adding any workflow under `.github/workflows/` or relying on hosted CI checks due to zero Actions budget.
- **Operational Consequence**: Website compilation (`bundle exec jekyll build`) and member-table refreshes (`scripts/update-members.sh`) are executed manually on a credentialed local machine before merge/release.

### `[2026-06-08 .. 2026-06-09] HIST-02 | AROS Onboarding & Glassmorphic UI Modernization`
- **Source Provenance**: `README.md#L116-L118`, `SPEC.md`, `js/custom.js`, `css/style.css`.
- **Decision**: Established `.wiki/` (`Wiki` symlink) and modernized `index.html` with light/dark theme persistence (`bsgou-theme`) and touch-swipe gallery controls.

---

## `2026-11-06` `LLM-Wiki` Persistent Memory Architecture Decisions

### `[2026-11-06T23:37:00+09:00] DEC-01 | Canonical LLM-Wiki Alongside Intact Legacy .wiki/`
- **What Changed**: Created `LLM-Wiki/` as the canonical persistent memory system while keeping `.wiki/` files untouched in place and cross-linking `.wiki/index.md`, `AGENTS.md`, and `CLAUDE.md` to `LLM-Wiki/`.
- **Why**: Satisfies the user requirement to build `LLM-Wiki/` and preserve originals/existing instructions (`[[page]]` Obsidian compatibility) while correcting factual hallucinations uncovered in `.wiki/entities/{gse284271,glycorna-imaging,zebrafish-history}.md` (`CON-01`, `CON-06`, `CON-07`).
- **Validation**: `wiki_cli.py verify` checks both `LLM-Wiki/` Markdown links and `[[wikilinks]]`.

### `[2026-11-06T23:37:10+09:00] DEC-02 | Preserve Root README.md Jekyll Page While Adding LLM-Wiki Guide`
- **What Changed**: Excluded `/LLM-Wiki`, `/.agents`, and `/.claude` in `_config.yml`, created standalone `LLM-Wiki/README.md`, and appended a Kramdown-compatible `LLM-Wiki` navigation, setup, workflow diagram, and verified CLI section to root `README.md`.
- **Why**: Root `README.md` uses Jekyll front matter (`layout: default`, `title: Vision and Strategic Plan`) and is served live at `/README.html` (linked from `index.html#L139` and `_data/navigation.yml#L30`). Overwriting it would break a primary public webpage.
- **Validation**: Verified via isolated `bundle exec jekyll build` (`Ruby 3.2.2` / `Jekyll 4.2.2`) that `/README.html` compiles cleanly with zero errors.

### `[2026-11-06T23:41:00+09:00] DEC-03 | Strict Separation of Raw SHA-256, Git Blob SHA-1, and Commit IDs + Self-Exclusion`
- **What Changed**: Implemented deterministic `LLM-Wiki/manifest/manifest.jsonl` storing `raw_sha256` (64-hex), `working_git_blob_oid` (40-hex SHA-1), and `git_index_blob_oid` per file, while recording `git_head_commit` in `manifest.summary.json` and `git_state.json`, and excluding self-referential manifest/cache paths.
- **Why**: Prevents recursive hash invalidation loops (`manifest.jsonl` hashing itself) and makes uncommitted/untracked file state explicit where a Git commit SHA alone is insufficient.
- **Validation**: Back-to-back `wiki_cli.py refresh` runs produce identical `manifest.jsonl` SHA-256 digests (`zero_diff: true`).

### `[2026-11-06T23:44:00+09:00] DEC-04 | Capability-Deduplicated Multi-Tier Skill Router & Disposable FTS5/Body Cache`
- **What Changed**: Inventoried `1,812` discovered `SKILL.md` files across Tier-1 `global` (`142` active host/IDE skills), Tier-2 `project` (`4` `.agents/skills/` skills), Tier-3 `external` (`24` `Yuan1z0825/nature-skills` + `915` across `K-Dense-AI`), and `727` local `~/.gemini/skills` entries; retained `1,539` unique capabilities in `LLM-Wiki/skills/catalog.jsonl` and recorded `273` genuine capability duplicates in `LLM-Wiki/skills/omissions.jsonl`. Stored compressed bodies (`skill_bodies_v1.jsonl.gz`) and SQLite FTS5 index (`search_index.sqlite`) in gitignored `LLM-Wiki/.cache/` with `fetch-skill-cache` rebuild support.
- **Why**: Enables instant local full-body search and `global -> project -> external` routing without committing multi-megabyte binary caches to Git or auto-installing unreviewed external Python packages.
- **Validation**: Verified via `wiki_cli.py verify` (`skill_body_retrieval` and `skill_router_precedence` checks).

### `[2026-11-06T23:45:00+09:00] DEC-05 | Task Branch Isolation on feat/llm-wiki-memory`
- **What Changed**: Executed all `LLM-Wiki` implementation and local checkpoint commits on branch `feat/llm-wiki-memory` branched from `main` (`b5eedef631ca7b102cccf9a32896468ded9b3501`), leaving `main` and `origin/main` untouched and unpushed.
- **Why**: Provides clean reviewable isolation and honors the non-push / non-destructive Git governance rules.
