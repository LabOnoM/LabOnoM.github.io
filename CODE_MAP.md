# CODE_MAP (Workspace Topology Index)

This map defines the layout, pipeline matrix, and dependency rules of the Bioinformatics Study Group Okayama University (BSGOU) repository.

---

## 1. Directory Structure Outline

```
LabOnoM.github.io/
├── LLM-Wiki/            # Canonical persistent memory, SHA-256 manifest, traceability chains, & skill router
├── .agents/             # Native workspace rules (.agents/rules/) and project skills (.agents/skills/)
├── .wiki/               # Legacy AROS LLM-Wiki preserved for Obsidian [[page]] compatibility
├── 00.RawData/          # Raw data directory housing PIPELINE_REGISTRY.md
├── GSE284271/           # Visium HD murine embryonic palate nuclei segmentation report (01.scRNAseq10xVisiumHD.html)
├── _data/               # Jekyll site data models (YAML/JSON navigation & locale)
├── _includes/           # Jekyll HTML fragments (reusable layouts)
├── _layouts/            # Jekyll layout definitions (home, post, page template wrappers)
├── _posts/              # Jekyll blog posts (YYYY-MM-DD-title.md) & PostAttachedFiles/ (.xlsx, .prism, .png)
├── _sass/               # Sass stylesheets for styling variables
├── assets/              # Static assets, fonts, icons, search scripts, and manifest configurations
├── css/                 # Compiled/vendor stylesheets (style.css, bootstrap.min.css)
├── fonts/               # Static typography assets (.otf, .woff, .woff2, .ttf, .eot)
├── img/                 # Website image assets, research gallery images, and favicons
├── js/                  # Website logic scripts (custom.js theme & swipe mechanics)
├── scripts/             # Member scraper & manual runner (fetch_bsgou_members.py, update-members.sh)
├── sources/             # Core value Markdown essays embedded via IFrames on index.html
└── tools/               # Command-line helper utilities (dir-tree.sh and legacy theme helpers)
```

---

## 2. Directory & Pipeline Matrix

| Component Directory | Language | Role / Purpose | Upstream Integration |
|---|---|---|---|
| `scripts/` | Python | Member contribution parsing, ranking calculations (Poisson normalization) | Run by hand with `scripts/update-members.sh` (no GitHub Actions) |
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

- [LLM-Wiki/index.md](LLM-Wiki/index.md): Master index of verified experiments, datasets, analyses, figures, results, contradictions, and skills.
- [LLM-Wiki/code-map.md](LLM-Wiki/code-map.md): Detailed component, script symbol, and file-format architecture map.
- [SPEC.md](SPEC.md): UI styling, layout parameters, theme class names, mobile suppression, and touch gesture variables.
- [AGENTS.md](AGENTS.md) & [CLAUDE.md](CLAUDE.md): Canonical multi-agent rules, testing instructions (`jekyll build`), skill routing, and manual CI/CD policy.
- [PIPELINE_REGISTRY.md](00.RawData/PIPELINE_REGISTRY.md): Registry of computational pipelines (see `CON-08` in `LLM-Wiki/contradictions.md` regarding manual `scripts/update-members.sh`).
- [.wiki/lessons-learned.md](.wiki/lessons-learned.md) & [LLM-Wiki/lessons-learned.md](LLM-Wiki/lessons-learned.md): Verified structural engineering and bioinformatics lessons.
