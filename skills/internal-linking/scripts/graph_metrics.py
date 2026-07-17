#!/usr/bin/env python3
"""Graph metrics + link-deficit scoring for the internal-linking skill.

Implements sections 1-4 of reference/methodology.md: per-URL link metrics,
value/equity/deficit scores, and priority tiers. Donor assignment and
anchor selection (sections 5-6) are judgment steps done by the skill, not
this script.

Usage:
    python graph_metrics.py edges.csv \
        [--gsc-pages Pages.csv] [--gsc-queries Queries.csv] \
        [--priority-urls priority.txt] [--home https://www.example.com] \
        [--out metrics.csv]

edges.csv columns (from crawl_links.py or a mapped Sitebulb export):
    source,target,anchor,position[,status]
Pages.csv / Queries.csv: standard GSC "compare" exports (page/query,
clicks, ..., impressions, ..., position columns; extra columns ignored).
priority.txt: one money-page URL per line.

Output metrics.csv, one row per URL, sorted by deficit descending:
    url,inlinks_content,donor_count,depth,orphan,clicks_3mo,
    impressions_3mo,sd_impressions,money_page,value,equity,deficit,tier
Also prints orphans, depth>3 pages, and broken/redirected targets.
"""

import argparse
import csv
import math
import sys
from collections import defaultdict, deque
from urllib.parse import urlparse


def norm_url(u):
    u = u.strip().split("#")[0]
    return u.rstrip("/") if urlparse(u).path not in ("", "/") else u


def read_edges(path):
    edges = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = {k.lower().strip(): (v or "").strip() for k, v in row.items()}
            src, tgt = row.get("source"), row.get("target")
            if not src or not tgt:
                continue
            edges.append(
                {
                    "source": norm_url(src),
                    "target": norm_url(tgt),
                    "anchor": row.get("anchor", ""),
                    "position": row.get("position", "content").lower(),
                    "status": row.get("status", ""),
                }
            )
    return edges


def read_gsc(path, key_hint):
    """Return {url_or_query: (clicks, impressions, position)} for the
    'last 3 months' columns of a GSC compare export."""
    out = {}
    if not path:
        return out
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        cols = [h.lower() for h in header]

        def find(word):
            for i, h in enumerate(cols):
                if word in h and "last" in h.replace("same period last year", ""):
                    return i
            for i, h in enumerate(cols):  # non-compare export fallback
                if word in h and "same period" not in h:
                    return i
            return None

        ci, ii, pi = find("click"), find("impression"), find("position")
        for row in reader:
            if not row or not row[0]:
                continue
            key = norm_url(row[0]) if key_hint == "url" else row[0].strip().lower()

            def num(idx):
                if idx is None or idx >= len(row) or not row[idx]:
                    return 0.0
                return float(row[idx].replace(",", "").replace("%", ""))

            out[key] = (num(ci), num(ii), num(pi))
    return out


