"""Workspace manifest scanning, incremental refresh, summary invalidation, and Git/worktree auditing."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .inspectors import inspect_workspace_file

# Directories excluded from workspace file ingestion (VCS internals, build outputs, disposable caches)
EXCLUDED_DIR_NAMES = frozenset(
    {
        ".git",
        "_site",
        ".jekyll-cache",
        ".sass-cache",
        "vendor",
        "node_modules",
        ".venv",
        "__pycache__",
        ".regent",
    }
)

# Relative directories/files excluded to prevent recursive self-hashing of generated manifests and caches
EXCLUDED_REL_PREFIXES = (
    "LLM-Wiki/.cache/",
    "LLM-Wiki/.cache",
)

SELF_EXCLUDED_REL_FILES = frozenset(
    {
        "LLM-Wiki/manifest/manifest.jsonl",
        "LLM-Wiki/manifest/manifest.summary.json",
        "LLM-Wiki/manifest/manifest_history.jsonl",
        "LLM-Wiki/manifest/stale_summaries.json",
        "LLM-Wiki/manifest/git_state.json",
    }
)

ALL_STATUS_KEYS = (
    "inspected_full",
    "inspected_structured",
    "inspected_visual_and_metadata",
    "inspected_anomalous",
    "inspected_metadata_only",
    "unhashed",
    "partial",
    "sampled",
    "unsupported",
    "excluded",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _run_git(repo_root: Path, args: List[str]) -> Tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout


def get_git_index_oids(repo_root: Path) -> Dict[str, str]:
    """Return mapping of rel_path -> 40-hex Git index blob SHA-1 OID."""
    rc, out = _run_git(repo_root, ["ls-files", "-s", "-z"])
    if rc != 0:
        return {}
    mapping: Dict[str, str] = {}
    for entry in out.split("\x00"):
        if not entry:
            continue
        # Format: "<mode> <oid> <stage>\t<path>"
        tab_idx = entry.find("\t")
        if tab_idx == -1:
            continue
        meta = entry[:tab_idx].split()
        path = entry[tab_idx + 1 :]
        if len(meta) >= 2:
            mapping[path] = meta[1]
    return mapping


def inspect_git_and_worktrees(repo_root: Path, write_json: bool = True) -> Dict[str, Any]:
    """Detect repository identity, nested .git dirs, worktrees, branches, base commit, and dirty state."""
    rc_head, head_out = _run_git(repo_root, ["rev-parse", "HEAD"])
    head_commit = head_out.strip() if rc_head == 0 else None

    rc_br, br_out = _run_git(repo_root, ["symbolic-ref", "--short", "HEAD"])
    current_branch = br_out.strip() if rc_br == 0 else "DETACHED"

    rc_main, main_out = _run_git(repo_root, ["rev-parse", "main"])
    main_commit = main_out.strip() if rc_main == 0 else None

    rc_mb, mb_out = _run_git(repo_root, ["merge-base", "HEAD", "main"])
    base_commit = mb_out.strip() if rc_mb == 0 else main_commit

    rc_rem, rem_out = _run_git(repo_root, ["remote", "-v"])
    remotes: Dict[str, str] = {}
    if rc_rem == 0:
        for ln in rem_out.splitlines():
            parts = ln.split()
            if len(parts) >= 2 and parts[0] not in remotes:
                remotes[parts[0]] = parts[1]

    rc_branches, branches_out = _run_git(
        repo_root,
        ["for-each-ref", "--format=%(refname:short)|%(objectname)", "refs/heads", "refs/remotes"],
    )
    refs: List[Dict[str, str]] = []
    if rc_branches == 0:
        for ln in branches_out.splitlines():
            if "|" in ln:
                rname, roid = ln.split("|", 1)
                refs.append({"ref": rname, "commit": roid})

    # Worktrees
    rc_wt, wt_out = _run_git(repo_root, ["worktree", "list", "--porcelain"])
    worktrees: List[Dict[str, str]] = []
    if rc_wt == 0:
        cur: Dict[str, str] = {}
        for ln in wt_out.splitlines() + [""]:
            if not ln.strip():
                if cur:
                    worktrees.append(cur)
                    cur = {}
                continue
            if " " in ln:
                k, v = ln.split(" ", 1)
                cur[k] = v
            else:
                cur[ln] = "true"

    # Nested .git check (excluding root .git)
    nested_git: List[str] = []
    for root_dir, dirs, files in os.walk(repo_root):
        rel_root = Path(root_dir).relative_to(repo_root)
        if rel_root != Path(".") and ".git" in (set(dirs) | set(files)):
            nested_git.append(str(rel_root / ".git"))
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIR_NAMES]

    # Porcelain dirty state
    rc_st, st_out = _run_git(repo_root, ["status", "--porcelain=v1", "-uall"])
    staged: List[str] = []
    unstaged: List[str] = []
    untracked: List[str] = []
    if rc_st == 0:
        for ln in st_out.splitlines():
            if len(ln) < 4:
                continue
            xy = ln[:2]
            p = ln[3:]
            if xy == "??":
                untracked.append(p)
            else:
                if xy[0] != " ":
                    staged.append(p)
                if xy[1] != " ":
                    unstaged.append(p)

    # Check isolated worktree findings staging directory
    wt_staging_dir = repo_root / "LLM-Wiki" / "worktrees"
    pending_worktree_notes: List[str] = []
    if wt_staging_dir.is_dir():
        for p in sorted(wt_staging_dir.rglob("*.md")):
            if p.name.lower() != "readme.md":
                pending_worktree_notes.append(str(p.relative_to(repo_root)))

    state = {
        "repository_root": str(repo_root),
        "current_branch": current_branch,
        "head_commit": head_commit,
        "base_branch": "main",
        "base_commit": base_commit,
        "remotes": remotes,
        "refs": refs,
        "worktree_count": len(worktrees),
        "worktrees": worktrees,
        "nested_repositories": nested_git,
        "is_dirty": bool(staged or unstaged or untracked),
        "staged_count": len(staged),
        "unstaged_count": len(unstaged),
        "untracked_count": len(untracked),
        "staged_paths": staged[:50],
        "unstaged_paths": unstaged[:50],
        "untracked_paths": untracked[:50],
        "pending_branch_integration": current_branch != "main",
        "pending_worktree_staging_files": pending_worktree_notes,
        "uncommitted_evidence_warning": (
            "A Git commit SHA identifies only committed tree snapshots; dirty or untracked "
            "files MUST be identified by their raw_sha256 in LLM-Wiki/manifest/manifest.jsonl."
        ),
        "backup_arrangements": "unknown (local Git and SHA-256 hashes do not back up untracked external raw data such as 240726_VisiumHD/*.tif/*.h5 or Stereo-seq *.barcodeToPos.h5/*.fq.gz)",
    }

    if write_json:
        out_path = repo_root / "LLM-Wiki" / "manifest" / "git_state.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return state


def enumerate_workspace(repo_root: Path) -> Tuple[List[Path], List[Dict[str, str]]]:
    """Walk workspace returning sorted in-scope files and explicit excluded records."""
    included: List[Path] = []
    excluded: List[Dict[str, str]] = []

    for root_dir, dirs, files in os.walk(repo_root, followlinks=False):
        root_path = Path(root_dir)
        rel_dir = root_path.relative_to(repo_root)
        rel_dir_str = "" if rel_dir == Path(".") else rel_dir.as_posix()

        kept_dirs: List[str] = []
        for d in sorted(dirs):
            d_path = root_path / d
            d_rel = f"{rel_dir_str}/{d}".lstrip("/")
            if d_path.is_symlink():
                excluded.append(
                    {
                        "rel_path": d_rel,
                        "inspection_status": "excluded",
                        "reason": f"directory_symlink_to_{os.readlink(d_path)}",
                    }
                )
                continue
            if d in EXCLUDED_DIR_NAMES or any(
                d_rel == pref.rstrip("/") or d_rel.startswith(pref)
                for pref in EXCLUDED_REL_PREFIXES
            ):
                excluded.append(
                    {
                        "rel_path": d_rel + "/",
                        "inspection_status": "excluded",
                        "reason": "vcs_build_or_disposable_cache_dir",
                    }
                )
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs

        for fname in sorted(files):
            f_path = root_path / fname
            f_rel = f"{rel_dir_str}/{fname}".lstrip("/")
            if fname == ".DS_Store":
                excluded.append(
                    {
                        "rel_path": f_rel,
                        "inspection_status": "excluded",
                        "reason": "macos_finder_metadata",
                    }
                )
                continue
            if f_path.is_symlink():
                excluded.append(
                    {
                        "rel_path": f_rel,
                        "inspection_status": "excluded",
                        "reason": f"symlink_to_{os.readlink(f_path)}",
                    }
                )
                continue
            if f_rel in SELF_EXCLUDED_REL_FILES or any(
                f_rel.startswith(pref) for pref in EXCLUDED_REL_PREFIXES
            ):
                excluded.append(
                    {
                        "rel_path": f_rel,
                        "inspection_status": "excluded",
                        "reason": "self_referential_manifest_or_cache",
                    }
                )
                continue
            included.append(f_path)

    included.sort(key=lambda p: p.relative_to(repo_root).as_posix())
    excluded.sort(key=lambda r: r["rel_path"])
    return included, excluded


def _extract_wiki_source_dependencies(repo_root: Path) -> Dict[str, Set[str]]:
    """Map source file rel_path -> set of LLM-Wiki summary rel_paths that cite it."""
    wiki_root = repo_root / "LLM-Wiki"
    dep_map: Dict[str, Set[str]] = {}
    if not wiki_root.is_dir():
        return dep_map

    for md_file in sorted(wiki_root.rglob("*.md")):
        md_rel = md_file.relative_to(repo_root).as_posix()
        text = md_file.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        # Parse YAML front matter source_refs list
        if lines and lines[0].strip() == "---":
            in_refs = False
            for ln in lines[1:120]:
                if ln.strip() == "---":
                    break
                if re.match(r"^source_refs\s*:", ln):
                    in_refs = True
                    continue
                if in_refs:
                    m_item = re.match(r"^\s*-\s*['\"]?([^'\"#:\n]+)", ln)
                    if m_item:
                        src = m_item.group(1).strip()
                        dep_map.setdefault(src, set()).add(md_rel)
                    elif re.match(r"^[A-Za-z0-9_-]+\s*:", ln):
                        in_refs = False

        # Also detect inline repo relative file references in backticks or links
        for m_inline in re.finditer(
            r"(?:_posts|GSE284271|scripts|sources|tools|img|css|js|00\.RawData|\.wiki)/[A-Za-z0-9_./~$-]+\.[A-Za-z0-9]+",
            text,
        ):
            src = m_inline.group(0)
            dep_map.setdefault(src, set()).add(md_rel)

    return dep_map


def load_manifest_map(manifest_path: Path) -> Dict[str, Dict[str, Any]]:
    records: Dict[str, Dict[str, Any]] = {}
    if not manifest_path.is_file():
        return records
    for ln in manifest_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        records[obj["rel_path"]] = obj
    return records


def build_summary_payload(
    records: List[Dict[str, Any]],
    excluded: List[Dict[str, str]],
    manifest_jsonl_sha256: str,
    git_head_commit: Optional[str],
    git_branch: str,
) -> Dict[str, Any]:
    status_counts = {k: 0 for k in ALL_STATUS_KEYS}
    format_counts: Counter[str] = Counter()
    ext_counts: Counter[str] = Counter()
    anomalies: List[Dict[str, Any]] = []
    total_bytes = 0
    git_tracked_count = 0
    git_dirty_count = 0

    for r in records:
        st = r["inspection_status"]
        status_counts[st] = status_counts.get(st, 0) + 1
        format_counts[r["detected_format"]] += 1
        ext_counts[r["ext"] or "<no_ext>"] += 1
        total_bytes += r["size_bytes"]
        if r.get("git_tracked"):
            git_tracked_count += 1
        if r.get("git_dirty_vs_index"):
            git_dirty_count += 1
        if r.get("format_mismatch") or st == "inspected_anomalous":
            anomalies.append(
                {
                    "rel_path": r["rel_path"],
                    "ext": r["ext"],
                    "detected_format": r["detected_format"],
                    "size_bytes": r["size_bytes"],
                    "raw_sha256": r["raw_sha256"],
                    "summary_metrics": r["summary_metrics"],
                }
            )

    status_counts["excluded"] = len(excluded)

    return {
        "schema_version": "1.0.0",
        "manifest_jsonl_sha256": manifest_jsonl_sha256,
        "git_branch_at_scan": git_branch,
        "git_head_commit_at_scan": git_head_commit,
        "total_in_scope_files": len(records),
        "total_in_scope_bytes": total_bytes,
        "git_tracked_files": git_tracked_count,
        "git_dirty_vs_index_files": git_dirty_count,
        "inspection_status_counts": status_counts,
        "detected_format_counts": dict(sorted(format_counts.items())),
        "extension_counts": dict(sorted(ext_counts.items())),
        "anomalous_or_mismatched_files": anomalies,
        "excluded_entries": excluded,
        "integrity_epistemology_note": (
            "Full-file raw_sha256 hashes verify byte-level identity on disk; git_index_blob_oid "
            "(SHA-1) tracks Git staging blobs; git_head_commit_at_scan tracks committed history "
            "only. Indexing and hashing never equate to scientific validation or understanding."
        ),
    }


def scan_or_refresh_manifest(
    repo_root: Path,
    incremental: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Scan workspace, optionally computing incremental diff, history retention, and invalidation."""
    manifest_dir = repo_root / "LLM-Wiki" / "manifest"
    manifest_path = manifest_dir / "manifest.jsonl"
    summary_path = manifest_dir / "manifest.summary.json"
    history_path = manifest_dir / "manifest_history.jsonl"
    stale_path = manifest_dir / "stale_summaries.json"

    prev_map = load_manifest_map(manifest_path) if manifest_path.is_file() else {}
    git_oids = get_git_index_oids(repo_root)
    git_info = inspect_git_and_worktrees(repo_root, write_json=not dry_run)
    included_paths, excluded_entries = enumerate_workspace(repo_root)

    current_records: List[Dict[str, Any]] = []
    current_map: Dict[str, Dict[str, Any]] = {}
    for abs_p in included_paths:
        rel_p = abs_p.relative_to(repo_root).as_posix()
        # Fast reuse in incremental mode if size + mtime_ns + git_oid match
        prev = prev_map.get(rel_p)
        st = abs_p.stat()
        g_oid = git_oids.get(rel_p)
        if (
            incremental
            and prev is not None
            and prev.get("size_bytes") == st.st_size
            and prev.get("mtime_ns") == st.st_mtime_ns
            and prev.get("git_index_blob_oid") == g_oid
            and prev.get("raw_sha256")
        ):
            rec = prev
        else:
            rec = inspect_workspace_file(abs_p, rel_p, git_index_oid=g_oid)
        current_records.append(rec)
        current_map[rel_p] = rec

    added: List[str] = []
    modified: List[Dict[str, Any]] = []
    deleted: List[Dict[str, Any]] = []

    if prev_map:
        for rel_p, rec in current_map.items():
            if rel_p not in prev_map:
                added.append(rel_p)
            elif prev_map[rel_p].get("raw_sha256") != rec.get("raw_sha256"):
                modified.append({"old": prev_map[rel_p], "new": rec})
        for rel_p, old_rec in prev_map.items():
            if rel_p not in current_map:
                deleted.append(old_rec)

    # Compute invalidated summaries if any source file changed or disappeared
    dep_map = _extract_wiki_source_dependencies(repo_root)
    invalidated: Dict[str, List[Dict[str, Any]]] = {}
    for mod in modified:
        src = mod["old"]["rel_path"]
        for wiki_page in sorted(dep_map.get(src, set())):
            invalidated.setdefault(wiki_page, []).append(
                {
                    "reason": "source_modified",
                    "source_path": src,
                    "old_raw_sha256": mod["old"]["raw_sha256"],
                    "new_raw_sha256": mod["new"]["raw_sha256"],
                }
            )
    for old_rec in deleted:
        src = old_rec["rel_path"]
        for wiki_page in sorted(dep_map.get(src, set())):
            invalidated.setdefault(wiki_page, []).append(
                {
                    "reason": "source_deleted",
                    "source_path": src,
                    "old_raw_sha256": old_rec["raw_sha256"],
                    "new_raw_sha256": None,
                }
            )

    jsonl_text = "".join(
        json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n"
        for r in current_records
    )
    manifest_sha256 = hashlib.sha256(jsonl_text.encode("utf-8")).hexdigest()
    summary_payload = build_summary_payload(
        records=current_records,
        excluded=excluded_entries,
        manifest_jsonl_sha256=manifest_sha256,
        git_head_commit=git_info.get("head_commit"),
        git_branch=git_info.get("current_branch", "unknown"),
    )

    if not dry_run:
        manifest_dir.mkdir(parents=True, exist_ok=True)
        # Only rewrite manifest.jsonl / summary if changed or missing (idempotent!)
        prev_bytes = manifest_path.read_bytes() if manifest_path.is_file() else None
        new_bytes = jsonl_text.encode("utf-8")
        if prev_bytes != new_bytes:
            manifest_path.write_bytes(new_bytes)
        summary_bytes = (
            json.dumps(summary_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
        ).encode("utf-8")
        if not summary_path.is_file() or summary_path.read_bytes() != summary_bytes:
            summary_path.write_bytes(summary_bytes)

        # Append superseded evidence to manifest_history.jsonl
        if modified or deleted:
            ts = now_iso()
            with history_path.open("a", encoding="utf-8") as hf:
                for mod in modified:
                    hf.write(
                        json.dumps(
                            {
                                "timestamp": ts,
                                "event": "modified",
                                "rel_path": mod["old"]["rel_path"],
                                "superseded_raw_sha256": mod["old"]["raw_sha256"],
                                "superseded_size_bytes": mod["old"]["size_bytes"],
                                "superseded_mtime_utc": mod["old"]["mtime_utc"],
                                "new_raw_sha256": mod["new"]["raw_sha256"],
                                "new_size_bytes": mod["new"]["size_bytes"],
                                "git_head_commit": git_info.get("head_commit"),
                            },
                            sort_keys=True,
                        )
                        + "\n"
                    )
                for old_rec in deleted:
                    hf.write(
                        json.dumps(
                            {
                                "timestamp": ts,
                                "event": "deleted",
                                "rel_path": old_rec["rel_path"],
                                "superseded_raw_sha256": old_rec["raw_sha256"],
                                "superseded_size_bytes": old_rec["size_bytes"],
                                "superseded_mtime_utc": old_rec["mtime_utc"],
                                "new_raw_sha256": None,
                                "new_size_bytes": None,
                                "git_head_commit": git_info.get("head_commit"),
                            },
                            sort_keys=True,
                        )
                        + "\n"
                    )
        elif not history_path.is_file():
            history_path.write_text("", encoding="utf-8")

        # Update stale_summaries.json deterministically when invalidation state changes
        existing_stale: Dict[str, Any] = {}
        if stale_path.is_file():
            try:
                existing_stale = json.loads(stale_path.read_text(encoding="utf-8")).get(
                    "stale_pages", {}
                )
            except Exception:
                existing_stale = {}
        merged_stale = dict(existing_stale)
        for page, reasons in invalidated.items():
            merged_stale[page] = reasons
        # Clear stale entries whose wiki page was updated more recently or explicitly cleared
        stale_payload = {
            "schema_version": "1.0.0",
            "stale_page_count": len(merged_stale),
            "stale_pages": dict(sorted(merged_stale.items())),
        }
        stale_bytes = (json.dumps(stale_payload, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
        if not stale_path.is_file() or stale_path.read_bytes() != stale_bytes:
            stale_path.write_bytes(stale_bytes)

    return {
        "total_in_scope_files": len(current_records),
        "excluded_count": len(excluded_entries),
        "manifest_jsonl_sha256": manifest_sha256,
        "added": added,
        "modified_count": len(modified),
        "modified_paths": [m["old"]["rel_path"] for m in modified],
        "deleted_count": len(deleted),
        "deleted_paths": [d["rel_path"] for d in deleted],
        "invalidated_summaries": invalidated,
        "status_counts": summary_payload["inspection_status_counts"],
    }
