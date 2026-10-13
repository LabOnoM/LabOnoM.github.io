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
- **Strict Grounding**: When answering questions or updating codebase components, search `.wiki/` first. Refer to entities using Obsidian style double bracket links `[[page]]`.
- **Gap Detection**: If you cannot resolve a question using workspace documentation or `.wiki/`, prompt the user: "Would you like me to run `/wiki-research` to investigate this topic?"
- **Slash Commands**: Recognize `/wiki-query`, `/wiki-research`, `/wiki-ingest`, `/wiki-update`, and `/wiki-build` as valid workflow commands.
- **Workspace Hygiene**: Always place temporary or scratch files in `~/.gemini/antigravity/brain/<session_id>/scratch/`. Do not pollute the repository root.
- **Large Artifacts Rule**: If generating files exceeding 3000 words, HTML reports, or massive tables, use Python script automation to write files rather than direct LLM completion to prevent content truncation.

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
