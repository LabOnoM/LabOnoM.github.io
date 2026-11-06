---
id: worktrees-staging-readme
type: governance
status: active
updated_at: 2026-11-06
source_refs:
  - LLM-Wiki/git-state.md
tags:
  - git
  - worktrees
  - isolation
---

# Isolated Worktree Findings Staging (`LLM-Wiki/worktrees/`)

## Isolation & Consolidation Protocol
When parallel agents or tasks execute in separate `git worktree` checkouts:
1. **Stage Separately First**: Write worktree-local observations, benchmark outputs, and draft summaries inside `LLM-Wiki/worktrees/<worktree-slug>/` rather than mutating canonical `LLM-Wiki/{experiments,datasets,analyses,figures,results}/` directly during unreviewed parallel runs.
2. **Automatic Pending-Integration Detection**: `python3 LLM-Wiki/scripts/wiki_cli.py git-state` scans `LLM-Wiki/worktrees/` for any staged `*.md` notes (other than this `README.md`) and flags `pending_worktree_staging_files` in `LLM-Wiki/manifest/git_state.json`.
3. **Review & Consolidate**: Before merging a task branch or worktree into `main`, verify all `source_refs` and SHA-256 digests, promote validated findings into canonical `LLM-Wiki/` pages, record the consolidation in `LLM-Wiki/log.md`, and remove the staged worktree draft only after review.
4. **Current Status (`2026-11-06`)**: `1` active repository worktree (`/Users/mac/Documents/GitHub/LabOnoM.github.io` on branch `feat/llm-wiki-memory`, branched from `main` @ `b5eedef631ca7b102cccf9a32896468ded9b3501`); `0` unmerged external worktree directories; branch `feat/llm-wiki-memory` itself is **pending owner review and local merge into `main`**.
