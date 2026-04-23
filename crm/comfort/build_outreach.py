#!/usr/bin/env python3
"""
Generate clean outreach list (Tier A) for Effira sales.
Output: outreach_tier_a.csv
"""

import json, csv

SCORED = "/Users/henrikharplinger/dev/comfort-scrape/stores_scored.json"
OUT    = "/Users/henrikharplinger/dev/comfort-scrape/outreach_tier_a.csv"

stores = json.load(open(SCORED, encoding="utf-8"))
tier_a = [s for s in stores if s["tier"] == "A"]

def best_email(s):
    return s.get("email_order") or s.get("contact_email") or s.get("email") or ""

def vd_firstname(s):
    name = s.get("abo_vd_name", "")
    if not name:
        return ""
    parts = name.strip().split()
    # Swedish names: "Jan Gunnar Magnus Johansson" — first given name
    return parts[0] if parts else ""

def pitch_angle(s):
    angles = []
    if s.get("has_wp_water"):  angles.append("värmepump (vatten)")
    if s.get("has_solar"):     angles.append("solceller")
    if s.get("has_energiopt"): angles.append("energioptimering")
    return ", ".join(angles) if angles else "VVS"

FIELDS = [
    "rank", "name", "city", "se_zone", "address",
    "vd_name", "vd_firstname", "vd_role",
    "best_email", "phone_number",
    "employees_int", "revenue_msek",
    "score_final", "tier",
    "has_wp_water", "has_solar", "has_energiopt",
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
    row["best_email"]   = best_email(s)
    row["pitch_angle"]  = pitch_angle(s)
    row["url"]          = f"https://www.comfort.se/butiker/{s.get('id','')}" if s.get("id") else ""
    rows.append(row)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

print(f"Wrote {len(rows)} Tier A leads → {OUT}")

# Quick sanity
no_email = sum(1 for r in rows if not r["best_email"])
no_vd    = sum(1 for r in rows if not r["vd_name"])
print(f"Missing email: {no_email}  |  Missing VD name: {no_vd}")
print("\nTop 10:")
for r in rows[:10]:
    print(f"  {r['rank']:>2}. {r['name']:<42} {r['vd_firstname']:<10} {r['best_email']}")
