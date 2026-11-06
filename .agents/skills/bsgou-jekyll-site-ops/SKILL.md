---
name: bsgou-jekyll-site-ops
description: Build, edit, and validate the BSGOU (LabOnoM.github.io) Jekyll website, multilingual Markdown pages, blog posts, and UI assets under the repository's manual-CI/no-GitHub-Actions policy.
---

# BSGOU Jekyll Site Operations (`bsgou-jekyll-site-ops`)

Use this project-local skill whenever modifying website pages (`index.html`, `members.html`, `journalclub.md`, `README*.md`), value essays (`sources/*.md`), blog posts (`_posts/YYYY-MM-DD-title.md`), styles (`css/style.css`, `_sass/`), or UI scripts (`js/custom.js`).

## Hard Constraints
1. **No GitHub Actions**: LabOnoM has a strict owner policy (`2026-10-13`) prohibiting `.github/workflows/`. Never add CI workflows or claim status checks.
2. **Dual Role of Root `README.md`**: Root `README.md` carries Jekyll front matter (`layout: default`, `title: Vision and Strategic Plan`) and renders live at `/README.html` alongside `README_JP.md` and `README_CH.md`. Preserve its front matter, language switcher, and strategic plan prose.
3. **Post Conventions**: Blog posts live in `_posts/YYYY-MM-DD-title.md` with at least `title` and `layout` YAML front matter keys. Store shared experimental attachments in `_posts/PostAttachedFiles/` and site images in `img/` or `assets/`.
4. **Config Exclusions**: Keep `/LLM-Wiki`, `/.agents`, `/.claude`, `/Wiki`, and `/00.RawData` in `_config.yml` `exclude:` so internal knowledge-base Markdown never collides with Liquid rendering.

## Local Build & Verification Workflow
1. Run `bundle exec jekyll build` locally (using an isolated Ruby >= 3.0 environment if macOS system Ruby 2.6 is active; place temporary `_site` or `BUNDLE_PATH` outputs in session scratch rather than polluting the repo root).
2. Confirm zero Liquid/Kramdown errors and inspect generated HTML for modified routes (`/index.html`, `/README.html`, `/blog/`).
3. Note that legacy `tools/assert-url.js` and `tools/diff.sh` came from upstream `jekyll-TeXt-theme` and expect `./test/_posts` and `./docs/en` (which do not exist in this repo); do not mistake their missing-directory failures for site regressions.
4. Refresh `LLM-Wiki` manifest after edits:
   ```bash
   python3 LLM-Wiki/scripts/wiki_cli.py refresh
   ```
