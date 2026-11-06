"""Full-text SQLite FTS5 search index and end-to-end verification suite for LLM-Wiki."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .inspectors import compute_git_blob_oid, compute_raw_sha256
from .manifest_ops import (
    SELF_EXCLUDED_REL_FILES,
    inspect_git_and_worktrees,
    load_manifest_map,
    scan_or_refresh_manifest,
)
from .skills_ops import (
    get_skill_body,
    load_catalog,
    load_omissions,
    load_skill_bodies_map,
    route_task_to_skills,
)


def _fts_Index_path(repo_root: Path) -> Path:
    return repo_root / "LLM-Wiki" / ".cache" / "search_index.sqlite"


def build_search_index(repo_root: Path) -> Dict[str, int]:
    """Build disposable SQLite FTS5 index over LLM-Wiki pages, manifest, and skill bodies."""
    db_path = _fts_Index_path(repo_root)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.is_file():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute(
        """
        CREATE VIRTUAL TABLE docs_fts USING fts5(
            doc_id UNINDEXED,
            scope UNINDEXED,
            title,
            path UNINDEXED,
            body,
            tokenize='porter unicode61'
        );
        """
    )

    counts = {"wiki": 0, "legacy_wiki": 0, "manifest": 0, "skills": 0}
    rows: List[Tuple[str, str, str, str, str]] = []

    # 1. Canonical LLM-Wiki Markdown pages
    wiki_dir = repo_root / "LLM-Wiki"
    if wiki_dir.is_dir():
        for md in sorted(wiki_dir.rglob("*.md")):
            rel_p = md.relative_to(repo_root).as_posix()
            txt = md.read_text(encoding="utf-8", errors="replace")
            m_h1 = re.search(r"^#\s+(.+)$", txt, flags=re.MULTILINE)
            title = m_h1.group(1).strip() if m_h1 else md.stem
            rows.append((f"wiki:{rel_p}", "wiki", title, rel_p, txt))
            counts["wiki"] += 1

    # 2. Legacy .wiki Markdown pages (indexed under legacy_wiki scope for auditability)
    legacy_dir = repo_root / ".wiki"
    if legacy_dir.is_dir():
        for md in sorted(legacy_dir.rglob("*.md")):
            rel_p = md.relative_to(repo_root).as_posix()
            txt = md.read_text(encoding="utf-8", errors="replace")
            m_h1 = re.search(r"^#\s+(.+)$", txt, flags=re.MULTILINE)
            title = m_h1.group(1).strip() if m_h1 else md.stem
            rows.append((f"legacy_wiki:{rel_p}", "legacy_wiki", title, rel_p, txt))
            counts["legacy_wiki"] += 1

    # 3. File manifest records
    manifest_map = load_manifest_map(repo_root / "LLM-Wiki" / "manifest" / "manifest.jsonl")
    for rel_p, rec in sorted(manifest_map.items()):
        body = (
            f"{rel_p} format={rec['detected_format']} status={rec['inspection_status']} "
            f"sha256={rec['raw_sha256']} git_oid={rec.get('git_index_blob_oid')} "
            f"metrics={json.dumps(rec.get('summary_metrics', {}))}"
        )
        rows.append((f"manifest:{rel_p}", "manifest", rel_p, rel_p, body))
        counts["manifest"] += 1

    # 4. Deduplicated skills catalog + full SKILL.md bodies
    catalog = load_catalog(repo_root)
    bodies = load_skill_bodies_map(repo_root)
    for srec in catalog:
        sid = srec["skill_id"]
        full_body = bodies.get(sid, "")
        combined = (
            f"{srec['name']} {srec['capability_key']} tier={srec['tier']} "
            f"repo={srec['source_repo']} commit={srec['source_commit']} "
            f"{srec['description']}\n{full_body}"
        )
        title = f"[{srec['tier']}] {srec['name']} ({srec['source_repo']})"
        rows.append((sid, "skills", title, srec["source_url"], combined))
        counts["skills"] += 1

    cur.executemany(
        "INSERT INTO docs_fts (doc_id, scope, title, path, body) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    conn.close()
    return counts


def _sanitize_fts_query(raw_query: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9_]{2,}", raw_query)
    if not tokens:
        return ""
    # Combine with AND first; caller can relax to OR if 0 hits
    return " AND ".join(f'"{t}"*' for t in tokens[:10])


def search_index(
    repo_root: Path,
    query: str,
    scope: str = "all",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Query FTS5 index across wiki, manifest, and skill bodies (with OR fallback)."""
    db_path = _fts_Index_path(repo_root)
    if not db_path.is_file():
        build_search_index(repo_root)

    tokens = re.findall(r"[A-Za-z0-9_]{2,}", query)
    if not tokens:
        return []

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    def _exec_fts(fts_expr: str) -> List[Tuple[Any, ...]]:
        if scope == "all":
            sql = """
                SELECT doc_id, scope, title, path,
                       snippet(docs_fts, 4, '[', ']', ' ... ', 24) AS snip,
                       bm25(docs_fts, 3.0, 1.0) AS score
                FROM docs_fts
                WHERE docs_fts MATCH ?
                ORDER BY CASE scope WHEN 'wiki' THEN 0 WHEN 'skills' THEN 1 WHEN 'manifest' THEN 2 ELSE 3 END,
                         score ASC
                LIMIT ?
            """
            return cur.execute(sql, (fts_expr, limit)).fetchall()
        sql = """
            SELECT doc_id, scope, title, path,
                   snippet(docs_fts, 4, '[', ']', ' ... ', 24) AS snip,
                   bm25(docs_fts, 3.0, 1.0) AS score
            FROM docs_fts
            WHERE docs_fts MATCH ? AND scope = ?
            ORDER BY score ASC
            LIMIT ?
        """
        return cur.execute(sql, (fts_expr, scope, limit)).fetchall()

    and_expr = " AND ".join(f'"{t}"*' for t in tokens[:10])
    hits = _exec_fts(and_expr)
    if not hits and len(tokens) > 1:
        or_expr = " OR ".join(f'"{t}"*' for t in tokens[:10])
        hits = _exec_fts(or_expr)

    conn.close()
    return [
        {
            "doc_id": r[0],
            "scope": r[1],
            "title": r[2],
            "path": r[3],
            "snippet": re.sub(r"\s+", " ", r[4]).strip(),
            "bm25": round(float(r[5]), 4),
        }
        for r in hits
    ]


