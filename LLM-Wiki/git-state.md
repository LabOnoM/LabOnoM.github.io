---
id: git-state
type: governance
status: verified
updated_at: 2026-11-06
source_refs:
  - .gitignore
  - AGENTS.md
  - CLAUDE.md
tags:
  - git
  - worktrees
  - integrity
  - backup-status
---

# Repository, Branch, Worktree, & Data-Backup Provenance

Live machine-readable state is refreshed via `python3 LLM-Wiki/scripts/wiki_cli.py git-state` into `LLM-Wiki/manifest/git_state.json`.

## 1. Repository & Worktree Identity
- **Repository Root**: `/Users/mac/Documents/GitHub/LabOnoM.github.io`
- **Remote Origin**: `https://github.com/LabOnoM/LabOnoM.github.io.git`
- **Nested Git Repositories**: `0` (verified recursively across all workspace subdirectories).
- **Active Worktrees**: `1` (`/Users/mac/Documents/GitHub/LabOnoM.github.io`; `0` secondary external `git worktree` checkouts).
- **Base / Source Branch**: `main` = `origin/main` = `b5eedef631ca7b102cccf9a32896468ded9b3501` (*"Stop using GitHub Actions; update member list manually"*, `2026-10-13`).
- **Other Existing Remote Branches (Preserved Untouched)**:
  - `origin/codex/fix-.badge-bar-responsive-layout` (`39a5070e18a62a006564f568b07b82479b6f0f02`)
  - `origin/codex/update-fetch_bsgou_members.py-for-forked-repos` (`d1cd985d1cf0fc0228db91f81c36f3179a127f41`)
- **Active Task Branch**: `feat/llm-wiki-memory` (branched locally from `b5eedef631ca7b102cccf9a32896468ded9b3501`).
- **Pending Integration Status**: `feat/llm-wiki-memory` contains local checkpoint commits for `LLM-Wiki/`, `.agents/`, and agent entry docs; it has **not** been merged into `main` or pushed to `origin` (awaiting owner review and local `jekyll build` + `wiki_cli.py verify` sign-off).

## 2. Digest Separation: `raw_sha256` vs. Git Blob SHA-1 vs. Git Commit ID
`LLM-Wiki` maintains three distinct cryptographic identifiers that MUST never be conflated:
1. **`raw_sha256` (64-hex SHA-256)**: Computed directly over raw file bytes (`SHA256(bytes)`). Identifies exact file contents regardless of whether a file is committed, modified, staged, or untracked.
2. **`working_git_blob_oid` / `git_index_blob_oid` (40-hex SHA-1)**: Computed with Git's object framing (`SHA1("blob <size>\0" + bytes)`). Comparing `working_git_blob_oid` against `git_index_blob_oid` detects unstaged working-tree edits per file.
3. **`git_head_commit` (40-hex Commit ID)**: Identifies a committed Git tree snapshot + parent history. **A commit ID alone cannot identify uncommitted, unstaged, or untracked research evidence**—always pair commit references with `git_state.json` dirty flags and `manifest.jsonl` `raw_sha256` digests.

## 3. Untracked Raw Data & Backup Caveat
- Cryptographic hashes in `LLM-Wiki/manifest/` and local Git commits **do not back up untracked external raw datasets** (such as `./240726_VisiumHD/RJ_7_23_24.tif`, Space Ranger `.h5`/`.parquet` matrices, or Stereo-seq `A02598A4.barcodeToPos.h5` and `E150018299_L01_62_*.fq.gz`).
- **Institutional / Offsite Backup Status**: **Unknown** (not documented anywhere in workspace files; flagged in [[open-questions]] `OQ-01`).
