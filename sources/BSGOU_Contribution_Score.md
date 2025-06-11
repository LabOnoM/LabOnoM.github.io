# 🐝 BSGOU Contribution Score Calculation Demo

This document explains how we calculate the contribution score for BSGOU (Bioinformatics Study Group in Okayama University) members. It is designed to fairly distribute recognition or shared resources (e.g., donations) based on actual contributions, while being robust against gaming by spammy commits or shallow participation.

## 📐 Scoring Formula

Each contributor receives a **raw score** based on their contribution activities:


$$\text{Raw Score}_i = 5 \times \text{PRs}_i + 3 \times \text{Issues}_i + 2 \times \text{Commits}_i + 1 \times \text{Repos}_i$$

Then, we apply two normalization steps:

1. **Linear Normalization** (relative to the top contributor):
   
   $$\text{Linear}_i = \left(\frac{\text{Raw Score}_i}{\max_j \text{Raw Score}_j}\right) \times 100$$

2. **Poisson Normalization** to emphasize rarity of high contributions:

   $$\text{Poisson}_i = 100 - \text{PoissonSF}(\text{Raw Score}_i - 1, \lambda), \quad \lambda = \text{mean of all raw scores}$$

   This gives a high score to contributors whose raw score is statistically rare (i.e., much higher than average).

3. **Final Score**: A weighted hybrid of the above:

   $$\text{Final Score}_i = 0.3 \times \text{Linear}_i + 0.7 \times \text{Poisson}_i$$

---

## 📊 Example

| GitHub ID | PRs | Issues | Commits | Repos | Raw Score | Linear Score | Poisson Score | Final Score |
|-----------|-----|--------|---------|--------|------------|------------|--------------|----------------|
| alice     | 6   | 4      | 10      | 2      | 56         | 100.00     | 100.00       | 100.00         |
| eve       | 3   | 2      | 8       | 1      | 32         | 57.14      | 87.64        | 78.49          |
| bob       | 2   | 2      | 3       | 1      | 25         | 44.64      | 42.64        | 43.24          |
| grace     | 1   | 1      | 0       | 0      | 8          | 14.29      | 0.01         | 4.29           |
| carol     | 1   | 1      | 2       | 1      | 12         | 21.43      | 0.10         | 6.50           |
| felix     | 1   | 0      | 0       | 0      | 5          | 8.93       | 0.00         | 2.68           |
| dan       | 0   | 0      | 1       | 1      | 3          | 5.36       | 0.00         | 1.61           |
| hank      | 0   | 1      | 0       | 0      | 3          | 5.36       | 0.00         | 1.61           |
| tom       | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| mia       | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| sam       | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| zoe       | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| john      | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| nina      | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| alex      | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| bella     | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| chris     | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| dana      | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| emily     | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |
| iris      | 0   | 0      | 0       | 0      | 0          | 0.00       | 0.00         | 0.00           |

> Most members have no contributions. The hybrid scoring preserves rank and distributes scores steeply to emphasize genuine effort.

---

## 🤔 Why This Method?

- **Preserve Ranking**: Top contributors maintain their rank by raw score.
- **Resist Gaming**: A high commit count alone won't reward shallow contributions.
- **Reward Rarity**: Poisson normalization highlights how unusual a high score is.
- **Fair Distribution**: Passive members receive minimal share; active ones are rewarded fairly.
- **Discourage Minimal Contributions**: Members who make very small, low-effort contributions (e.g., just one PR or issue) receive minimal recognition due to the nature of the scoring formula and normalization. The Poisson adjustment especially penalizes common, low-level activity, ensuring that only meaningful, sustained effort gets proportionally rewarded.

This model allows BSGOU to transparently recognize contributions and distribute benefits (e.g., donations) without manual judgment or bias.

---

## 📬 Feedback

If you have questions or suggestions, please raise an issue at [github.com/LabOnoM](https://github.com/LabOnoM).
