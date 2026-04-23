#!/usr/bin/env python3
"""Re-extract cities from the BV listing page and patch bv_stores_final.json + bv_stores.json."""

import json, re, html as html_mod, urllib.request

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

def clean(s):
    return html_mod.unescape(re.sub(r'<[^>]+>', ' ', s)).strip()

def clean_ws(s):
    return re.sub(r'\s+', ' ', clean(s)).strip()

html = fetch('https://www.bad-varme.se/ort/')
articles = re.findall(r'<article[^>]+elementor-post[^>]+>(.*?)</article>', html, re.DOTALL)

# Build slug → city map
slug_city = {}
for art in articles:
    links = re.findall(r'href="(https://www\.bad-varme\.se/ort/[^"]+)"', art)
    store_links = [l for l in links if l.rstrip('/').count('/') == 4]
    if not store_links:
        continue
    slug = store_links[0].rstrip('/').split('/')[-1]

    containers = re.findall(r'<div class="elementor-widget-container">(.*?)</div>', art, re.DOTALL)
    texts = []
    for c in containers:
        t = clean_ws(c)
        if t and not t.startswith(('.', '#', 'webien', '.cls')):
            texts.append(t)

    # City = text immediately before first Tel:
    tel_idx = next((i for i, t in enumerate(texts) if t.startswith('Tel:')), None)
    if tel_idx and tel_idx > 0:
        city = texts[tel_idx - 1]
        # Sanity: reject if it looks like a store name (contains common BV noise words)
        if not any(w in city.lower() for w in ('rör', 'vvs', 'värme', 'bad', 'sanitet',
                                                 'installatör', 'teknik', 'energi', 'el ')):
            slug_city[slug] = city

print(f'City map built: {len(slug_city)} slugs resolved')

# Patch both JSON files
for path in [
    '/Users/henrikharplinger/dev/bv-scrape/bv_stores.json',
    '/Users/henrikharplinger/dev/bv-scrape/bv_stores_final.json',
]:
    data = json.load(open(path, encoding='utf-8'))
    patched = 0
    for s in data:
        slug = s.get('id') or s.get('url', '').rstrip('/').split('/')[-1]
        if slug in slug_city:
            old = s.get('city', '')
            new = slug_city[slug]
            if old != new:
                s['city'] = new
                patched += 1
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Patched {patched} cities in {path.split("/")[-1]}')

# Spot-check
data = json.load(open('/Users/henrikharplinger/dev/bv-scrape/bv_stores_final.json'))
bad = [(s['name'], s['city']) for s in data if s['city'] == s['name'] or not s['city']]
print(f'\nStill bad/missing: {len(bad)}')
for n, c in bad[:10]:
    print(f'  {n!r} -> {c!r}')
