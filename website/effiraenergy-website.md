# effiraenergy.com — Site Analysis

*Fetched 2026-04-23 | Updated from WordPress XML export 2026-04-23*

## Purpose

Sells OPTi, a heat pump control system that shifts heating/hot water to cheap electricity hours using the home's thermal mass as a "heat battery". Claims 6,000–12,000 SEK annual savings (~30%). Swedish market, primary language Swedish. Launched November 27, 2025. Founded 2014 as Easyserv, Halmstad, org 556948-4628.

## Tech stack (confirmed from WP export)

- **WordPress 6.8.5**, multisite (`effiraenergy.com/se`)
- **WooCommerce** with WooCommerce Subscriptions (shop orders, subscriptions present)
- **ACF (Advanced Custom Fields)** — all page content in custom blocks (`acf/page-hero`, `acf/wysiwyg-text`, `acf/frontpage-hero`, `acf/image-and-text`)
- **Gutenberg** block editor
- Custom fonts via `wp_font_family` / `wp_font_face` post types (36 font faces, 12 families)

## Navigation

- **OPTi** (hub)
  - Så fungerar OPTi (`/se/optimera-varmepumpen/`)
  - Effira-appen (`/se/effira-appen/`)
  - Priser 2026 (`/se/opti-priser-2026/`)
  - Fungerar med OPTi / Kompatibilitet (`/se/kompatibilitet/`)
  - Kunskapsbanken (`/se/kunskapsbanken/`)
- **Räkna ut din besparing** (`/se/rakna-ut-din-besparing/`)
- **Ring upp mig** (`/se/ring-upp-mig/`)
- **Support** (`/se/support/`)
- **Beställ OPTi** (`/se/bestall-opti/`)

## All Pages (from WP export)

### Published pages

| ID | Title | URL slug |
|----|-------|----------|
| 575 | Hem (homepage) | `/se/` |
| 590 | Besparingsgaranti | `/se/besparingsgaranti/` |
| 592 | Effira-appen | `/se/effira-appen/` |
| 611 | Så fungerar OPTi | `/se/optimera-varmepumpen/` |
| 632 | Huset som ett batteri | `/se/huset-som-ett-batteri/` |
| 1062 | Artiklar för dig som vill bli en energihjälte | `/se/artiklar-for-dig-som-vill-bli-en-energihjalte/` |
| 1072 | Om oss | `/se/om-oss/` |
| 1090 | Räkna ut din besparing | `/se/rakna-ut-din-besparing/` |
| 1092 | Integritetspolicy | `/se/integritetspolicy/` |
| 1099 | Support | `/se/support/` |
| 1169 | Cart | `/se/cart/` |
| 1171 | Checkout | `/se/checkout/` |
| 1248 | Beställ OPTi | `/se/bestall-opti/` |
| 1255 | Press | `/se/press/` |
| 1809 | Beställ Splitter för P1-kontakt | `/se/bestall-splitter/` |
| 2013 | Effira OPTi - funktioner och egenskaper | `/se/effira-opti-funktioner-och-egenskaper/` |
| 2176 | Priser 2026 | `/se/opti-priser-2026/` |
| 2193 | Fungerar med OPTi | `/se/kompatibilitet/` |
| 2631 | Hur jobbar din värmepump? | `/se/hur-jobbar-din-varmepump_2/` |
| 2805 | Seminarie | `/se/seminarie/` |
| 3150 | Radera konto | `/se/radera-konto/` |
| 3161 | Delete account | `/se/delete-account/` |
| 3287 | Nyhetsbrev | `/se/nyhetsbrev/` |
| 3417 | Ring upp mig | `/se/ring-upp-mig/` |
| 3437 | Effira Webinar | `/se/effira-webinar/` |
| 4078 | Kunskapsbanken | `/se/kunskapsbanken/` |
| 5 | Butik | `/se/butik/` |
| 9 | Allmänna villkor | `/se/allmanna_villkor/` |

### Private/draft pages

| ID | Title | Notes |
|----|-------|-------|
| 1097 | Kontakt & personal | Internal |
| 1114 | Systemdelar | Internal |
| 1132 | Smart värme | Internal |
| 1850 | OPTi användare i Sverige | Internal |
| 1870 | Hur arbetar din värmepump? | Old version |
| 2727 | Beställ OPTi v2 | Old version |
| 2803 | Beställ OPTi v3 | Old version |
| 3073 | Räkna ut din besparing v2 | Old version |
| 3366 | Installation | Internal |
| 8 | Mitt konto | Draft |

## Products (WooCommerce)

