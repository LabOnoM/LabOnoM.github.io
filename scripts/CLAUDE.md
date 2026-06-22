# CLAUDE (Scripts Component Context)

This package contains Python-based data pipelines for member tracking, scrapers, and calculation engines.

## 1. Component Rules & Architecture

- **Main Pipeline**: `fetch_bsgou_members.py`
  - Scrapes contribution data (Commits, PRs, Issues, Repos) for members within the `LabOnoM` GitHub organization.
  - Normalizes scores using a Poisson-distribution formula to handle ranking statistics fairly.
  - Outputs are written directly to `members.html` and `members.xlsx` artifact files.
- **Git Token Shadowing**: If the scraper scripts fail due to API limit or token validation issues inside the IDE sandbox, run them by unsetting the dummy token: `env -u GITHUB_TOKEN python scripts/fetch_bsgou_members.py`.

---

## 2. Local Commands

- **Run Scraper Pipeline**: `python scripts/fetch_bsgou_members.py`
- **Install Dependencies**: `pip install requests openpyxl scipy numpy pandas`

---

## 3. Component Standards

- **Formatting**: Adhere to PEP 8 guidelines. Keep line lengths under 100 characters.
- **Typing**: Use static type hints (`typing` module) for all function arguments and return types.
- **Error Handling**: Use explicit try-except blocks for web requests and file operations; do not suppress errors silently.
