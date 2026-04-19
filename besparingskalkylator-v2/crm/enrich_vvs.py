#!/usr/bin/env python3
"""Enrich VVS company list with data from Allabolag.se"""

import csv
import json
import re
import time
import urllib.parse
import urllib.request
import openpyxl
from difflib import SequenceMatcher

EXCEL_PATH = "/Users/HHARPLIN/Downloads/VVS lista på ÅF med god omsättning..xlsx"
OUTPUT_PATH = "/Users/HHARPLIN/dev/Effira/crm/vvs-enriched.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_allabolag(company_name):
    url = f"https://www.allabolag.se/what/{urllib.parse.quote(company_name)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None, str(e)

    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', data, re.DOTALL)
    if not m:
        return None, "no __NEXT_DATA__"
    try:
        j = json.loads(m.group(1))
    except Exception as e:
        return None, f"json parse error: {e}"

    try:
        companies = j["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"]["companies"]
    except (KeyError, TypeError):
        return None, "path not found"

    if not companies:
        return None, "empty results"

    # Score candidates: fuzzy name match + prefer higher revenue
    best = None
    best_score = -1
    for c in companies:
        name = c.get("name", "")
        score = similarity(company_name, name)
        # Boost score if revenue available (to break ties)
        rev_str = c.get("revenue", "") or ""
        rev_boost = 0.01 if rev_str.strip() else 0
        total = score + rev_boost
        if total > best_score:
            best_score = total
            best = c

    return best, None

def extract(company):
    if not company:
        return {k: "" for k in ["revenue", "employees", "email", "phone",
                                  "county", "municipality", "city", "zip",
                                  "contact_person", "contact_role"]}
    loc = company.get("location") or {}
    addr = company.get("visitorAddress") or {}
    cp = company.get("contactPerson") or {}
    return {
        "revenue": company.get("revenue") or "",
        "employees": company.get("employees") or "",
        "email": company.get("email") or "",
        "phone": company.get("phone") or "",
        "county": loc.get("county") or "",
        "municipality": loc.get("municipality") or "",
        "city": addr.get("postPlace") or "",
        "zip": addr.get("zipCode") or "",
        "contact_person": cp.get("name") or "",
        "contact_role": cp.get("role") or "",
    }

def main():
    # Load Excel
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    header_row = rows[0]
    print(f"Columns: {header_row}")

    # Find column indices
    cols = {str(h).strip() if h else "": i for i, h in enumerate(header_row)}
    print(f"Column map: {cols}")

    data_rows = rows[1:]
    total = len(data_rows)
    print(f"Total companies: {total}")

    results = []
    had_revenue = 0
    had_email = 0
    county_dist = {}

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Företagsnamn", "Geografi_original", "Landskap_original",
            "Revenue_SEK", "Employees", "Email", "Phone",
            "County", "Municipality", "City", "ZipCode",
            "ContactPerson", "ContactRole"
        ])
        writer.writeheader()

        for i, row in enumerate(data_rows):
            def cell(col_name):
                idx = cols.get(col_name)
                if idx is None:
                    return ""
                v = row[idx]
                return str(v).strip() if v is not None else ""

            company_name = cell("Företagsnamn")
            geografi = cell("Geografi")
            landskap = cell("Landskap")

            if not company_name:
                continue

            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{total} | Revenue found: {had_revenue} | Email found: {had_email}")

            best, err = search_allabolag(company_name)
            if err and not best:
                # silently continue with empty data
                pass

            info = extract(best)

            if info["revenue"]:
                had_revenue += 1
            if info["email"]:
                had_email += 1
            county = info["county"]
            if county:
                county_dist[county] = county_dist.get(county, 0) + 1

            writer.writerow({
                "Företagsnamn": company_name,
                "Geografi_original": geografi,
                "Landskap_original": landskap,
                "Revenue_SEK": info["revenue"],
                "Employees": info["employees"],
                "Email": info["email"],
                "Phone": info["phone"],
                "County": info["county"],
                "Municipality": info["municipality"],
                "City": info["city"],
                "ZipCode": info["zip"],
                "ContactPerson": info["contact_person"],
                "ContactRole": info["contact_role"],
            })
            f.flush()

            time.sleep(0.5)

    print(f"\n=== SUMMARY ===")
    print(f"Total companies processed: {total}")
    print(f"Had revenue data:          {had_revenue} ({100*had_revenue//total}%)")
    print(f"Had email data:            {had_email} ({100*had_email//total}%)")
    print(f"\nGeographic distribution by county:")
    for county, count in sorted(county_dist.items(), key=lambda x: -x[1]):
        print(f"  {county}: {count}")
    print(f"\nOutput saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
