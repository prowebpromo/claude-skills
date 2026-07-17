# internal-linking routing eval — July 17, 2026

First triggering eval after uploading the new `internal-linking` skill
(source: [`skills/internal-linking/`](../skills/internal-linking/), commit
b9afe11) to the claude.ai workspace where it competes live with
sitebulb-sow-builder.

**Method:** head-to-head routing in the live skill environment — each query
sent to fresh Claude instances that see the full skill list, 3 runs per
query. This was chosen over skill-creator's `run_eval.py` trigger-rate
loop, which injects one skill in isolation and structurally cannot detect
which of two competing skills wins a query.

## Results — 9/9 correct

| Query | Expected | Result |
|---|---|---|
| "find internal link opportunities from this Sitebulb export" | internal-linking | internal-linking ×3 ✅ |
| "build an internal link plan for dandalaw.com" | internal-linking | internal-linking ×3 ✅ |
| "turn these Sitebulb hints into a dev SOW" | sitebulb-sow-builder | sitebulb-sow-builder ×3 ✅ |

The Sitebulb-input query is the one that matters: both skills claim
Sitebulb exports as input. Routing was driven by the internal-link intent
language, plus sitebulb-sow-builder's explicit internal-link carve-out.
No cross-contamination in either direction.

## Not yet tested (rerun candidates)

Mixed-signal phrasings most likely to split, worth a follow-up eval:

1. "audit the internal linking on this Sitebulb crawl and tell me what to
   fix" — audit + internal-link + Sitebulb signals combined
2. "here's a Sitebulb export — fix the orphan pages" — orphans belong to
   internal-linking, but "fix" language pulls toward the SOW builder
3. "here are my GSC exports, improve our internal links" — must route to
   internal-linking, not gsc-sow-builder (GSC input overlap)
4. "build me a work plan from this Sitebulb export" — must still route to
   sitebulb-sow-builder (no internal-link intent)

If any of these split, fix the description in
`skills/internal-linking/SKILL.md` here first, re-zip, re-upload — git
stays canonical.
