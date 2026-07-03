# V2 Känslighetsmodell — Antaganden, Källor och Fel
**Ärlig genomgång av vad modellen byggde på och var den gick fel**

---

## Varför FCR-D valdes som primärmarknad

### Resonemanget
FCR-D hade de i särklass högsta historiska priserna av alla stödtjänster i Sverige under 2022–2023. Under energikrisen (Ukraina-krig, gasprischock) låg priserna på €100–200/MW/dag. Det verkade som den uppenbara primärmarknaden för en stor flotta med snabb av/på-förmåga.

Resonemanget var:
1. Värmepumpar kan stängas av snabbt → FCR-D "upp" (minska förbrukning) verkar möjligt
2. Historiska priser var attraktiva
3. Prequalificering möjlig med typkvalificering för likadana enheter (OPTi är standardiserat)

### Vad som missades
- FCR-D kräver **autonom** 30-sekunders respons utan extern signal — pumpen måste reagera på nätfrekvensen själv, utan att vi skickar ett kommando. Det krävs inbyggd frekvensmätning i OPTi-hårdvaran. Den finns inte idag.
- Prequalificering kräver **garanterad tillgänglighet** — pumpen måste vara igång vid aktiveringstillfället. Om den inte kör finns inget att leverera.
- Marknaden kraschade: FCR-D kollapsade 2024–2025 pga BESS-överskott (batterilager tar marknaden). April 2025: €8,91/MW/dag — ned 95% från 2022-topparna.

---

## Prisenhetsfelet — den stora misstaget

### Vad modellen gjorde
V2-modellen använde `fcrdP` som **EUR/MW/timme** och beräknade:

```
fcrdEUR = peakMW × fcrdP[EUR/MW/h] × hoursPerYear
```

Exempelberäkning vid "Balanserat"-scenario (fcrdP = 16):
```
peakMW = 400 MW
hoursPerYear = 8760 × 0,5 × 0,65 = 2 847 h/år
fcrdEUR = 400 × 16 × 2 847 = 18 220 800 EUR/år
```

Det ger 1 500 kr/pump/mån i VPP-intäkt (vid 50% Effira-andel). Det var siffran som landade i styrelseplanens "125 kr VPP/pump/mån."

### Vad som är fel
FCR-D-marknaden prisar kapacitet i **EUR/MW/dag**, inte per timme. 

Faktiska priser april 2025: **€8,91/MW/dag** = €0,37/MW/h.

Modellens "konservativa" scenario använde `fcrdP = 7` vilket tolkades som 7 EUR/MW/h = **168 EUR/MW/dag** — ungefär **20 gånger** för högt.

"Balanserat"-scenariots fcrdP = 16 EUR/MW/h = **384 EUR/MW/dag** — ungefär **43 gånger** för högt mot nuvarande marknad.

### Varför felet uppstod
Priset "7 EUR/MW/h" kom från en tidig uppskattning utan referens till faktiska marknadsdata. Stödtjänstpriser citeras på olika vis i olika källor (per timme, per dag, per vecka) och enhetens kontext missades.

---

## Övriga antaganden som var fel

### aFRR som sekundärprodukt
V2 hade aFRR (5-minuters respons) som sekundär marknad. Det är tekniskt rimligare än FCR-D — men aFRR kräver en **kontinuerlig SCADA-setpunktsignal** från SvK som resursen måste följa i realtid. Ingen dispens möjlig. Det kräver real-time telemetri-infrastruktur vi inte har.

Tibber (från deras mail) rangordnar aFRR som #5 av 6 — under mFRR. Den underordningen missades i V2.

### mFRR saknades helt
Den mest realistiska SvK-produkten för värmepumpsaggregering (15-minuters respons, manuell dispatch, 1 MW min-bud) fanns inte alls i V2. Den borde ha varit primärprodukten.

### Inget Tibber-värde modellerades
Intradag/obalans-värdet till Tibber som BRP, och helhemsoptimeringsekosystemet, saknades. Det är #1 och #2 i Tibbers rangordning.

### Lokal flex saknades
Nodes/Effekthandel Väst (50 kW min-bud, ingen BSP-licens krävs, ~30 min responstid) saknades. Det är den enklaste ingångspunkten.

---

## V1 → V2: Matematikbugen som fixades

I V1 beräknades:
```
totalMW = peakMW × duty × season    // "genomsnittlig kapacitet"
fcrdEUR = totalMW × fcrdP × 8760   // hela årets timmar
```

Detta tillämpade duty×season på **båda** MW och timmarna — faktorn kvadrerades:
`revenue ∝ peakMW × (duty×season) × 8760 × (duty×season)`

Vid duty=0,65, season=0,50: faktorn 0,325 kvadrerades → 0,106 istället för 0,325. Revenue underskattades ~3×.

V2-fixet: separera peakMW (ingen duty/season-justering) från hoursPerYear (med duty×season):
```
peakMW = pumps × kW / 1000
hoursPerYear = 8760 × duty × season
fcrdEUR = peakMW × fcrdP × hoursPerYear
```

Detta var korrekt matematiskt, men prisenhetsfelet (EUR/MW/h vs EUR/MW/dag) kvarstod.

---

## Vad V2 borde ha sagt

| Metric | V2 (balanserat) | Korrekt (EUR/MW/dag, aktuella priser) |
|---|---|---|
| FCR-D pris | 16 EUR/MW/h = 384 EUR/MW/dag | €3–25/MW/dag (apr 2025: 8,91) |
| VPP per pump (FCR-D) | ~80 kr/mån | ~2–8 kr/mån |
| Primärmarknad | FCR-D | mFRR + lokal flex |
| Break-even | ~11 700 enheter | ~14 000–17 000 enheter (mFRR-bas) |

---

## Vad som fortfarande stämmer

- **FCR-N exkluderat** — korrekt. Kräver millisekunds-respons, ej möjligt för VP-kompressorer.
- **Grundlogiken** — en stor standardiserad flotta VP:ar har flexibilitetsvärde. Stämmer.
- **Upp-reglering only** — vi kan bara stänga av pumpar (minska förbrukning). Korrekt modellerat.
- **Rebound-hanteringen** — identifierades men inte kvantifierades. Viktigt att ta med i V3.
- **Abonnemangsdelen** — 129 kr − 69 kr = 60 kr netto. Oförändrat.

---

## Sammanfattning

V2 överskattade VPP-intäkten med ca **20–40×** beroende på scenario. Orsak: prisenhet (EUR/MW/h vs EUR/MW/dag) kombinerat med att FCR-D-marknaden kollapsade. Affärslogiken håller men vägen dit är via mFRR och lokal flex, inte FCR-D — och intäktsrampen är långsammare.

V3 korrigerar: korrekt enhet (EUR/MW/dag), korrekt marknadshierarki (mFRR primär), korrekt break-even.