def minmax(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return lambda v: 0.0
    return lambda v: (v - lo) / (hi - lo)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("edges")
    ap.add_argument("--gsc-pages")
    ap.add_argument("--gsc-queries")
    ap.add_argument("--priority-urls")
    ap.add_argument("--home", help="Homepage URL for depth BFS (default: shortest-path URL in graph)")
    ap.add_argument("--out", default="metrics.csv")
    args = ap.parse_args()

    edges = read_edges(args.edges)
    if not edges:
        sys.exit("No edges parsed — check the CSV headers (source,target,anchor,position).")

    urls = sorted({e["source"] for e in edges} | {e["target"] for e in edges})
    content_pairs = {(e["source"], e["target"]) for e in edges if e["position"] == "content" and e["source"] != e["target"]}
    inlinks = defaultdict(set)
    for src, tgt in content_pairs:
        inlinks[tgt].add(src)

    adj = defaultdict(set)
    for e in edges:
        if e["source"] != e["target"]:
            adj[e["source"]].add(e["target"])

    home = norm_url(args.home) if args.home else min(
        urls, key=lambda u: (len(urlparse(u).path), u)
    )
    depth = {home: 0}
    dq = deque([home])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v not in depth:
                depth[v] = depth[u] + 1
                dq.append(v)

    pages = read_gsc(args.gsc_pages, "url")
    queries = read_gsc(args.gsc_queries, "query")
    # Striking-distance impressions can only be attributed per-page when the
    # user maps queries to pages; as a proxy, count SD impressions site-wide
    # and attribute via the Pages export position band (4-15).
    sd_by_page = {
        u: imp for u, (_, imp, pos) in pages.items() if 4 <= pos <= 15
    }
    sd_total = sum(imp for _, imp, pos in queries.values() if 4 <= pos <= 15 and imp >= 50)

    priority = set()
    if args.priority_urls:
        with open(args.priority_urls, encoding="utf-8-sig") as f:
            priority = {norm_url(l) for l in f if l.strip()}
    MONEY_HINTS = ("/practice-areas/", "/services/", "/products/", "/service/", "/product/")

    rows = []
    for u in urls:
        clicks, imps, _ = pages.get(u, (0.0, 0.0, 0.0))
        rows.append(
            {
                "url": u,
                "inlinks_content": len(inlinks[u]),
                "donor_count": len(inlinks[u]),
                "depth": depth.get(u, ""),
                "orphan": int(len(inlinks[u]) == 0 and u != home),
                "clicks_3mo": clicks,
                "impressions_3mo": imps,
                "sd_impressions": sd_by_page.get(u, 0.0),
                "money_page": int(u in priority or any(h in u for h in MONEY_HINTS)),
            }
        )

    has_gsc = bool(pages)
    n_imp = minmax([math.log1p(r["impressions_3mo"]) for r in rows])
    n_clk = minmax([math.log1p(r["clicks_3mo"]) for r in rows])
    n_sd = minmax([r["sd_impressions"] for r in rows])
    n_in = minmax([math.log1p(r["inlinks_content"]) for r in rows])
    n_don = minmax([math.log1p(r["donor_count"]) for r in rows])

    def depth_factor(d):
        if d == "":
            return 0.5  # unknown depth: neutral
        return {0: 1.0, 1: 1.0, 2: 0.6, 3: 0.3}.get(d, 0.0)

    for r in rows:
        if has_gsc:
            r["value"] = round(
                35 * n_imp(math.log1p(r["impressions_3mo"]))
                + 25 * n_clk(math.log1p(r["clicks_3mo"]))
                + 25 * n_sd(r["sd_impressions"])
                + 15 * r["money_page"],
                1,
            )
        else:
            r["value"] = round(60 * r["money_page"] + 40 * 0.5, 1)  # structural mode
        r["equity"] = round(
            60 * n_in(math.log1p(r["inlinks_content"]))
            + 25 * n_don(math.log1p(r["donor_count"]))
            + 15 * depth_factor(r["depth"]),
            1,
        )
        r["deficit"] = round(r["value"] - r["equity"], 1)
        if r["deficit"] >= 40 or (r["orphan"] and r["value"] >= 30):
            r["tier"] = "P1"
        elif r["deficit"] >= 20:
            r["tier"] = "P2"
        elif r["value"] >= 20 and (
            (isinstance(r["depth"], int) and r["depth"] > 3) or r["donor_count"] <= 1
        ):
            r["tier"] = "P3"
        else:
            r["tier"] = ""

    rows.sort(key=lambda r: -r["deficit"])
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    orphans = [r for r in rows if r["orphan"]]
    deep = [r for r in rows if isinstance(r["depth"], int) and r["depth"] > 3]
    broken = sorted(
        {e["target"] for e in edges if e["status"] and e["status"] not in ("200", "")}
    )
    print(f"{len(urls)} URLs, {len(content_pairs)} unique content links -> {args.out}")
    print(f"GSC data: {'yes' if has_gsc else 'NO — structural mode, note it in the deliverable'}")
    if sd_total:
        print(f"Site-wide striking-distance impressions (pos 4-15): {sd_total:.0f}")
    print(f"Orphans: {len(orphans)} | depth>3: {len(deep)} | non-200 link targets: {len(broken)}")
    for r in rows[:15]:
        print(f"  {r['tier'] or '--'} deficit {r['deficit']:>6} v{r['value']:>5} e{r['equity']:>5} {r['url']}")


if __name__ == "__main__":
    main()
