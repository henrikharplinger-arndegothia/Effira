# V3 Känslighetsmodell — Antaganden, Priser och Källor
**Fullständig genomgång av alla ingångsvärden, beräkningslogik och osäkerheter**

---

## Sammandrag: Vad V3 säger

| Scenario | VPP kr/mån | VPP kr/år | Total med abo-netto | Anmärkning |
|---|---|---|---|---|
| År 1 | ~42 kr | ~506 kr | ~102 kr/mån | Bas mFRR + lokal flex, inget aFRR |
| År 2 (bas) | ~83 kr | ~1 002 kr | ~143 kr/mån | mFRR + aFRR start + Tibber Grid Rewards |
| År 3 (GBG) | ~133 kr | ~1 600 kr | ~193 kr/mån | Effekthandel Väst-priser ~220 EUR/MWh |
| Toppnivå (GBG) | ~208 kr | ~2 500 kr | ~268 kr/mån | Effekthandel Väst snitt 2023/24 ~325 EUR/MWh |

Abonnemangsnetton (129 − 69 = 60 kr/mån) tillkommer alltid. Kundernas el- och effektbesparingar via OPTi-optimering tillfaller kunden och ingår **inte** i dessa siffror.

**GBG = antag signifikant Göteborg-penetration (Effekthandel Väst). År 1/2 baseras på sthlmflex-nivåpriser (konservativt).**

---

## Beräkningsmodellens logik

### Flottparametrar

```
peakMW     = antal_pumpar × kW_per_pump / 1 000
availFrac  = duty × season                     // andel av hela året pumpen kör
availDays  = 365 × availFrac                   // dagar/år tillgänglig
```

**Duty (drifttid inom säsong):** Andelen av uppvärmningssäsongen som pumpen faktiskt kör.
- Bas-antagande: **65%** — pump kör ~2/3 av heatings säsongen.
- Toppnivå: 70%.
- Källa: Schablonvärde för luftvärmepump i Sverige. Inga publicerade Effira/OPTi-data tillgängliga.

**Season (uppvärmningssäsong):** Andel av hela kalenderåret som det är uppvärmningssäsong.
- Bas-antagande: **50%** (okt–apr ≈ 183 dagar / 365 dagar = 50%).
- Toppnivå: 55%.
- Källa: Standardvärde för mellansverige (SE2/SE3).

**kW per pump:** Elvärmeeffekt vid drift.
- Bas: **4,0 kW** — genomsnittsvärde för luftvärmepump i villa (typ NIBE S-serie, Daikin Altherma, Mitsubishi Zubadan).
- Toppnivå: 4,5 kW.
- Källa: Branschdata (NIBE, Daikin produktblad). Kompressorbehov varierar 2–8 kW beroende på modell och belastning.

**Exempelflotta (bas-scenario):**
```
peakMW    = 100 000 × 4,0 / 1 000 = 400 MW
availFrac = 0,65 × 0,50 = 0,325
availDays = 365 × 0,325 = 118,6 dagar/år
```

---

## Marknad 1: mFRR — Manuell Frekvensåterställning

### Vad det är
SvK:s primära balansmarknad för manuellt aktiverad upp/ned-reglering. Resursen bjuder in D-1 i daglig kapacitetsauktion (sedan okt 2023). Vid aktivering skickar SvK signal till BSP (i vårt fall Tibber), som reläer till flottan. Responstid: 15 minuter (upp till full effekt), aktivering håller minst 1 timme.

### Prismarknad — bekräftade data (SvK Mimer, april 2025)

**Kapacitetspris (EUR/MW/dag):**
| Elområde | Up-reg apr 2025 | Kommentar |
|---|---|---|
| SE1 (Luleå) | 20,7 EUR/MW/dag | Lägst — liten efterfrågan norr |
| SE2 (Sundsvall) | 20,6 EUR/MW/dag | Liknande SE1 |
| SE3 (Stockholm) | 27,0 EUR/MW/dag | **Referens i modellen** |
| SE4 (Malmö) | 33,8 EUR/MW/dag | Högst — tätast nät |

