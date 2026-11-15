---
id: STATE
type: governance
status: live_dashboard
updated_at: 2026-11-15
source_refs:
  - LLM-Wiki/manifest/manifest.summary.json
  - LLM-Wiki/manifest/git_state.json
  - LLM-Wiki/manifest/stale_summaries.json
tags:
  - state
  - startup
  - memory
---

# `LLM-Wiki` Current State Dashboard

> **Agent Startup Rule**: Read this page first at the start of every session, then run `python3 LLM-Wiki/scripts/wiki_cli.py refresh --dry-run` and `python3 LLM-Wiki/scripts/wiki_cli.py git-state` to check live workspace files against recorded memory.

## 1. Repository & Branch Snapshot (`2026-11-15`)
- **Workspace Root**: `/Users/mac/Documents/GitHub/LabOnoM.github.io` (`1` worktree, `0` nested `.git` repositories).
- **Prior `main` Commit**: `ad119b53383a27d73a07be277550cd22170d0a75` (`2026-11-07`, manual CI / no GitHub Actions).
- **Active Branch**: `main` (fast-forward merged from `feat/blog-math-ai-era` with owner authorization on `2026-11-15`, publishing `_posts/2026-11-15-after-proof-scarcity.md`, `img/Post/2026/after-proof-scarcity-cover.png`, and `LLM-Wiki/analyses/ana-after-proof-scarcity.md` to `https://www.bs-gou.com/blog/`; `0` external worktree staging drafts).
- **Website Compilation Check**: Verified clean (`0` errors) via isolated `Ruby 3.2.2` + `Jekyll 4.2.2` (`bundle exec jekyll build` in ~2.4 s), including `/blog/index.html` and `/2026/11/15/after-proof-scarcity.html`.

## 2. File Integrity & Knowledge Coverage
- **Manifest Coverage**: All `504` in-scope workspace files full-file hashed (`raw_sha256` + `working_git_blob_oid` + `git_index_blob_oid`), `0` `unhashed`, `0` `partial`, `0` `sampled`, `0` `unsupported`, `0` stale summaries (`stale_summaries.json`), and `22` explicitly flagged format-mismatch/anomalous files (`~$Frame_Article.pptx`, `00.NIH_10xVisiumHD.html`, and `20` LiteSpeed 404 `.html` stubs).
- **Scientific Traceability**: `3` complete `experiment -> dataset -> analysis -> figure -> result` chains (`GSE284271` Visium HD palate, `qPCR` $2^{-\Delta\Delta C_T}$ `Example_qPCR.xlsx`/`*.prism`, and `Stereo-seq` `A02598A4` CID decoding) + `6` literature/community/epistemology quantitative reviews (including `ana-beyond-the-silicon-mirage` and `ana-after-proof-scarcity`).
- **Active Contradictions Flagged**: `9` (`CON-01` through `CON-09` in [[contradictions]]). Originals kept intact.
- **Skills Catalog & Router**: `1,812` `SKILL.md` files inventoried across Global (`142`), Project-Local (`4` in `.agents/skills/`), `Yuan1z0825/nature-skills` (`24`), and `K-Dense-AI` (`915` across `8` repos; all `16` org repos audited) + `~/.gemini/skills` (`727`) $\to$ **`1,539` unique capabilities retained** (`catalog.jsonl`) and **`273` redundant duplicates omitted** (`omissions.jsonl`).

## 3. Data Backup Caveat & Next Actions
- **Untracked Raw Data Backup**: External storage/backup arrangements for untracked multi-GB datasets (`./240726_VisiumHD/*.tif/*.h5` and `A02598A4.*` / `*.fq.gz`) are **unknown** (`OQ-01`). Local Git and `manifest.jsonl` hashes verify integrity but do not back up untracked external data.
- **Next Recommended Actions for Owner**:
  1. Review [[contradictions]] (`CON-01`–`CON-09`) and [[open-questions]] (`OQ-01`–`OQ-06`), particularly the `0.5/0.5` vs `0.3/0.7` contribution score formula (`CON-05`) and `qPCR` variance $F$-test prose (`CON-04`).
  2. Optionally run `./scripts/update-members.sh` from `main` to refresh `members.html` after publishing the new blog post (per `README.md` "Checks and deploys").
