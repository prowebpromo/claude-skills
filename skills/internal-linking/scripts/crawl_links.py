#!/usr/bin/env python3
"""Fallback internal-link crawler for the internal-linking skill.

Builds an internal link edge list when no Sitebulb export is available.
Polite by design: respects robots.txt, stays on the target host (plus its
www/non-www twin), rate-limits, and caps page count.

Usage:
    pip install requests beautifulsoup4
    python crawl_links.py https://www.example.com \
        --max-pages 500 --delay 0.5 --out edges.csv

Output CSV columns:
    source,target,anchor,position,status
position is "content" or "boilerplate" (link found inside nav/header/
footer/aside/breadcrumb containers). status is the HTTP status of the
TARGET when it was fetched (blank if the target was never dequeued).
"""

import argparse
import csv
import sys
import time
import urllib.robotparser
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

BOILERPLATE_TAGS = {"nav", "header", "footer", "aside"}
BOILERPLATE_HINTS = ("breadcrumb", "menu", "footer", "header", "sidebar", "nav")
SKIP_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".pdf",
    ".zip", ".doc", ".docx", ".xls", ".xlsx", ".mp4", ".mp3", ".css", ".js",
)
UA = "internal-linking-skill-crawler/1.0 (site audit on behalf of site owner)"


def same_site(url, roots):
    host = urlparse(url).netloc.lower()
    return host in roots


def normalize(url):
    url, _ = urldefrag(url)
    return url.rstrip("/") if urlparse(url).path not in ("", "/") else url


def is_boilerplate(a_tag):
    for parent in a_tag.parents:
        if parent.name in BOILERPLATE_TAGS:
            return True
        attrs = " ".join(
            [str(parent.get("class", "")), str(parent.get("id", ""))]
        ).lower()
        if any(h in attrs for h in BOILERPLATE_HINTS):
            return True
    return False


def crawl(start, max_pages, delay, out_path):
    parsed = urlparse(start)
    host = parsed.netloc.lower()
    twin = host[4:] if host.startswith("www.") else "www." + host
    roots = {host, twin}

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{parsed.scheme}://{host}/robots.txt")
    try:
        rp.read()
    except Exception:
        pass  # unreadable robots.txt -> proceed, we are auditing owner's site

    session = requests.Session()
    session.headers["User-Agent"] = UA

    queue = deque([normalize(start)])
    seen = {normalize(start)}
    statuses = {}
    edges = []
    fetched = 0

    while queue and fetched < max_pages:
        url = queue.popleft()
        if not rp.can_fetch(UA, url):
            continue
        try:
            resp = session.get(url, timeout=15, allow_redirects=True)
        except requests.RequestException as e:
            print(f"  ! {url} — {e.__class__.__name__}", file=sys.stderr)
            statuses[url] = "error"
            continue
        fetched += 1
        statuses[url] = resp.status_code
        final_url = normalize(resp.url)
        if resp.status_code != 200 or "text/html" not in resp.headers.get(
            "Content-Type", ""
        ):
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            target = normalize(urljoin(final_url, a["href"]))
            if not target.startswith("http") or not same_site(target, roots):
                continue
            if target.lower().endswith(SKIP_EXTENSIONS):
                continue
            anchor = " ".join(a.get_text(" ", strip=True).split())[:200]
            position = "boilerplate" if is_boilerplate(a) else "content"
            edges.append((final_url, target, anchor, position))
            if target not in seen:
                seen.add(target)
                queue.append(target)

        if fetched % 25 == 0:
            print(f"  fetched {fetched} pages, {len(edges)} links…")
        time.sleep(delay)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target", "anchor", "position", "status"])
        for src, tgt, anchor, position in edges:
            w.writerow([src, tgt, anchor, position, statuses.get(tgt, "")])

    print(
        f"Done: {fetched} pages fetched, {len(edges)} internal links "
        f"-> {out_path}"
    )
    if fetched >= max_pages:
        print(
            "NOTE: page cap reached — the graph is partial. Raise "
            "--max-pages only with the site owner's OK."
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("start_url", help="Homepage URL, e.g. https://www.example.com")
    ap.add_argument("--max-pages", type=int, default=500)
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    ap.add_argument("--out", default="edges.csv")
    args = ap.parse_args()
    crawl(args.start_url, args.max_pages, args.delay, args.out)


if __name__ == "__main__":
    main()