**Källa:** SvK Mimer (mimer.svk.se/ManualFrequencyRestorationReserveCM) + SvK månadsrapport april 2025.

Sommarpriser (jun–aug) är lägre: SE1/SE2 ~12–13 EUR/MW/dag, SE3/SE4 ~16–18 EUR/MW/dag. Modellens årsgenomsnittsantagande (~25–40 EUR/MW/dag för bas/optimistiskt) är konsistent med SE3/SE4-nivå inkl. säsongsvariation.

**Aktiveringsvolym:** ~70 GWh upp-reglering aktiverat i Sverige totalt under april 2025 (SvK månadsrapport). Omräknat till timmar för en 400 MW-flotta: 70 000 MWh / 400 MW ≈ 175 timmar/mån nationellt — men Effiras andel är en bråkdel av total SvK-portfölj.

### Beräkningsformel

```
mfrrCapRevEUR = peakMW × mfrrCap[EUR/MW/dag] × availDays
mfrrActRevEUR = peakMW × mfrrActP[EUR/MWh] × mfrrActH[h/år] × availFrac
```

**Varför duty×season på aktivering:** Aktivering sker bara om pumpen faktiskt kör. `availFrac` approximerar sannolikheten att pumpen är igång vid dispatch-signal. Antagandet är att SvK:s dispatchtiming är oberoende av pumpstatus — konservativt, eftersom SvK tenderar att dispatcha vid kalla dagar (hög korrelation med att pumpen kör). Modellen underskattar därmed aktiveringsintäkten något.

**Varför inte duty×season på kapaciteten:** Kapacitetsbetalningen är D-1-auktionerad och betalas per dag oberoende av om pumpen kör den dagen. Men vi antar att Effira bara bjuder in dagar då flottan är tillgänglig (uppvärmningssäsong). Alternativt: om Effira bjuder in hela året men inte kan leverera sommartid = prequalificeringsrisk. Modellen är konservativ: vi bjuder bara in `availDays`.

### Scenariospecifika antaganden

| Scenario | Kapacitetspris | Aktiveringspris | Aktiveringstimmar | Motivering |
|---|---|---|---|---|
| År 1 | 25 EUR/MW/dag | 120 EUR/MWh | 120 h/år | Nystart, liten portfölj, SE3-priser |
| År 2 | 27 EUR/MW/dag | 130 EUR/MWh | 160 h/år | Etablerad, fler dispatch-events |
| År 3 gynnsamt | 40 EUR/MW/dag | 150 EUR/MWh | 220 h/år | Högre vinterpriser, fler events |
| Toppnivå | 55 EUR/MW/dag | 170 EUR/MWh | 200 h/år | Stramare marknad, vinterspetsar |

**Aktiveringspris 120–170 EUR/MWh:** mFRR aktiveras vid hög systemspänning — priset reflekterar rörlig kostnad för resursägaren + spot-priskorrelation. Nordisk spotpris under vinterspetsar: 100–500 EUR/MWh (2023–24). 120–170 EUR/MWh är mitt i spannet för normala (ej kris) vinterhändelser.

**Aktiveringstimmar 120–220 h/år:** CheckWatt rapporterar att deras flotta aktiverades ca 2–4 gånger per vecka under vinter 2024–25 med en genomsnittlig varaktighet 1–2 timmar. För en flotta som startar smått (år 1) är 120 h/år (≈ 2,3 h/vecka) konservativt, för en etablerad flotta är 160–220 h/år rimligt.

### Osäkerheter
- **Marknadsmättnad:** Den trilaterala marknaden (SE-FI-DK, lanserad nov 2024) kan komprimera priser. Okänd effekt 2025+.
- **Minimibud:** SvK kräver minst 1 MW per bud. Effira behöver ~250 pumpar för 1 MW. Ingen risk vid 100 000-flotta.
- **Prequalificering:** SvK:s tekniska krav granskas inte i modellen. Tibber BSP-licens täcker detta.

