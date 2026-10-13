# Entity: Member Fetch Pipeline

This pipeline automates the tracking of BSGOU members and calculates their contribution scores based on GitHub activity.

## Components
1. **Update script**: `scripts/update-members.sh` (the GitHub Actions workflow `update_members.yml` was removed on 2026-10-13)
   - Run by hand by the owner, once a month and after publishing a post or changing `index.html`.
   - Installs Python dependencies (`requests`, `pandas`, `scipy`, `openpyxl`) in a local virtual environment.
   - Runs `scripts/fetch_bsgou_members.py`.
   - Commits `members.html` and pushes it to `main`; `members.xlsx` stays local.
2. **Python Script**: `scripts/fetch_bsgou_members.py`
   - **Verification**: Scans the GitHub API for users with files containing the specific verification tag `<!-- RecognizeID=BSGOU_Member_a;slkA#(T*d76jbtfgm*AUHV∞®§´†∂UCA(•§¶J# -->`.
   - **Scoring**: Counts Pull Requests, Issues, Commits, and Repos contributed within the `LabOnoM` organization.
   - **Normalization**:
     - Raw Score = $5 \times \text{PRs} + 3 \times \text{Issues} + 2 \times \text{Commits} + \text{Repos}$
     - Linear Score = $(\text{Raw} / \text{Max Raw}) \times 100$
     - Poisson Score = $100 - \text{Poisson.sf}(\text{Raw}-1, \mu) \times 100$ (where $\mu$ is the average Raw score of all members).
     - Final Score = $0.5 \times \text{Linear} + 0.5 \times \text{Poisson}$
   - **Output**: Writes rankings to `members.html` and `members.xlsx`.

For details on the math, check the original post [[qpcr-analysis]] since the normalization is mathematically verified.
