#!/usr/bin/env python3
"""
Targeted resolution for the 22 unresolved stores.

Strategy:
1. Multi-location brands (Storfors Plåt, Ternstedt, Infjärdens Värme):
   search by brand name only, pick the right entity
2. Others: try (a) email domain as search query, (b) phone match across results,
   (c) stripped/simplified name
"""

import json, re, time, urllib.request, urllib.parse

FINAL_JSON  = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.json"
OUTPUT_JSON = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.json"
OUTPUT_CSV  = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")

def extract_companies(html):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html, re.DOTALL)
    if not m: return []
    data = json.loads(m.group(1))
    try: return data["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"]["companies"] or []
    except: return []

def get_company(orgnr):
    html = fetch(f"https://www.allabolag.se/{orgnr}")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html, re.DOTALL)
    if not m: return None
    data = json.loads(m.group(1))
    try: return data["props"]["pageProps"]["company"]
    except: return None

def norm_phone(p):
    return re.sub(r"[^0-9]", "", p or "")

def search(name, city=None):
    q = urllib.parse.quote(name)
    url = (f"https://www.allabolag.se/what/{q}/where/{urllib.parse.quote(city)}"
           if city else f"https://www.allabolag.se/what/{q}")
    try:
        return extract_companies(fetch(url))
    except Exception as e:
        print(f"    search error: {e}")
        return []

def find_by_phone(candidates, target_phone):
    tp = norm_phone(target_phone)
    if not tp: return None
    for c in candidates:
        for field in ("phone", "phone2", "mobile", "mobile2"):
            if norm_phone(c.get(field) or "") == tp:
                return c
    return None

def extract_fields(company):
    if not company: return {}
    cp = company.get("contactPerson") or {}
    return {
        "abo_orgnr":     company.get("orgnr") or "",
        "abo_employees": company.get("employees") or "",
        "abo_vd_name":   cp.get("name") or "",
        "abo_vd_role":   cp.get("role") or "",
    }

def resolve(name, city, phone, email):
    """Try multiple strategies, return (company, method) or (None, 'failed')."""
    domain = email.split("@")[1].split(".")[0] if "@" in email else ""

    # Strategy 1: phone match - search by name+city, then name-only
    for q, c in [(name, city), (name, None)]:
        candidates = search(q, c)
        time.sleep(0.4)
        match = find_by_phone(candidates, phone)
        if match:
            return match, f"phone-match ({q})"

    # Strategy 2: search by email domain (more specific than brand name)
    if domain and len(domain) > 4:
        candidates = search(domain, city)
        time.sleep(0.4)
        if candidates:
            # First try phone match
            match = find_by_phone(candidates, phone)
            if match:
                return match, "phone-match (domain)"
            # Then take first result if it looks plausible
            if len(candidates) == 1:
                return candidates[0], "domain-single-result"

    # Strategy 3: try without city suffixes in name
    stripped = re.sub(r'\s+' + re.escape(city) + r'\s*$', '', name, flags=re.IGNORECASE).strip()
    stripped = re.sub(r'\s*[-–]\s*\w+$', '', stripped).strip()  # remove " - Linköping" suffix
    if stripped != name and len(stripped) > 4:
        candidates = search(stripped, city)
        time.sleep(0.4)
        match = find_by_phone(candidates, phone)
        if match:
            return match, f"phone-match (stripped: {stripped})"
        if candidates and len(candidates) <= 3:
            # small result set - take best name match
            best = max(candidates, key=lambda c: len(set(stripped.lower().split()) & set((c.get('name') or '').lower().split())))
            if best:
                return best, f"stripped-best ({stripped})"

    return None, "failed"


# ---- KNOWN PARENT COMPANIES (multi-location branches) ----
# These share one legal entity; verified by finding the parent org.
KNOWN = {
    # Storfors Plåtslageri AB - confirmed parent for all Storfors Plåt locations
    "Storfors Plåt Arvidsjaur":     "5560849795",
    "Storfors Plåt Boden":          "5560849795",
    "Storfors Plåt Luleå":          "5560849795",
    "Storfors Plåt Lycksele":       "5560849795",
    "Storfors Plåt Piteå":          "5560849795",
    "Storfors Plåt Skellefteå":     "5560849795",
}


def main():
    import csv
    stores = json.load(open(FINAL_JSON, encoding="utf-8"))
    unresolved = [s for s in stores if s["confidence"] == "unresolved"]
    print(f"Unresolved: {len(unresolved)}")

    resolved_map = {}  # store name -> fields

    # Pre-fetch known parent companies
    known_cache = {}
    for orgnr in set(KNOWN.values()):
        print(f"Fetching known parent {orgnr}...")
        comp = get_company(orgnr)
        known_cache[orgnr] = comp
        time.sleep(0.5)

    for store in unresolved:
        name  = store["name"]
        city  = store["city"]
        phone = store.get("contact_phone") or ""
        email = store.get("contact_email") or ""

        print(f"\n--- {name} | {city}")

        # Known parent?
        if name in KNOWN:
            orgnr = KNOWN[name]
            comp  = known_cache.get(orgnr)
            fields = extract_fields(comp)
            fields["confidence"] = "low"   # branch office, not exact legal match
            resolved_map[name] = fields
            print(f"    -> KNOWN PARENT {orgnr} | emp={fields.get('abo_employees')} | vd={fields.get('abo_vd_name')}")
            continue

        # Auto-resolve
        comp, method = resolve(name, city, phone, email)
        if comp:
            fields = extract_fields(comp)
            fields["confidence"] = "ok" if "phone-match" in method else "low"
            resolved_map[name] = fields
            print(f"    -> {method} | orgnr={fields['abo_orgnr']} | emp={fields['abo_employees']} | vd={fields['abo_vd_name']}")
        else:
            resolved_map[name] = {"confidence": "unresolved"}
            print(f"    -> still unresolved")

    # Patch stores
    for store in stores:
        if store["name"] in resolved_map:
            patch = resolved_map[store["name"]]
            store.update(patch)

    # Save
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(stores, f, indent=2, ensure_ascii=False)

    fieldnames = list(stores[0].keys())
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in stores:
            flat = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                    for k, v in row.items()}
            w.writerow(flat)

    from collections import Counter
    conf = Counter(s.get("confidence") for s in stores)
    still = [s["name"] for s in stores if s.get("confidence") == "unresolved"]
    print(f"\n--- Final ---")
    print(f"ok={conf['ok']}  low={conf['low']}  unresolved={conf['unresolved']}")
    if still:
        print("Still unresolved:")
        for n in still:
            print(f"  {n}")


if __name__ == "__main__":
    main()
