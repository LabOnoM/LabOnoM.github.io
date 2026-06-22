# CODE_MAP (Workspace Topology Index)

This map defines the layout, pipeline matrix, and dependency rules of the Bioinformatics Study Group Okayama University (BSGOU) repository.

---

## 1. Directory Structure Outline

```
LabOnoM.github.io/
├── .github/             # GitHub Actions configurations (cron-based updates)
├── .wiki/               # LLM-Wiki containing domain concept definitions and timelines
├── 00.RawData/          # Raw data directory housing the master PIPELINE_REGISTRY.md
├── GSE284271/           # Visium HD nuclei segmentation datasets and output reports
├── _data/               # Jekyll site data models (YAML/JSON rosters)
├── _includes/           # Jekyll HTML fragments (reusable layouts)
├── _layouts/            # Jekyll layout definitions (home, post, page template wrappers)
├── _posts/              # Jekyll blog posts database (YYYY-MM-DD-title.md)
├── _sass/               # Sass stylesheets for styling variables
├── assets/              # Static assets, fonts, icons, search scripts, and manifest configurations
├── css/                 # Compiled/vendor stylesheets (style.css, bootstrap.min.css)
├── fonts/               # Static typography assets
├── img/                 # General website image assets, slider images, and favicons
├── js/                  # Website logic scripts (custom.js theme & swipe mechanics)
├── scripts/             # Main python pipeline scripts (fetch_bsgou_members.py)
├── sources/             # Generated member lists and contribution tables (HTML/Excel)
└── tools/               # Command-line helper utilities and diff validation scripts
```

---

## 2. Directory & Pipeline Matrix

| Component Directory | Language | Role / Purpose | Upstream Integration |
|---|---|---|---|
| `scripts/` | Python | Member contribution parsing, ranking calculations (Poisson normalization) | Runs on push events in `.github/workflows/update_members.yml` |
| `css/` / `js/` / `img/` | CSS / Vanilla JS | Site layout styling, theme switching (dark/light), sliding carousels, mobile navigation | Interacts with `index.html` elements |
| `GSE284271/` | Python / HTML | Visium HD Nuclei Segmentation, spatial binning, Scanpy clustering reports | Custom Jupyter/Scanpy analytical pipelines |
| `.wiki/` | Markdown | AROS LLM-Wiki capturing lessons learned, timeline validation, project specs | Grounded to `/wiki-` workflows and system agents |
| `tools/` | Bash / JS | Local workspace validations, URL assertions, directory tree generators | CLI developer utility helpers |

---

## 3. External Dependencies & Frameworks

- **Jekyll (Static Site Generator)**: Compiles HTML pages using Liquid templates. Controlled by `_config.yml` and `Gemfile`.
- **Python 3**: Used in data parsing scripts (`fetch_bsgou_members.py`) and data analysis.
  - *Key Python Packages*: `requests`, `openpyxl` (member scraper), `scipy`, `numpy`, `pandas`, `scanpy`, `stardist` (spatial transcriptomics analysis).
- **Node.js**: Runs image path validation and link assertion scripts (`tools/assert-url.js`).

---

## 4. Key Documentation Index

- [SPEC.md](file:///home/ubuntu4/GitHub/LabOnoM.github.io/SPEC.md): UI styling, layout parameters, theme class names, mobile suppression, and touch gesture variables.
- [AGENTS.md](file:///home/ubuntu4/GitHub/LabOnoM.github.io/AGENTS.md): Codex Agent behavioral rules, testing instructions (`jekyll build`), and AROS integration policies.
- [PIPELINE_REGISTRY.md](file:///home/ubuntu4/GitHub/LabOnoM.github.io/00.RawData/PIPELINE_REGISTRY.md): Tracks status and descriptions of all computational pipelines.
- [.wiki/lessons-learned.md](file:///home/ubuntu4/GitHub/LabOnoM.github.io/.wiki/lessons-learned.md): Logs structural engineering rules, conda compiler flags, and workspace fixes.
