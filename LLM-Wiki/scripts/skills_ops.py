"""Skills catalog builder, capability deduplicator, versioned body cache, and priority router.

Inventories:
  1. Tier 1 (`global`): Active Antigravity built-in & plugin skills, plus host Codex/Claude/Gemini skill stores.
  2. Tier 2 (`project`): Repository-local skills under `.agents/skills/`.
  3. Tier 3 (`external`): All discoverable skills in `Yuan1z0825/nature-skills` and all 16 repositories in `K-Dense-AI`.

Deduplicates genuinely redundant external/unmounted skills by canonical capability against
higher-priority skills while retaining explicit omission records (`omissions.jsonl`) and
all complementary skills. Implements `global -> project -> external` priority routing and
progressive `skill-body` retrieval without bulk-installing external dependencies.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import math
import os
import re
import tarfile
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

# Pinned metadata for external repositories audited in Yuan1z0825/nature-skills and K-Dense-AI
PINNED_EXTERNAL_REPOS: List[Dict[str, Any]] = [
    {
        "repo": "Yuan1z0825/nature-skills",
        "url": "https://github.com/Yuan1z0825/nature-skills",
        "branch": "main",
        "tree_or_commit_sha": "d774add241c65e89ed17a4da573b472b0972fd42",
        "tarball_slug": "Yuan1z0825_nature-skills.tar.gz",
        "scope": "End-to-end scientific research, academic search, citation verification, figure styling, manuscript drafting, peer review, and rebuttal workflows.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/scientific-agent-skills",
        "url": "https://github.com/K-Dense-AI/scientific-agent-skills",
        "branch": "main",
        "tree_or_commit_sha": "a25cf9ec00",
        "tarball_slug": "K-Dense-AI_scientific-agent-skills.tar.gz",
        "scope": "Core K-Dense scientific agent skills across bioinformatics, single-cell/spatial omics, cheminformatics, physics, statistics, ML, and databases.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/claude-scientific-writer",
        "url": "https://github.com/K-Dense-AI/claude-scientific-writer",
        "branch": "main",
        "tree_or_commit_sha": "529b9f73ab",
        "tarball_slug": "K-Dense-AI_claude-scientific-writer.tar.gz",
        "scope": "Scientific manuscript writing, grant proposals, LaTeX/venue templates, peer review, clinical reports, and bundled scientific helpers.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/drug-discovery-agent-skills",
        "url": "https://github.com/K-Dense-AI/drug-discovery-agent-skills",
        "branch": "main",
        "tree_or_commit_sha": "ee7655f065",
        "tarball_slug": "K-Dense-AI_drug-discovery-agent-skills.tar.gz",
        "scope": "Computational drug discovery, ADMET, SAR, retrosynthesis, degraders/molecular glues, antibody engineering, and virtual screening.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/science-superpowers",
        "url": "https://github.com/K-Dense-AI/science-superpowers",
        "branch": "main",
        "tree_or_commit_sha": "0374bdf82c",
        "tarball_slug": "K-Dense-AI_science-superpowers.tar.gz",
        "scope": "Meta-scientific methodology skills: preregistration, feasibility checks, red-team review, anomaly investigation, and reproducible analysis setup.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/scientific-agents",
        "url": "https://github.com/K-Dense-AI/scientific-agents",
        "branch": "main",
        "tree_or_commit_sha": "98c7fae466",
        "tarball_slug": "K-Dense-AI_scientific-agents.tar.gz",
        "scope": "503 specialist scientific discipline persona skills spanning life sciences, clinical medicine, chemistry, physics, earth science, and engineering.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/mimeographs",
        "url": "https://github.com/K-Dense-AI/mimeographs",
        "branch": "main",
        "tree_or_commit_sha": "a38f5fcad0",
        "tarball_slug": "K-Dense-AI_mimeographs.tar.gz",
        "scope": "80 analytical reasoning and writing-style guides distilled from prominent scientists, mathematicians, engineers, and essayists.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/mimeo",
        "url": "https://github.com/K-Dense-AI/mimeo",
        "branch": "main",
        "tree_or_commit_sha": "a4cea1842a",
        "tarball_slug": "K-Dense-AI_mimeo.tar.gz",
        "scope": "Corpus extraction and style-guide synthesis pipeline (`extract-style`, `generate-corpus`, `synthesize-guide`) plus 19 early output profiles.",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/skill-101-webinar",
        "url": "https://github.com/K-Dense-AI/skill-101-webinar",
        "branch": "main",
        "tree_or_commit_sha": "f51b0a70c8",
        "tarball_slug": "K-Dense-AI_skill-101-webinar.tar.gz",
        "scope": "Instructional webinar templates (`plain-language-summary` and `paper-draft-SKILL` template).",
        "has_skills": True,
    },
    {
        "repo": "K-Dense-AI/agentic-data-scientist",
        "url": "https://github.com/K-Dense-AI/agentic-data-scientist",
        "branch": "main",
        "tree_or_commit_sha": "702dee9dfb",
        "tarball_slug": None,
        "scope": "Standalone Python agentic data science application (0 SKILL.md files; audited for completeness).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/claude-skills-mcp",
        "url": "https://github.com/K-Dense-AI/claude-skills-mcp",
        "branch": "main",
        "tree_or_commit_sha": "72a7b50223",
        "tarball_slug": None,
        "scope": "MCP server wrapper exposing K-Dense scientific skills over Model Context Protocol (0 standalone SKILL.md files).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/lab-instrument-mcps",
        "url": "https://github.com/K-Dense-AI/lab-instrument-mcps",
        "branch": "main",
        "tree_or_commit_sha": "46545ea7eb",
        "tarball_slug": None,
        "scope": "Laboratory hardware MCP servers (0 SKILL.md files; MCP server code only).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/rowan-autosearch",
        "url": "https://github.com/K-Dense-AI/rowan-autosearch",
        "branch": "main",
        "tree_or_commit_sha": "faebbb2aaa",
        "tarball_slug": None,
        "scope": "Rowan computational chemistry autosearch harness (contains 1 repo AGENTS.md, 0 SKILL.md files).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/k-dense-byok",
        "url": "https://github.com/K-Dense-AI/k-dense-byok",
        "branch": "main",
        "tree_or_commit_sha": "6a55f5ce6f",
        "tarball_slug": None,
        "scope": "Bring-Your-Own-Key web application stack (contains 1 repo AGENTS.md, 0 SKILL.md files).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/karpathy",
        "url": "https://github.com/K-Dense-AI/karpathy",
        "branch": "main",
        "tree_or_commit_sha": "f92b680a48",
        "tarball_slug": None,
        "scope": "Single-profile standalone repo superseded by `K-Dense-AI/mimeographs` (0 SKILL.md files).",
        "has_skills": False,
    },
    {
        "repo": "K-Dense-AI/hf-mva-hackathon-2026",
        "url": "https://github.com/K-Dense-AI/hf-mva-hackathon-2026",
        "branch": "main",
        "tree_or_commit_sha": "1fc4279131",
        "tarball_slug": None,
        "scope": "Hackathon submission repository (0 SKILL.md files).",
        "has_skills": False,
    },
]

# Canonical capability equivalence mapping aligning external/mirror skill names to Tier-1 Global capabilities
CAPABILITY_SYNONYMS: Dict[str, str] = {
    "chembl": "chembl-database",
    "chembl-database": "chembl-database",
    "pubchem": "pubchem-database",
    "pubchem-database": "pubchem-database",
    "uniprot": "uniprot-database",
    "uniprot-database": "uniprot-database",
    "clinvar": "clinvar-database",
    "clinvar-database": "clinvar-database",
    "clinicaltrials": "clinical-trials-database",
    "clinicaltrials-database": "clinical-trials-database",
    "clinical-trials-database": "clinical-trials-database",
    "ensembl": "ensembl-database",
    "ensembl-database": "ensembl-database",
    "pdb": "pdb-database",
    "pdb-database": "pdb-database",
    "alphafold": "alphafold-database",
    "alphafold-database": "alphafold-database",
    "alphafold-database-fetch-and-analyze": "alphafold-database",
    "gnomad": "gnomad-database",
    "gnomad-database": "gnomad-database",
    "gtex": "gtex-database",
    "gtex-database": "gtex-database",
    "opentargets": "opentargets-database",
    "opentargets-database": "opentargets-database",
    "openfda": "openfda-database",
    "fda-database": "openfda-database",
    "openfda-database": "openfda-database",
    "pubmed": "pubmed-database",
    "pubmed-database": "pubmed-database",
    "biorxiv-database": "literature-search-biorxiv",
    "literature-search-biorxiv": "literature-search-biorxiv",
    "openalex-database": "literature-search-openalex",
    "literature-search-openalex": "literature-search-openalex",
    "arxiv-database": "literature-search-arxiv",
    "literature-search-arxiv": "literature-search-arxiv",
    "europepmc-database": "literature-search-europepmc",
    "literature-search-europepmc": "literature-search-europepmc",
    "ols-database": "embl-ebi-ols",
    "embl-ebi-ols": "embl-ebi-ols",
    "reactome": "reactome-database",
    "reactome-database": "reactome-database",
    "string": "string-database",
    "string-database": "string-database",
    "interpro": "interpro-database",
    "interpro-database": "interpro-database",
    "jaspar": "jaspar-database",
    "jaspar-database": "jaspar-database",
    "pymol": "pymol-structure-viz",
    "rdkit": "rdkit-cheminformatics",
    "rdkit-general": "rdkit-cheminformatics",
    "autodock-vina": "cheminformatics-physics-docking",
    "cheminformatics-physics": "cheminformatics-physics-docking",
    "boltz": "cheminformatics-cofolding",
    "cheminformatics-cofolding": "cheminformatics-cofolding",
}

STOPWORDS = frozenset(
    {
        "the",
        "and",
        "for",
        "with",
        "use",
        "when",
        "from",
        "this",
        "that",
        "into",
        "using",
        "your",
        "are",
        "can",
        "how",
        "all",
        "any",
        "not",
        "skill",
        "data",
        "via",
        "or",
        "to",
        "of",
        "in",
        "on",
        "by",
        "a",
        "an",
    }
)


def _normalize_slug(raw: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", raw.strip().lower()).strip("-")


def canonical_capability_key(skill_name: str, rel_path: str, source_repo: str) -> str:
    slug = _normalize_slug(skill_name)
    if slug in CAPABILITY_SYNONYMS:
        return CAPABILITY_SYNONYMS[slug]
    # Align mimeo legacy output/<thinker>/SKILL.md with mimeographs/<thinker>/skills/<thinker>/SKILL.md
    if source_repo in ("K-Dense-AI/mimeo", "K-Dense-AI/mimeographs"):
        if "output/" in rel_path or "mimeographs/" in rel_path:
            return f"thinker-style:{slug}"
    if source_repo == "K-Dense-AI/scientific-agents":
        return f"specialist-persona:{slug}"
    return slug


def parse_skill_markdown(text: str, fallback_name: str) -> Dict[str, Any]:
    """Extract YAML front matter, headings, dependencies, and security signals from SKILL.md."""
    lines = text.splitlines()
    name = fallback_name
    description = ""
    license_val = ""
    version_val = ""

    if lines and lines[0].strip() == "---":
        fm_lines: List[str] = []
        end_idx = 0
        for idx, ln in enumerate(lines[1:120], start=1):
            if ln.strip() == "---":
                end_idx = idx
                break
            fm_lines.append(ln)
        if end_idx > 0:
            cur_key = ""
            desc_parts: List[str] = []
            for ln in fm_lines:
                m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ln)
                if m:
                    cur_key = m.group(1).lower()
                    val = m.group(2).strip().strip("'\"")
                    if cur_key == "name" and val:
                        name = val
                    elif cur_key == "description":
                        if val not in ("|", ">", ">-", "|-"):
                            desc_parts.append(val)
                    elif cur_key == "license" and val:
                        license_val = val
                    elif cur_key == "version" and val:
                        version_val = val
                elif cur_key == "description" and ln.startswith((" ", "\t")):
                    desc_parts.append(ln.strip())
            if desc_parts:
                description = " ".join(desc_parts).strip()

    if not description:
        # Fallback to first non-empty prose paragraph
        for ln in lines:
            s = ln.strip()
            if s and not s.startswith(("---", "#", "```", ">", "|", "- ")):
                description = s[:400]
                break

    headings = [
        ln.lstrip("#").strip()
        for ln in lines
        if re.match(r"^#{1,3}\s+", ln)
    ][:10]

    # Detect runtime / package / credential dependencies from skill text
    deps: Set[str] = set()
    for pkg in (
        "scanpy",
        "anndata",
        "stardist",
        "geopandas",
        "squidpy",
        "scvi-tools",
        "seurat",
        "biopython",
        "rdkit",
        "openmm",
        "pymol",
        "scipy",
        "statsmodels",
        "scikit-learn",
        "pytorch",
        "torch",
        "tensorflow",
        "networkx",
        "matplotlib",
        "seaborn",
        "plotly",
        "openpyxl",
        "pandas",
        "polars",
        "duckdb",
        "gcloud",
        "bq",
        "firebase",
        "jekyll",
        "adb",
    ):
        if re.search(rf"\b{re.escape(pkg)}\b", text, flags=re.IGNORECASE):
            deps.add(pkg)

    env_keys = sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}_(?:API_KEY|TOKEN|SECRET)\b", text)))
    has_install_cmds = bool(
        re.search(r"\b(?:pip\s+install|uv\s+pip\s+install|conda\s+install|npm\s+install|apt-get\s+install)\b", text)
    )
    has_network_calls = bool(
        re.search(r"https?://(?!(?:github\.com|doi\.org|www\.w3\.org|schemas\.))", text)
    )

    # Extract concise capability keywords
    token_src = f"{name} {description} {' '.join(headings[:4])}".lower()
    raw_tokens = re.findall(r"[a-z0-9][a-z0-9_-]{2,}", token_src)
    keywords: List[str] = []
    seen_kw: Set[str] = set()
    for tok in raw_tokens:
        if tok not in STOPWORDS and tok not in seen_kw:
            seen_kw.add(tok)
            keywords.append(tok)
        if len(keywords) >= 24:
            break

    return {
        "name": name,
        "description": description[:600],
        "license": license_val or None,
        "version": version_val or None,
        "headings": headings,
        "dependencies": sorted(deps),
        "required_env_vars": env_keys[:10],
        "security_flags": {
            "mentions_package_install": has_install_cmds,
            "mentions_external_endpoints": has_network_calls,
            "requires_credentials": bool(env_keys),
            "review_status": "host_trusted" if False else "review_before_exec",
        },
        "keywords": keywords,
        "body_bytes": len(text.encode("utf-8")),
        "body_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def _collect_local_dir_skills(
    base_dir: Path,
    tier: str,
    source_id: str,
    availability: str,
    priority_rank: int,
) -> List[Tuple[Dict[str, Any], str]]:
    items: List[Tuple[Dict[str, Any], str]] = []
    if not base_dir.is_dir():
        return items
    for skill_md in sorted(base_dir.rglob("SKILL.md")):
        if not skill_md.is_file():
            continue
        rel_p = skill_md.relative_to(base_dir).as_posix()
        fallback = skill_md.parent.name
        if fallback == "skills" and skill_md.parent.parent != base_dir:
            fallback = skill_md.parent.parent.name
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        parsed = parse_skill_markdown(text, fallback)
        if tier in ("global", "project") and availability.startswith("active_"):
            parsed["security_flags"]["review_status"] = "host_or_project_verified"
        cap_key = canonical_capability_key(parsed["name"], rel_p, source_id)
        slug = _normalize_slug(parsed["name"] or fallback)
        skill_id = f"{tier}:{source_id}:{slug}"
        rec = {
            "skill_id": skill_id,
            "name": parsed["name"],
            "tier": tier,
            "priority_rank": priority_rank,
            "availability": availability,
            "source_repo": source_id,
            "source_url": f"file://{skill_md}",
            "source_commit": "local-disk",
            "rel_path": rel_p,
            "capability_key": cap_key,
            "description": parsed["description"],
            "headings": parsed["headings"],
            "keywords": parsed["keywords"],
            "dependencies": parsed["dependencies"],
            "required_env_vars": parsed["required_env_vars"],
            "security_flags": parsed["security_flags"],
            "body_bytes": parsed["body_bytes"],
            "body_sha256": parsed["body_sha256"],
        }
        items.append((rec, text))
    return items


def _collect_tarball_skills(
    tar_path: Path,
    repo_meta: Dict[str, Any],
    priority_rank: int,
) -> Tuple[str, List[Tuple[Dict[str, Any], str]]]:
    items: List[Tuple[Dict[str, Any], str]] = []
    commit_sha = repo_meta["tree_or_commit_sha"]
    with tarfile.open(tar_path, "r:gz") as tf:
        if tf.pax_headers and tf.pax_headers.get("comment"):
            commit_sha = tf.pax_headers["comment"].strip()
        members = [
            m
            for m in tf.getmembers()
            if m.isfile() and (m.name.endswith("/SKILL.md") or m.name.endswith("SKILL.md"))
        ]
        members.sort(key=lambda m: m.name)
        for m in members:
            parts = m.name.split("/", 1)
            rel_p = parts[1] if len(parts) > 1 else m.name
            fobj = tf.extractfile(m)
            if fobj is None:
                continue
            text = fobj.read().decode("utf-8", errors="replace")
            parent_dir = Path(rel_p).parent.name or Path(rel_p).stem
            parsed = parse_skill_markdown(text, parent_dir)
            cap_key = canonical_capability_key(parsed["name"], rel_p, repo_meta["repo"])
            slug = _normalize_slug(parsed["name"] or parent_dir)
            repo_short = repo_meta["repo"].split("/")[-1]
            skill_id = f"external:{repo_short}:{slug}"
            rec = {
                "skill_id": skill_id,
                "name": parsed["name"],
                "tier": "external",
                "priority_rank": priority_rank,
                "availability": "indexed_external_cached",
                "source_repo": repo_meta["repo"],
                "source_url": f"{repo_meta['url']}/blob/{commit_sha}/{rel_p}",
                "source_commit": commit_sha,
                "rel_path": rel_p,
                "capability_key": cap_key,
                "description": parsed["description"],
                "headings": parsed["headings"],
                "keywords": parsed["keywords"],
                "dependencies": parsed["dependencies"],
                "required_env_vars": parsed["required_env_vars"],
                "security_flags": parsed["security_flags"],
                "body_bytes": parsed["body_bytes"],
                "body_sha256": parsed["body_sha256"],
            }
            items.append((rec, text))
    return commit_sha, items


def build_skills_catalog(
    repo_root: Path,
    scratch_repos_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Inventory global, project, and external skills; deduplicate by capability; write catalog & cache."""
    home = Path.home()
    candidates: List[Tuple[Dict[str, Any], str]] = []

    # 1. Tier 1A: Active Antigravity Host Skills (Built-in + Installed Plugins)
    candidates.extend(
        _collect_local_dir_skills(
            home / ".gemini" / "antigravity" / "builtin" / "skills",
            tier="global",
            source_id="antigravity-builtin",
            availability="active_host_global",
            priority_rank=10,
        )
    )
    plugins_dir = home / ".gemini" / "config" / "plugins"
    if plugins_dir.is_dir():
        for pdir in sorted(plugins_dir.iterdir()):
            if pdir.is_dir():
                candidates.extend(
                    _collect_local_dir_skills(
                        pdir,
                        tier="global",
                        source_id=f"antigravity-plugin:{pdir.name}",
                        availability="active_host_global",
                        priority_rank=12,
                    )
                )

    # 1. Tier 1B: Secondary Host-Installed Global Skill Stores (Codex, Claude Marketplace)
    candidates.extend(
        _collect_local_dir_skills(
            home / ".codex" / "skills",
            tier="global",
            source_id="codex-system",
            availability="host_installed_codex",
            priority_rank=16,
        )
    )
    candidates.extend(
        _collect_local_dir_skills(
            home / ".claude" / "plugins" / "marketplaces",
            tier="global",
            source_id="claude-marketplace",
            availability="host_installed_claude",
            priority_rank=18,
        )
    )

    # 2. Tier 2: Project-Local Skills (.agents/skills/)
    for proj_rec, proj_txt in _collect_local_dir_skills(
        repo_root / ".agents" / "skills",
        tier="project",
        source_id="LabOnoM.github.io",
        availability="active_project_local",
        priority_rank=20,
    ):
        proj_rec["source_url"] = f".agents/skills/{proj_rec['rel_path']}"
        candidates.append((proj_rec, proj_txt))

    # 3. Tier 3: External Collections (`Yuan1z0825/nature-skills` + `K-Dense-AI`)
    repo_audit_records: List[Dict[str, Any]] = []
    # Load existing cached bodies as fallback if scratch tarballs were already cleaned up
    existing_bodies = load_skill_bodies_map(repo_root)

    for idx, rmeta in enumerate(PINNED_EXTERNAL_REPOS):
        entry = dict(rmeta)
        tar_slug = rmeta.get("tarball_slug")
        tar_file = (scratch_repos_dir / tar_slug) if (scratch_repos_dir and tar_slug) else None
        if tar_file and tar_file.is_file():
            commit_sha, ext_items = _collect_tarball_skills(
                tar_file, rmeta, priority_rank=30 + idx
            )
            entry["resolved_commit_sha"] = commit_sha
            entry["discovered_skill_md_count"] = len(ext_items)
            candidates.extend(ext_items)
        else:
            entry["resolved_commit_sha"] = rmeta["tree_or_commit_sha"]
            entry["discovered_skill_md_count"] = 0
        repo_audit_records.append(entry)

    # 4. Tier 1C (lowest priority local mirror): Unmounted ~/.gemini/skills local disk pack
    # Placed after canonical K-Dense-AI / nature-skills only for exact mirror dedup?
    # Wait: host local unmounted skills vs pinned external GitHub repos:
    # Active global (10-18) > Project-local (20) > Pinned external repos (30-38) or local unmounted disk pack (25)?
    # Note: ~/.gemini/skills on this machine contains unversioned local copies of K-Dense/OpenClaw skills.
    # Keeping active host global (10-18) > project-local (20) > local unmounted unique skills (25) > external (30+)
    # OR deduplicating ~/.gemini/skills mirrors against active global/project and recording local availability!
    # Let's inventory ~/.gemini/skills at priority_rank=45 so version-pinned external GitHub records keep exact commit SHAs,
    # while any unique local-disk skills in ~/.gemini/skills not in GitHub repos are ALSO retained!
    candidates.extend(
        _collect_local_dir_skills(
            home / ".gemini" / "skills",
            tier="global_unmounted_cache",
            source_id="local-gemini-skills-dir",
            availability="local_disk_unmounted",
            priority_rank=45,
        )
    )

    # Sort deterministically by (priority_rank, source_repo, rel_path)
    candidates.sort(key=lambda pair: (pair[0]["priority_rank"], pair[0]["source_repo"], pair[0]["rel_path"]))

    retained: List[Dict[str, Any]] = []
    omissions: List[Dict[str, Any]] = []
    bodies_to_cache: Dict[str, str] = dict(existing_bodies)
    seen_capabilities: Dict[str, Dict[str, Any]] = {}
    seen_ids: Set[str] = set()

    for rec, body_text in candidates:
        cap = rec["capability_key"]
        # Ensure unique skill_id even if two non-redundant skills in same repo share a slug
        base_id = rec["skill_id"]
        if base_id in seen_ids:
            suffix = _normalize_slug(Path(rec["rel_path"]).parent.as_posix())
            rec["skill_id"] = f"{base_id}-{suffix}"

        winner = seen_capabilities.get(cap)
        # Active host global (rank <= 18) and active project-local (rank == 20) are NEVER omitted;
        # External and unmounted mirror skills with an identical canonical capability_key ARE omitted!
        if winner is not None and rec["priority_rank"] >= 30:
            omissions.append(
                {
                    "omitted_skill_id": rec["skill_id"],
                    "name": rec["name"],
                    "tier": rec["tier"],
                    "source_repo": rec["source_repo"],
                    "source_commit": rec["source_commit"],
                    "rel_path": rec["rel_path"],
                    "capability_key": cap,
                    "superseded_by_skill_id": winner["skill_id"],
                    "superseded_by_tier": winner["tier"],
                    "superseded_by_source": winner["source_repo"],
                    "reason": (
                        f"Redundant capability `{cap}` already provided at higher priority by "
                        f"`{winner['skill_id']}` ({winner['availability']})."
                    ),
                    "body_sha256": rec["body_sha256"],
                }
            )
            continue

        if cap not in seen_capabilities:
            seen_capabilities[cap] = rec
        seen_ids.add(rec["skill_id"])
        retained.append(rec)
        bodies_to_cache[rec["skill_id"]] = body_text

    skills_dir = repo_root / "LLM-Wiki" / "skills"
    cache_dir = repo_root / "LLM-Wiki" / ".cache"
    skills_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    catalog_path = skills_dir / "catalog.jsonl"
    omissions_path = skills_dir / "omissions.jsonl"
    repos_path = skills_dir / "repositories.json"
    body_cache_path = cache_dir / "skill_bodies_v1.jsonl.gz"

    catalog_path.write_text(
        "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in retained),
        encoding="utf-8",
    )
    omissions_path.write_text(
        "".join(json.dumps(o, sort_keys=True, ensure_ascii=False) + "\n" for o in omissions),
        encoding="utf-8",
    )

    tier_counts = Counter(r["tier"] for r in retained)
    source_counts = Counter(r["source_repo"] for r in retained)
    omitted_by_source = Counter(o["source_repo"] for o in omissions)

    repos_summary = {
        "schema_version": "1.0.0",
        "routing_precedence": [
            "1. global (active_host_global -> host_installed_codex/claude)",
            "2. project (.agents/skills/ active_project_local)",
            "3. external (pinned Yuan1z0825/nature-skills and K-Dense-AI complementary skills)",
            "4. global_unmounted_cache (unique local ~/.gemini/skills entries not in upstream repos)",
        ],
        "total_discovered_skill_md": len(candidates),
        "retained_count": len(retained),
        "omitted_redundant_count": len(omissions),
        "retained_by_tier": dict(sorted(tier_counts.items())),
        "retained_by_source": dict(sorted(source_counts.items())),
        "omitted_by_source": dict(sorted(omitted_by_source.items())),
        "external_repositories": repo_audit_records,
    }
    repos_path.write_text(
        json.dumps(repos_summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with gzip.open(body_cache_path, "wt", encoding="utf-8", compresslevel=6) as gz:
        for sid in sorted(bodies_to_cache):
            gz.write(
                json.dumps(
                    {"skill_id": sid, "body": bodies_to_cache[sid]},
                    ensure_ascii=False,
                )
                + "\n"
            )

    return repos_summary


def load_catalog(repo_root: Path) -> List[Dict[str, Any]]:
    path = repo_root / "LLM-Wiki" / "skills" / "catalog.jsonl"
    if not path.is_file():
        return []
    return [
        json.loads(ln)
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def load_omissions(repo_root: Path) -> List[Dict[str, Any]]:
    path = repo_root / "LLM-Wiki" / "skills" / "omissions.jsonl"
    if not path.is_file():
        return []
    return [
        json.loads(ln)
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]


def load_skill_bodies_map(repo_root: Path) -> Dict[str, str]:
    cache_path = repo_root / "LLM-Wiki" / ".cache" / "skill_bodies_v1.jsonl.gz"
    bodies: Dict[str, str] = {}
    if cache_path.is_file():
        with gzip.open(cache_path, "rt", encoding="utf-8") as gz:
            for ln in gz:
                if ln.strip():
                    obj = json.loads(ln)
                    bodies[obj["skill_id"]] = obj["body"]
    return bodies


def get_skill_body(repo_root: Path, skill_query: str) -> Optional[Dict[str, Any]]:
    """Retrieve exact SKILL.md body for a single selected skill (progressive loading)."""
    catalog = load_catalog(repo_root)
    match: Optional[Dict[str, Any]] = None
    q_low = skill_query.strip().lower()
    for rec in catalog:
        if rec["skill_id"].lower() == q_low or rec["name"].lower() == q_low:
            match = rec
            break
    if match is None:
        for rec in catalog:
            if q_low in rec["skill_id"].lower():
                match = rec
                break
    if match is None:
        return None

    bodies = load_skill_bodies_map(repo_root)
    body = bodies.get(match["skill_id"])

    # Live disk fallback for global/project skills if .cache was cleared
    if body is None:
        src_url = match.get("source_url", "")
        if src_url.startswith("file://"):
            p = Path(src_url[len("file://") :])
            if p.is_file():
                body = p.read_text(encoding="utf-8", errors="replace")
        elif src_url.startswith(".agents/"):
            p = repo_root / src_url
            if p.is_file():
                body = p.read_text(encoding="utf-8", errors="replace")

    return {"metadata": match, "body": body}


def fetch_external_skill_cache(repo_root: Path) -> Dict[str, int]:
    """Re-populate LLM-Wiki/.cache/skill_bodies_v1.jsonl.gz from pinned GitHub commit tarballs on demand."""
    repos_path = repo_root / "LLM-Wiki" / "skills" / "repositories.json"
    if not repos_path.is_file():
        raise FileNotFoundError("Missing LLM-Wiki/skills/repositories.json")
    repos_meta = json.loads(repos_path.read_text(encoding="utf-8"))
    catalog = load_catalog(repo_root)
    wanted_by_repo: Dict[str, Dict[str, str]] = {}
    for rec in catalog:
        if rec["tier"] == "external":
            wanted_by_repo.setdefault(rec["source_repo"], {})[rec["rel_path"]] = rec["skill_id"]

    bodies = load_skill_bodies_map(repo_root)
    fetched_count = 0
    for rmeta in repos_meta.get("external_repositories", []):
        repo_name = rmeta["repo"]
        if not rmeta.get("has_skills") or repo_name not in wanted_by_repo:
            continue
        wanted_paths = wanted_by_repo[repo_name]
        if all(sid in bodies for sid in wanted_paths.values()):
            continue
        sha = rmeta.get("resolved_commit_sha") or rmeta["tree_or_commit_sha"]
        url = f"https://codeload.github.com/{repo_name}/tar.gz/{sha}"
        with urllib.request.urlopen(url, timeout=60) as resp:
            raw = resp.read()
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
            for m in tf.getmembers():
                if not m.isfile():
                    continue
                parts = m.name.split("/", 1)
                rel_p = parts[1] if len(parts) > 1 else m.name
                if rel_p in wanted_paths:
                    fobj = tf.extractfile(m)
                    if fobj:
                        bodies[wanted_paths[rel_p]] = fobj.read().decode("utf-8", errors="replace")
                        fetched_count += 1

    cache_path = repo_root / "LLM-Wiki" / ".cache" / "skill_bodies_v1.jsonl.gz"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(cache_path, "wt", encoding="utf-8", compresslevel=6) as gz:
        for sid in sorted(bodies):
            gz.write(json.dumps({"skill_id": sid, "body": bodies[sid]}, ensure_ascii=False) + "\n")
    return {"cached_total": len(bodies), "newly_fetched": fetched_count}


def route_task_to_skills(
    repo_root: Path,
    task_query: str,
    top_k: int = 8,
) -> Dict[str, Any]:
    """Route a task across Global -> Project-Local -> External complementary skills.

    Enforces strict tier precedence when relevance is comparable:
      1. Active Host Global skills (`global`, `active_host_global`)
      2. Project-Local skills (`project`, `.agents/skills/`)
      3. Complementary External skills (`external`, `nature-skills` & `K-Dense-AI`)
    """
    catalog = load_catalog(repo_root)
    omissions = load_omissions(repo_root)

    raw_q_tokens = [
        t
        for t in re.findall(r"[a-z0-9][a-z0-9_-]{1,}", task_query.lower())
        if t not in STOPWORDS
    ]
    # Expand hyphenated tokens as sub-tokens too
    q_tokens: List[str] = []
    for t in raw_q_tokens:
        q_tokens.append(t)
        if "-" in t:
            q_tokens.extend(p for p in t.split("-") if len(p) >= 2 and p not in STOPWORDS)
    q_set = set(q_tokens)

    if not q_set:
        return {"query": task_query, "selected": [], "suppressed_redundant": []}

    # IDF across catalog documents
    doc_freq: Counter[str] = Counter()
    doc_blobs: List[Tuple[Dict[str, Any], Set[str], str]] = []
    for rec in catalog:
        text_blob = (
            f"{rec['name']} {rec['capability_key']} {rec['description']} "
            f"{' '.join(rec.get('keywords', []))} {' '.join(rec.get('headings', []))}"
        ).lower()
        toks = set(re.findall(r"[a-z0-9][a-z0-9_-]{1,}", text_blob))
        expanded: Set[str] = set(toks)
        for tok in toks:
            if "-" in tok:
                expanded.update(p for p in tok.split("-") if len(p) >= 2)
        for qt in q_set:
            if qt in expanded:
                doc_freq[qt] += 1
        doc_blobs.append((rec, expanded, text_blob))

    n_docs = max(1, len(catalog))
    scored_by_tier: Dict[str, List[Dict[str, Any]]] = {
        "global": [],
        "project": [],
        "external": [],
    }

    for rec, doc_toks, text_blob in doc_blobs:
        matched = sorted(q_set & doc_toks)
        if not matched:
            continue
        lexical_score = 0.0
        name_toks = set(re.findall(r"[a-z0-9]+", rec["name"].lower()))
        cap_toks = set(re.findall(r"[a-z0-9]+", rec["capability_key"].lower()))
        kw_set = set(rec.get("keywords", []))
        for qt in matched:
            idf = math.log(1.0 + (n_docs - doc_freq[qt] + 0.5) / (doc_freq[qt] + 0.5))
            weight = 1.0
            if qt in name_toks or qt in cap_toks:
                weight = 2.8
            elif qt in kw_set:
                weight = 1.6
            lexical_score += idf * weight

        # Phrase match bonus
        q_norm = " ".join(raw_q_tokens)
        if len(q_norm) >= 4 and q_norm in text_blob:
            lexical_score += 4.0

        # Coverage ratio bonus
        coverage = len(matched) / max(1, len(q_set))
        relevance = round(lexical_score * (0.55 + 0.45 * coverage), 4)
        if relevance < 2.2 or (len(q_set) >= 3 and len(matched) < 2):
            continue

        bucket = (
            "global"
            if rec["tier"] == "global" and rec["availability"] == "active_host_global"
            else ("project" if rec["tier"] == "project" else "external")
        )
        # Demote specialist-persona / thinker-style unless explicitly requested
        if rec["capability_key"].startswith(("specialist-persona:", "thinker-style:")):
            if not any(w in q_set for w in ("persona", "agent", "specialist", "style", "write", "essay")):
                relevance = round(relevance * 0.45, 4)

        scored_by_tier[bucket].append(
            {
                "skill_id": rec["skill_id"],
                "name": rec["name"],
                "tier": rec["tier"],
                "routing_bucket": bucket,
                "availability": rec["availability"],
                "source_repo": rec["source_repo"],
                "source_commit": rec["source_commit"],
                "capability_key": rec["capability_key"],
                "relevance_score": relevance,
                "matched_terms": matched,
                "dependencies": rec.get("dependencies", []),
                "security_review": rec.get("security_flags", {}).get("review_status"),
                "description": rec["description"][:220],
            }
        )

    for b in scored_by_tier:
        scored_by_tier[b].sort(
            key=lambda x: (-x["relevance_score"], x["skill_id"])
        )

    best_overall = max(
        (
            item["relevance_score"]
            for bucket_items in scored_by_tier.values()
            for item in bucket_items
        ),
        default=0.0,
    )
    suitability_floor = max(4.0, round(0.45 * best_overall, 4))

    # Assemble strict priority-ordered routing plan:
    # 1. Suitable Global skills first
    # 2. Suitable Project-local skills next
    # 3. Complementary External skills for remaining capability gaps not already covered
    selected: List[Dict[str, Any]] = []
    covered_caps: Set[str] = set()

    for item in scored_by_tier["global"][:3]:
        if item["relevance_score"] >= suitability_floor:
            item["routing_rationale"] = "Tier-1 active host global skill matches task capability."
            selected.append(item)
            covered_caps.add(item["capability_key"])

    for item in scored_by_tier["project"][:3]:
        if (
            item["relevance_score"] >= suitability_floor
            and item["capability_key"] not in covered_caps
        ):
            item["routing_rationale"] = "Tier-2 project-local BSGOU/LLM-Wiki workflow skill."
            selected.append(item)
            covered_caps.add(item["capability_key"])

    remaining_slots = max(1, top_k - len(selected))
    ext_floor = max(3.5, round(0.35 * best_overall, 4))
    for item in scored_by_tier["external"]:
        if len(selected) >= top_k or remaining_slots <= 0:
            break
        if item["relevance_score"] < ext_floor or item["capability_key"] in covered_caps:
            continue
        item["routing_rationale"] = (
            "Tier-3 complementary external skill filling capability gap; inspect body via "
            f"`wiki_cli.py skill-body {item['skill_id']}` and review instructions before execution."
        )
        selected.append(item)
        covered_caps.add(item["capability_key"])
        remaining_slots -= 1

    # Surface any omitted external duplicates whose capability matched the selected global/project skills
    omitted_hits = [
        {
            "omitted_skill_id": o["omitted_skill_id"],
            "source_repo": o["source_repo"],
            "capability_key": o["capability_key"],
            "superseded_by_skill_id": o["superseded_by_skill_id"],
        }
        for o in omissions
        if o["capability_key"] in covered_caps
    ][:10]

    return {
        "query": task_query,
        "precedence_policy": "global -> project -> external (complementary gaps only)",
        "progressive_loading_note": (
            "Router returns metadata only. Load full instructions only for chosen skill(s) via "
            "`python3 LLM-Wiki/scripts/wiki_cli.py skill-body <skill_id>`."
        ),
        "selected_count": len(selected),
        "selected": selected,
        "suppressed_redundant_external": omitted_hits,
    }
