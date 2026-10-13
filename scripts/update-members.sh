#!/usr/bin/env bash
# Regenerate the website's member list (members.html, plus members.xlsx) and publish it.
# Replaces the former GitHub Actions workflow .github/workflows/update_members.yml, removed on 2026-10-13
# (LabOnoM does not use GitHub Actions), which ran on every push touching index.html or _posts/**.
# When to run: by hand, once a month and after publishing a post or changing index.html, from an up-to-date main.
# Credentials: BSGOU_GITHUB_TOKEN from the owner's environment if set (the token the workflow used), otherwise the
# owner's own `gh auth login` token. Nothing is read from a file in the repository.
set -euo pipefail
cd "$(dirname "$0")/.."

# Guards: the commit is pushed straight to main, which GitHub Pages serves.
branch=$(git rev-parse --abbrev-ref HEAD)
[ "$branch" = main ] || { echo "FAIL  run from main, not $branch" >&2; exit 1; }
git fetch --quiet origin main
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || { echo "FAIL  local main differs from origin/main" >&2; exit 1; }
[ -z "$(git status --porcelain -- members.html)" ] || { echo "FAIL  members.html has uncommitted changes" >&2; exit 1; }

# Ignore a GITHUB_TOKEN already in the environment: IDE sessions inject a dummy one (.wiki/system/lessons-learned.md).
token="${BSGOU_GITHUB_TOKEN:-$(env -u GITHUB_TOKEN -u GH_TOKEN gh auth token)}"

# "Set up Python" (3.10) and "Install dependencies", in a virtual environment outside the repository.
venv="${XDG_CACHE_HOME:-$HOME/.cache}/labonom-website-members/venv"
[ -x "$venv/bin/python" ] || python3.10 -m venv "$venv"
"$venv/bin/python" -m pip install --quiet requests pandas scipy openpyxl

# "Run fetch_bsgou_members.py": writes members.html and members.xlsx in the repository root.
GITHUB_TOKEN="$token" "$venv/bin/python" scripts/fetch_bsgou_members.py

# "Commit": only members.html is committed, as before.
git add members.html
if git diff --staged --quiet; then
  echo "No changes to commit"
else
  git commit --quiet -m "Update members.html"
  env -u GITHUB_TOKEN -u GH_TOKEN git push --quiet origin main
  echo "OK    pushed $(git rev-parse --short HEAD) to main"
fi
# The workflow uploaded members.xlsx and members.html as run artifacts; here they stay in the working tree.
echo "      members.xlsx is in $(pwd) (not committed)."
