# VPP — Teknisk beräkning och marknadslogik

> Arbetsdokument. Senast uppdaterad: 2026-06-15

---

## Vad betalar Svenska Kraftnät för?

Svenska Kraftnät köper **tillgänglig kapacitet i MW** — inte förbrukad energi i MWh.

Du får betalt för att *finnas tillgänglig*, oavsett om nätet faktiskt aktiverar dig. Undantaget är aFRR-aktivering där du också får betalt per MWh när du väl kallas in.

| Marknad | Betalar för | Enhet | När betalas |
|---------|------------|-------|------------|
| FCR-N | Tillgänglig kapacitet | EUR/MW/h | Alltid (kapacitetsauktion) |
| FCR-D | Tillgänglig kapacitet | EUR/MW/h | Alltid (kapacitetsauktion) |
| aFRR | Tillgänglig kapacitet + aktivering | EUR/MW/h + EUR/MWh | Kapacitet alltid, aktivering vid händelse |

**Auktionsmekanik:**
- FCR-marknaderna auktioneras dagligen i 4-timmarsblock
- Uniform price auction: lägsta antagna bud sätter priset för alla
- Priserna varierar kraftigt med marknadsläge (april 2025: 37 EUR/MW/h för FCR-N)
- Effira/Tibber tar del av clearing-priset för den kapacitet man vunnit

---

## Hur mäts förmågan?

### Steg 1 — Prekvali­ficering (en gång)
Tibber (som BSP — Balance Service Provider) genomför prekvali­ficeringstest mot Svenska Kraftnät:
- **FCR-D:** Demonstrera att X MW kan aktiveras inom 30 sekunder
- **FCR-N:** Demonstrera kontinuerlig droop-respons proportionell mot frekvensavvikelse
- **aFRR:** Demonstrera realtidsmätning OCH respons inom 5 minuter

Effira bidrar med: faktisk pumpdemostraion, mätdata, responsbevis.

### Steg 2 — Löpande drift och mätning

**FCR-N och FCR-D — automatisk respons:**
- Ingen dispatch-signal från Svenska Kraftnät
- Pumpen/OPTi reagerar automatiskt på nätfrekvensen (eller Tibbers aggregeringslager gör det)
- Svenska Kraftnät övervakar frekvenskvaliteten och verifierar statistiskt att kapaciteten levereras

**aFRR — signalstyrd:**
- Svenska Kraftnät skickar en styrsignal (AGC — Automatic Generation Control) till Tibber
- Tibber skickar dispatch-kommando till Effiras pumpar
- OPTi läser pumpens faktiska effektuttag före och efter kommando
- Realtidsmätdata skickas tillbaka: Svenska Kraftnät → Tibber → Effira → pumpdata
- Levererad reducering = summan av alla pumpars faktiska delta i kW

**Mätning per pump (OPTi):**
```
Innan kommando:   pump drar 4,2 kW   ← OPTi läser via pumpens API
Kommando: "stop"
Efter kommando:   pump drar 0 kW    ← OPTi läser
Delta:            4,2 kW bevisad reducering
```

**Aggregeringseffekt:**
Vid 10 000+ pumpar jämnas individuell variation ut. Statistisk leverans blir förutsägbar.
Vi binder oss till 80% av beräknad kapacitet — levererar konsekvent mer.

---

## Hur lång tid håller effekten?

Huset är en värmebuffert. Hur länge pumpen kan vara av utan komfortproblem:

| Hustyp | Utomhustemp | Max av-tid |
|--------|-------------|-----------|
| Vällisolerat (energiklass A) | 0°C | 2–4 timmar |
| Normallisolerat | 0°C | 60–90 min |
| Normallisolerat | −10°C | 20–30 min |
| Alla vid −15°C+ | — | Ej möjligt — stängs ej av |

**Vs. marknadskrav:**

| Marknad | Krav | Effira klarar |
|---------|------|--------------|
| FCR-D | 15 min | ✓ Alla hus vid rimlig temp |
| aFRR | 15–60 min | ✓ De flesta hus |

---

## Hur räknar vi fram Effiras VPP-förmåga?

### Kapacitetsformel

```
Effektiv VPP-kapacitet =
  Antal pumpar
  × Genomsnittligt effektuttag vid drift (kW)
  × Driftcykel (% av tiden pumpen faktiskt kör)
  × Säsongsandel (% av året kapaciteten finns)
```