---

## Marknad 2: aFRR — Automatisk Frekvensåterställning

### Vad det är
SvK:s automatiska balansmarknad. Liknande priser som mFRR men med striktare tekniska krav: resursen måste följa en kontinuerlig setpunktssignal från SvK i realtid (5 min responstid, ingen dispens). Kräver realtids-SCADA-telemetri via BSP.

### Bekräftade priser
aFRR-priser april 2025 (SvK månadsrapport) är i samma storleksordning som mFRR: SE3 ~20–30 EUR/MW/dag för kapacitet. I modellen antas aFRR-priser något lägre än mFRR (fler alternativa resurser, mer komplex dispatch).

### Modellens antaganden

```
afrrMW         = peakMW × 0,60    // 60% av flottan tillgänglig för aFRR
afrrCapRevEUR  = afrrMW × afrrCap × availDays
afrrActRevEUR  = afrrMW × afrrActP × afrrActH × availFrac
```

**60%-faktorn:** aFRR kräver kontinuerlig uppföljning av setpunktsignalen. Vi antar att ~60% av flottan vid varje givet tillfälle kan följa en kontinuerlig reglerkurva (resten kör på termostatstyrning eller är i otillgänglighetsläge). Antagandet är uppskattning utan empirisk grund — Effiras systemarkitektur avgör det verkliga värdet.

**Tidslinje:** aFRR ingår inte i År 1. Startar år 2 med lägre tillgänglighet, år 3 med full potential.

| Scenario | Kapacitetspris | Aktiveringspris | Aktiveringstimmar |
|---|---|---|---|
| År 1 | 0 | 0 | 0 |
| År 2 | 22 EUR/MW/dag | 90 EUR/MWh | 130 h/år |
| År 3 gynnsamt | 35 EUR/MW/dag | 100 EUR/MWh | 200 h/år |
| Toppnivå | 50 EUR/MW/dag | 110 EUR/MWh | 220 h/år |

### Osäkerheter
- **Infrastruktur:** Realtids-setpunktsföljning kräver 4–6 månaders byggnad ovanpå mFRR-integrationen.
- **Tibbers BSP-kapacitet:** Tibber måste ha teknisk infrastruktur för aFRR-dispatch. Ej bekräftat från mötet.
- **Ramp-förmåga:** Flotta av on/off-pumpar kan approximera kontinuerlig ramp via staggerad omstart, men leveransträffsäkerheten är osäker.

---

## Marknad 3: Lokal flex — Effekthandel Väst (Göteborg) + NODES-plattform

### Vad det är
DSO-drivet flexibilitetsköp för flaskhalshantering i distributionsnätet. Ingen BSP-licens krävs. Minimivolym: 50 kW. Responstid: ~30 minuter. Geografiskt begränsat till respektive DSO:s nätområde.

### Primär referensmarknad: Effekthandel Väst — Göteborg

**Effekthandel Väst är AKTIV och växande** — drivs av Göteborg Energi Nät AB via NODES-plattformen (samma plattform som sthlmflex, men separat marknadsinstans).

**Tre produkttyper:**
| Produkt | Struktur | Prisbild |
|---|---|---|
| ShortFlex | Spotbuds, timvis | Snitt 3 737 SEK/MWh 2023/24 (≈325 EUR/MWh). 2024/25: ~2 000–3 000 SEK/MWh (≈174–261 EUR/MWh) |
| LongFlex | Kontrakt per månad/säsong, betalar tillgänglighet + aktivering | Tariff ej publicerad, "höga ersättningsnivåer" |
| MaxUsage | Provider håller sig under förbrukningstak, betalas per period | Per period/säsong |

