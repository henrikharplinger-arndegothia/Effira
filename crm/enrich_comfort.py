#!/usr/bin/env python3
"""Enrich Comfort-network VVS companies with financial data from Allabolag.se."""

import csv
import json
import re
import time
import urllib.request
from pathlib import Path

import openpyxl

XLSX = "/Users/HHARPLIN/Downloads/Uppdat_ Distributionslista K4 2019_15000 ex 153 Adresser extra..xlsx"
SHEET = "Medlemsregister Bilaga 1"
OUT = Path("/Users/HHARPLIN/dev/Effira/crm/comfort-enriched.csv")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch_allabolag(orgnr: str) -> dict:
    """Fetch financial data for org number from Allabolag."""
    url = f"https://www.allabolag.se/what/{orgnr}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [ERR] fetch {orgnr}: {e}")
        return {}

    m = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>',
        data,
        re.DOTALL,
    )
    if not m:
        print(f"  [WARN] No __NEXT_DATA__ for {orgnr}")
        return {}

    try:
        nd = json.loads(m.group(1))
        companies = (
            nd["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"][
                "companies"
            ]
        )
    except (KeyError, json.JSONDecodeError) as e:
        print(f"  [WARN] Parse error {orgnr}: {e}")
        return {}

    if not companies:
        print(f"  [WARN] No companies in result for {orgnr}")
        return {}

    c = companies[0]
    revenue_raw = c.get("revenue", "") or ""
    try:
        revenue_msek = round(float(revenue_raw) / 1000, 1) if revenue_raw else ""
    except (ValueError, TypeError):
        revenue_msek = ""

    return {
        "Revenue_MSEK": revenue_msek,
        "Employees": c.get("employees", "") or "",
        "County": (c.get("location") or {}).get("county", "") or "",
        "Municipality": (c.get("location") or {}).get("municipality", "") or "",
        "City": ((c.get("visitorAddress") or {}).get("postPlace", "") or ""),
        "ZipCode": ((c.get("visitorAddress") or {}).get("zipCode", "") or ""),
    }


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    ws = wb[SHEET]
    rows = list(ws.iter_rows(values_only=True))
    data_rows = rows[1:]  # skip header

    OUT.parent.mkdir(parents=True, exist_ok=True)

    results = []
    total = len(data_rows)

    for i, row in enumerate(data_rows, 1):
        name = str(row[4]).strip() if row[4] else ""
        contact = str(row[6]).strip() if row[6] else ""
        city = str(row[9]).strip() if row[9] else ""
        email = str(row[14]).strip() if row[14] else ""
        orgnr = str(row[18]).strip() if row[18] else ""
        butik = str(row[19]).strip() if row[19] else ""
        foretagstyp = str(row[20]).strip() if row[20] else ""
        comfort = str(row[22]).strip() if row[22] else ""

        print(f"[{i:3}/{total}] {name or '(empty)'} | OrgNr: {orgnr or 'N/A'}")

        enriched = {}
        if orgnr and orgnr != "None":
            enriched = fetch_allabolag(orgnr)
            time.sleep(0.5)

        results.append(
            {
                "Företagsnamn": name,
                "Kontakt": contact,
                "Ort": city,
                "Email": email,
                "OrgNr": orgnr if orgnr != "None" else "",
                "Butik": butik if butik != "None" else "",
                "Företagstyp": foretagstyp if foretagstyp != "None" else "",
                "Comfortverksamhet": comfort if comfort != "None" else "",
                "Revenue_MSEK": enriched.get("Revenue_MSEK", ""),
                "Employees": enriched.get("Employees", ""),
                "County": enriched.get("County", ""),
                "Municipality": enriched.get("Municipality", ""),
            }
        )

    # Write CSV
    fieldnames = [
        "Företagsnamn", "Kontakt", "Ort", "Email", "OrgNr",
        "Butik", "Företagstyp", "Comfortverksamhet",
        "Revenue_MSEK", "Employees", "County", "Municipality",
    ]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Saved {len(results)} rows → {OUT}")

    # --- Summary ---
    with_revenue = [r for r in results if r["Revenue_MSEK"] != ""]
    print(f"\n📊 Revenue data available: {len(with_revenue)}/{len(results)}")

    print("\n🏆 Top 20 by Revenue_MSEK:")
    sorted_rev = sorted(with_revenue, key=lambda r: float(r["Revenue_MSEK"]), reverse=True)
    print(f"{'Company':<40} {'City':<20} {'Revenue (MSEK)':>14} {'Employees':>10}")
    print("-" * 90)
    for r in sorted_rev[:20]:
        print(
            f"{r['Företagsnamn']:<40} {r['Ort']:<20} "
            f"{r['Revenue_MSEK']:>14} {str(r['Employees']):>10}"
        )

    # County spread
    county_counts: dict = {}
    for r in results:
        c = r["County"] or "(unknown)"
        county_counts[c] = county_counts.get(c, 0) + 1
    print("\n🗺️  Geographic spread by county:")
    for county, count in sorted(county_counts.items(), key=lambda x: -x[1]):
        print(f"  {county:<30} {count}")


if __name__ == "__main__":
    main()
