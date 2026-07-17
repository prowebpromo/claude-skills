---
name: gbp-optimization
description: Audit and optimize a Google Business Profile (GBP) and surrounding local-SEO signals — weighted profile scoring, category strategy, review velocity and response plan, NAP/citation consistency across core and vertical directories, LocalBusiness schema, and landing page alignment. Use whenever the user asks to: audit or optimize a GBP, Google Business Profile, or Google Maps listing; run a local SEO audit; check citations or NAP consistency; improve local pack / map pack presence; build a review strategy; or drops GBP screenshots, Insights exports, or a business's name/address/phone and asks what to fix. Trigger on "GBP audit for [client]", "why isn't [client] in the map pack", or "local SEO audit for [business]". Outputs a .docx optimization plan plus .xlsx citation log and task list. No paid APIs required. Do NOT use for organic recovery SOWs (gsc-sow-builder), crawl-based dev SOWs (sitebulb-sow-builder), internal link plans (internal-linking), or landing page copy (legal-page-rewrite, wp-classic-designer).
---

# gbp-optimization

Audit a business's Google Business Profile and surrounding local-SEO
signals, then produce an execution-ready optimization plan. Everything is
scored against the weighted scorecard in `reference/gbp_scorecard.md` and
every recommendation cites the evidence behind it. This skill plans and
audits local presence; it does not write landing page copy
(legal-page-rewrite, wp-classic-designer), plan internal links
(internal-linking), or build organic recovery SOWs (gsc-sow-builder).

## Inputs — files and web evidence, no paid APIs

1. **Canonical business facts (required).** Exact business name, address,
   phone, website URL, primary services, and service area. If the user
   hasn't provided them, ask — never guess or infer the canonical NAP,
   because the whole citation audit compares against it.
2. **GBP evidence (best available).** Dashboard screenshots, GBP Insights
   exports, or the public listing (fetch the Maps/knowledge panel view via
   web search for the business name + city). State plainly in the
   deliverable which parts were verified from the dashboard vs. the public
   listing vs. not visible at all — dashboard-only facts (e.g. messaging
   settings, unpublished services) cannot be audited from outside.
3. **The client's website.** Fetch the GBP-linked landing page and key
   location/service pages: LocalBusiness schema, NAP in the footer,
   title/H1 city+service alignment, embedded map, internal links.
4. **Directory listings.** Fetch/search the core and vertical directories
   from `reference/citation_sources.md` and record each listing's NAP in
   `citations.csv` for the comparison script.
5. **Optional:** GSC Queries.csv (filter for geo-modified queries),
   competitor names for the pack benchmark, prior audit for delta
   reporting.

## Workflow

### 1. Establish the canonical record

Lock the canonical NAP + categories + money services with the user before
auditing. Format rules live in `reference/citation_sources.md`.

### 2. Collect evidence

- Public GBP listing: name as displayed, primary/secondary categories,
  description, hours, photos count/recency, review count/rating, Q&A,
  posts recency, linked URL.
- Website: schema (fetch and parse JSON-LD), NAP, landing page alignment.
- Citations: one row per directory in `citations.csv` (source, name,
  address, phone, url, status, notes). Mark missing listings and
  suspected duplicates.
- Local pack benchmark: search 3–5 money queries ("[service] [city]");
  record which businesses take the pack, their categories, review counts,
  and ratings. The gap between the client and the weakest pack entrant is
  the headline finding.

### 3. Score the profile

Apply `reference/gbp_scorecard.md` — seven weighted sections totaling 100.
Report per-section scores, the total, and the band (Maintain 85+,
Optimize 65–84, Rebuild <65). Items that cannot be verified from the
available evidence score as "unverified", are excluded from the
denominator, and are listed for the client to confirm — never silently
assumed compliant.

### 4. Run the citation comparison

`python scripts/nap_compare.py citations.csv --name "..." --address "..."
--phone "..."` normalizes and diffs every listing against the canonical
record and emits a per-field mismatch report with severity. Wrong-phone
and wrong-address are P1 (they leak calls and confuse entity resolution);
formatting-only variants are noted but not action items.

### 5. Assemble the deliverables

**`gbp_optimization_plan.docx`** (docx skill conventions):
- Executive summary — score, band, top-3 gaps vs the local pack.
- Scorecard table with per-section findings and evidence.
- Prioritized fixes P1–P3, each with the exact action, owner, and
  ready-to-paste copy where applicable: GBP description (≤750 chars),
  services list with descriptions, review-request message templates, and
  a 4-week posts calendar.
- Review strategy — target velocity benchmarked against pack competitors,
  response templates for positive/negative, response-time SLA.

**`gbp_citation_log.xlsx`**:
- `Citation Log` — one row per directory: NAP found, per-field
  match/mismatch, severity, fix URL, status column for the implementer.
- `Task List` — every P1–P3 fix as a row with owner and status.
- `Pack Benchmark` — the money-query pack table from step 2.

## Hard rules

- **Never recommend policy-violating tactics:** no keyword-stuffing the
  business name (suspension risk — flag it if the client is already doing
  it), no review gating, no incentivized or fabricated reviews, no fake
  service-area addresses. If the client's current listing violates
  policy, the fix is remediation, listed as P1 with the risk explained.
- Every recommendation cites its evidence (screenshot, fetched page,
  search result). Unverifiable ≠ compliant — say "unverified".
- Never fabricate directory listings or review counts. If a directory
  can't be fetched, mark it "not checked" in the log.
- Legal/medical verticals: review-solicitation rules vary by jurisdiction
  and bar association — flag the review strategy for the client's
  compliance sign-off instead of asserting it is permitted.

## Edge cases

- **Multi-location businesses:** one scorecard + citation log tab per
  location; canonical NAP per location. Ask which locations are in scope
  before fetching everything.
- **Service-area businesses (hidden address):** skip address-display
  checks, audit service-area settings instead; citations use the
  registered address per Google's SAB rules.
- **Suspended or unverified listings:** stop and say so — recovery is a
  different workflow (reinstatement request), not an optimization plan.
- **Prior audit provided:** lead the summary with the score delta and
  close/carry-forward each prior task before adding new ones.