| ID | Name | Price | Type |
|----|------|-------|------|
| 1686 | OPTi Standard | 99 SEK/month | Subscription (customer owns hardware) |
| 1603 | OPTi Flex | 299 SEK/month | Subscription (hardware loaned) |
| 4280 | OPTi Standard abonnemang | 129 SEK/month (1290/year) | Subscription |
| 4276 | OPTi Flex abonnemang | 299 SEK/month (2990/year) | Subscription |
| 1702 | Splitter (RJ12/P1) | 395 SEK | Physical product |
| 1823 | P1 | 0 SEK | Accessory/included |
| 1825 | HAN | 0 SEK | Accessory/included |
| 1827 | Kamstrup | 0 SEK | Accessory/included |
| 4545 | OPTi ÖKAB | 0 SEK/month | Special partner subscription |

**OPTi Standard**: Customer buys/owns the unit, pays lower monthly subscription (99–129 SEK/month). No lock-in.  
**OPTi Flex**: Customer borrows hardware, pays one monthly fee covering equipment + subscription (299 SEK/month). Return unit on cancellation.  
**Included in both**: Professional installation, OPTi control unit, temperature sensor, real-time meter (P1/HAN/Kamstrup), mobile connectivity, smart heating control, smart hot water control, spot price optimization, peak demand management, solar energy steering, savings guarantee year 1.

## Besparingsgaranti (Savings Guarantee)

- Minimum 3,600 SEK/year guaranteed savings
- Conditions: customer must have hourly pricing (timprisavtal), ≥7,000 kWh annual heating usage, average price volatility >0.8 SEK/day (per SVK data)
- Assessed after 12 months; included in both Standard and Flex during year 1
- Tracked in the Effira app

## Knowledge Base — Kunskapsbanken (`/se/kunskapsbanken/`)

Hub page for: articles, webinars, product component info. Currently links to articles page and features video content inline.

### Published Articles (blog posts at `/se/artiklar-for-dig-som-vill-bli-en-energihjalte/`)

| # | Title | URL | Topic |
|---|-------|-----|-------|
| 1 | Ökande elförbrukning | `/se/artikel-1-okande-elforbrukning/` | Rising electricity demand in the Nordics; electrification of industry, transport, data centers; doubled demand within 10 years |
| 2 | Elprisernas volatilitet | `/se/artikel-2-elprisernas-volatilitet/` | Why prices swing more (wind dependency, hydrology, nuclear availability, grid bottlenecks SE1–SE4) |
| 3 | Solel i vanliga villor | `/se/artikel3-solel-i-vanliga-villor-mojligheter-risker-och-smart-anvandning/` | Solar PV for villas; profitability, risks, smart use; tax reductions; need to combine with smart control |
| 4 | Börsel (spot) vs. fast | `/se/artikel-4-borsel-spot-vs-fast/` | Hourly pricing vs fixed price; hybrid contracts; why spot wins long-term |
| 5 | Lokala flexmarknader | `/se/artikel5-lokala-flexmarknader/` | Flexibility markets; DSO/TSO, aggregators; how households can participate |
| 6 | *(draft — "Vilken typs pump har jag?")* | `/se/?p=2441` | Heat pump type identification — not yet published |
| 7 | Effektavgifter | `/se/artikel7-effektavgifter-vad-ar-syftet-och-hur-paverkas-du/` | Peak demand tariffs (effekttariffer); how kW peaks affect monthly grid fees; when peaks occur |
| 8 | Till vem betalar du för elen? | `/se/artikel-8-till-vem-betalar-du-for-elen/` | Two-invoice system: grid company (DSO) vs electricity trader; what each covers |
| 9 | Hur räknar man hem investeringen? | `/se/artikel-9-hur-raknar-man-hem-investeringen/` | Payback time calculation; ROT deductions; examples for solar, heat pump, smart control |
| 10 | Timpris – potentialen i varje timme | `/se/artikel-10-timpris-potentialen-i-varje-timme/` | Hourly vs monthly variable pricing; heating/hot water = 75% of consumption; shift loads to cheap hours |

### Webinars (published posts, video embeds)

| Title | URL | YouTube | Summary |
|-------|-----|---------|---------|
| Spara 8 000–10 000 kr per år i din villa | `/se/effira-webinar-spara-8-000-till-10-000-kr-per-ar-i-din-villa/` | `aRzq4pa7gJw` | Smart heating control; quarterly pricing; peak tariffs; avoid heating when expensive |
| 5 sätt att sänka dina elkostnader i villan | `/se/5-satt-att-sanka-dina-elkostnader-i-villan/` | `6OA4FCtBe18` | 5 practical ways to cut electricity costs |
| OPTi och solceller | `/se/opti-och-solceller/` | `6OA4FCtBe18` | OPTi + solar PV; self-consumption increase |
| OPTi och effekttariffer | `/se/opti-och-effekttariffer/` | `5O8DaGTuHfE` | OPTi and peak demand tariffs; reducing grid fees |
| Så maximerar du värdet av batteri och solceller | `/se/effira-webinar-sa-sanker-du-elrakningen-med-smart-varmestyrning/` | `bX9L6Ffqk5g` | OPTi + battery + solar; shift 8–10 kWh/day; house as heat battery |
| Få ut mer värde från dina solcellers | `/se/effira-webinar-fa-ut-mer-varde-fran-dina-solcellers/` | `NjGlptcrXqs` | Solar self-consumption +45% with OPTi; volatility = opportunity |

