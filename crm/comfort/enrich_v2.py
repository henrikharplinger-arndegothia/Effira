#!/usr/bin/env python3
"""
Pass 2: clean + re-resolve duplicate org numbers.

Changes vs v1:
- comfort.se email/phone are kept as primary contact fields
- allabolag data used only for employees + VD
- duplicate-orgnr stores retried with stricter name matching
- confidence flag: 'ok' | 'low' | 'unresolved'
"""

import json
import csv
import time
import re
import urllib.parse
import urllib.request
from collections import Counter

ENRICHED_JSON   = "/Users/henrikharplinger/dev/comfort-scrape/stores_enriched.json"
OUTPUT_JSON     = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.json"
OUTPUT_CSV      = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv,en;q=0.5",
}

STOP_WORDS = {"ab", "i", "och", "rör", "vvs", "el", "värme", "comfort", "sanitet",
              "service", "teknik", "energia", "energi", "installationer", "installation",
              "&", "-", "af", "as", "oy", "kb"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_next_data(html):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>',
                  html, re.DOTALL)
    return json.loads(m.group(1)) if m else None


def search_companies(name, city=None):
    """Return list of company dicts from allabolag search."""
    q_name = urllib.parse.quote(name)
    if city:
        url = f"https://www.allabolag.se/what/{q_name}/where/{urllib.parse.quote(city)}"
    else:
        url = f"https://www.allabolag.se/what/{q_name}"
    try:
        html = fetch(url)
    except Exception as e:
        print(f"    fetch error: {e}")
        return []
    data = extract_next_data(html)
    if not data:
        return []
    try:
        return data["props"]["pageProps"]["hydrationData"]["searchStore"]["companies"]["companies"] or []
    except (KeyError, TypeError):
        return []


def name_tokens(name):
    """Meaningful lowercased tokens from a company name."""
    tokens = re.split(r'[\s,.\-/]+', name.lower())
    return {t for t in tokens if t and t not in STOP_WORDS and len(t) > 1}


def score_match(store_name, candidate_name):
    """0.0-1.0 overlap score between store name and allabolag candidate name."""
    s = name_tokens(store_name)
    c = name_tokens(candidate_name)
    if not s or not c:
        return 0.0
    overlap = s & c
    return len(overlap) / max(len(s), len(c))


def best_match(store_name, companies, min_score=0.35):
    """Return (company, score) for the best name match, or (None, 0)."""
    best, best_score = None, 0.0
    for comp in companies:
        sc = score_match(store_name, comp.get("name") or "")
        if sc > best_score:
            best_score = sc
            best = comp
    if best_score >= min_score:
        return best, best_score
    return None, best_score


def extract_fields(company):
    if not company:
        return {}
    cp = company.get("contactPerson") or {}
    return {
        "abo_orgnr":    company.get("orgnr") or "",
        "abo_employees": company.get("employees") or "",
        "abo_vd_name":  cp.get("name") or "",
        "abo_vd_role":  cp.get("role") or "",
    }


def main():
    stores = json.load(open(ENRICHED_JSON, encoding="utf-8"))

    # Which org numbers are duplicated?
    orgnr_counts = Counter(s["abo_orgnr"] for s in stores if s.get("abo_orgnr"))
    dup_orgnrs   = {k for k, v in orgnr_counts.items() if v > 1}
    print(f"Stores with duplicate org numbers: "
          f"{sum(1 for s in stores if s.get('abo_orgnr') in dup_orgnrs)} "
          f"across {len(dup_orgnrs)} org numbers\n")

    results = []

    for i, store in enumerate(stores, 1):
        name      = store.get("name") or ""
        city      = store.get("city") or ""
        orgnr     = store.get("abo_orgnr") or ""
        is_dup    = orgnr in dup_orgnrs

        # --- Part A: use comfort.se contact as primary ---
        primary_email = store.get("email") or ""
        primary_phone = store.get("phone_number") or ""

        row = {k: v for k, v in store.items()}

        # Remove old allabolag contact fields — keep only VD + employees
        for k in ("abo_email", "abo_phone"):
            row.pop(k, None)

        # Set primary contact
        row["contact_email"] = primary_email
        row["contact_phone"] = primary_phone

        if not is_dup:
            row["confidence"] = "ok"
            results.append(row)
            continue

        # --- Part B: re-resolve duplicate org numbers ---
        print(f"[{i}/{len(stores)}] RE-RESOLVING: {name} | {city}")

        # Strategy 1: name + city, pick best scoring match
        candidates = search_companies(name, city)
        matched, score = best_match(name, candidates)
        time.sleep(0.5)

        # Strategy 2: if no good match, try without city
        if not matched or score < 0.45:
            candidates2 = search_companies(name)
            matched2, score2 = best_match(name, candidates2)
            time.sleep(0.5)
            if score2 > score:
                matched, score = matched2, score2

        # Strategy 3: strip trailing city name from store name and retry
        if not matched or score < 0.45:
            stripped = re.sub(r'\s+' + re.escape(city) + r'\s*$', '', name, flags=re.IGNORECASE).strip()
            if stripped != name:
                candidates3 = search_companies(stripped, city)
                matched3, score3 = best_match(stripped, candidates3)
                time.sleep(0.5)
                if score3 > score:
                    matched, score = matched3, score3

        if matched:
            new_orgnr = matched.get("orgnr") or ""
            fields = extract_fields(matched)
            row.update(fields)
            if new_orgnr != orgnr:
                print(f"    ✓ re-matched  score={score:.2f}  new_orgnr={new_orgnr}  "
                      f"vd={fields.get('abo_vd_name')}  emp={fields.get('abo_employees')}")
                row["confidence"] = "ok" if score >= 0.6 else "low"
            else:
                print(f"    ~ same orgnr  score={score:.2f}  (may still be correct group match)")
                row["confidence"] = "low"
        else:
            print(f"    ✗ unresolved  best_score={score:.2f}")
            row["confidence"] = "unresolved"

        results.append(row)

    # --- Save ---
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    if results:
        fieldnames = list(results[0].keys())
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in results:
                flat = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                        for k, v in row.items()}
                w.writerow(flat)

    conf = Counter(r.get("confidence") for r in results)
    print(f"\n--- Done ---")
    print(f"ok={conf['ok']}  low={conf['low']}  unresolved={conf['unresolved']}")
    print(f"Saved to {OUTPUT_JSON} and {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
