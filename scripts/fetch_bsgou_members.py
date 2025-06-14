import os
import requests
import pandas as pd
import numpy as np
import scipy.stats as stats

# === Configuration ===
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ORG_NAME = "LabOnoM"
SEARCH_TAG = '<!-- RecognizeID=BSGOU_Member_a;slkA#(T*d76jbtfgm*AUHV∞®§´†∂UCA(•§¶J# -->'

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

def fetch_members():
    """Return a sorted list of unique GitHub users recognized by SEARCH_TAG.

    The tag is searched both in forked and non-forked repositories because the
    result counts can differ between the two. Duplicated users from the two
    searches are removed.
    """

    members = set()

    # Search once in non-fork repositories and once in forks. GitHub defaults to
    # non-forks, so we run two separate queries and combine the unique users.
    for fork_param in ("", "fork:true"):
        page = 1
        while True:
            query = f'"{SEARCH_TAG}" in:file'
            if fork_param:
                query += f" {fork_param}"
            params = {
                "q": query,
                "per_page": 100,
                "page": page,
            }
            r = requests.get(
                "https://api.github.com/search/code",
                headers=HEADERS,
                params=params,
            ).json()
            for item in r.get("items", []):
                user = item["repository"]["owner"]["login"]
                if user != ORG_NAME:
                    members.add(user)
            if len(r.get("items", [])) < 100:
                break
            page += 1

    return sorted(members)

# Get list of all repos in the organization
def get_org_repos():
    """Return a list of repositories for the organization."""

    repos = []
    page = 1
    while True:
        params = {
            "per_page": 100,
            "page": page,
        }
        res = requests.get(
            f"https://api.github.com/orgs/{ORG_NAME}/repos",
            headers=HEADERS,
            params=params,
        )
        res.raise_for_status()
        batch = res.json()
        repos.extend(repo["name"] for repo in batch)
        if len(batch) < 100:
            break
        page += 1
    return repos

# Get user contributions per repo
def get_contributions(user, repos):
    pr_count = issue_count = commit_total = repo_contributed = 0

    def paged_count(url, params):
        """Count items from a paginated GitHub API listing."""
        total = 0
        page = 1
        while True:
            params["page"] = page
            res = requests.get(url, headers=HEADERS, params=params)
            if res.status_code != 200:
                break
            items = res.json()
            total += len(items)
            if len(items) < 100:
                break
            page += 1
        return total

    def search_count(query):
        """Return the number of search results for the GitHub search API."""
        total = 0
        page = 1
        while True:
            params = {"q": query, "per_page": 100, "page": page}
            res = requests.get(
                "https://api.github.com/search/issues", headers=HEADERS, params=params
            )
            if res.status_code != 200:
                break
            data = res.json()
            items = data.get("items", [])
            total += len(items)
            if len(items) < 100:
                break
            page += 1
        return total

    for repo in repos:
        pr_count += search_count(
            f"repo:{ORG_NAME}/{repo} type:pr author:{user}"
        )

        issue_count += paged_count(
            f"https://api.github.com/repos/{ORG_NAME}/{repo}/issues",
            {"state": "all", "per_page": 100, "creator": user},
        )

        commits = paged_count(
            f"https://api.github.com/repos/{ORG_NAME}/{repo}/commits",
            {"author": user, "per_page": 100},
        )
        commit_total += commits
        if commits > 0:
            repo_contributed += 1

    return pr_count, issue_count, commit_total, repo_contributed

# Scoring and normalization
def calculate_scores(df):
    df["Raw"] = 5 * df["PRs"] + 3 * df["Issues"] + 2 * df["Commits"] + df["Repos"]
    max_raw = df["Raw"].max()
    df["Linear"] = (df["Raw"] / max_raw) * 100
    lambda_ = df["Raw"].mean()
    df["Poisson"] = 100 - stats.poisson.sf(df["Raw"] - 1, mu=lambda_) * 100
    df["Final"] = 0.5 * df["Linear"] + 0.5 * df["Poisson"]
    df = df.sort_values("Final", ascending=False).reset_index(drop=True)
    return df

def generate_outputs(df):
    df.to_excel("members.xlsx", index=False)

    html_head = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BSGOU Member Directory</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #f5f7fa; margin: 0; padding: 20px; }
    h2 { color: #222; }
    table { border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    th, td { text-align: center; padding: 12px; border-bottom: 1px solid #eee; }
    th { background: #004466; color: white; }
    tr:hover { background-color: #f1f1f1; }
    a { color: #007acc; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h2><a href="members.html" target="_blank">🐝 BSGOU Member Directory</a></h2>
  <p>Ranked by Contribution Score (50% linear + 50% Poisson normalization).</p>
  <p>For more details, please check a demo of
     <a href="https://www.bs-gou.com/2025/06/12/BSGOU-Contribution-Score.html" target="_blank">
     🐝 BSGOU Contribution Score Calculation</a></p>
  <table>
    <thead>
      <tr>
        <th>GitHub ID</th>
        <th>PRs</th>
        <th>Issues</th>
        <th>Commits</th>
        <th>Repos</th>
        <th>Raw Score</th>
        <th>Linear Score</th>
        <th>Poisson Score</th>
        <th>Contribution Score</th>
      </tr>
    </thead>
    <tbody>
"""

    html_rows = ""
    for _, row in df.iterrows():
        html_rows += f"""<tr>
  <td><a href="https://github.com/{row['GitHub ID']}" target="_blank">{row['GitHub ID']}</a></td>
  <td>{row['PRs']}</td>
  <td>{row['Issues']}</td>
  <td>{row['Commits']}</td>
  <td>{row['Repos']}</td>
  <td>{row['Raw']:.2f}</td>
  <td>{row['Linear']:.2f}</td>
  <td>{row['Poisson']:.2f}</td>
  <td>{row['Final']:.2f}</td>
</tr>
"""

    html_footer = """    </tbody>
  </table>
</body>
</html>"""

    with open("members.html", "w", encoding="utf-8") as f:
        f.write(html_head + html_rows + html_footer)


# Main pipeline
if __name__ == "__main__":
    members = fetch_members()
    repos = get_org_repos()
    records = []
    for user in members:
        pr, issue, commits, repo = get_contributions(user, repos)
        records.append({"GitHub ID": user, "PRs": pr, "Issues": issue, "Commits": commits, "Repos": repo})
    df = pd.DataFrame(records)
    df = calculate_scores(df)
    generate_outputs(df)
    print("✅ Generated members.html and members.xlsx")
