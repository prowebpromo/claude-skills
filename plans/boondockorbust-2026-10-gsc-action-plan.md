# Boondock or Bust: GSC Action Plan (October 2026)

Source: GSC observations from the export window that ends September 30, 2026. Walmart clicks (1,343) match the earlier export, so this is the same window, not a trend shift.

Constraints on this draft:
- No GSC source is connected in Ahrefs (project 7574333 returns no rows) or Windsor. Exact URLs and per-URL query lists still need to come from a GSC export.
- boondockorbust.com was blocked by the network policy, so the current titles and on-page copy were not checked. Compare each proposed title with the live one before you publish.
- Proposed titles stay under about 60 characters. Prices, laws and policy claims must be checked against primary sources on the day you publish. This plan states none of them as fact.

Order: Batch 1 → 2 → 3 → 4. The Walmart title moved into Batch 1 because it has the most clicks to gain for the least work.

---

## Batch 1: existing-page pushes + Walmart title

Shared steps for each page in this batch:
1. Put a 40 to 60 word direct answer to the main query right under the H1.
2. Add 3 to 5 contextual internal links from related posts. Use descriptive anchors that vary, not just "click here" or the exact keyword every time.
3. Update the visible "last updated" date and `dateModified` in Article schema, but only when the content actually changed.
4. Request indexing in GSC after publishing.
5. Log the date each change shipped, so the 28-day before and after comparison uses clean windows.

### 1.1 Walmart overnight parking (111K impr, pos 6.7, 1.21% CTR)
- Problem: the title leads with "policy by state 2026". The question people search for ("can you park overnight at walmart", 2,544 impr, 0.79% CTR) never shows up in the title.
- Title: `Can You Park Overnight at Walmart? 2026 Rules by State`
- Meta: `Often yes, but it depends on the store manager and local law. See which states and cities restrict it, how to ask, and the etiquette that keeps lots open.`
- On-page: open with a yes/it-depends answer and how to confirm with a specific store. Keep the by-state table below it. Before publishing, check the "manager and local law" wording against Walmart's current public statement.
- Done when: the title and meta are live, the answer block sits above the fold, and the URL is resubmitted.
- Target: CTR at position 6 to 7 rises from 1.21% toward 3%+ over 28 days. This target is an assumption based on typical page-one CTR. It has not been benchmarked for this site.

### 1.2 UTV street legal laws (15,928 impr, pos 11.2, 0.4% CTR)
- Title: `Street Legal UTV Laws by State (2026): Where You Can Drive`
- Content: a state-by-state table (allowed / restricted / not allowed, registration path, plate type), an equipment checklist (lights, mirrors, horn, windshield, insurance), and a "how to make a UTV street legal" section. Cite each state's DMV or statute.
- Links in: RV towing, off-road and dispersed camping posts.
- Done when: every state row cites a source and has a check date.

### 1.3 RV dump stations guide (10,634 impr, pos 14.8) + "near me" (~2,000 impr, ~0 clicks)
- Title: `RV Dump Stations Near Me: How to Find One Fast (Free + Paid)`
- Content: an H2 called "How to find an RV dump station near you" that covers apps, truck stops, rest areas, campgrounds, municipal sites and RV dealers. Add a comparison table (cost range, how to verify, hours caveat) and dump etiquette and steps.
- Link to the free RV GPS app post and the free campsite apps post.
- Do not build a fake locator. Point readers to the tools that have live data.

### 1.4 Best apps for free campsites (8,738 impr, pos 14.8)
- Title: `Best Apps for Free Campsites in 2026, Compared`
- Content: a comparison table (free vs paid tier, offline maps, data source, best for). Give each app a "who it's for" verdict and state first-hand use where you have it.
- Cross-link with 1.3, 1.6 and the boondocking pillar (Batch 3).

### 1.5 Used Class B buyer's guide (8,601 impr, pos 11.7)
- Title: `Used Class B RV Buyer's Guide: What to Check Before You Buy`
- Content: a printable inspection checklist, chassis-specific weak points, a price/value section, and a link to the depreciation post (Batch 4.4) once it is live.
- Done when: the checklist is live and the forward link is in place or queued.

### 1.6 Best free RV GPS app (7,162 impr, pos 11.2, 102 clicks)
- The title already earns clicks from page two, so don't change it. This page needs better content and more internal links.
- Content: an updated comparison table, RV-specific routing (height/weight restrictions) per app, and offline support.
- Links in: from 1.3, 1.4 and the pillar.

---

## Batch 2: titles that lose the click

### 2.1 Yosemite toolkit (10,552 impr, 0.08% CTR, 8 clicks)
Diagnose before rewriting:
1. In GSC, filter Performance by Page = Yosemite URL, then export Queries.
2. Decision rule:
   - Mostly relevant queries (Yosemite camping, reservations, RV access): rewrite the title and meta to match the top 3 queries.
   - Mostly irrelevant queries (broad "Yosemite" or news terms): don't optimize for them. Retarget the page at the relevant queries and accept fewer impressions.
3. Deliverable: the query export, the decision, then the new title and meta.

### 2.2 Google Maps dispersed camping guide (5,460 impr, 0.15% CTR)
- Title: `How to Find Dispersed Camping on Google Maps (Step by Step)`
- Meta: `Find free dispersed campsites with Google Maps layers, satellite view and public land boundaries. Then confirm legality before you go.`
- Related check: "dispersed camping" queries rank around position 5 with zero clicks. In GSC, find which URL ranks for them. If it's this page, the new title fixes it. If it's another page, put "dispersed camping" plainly in that page's title too, and make sure the two pages don't compete for the same queries.

