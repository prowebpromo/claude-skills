---
name: internal-linking
description: Produce a prioritized internal link plan — exact source page, target page, anchor text, and placement — from Sitebulb link exports, GSC Pages/Queries exports, or a bundled crawler when no exports exist. Use this skill whenever the user asks for an internal link plan, internal linking audit, internal link opportunities, link equity distribution, "which pages should link to [page]", orphan page fixes, crawl depth fixes, or internal anchor text review, or drops Sitebulb internal-link exports / GSC exports and asks how to improve internal linking. Also trigger on "build an internal link plan for [site]" or "find internal link opportunities". Output is an .xlsx link plan (donor, target, anchor, priority, rationale) plus orphan and depth fix lists, with an optional .docx summary. No Ahrefs or paid APIs required. Do NOT use for developer SOWs from Sitebulb hints (sitebulb-sow-builder), GSC recovery SOWs (gsc-sow-builder), external link building or outreach, or writing page content (geo-master-blueprint).
---

# internal-linking

Produce a prioritized, execution-ready internal link plan for one site. The
deliverable tells the client's team **exactly which page links to which page,
with what anchor, placed where, and why** — no judgment calls left to the
implementer. This skill plans links only; it does not write page copy
(geo-master-blueprint), build dev SOWs (sitebulb-sow-builder), or plan
recovery sprints (gsc-sow-builder).

## Inputs — files first, APIs never required

Accept whichever of these the user provides, in this priority order. Never
require a paid API. If only a domain is given, use the bundled crawler.

1. **Sitebulb link exports** (best source). Any of: "All Links" /
   "Internal Links" CSV (source URL, target URL, anchor text, link position),
   "Indexable URLs" CSV (unique inlinks count, crawl depth). Column names
   vary by Sitebulb version — map by meaning, not exact header.
2. **GSC exports** — the standard 3-month-with-YoY `Pages.csv` and
   `Queries.csv`. These drive target prioritization and anchor selection.
   The skill works without them, but say so in the deliverable: priorities
   are then structural (depth/orphans) rather than value-weighted.
3. **Bundled crawler fallback** — `scripts/crawl_links.py` builds the edge
   list from a live crawl when no Sitebulb export exists. Default cap 500
   pages; ask before crawling larger sites. Respect the cap and delay —
   never hammer a client's server.
4. **Optional client priority list** — money pages / practice areas /
   product pages the client cares about. If absent, infer money pages from
   URL patterns (e.g. /practice-areas/, /services/, /products/) and GSC
   value, and flag the inference in the deliverable.

## Workflow

Run `scripts/graph_metrics.py` to do the mechanical parts (steps 1–2);
do steps 3–5 yourself with judgment.

### 1. Build the link graph

Ingest the edge list (Sitebulb or crawler output). Classify each link as
`content` or `boilerplate` (nav/footer/sidebar/breadcrumb). Only content
links count toward equity; boilerplate links are noise. Compute per URL:
unique content inlinks, unique donor count, crawl depth from homepage,
orphan status (zero content inlinks). Flag internal links that hit
redirects or 404s — these go in the Fix list regardless of the plan.

### 2. Score targets (link-deficit model)

A target is a page whose value exceeds its link equity. Score per
`reference/methodology.md`: value from GSC impressions/clicks, striking-
distance queries (positions 4–15), and money-page status; equity from
content inlinks and depth. The top-deficit pages become plan targets.
Cap the plan at ~25 targets per run — a 200-row plan never gets executed.

### 3. Select donors for each target

Donor pages must clear ALL of these bars:
- **Topical relevance** — same section, overlapping URL/title tokens, or
  the donor's content genuinely discusses the target's topic. Never force
  a link from an unrelated page; an irrelevant internal link is worse
  than no link.
- **Has equity to give** — decent inlinks or traffic of its own.
- **Doesn't already link to the target** (in content).
- **Budget** — max 3 new outbound links added per donor per plan, max 10
  total content links added to any single page.

Prefer high-traffic blog/FAQ pages as donors for money-page targets:
informational pages earning traffic that should hand equity (and readers)
to commercial pages is the highest-value pattern this skill produces.

### 4. Choose anchors

Anchor source is the target's striking-distance queries from Queries.csv
(positions 4–15), reworded to read naturally in the donor's copy. Rules:
- Vary anchors across donors; no more than ~30% of a target's new anchors
  may be the same exact phrase.
- Never use an anchor that is the DONOR's own primary query — that reads
  as the donor competing with itself (cannibalization guard).
- 2–6 words, natural phrasing; no "click here", no bare URLs.
- Without GSC data, derive anchors from the target's title/H1, varied.

### 5. Assemble the deliverable

**`internal_link_plan.xlsx`** with these tabs:
- `Summary` — site, date, data sources used, counts, top-5 takeaways.
- `Link Plan` — one row per link: Priority (P1/P2/P3), Donor URL, Target
  URL, Anchor text, Placement note (e.g. "in the paragraph discussing X"),
  Rationale (one sentence citing the data), Status column left blank for
  the implementer.
- `Orphans & Depth` — orphan pages and pages deeper than 3 clicks, each
  with a recommended fix.
- `Broken & Redirected` — internal links hitting 3xx/4xx, with the
  correct target URL.
- `Anchor Inventory` — existing content anchors per target, so the
  implementer can see distribution before/after.

If the user wants a client-facing summary, add a 1-page .docx (docx skill
conventions) — plan highlights only, no tab dumps.

## Hard rules

- Every recommendation must be traceable to data in the inputs. No
  "consider adding links" filler — exact donor, exact target, exact anchor.
- Never recommend sitewide nav/footer links as an equity tactic.
- Never fabricate URLs. Every donor and target must exist in the crawl or
  export.
- If inputs conflict (e.g. Sitebulb depth vs crawler depth), prefer
  Sitebulb and note the discrepancy in Summary.
- State data gaps plainly in the Summary tab (e.g. "no GSC data — targets
  prioritized structurally").

## Edge cases

- **Huge sites (>5k URLs):** plan one section at a time; ask which section
  matters most rather than sampling arbitrarily.
- **No homepage in edge list:** depth is uncomputable; skip depth scoring
  and say so.
- **Pagination/faceted URLs:** exclude from targets and donors
  (`?`, `/page/`, `/tag/` patterns) unless the user says otherwise.
- **Sitebulb SOW follow-on:** when the user has a sitebulb-sow-builder
  deliverable in the same conversation, reuse its crawl data and reference
  its ticket IDs in the Rationale column instead of re-deriving issues.
