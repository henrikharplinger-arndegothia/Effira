#!/usr/bin/env python3
"""
Enrich comfort.se store list with allabolag.se data:
- Number of employees
- VD (CEO) name
- Contact email
- Contact phone
"""

import json
import csv
import time
import re
import urllib.parse
import urllib.request

STORES_JSON = "/Users/henrikharplinger/dev/comfort-scrape/stores.json"
OUTPUT_JSON = "/Users/henrikharplinger/dev/comfort-scrape/stores_enriched.json"
OUTPUT_CSV  = "/Users/henrikharplinger/dev/comfort-scrape/stores_enriched.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sv,en;q=0.5",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_next_data(html):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html, re.DOTALL)
    if not m:
        return None
    return json.loads(m.group(1))


def search_company(name, city):
    """Search allabolag.se and return the best-matching company dict, or None."""
    q_name = urllib.parse.quote(name)
    q_city = urllib.parse.quote(city)
    url = f"https://www.allabolag.se/what/{q_name}/where/{q_city}"
    try:
        html = fetch(url)
    except Exception as e:
        print(f"    Search error ({name}): {e}")
        return None

    data = extract_next_data(html)
    if not data:
        return None

    try:
        companies = data["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"]["companies"]
    except (KeyError, TypeError):
        return None

    if not companies:
        # Try without city
        url2 = f"https://www.allabolag.se/what/{q_name}"
        try:
            html2 = fetch(url2)
            data2 = extract_next_data(html2)
            companies = data2["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"]["companies"]
        except Exception:
            return None

    if not companies:
        return None

    # Prefer exact name match (case-insensitive)
    name_lower = name.lower()
    for c in companies:
        cname = (c.get("name") or "").lower()
        if cname == name_lower or cname.replace(" aktiebolag", " ab") == name_lower.replace(" aktiebolag", " ab"):
            return c

    # Fuzzy: name contains match
    for c in companies:
        cname = (c.get("name") or "").lower()
        if name_lower in cname or cname in name_lower:
            return c

    # Fall back to first result
    return companies[0]


def get_company_page(orgnr):
    """Fetch full company page — sometimes has more detail than search result."""
    url = f"https://www.allabolag.se/{orgnr}"
    try:
        html = fetch(url)
    except Exception as e:
        print(f"    Page error ({orgnr}): {e}")
        return None
    data = extract_next_data(html)
    if not data:
        return None
    try:
        return data["props"]["pageProps"]["company"]
    except (KeyError, TypeError):
        return None


def extract_fields(company):
    if not company:
        return {}

    cp = company.get("contactPerson") or {}
    vd_name = cp.get("name", "")
    vd_role = cp.get("role", "")

    email = company.get("email") or ""
    phone = company.get("phone") or company.get("phone2") or company.get("mobile") or ""
    employees = company.get("employees") or ""
    orgnr = company.get("orgnr") or ""

    return {
        "abo_orgnr": orgnr,
        "abo_employees": employees,
        "abo_vd_name": vd_name,
        "abo_vd_role": vd_role,
        "abo_email": email,
        "abo_phone": phone,
    }


def main():
    with open(STORES_JSON, encoding="utf-8") as f:
        stores = json.load(f)

    enriched = []
    total = len(stores)

    for i, store in enumerate(stores, 1):
        name = store.get("name", "")
        city = store.get("city", "")
        print(f"[{i}/{total}] {name} | {city}")

        company = search_company(name, city)

        # If search result has employees/contactPerson already, use it directly
        abo = extract_fields(company)

        # If we got an orgnr but no employees, fetch full page
        if abo.get("abo_orgnr") and not abo.get("abo_employees"):
            time.sleep(0.3)
            full = get_company_page(abo["abo_orgnr"])
            if full:
                abo = extract_fields(full)

        if abo:
            print(f"    -> {abo.get('abo_orgnr')} | employees={abo.get('abo_employees')} | vd={abo.get('abo_vd_name')} | email={abo.get('abo_email')} | phone={abo.get('abo_phone')}")
        else:
            print(f"    -> NOT FOUND")

        enriched.append({**store, **abo})
        time.sleep(0.6)  # be polite

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    # Save CSV
    if enriched:
        fieldnames = list(enriched[0].keys())
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in enriched:
                flat = {}
                for k, v in row.items():
                    if isinstance(v, (dict, list)):
                        flat[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        flat[k] = v
                w.writerow(flat)

    found = sum(1 for r in enriched if r.get("abo_orgnr"))
    print(f"\nDone. {found}/{total} stores matched on allabolag.se")
    print(f"Saved to {OUTPUT_JSON} and {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
