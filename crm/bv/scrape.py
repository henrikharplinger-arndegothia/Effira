#!/usr/bin/env python3
"""
Scrape all Bad & Värme stores.

Step 1: Get all store cards from /ort/ (all 139 are on page 1).
Step 2: Fetch each individual store page for brand/service keywords.

Output: bv_stores.json
"""

import json, re, time, html as html_mod, urllib.request

BASE   = "https://www.bad-varme.se"
OUT    = "/Users/henrikharplinger/dev/bv-scrape/bv_stores.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv,en;q=0.5",
}

# Keywords to check in individual store pages (all lowercase)
# Checked in the store description text ONLY (after the nav section)
BRAND_KEYWORDS = ["nibe", "bosch", "ivt", "ctc", "thermia", "mitsubishi",
                  "daikin", "panasonic", "vaillant", "viessmann"]
SERVICE_KEYWORDS = {
    "solceller":    "solar",
    "solcell":      "solar",
    "elbil":        "ev_charging",
    "laddstation":  "ev_charging",
    "energikalkyl": "energi_calc",
    "energioptim":  "energiopt",
    "bergvärme":    "wp_bergvarme",   # only if in store content, not nav
    "luft/vatten":  "wp_luft_vatten",
    "frånluft":     "wp_franluft",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def clean(s):
    return html_mod.unescape(re.sub(r"\s+", " ", strip_tags(s))).strip()


def get_store_content(html):
    """Return store-specific content: 12 000 chars from the 'Välkommen' heading.
    This avoids sitewide CTA blocks (Energikalkyl ~26K away, IVT CTA ~30K+ away)."""
    pos = html.lower().find("välkommen till")
    if pos < 0:
        pos = html.lower().find("välkommen")
    if pos >= 0:
        return html[pos:pos + 12_000]
    # Fallback: main content area minus last 150K (sitewide CTAs are at end)
    m = re.search(r'<main[^>]*>', html)
    start = m.start() if m else 260_000
    return html[start:start + 30_000]


def parse_store_detail(url):
    """Fetch a store page and extract brand/service flags."""
    try:
        html = fetch(url)
        content = get_store_content(html)
        content_lower = content.lower()

        services = set()
        for kw, label in SERVICE_KEYWORDS.items():
            if kw in content_lower:
                services.add(label)

        brands = [b for b in BRAND_KEYWORDS if b in content_lower]

        # Extract opening hours text block if available
        hours_m = re.search(r'Öppettider.*?(?=<(?:h[1-6]|section|footer))', content, re.DOTALL | re.IGNORECASE)
        hours = clean(hours_m.group(0))[:200] if hours_m else ""

        return {"services": sorted(services), "brands": brands, "opening_hours_text": hours}
    except Exception as e:
        return {"services": [], "brands": [], "opening_hours_text": "", "fetch_error": str(e)}


def scrape_listing():
    """Scrape the /ort/ listing page and return list of basic store dicts."""
    html = fetch(f"{BASE}/ort/")
    articles = re.findall(r'<article[^>]+elementor-post[^>]+>(.*?)</article>', html, re.DOTALL)
    print(f"Found {len(articles)} store articles on listing page")

    stores = []
    seen_slugs = set()

    for art in articles:
        # Store URL / slug
        links = re.findall(r'href="(https://www\.bad-varme\.se/ort/[^"]+)"', art)
        store_links = [l for l in links if l.rstrip("/").count("/") == 4]
        if not store_links:
            continue
        url = store_links[0].rstrip("/") + "/"
        slug = url.rstrip("/").split("/")[-1]
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        # Name
        name_m = re.search(r'<h4[^>]*elementor-heading-title[^>]*>(.*?)</h4>', art, re.DOTALL)
        name = clean(name_m.group(1)) if name_m else ""

        # Contact fields — extract from widget-container text
        containers = re.findall(
            r'<div class="elementor-widget-container">(.*?)</div>', art, re.DOTALL
        )
        texts = [clean(c) for c in containers if clean(c) and len(clean(c)) < 200]

        city = phone = email = address = ""
        for t in texts:
            if t.startswith("Tel:"):
                phone = t[4:].strip()
            elif t.startswith("Mail:"):
                email = t[5:].strip()
            elif t.startswith("Adress:"):
                address = t[7:].strip()
            elif not city and t and not t.startswith((".", "#", "Välj", "Elterm", "Djupedal")):
                # Heuristic: first plain non-prefix text is city
                # Only if it looks like a Swedish city (no special chars, short)
                if re.match(r'^[A-ZÅÄÖa-zåäö\s\-]{2,25}$', t):
                    city = t

        # If city still not set, try to derive from URL slug
        if not city:
            city = slug.replace("-", " ").title()

        stores.append({
            "id":      slug,
            "name":    name,
            "url":     url,
            "city":    city,
            "phone":   phone,
            "email":   email,
            "address": address,
        })

    return stores


def main():
    stores = scrape_listing()
    print(f"\nFetching individual store pages for {len(stores)} stores...")

    enriched = []
    for i, store in enumerate(stores, 1):
        detail = parse_store_detail(store["url"])
        row = {**store, **detail}
        enriched.append(row)
        svc = ",".join(detail["services"]) or "-"
        brands = ",".join(detail["brands"][:3]) or "-"
        print(f"  [{i}/{len(stores)}] {store['name']:<40} svc={svc}  brands={brands}")
        time.sleep(0.4)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(enriched)} stores → {OUT}")
    has_solar = sum(1 for s in enriched if "solar" in s.get("services", []))
    has_ev    = sum(1 for s in enriched if "ev_charging" in s.get("services", []))
    has_wp_lv = sum(1 for s in enriched if "wp_luft_vatten" in s.get("services", []))
    has_brand = sum(1 for s in enriched if s.get("brands"))
    print(f"  solar={has_solar}  ev_charging={has_ev}  wp_luft_vatten={has_wp_lv}  has_brand={has_brand}")


if __name__ == "__main__":
    main()