**Marknadsdata:**
| Säsong | Aktiverat | Tillgänglighet | Leverantörer |
|---|---|---|---|
| 2023/24 | ~420 MWh | — | — |
| 2024/25 | **930 MWh** | **8 800 MWh** tillgänglighet | 27 leverantörer, 500+ resurser |
| 2025/26 | ~70 MW tillgänglig kapacitet | 1 500 enheter | Mölndal Energi Nät tillkom |

**Strukturell drivkraft:** Göteborg begränsas av Skogssäter–Ingelkärr-flaskhalsen (400 kV, nordsegmentet klart 2031). Göteborg Energi Nät har formellt tilldelats 426 MW extra kapacitet från Vattenfall Eldistribution, men det steppar in gradvis till 2035. Lokal flex är ett **permanent bridging-verktyg till 2031**, inte en pilot.

**Jämförelse sthlmflex vs Effekthandel Väst:**
| | sthlmflex (Stockholm) | Effekthandel Väst (Göteborg) |
|---|---|---|
| Status 2025/26 | Avslutad som R&D-projekt | AKTIV och växande |
| Snitt aktivering | 485–897 SEK/MWh | **2 000–3 737 SEK/MWh** |
| Tillgänglighetsbetalning | Nej (primärt spotaktivering) | **Ja** — LongFlex, MaxUsage |
| Värmepumpdeltagare | Testats begränsat | Uttryckligen välkomnade |

**Källa:** Göteborg Energi (goteborgenergi.se/effekthandel-vast) · NODES (nodesmarket.com/effekthandel-vast) · SvK Västra Götalands regionplan · ENERGInyheter nov 2024.

### sthlmflex — Status

- Avslutad som R&D-projekt efter 4 säsonger (Ellevio slutrapport 2025)
- Historiska priser 2020–22: 485–897 SEK/MWh snitt, toppar 5 000 SEK/MWh
- E.ON Switch (successorpilot) kör i Halland och i övriga E.ON-nät men inte i Göteborg-stadsnätet

### Beräkningsformel

```
lfRevEUR = peakMW × lfP[EUR/MWh] × lfH[h/år] × availFrac
```

Ingen kapacitetsbetalning i grundmodellen — lokal flex betalar vid faktisk aktivering.  
LongFlex/MaxUsage-värdet (tillgänglighet utan aktivering) är **ej modellerat** och är en ytterligare, konservativt utelämnad intäkt.

| Scenario | Aktiveringspris | Aktiveringstimmar | Motivering |
|---|---|---|---|
| År 1 | 80 EUR/MWh | 40 h/år | Begränsad tillgång, sthlmflex-prisreferens |
| År 2 | 90 EUR/MWh | 60 h/år | Tidig Effekthandel Väst-tillgång, konservativt |
| År 3 (GBG) | **220 EUR/MWh** | 90 h/år | Effekthandel Väst 2024/25 nedre intervall (~2 500 SEK/MWh) |
| Toppnivå (GBG) | **325 EUR/MWh** | 110 h/år | Effekthandel Väst 2023/24 snitt (3 737 SEK/MWh) |

### Osäkerheter
- **Geografisk begränsning:** Effekthandel Väst täcker Göteborg Energi Nät + Mölndal — inte hela Sverige. År 3/Toppnivå-scenarierna förutsätter att en signifikant andel av Effiras flotta finns i detta område.
- **LongFlex-tillgänglighet ej modellerad:** En kontrakt-baserad tillgänglighetsbetalning (ej aktivering) är en extra intäktsström som är konservativt utesluten.
- **Ej Vattenfall/E.ON-exponering:** De täcker inte Göteborg stadsområde — Göteborg Energi Nät är ensam DSO-köpare.

---

## Marknad 4: Tibber — Kommersiellt avtal

