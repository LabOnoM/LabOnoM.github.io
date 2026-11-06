#!/usr/bin/env python3
"""Unified CLI for LabOnoM LLM-Wiki persistent project memory, skill router, and integrity verifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running directly as `python3 LLM-Wiki/scripts/wiki_cli.py ...`
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "LLM-Wiki") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "LLM-Wiki"))

from scripts.manifest_ops import inspect_git_and_worktrees, scan_or_refresh_manifest  # noqa: E402
from scripts.search_verify import (  # noqa: E402
    build_search_index,
    run_verification_suite,
    search_index,
)
from scripts.skills_ops import (  # noqa: E402
    build_skills_catalog,
    fetch_external_skill_cache,
    get_skill_body,
    route_task_to_skills,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="wiki_cli.py",
        description=(
            "LabOnoM LLM-Wiki CLI: format-aware file manifest, incremental refresh, "
            "FTS5 search, global->project->external skill router, and traceability verifier."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="Full format-aware workspace scan and SHA-256 manifest build")
    p_scan.add_argument("--dry-run", action="store_true", help="Compute without writing manifest files")

    p_ref = sub.add_parser(
        "refresh",
        help="Incremental manifest refresh: detect added/modified/deleted files, retain history, invalidate stale wiki pages",
    )
    p_ref.add_argument("--dry-run", action="store_true", help="Report changes without modifying manifest files")
    p_ref.add_argument("--reindex", action="store_true", help="Rebuild FTS5 search index after refresh")

    p_git = sub.add_parser("git-state", help="Inspect repository, branches, worktrees, nested repos, and dirty state")
    p_git.add_argument("--dry-run", action="store_true", help="Print state without writing git_state.json")

    p_bs = sub.add_parser("build-skills", help="Inventory global, project, nature-skills, and K-Dense-AI skills")
    p_bs.add_argument(
        "--scratch-repos",
        type=Path,
        default=None,
        help="Directory containing downloaded external repo .tar.gz archives",
    )

    sub.add_parser(
        "fetch-skill-cache",
        help="Populate LLM-Wiki/.cache/skill_bodies_v1.jsonl.gz from pinned GitHub commit tarballs",
    )

    p_index = sub.add_parser("index", help="Build disposable SQLite FTS5 search index in LLM-Wiki/.cache/")
    p_index.set_defaults(_noop=True)

    p_search = sub.add_parser("search", help="Full-text BM25 search across wiki pages, manifest, and skill bodies")
    p_search.add_argument("query", help="Search query string")
    p_search.add_argument(
        "--scope",
        choices=["all", "wiki", "skills", "manifest", "legacy_wiki"],
        default="all",
        help="Restrict search scope",
    )
    p_search.add_argument("--limit", type=int, default=10, help="Max results to return")

    p_ssearch = sub.add_parser("skill-search", help="Search deduplicated skills catalog and cached SKILL.md bodies")
    p_ssearch.add_argument("query", help="Skill search query")
    p_ssearch.add_argument("--limit", type=int, default=10)

    p_sbody = sub.add_parser("skill-body", help="Retrieve exact SKILL.md instructions for a selected skill_id")
    p_sbody.add_argument("skill_id", help="Exact or partial skill_id / skill name")
    p_sbody.add_argument("--max-lines", type=int, default=0, help="Optional line cap (0 = full body)")

    p_route = sub.add_parser("route", help="Route task across global -> project-local -> complementary external skills")
    p_route.add_argument("task", help="Natural-language task description")
    p_route.add_argument("--top-k", type=int, default=8)

    sub.add_parser("verify", help="Run full SHA-256, link, traceability, skill-body, routing, Git, and rerun checks")

    args = parser.parse_args(argv)

    if args.cmd == "scan":
        out = scan_or_refresh_manifest(REPO_ROOT, incremental=False, dry_run=args.dry_run)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "refresh":
        out = scan_or_refresh_manifest(REPO_ROOT, incremental=True, dry_run=args.dry_run)
        if args.reindex and not args.dry_run:
            out["fts_index_counts"] = build_search_index(REPO_ROOT)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "git-state":
        out = inspect_git_and_worktrees(REPO_ROOT, write_json=not args.dry_run)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "build-skills":
        out = build_skills_catalog(REPO_ROOT, scratch_repos_dir=args.scratch_repos)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "fetch-skill-cache":
        out = fetch_external_skill_cache(REPO_ROOT)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "index":
        out = build_search_index(REPO_ROOT)
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    if args.cmd == "search":
        hits = search_index(REPO_ROOT, args.query, scope=args.scope, limit=args.limit)
        print(json.dumps({"query": args.query, "scope": args.scope, "count": len(hits), "results": hits}, indent=2))
        return 0

    if args.cmd == "skill-search":
        hits = search_index(REPO_ROOT, args.query, scope="skills", limit=args.limit)
        print(json.dumps({"query": args.query, "count": len(hits), "results": hits}, indent=2))
        return 0

    if args.cmd == "skill-body":
        res = get_skill_body(REPO_ROOT, args.skill_id)
        if res is None:
            print(json.dumps({"error": f"No skill matched '{args.skill_id}'"}), file=sys.stderr)
            return 1
        meta = res["metadata"]
        body = res["body"] or ""
        if args.max_lines and args.max_lines > 0:
            body = "\n".join(body.splitlines()[: args.max_lines])
        print(f"# Skill Metadata: {meta['skill_id']}")
        print(json.dumps(meta, indent=2, sort_keys=True))
        print("\n# SKILL.md Body\n")
        print(body)
        return 0

    if args.cmd == "route":
        out = route_task_to_skills(REPO_ROOT, args.task, top_k=args.top_k)
        print(json.dumps(out, indent=2))
        return 0

    if args.cmd == "verify":
        out = run_verification_suite(REPO_ROOT)
        print(json.dumps(out, indent=2))
        return 0 if out["overall_status"] == "PASS" else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
