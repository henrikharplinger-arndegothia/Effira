#!/usr/bin/env python3
"""
Step 1: Score and rank Comfort stores for Effira OPTi lead attractiveness.

Scoring dimensions:
  A) SE electricity zone     (multiplier — drives OPTi customer ROI)
  B) Service profile         (points — heat pump type, solar, energy services)
  C) Company size            (multiplier — headcount sweet spot)
  D) Revenue                 (points — fetched live from allabolag)
"""

import json, csv, re, time, urllib.request

FINAL_JSON   = "/Users/henrikharplinger/dev/comfort-scrape/stores_final.json"
SCORED_JSON  = "/Users/henrikharplinger/dev/comfort-scrape/stores_scored.json"
SCORED_CSV   = "/Users/henrikharplinger/dev/comfort-scrape/stores_scored.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# ── A. SE electricity zone ────────────────────────────────────────────────────
# SE4 (south) has highest prices → strongest OPTi ROI
SE_ZONE = {
    # SE1 – Norrbotten
    "Arjeplog":1,"Arvidsjaur":1,"Boden":1,"Haparanda":1,"Kalix":1,
    "Luleå":1,"Öjebyn":1,"Piteå":1,
    # SE2 – Norrland south + Dalarna + Gävleborg
    "Bollnäs":2,"Borlänge":2,"Gävle":2,"Holmsund":2,"Hudiksvall":2,
    "Härnösand":2,"Kramfors":2,"Lima":2,"Linghed":2,"Ljusdal":2,
    "Lycksele":2,"Malå":2,"Malung":2,"Mora":2,"Östersund":2,
    "Sandviken":2,"Skellefteå":2,"Sollefteå":2,"Söderhamn":2,
    "Storvik":2,"Sundsvall":2,"Tärnaby":2,"Umeå":2,"Vemdalen":2,
    "Vindeln":2,"Arnäsvall":2,
    # SE4 – Skåne, Blekinge, Halland, Kronoberg, Kalmar, Gotland + south Småland
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
    return SE_ZONE.get(city, 3)   # default SE3


# ── B. Services scoring ───────────────────────────────────────────────────────
SERVICE_SCORES = {
    "b2c|varmepump|luft_vatten_varmepump": 3,   # primary OPTi target
    "b2c|varmepump|bergvarme":             2,   # also water-circuit
    "b2c|varmepump|franluftsvarmepump":    1,   # compatible
    "b2c|varmepump|varmepump_generellt":   1,   # generic heat pump
    "b2c|el|solceller":                    1,   # energy-aware customers
    "b2c|vvs|service_reparationer":        1,   # ongoing service relationships
    "b2b|vvs|energioptimering":            1,   # already selling energy optimization
    "b2c|el|energioptimering":             1,
}

def services_score(services):
    svcs = set(services or [])
    score = sum(v for k, v in SERVICE_SCORES.items() if k in svcs)

    # Penalty: air-air only (no water circuit = OPTi incompatible)
    has_water = any(k in svcs for k in (
        "b2c|varmepump|luft_vatten_varmepump",
        "b2c|varmepump|bergvarme",
        "b2c|varmepump|franluftsvarmepump",
        "b2c|varmepump|varmepump_generellt",
    ))
    has_luft_luft = "b2c|varmepump|luft_luft_varmepump" in svcs
    if has_luft_luft and not has_water:
        score -= 3

    # No B2C at all — purely commercial installer, bad fit
    if not any(s.startswith("b2c") for s in svcs):
        score -= 2

    return max(score, 0)


def service_flags(services):
    svcs = set(services or [])
    return {
        "has_wp_water":  any(s in svcs for s in (
            "b2c|varmepump|luft_vatten_varmepump",
            "b2c|varmepump|bergvarme",
            "b2c|varmepump|franluftsvarmepump")),
        "has_wp_luftluft": "b2c|varmepump|luft_luft_varmepump" in svcs,
        "has_solar":       "b2c|el|solceller" in svcs,
        "has_energiopt":   ("b2b|vvs|energioptimering" in svcs or
                            "b2c|el|energioptimering"  in svcs),
        "has_b2c_service": "b2c|vvs|service_reparationer" in svcs,
        "b2c_only":        not any(s.startswith("b2b") for s in svcs),
    }


# ── C. Size scoring ───────────────────────────────────────────────────────────
def parse_employees(val):
    """Return int from strings like '21', '1-4', '10-19', '' etc."""
    if not val or val in ("", "0"):
        return 0
    m = re.match(r'(\d+)', str(val))
    return int(m.group(1)) if m else 0

def size_mult(emp):
    if emp == 0:        return 0.60
    if emp < 5:         return 0.70
    if emp < 16:        return 0.90
    if emp < 41:        return 1.00   # sweet spot
    if emp < 101:       return 0.90
    return 0.75                        # >100: slow procurement


# ── D. Revenue from allabolag ─────────────────────────────────────────────────
def fetch_revenue(orgnr):
    """Fetch revenue (kSEK) from allabolag company page."""
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
    """0-3 points based on annual revenue."""
    if rev_ksek is None: return 0
    if rev_ksek >= 100_000: return 3   # ≥100 MSEK
    if rev_ksek >= 30_000:  return 2   # ≥30 MSEK
    if rev_ksek >= 10_000:  return 1   # ≥10 MSEK
    return 0


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    stores = json.load(open(FINAL_JSON, encoding="utf-8"))

    # De-duplicate org numbers for revenue fetching
    unique_orgnrs = list({s["abo_orgnr"] for s in stores if s.get("abo_orgnr")})
    print(f"Fetching revenue for {len(unique_orgnrs)} unique org numbers...")
    revenue_cache = {}
    for i, orgnr in enumerate(unique_orgnrs, 1):
        rev = fetch_revenue(orgnr)
        revenue_cache[orgnr] = rev
        if rev is not None:
            print(f"  [{i}/{len(unique_orgnrs)}] {orgnr} -> {rev:,} kSEK")
        else:
            print(f"  [{i}/{len(unique_orgnrs)}] {orgnr} -> n/a")
        time.sleep(0.45)

    print("\nScoring stores...")
    scored = []
    for store in stores:
        city     = store.get("city", "")
        services = store.get("services", [])
        orgnr    = store.get("abo_orgnr", "")
        emp      = parse_employees(store.get("abo_employees", ""))
        revenue  = revenue_cache.get(orgnr)

        zone     = get_zone(city)
        z_mult   = SE_MULT[zone]
        s_score  = services_score(services)
        s_mult   = size_mult(emp)
        r_pts    = revenue_points(revenue)
        flags    = service_flags(services)

        # Raw score before multipliers
        raw = s_score + r_pts

        # Final score
        final = round(raw * z_mult * s_mult, 2)

        tier = ("A" if final >= 5 else
                "B" if final >= 3 else
                "C" if final >= 1 else "D")

        row = {
            **{k: v for k, v in store.items()
               if k not in ("services","geolocation","opening_hours","phone_hours",
                             "deviating_opening_hours","deviating_phone_hours")},
            "se_zone":          zone,
            "revenue_ksek":     revenue,
            "revenue_msek":     round(revenue / 1000, 1) if revenue else "",
            "employees_int":    emp,
            "score_services":   s_score,
            "score_revenue":    r_pts,
            "score_raw":        raw,
            "mult_zone":        z_mult,
            "mult_size":        s_mult,
            "score_final":      final,
            "tier":             tier,
            **{k: int(v) for k, v in flags.items()},
        }
        scored.append(row)

    scored.sort(key=lambda r: -r["score_final"])

    # Save
    with open(SCORED_JSON, "w", encoding="utf-8") as f:
        json.dump(scored, f, indent=2, ensure_ascii=False)

    fieldnames = list(scored[0].keys())
    with open(SCORED_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(scored)

    # Summary
    from collections import Counter
    tiers = Counter(r["tier"] for r in scored)
    print(f"\n{'='*60}")
    print(f"Tier A (score≥5): {tiers['A']}  |  B (≥3): {tiers['B']}  "
          f"|  C (≥1): {tiers['C']}  |  D (<1): {tiers['D']}")
    print(f"\nTop 20 stores:")
    print(f"{'#':<3} {'Name':<42} {'City':<14} {'Zone'} {'Emp':>5} {'Rev MSEK':>9} {'Score':>6} {'Tier'}")
    print("-" * 95)
    for i, r in enumerate(scored[:20], 1):
        rev = f"{r['revenue_msek']}" if r['revenue_msek'] else "-"
        print(f"{i:<3} {r['name']:<42} {r['city']:<14} SE{r['se_zone']}  "
              f"{r['employees_int']:>5}  {rev:>8}  {r['score_final']:>6}  {r['tier']}")

    print(f"\nSaved → {SCORED_CSV}")


if __name__ == "__main__":
    main()
