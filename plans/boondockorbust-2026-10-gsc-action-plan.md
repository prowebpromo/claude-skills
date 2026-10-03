# Boondock or Bust: GSC Action Plan (October 2026, v2)

Version 2 uses the Pages.csv and Queries.csv exports. It keeps the four-batch structure and adds the corrections from the second review.

## Data limits (read first)
- The exports have no date range. The page totals don't match the earlier observations. In this export the Walmart page has 42,127 impressions and 659 clicks. The observations had 111K and 1,343. That makes this a different, probably shorter, window. Record the export dates and filters before using either set as a baseline.
- Queries.csv is capped at 1,000 rows and leaves out anonymized queries. Walmart queries in it add up to 9,524 impressions, against 42,127 for the page. Query-level analysis covers only the visible share.
- The exports have no query-to-page pairs. Wherever a task says "which URL ranks for X", run a GSC Performance report filtered by query and read the Pages tab.
- The live site was not crawled because the network policy blocks it. Check current titles, H1s and canonicals before you edit.
- Two corrections to the original brief:
  - A move to page one does not predict a given traffic gain.
  - Low CTR does not prove the title is wrong. Check the query mix, position, SERP features and device first.

Each task carries two statuses:
- Implementation: VERIFIED / NOT VERIFIED
- Performance impact: ESTABLISHED / NOT YET ESTABLISHED

---

## Live check (crawled 2026-10-03)

Most target pages were edited between Sept 25 and Oct 1, 2026, at or after the end of the GSC window. The export therefore measures the old versions of those pages.

Rule: don't re-edit a page changed on or after Sept 25 until 28 days of post-change data exist. Measure it instead.

| Page | Last modified | Live title | Status |
|---|---|---|---|
| Walmart | 2026-05-23 | Walmart Overnight RV Parking Policy by State 2026 | Edit now (1.1) |
| RV rental companies | 2026-05-22 | Best RV Rental Companies 2026: Real Costs Compared | Edit now (2.3) |
| Free RV GPS app | 2026-07-18 | Free Truck GPS Apps for RVers: Avoid Low Bridges (2026) | Edit now: title and H1 miss "free RV GPS app" (pos 9.29) |
| Camper on property | 2026-09-12 | How Long Can Someone Live in a Camper on Your Property? | Edit now (1.7): "can I live" phrasing not covered |
| UTV street legal | 2026-10-01 | Street Legal UTV Laws by State (2026): All 50 States Checked | Measure. "Side by side" is still missing, so queue it for the next edit |
| Dump stations | 2026-09-29 | RV Dump Stations: Finder Apps, Fees and Free Options | Measure. "Near me" is still missing, so queue it |
| Free campsite apps | 2026-09-30 | Best Free Camping Apps 2026 \| Guide to Free RV Sites | Measure |
| Yosemite | 2026-09-26 | Yosemite 2026 RV Guide: Parking, Passes and Towing | Measure. The meta now covers fees |
| Dispersed / Google Maps | 2026-09-29 | How to Find Dispersed Camping With Google Maps | Measure. The title already says "dispersed camping", so the original premise was wrong |
| Senior discounts | 2026-09-29 | Senior RV Camping Discounts: Are They Worth It? (2026) | Measure. Remove the leaked build-note HTML comment from the content |
| Boondocking pages (4) | 2026-09-25 to 09-30 | See Batch 3 | Consolidation decision still needed |
| Membership pages | 2026-09-29 to 09-30 | See 4.1 | Duplicate titles confirmed |
| Bully Hill | 2026-09-29 | Bully Hill Vineyards Harvest Hosts RV Stay Review | Measure |

Already handled on the live site:
- The 2025 used Class B guide 301s to the 2026 version.
- The 2025 best and worst Class B page 301s to the 2026 version.
- The UTV and club-membership URL variants 301 correctly.
- The `[YOUR-EMAIL-SIGNUP-URL]` placeholder is gone.

