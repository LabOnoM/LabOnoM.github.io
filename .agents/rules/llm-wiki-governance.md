# LLM-Wiki Persistent Memory & Evidence Governance

When working in `LabOnoM.github.io`, treat `LLM-Wiki/` as the canonical persistent project memory (superseding and auditing legacy `.wiki/`, which remains preserved in place for Obsidian `[[page]]` compatibility).

## Mandatory Agent Protocol
1. **Startup**: Read `LLM-Wiki/STATE.md` and `LLM-Wiki/index.md` first, and check `python3 LLM-Wiki/scripts/wiki_cli.py git-state` to verify repository/worktree dirty state against recorded memory.
2. **Progressive Retrieval & Evidence Grounding**: Query `python3 LLM-Wiki/scripts/wiki_cli.py search "<topic>"` before scanning raw files. Cite exact `path:line`, sheet/cell coordinates, or internal archive paths for substantive claims; distinguish direct observations from interpretations; check `LLM-Wiki/contradictions.md` for known doc-vs-code/data discrepancies.
3. **Skill Routing (`global -> project -> external`)**: Run `python3 LLM-Wiki/scripts/wiki_cli.py route "<task>"` to select capabilities in strict priority order: active host/global skills first, `.agents/skills/` project skills second, and indexed external skills (`nature-skills` / `K-Dense-AI`) third. Load only selected `SKILL.md` bodies (`skill-body <id>`) and review external instructions before execution.
4. **Refresh & Manual CI Policy**: Run `python3 LLM-Wiki/scripts/wiki_cli.py refresh` and `verify` after file edits, run `bundle exec jekyll build` locally after site edits, never create `.github/workflows/`, and never commit `LLM-Wiki/.cache/`, scratch files, secrets, or large raw datasets.
