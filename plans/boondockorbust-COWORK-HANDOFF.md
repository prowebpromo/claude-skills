# Cowork handoff: Boondock or Bust change package (2026-10-03)

Run this in Cowork. The cloud session could not finish because:
- It has no Hostinger access.
- WordPress never receives the REST Authorization header. A bogus login and the real login both return `rest_not_logged_in`.

Cowork does every step below. Chuck's only job is the single "go" in step 3.

Repo: `prowebpromo/claude-skills`, branch `claude/lucid-franklin-wjny5o`
Context: `plans/boondockorbust-HANDOFF.md`, `plans/boondockorbust-2026-10-gsc-action-plan.md`

Rules:
- Never print credentials.
- Change nothing beyond the fields listed here.
- WordPress has no draft state for a published post. Saving a post makes it live.

## Step 1. Fix the REST Authorization header (Hostinger)
1. Log in to Hostinger hPanel. Go to boondockorbust.com, then File Manager, then `public_html/.htaccess`.
2. Save a copy as `public_html/.htaccess.bak-2026-10-03`.
3. Insert this at the very top of the file, above `# BEGIN WordPress` and any LiteSpeed block:
   ```
   # BEGIN Pass Authorization header
   <IfModule mod_rewrite.c>
   RewriteEngine On
   RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
   </IfModule>
   <IfModule mod_setenvif.c>
   SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
   </IfModule>
   # END Pass Authorization header
   ```
4. Save. Load `https://boondockorbust.com/` and `/resources/whats-the-best-free-rv-gps-app/`. If either returns 500, restore the backup and stop.
5. Purge the Hostinger CDN cache (hPanel, then Performance, then CDN).

## Step 2. Authenticate read-only and read current values
- Credentials: the env vars are `Boondockorbust_WP_USER` and `Boondockorbust_WP_APP_PASSWORD`. The older handoff calls them `BOB_WP_*`, which is wrong.
- Call `GET https://boondockorbust.com/wp-json/wp/v2/users/me?context=edit` with HTTP Basic auth. Expect 200 and the Editor or Administrator role.
- If REST still returns 401, log in to wp-admin in the browser and do steps 2 to 5 there. Rank Math's fields are in the post editor's Rank Math panel, under Edit Snippet.
- For each post below, read the raw post title, `rank_math_title`, `rank_math_description` and `content.raw` (`GET /wp/v2/posts/<id>?context=edit`).

Public live values read 2026-10-03. Confirm the raw values match these:

| ID | Field | Current (live) | Proposed |
|---|---|---|---|
| 68886 | SEO title | Walmart Overnight RV Parking Policy by State 2026 | Can You Park Overnight at Walmart? RV Rules by State |
| 68886 | Post title / H1 | Walmart Overnight RV Parking Policy by State — Your 2026 Survival Guide | Can You Park Overnight at Walmart? RV Parking Rules by State |
| 68886 | Meta | Check Walmart overnight RV parking rules by state in 2026. Learn when to call, what local laws override, and where to find backup stops. | Walmart corporate allows overnight RV parking, but store managers and local laws decide. Check your state, verify the store first, and know your backups. |
| 59663 | SEO title | Free Truck GPS Apps for RVers: Avoid Low Bridges (2026) | Best Free RV GPS App? Truck GPS Apps That Flag Low Bridges |
| 59663 | Meta | TruckMap and TruckRouter.com help RVers check routes for low bridges, weight limits and restricted roads for free, which Google Maps cannot do. | TruckMap and TruckRouter.com flag low bridges and weight limits Google Maps misses. See when free truck GPS apps work for RVs and where they fall short. |
| 59663 | Content | Contains `<!-- Paste into WordPress > Pages > Edit > Text tab -->` | Delete that one comment only |
| 58167 | SEO title | How Long Can Someone Live in a Camper on Your Property? | Can Someone Live in a Camper on Your Property? Laws by State |
| 58167 | Meta | How long someone can live in a camper on your property, plus permit costs, the rent-free tenant trap, and fines if caught. 50-state 2026 rules. | It depends on state law, county zoning and permits. See 2026 rules by state, how long a guest can stay, permit steps and the tenant-law trap to avoid. |
| 57732 | Content | Contains a build-note comment beginning `<!-- ====` with `PAGE: Senior RV Camping Discounts` and "Paste into WordPress" | Delete that one comment only. Change nothing else. |
| 56261 | SEO title | Best RV Rental Companies 2026: Real Costs Compared | NO CHANGE. The page has no Cruise America alternatives section yet. |
| 56261 | Meta | Rental costs run 20-60% above advertised rates after mileage, generator and insurance fees. Compare Outdoorsy, RVshare and Cruise America. See real totals. | NO CHANGE. The current meta is already strong. Skip it unless Chuck asks. |

Before showing the table:
- Check the Walmart meta's "corporate allows" claim against Walmart's current public statement. Report what you find, with the source URL.
- If it doesn't hold, propose replacement wording.

## Step 3. Approval gate
Show Chuck one table with the raw current value, the proposed value and the character count for each row. Wait for "go". This is the only stop.

## Step 4. Apply
- SEO fields: `POST /wp-json/rankmath/v1/updateMeta` with body `{"objectID": <id>, "objectType": "post", "meta": {"rank_math_title": "...", "rank_math_description": "..."}}`.
  - This endpoint is untested. Try it on 59663 first and verify before doing the rest.
  - If it fails, use the wp-admin Rank Math panel instead.
- Post title (68886): `POST /wp/v2/posts/68886` with `{"title": "..."}`.
- Comment removals (59663, 57732):
  1. Take `content.raw`.
  2. Remove only the exact comment string.
  3. Confirm that is the only difference from the original.
  4. `POST /wp/v2/posts/<id>` with `{"content": "..."}`.
  5. Save the original `content.raw` locally first as a rollback copy.
- After each post, purge the LiteSpeed cache for that URL (LiteSpeed admin bar, or LiteSpeed Cache, then Toolbox, then Purge by URL). Then purge the Hostinger CDN cache.

## Step 5. Verify, then log
Re-crawl each URL without following redirects, adding a cache-buster query string. Confirm:
- `<title>` and the meta description match the approved values.
- Exactly one H1, and the canonical and robots meta are unchanged.
- 59663 and 57732: no `Paste into WordPress` left in the source.
- 57732: word count still about 4,950. Count with html.parser, not regex.

Mark each task Implementation VERIFIED or NOT VERIFIED, and Performance NOT YET ESTABLISHED.

Append a dated change log to `plans/boondockorbust-2026-10-gsc-action-plan.md` with the URL, field, old value, new value and timestamp. Commit and push to `claude/lucid-franklin-wjny5o`.

## Not in scope for this run
- Redirection plugin fixes (410s, the Walmart variant).
- The blackjack URL investigation.
- The UTV PDF noindex.
- The RV rental content section.

These stay queued in `plans/boondockorbust-HANDOFF.md`.
