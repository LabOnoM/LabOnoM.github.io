# CLAUDE (Workspace Entry Rules)

This document contains global constraints, build/test command lists, and coding standards for Codex agents.

## 1. Codebase Navigation Rules

> [!IMPORTANT]
> 1. **Read `CODE_MAP.md` first** to understand the layout and topological mapping of packages and components.
> 2. Do not execute broad semantic searches or grep actions across the whole repository unless targeted.
> 3. Before modifying or inspecting a package or component, read its local `CLAUDE.md` context file (e.g., `scripts/CLAUDE.md` or `css/CLAUDE.md`).

---

## 2. LLM-Wiki Grounding, Skill Routing, & Drift Prevention

- **Startup & Strict Grounding**: Read `LLM-Wiki/STATE.md` and `LLM-Wiki/index.md` first (canonical persistent memory), and run `python3 LLM-Wiki/scripts/wiki_cli.py refresh --dry-run` + `git-state` to verify memory against live files. Legacy `.wiki/` remains in place for Obsidian `[[page]]` compatibility; always check `LLM-Wiki/contradictions.md` (`CON-01`–`CON-09`) before citing legacy summaries.
- **Progressive Retrieval & Evidence Checking**: Search locally via `python3 LLM-Wiki/scripts/wiki_cli.py search "<query>"` before broad file scans. Cite exact `path#Lstart-Lend`, sheet/cell, or internal archive paths for substantive claims, and distinguish observations from interpretations.
- **Skill Routing (`global -> project -> external`)**: Route tasks with `python3 LLM-Wiki/scripts/wiki_cli.py route "<task>"` (active host global skills $\to$ `.agents/skills/` project skills $\to$ complementary `nature-skills` / `K-Dense-AI` external skills). Fetch only selected bodies (`wiki_cli.py skill-body <id>`) and review external instructions before running commands.
- **Wikilinks**: Refer to domain entities using Obsidian-style double bracket links, e.g., `[[overview]]`, `[[contradictions]]`, or `[[lessons-learned]]`.
- **Refresh, Verification, & Checkpointing**: Whenever you modify a core data structure, styling convention, or computational pipeline, update affected `LLM-Wiki/` pages and `CODE_MAP.md`, run `python3 LLM-Wiki/scripts/wiki_cli.py refresh --reindex` and `python3 LLM-Wiki/scripts/wiki_cli.py verify`, append to `LLM-Wiki/log.md`, and stage only attributable docs/manifests/code (never commit `LLM-Wiki/.cache/`, secrets, or raw omics data).

---

## 3. Development Commands

- **LLM-Wiki Integrity & Search CLI**: `python3 LLM-Wiki/scripts/wiki_cli.py {scan,refresh,search,route,skill-body,git-state,verify}`
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