Still open:
- The blackjack URL, both `/routes/` pages and the Walmart variant `/resources/walmart-overnight-rv-parking-policy-state-2026` 301 to the homepage. Google usually treats a redirect to the homepage as a soft 404.
  - Return 410 for the blackjack and `/routes/` URLs.
  - Point the Walmart variant at the Walmart page.
- The UTV PDF (`/wp-content/uploads/2026/02/navigating-the-asphalt-with-your-utv.pdf`) still returns 200. Add an `X-Robots-Tag: noindex` header, or link it only from the UTV page.
- The senior discounts page publishes an editing-instructions HTML comment ("Paste into WordPress > Pages > Edit…") inside the content. Browsers ignore it, but it is public in the page source. Delete it. Spot checks of four other pages found no such comment.

---

## Batch 0: baseline and site hygiene (do first, small)

| # | Task | Evidence | Done when |
|---|---|---|---|
| 0.1 | Record the baseline: export dates, search type, country/device filters, and per-URL clicks/impressions/CTR/position for every URL below | The window mismatch above | One dated baseline sheet plus a change log |
| 0.2 | Investigate `/uncategorized/best-free-blackjack-software-for-online/` | An off-topic gambling URL that Google indexed | Confirmed clean or removed. If it was injected, check users, plugins and recent posts. URL returns 410/404 and is out of the sitemap |
| 0.3 | Fix the placeholder link `[YOUR-EMAIL-SIGNUP-URL]` on `/resources/where-to-dump-trash-while-boondocking-legal-rules-disposal-locations/` | Google discovered it as a URL | Real signup URL in place, or the link removed |
| 0.4 | Check redirects for URL variants: `/resources/street-legal-utv-laws/`, `/resources/walmart-overnight-rv-parking-policy-state-2026`, `/boondockering-guide/guide-to-rv-club-memberships/` | Variants are getting impressions | Each one 301s to its canonical URL |
| 0.5 | Look at the off-topic `/routes/` pages (`pico-bolivar-summit`, `roraima-trek`) | Not RV content | Keep with a reason, or noindex/remove |

---

## Batch 1: existing pages + Walmart snippet

### 1.1 Walmart snippet
URL: `/resources/walmart-overnight-rv-parking-policy-by-state-2026/` (42,127 impr, 1.56% CTR, pos 6.43)

Query evidence (visible share only):
- Question queries ("can you / does / is…") get 1.89% CTR across 6,914 impr at weighted pos 5.1.
- Non-question queries get 4.48% across 2,610 impr at pos 5.7.
- The head term "walmart overnight parking" already gets 9.69% at pos 3.36.

Question searchers click about half as often at the same position. Google may be answering them on the results page, but no SERP check has been done to confirm that. A title that mirrors the question is worth testing. It should not drop the head term.

- Title: `Can You Park Overnight at Walmart? RV Rules by State` (51 chars). It keeps "by state" for the "which walmarts allow" queries and the state-specific ones.
- H1: matches the question.
- Opening paragraph: answers directly that it depends on the store manager and local ordinance. Check this against Walmart's current public statement.
- Meta: answer first, then a pointer to the state table and the "how to confirm a store" steps.
- Do not change the URL. The year in the slug stays. Plan to update the content in place each year.

### 1.2 UTV street legal laws
URL: `/resources/utv-street-legal-laws/` (10,000 impr, 0.31%, pos 9.88)
- 1,052 of 2,181 cluster impressions use "side by side" wording, with 0 clicks. Put "side-by-side" in the title, H1 and one H2.
- North Carolina queries total 313 impr. Add an NC section sourced from NCDMV or the state statute.
- Title: `Are UTVs and Side-by-Sides Street Legal? Laws by State`
- Make no blanket nationwide legality claims. Cite an official source for each state row.
- Check the stray PDF `/wp-content/uploads/2026/02/navigating-the-asphalt-with-your-utv.pdf`. If it duplicates the page, canonicalize or noindex it.