### 2.3 Smaller CTR fixes
Title formula: say what's on the page in the searcher's own words, then add a reason to click.

| Page | Impr | CTR | Proposed title |
|---|---|---|---|
| Senior discounts | 10.7K | 0.61% | `RV and Camping Senior Discounts: Every Deal Worth Using` |
| RV rental companies | 7K | 0.40% | `Best RV Rental Companies Compared: Prices, Fees, Fine Print` |
| Starlink data traps | 4.3K | 0.63% | `Starlink for RVs: Data Limits and Plan Traps to Avoid` |

Before publishing each one, pull that page's top queries from GSC and adjust the wording if they differ from what the title assumes.

---

## Batch 3: boondocking pillar repair

Current state: "boondocking" (657 impr) ranks 23rd and "RV boondocking" ranks 23rd, both with zero clicks. The boondocking-101 pillar ranks 46th.

### 3.1 Diagnose cannibalization first
Position 46 for the pillar while the site ranks 23rd for the head term means a different URL is probably ranking for it.
1. In GSC, filter Query = "boondocking", then open the Pages tab and list every URL that gets impressions.
2. If another URL holds position 23:
   - If it covers the same topic, merge it into the pillar and 301 redirect it.
   - If it covers a subtopic, keep it, refocus its title on that subtopic, and link it up to the pillar.
3. Confirm the pillar is indexed, self-canonical, and not blocked or noindexed.

### 3.2 Consolidate internal links
- Add the pillar to the main navigation and to the boondocking category hub.
- On every post that mentions boondocking, link the first mention to the pillar. Vary the anchors: "boondocking", "what boondocking is", "boondocking for beginners", "RV boondocking guide".
- Remove or redirect internal links that point to competing URLs for the head term.
- Done when: a crawl shows the pillar as the most internally linked boondocking URL.

### 3.3 Make it the definitive page
- Start with a definition block: what boondocking is, in 2 sentences, plus how it differs from dry camping and dispersed camping.
- Cover these entities: BLM land, national forests, Motor Vehicle Use Maps (MVUM), stay limits, Leave No Trace, power (solar, generator), water and waste management, connectivity, safety, and etiquette. Check each rule against BLM and USFS sources.
- Add hub sections that link down to the cluster: free campsite apps (1.4), dump stations (1.3), Google Maps dispersed camping (2.2), Walmart (1.1), Starlink (2.3), and memberships (4.1).
- Make the experience visible: real stays, photos and lessons learned. This is the information-gain edge on a term that generic listicles dominate.
- Schema: Article with author and `dateModified`. Use FAQ markup only for real on-page Q&A.
- Title: `Boondocking 101: The Complete Guide to Free RV Camping`

---

## Batch 4: new content (affiliate-led)

### 4.1 Camping membership costs compared (new post)
- Target queries: "good sam membership cost" (284 impr, pos 6.2, 0 clicks), "how much does harvest host cost" (148, pos 20), "thousand trails campgrounds" (241, pos 8.6, 0 clicks).
- Working title: `Camping Membership Costs Compared: Good Sam, Harvest Hosts, Thousand Trails`
- Structure: an answer table up top (annual cost, what's included, who it's for, break-even nights), then one section per membership, then "which one pays for itself".
- Rules: take prices from each official pricing page on the day you publish, and show the check date. Add the affiliate disclosure above the first affiliate link.
- Also update the old pages that rank for these queries with a link to the new post. Find them in GSC under Query → Pages.

### 4.2 Harvest Hosts reviews: push from 13.5 to page one
- Model it on the "RV Overnights vs Harvest Hosts" page, which gets 50 clicks at 10% CTR from position 3.6. Copy its structure: verdict up top, a pros and cons table, first-hand stay notes, and who should skip it.
- Link it from 4.1 and from the comparison page.

### 4.3 Individual Harvest Hosts location reviews (open lane)
- Pilot: Bully Hill Vineyards (1,370 impr, pos 9.7, 0 clicks).
- Only publish if you stayed there or can document the visit. A review without first-hand detail is thin content.
- Template: location summary, RV access and parking, the experience, purchase expectations, nearby, photos, and a verdict. Link to 4.2.
- If the pilot earns clicks within 28 days, roll out to other locations you've visited.

### 4.4 Class B RV depreciation (689 impr, pos 33, 0 clicks)
- Working title: `Class B RV Depreciation: How Fast Values Drop by Year`
- Data: cite valuation sources (e.g., J.D. Power RV values) or a documented sample of listings. Don't publish depreciation percentages without a named source.
- Links: two-way with the used Class B buyer's guide (1.5).

---

## Do not chase
- Navigational queries such as "allstays" and "rv overnights". The official sites own those clicks.

## Measurement
- Baseline: the window that ends September 30.
- Check each batch 28 days after it ships against the 28 days before it, matching days of the week.
- Batch 1 and 4.2: average position and clicks per URL.
- Batch 2: CTR at the same average position. A position change makes the CTR comparison invalid.
- Batch 3: position for "boondocking" and "RV boondocking", the pillar's position, and whether one URL owns the head term.
- Batch 4: indexed and ranking within 28 days, then affiliate clicks per post.

## Data needed to close the gaps
Export GSC Pages and Queries for the same window, plus page-filtered query exports for Yosemite, "boondocking" and "dispersed camping". Alternatively, connect Search Console to the Ahrefs Boondockorbust project. Either one lets these tasks name exact URLs and current titles.
