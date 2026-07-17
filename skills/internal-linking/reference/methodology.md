# internal-linking — scoring methodology

The plan is built from a link-deficit model: **targets** are pages whose
search value exceeds their internal link equity; **donors** are pages with
equity to spare and topical relevance. This file defines the numbers.
`scripts/graph_metrics.py` implements the mechanical parts.

## 1. Per-URL metrics

From the edge list (Sitebulb export or crawler output):

| Metric | Definition |
|---|---|
| `inlinks_content` | Unique (donor, target) pairs where position = content |
| `donor_count` | Unique donor pages linking in content |
| `depth` | BFS hops from homepage following content+boilerplate links |
| `orphan` | `inlinks_content == 0` |

From GSC (when provided), per URL: `clicks_3mo`, `impressions_3mo`,
striking-distance queries = queries mapped to the page with
4 ≤ position ≤ 15 and impressions ≥ 50.

## 2. Value score (0–100)

```
value = 35 * norm(log(1 + impressions_3mo))
      + 25 * norm(log(1 + clicks_3mo))
      + 25 * norm(striking_distance_impressions)
      + 15 * money_page          # 1 if on priority list / money URL pattern
```

`norm()` = min-max normalization over the analyzed URL set.
Without GSC data: `value = 60 * money_page + 40 * norm(title/URL token
match against site's core topics)` — and the deliverable must state that
prioritization is structural, not value-weighted.

## 3. Equity score (0–100)

```
equity = 60 * norm(log(1 + inlinks_content))
       + 25 * norm(log(1 + donor_count))
       + 15 * depth_factor      # 1.0 at depth ≤1, 0.6 depth 2, 0.3 depth 3, 0 deeper
```

## 4. Deficit and priority

```
deficit = value - equity
```

Rank by deficit descending; take top ~25 as plan targets.

- **P1** — deficit ≥ 40, or any orphan with value ≥ 30
- **P2** — deficit 20–39
- **P3** — deficit < 20 but structurally weak (depth > 3 or ≤ 1 donor)
  AND value ≥ 20 — zero-value pages never earn a tier

Links per target: P1 gets 4–6 new links, P2 gets 2–4, P3 gets 1–2.

## 5. Donor eligibility

A donor must pass ALL:

1. Topical relevance — same URL section as target, OR ≥ 2 meaningful
   shared tokens between titles/H1s (ignore stopwords and the brand name),
   OR its content demonstrably covers the target's topic.
2. `equity ≥ median equity` of the URL set, OR `clicks_3mo` in the top
   quartile (high-traffic informational pages are prime donors even when
   their own inlink count is modest).
3. No existing content link to the target.
4. Budget: ≤ 3 new outbound links per donor per plan; target page ends
   with ≤ 10 added content links total.

Rank eligible donors by `0.6 * relevance + 0.4 * norm(clicks_3mo)` and
assign from the top until the target's link quota is filled.

## 6. Anchor selection

Pool = target's striking-distance queries, highest impressions first.

- ≤ 30% of a target's new anchors may share the same exact phrase; reword
  the rest (query "nypd accident report online" → anchors "get your NYPD
  accident report online", "requesting an NYPD collision report", …).
- Exclusion: never use a phrase that is a striking-distance or ranking
  query of the DONOR page (cannibalization guard).
- Length 2–6 words; must read as natural prose at the placement point.
- No GSC data → derive from target H1/title with the same variation rules.

## 7. Structural fixes (always included, independent of the plan)

- Orphans: every orphan gets ≥ 1 recommended content link (or a
  recommendation to deindex/remove if it has no value signal).
- Depth: pages with value ≥ 30 at depth > 3 get a link from a depth ≤ 2
  donor.
- Broken/redirected internal links: list with the resolved final URL;
  these are implementer fixes, not plan links.
