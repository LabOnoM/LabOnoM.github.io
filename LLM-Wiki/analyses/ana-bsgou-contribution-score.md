---
id: ana-bsgou-contribution-score
type: analysis
status: verified_with_flagged_contradictions
updated_at: 2026-11-06
source_refs:
  - _posts/2025-06-12-BSGOU-Contribution-Score.md
  - scripts/fetch_bsgou_members.py#L83-L154
  - scripts/update-members.sh
  - members.html
tags:
  - analysis
  - contribution-score
  - poisson-sf
  - github-api
  - members
---

# Analysis: BSGOU Community Contribution Scoring Pipeline & Formula Audit

## Cross-Links
- **Code Map**: [[code-map]]
- **Flagged Contradictions**: [[contradictions]] (`CON-05`, `CON-08`)
- **Decisions**: [[decisions]]

## 1. Raw Activity Point Formula (`scripts/fetch_bsgou_members.py#L83-L144`)
`fetch_bsgou_members.py` enumerates public repositories in `LabOnoM` (`get_org_repos`) and computes four counts per member (`get_contributions`, lines `83–139`), combined at line `143` via `pandas`:
$$\text{Raw}_i = 5 \cdot \text{PRs}_i + 3 \cdot \text{Issues}_i + 2 \cdot \text{Commits}_i + 1 \cdot \text{Repos}_i$$

| Term | Source Endpoint (`fetch_bsgou_members.py`) | Weight (`L143`) | Implementation Detail Observed |
|---|---|---:|---|
| `PRs` | `/search/issues?q=repo:LabOnoM/<repo> type:pr author:<user>` (`L122–124`) | `5` | Counts authored PRs via Search API |
| `Issues` | `/repos/LabOnoM/<repo>/issues?state=all&creator=<user>` (`L126–129`) | `3` | Note: GitHub REST v3 `/issues` includes PRs unless `pull_request` key is filtered out |
| `Commits` | `/repos/LabOnoM/<repo>/commits?author=<user>` (`L131–135`) | `2` | Default branch commit count |
| `Repos` | `repo_contributed += 1` if `commits > 0` (`L136–137`) | `1` | Distinct `LabOnoM` repos with `>= 1` commit |

## 2. Hybrid Linear + Poisson Normalization (`scripts/fetch_bsgou_members.py#L144-L150`)
Given raw scores $\{s_1, \dots, s_N\}$ with maximum $s_{\max} = \max_i s_i$ and sample mean $\lambda = \frac{1}{N}\sum_{i=1}^N s_i$:
1. **Linear Score (`L145`)**:
   $$L_i = 100 \times \frac{s_i}{s_{\max}}$$
2. **Poisson Cumulative Score (`L147`)**:
   $$P_i = 100 - 100 \times \text{sf}_{\text{Poisson}}(s_i - 1;\; \mu = \lambda) = 100 \times P(X \le s_i - 1 \mid X \sim \text{Poisson}(\lambda))$$
   computed via `100 - stats.poisson.sf(df["Raw"] - 1, mu=lambda_) * 100` (`scipy.stats.poisson`).

## 3. Specification vs. Production Code Discrepancy (`CON-05`)
- **Published Blog Specification** (`_posts/2025-06-12-BSGOU-Contribution-Score.md#L395`):
  $$\text{Final Score}_{\text{post}} = 0.3 \cdot L_i + 0.7 \cdot P_i$$
- **Active Python Implementation** (`scripts/fetch_bsgou_members.py#L148`):
  $$\text{Final Score}_{\text{code}} = 0.5 \cdot L_i + 0.5 \cdot P_i$$
- **Exact Numerical Reproduction of `members.html`**:
  - `members.html` currently lists **$N = 1$ member**: `wong-ziyi` with `Raw = 4988` ($\lambda = 4988$, $s_{\max} = 4988$).
  - Under `L145–L148`: $L_1 = 100.00$, $P_1 = 100 - 100 \times \text{sf}_{\text{Poisson}}(4987;\; 4988) = 49.8117$, yielding $\text{Final}_1 = 0.5(100.00) + 0.5(49.8117) = 74.9058 \to \mathbf{74.91}$, matching `members.html` (`74.91`) to the hundredth! (Under the blog's `0.3 / 0.7` formula, the score would instead be `64.87`.)
- **Output Hygiene**: `generate_outputs` (`L152–L154`) writes `members.xlsx` (`pandas.DataFrame.to_excel`, untracked via `.gitignore`) and overwrites tracked `members.html`.

## 4. Manual Execution Policy (`CON-08`)
- `scripts/update-members.sh` replaced `.github/workflows/update_members.yml` on `2026-10-13` (commit `b5eedef`), but `00.RawData/PIPELINE_REGISTRY.md#L7` still lists `.github/workflows/update_members.yml` as `Active`.
