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

## Round 2 — mixed-signal edge cases, 12/12 correct

Same method, same day. The four phrasings most likely to split:

| Query | Expected | Result |
|---|---|---|
| "audit the internal linking on this Sitebulb crawl and tell me what to fix" | internal-linking | internal-linking ×3 ✅ |
| "here's a Sitebulb export — fix the orphan pages" | internal-linking | internal-linking ×3 ✅ |
| "here are my GSC exports, improve our internal links" | internal-linking | internal-linking ×3 ✅ |
| "build me a work plan from this Sitebulb export" | sitebulb-sow-builder | sitebulb-sow-builder ×3 ✅ |

**Combined: 21/21 across both rounds, all unanimous, zero
cross-contamination.** In the orphan-pages runs, subagents explicitly
reasoned through the boundary ("sitebulb-sow-builder targets dev-hint
tickets, this is orphan fixing") — the carve-out language is doing real
disambiguation work. The GSC collision (query 3) resolved on intent verbs:
gsc-sow-builder scopes itself to recovery SOWs, and no recovery/work-plan
language was present.

## Status and residual risk

Routing is **settled** at this sample size. Caveats for the record:

- 3 unanimous runs per query rules out consistent misrouting, not rare
  flips near a decision boundary; nothing at n=3 suggests one exists.
- The untested risky shape: a query combining GSC exports + recovery/SOW
  language + internal-link language in one breath (e.g. "build a recovery
  work plan from these GSC exports, including internal linking"). By
  design that should go to gsc-sow-builder with internal-linking as a
  follow-on. Test only if this phrasing shows up in real use.
- Re-run this eval whenever either skill's description changes — fix
  descriptions in this repo first, re-zip, re-upload; git stays canonical.
