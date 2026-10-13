# CLAUDE (Workspace Entry Rules)

This document contains global constraints, build/test command lists, and coding standards for Codex agents.

## 1. Codebase Navigation Rules

> [!IMPORTANT]
> 1. **Read `CODE_MAP.md` first** to understand the layout and topological mapping of packages and components.
> 2. Do not execute broad semantic searches or grep actions across the whole repository unless targeted.
> 3. Before modifying or inspecting a package or component, read its local `CLAUDE.md` context file (e.g., `scripts/CLAUDE.md` or `css/CLAUDE.md`).

---

## 2. LLM-Wiki Grounding & Drift Prevention

- **Strict Grounding**: Always search the `.wiki/` directory first for architectural patterns and concepts before writing code.
- **Wikilinks**: Refer to domain entities using Obsidian-style double bracket links, e.g., `[[overview]]` or `[[lessons-learned]]`.
- **Drift Prevention**: Whenever you modify a core data structure, styling convention, or computational pipeline, you **MUST** update the corresponding `.wiki/` page or `CODE_MAP.md` sections immediately to prevent knowledge rot.

---

## 3. Development Commands

- **Jekyll Site Compilation**: `bundle exec jekyll build` or `jekyll build`
- **Jekyll Site Preview**: `bundle exec jekyll serve`
- **Scraper Pipeline Execution**: `python scripts/fetch_bsgou_members.py`
- **Image URL Asset Checker**: `node tools/assert-url.js`
- **Directory Tree Generator**: `./tools/dir-tree.sh`

---

## 4. Global Coding Standards

- **Git Rules**: Never commit broken build artifacts or temp files. If pushing to the remote repository, bypass dummy token wrappers using `env -u GITHUB_TOKEN git push origin main`.
- **Python**: Use Python 3.x, enforce static type hinting, follow PEP 8 rules, and write docstrings for new methods.
- **HTML & Web Layouts**: Write semantic HTML5, ensure unique element IDs for test scripts, and maintain accessibility standards.
- **Hygiene**: Never create temporary, scratch, or test files in the workspace root directory. Use `<appDataDir>/brain/<session_id>/scratch/` for all temporary executions.

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
