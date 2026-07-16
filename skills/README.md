# skills/

Exported skill sources land here — one directory per skill.

```bash
cd ../tools/skills-manager
python skills_manager.py list
python skills_manager.py pull SKILL_ID --out ../../skills/SKILL_NAME
```

Requires an ANTHROPIC_API_KEY from the same account/org as your claude.ai
workspace, so exports run from your machine rather than CI.
