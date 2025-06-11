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
    members = set()
    page = 1
    while True:
        url = f"https://api.github.com/search/code?q={SEARCH_TAG}+in:file&per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS).json()
        for item in r.get("items", []):
            user = item["repository"]["owner"]["login"]
            members.add(user)
        if len(r.get("items", [])) < 100:
            break
        page += 1
    return sorted(members)

# Get list of all repos in the organization
def get_org_repos():
    repos = []
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=500"
    while url:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        repos += [repo["name"] for repo in res.json()]
        url = res.links.get("next", {}).get("url")
    return repos

# Get user contributions per repo
def get_contributions(user, repos):
    pr_count = issue_count = commit_total = repo_contributed = 0
    for repo in repos:
        pr_url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/pulls?state=all&per_page=1&creator={user}"
        pr_res = requests.get(pr_url, headers=HEADERS)
        if pr_res.status_code == 200:
            pr_count += int(pr_res.headers.get("Link", "").count("rel=\"next\"")) + len(pr_res.json())

        issue_url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/issues?state=all&per_page=1&creator={user}"
        issue_res = requests.get(issue_url, headers=HEADERS)
        if issue_res.status_code == 200:
            issue_count += int(issue_res.headers.get("Link", "").count("rel=\"next\"")) + len(issue_res.json())

        commit_url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/commits?author={user}&per_page=1"
        commit_res = requests.get(commit_url, headers=HEADERS)
        if commit_res.status_code == 200:
            commit_total += int(commit_res.headers.get("Link", "").count("rel=\"next\"")) + len(commit_res.json())
            if len(commit_res.json()) > 0:
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
  <h2>🐝 BSGOU Member Directory</h2>
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