### Vad det är
Tibber är BRP (Balance Responsible Party) och BSP (Balancing Service Provider). Kommersiellt avtal täcker:
1. **Intradag-värde:** Tibber kan förbättra sin position på intradagmarknaden (Elbas) om flottan justerar förbrukning i realtid.
2. **Obalansvärde:** Om flottan konsumerar mer när systemet har överskott (prissignal negativ) förbättras Tibbers eSett-avräkning. Nordisk obalansavgift: 1,15 EUR/MWh bas, men kan spika till 10+ EUR/MWh vid stress.
3. **Hemoptimering/Grid Rewards:** Tibber betalar idag ~1 000 SEK/år för EV-laddning, ~3 200 SEK/år för home battery via Grid Rewards. Värmepumpar är "coming soon" (Tibber, juni 2025).
4. **15-min settlement (tailwind):** Sverige gick till 15-min mätintervall nov 2023. Fler dispatch-fönster per dag ökar värdet.

**Källa:** Tibber Grid Rewards (tibber.com/se/grid-rewards) · SvK 15-min-rapport 2023.

### Modellens antaganden

Tibber-värdet är en **förhandlad siffra** och modelleras som SEK/pump/mån direkt. Ingen EUR-konvertering.

| Scenario | SEK/pump/mån | Motivering |
|---|---|---|
| År 1 | 12 kr | Tidigt avtal, begränsat flottvärde |
| År 2 | 27 kr | Etablerad relation, BRP-värde validerat |
| År 3 (GBG) | 33 kr | Grid Rewards VP aktiverat, starkt BRP-värde |
| Toppnivå (GBG) | 45 kr | Fullt integrerat, 15-min-fönster utnyttjas |

**Osäkerhet:** Tibbers faktiska betalningsvilja är okänd — siffran är förhandlingsbar. BRP-imbalansevärdet är svårt att kvantifiera exakt.

---

## Affärsparametrar

| Parameter | Värde | Källa / motivering |
|---|---|---|
| Fast kostnad | 1 350 kkr/mån | Baserat på styresleplanens bemanning + infrastruktur |
| Abonnemang brutto | 129 kr/mån | Effiras planerade prispunkt |
| Rörlig kostnad per enhet | 69 kr/mån | Support, cloud, delad OPTi-kostnad |
| Abonnemang netto | 60 kr/mån | 129 − 69 |
| Valutakurs | 11,5 SEK/EUR | Referensnivå. Range modelleras med slider. |

---

## Scenariojämförelse: exempelkalkyl (bas, 100 000 pumpar)

```
peakMW    = 400 MW
availFrac = 0,325
availDays = 118,6 dagar/år

mFRR kapacitet: 400 × 27 × 118,6 × 11,5 / 100 000 / 12 = 12,3 kr/pump/mån
mFRR aktivering: 400 × 130 × 160 × 0,325 × 11,5 / 100 000 / 12 = 25,9 kr/pump/mån
aFRR kapacitet (60%): 240 × 22 × 118,6 × 11,5 / 100 000 / 12 = 6,0 kr/pump/mån
aFRR aktivering (60%): 240 × 90 × 130 × 0,325 × 11,5 / 100 000 / 12 = 8,7 kr/pump/mån
Lokal flex: 400 × 110 × 60 × 0,325 × 11,5 / 100 000 / 12 = 8,2 kr/pump/mån
Tibber: 22 kr/pump/mån
─────────────────────────────────────────────
VPP totalt: 83 kr/pump/mån = 996 kr/år
+ Abo netto: 60 kr/pump/mån
= TOTALT: 143 kr/pump/mån
```

---

## Verifikation mot branschdata

### CheckWatt-benchmark (BESS, H1 2025)
- 10 kWh batteri: 3 230–4 230 SEK för H1 2025 → extrapolerat ~6 500–8 500 SEK/år
- Per kW: 650–850 SEK/kW/år (10 kW batteri)

**Vår modell (bas, 4 kW pump):** 996 kr/år ÷ 4 kW = **249 SEK/kW/år**

Effiras pump ger ~30–38% av BESS-avkastningen per kW. Detta är rimligt av tre skäl:
1. Batteri kan leverera ner-reglering (öka förbrukning) — värmepump kan bara upp-reglera (stänga av)
2. Batteri har linjär dispatch-förmåga — pump är on/off
3. Batteri är tillgänglig 24/7 — pump kör bara ~32% av året

