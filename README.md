# claude-skills

Canonical source and tooling for MeasurableSEO's custom claude.ai skills —
the 16 skills behind the diagnostic → proposal → IO → report pipeline
(diagnostic-builder, proposal-builder, io-generator, csuite-report, the SOW
builders, geo-master-blueprint, legal-page-rewrite, and the rest).

## Layout

| Path | What it is |
|---|---|
| `tools/skills-manager/` | CLI for listing, exporting, and updating skills through the Anthropic Skills API — see its [README](tools/skills-manager/README.md) |
| `audits/` | Dated skill-audit reports (trigger conflicts, description fixes) |
| `skills/` | Exported skill sources — one directory per skill, produced by `skills_manager.py pull` |

## Workflows

**Apply the current audit's description fixes** (one command, all 9 skills):

```bash
cd tools/skills-manager
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...
python skills_manager.py apply-audit --dry-run   # preview
python skills_manager.py apply-audit             # create new versions
```

**Export all skill sources into `skills/`** so future audits can cover the
full SKILL.md bodies and reference files, not just descriptions:

```bash
cd tools/skills-manager
python skills_manager.py list
# for each skill id from the listing:
python skills_manager.py pull SKILL_ID --out ../../skills/SKILL_NAME
```

Commit the result. From then on, edit skills here, version them in git, and
push updates with `skills_manager.py update-description` (descriptions) or a
new `versions.create` upload (full bundles).

## Why this repo exists

The 2026-07-16 audit ([audits/2026-07-16-skills-audit.md](audits/2026-07-16-skills-audit.md))
found 9 trigger-routing issues across the skill suite and recommended keeping
skill sources in a dedicated repo so they can be audited, diffed, and
versioned alongside the deliverable templates they generate. This is that repo.
