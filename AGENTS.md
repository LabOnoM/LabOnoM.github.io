# Guidelines for Codex Agents

## Testing
- After modifying website content or configuration, run `jekyll build` to ensure the site compiles.

## Posts
- Blog posts reside in `_posts/` and use the `YYYY-MM-DD-title.md` naming scheme.
- Include YAML front matter with at least `title` and `layout` keys.

## Pages and Assets
- Place standalone pages in the repo root or appropriate folders.
- Store images in `img/` or `assets/`.

## Environment
- The development environment is defined in `codex.yaml`.

## AROS LLM-Wiki Integration & Governance
- **Strict Grounding**: Search canonical `LLM-Wiki/` (`LLM-Wiki/STATE.md`, `LLM-Wiki/index.md`) first, alongside legacy `.wiki/` (preserved for Obsidian `[[page]]` compatibility). Refer to entities using Obsidian style double bracket links `[[page]]` or clickable file links.
- **Gap Detection**: If you cannot resolve a question using workspace documentation, `LLM-Wiki/`, or `.wiki/`, prompt the user: "Would you like me to run `/wiki-research` to investigate this topic?"
- **Slash Commands**: Recognize `/wiki-query`, `/wiki-research`, `/wiki-ingest`, `/wiki-update`, and `/wiki-build` as valid workflow commands.
- **Workspace Hygiene**: Always place temporary or scratch files in `~/.gemini/antigravity/brain/<session_id>/scratch/`. Do not pollute the repository root.
- **Large Artifacts Rule**: If generating files exceeding 3000 words, HTML reports, or massive tables, use Python script automation to write files rather than direct LLM completion to prevent content truncation.

## Canonical `LLM-Wiki` Multi-Agent Workflow (`Antigravity`, `Claude Code`, `Codex`, `OpenClaw`)

All coding and research agents share one canonical memory workflow backed by zero-dependency `LLM-Wiki/scripts/wiki_cli.py`:

- **Host Instruction Discovery**:
  - **Antigravity**: Loads `AGENTS.md`, `.agents/rules/llm-wiki-governance.md`, and `.agents/skills/*/SKILL.md` (workspace > global `~/.gemini/config/` > built-in).
  - **Claude Code**: Loads root `CLAUDE.md` and directory-scoped `CLAUDE.md` (`LLM-Wiki/CLAUDE.md`, `scripts/CLAUDE.md`, `GSE284271/CLAUDE.md`, `css/CLAUDE.md`, `tools/CLAUDE.md`).
  - **Codex**: Loads `codex.yaml`, `AGENTS.md`, and `.agents/skills/*/SKILL.md`.
  - **OpenClaw**: Reads `AGENTS.md` and standard `SKILL.md` definitions in `.agents/skills/`.
- **1. Startup**: Read `LLM-Wiki/STATE.md` and `LLM-Wiki/index.md`; run `python3 LLM-Wiki/scripts/wiki_cli.py git-state` and `python3 LLM-Wiki/scripts/wiki_cli.py refresh --dry-run` to detect dirty/changed files or pending worktree drafts (`LLM-Wiki/worktrees/`).
- **2. Progressive Retrieval**: Query `python3 LLM-Wiki/scripts/wiki_cli.py search "<query>"` (`--scope wiki|skills|manifest`) before broad repo greps; open only relevant summary pages.
- **3. Evidence Checking**: Check `LLM-Wiki/contradictions.md` (`CON-01`–`CON-09`) before relying on inherited prose or legacy `.wiki/` pages; verify `source_refs` against primary spreadsheets, `.prism` archives, notebooks, and code; separate direct observations from interpretations.
- **4. Skill Routing (`global -> project -> external`)**: Run `python3 LLM-Wiki/scripts/wiki_cli.py route "<task>"` so suitable host/global skills run first, `.agents/skills/` project skills second, and complementary external skills (`Yuan1z0825/nature-skills`, `K-Dense-AI`) third. Load only selected instructions via `wiki_cli.py skill-body <skill_id>` and review external instructions/dependencies before execution (see `LLM-Wiki/skills/SECURITY_REVIEW.md`).
- **5. Memory Refresh & Checkpointing**: After modifying workspace files, run `python3 LLM-Wiki/scripts/wiki_cli.py refresh --reindex` and `python3 LLM-Wiki/scripts/wiki_cli.py verify`, resolve any invalidated summaries in `LLM-Wiki/manifest/stale_summaries.json`, append to `LLM-Wiki/log.md` (and `LLM-Wiki/decisions.md` for architecture choices), update `LLM-Wiki/STATE.md`, and create local Git checkpoint commits excluding `LLM-Wiki/.cache/`, secrets, and untracked raw datasets. Never push or rewrite history without authorization.

## CI/CD is manual: no GitHub Actions (owner's decision, 2026-10-13)

LabOnoM does not use GitHub Actions: there is no budget for it. Never add a file under `.github/workflows/`, never
rely on or wait for a GitHub status check, and never describe a change as "green on CI". Instead:

- **Before every merge**, run this repository's checks locally (the commands in the "Checks and deploys" section of
  the README) and write the pass, fail and skip counts in the pull request.
- **Deploys and releases** are run by hand from a machine that holds the owner's credentials, with the scripts in
  `scripts/` (or the documented commands), never by a hosted runner; record what ran and its result (revision,
  version, digest) in the pull request or the session receipt.
- Steps that need a platform this machine is not (macOS or Windows builds, signing) are run on such a machine by
  the owner, or are recorded as not run; they are never claimed.
