#!/usr/bin/env python3
"""Generate clean outreach list (Tier A) from scored BV stores."""

import json, csv

SCORED = "/Users/henrikharplinger/dev/bv-scrape/bv_stores_scored.json"
OUT    = "/Users/henrikharplinger/dev/bv-scrape/outreach_tier_ab.csv"

stores = json.load(open(SCORED, encoding="utf-8"))
tier_a = [s for s in stores if s["tier"] in ("A", "B")]


def vd_firstname(s):
    name = s.get("abo_vd_name", "")
    parts = name.strip().split() if name else []
    return parts[0] if parts else ""


def pitch_angle(s):
    angles = []
    if s.get("has_water_brand"): angles.append("aukt. VP-märke")
    if s.get("has_solar"):       angles.append("solceller")
    if s.get("has_ev"):          angles.append("elbilsladdning")
    return ", ".join(angles) if angles else "VVS/värme"


FIELDS = [
    "rank", "name", "city", "se_zone",
    "vd_name", "vd_firstname", "vd_role",
    "email", "phone",
    "employees_int", "revenue_msek",
    "score_final", "tier",
    "has_water_brand", "has_nibe", "has_bosch", "has_solar", "has_ev",
    "brands_list", "services_list",
    "pitch_angle",
    "url",
]

rows = []
for i, s in enumerate(tier_a, 1):
    row = {k: s.get(k, "") for k in FIELDS}
    row["rank"]         = i
    row["vd_name"]      = s.get("abo_vd_name", "")
    row["vd_firstname"] = vd_firstname(s)
    row["vd_role"]      = s.get("abo_vd_role", "")
    row["pitch_angle"]  = pitch_angle(s)
    rows.append(row)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} Tier A leads → {OUT}")
no_email = sum(1 for r in rows if not r["email"])
no_vd    = sum(1 for r in rows if not r["vd_name"])
print(f"Missing email: {no_email}  |  Missing VD: {no_vd}")
print("\nTop 15:")
for r in rows[:15]:
    print(f"  {r['rank']:>2}. {r['name']:<42} {r['vd_firstname']:<10} {r['email']}")
