# gbp-optimization — citation sources & NAP rules

## Canonical NAP record

Locked with the client before the audit. Fields: legal display name (with
suffix policy decided — "LLP"/"LLC" in or out, applied consistently),
street address (suite format decided once, e.g. "Suite 200" vs "#200"),
local phone in one format (prefer the GBP primary number; note any call
tracking numbers — tracking numbers on citations are a common NAP breaker),
website URL (canonical protocol + www form).

## Matching rules (implemented in scripts/nap_compare.py)

- **Phone:** compare digits only; country code stripped. Any digit
  difference = MISMATCH (P1).
- **Address:** normalize case, punctuation, directionals (N/North),
  street suffixes (St/Street, Ave/Avenue), and suite markers
  (Ste/Suite/#). After normalization: different street number, street
  name, city, state, or ZIP = MISMATCH (P1); suite present vs absent =
  PARTIAL (P2); formatting-only differences = FORMAT (note, no action).
- **Name:** normalize case/punctuation/"&"-vs-"and"; legal-suffix
  presence = PARTIAL (P3) if otherwise identical; different name or
  added keywords = MISMATCH (P2 — and check whether it's an old brand or
  a stuffed variant).

## Core directories (check for every client)

1. Google Business Profile (the audit subject)
2. Apple Business Connect (Apple Maps)
3. Bing Places
4. Yelp
5. Facebook business page
6. Better Business Bureau
7. Yellow Pages (yellowpages.com)
8. Foursquare
9. Nextdoor

Plus the data aggregators that seed hundreds of long-tail directories —
worth checking/correcting once per client: Data Axle, Foursquare Places
(ex-Factual), Neustar Localeze.

## Vertical directories

**Legal:** Avvo, Justia, FindLaw, Martindale-Hubbell, Lawyers.com,
Super Lawyers, NOLO, state bar association profile.
**Medical/dental:** Healthgrades, Zocdoc, Vitals, WebMD, state licensing
board profile.
**Home services:** Angi, HomeAdvisor, Thumbtack, Houzz, Porch.
**Restaurants/hospitality:** TripAdvisor, OpenTable, DoorDash/UberEats
listings (NAP leaks from these are common).
**Other verticals:** search "[industry] directory" + "top [industry]
directories [year]" and audit the top 5 with real domain authority; skip
pay-to-play farms.

## Duplicate detection

Search each core directory for the business phone AND the street address
independently — duplicates usually carry an old phone or pre-move address.
Every live duplicate goes in the Citation Log with severity P1 and the
directory's merge/removal URL in the fix column.