### 1.3 RV dump stations
URL: `/resources/quick-guide-to-finding-rv-dump-stations-while-on-the-road/` (5,706 impr, 0.23%, pos 11.68)
- "Near me" variants: 37 queries, 2,686 impr, 3 clicks, weighted pos 12.
- Expect limited upside. "Near me" searches are usually served by map and local results. This is a SERP assumption that hasn't been checked.
- Add an H2 called "Find an RV dump station near you". Cover the finder apps/sites, truck stop chains, rest areas and campgrounds, a "call ahead" fee and access check, and the "by zip code" and "map" phrasing.
- Title: `RV Dump Stations Near Me: How to Find One Fast`
- Do not imply live listings or location awareness.

### 1.4 Free campsite apps
URL: `/boondocking-guide/the-best-apps-for-finding-free-campsites/` (3,024 impr, 0.6%, pos 11.5)
- Head-to-head queries convert: "ioverlander vs the dyrt", "the dyrt vs campendium" and "campendium vs ioverlander" get 4.08% CTR at pos 6.4. Head terms like "free camping app" sit at pos 40+.
- Add head-to-head comparison sections and an "alternatives to FreeRoam / AllStays" section. Check current features and pricing for each app.
- Clarify the overlap with the GPS app page and the Google Maps page (link between them, don't duplicate content).

### 1.5 Used Class B buyer's guide (cannibalization)
- `/class-b-rv/dont-buy-a-used-class-b-rv-in-2026-until-you-read-this-complete-guide/`: 2,586 impr, pos 12.34
- `/class-b-rv/dont-buy-a-used-class-b-rv-in-2025-until-you-read-this/`: 161 impr, pos 8.24
- `/class-b-rv/the-essential-class-b-rv-buying-guide-for-2026/`: 129 impr, pos 8.53
- Same pattern on `/class-b-rv/honest-reviews-of-the-best-and-worst-class-b-rvs-of-2025/` vs `…-of-2026/`.

Action: pick one primary used-buyer URL, merge the unique content into it, and 301 the 2025 version. Then strengthen the inspection and ownership-cost sections. Make no unsupported reliability claims.

### 1.6 Free RV GPS app
URL: `/resources/whats-the-best-free-rv-gps-app/` (3,027 impr, 48 clicks, pos 9.66)
- Already earns clicks. Content work only: which apps are free, which support RV dimensions, and the routing limits.
- RV-routing questions show up ("which gps apps route around low bridges…", "avoiding tight turns"). Answer them directly.

### 1.7 Added: camper-on-property page (missing from the original brief)
URL: `/resources/can-someone-live-in-a-camper-on-my-property/`
- 19,445 impr, 0.38%, pos 7.63. Fragment URLs (#section-1 to 5, #scenario-answers, #zoning-quick-ref) add about 6,500 more impressions.
- This is the second-largest impression page. Its CTR is close to the UTV page.
- Queries split between "can someone live" and "can I live", and are state-specific (NC, PA, OH, GA).
- Action: validate the query mix, tighten the title and answer around "it depends on local zoning", and add state quick answers sourced to statutes or county code. This is YMYL-adjacent, so make no blanket legality claims.

---

## Batch 2: low-CTR diagnosis and repair

### 2.1 Yosemite toolkit
URL: `/resources/the-2026-yosemite-toolkit-reservations-closures-parking-solved/` (4,879 impr, 1 click)
- The visible queries are mostly about the entrance fee ("yosemite national park entrance fee per vehicle 7 days 2026" and variants). Several start with "+" or "%". That points to automated or tool-generated queries, not people. This is an inference that can't be verified from GSC.
- The title promises reservations, closures and parking. It doesn't mention fees.
- Decision:
  - If the page covers fees, add a fee section sourced to NPS and put "entrance fee" in the meta.
  - If it doesn't, leave the title and treat the impressions as low-value.
  - Don't count prefixed queries in CTR targets.

### 2.2 Dispersed camping
URL: `/boondocking-guide/how-to-find-free-dispersed-camping-sites-using-google-maps/` (3,405 impr, 0.09%, pos 6.72)
- The "dispersed" cluster has 2,761 impr and 1 click at pos 5.7. Most of it is "dispersed campi" (1,313), "dispersed camping near me" (601) and "dispersed camping" (384).
- The slug already says "dispersed camping". The original premise that "the title never says dispersed camping" may be wrong. Confirm the live title.
- More likely cause: intent mismatch. "Near me" and head-term searchers want locations or maps, not a Google Maps tutorial.
- Action:
  1. Confirm which URL ranks for these queries.
  2. Test the title `Dispersed Camping Near You: Find Free Sites on Google Maps`.
  3. Add a section on checking land status and rules (MVUM, BLM, stay limits) that cites agency sources.
- Larger option, for a separate decision: a dispersed camping hub organized by state.

### 2.3 RV rental companies
URL: `/boondocking-guide/the-best-rv-rental-companies-of-2026/` (2,857 impr, 0.49%)
- 729 of 1,131 rental-query impressions are long, AI-prompt-style queries ("find me rv rental options with top brand reputations", "give me a list of rv rental companies…"), with 1 click.
- A title rewrite won't fix that share. Judge CTR on the conventional queries only ("best rv rental companies", "cruise america alternatives" with 204 impr at pos 10.24).
- Action: add a "Cruise America alternatives" section and a reputation and customer service comparison. Check fees and terms against each company's site.

### 2.4 Senior discounts and Starlink
- `/resources/exclusive-senior-citizen-discounts-for-campers/` (3,304, 0.45%): the queries say "camping discounts", "senior camping discounts", "AARP". Membership and discount queries overall: 1,368 impr, 1 click. Check the current discount terms before rewriting.
- `/resources/where-did-my-starlink-data-go-5-traps-draining-your-100gb-plan/` (1,880, 0.64%): check the current Starlink plan terms first. Low priority.

### 2.5 Harvest Hosts reviews (fragmented)
- Harvest Hosts queries add up to only 324 impr. "harvest hosts review" is at pos 26 in this window, not 13.5.
- Coverage is split across `/resources/harvest-hosts-how-it-works-top-regrets/` (pos 18.3), `/blog/harvest-hosts-is-it-really-free-camping/` (pos 16.4) and the comparison pages.
- Action: pick one review URL, merge in the unique content from the other, and keep the RV Overnights comparison page separate. Low volume, so do this after Batch 3.

---

## Batch 3: boondocking pillar

Cannibalization confirmed at the page level:

| URL | Impr | Pos |
|---|---|---|
| `/boondocking-guide/boondocking-for-beginners/` | 210 | 7.86 |
| `/rv-boondocking/` | 203 | 30.38 |
| `/boondocking-guide/boondocking-101-everything-you-need-to-know-to-get-started/` | 85 | 21.81 |
| `/boondocking-guide/` (hub) | 77 | 11.18 |
| `/beginners-guide/` | 71 | 28.18 |
| `/boondocking-guide/boondocking-tips/` | 247 | 10.15 |

Query side:
- "boondocking": 320 impr, pos 16.04
- "rv boondocking": 83, pos 18.39
- "boondocking for beginners": 36, pos 40.44

Live titles and H1s show four pages with the same promise:
- boondocking-101 H1: "Ultimate Guide to RV Boondocking…"
- `/rv-boondocking/` title: "Ultimate guide to RV boondocking…"
- `/beginners-guide/` H1: "Beginner's Guide to RV Boondocking"
- `boondocking-for-beginners`: "Boondocking for Beginners…"

All four were edited between Sept 25 and 30. That edit tuned each page separately and did not consolidate them.

Steps:
1. Pick the primary URL from evidence, not from the name. `boondocking-for-beginners` ranks best right now, but boondocking-101 was the planned pillar. Check which URL Google shows for "boondocking" in a query-filtered GSC report. Also check backlinks to each candidate.
2. Merge boondocking-101, `/rv-boondocking/` and `/beginners-guide/` into the primary where they substantially overlap. 301 the retired URLs and update the internal links that point to them.
3. Cover the core topics: definition, boondocking vs dry camping vs dispersed camping, finding legal sites, water, waste, power, connectivity, safety, etiquette and stay limits. Source rules to BLM and USFS.
4. Build an internal link map from cluster pages to the pillar with varied anchors. Keep the links to specialist guides (LTVA, BLM rules, water management, pop-up camper).
5. Done when: there is one designated pillar, the retired URLs 301, no broken links or orphans, and the internal-link crawl confirms the pillar as the top-linked boondocking URL.

Weakest assumption: that consolidation alone closes the gap. Site authority and the competing results may limit the head term.

---

## Batch 4: commercial content

### 4.1 Membership costs: expand existing pages, don't start from zero
The live check confirms duplicate intent:
- `guide-to-rv-club-memberships` title: "Are RV Memberships Worth It? 2026 Break-Even Math"
- The economics report H1: "Are RV Memberships Worth It? Break-Even Math for 2026"
- The Good Sam vs HH vs RVO title also leads on costs.

Give each page one distinct job before adding anything:
- The economics report becomes the cost-comparison hub.
- The club guide covers which club fits which traveler.
- The three-way comparison stays a head-to-head.

Existing pages that already target this:
- `/boondocking-guide/guide-to-rv-club-memberships/` (775 impr)
- `/resources/the-2026-rv-membership-economics-report-break-even-analysis-hidden-cost-data/` (109)
- `/resources/rv-membership-break-even-calculator/`
- `/boondocking-guide/good-sam-vs-harvest-hosts-vs-rvo/` (2,234)
- `/resources/thousand-trails-membership-a-comprehensive-guide/` (749 impr, 0 clicks)

Demand:
- Good Sam cost queries: 632 impr, 4 clicks, pos 8.0
- Thousand Trails: 469 impr, 0 clicks
- "how much does harvest host cost": 73, pos 19.85

A new "costs compared" post would compete with these five pages. Instead:
- Make the membership economics report the cost hub. Retitle it around "camping membership costs compared".
- Add dated, sourced price tables.
- Link to it from the other four with cost-intent anchors.
- Add the Good Sam and Harvest Hosts cost answers near the top.
- Check every affiliate destination and disclosure.

### 4.2 Bully Hill: the page already exists
- `/blog/bully-hill-vineyards-harvest-host-review/` has 394 impr, pos 9.7 and 1 click. "bully hill vineyards reviews" has 277 impr and 0 clicks.
- It is not an open lane. The page is there and doesn't win the click, and general winery-review searchers likely prefer review platforms.
- Other location reviews also get little: Meiers Creek pos 15.4, Cayuga Ridge pos 13.7, Rustic Ridge pos 18.6.
- Action: retitle around the RV and Harvest Hosts stay angle and refresh it with first-hand notes and photos. Don't scale location reviews until one of them earns clicks.

### 4.3 Class B depreciation
- "class b rv depreciation" has 238 impr at pos 32.4. "rv depreciation" has 160 at pos 75. The ranking URL is unknown.
- Low volume. Write it after 1.5, sourced to valuation guides or documented sold-price data, not asking prices.
- Link it two-way with the buyer's guide.

---

## Do not chase
- Navigational queries: "allstays" (1,254 impr), "rv overnights" (731), "thousand trails" and "goodsam.com".
- Query-operator or prompt-style impressions as CTR targets.

## Measurement
- Compare 28 and 56 days after each change against matched windows. Account for seasonality and changes in query mix.
- For CTR tasks, compare at a similar average position, or report the position change alongside.