**Slutsats:** Modellen är konsistent med branschdata. Inget uppenbarat fel i storleksordningen.

### Tibber Grid Rewards-benchmark
- EV: ~1 000 SEK/år = 250 SEK/kW/år (4 kW laddfart)
- Batteri: ~3 200 SEK/år = 320 SEK/kW/år (10 kW)

**Vår modell (bas):** 996 kr/år ÷ 4 kW = **249 SEK/kW/år** — exakt i linje med EV-benchmark. Rimligt.

---

## Vad som inte modellerats (och varför)

| Ström | Varför utanför modellen |
|---|---|
| Kunds elbesparingar (spotoptimering) | Kunden behåller besparingen — inte VPP-intäkt |
| Effektavgift-reduktion för kund | Kunden behåller besparingen — inte VPP-intäkt |
| FCR-D | Marknaden kollapsad (€8,91/MW/dag apr 2025), autonom respons krävs (ej möjlig utan hårdvaruändring) |
| FCR-N | Kräver millisekunds-respons och kontinuerlig frekvensstyrning — omöjligt för kompressordrivna VP |
| Elcertifikat / ursprungsgarantier | Gäller bara produktion, inte flexibilitet |
| EU-bidrag / Vinnova | Projektfinansiering, ej löpande intäkt |
| DSO effektreserv (effektreserv) | Minimivolym för industriella aktörer, residential aggregatorer ej aktiva |
| BRF peak-shaving (kommersiellt) | Separat produktkoncept, inte VPP-pipeline |

---

## Korrektioner från V2

V2 överskattade VPP-intäkten med 20–43× pga:
1. **Prisenhetsfelet:** fcrdP i V2 tolkades som EUR/MW/**timme** men priser citeras EUR/MW/**dag**. V2:s "7 EUR/MW/h" = 168 EUR/MW/dag — 20× faktisk marknad (€8,91/MW/dag apr 2025).
2. **Fel primärmarknad:** FCR-D valdes för historiskt höga priser, men marknaden kraschade. V3 korrekterar till mFRR som primärmarknad.
3. **aFRR för högt rankad:** V2 hade aFRR som sekundär men rangordnade den framför mFRR. Peters feedback (Tibber) bekräftar att mFRR är mer realistisk ingångspunkt.
4. **mFRR saknades helt** i V2.
5. **Matematikbugen V1→V2:** Duty×season kvadrerades i V1 (fixat i V2, kvarstår korrekt i V3).

---

## Källor (komplett lista)

| Källa | Vad | Länk |
|---|---|---|
| SvK Mimer | mFRR live auktionsdata | mimer.svk.se/ManualFrequencyRestorationReserveCM |
| SvK månadsrapport apr 2025 | Bekräftade priser SE1–SE4 | svk.se/press-och-nyheter/nyheter/balansansvar/2025/... |
| SvK Balancing Market Outlook 2030 | Framtida marknadsutveckling | svk.se (dec 2024) |
| Sourceful | FCR-D april 2025 (€8,91/dag) | sourceful.energy/blog/april-2025-market-update-... |
| CheckWatt | H1 2025 VPP-intjäning | checkwatt.com/sv/news/sa-hade-checkwatts-... |
| CheckWatt | mFRR-avtal via Bixia (maj 2025) | checkwatt.com/news/forsta-avtalet-... |
| Tibber | Grid Rewards programbeskrivning | tibber.com/se/grid-rewards |
| NODES / sthlmflex | Marknadsöversikt och priser | nodesmarket.com/sthlmflex |
| Montel News | 5 000 SEK/MWh sthlmflex-topp | montelnews.com/se/story/5000-sekmwh-... |
| Peters email (Tibber) | Rangordning och tekniska krav | moten/tibber-mote-svar.md |
