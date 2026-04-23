#!/usr/bin/env python3
"""
Score and rank Bad & Värme stores for Effira OPTi lead attractiveness.

Scoring:
  A) SE electricity zone     (multiplier)
  B) Service profile         (points — brands, solar, ev)
  C) Company size            (multiplier)
  D) Revenue                 (points — from allabolag)
"""

import json, csv, re, time, urllib.request

FINAL_JSON  = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_final.json"
SCORED_JSON = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_scored.json"
SCORED_CSV  = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_scored.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# ── A. SE electricity zone ────────────────────────────────────────────────────
SE_ZONE = {
    "Arjeplog":1,"Arvidsjaur":1,"Boden":1,"Haparanda":1,"Kalix":1,
    "Luleå":1,"Öjebyn":1,"Piteå":1,
    "Bollnäs":2,"Borlänge":2,"Gävle":2,"Holmsund":2,"Hudiksvall":2,
    "Härnösand":2,"Kramfors":2,"Lima":2,"Linghed":2,"Ljusdal":2,
    "Lycksele":2,"Malå":2,"Malung":2,"Mora":2,"Östersund":2,
    "Sandviken":2,"Skellefteå":2,"Sollefteå":2,"Söderhamn":2,
    "Storvik":2,"Sundsvall":2,"Tärnaby":2,"Umeå":2,"Vemdalen":2,
    "Vindeln":2,"Arnäsvall":2,
    "Asarum":4,"Falkenberg":4,"Färjestaden":4,"Halmstad":4,
    "Helsingborg":4,"Hässleholm":4,"Kalmar":4,"Kristianstad":4,
    "Kungsbacka":4,"Landskrona":4,"Limhamn":4,"Ljungby":4,
    "Löttorp":4,"Malmö":4,"Mönsterås":4,"Mörbylånga":4,
    "Olofström":4,"Osby":4,"Oskarshamn":4,"Sjöbo":4,
    "Svedala":4,"Trelleborg":4,"Varberg":4,"Visby":4,
    "Västervik":4,"Åseda":4,
}
SE_MULT = {1: 0.60, 2: 0.78, 3: 1.00, 4: 1.28}

def get_zone(city):
    return SE_ZONE.get(city, 3)


# ── B. Service/brand scoring ──────────────────────────────────────────────────
# Bad & Värme are ALL VVS/heating specialists — so base score is already high.
# Differentiate on: authorized brands (water-circuit VP), solar, energy calc.
WATER_BRANDS = {"nibe", "bosch", "ivt", "ctc", "thermia"}   # water-circuit heat pumps
COOL_BRANDS  = {"mitsubishi", "daikin", "panasonic"}          # air-air, lower OPTi fit

def services_score(services, brands):
    svcs = set(services or [])
    brds = set(b.lower() for b in (brands or []))

    score = 0

    # All BV stores do heating/VVS — give base point for being in the chain
    score += 2

    # Authorized for water-circuit brands → OPTi-compatible customers
    water_brand_count = len(brds & WATER_BRANDS)
    score += min(water_brand_count, 2)   # +1 per brand, max 2

    # Solar → energy-aware customers, stronger OPTi pitch
    if "solar" in svcs:
        score += 1

    # EV charging → modern/premium installer
    if "ev_charging" in svcs:
        score += 1

    # Energie calculation service → already selling energy optimization
    if "energiopt" in svcs or "energi_calc" in svcs:
        score += 1

    # Penalty: only cool-air brands (no water circuit authorisation)
    has_water_brand = bool(brds & WATER_BRANDS)
    has_cool_only   = bool(brds & COOL_BRANDS) and not has_water_brand
    if has_cool_only:
        score -= 1

    return max(score, 0)


def service_flags(services, brands):
    svcs = set(services or [])
    brds = set(b.lower() for b in (brands or []))
    return {
        "has_water_brand": int(bool(brds & WATER_BRANDS)),
        "has_nibe":        int("nibe" in brds),
        "has_bosch":       int("bosch" in brds),
        "has_solar":       int("solar" in svcs),
        "has_ev":          int("ev_charging" in svcs),
        "has_energiopt":   int("energiopt" in svcs or "energi_calc" in svcs),
        "brands_list":     ",".join(sorted(brds)) if brds else "",
    }


# ── C. Size scoring ───────────────────────────────────────────────────────────
def parse_employees(val):
    if not val or val in ("", "0"):
        return 0
    m = re.match(r'(\d+)', str(val))
    return int(m.group(1)) if m else 0

