# fixes/

One plain-text file per skill: the current canonical trigger description,
ready to copy-paste. As of the [2026-07-17 description
trim](../audits/2026-07-17-description-trim.md) these are the trimmed
texts (which fold in the 2026-07-16 audit's routing fixes — the July 16
texts remain in git history). Open the file, select all, copy, and replace
the `description:` value in that skill's SKILL.md frontmatter
(claude.ai -> Settings -> Capabilities -> Skills), keeping the YAML
quoting intact. Each text is verified under the 1024-character limit.

Prefer applying programmatically:
`python tools/skills-manager/skills_manager.py apply-audit --fixes tools/skills-manager/trim_fixes.json`
