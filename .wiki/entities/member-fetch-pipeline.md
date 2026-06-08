# Entity: Member Fetch Pipeline

This pipeline automates the tracking of BSGOU members and calculates their contribution scores based on GitHub activity.

## Components
1. **GitHub Workflow**: `.github/workflows/update_members.yml`
   - Executes daily at 3 AM UTC.
   - Installs Python dependencies (`requests`, `pandas`, `scipy`, `openpyxl`).
   - Runs `scripts/fetch_bsgou_members.py`.
   - Automatically commits `members.html` and uploads artifacts.
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