### Parametrar

| Parameter | Värde | Motivering |
|-----------|-------|-----------|
| Antal pumpar | 100 000 | Steg 3-målet |
| Effektuttag vid drift | 4 kW | Genomsnitt svenska villor (max 5 kW, men 4 kW realistiskt årsmedel) |
| Driftcykel | 65% | Pumpen cyklar via termostat — kör ej 100% av uppvärmningssäsongen |
| Säsongsandel | 50% | Uppvärmningssäsong okt–apr (~5 100 h) minus extremkyla / 8 760 h |

### Beräkning

```
100 000 × 4 kW × 65% × 50% = 130 000 kW = 130 MW
```

### Fördelning per marknad

| Marknad | Andel av flottan | Motivering | MW |
|---------|-----------------|-----------|-----|
| FCR-N | 20% | Kräver inverterdriven pump med droop-reglering | 26 MW |
| FCR-D up | 80% | Kräver av inom 30 sek — nästan alla pumpar klarar | 104 MW |
| aFRR | 60% | Kräver realtidsmätning — staplas på FCR-D | 78 MW |
| FFR | 0% | Kräver < 1 sek respons — omöjligt | 0 MW |

*aFRR staplas på FCR-D: samma 78 MW deltar i båda. FCR-D aktiveras vid störning, aFRR återställer efteråt. Ingen dubbelräkning.*

---

## Intäktsberäkning — 100 000 pumpar

**Förutsättningar:**
- Tillgänglig kapacitet: 130 MW (se beräkning ovan)
- Tillgängliga timmar: 4 380 h/år (50% × 8 760)
- Valuta: 11,5 SEK/EUR
- Intäktsdelning Effira/Tibber: 50/50

| Marknad | MW | Pris | Timmar | Brutto/år | Effira (50%) |
|---------|-----|------|--------|-----------|--------------|
| FCR-N | 26 | 15 EUR/MW/h | 4 380 | 20 Mkr | 10 Mkr |
| FCR-D up | 104 | 15 EUR/MW/h | 4 380 | 79 Mkr | 39 Mkr |
| aFRR kapacitet | 78 | 8 EUR/MW/h | 4 380 | 31 Mkr | 16 Mkr |
| aFRR aktivering | 78 | 50 EUR/MW/h | 100 | 4 Mkr | 2 Mkr |
| **Totalt** | | | | **134 Mkr** | **67 Mkr/år** |

**Per enhet:**
```
67 Mkr ÷ 100 000 enheter = 670 kr/enhet/år = 56 kr/enhet/mån
```

### I skala

| Enheter | Kapacitet | VPP till Effira/år |
|---------|----------|-------------------|
| 2 000 | 2,6 MW | ~1,3 Mkr |
| 10 000 | 13 MW | ~6,7 Mkr |
| 100 000 | 130 MW | ~67 Mkr |

---

## Osäkerheter och känslighetsanalys

| Antagande | Värde | Om högre | Om lägre |
|-----------|-------|---------|---------|
| FCR-D pris | 15 EUR/MW/h | April 2025: 37 EUR → +84 Mkr brutto | Historiskt minimum: ~5 EUR |
| Driftcykel | 65% | 75%: +15% kapacitet | 50%: −23% kapacitet |
| Intäktsdelning | 50% Effira | 60%: +13 Mkr till Effira | 40%: −13 Mkr |
| Inverterflotta (FCR-N) | 20% | Liten effekt — FCR-D dominerar | — |

**FCR-D-priset är den enskilt viktigaste osäkerheten.** Vid historiska toppnivåer (37 EUR) är Effiras andel ~165 Mkr/år istället för 67 Mkr.

---

## Vad vi behöver lösa tekniskt för VPP

| Leverabel | Syfte | Krav från marknaden |
|-----------|-------|---------------------|
| Realtidsmätning per pump | Bevisa leverans till Svenska Kraftnät | Obligatoriskt för aFRR |
| Aggregeringslager | Samla och dispatcha alla pumpar som en resurs | Krävs för Tibbers BSP-roll |
| Prekvali­ficering (via Tibber) | Tillstånd att delta i FCR/aFRR | Engångskrav |
| Baseline-metodik | Bevisa delta vid aktivering | God praxis, krävs för trovärdighet |
