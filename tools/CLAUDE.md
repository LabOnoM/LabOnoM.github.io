# CLAUDE (Tools Component Context)

This package contains shell script and JavaScript helpers to automate checks and environment validation.

## 1. Tool Index & Command Usage

- **Directory Tree Printer** (`dir-tree.sh`):
  - prints the directory structure while ignoring build outputs (`_site`, `.jekyll-cache`) and dependencies.
  - Run: `./tools/dir-tree.sh`
- **Diff Script** (`diff.sh`):
  - Compare configurations between local dev and remote environments.
  - Run: `./tools/diff.sh`
- **Markdown URL Validator** (`assert-url.js`):
  - Scans markdown files and asserts relative image paths point to raw GitHub URLs to prevent rendering drift.
  - Run: `node tools/assert-url.js`

---

## 2. Coding Standards

- **Bash**: Write POSIX-compliant shell scripts. Ensure executable permissions are set.
- **Node.js**: Maintain zero external package dependencies for utility scripts if possible. Use ES6 syntax.
