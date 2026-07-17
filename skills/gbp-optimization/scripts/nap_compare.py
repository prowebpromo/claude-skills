#!/usr/bin/env python3
"""NAP consistency checker for the gbp-optimization skill.

Compares every directory listing in citations.csv against the canonical
business record and emits a per-field mismatch report with severity, per
the matching rules in reference/citation_sources.md. Stdlib only.

Usage:
    python nap_compare.py citations.csv \
        --name "Dansker & Aspromonte Associates LLP" \
        --address "100 Broadway, Suite 200, New York, NY 10005" \
        --phone "(212) 555-0100" \
        [--out nap_report.csv]

citations.csv columns (extra columns pass through untouched):
    source,name,address,phone,url,status
Rows with status "missing" or "not checked" are reported as-is and not
diffed. Severity: P1 phone/address mismatch or duplicate, P2 partial
address (suite) or name mismatch, P3 name suffix only, FORMAT
formatting-only, OK exact after normalization.
"""

import argparse
import csv
import re
import sys

SUFFIXES = r"\b(llp|llc|pllc|pc|p\.c\.|inc|inc\.|ltd|co)\b"
STREET_ABBR = {
    "street": "st", "avenue": "ave", "boulevard": "blvd", "drive": "dr",
    "road": "rd", "lane": "ln", "court": "ct", "place": "pl",
    "parkway": "pkwy", "highway": "hwy", "square": "sq", "floor": "fl",
    "north": "n", "south": "s", "east": "e", "west": "w",
}
SUITE_MARKERS = r"\b(suite|ste|unit|apt|#)\s*\.?\s*"


def digits(phone):
    d = re.sub(r"\D", "", phone or "")
    return d[1:] if len(d) == 11 and d.startswith("1") else d


def norm_text(s):
    s = (s or "").lower().replace("&", "and")
    s = re.sub(r"[^\w\s#]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_name(s, strip_suffix=False):
    s = norm_text(s)
    if strip_suffix:
        s = re.sub(SUFFIXES, "", s).strip()
    return re.sub(r"\s+", " ", s)


def split_suite(addr):
    """Return (address_without_suite, suite_number_or_empty)."""
    m = re.search(SUITE_MARKERS + r"(\w+)", addr)
    if not m:
        return addr, ""
    base = (addr[: m.start()] + " " + addr[m.end():]).strip()
    return re.sub(r"\s+", " ", base), m.group(2)


def norm_address(s):
    s = norm_text(s)
    words = [STREET_ABBR.get(w, w) for w in s.split()]
    s = " ".join(words)
    return split_suite(s)


def compare(canon, row):
    """Return (severity, detail) for one listing vs the canonical record."""
    problems = []

    if digits(row.get("phone", "")) and digits(row["phone"]) != canon["phone_d"]:
        problems.append(("P1", "phone differs"))

    if (row.get("address") or "").strip():
        base, suite = norm_address(row["address"])
        if base != canon["addr_base"]:
            problems.append(("P1", "address differs"))
        elif suite != canon["addr_suite"]:
            problems.append(("P2", "suite missing/differs"))
        elif norm_text(row["address"]) != canon["addr_raw_norm"]:
            problems.append(("FORMAT", "address formatting variant"))

    name = row.get("name") or ""
    if name.strip():
        if norm_name(name) == canon["name_norm"]:
            pass
        elif norm_name(name, True) == canon["name_nosfx"]:
            problems.append(("P3", "legal suffix differs"))
        else:
            problems.append(("P2", "name differs"))

    if not problems:
        return "OK", "consistent"
    order = {"P1": 0, "P2": 1, "P3": 2, "FORMAT": 3}
    problems.sort(key=lambda p: order[p[0]])
    return problems[0][0], "; ".join(f"{sev}: {msg}" for sev, msg in problems)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("citations")
    ap.add_argument("--name", required=True)
    ap.add_argument("--address", required=True)
    ap.add_argument("--phone", required=True)
    ap.add_argument("--out", default="nap_report.csv")
    args = ap.parse_args()

    addr_base, addr_suite = norm_address(args.address)
    canon = {
        "phone_d": digits(args.phone),
        "addr_base": addr_base,
        "addr_suite": addr_suite,
        "addr_raw_norm": norm_text(args.address),
        "name_norm": norm_name(args.name),
        "name_nosfx": norm_name(args.name, True),
    }

    with open(args.citations, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [{k.lower().strip(): (v or "").strip() for k, v in r.items()} for r in reader]
    if not rows:
        sys.exit("citations.csv is empty")

    counts = {}
    for row in rows:
        status = (row.get("status") or "").lower()
        if status in ("missing", "not checked"):
            row["severity"], row["detail"] = status.upper(), "listing " + status
        elif status == "duplicate":
            row["severity"], row["detail"] = "P1", "duplicate listing — merge/remove"
        else:
            row["severity"], row["detail"] = compare(canon, row)
        counts[row["severity"]] = counts.get(row["severity"], 0) + 1

    fields = list(rows[0].keys())
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} listings -> {args.out}")
    for sev in ("P1", "P2", "P3", "FORMAT", "MISSING", "NOT CHECKED", "OK"):
        if sev in counts:
            print(f"  {sev:12} {counts[sev]}")
    for row in rows:
        if row["severity"] in ("P1", "P2"):
            print(f"  {row['severity']} {row.get('source', '?'):20} {row['detail']}")


if __name__ == "__main__":
    main()
