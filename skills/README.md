# skills/

Skill sources live here — one directory per skill. Two kinds:

- **Authored here** (e.g. `internal-linking/`) — written in this repo first,
  then zipped and uploaded in claude.ai → Settings → Capabilities → Skills.
- **Exported** from the Skills API via `skills_manager.py pull` (workflow
  below; currently blocked, see the root README status note).

```bash
cd ../tools/skills-manager
python skills_manager.py list
python skills_manager.py pull SKILL_ID --out ../../skills/SKILL_NAME
```

Requires an ANTHROPIC_API_KEY from the same account/org as your claude.ai
workspace, so exports run from your machine rather than CI.