def _build_wikilink_map(repo_root: Path) -> Dict[str, Path]:
    mapping: Dict[str, Path] = {}
    for base in (repo_root / "LLM-Wiki", repo_root / ".wiki"):
        if not base.is_dir():
            continue
        for md in sorted(base.rglob("*.md")):
            stem = md.stem.lower()
            rel_no_ext = md.relative_to(base).with_suffix("").as_posix().lower()
            if stem not in mapping:
                mapping[stem] = md
            if rel_no_ext not in mapping:
                mapping[rel_no_ext] = md
    return mapping


def run_verification_suite(repo_root: Path) -> Dict[str, Any]:
    """Run all 7 integrity, citation, traceability, skill-routing, Git, and stability checks."""
    results: Dict[str, Any] = {"checks": {}, "passed": 0, "failed": 0}

    def _record(name: str, ok: bool, details: Dict[str, Any]) -> None:
        results["checks"][name] = {"status": "PASS" if ok else "FAIL", **details}
        if ok:
            results["passed"] += 1
        else:
            results["failed"] += 1

    # 1. Manifest Integrity & Digest Separation
    manifest_path = repo_root / "LLM-Wiki" / "manifest" / "manifest.jsonl"
    manifest_map = load_manifest_map(manifest_path)
    mismatched_hashes: List[str] = []
    missing_files: List[str] = []
    self_leakage = [p for p in SELF_EXCLUDED_REL_FILES if p in manifest_map] or [
        p for p in manifest_map if p.startswith("LLM-Wiki/.cache/")
    ]
    representative_samples: List[Dict[str, Any]] = []
    rep_targets = [
        "_posts/PostAttachedFiles/Example_qPCR.xlsx",
        "_posts/PostAttachedFiles/AM_Calibrator_2DDCt.prism",
        "GSE284271/01.scRNAseq10xVisiumHD.html",
        "GSE284271/00.NIH_10xVisiumHD.html",
        "_posts/PostAttachedFiles/IGV_BAM_Screenshot.png",
        "img/gallery/~$Frame_Article.pptx",
        "scripts/fetch_bsgou_members.py",
    ]
    for rel_p, rec in manifest_map.items():
        abs_p = repo_root / rel_p
        if not abs_p.is_file():
            missing_files.append(rel_p)
            continue
        data = abs_p.read_bytes()
        disk_sha256 = compute_raw_sha256(data)
        disk_blob_oid = compute_git_blob_oid(data)
        if disk_sha256 != rec.get("raw_sha256") or disk_blob_oid != rec.get(
            "working_git_blob_oid"
        ):
            mismatched_hashes.append(rel_p)
        if rel_p in rep_targets:
            representative_samples.append(
                {
                    "rel_path": rel_p,
                    "raw_sha256": disk_sha256,
                    "working_git_blob_oid": disk_blob_oid,
                    "detected_format": rec["detected_format"],
                    "inspection_status": rec["inspection_status"],
                }
            )

    _record(
        "manifest_hashes_and_self_exclusion",
        bool(manifest_map)
        and not mismatched_hashes
        and not missing_files
        and not self_leakage,
        {
            "verified_file_count": len(manifest_map),
            "mismatched_hashes": mismatched_hashes,
            "missing_files": missing_files,
            "self_inclusion_leakage": self_leakage,
            "representative_verified": representative_samples,
        },
    )

    # 2. Source Links, [[wikilinks]], and YAML `source_refs` Citations
    wiki_root = repo_root / "LLM-Wiki"
    wikilink_map = _build_wikilink_map(repo_root)
    broken_source_refs: List[str] = []
    broken_md_links: List[str] = []
    broken_wikilinks: List[str] = []
    checked_source_refs = 0
    checked_md_links = 0
    checked_wikilinks = 0

    for md_file in sorted(wiki_root.rglob("*.md")):
        md_rel = md_file.relative_to(repo_root).as_posix()
        text = md_file.read_text(encoding="utf-8", errors="replace")
        # Strip fenced code blocks before checking links/wikilinks
        text_no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text_no_inline_code = re.sub(r"`[^`\n]+`", "", text_no_code)

        # Check frontmatter source_refs
        lines = text.splitlines()
        if lines and lines[0].strip() == "---":
            in_refs = False
            for ln in lines[1:120]:
                if ln.strip() == "---":
                    break
                if re.match(r"^source_refs\s*:", ln):
                    in_refs = True
                    continue
                if in_refs:
                    m_ref = re.match(r"^\s*-\s*['\"]?([^'\"\n]+?)['\"]?\s*$", ln)
                    if m_ref:
                        raw_ref = m_ref.group(1).strip()
                        checked_source_refs += 1
                        path_part = raw_ref.split("#", 1)[0].split(":", 1)[0]
                        target_p = repo_root / path_part
                        if not target_p.exists():
                            broken_source_refs.append(f"{md_rel} -> {raw_ref}")
                        else:
                            m_line = re.search(r"(?:#L|:)(\d+)(?:-L?(\d+))?$", raw_ref)
                            if m_line and target_p.is_file():
                                max_ln = len(
                                    target_p.read_text(
                                        encoding="utf-8", errors="replace"
                                    ).splitlines()
                                )
                                end_ln = int(m_line.group(2) or m_line.group(1))
                                if end_ln > max_ln:
                                    broken_source_refs.append(
                                        f"{md_rel} -> {raw_ref} (exceeds {max_ln} lines)"
                                    )
                    elif re.match(r"^[A-Za-z0-9_-]+\s*:", ln):
                        in_refs = False

        # Check Markdown relative links
        for m_lnk in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text_no_inline_code):
            href = m_lnk.group(1).strip()
            if href.startswith(("http://", "https://", "mailto:", "#", "sidecar://", "conversation://")):
                continue
            checked_md_links += 1
            if href.startswith("file://"):
                clean_p = href[len("file://") :].split("#", 1)[0]
                if not Path(clean_p).exists():
                    broken_md_links.append(f"{md_rel} -> {href}")
            else:
                clean_rel = href.split("#", 1)[0]
                if not clean_rel:
                    continue
                resolved = (md_file.parent / clean_rel).resolve()
                if not resolved.exists():
                    broken_md_links.append(f"{md_rel} -> {href}")

        # Check [[wikilinks]]
        for m_wl in re.finditer(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", text_no_inline_code):
            target_key = m_wl.group(1).strip().lower()
            if target_key in ("page", "wikilink", "entity"):
                continue
            checked_wikilinks += 1
            if target_key not in wikilink_map:
                broken_wikilinks.append(f"{md_rel} -> [[{m_wl.group(1)}]]")

    _record(
        "source_links_and_citations",
        not broken_source_refs and not broken_md_links and not broken_wikilinks,
        {
            "checked_source_refs": checked_source_refs,
            "checked_markdown_links": checked_md_links,
            "checked_wikilinks": checked_wikilinks,
            "broken_source_refs": broken_source_refs,
            "broken_markdown_links": broken_md_links,
            "broken_wikilinks": broken_wikilinks,
        },
    )

    # 3. Scientific Result Traceability (experiment -> dataset -> analysis -> figure -> result)
    results_dir = wiki_root / "results"
    result_pages = sorted(results_dir.glob("*.md")) if results_dir.is_dir() else []
    incomplete_chains: List[str] = []
    verified_chains: List[str] = []
    for rp in result_pages:
        txt = rp.read_text(encoding="utf-8", errors="replace")
        has_exp = bool(re.search(r"exp-[a-z0-9-]+", txt))
        has_ds = bool(re.search(r"ds-[a-z0-9-]+", txt))
        has_ana = bool(re.search(r"ana-[a-z0-9-]+", txt))
        has_fig = bool(re.search(r"fig-[a-z0-9-]+", txt))
        if has_exp and has_ds and has_ana and has_fig:
            verified_chains.append(rp.name)
        else:
            incomplete_chains.append(rp.name)

    _record(
        "result_traceability_chains",
        len(result_pages) >= 3 and not incomplete_chains,
        {
            "verified_result_chains": verified_chains,
            "incomplete_chains": incomplete_chains,
        },
    )

    # 4. Skill-Body Retrieval & Digest Match Across All Tiers
    catalog = load_catalog(repo_root)
    tier_probes: List[Optional[Dict[str, Any]]] = [
        next((r for r in catalog if r["tier"] == "global" and "chembl" in r["skill_id"]), None),
        next((r for r in catalog if r["tier"] == "project"), None),
        next((r for r in catalog if r["source_repo"] == "Yuan1z0825/nature-skills"), None),
        next((r for r in catalog if r["source_repo"].startswith("K-Dense-AI/")), None),
    ]
    probe_outcomes: List[Dict[str, Any]] = []
    all_probes_ok = len(catalog) > 100
    for probe in tier_probes:
        if probe is None:
            all_probes_ok = False
            probe_outcomes.append({"error": "missing_tier_probe"})
            continue
        res = get_skill_body(repo_root, probe["skill_id"])
        body_txt = (res or {}).get("body") or ""
        sha_ok = (
            hashlib.sha256(body_txt.encode("utf-8")).hexdigest()
            == probe["body_sha256"]
        )
        all_probes_ok = all_probes_ok and bool(body_txt) and sha_ok
        probe_outcomes.append(
            {
                "skill_id": probe["skill_id"],
                "tier": probe["tier"],
                "source_repo": probe["source_repo"],
                "body_bytes": len(body_txt.encode("utf-8")),
                "sha256_verified": sha_ok,
            }
        )

    _record(
        "skill_body_retrieval",
        all_probes_ok,
        {
            "catalog_size": len(catalog),
            "omissions_size": len(load_omissions(repo_root)),
            "probes": probe_outcomes,
        },
    )

    # 5. Skill Router Priority Ordering (global -> project -> external)
    r_global = route_task_to_skills(repo_root, "Query ChEMBL bioactivity IC50 for kinase target")
    r_proj = route_task_to_skills(
        repo_root,
        "Decode BGI Stereo-seq barcodeToPos.h5 CID and bin Visium HD StarDist nuclei in GSE284271",
    )
    r_ext = route_task_to_skills(
        repo_root,
        "Draft a point-by-point Nature journal peer-review rebuttal letter and revision plan",
    )
    ok_global = bool(r_global["selected"]) and r_global["selected"][0]["routing_bucket"] == "global"
    ok_proj = any(s["routing_bucket"] == "project" for s in r_proj["selected"][:2])
    ok_ext = any(s["routing_bucket"] == "external" for s in r_ext["selected"])

    _record(
        "skill_router_precedence",
        ok_global and ok_proj and ok_ext,
        {
            "chembl_top_hit": r_global["selected"][0]["skill_id"] if r_global["selected"] else None,
            "chembl_suppressed_duplicates": len(r_global["suppressed_redundant_external"]),
            "spatial_project_hits": [s["skill_id"] for s in r_proj["selected"][:3]],
            "nature_rebuttal_hits": [s["skill_id"] for s in r_ext["selected"][:3]],
        },
    )

    # 6. Git & Worktree Record Accuracy
    git_json_path = repo_root / "LLM-Wiki" / "manifest" / "git_state.json"
    live_git = inspect_git_and_worktrees(repo_root, write_json=False)
    recorded_git = (
        json.loads(git_json_path.read_text(encoding="utf-8"))
        if git_json_path.is_file()
        else {}
    )
    import subprocess as _sp
    _p_rc, _p_out = _sp.run(
        ["git", "rev-parse", "HEAD~1"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    ).returncode, ""
    _parent_proc = _sp.run(
        ["git", "rev-parse", "HEAD~1"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    valid_heads = {live_git.get("head_commit")}
    if _parent_proc.returncode == 0:
        valid_heads.add(_parent_proc.stdout.strip())
    git_ok = (
        recorded_git.get("head_commit") in valid_heads
        and recorded_git.get("current_branch") == live_git.get("current_branch")
        and recorded_git.get("worktree_count") == live_git.get("worktree_count")
    )
    _record(
        "git_and_worktree_records",
        git_ok,
        {
            "current_branch": live_git.get("current_branch"),
            "head_commit": live_git.get("head_commit"),
            "base_commit": live_git.get("base_commit"),
            "worktree_count": live_git.get("worktree_count"),
            "nested_repositories": live_git.get("nested_repositories"),
            "is_dirty": live_git.get("is_dirty"),
        },
    )

    # 7. Rerun Stability (idempotent read-only incremental refresh check)
    before_sha = (
        compute_raw_sha256(manifest_path.read_bytes()) if manifest_path.is_file() else ""
    )
    refresh_out = scan_or_refresh_manifest(repo_root, incremental=True, dry_run=True)
    after_sha = refresh_out["manifest_jsonl_sha256"]
    rerun_ok = (
        bool(before_sha)
        and before_sha == after_sha
        and refresh_out["modified_count"] == 0
        and refresh_out["deleted_count"] == 0
        and len(refresh_out["added"]) == 0
    )
    _record(
        "rerun_stability",
        rerun_ok,
        {
            "manifest_sha256_before": before_sha,
            "manifest_sha256_after": after_sha,
            "zero_diff": before_sha == after_sha,
        },
    )

    results["overall_status"] = "PASS" if results["failed"] == 0 else "FAIL"
    return results
