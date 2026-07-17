# gbp-optimization routing eval — July 17, 2026

Triggering eval after uploading the new `gbp-optimization` skill (source:
[`skills/gbp-optimization/`](../skills/gbp-optimization/), commit 37a48c2).
Same head-to-head method as the
[internal-linking eval](2026-07-17-internal-linking-routing-eval.md):
fresh instances seeing the full live skill list, 3 runs per query. The
"audit this page" case used a real law-firm practice-area URL so the
legal context was present without naming any skill.

## Results — 12/12 correct

| Query | Expected | Result |
|---|---|---|
| "run a local SEO audit for dandalaw.com" | gbp-optimization | gbp-optimization ×3 ✅ |
| "audit this page" (law-firm practice-area URL) | legal-page-rewrite | legal-page-rewrite ×3 ✅ |
| "why isn't my client showing in the map pack" | gbp-optimization | gbp-optimization ×3 ✅ |
| "is [prospect] getting cited by AI" | diagnostic-builder | diagnostic-builder ×3 ✅ |

**Running total across all three sweeps: 33/33, all unanimous, zero
cross-contamination.**

Both guardrail cases held. The bare verb "audit" with a law-firm page
went to legal-page-rewrite every time (subagents cited its Stage 3
critique), so the vertical context overrides the generic verb.
The AI-citation query stayed with diagnostic-builder on its exact-phrase
trigger; no local/map signal was present to pull gbp-optimization in.

## Untested middle — and why it's a different kind of test

Queries pairing local intent with a competing signal in one sentence:

1. "audit the local SEO and the GBP landing page copy for this law firm"
   (gbp-optimization × legal-page-rewrite)
2. "run a local SEO audit and tell me if they're cited by AI"
   (gbp-optimization × diagnostic-builder)

These are genuinely **dual-intent requests, not routing ambiguities** —
the correct behavior is both deliverables getting covered (primary skill
loads, second intent handled or explicitly handed off), not one skill
"winning". A future eval of these should score coverage of both intents,
not just which skill loads first. Deferred until the phrasing shows up
in real use.

## Caveat (unchanged)

n=3 unanimous per query shows consistent routing, not immunity to rare
flips. Re-run when either description changes; descriptions change in
this repo first, then re-zip and re-upload.
