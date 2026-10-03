# Handoff: Boondock or Bust GSC work (resume in a new session)

Repo: `prowebpromo/claude-skills`, branch `claude/clever-ptolemy-rj131c`
Plan: `plans/boondockorbust-2026-10-gsc-action-plan.md` (v2.1, includes the live-site check of 2026-10-03)

## Paste this to start the new session
> Resume Boondock or Bust work. Read `plans/boondockorbust-HANDOFF.md` and `plans/boondockorbust-2026-10-gsc-action-plan.md` on branch `claude/clever-ptolemy-rj131c`. Confirm `BOB_WP_USER` and `BOB_WP_APP_PASSWORD` are set and authenticate read-only first. Then show me the current vs proposed values for the change package before writing anything.

## State at handoff
- Network: `boondockorbust.com` is reachable (allowlisted).
- Credentials: `BOB_WP_USER` and `BOB_WP_APP_PASSWORD` were added to the environment but were not visible in the old session. A new session is needed to pick them up. Never print their values.
- GSC: there is no connected source (the Ahrefs project 7574333 has no GSC data, and Windsor has no searchconsole connection). The data came from the uploaded Pages.csv and Queries.csv. They have no date range and come from a different window than the original observations.
- Site stack (from `/wp-json/`): WordPress with application-password auth, Rank Math (`rankmath/v1`), the Redirection plugin (`redirection/v1`), Divi, LiteSpeed Cache, Code Snippets.
- Measure-only rule: don't edit pages modified on or after 2026-09-25 until 28 days of post-change GSC data exist. The list is in the plan's Live check table.

## Change package (approved for staging, NOT yet approved to publish)
WordPress has no native "draft" for a published post. Updating one changes it live. Process:
1. Read the current values (post title, Rank Math title and description).
2. Show the before and after.
3. Apply only after Chuck says go.
4. Purge the LiteSpeed cache for the URL.
5. Log the change date in the plan.

| Post ID | URL | Field | Proposed |
|---|---|---|---|
| 68886 | /resources/walmart-overnight-rv-parking-policy-by-state-2026/ | SEO title (52) | Can You Park Overnight at Walmart? RV Rules by State |
| 68886 | same | Post title / H1 | Can You Park Overnight at Walmart? RV Parking Rules by State |
| 68886 | same | Meta (153) | Walmart corporate allows overnight RV parking, but store managers and local laws decide. Check your state, verify the store first, and know your backups. |
| 59663 | /resources/whats-the-best-free-rv-gps-app/ | SEO title (58) | Best Free RV GPS App? Truck GPS Apps That Flag Low Bridges |
| 59663 | same | Meta (~150) | TruckMap and TruckRouter.com flag low bridges and weight limits Google Maps misses. See when free truck GPS apps work for RVs and where they fall short. |
| 58167 | /resources/can-someone-live-in-a-camper-on-my-property/ | SEO title (60) | Can Someone Live in a Camper on Your Property? Laws by State |
| 58167 | same | Meta (150) | It depends on state law, county zoning and permits. See 2026 rules by state, how long a guest can stay, permit steps and the tenant-law trap to avoid. |
| 56261 | /boondocking-guide/the-best-rv-rental-companies-of-2026/ | SEO title (62) | Best RV Rental Companies 2026: Cruise America and Alternatives |
| 56261 | same | Meta (142) | RV rentals run 20-60% above advertised rates once fees hit. Compare Cruise America, Outdoorsy and RVshare on real trip totals before you book. |
| 57732 | /resources/exclusive-senior-citizen-discounts-for-campers/ | Content | Delete the leaked HTML comment that begins `<!-- ====...PAGE: Senior RV Camping Discounts` and contains "Paste into WordPress". Change nothing else. Re-crawl after and confirm 1 H1 and unchanged word count (about 4,950). |

Notes on the package:
- Walmart:
  - The H1 currently comes from the post title. The H1 change keeps the head term "walmart overnight parking" out of the leading words, but the SEO title keeps "Overnight at Walmart". Queries show question searches at 1.89% CTR vs 4.48% for non-question searches. That supports testing the question-led title. It does not prove the old title was wrong.
  - The meta's "corporate allows" comes from the page's own copy ("Corporate says yes"). Check it against Walmart's current public statement before publishing.
- GPS app: the page is about truck GPS apps used as an RV backup. The title keeps that honest and adds the query "free RV GPS app" (pos 9.29).
- Camper: this keeps "someone", because "how long can someone live…" had clicks at pos 5.19. The H1 stays unchanged and still carries "How Long".
- RV rentals: about two-thirds of the impressions are AI-prompt-style queries, so expect only a small CTR change. The title assumes a "Cruise America alternatives" section exists. Check the page, and add the section first if it's missing.
- Fact check: the 20-60% figure and the Outdoorsy/RVshare/Cruise America names come from the page itself, not from independent checks.

## Also queued (needs approval, low risk)
- Redirection plugin:
  - `/resources/walmart-overnight-rv-parking-policy-state-2026` currently 301s to the homepage. Point it at the Walmart page instead.
  - `/uncategorized/best-free-blackjack-software-for-online/` and `/routes/pico-bolivar-summit/` and `/routes/roraima-trek/` 301 to the homepage. Change them to 410.
  - Check first whether a redirect rule or a theme fallback is producing the homepage redirect.
- Investigate the blackjack URL's origin. Look at users, plugins and recent posts for signs of injection.
- UTV PDF `/wp-content/uploads/2026/02/navigating-the-asphalt-with-your-utv.pdf`: add a noindex header (LiteSpeed/.htaccess) or leave it as is. This needs a decision.

## Implementation notes
- Auth: HTTP Basic with `$BOB_WP_USER:$BOB_WP_APP_PASSWORD` against `https://boondockorbust.com/wp-json/`. First call: `GET /wp/v2/users/me?context=edit` to confirm the role (Editor expected).
- Raw content: `GET /wp/v2/posts/<id>?context=edit` (use `content.raw`).
- Rank Math fields: the meta keys are `rank_math_title` and `rank_math_description`. The usual write path is `POST /rankmath/v1/updateMeta` with `objectID`, `objectType: "post"` and `meta: {...}`. This endpoint was not tested. Confirm it on one post, then re-crawl `<title>` and the meta description to verify.
- Verify after each change: the live `<title>`, the meta description, the H1 count, the canonical and robots meta. Use `/tmp/.../scratchpad/crawl.py` logic, or re-create it: urllib with no redirect follow, regex for the title/meta/canonical, and html.parser for word counts. A regex word count breaks on the senior page because of the leaked comment.
- Statuses per task: Implementation VERIFIED / NOT VERIFIED, and Performance ESTABLISHED / NOT YET ESTABLISHED.

## Open items still needing data
- Query-filtered GSC page reports for "boondocking" and "dispersed camping", to choose the boondocking pillar and confirm which URL ranks for the dispersed queries.
- Export dates for Pages.csv and Queries.csv.
