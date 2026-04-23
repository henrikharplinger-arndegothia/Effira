#!/usr/bin/env python3
"""
Enrich Bad & Värme stores with allabolag data.
Fetches: org number, employees, VD name/role.
Output: bv_stores_final.json
"""

import json, csv, re, time, urllib.parse, urllib.request
from collections import Counter

IN_JSON  = "/Users/henrikharplinger/dev/bv-scrape/bv_stores.json"
OUT_JSON = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_final.json"
OUT_CSV  = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_final.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv,en;q=0.5",
}

STOP_WORDS = {"ab", "i", "och", "rör", "vvs", "el", "värme", "bad", "sanitet",
              "service", "teknik", "energi", "installationer", "installation",
              "&", "-", "af", "as", "oy", "kb", "varme"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_next_data(html):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>',
                  html, re.DOTALL)
    return json.loads(m.group(1)) if m else None


def search_companies(name, city=None):
    q = urllib.parse.quote(name)
    url = (f"https://www.allabolag.se/what/{q}/where/{urllib.parse.quote(city)}"
           if city else f"https://www.allabolag.se/what/{q}")
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
    tokens = re.split(r'[\s,.\-/]+', name.lower())
    return {t for t in tokens if t and t not in STOP_WORDS and len(t) > 1}


def score_match(a, b):
    sa, sb = name_tokens(a), name_tokens(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(len(sa), len(sb))


def best_match(store_name, companies, min_score=0.35):
    best, best_score = None, 0.0
    for comp in companies:
        sc = score_match(store_name, comp.get("name") or "")
        if sc > best_score:
            best_score, best = sc, comp
    return (best, best_score) if best_score >= min_score else (None, best_score)


def extract_fields(company):
    if not company:
        return {}
    cp = company.get("contactPerson") or {}
    return {
        "abo_orgnr":     company.get("orgnr") or "",
        "abo_employees": company.get("employees") or "",
        "abo_vd_name":   cp.get("name") or "",
        "abo_vd_role":   cp.get("role") or "",
    }


def main():
    stores = json.load(open(IN_JSON, encoding="utf-8"))
    print(f"Enriching {len(stores)} stores via allabolag...\n")

    results = []
    for i, store in enumerate(stores, 1):
        name = store.get("name") or ""
        city = store.get("city") or ""
        print(f"[{i}/{len(stores)}] {name} | {city}")

        # Strategy 1: name + city
        candidates = search_companies(name, city)
        matched, score = best_match(name, candidates)
        time.sleep(0.5)

        # Strategy 2: name only
        if not matched or score < 0.45:
            candidates2 = search_companies(name)
            matched2, score2 = best_match(name, candidates2)
            time.sleep(0.5)
            if score2 > score:
                matched, score = matched2, score2

        # Strategy 3: strip city from name
        if not matched or score < 0.45:
            stripped = re.sub(r'\s+' + re.escape(city) + r'\s*$', '', name,
                              flags=re.IGNORECASE).strip()
            if stripped != name:
                candidates3 = search_companies(stripped, city)
                matched3, score3 = best_match(stripped, candidates3)
                time.sleep(0.5)
                if score3 > score:
                    matched, score = matched3, score3

        fields = extract_fields(matched)
        confidence = ("ok" if score >= 0.6 else
                      "low" if score >= 0.35 else "unresolved")

        if matched:
            print(f"  ✓ {matched.get('name')}  score={score:.2f}  "
                  f"orgnr={fields.get('abo_orgnr')}  emp={fields.get('abo_employees')}")
        else:
            print(f"  ✗ unresolved  best={score:.2f}")

        row = {
            **store,
            **fields,
            "contact_email": store.get("email") or "",
            "contact_phone": store.get("phone") or "",
            "confidence": confidence,
        }
        results.append(row)

    # Save
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    if results:
        fieldnames = list(results[0].keys())
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in results:
                flat = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
                        for k, v in row.items()}
                w.writerow(flat)

    conf = Counter(r.get("confidence") for r in results)
    print(f"\nDone. ok={conf['ok']}  low={conf['low']}  unresolved={conf['unresolved']}")
    print(f"Saved → {OUT_JSON}")


if __name__ == "__main__":
    main()
