---
name: bsgou-member-scoring
description: Execute, audit, and maintain the BSGOU GitHub contribution scraper and Linear+Poisson normalization pipeline (scripts/fetch_bsgou_members.py, scripts/update-members.sh, members.html).
---

# BSGOU Member Contribution Scoring (`bsgou-member-scoring`)

Use this project-local skill when updating `members.html`, modifying `scripts/fetch_bsgou_members.py`, or auditing BSGOU community contribution scores.

## Pipeline Architecture
- **Entry Script**: `scripts/update-members.sh` (run manually by the repository owner from a clean, up-to-date `main` branch; never automated via GitHub Actions).
- **Token Resolution**: Uses `BSGOU_GITHUB_TOKEN` if exported, otherwise falls back to `gh auth token`. Never hardcode or commit tokens.
- **Core Scorer**: `scripts/fetch_bsgou_members.py` queries `LabOnoM` public repositories, pull requests (`/search/issues`), issues (`/repos/.../issues`), commits (`/repos/.../commits`), and contributed repo counts (`Raw = 5*PRs + 3*Issues + 2*Commits + Repos`), writing tracked `members.html` and untracked `members.xlsx`.

## Known Specification vs Implementation Discrepancy
Check `LLM-Wiki/contradictions.md` (`CON-05`) before changing weights:
- **Blog specification** (`_posts/2025-06-12-BSGOU-Contribution-Score.md:395`): defines `Final Score = 0.3 * Linear Score + 0.7 * Poisson Score`.
- **Active code & rendered table** (`scripts/fetch_bsgou_members.py:147-148`, `members.html`): computes `Poisson = 100 - stats.poisson.sf(Raw - 1, mu=lambda_) * 100` and `Final = 0.5 * Linear + 0.5 * Poisson` (producing `74.91` for `Raw = 4988`).
Do not silently alter weights without an explicit owner decision recorded in `LLM-Wiki/decisions.md`.

## Dependencies & Execution
Run inside an isolated virtual environment containing `requests`, `pandas`, `openpyxl`, and `scipy`:
```bash
./scripts/update-members.sh
```
Note: `scripts/update-members.sh` automatically runs `git commit` and `git push origin HEAD:main` when `members.html` changes—do **not** invoke `update-members.sh` during dry-run or unpushed agent sessions; inspect or test `fetch_bsgou_members.py` in scratch instead.