def size_mult(emp):
    if emp == 0:    return 0.60
    if emp < 5:     return 0.70
    if emp < 16:    return 0.90
    if emp < 41:    return 1.00
    if emp < 101:   return 0.90
    return 0.75


# ── D. Revenue from allabolag ─────────────────────────────────────────────────
def fetch_revenue(orgnr):
    try:
        url = f"https://www.allabolag.se/{orgnr}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode("utf-8", errors="replace")
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>',
                      html, re.DOTALL)
        if not m: return None
        data = json.loads(m.group(1))
        comp = data["props"]["pageProps"]["company"]
        rev = comp.get("revenue")
        return int(rev) if rev and str(rev).lstrip("-").isdigit() else None
    except Exception:
        return None

def revenue_points(rev_ksek):
    if rev_ksek is None: return 0
    if rev_ksek >= 100_000: return 3
    if rev_ksek >= 30_000:  return 2
    if rev_ksek >= 10_000:  return 1
    return 0


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    stores = json.load(open(FINAL_JSON, encoding="utf-8"))

    unique_orgnrs = list({s["abo_orgnr"] for s in stores if s.get("abo_orgnr")})
    print(f"Fetching revenue for {len(unique_orgnrs)} unique org numbers...")
    revenue_cache = {}
    for i, orgnr in enumerate(unique_orgnrs, 1):
        rev = fetch_revenue(orgnr)
        revenue_cache[orgnr] = rev
        status = f"{rev:,} kSEK" if rev else "n/a"
        print(f"  [{i}/{len(unique_orgnrs)}] {orgnr} -> {status}")
        time.sleep(0.45)

    print("\nScoring stores...")
    scored = []
    for store in stores:
        city     = store.get("city", "")
        services = store.get("services", [])
        brands   = store.get("brands", [])
        orgnr    = store.get("abo_orgnr", "")
        emp      = parse_employees(store.get("abo_employees", ""))
        revenue  = revenue_cache.get(orgnr)

        zone   = get_zone(city)
        z_mult = SE_MULT[zone]
        s_score = services_score(services, brands)
        s_mult  = size_mult(emp)
        r_pts   = revenue_points(revenue)
        flags   = service_flags(services, brands)

        raw   = s_score + r_pts
        final = round(raw * z_mult * s_mult, 2)
        tier  = ("A" if final >= 5 else
                 "B" if final >= 3 else
                 "C" if final >= 1 else "D")

        row = {
            **{k: v for k, v in store.items()
               if k not in ("services", "brands", "opening_hours_text", "fetch_error")},
            "services_list":  ",".join(services or []),
            "se_zone":        zone,
            "revenue_ksek":   revenue,
            "revenue_msek":   round(revenue / 1000, 1) if revenue else "",
            "employees_int":  emp,
            "score_services": s_score,
            "score_revenue":  r_pts,
            "score_raw":      raw,
            "mult_zone":      z_mult,
            "mult_size":      s_mult,
            "score_final":    final,
            "tier":           tier,
            **flags,
        }
        scored.append(row)

    scored.sort(key=lambda r: -r["score_final"])

    with open(SCORED_JSON, "w", encoding="utf-8") as f:
        json.dump(scored, f, indent=2, ensure_ascii=False)

    fieldnames = list(scored[0].keys())
    with open(SCORED_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(scored)

    from collections import Counter
    tiers = Counter(r["tier"] for r in scored)
    print(f"\n{'='*60}")
    print(f"Tier A (≥5): {tiers['A']}  |  B (≥3): {tiers['B']}  "
          f"|  C (≥1): {tiers['C']}  |  D (<1): {tiers['D']}")
    print(f"\nTop 20 stores:")
    print(f"{'#':<3} {'Name':<40} {'City':<14} {'Zone'} {'Emp':>5} {'Rev MSEK':>9} {'Score':>6} {'Tier'}")
    print("-" * 90)
    for i, r in enumerate(scored[:20], 1):
        rev = f"{r['revenue_msek']}" if r["revenue_msek"] != "" else "-"
        print(f"{i:<3} {r['name']:<40} {r['city']:<14} SE{r['se_zone']}  "
              f"{r['employees_int']:>5}  {rev:>8}  {r['score_final']:>6}  {r['tier']}")

    print(f"\nSaved → {SCORED_CSV}")


if __name__ == "__main__":
    main()
