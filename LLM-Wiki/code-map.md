---
id: code-map
type: overview
status: verified
updated_at: 2026-11-06
source_refs:
  - CODE_MAP.md
  - _config.yml
  - Gemfile
  - codex.yaml
  - js/custom.js
  - css/style.css
  - scripts/fetch_bsgou_members.py
  - scripts/update-members.sh
  - LLM-Wiki/scripts/wiki_cli.py
tags:
  - code-map
  - architecture
  - jekyll
  - python
---

# Verified Repository File & Code Map

## 1. Workspace Directory Topology (`/Users/mac/Documents/GitHub/LabOnoM.github.io`)
| Path | Primary Formats | Role & Verified Behavior |
|---|---|---|
| `LLM-Wiki/` | `.md`, `.jsonl`, `.json`, `.py` | **Canonical persistent project memory**, hash manifest, traceability chains, skill catalog/router, and `wiki_cli.py`. Excluded from Jekyll build in `_config.yml`. |
| `.agents/` | `.md` | Workspace-level agent rules (`.agents/rules/llm-wiki-governance.md`) and 4 project-local skills (`.agents/skills/*/SKILL.md`). Excluded from Jekyll build. |
| `.wiki/` (`Wiki` symlink) | `.md` | Legacy AROS wiki (`15` Markdown files) preserved in place for Obsidian `[[page]]` compatibility; factual errors audited in [[contradictions]]. |
| `_posts/` & `PostAttachedFiles/` | `.md`, `.xlsx`, `.prism`, `.png` | `9` Jekyll blog posts (`YYYY-MM-DD-*.md`) plus primary qPCR spreadsheets/Prism archives and Stereo-seq/zebrafish evidence figures. |
| `GSE284271/` | `.html`, `.md` | `01.scRNAseq10xVisiumHD.html` (29-cell executed StarDist + Scanpy Visium HD notebook) and `00.NIH_10xVisiumHD.html` (117 B truncated fragment). |
| `scripts/` | `.py`, `.sh`, `.md` | `fetch_bsgou_members.py` (`get_org_repos`, `get_contributions`, `calculate_scores`, `generate_outputs`) and manual runner `update-members.sh`. |
| `sources/` | `.md` | `9` core BSGOU philosophy essays rendered and embedded via IFrames on `index.html`. |
| `js/` & `css/` & `_sass/` | `.js`, `.css`, `.scss` | Vanilla JS UI controller `js/custom.js` (`localStorage['bsgou-theme']`, mobile nav, touch-swipe carousels), Bootstrap/TeXt stylesheets, and theme Sass modules. |
| `_layouts/`, `_includes/`, `_data/` | `.html`, `.yml` | Liquid page wrappers, navigation menus (`_data/navigation.yml`), and localization strings (`_data/locale.yml`). |
| `img/` & `assets/` & `fonts/` | `.png`, `.jpg`, `.gif`, `.svg`, `.ico`, `.otf`, `.woff*` | Logos, research gallery composites (`img/gallery/`), search JS, and web fonts. Note `~$Frame_Article.pptx` lock file and `18` LiteSpeed 404 `.html` stubs (`CON-09`). |
| `tools/` | `.js`, `.sh`, `.md` | `dir-tree.sh` (active), plus upstream `jekyll-TeXt-theme` leftovers `assert-url.js` and `diff.sh` referencing absent `./test/_posts` and `./docs/en`. |
| `00.RawData/` | `.md` | Contains `PIPELINE_REGISTRY.md` (note stale `.github/workflows/update_members.yml` entry, `CON-08`). |

## 2. Key Executable Entry Points & Symbols
1. **`LLM-Wiki/scripts/wiki_cli.py`** (Python 3.9+ stdlib only):
   - `scripts.inspectors.inspect_workspace_file`: Magic-byte + container parser computing `raw_sha256` and `working_git_blob_oid`.
   - `scripts.manifest_ops.scan_or_refresh_manifest`: Deterministic manifest builder, `manifest_history.jsonl` superseded-hash logger, and `stale_summaries.json` invalidator.
   - `scripts.skills_ops.build_skills_catalog` / `route_task_to_skills` / `get_skill_body`: Capability-deduplicated skill indexer and `global -> project -> external` priority router.
   - `scripts.search_verify.build_search_index` / `search_index` / `run_verification_suite`: SQLite FTS5 BM25 search and 7-gate integrity/traceability verifier.
2. **`scripts/fetch_bsgou_members.py`** (requires `requests`, `pandas`, `scipy`, `openpyxl`):
   - `get_org_repos()`, `get_contributions(user, repos)`, `calculate_scores(df)`, `generate_outputs(df)`.
3. **`scripts/update-members.sh`**:
   - Pre-flights clean `main` branch + `BSGOU_GITHUB_TOKEN` / `gh auth token`, runs `fetch_bsgou_members.py`, commits `members.html`, and pushes manually to `origin HEAD:main`.
4. **Website Build (`Gemfile` + `_config.yml`)**:
   - `bundle exec jekyll build` (`Jekyll 4.2.2`, `kramdown`, `rouge`, `jekyll-feed`, `jekyll-paginate`, `jekyll-sitemap`, `jemoji`).