### Other published posts

| Title | URL | Notes |
|-------|-----|-------|
| OPTi med solceller och batterier | `/se/opti-med-solceller-och-batterier/` | Full article: house as heat battery; 95% of solution already in the house; solar PV complement |
| Vattenfalls Energibarometer | `/se/vattenfalls-energibarometer/` | Summary of Vattenfall's 2026 energy survey; >50% of Swedes find electricity market hard to understand; heating = up to 75% of consumption |
| Energiseminarium i Steninge | `/se/energiseminarium-i-steninge/` | Completed local seminar; new 2026 tariffs; how to save up to 30% |
| Pressmeddelande 20251127 | `/se/pressmeddelande_20251119/` | Launch press release: 1M heat pumps in Sweden; 200K connected = 1 nuclear reactor at peak; OPTi launched Nov 27, 2025 with savings guarantee |
| PRESSMEDDELANDE 20251216 | `/se/pressmeddelande-20251216/` | Partnership: Effira + Smartify; professional installation rollout |

## Key Page Summaries

### Så fungerar OPTi (`/se/optimera-varmepumpen/`)
Most heat pumps work at a constant rate regardless of electricity cost. OPTi shifts heating and hot water to the cheapest hours. The home's thermal mass (walls, floors, structure) stores heat for hours. Compatible with 90%+ of heat pump models. Installation by certified Effira technician, no rebuilding required, ~30 min.

### Effira-appen (`/se/effira-appen/`)
Shows real-time OPTi activity: electricity price, energy use, savings, heat battery charge level (blue bars). Start page shows daily savings + live price. Fully automatic — user just monitors.

### Huset som ett batteri (`/se/huset-som-ett-batteri/`)
Core concept page. Walls, floors, and structure store heat. OPTi charges the "heat battery" during cheap hours and draws from it during expensive hours. Includes savings calculator.

### Priser 2026 (`/se/opti-priser-2026/`)
Two models: **Standard** (own the unit, lower monthly fee) and **Flex** (borrow hardware, all-inclusive monthly fee). Both include: professional installation, OPTi unit, temperature sensor, P1/HAN/Kamstrup meter, mobile connectivity, smart heating, hot water control, spot price optimization, peak demand steering, solar steering.

### Kompatibilitet (`/se/kompatibilitet/`)
Compatibility checker for heat pump models. 90%+ of models supported. Compatibility always verified before shipping. Manufacturers added continuously.

### Besparingsgaranti (`/se/besparingsgaranti/`)
Minimum 3,600 SEK/year guaranteed. Conditions: hourly price contract, ≥7,000 kWh heating/year, market volatility >0.8 SEK/day. Settles after 12 months via app tracking.

### Om oss (`/se/om-oss/`)
Founded as insight that energy management in homes is unnecessarily complex. 25+ years experience in heat pump industry. Core values: cost savings, innovation, security, simplicity, sustainability. OPTi developed and manufactured in Sweden, installed by authorized technicians.

### Support (`/se/support/`)
FAQ section + contact form. Content loaded dynamically via ACF blocks (FAQ items not in XML export body).

## Authors / Team

| Login | Name | Email |
|-------|------|-------|
| stefan | Stefan Lundström | stefan.lundstrom@effiraenergy.com |
| johan | Johan Lundgren | johan.lundgren@effiraenergy.com |
| robert | Robert Kullström | robert.kullstrom@effiraenergy.com |
| peter.tellram | Peter Tellram | peter.tellram@effiraenergy.com |
| williamgustafsson | William Gustafsson | william.gustafsson@effiraenergy.com |

## Conversion CTAs

1. Savings calculator (`/se/rakna-ut-din-besparing/`)
2. "Ring upp mig" — callback request form (`/se/ring-upp-mig/`)
3. Compatibility checker (`/se/kompatibilitet/`)
4. Order OPTi (`/se/bestall-opti/`)
5. Webinar registration (upcoming April 29 event at `/se/effira-webinar/`)
6. Newsletter signup (`/se/nyhetsbrev/`)
7. App Store / Google Play links (in Effira-appen page)

## Target audience

Swedish villa owners, 35–65, with existing water-based heat pump. Middle to upper-middle income. Motivated by rising electricity costs and 2026 peak demand tariff changes. Values comfort without behavioral change. Secondary audience: solar PV owners wanting to maximize self-consumption.

## WooCommerce data (from export)

- 202 shop orders (184 completed, 3 processing, 9 on-hold, 21 cancelled)
- 136 subscriptions (14 active, 109 on-hold, 9 refunded cancelled)
- 9 refunds
- Active subscription count ~14 (early stage, launched Nov 2025)
