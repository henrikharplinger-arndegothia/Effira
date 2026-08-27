# EFFIRA OPTI — PRISSÄTTNINGSSTRATEGI & JUSTERING

**Datum:** Augusti 2026  
**Version:** Arbetsdokument v1  
**Input-dokument:** Diskussionsunderlag OPTi Ny prissättning + Kostnader-2026-08-20.xlsx

---

## SITUATION & UTMANING

### Målet
- Hårdvara: **Kostnadsnetralt** (ingen marginaltänjning)
- Abonnemang: ~**129 kr/månad från kund** → 60 kr netto för Effira
- **Kundvärde:** Positiv ekonomi varje månad (aldrig går kunden i förlust)

### Problemet (från websidan & tidigare modeller)
**Modell A (30% riskdelning):**
- Vinter (starka besparingar): mål 94 kr/mån + VPP = ✅ lönsamt
- **Sommar (svaga besparingar): 0-20 kr/mån** = ❌ kund ser ingen värde
- Effira tjänar bara 30% × låg sparsamhet = minimalt

**Modell B (49 kr + 30%):**
- Vinterspetsar: 143 kr/mån = ✅ excellent
- **Juli månad:** ~65 kr debitering vs ~52 kr sparsamhet = ❌ **kund går 13 kr minus**
- Kunden upplever det som "dyrare än besparingen"

**Modell C (Fast 129 kr):**
- Enkel, förutsägbar
- **Sommarperiod:** 129 kr fast kostnad för mycket liten sparsamhet
- Kan uppfattas som dyrt vs. faktisk sparsamhet sommartid

---

## AFFÄRSSTRUKTUR & KOSTNADER

### Hardware (Kostnadsnetralt - ingen marginal)

```
SG-A (värmepumpenstyrenhet):  1,183 kr
SG-T (sensor):                  450 kr
P1/HAN/Kamstrup (mätare):       200 kr
Installation (arbetskostnad):  1,000 kr
Shipping:                        150 kr
─────────────────────────────────────
TOTAL HARDWARE:                2,983 kr @ 2K volume

SELLING PRICE TARGET:          3,500 kr (kostnadsberäknat, minst marginal)
CURRENT MARGIN:                  517 kr / unit (14.8%)

🎯 NYA MÅLET: Sälja för ~3,000 kr (kostnadsnetralt)
```

### Operating Costs (Monthly)

**Fixed:**
- SaveEye (pump cloud): 1,500 kr
- Onomondo (SIM & data): 16,600 kr
- **Total monthly fixed:** 18,100 kr

**Variable per unit:**
- SaveEye: 8 kr
- Onomondo: 10 kr
- Hosting/Cloud: ~5 kr (estimate)
- **Total per unit:** ~23 kr/månad

### Unit Economics (Current Model C: 129 kr/mån)

```
Revenue per unit/mån:     129 kr (gross)
Variable cost:            -23 kr
Gross contribution:       106 kr/månad

Fixed cost allocation:    18,100 kr / X units
Breakeven:               ~171 units (at 106 kr contrib)
```

---

## CUSTOMER VALUE PROBLEM

### Summer Months Pain Point

**Actual customer savings by season (central case from costing doc):**

| Månad | Savings/mån | Model A (30%) | Model B (49+30%) | Model C (fixed) | Problem |
|-------|------------|--------------|------------------|-----------------|---------|
| **Jan** | 400 kr | 120 kr ✅ | 169 kr ✅ | 129 kr ✅ | None |
| **Feb** | 380 kr | 114 kr ✅ | 163 kr ✅ | 129 kr ✅ | None |
| **Mar** | 300 kr | 90 kr ✅ | 139 kr ✅ | 129 kr ✅ | None |
| **Apr** | 200 kr | 60 kr ❌ | 109 kr ✅ | 129 kr ❌ | Low savings |
| **May** | 100 kr | 30 kr ❌ | 79 kr ✅ | 129 kr ❌ | Low savings |
| **Jun** | 50 kr | 15 kr ❌ | 64 kr ✅ | 129 kr ❌ | **Lowest** |
| **Jul** | 52 kr | 16 kr ❌ | 65 kr ❌ | 129 kr ❌ | **Customer loses 13 kr (B)** |
| **Aug** | 80 kr | 24 kr ❌ | 79 kr ✅ | 129 kr ❌ | Low savings |
| **Sep** | 150 kr | 45 kr ❌ | 94 kr ✅ | 129 kr ❌ | Low savings |
| **Oct** | 250 kr | 75 kr ✅ | 124 kr ✅ | 129 kr ✅ | None |
| **Nov** | 350 kr | 105 kr ✅ | 154 kr ✅ | 129 kr ✅ | None |
| **Dec** | 380 kr | 114 kr ✅ | 163 kr ✅ | 129 kr ✅ | None |
| **Totalt** | 3,748 kr | 1,124 kr | 1,550 kr | 1,548 kr | ❌ **6 months of customer pain** |

**Customer perception issue:**
- "Varför betalar jag 129 kr när jag bara sparar 52 kr?" (Modell B/C i juli)
- "Inte är det värt att ha OPTi på sommaren" (low savings months)
- Trust erosion when perceived cost > perceived benefit

---

## PRICING STRATEGIER & ALTERNATIV

### ALTERNATIV 1: Dynam Prissättning (Per Season)

**Idé:** Variera kundavgiften baserat på årstid

```
SOMMAR (Jun-Sep, låg sparsamhet):
  Modell A-Sommar: 20 % (vs 30%) → kund får mer värde
  Effira får: ~2,5 kr/enhet/månad (vs 10-15 kr)
  
VINTER (Okt-Maj, höga sparsamhet):
  Modell A-Vinter: 35 % (vs 30%) → Effira får mer
  Effira får: ~18 kr/enhet/månad (vs 12 kr)

RESULTAT: Balanserar årligt medan kund alltid vinner
```

**Fördelar:**
✅ Kunden tjänar pengar varje månad
✅ Effira får både vinter- och sommarintäkt
✅ Transparent: "Vi anpassar priset till din sparsamhet"

**Nackdelar:**
❌ Variabel debitering är komplex (Klarna, Kustom, kort)
❌ Kundkommunikation svårare ("varför olika pris?")

---

### ALTERNATIV 2: Garantipris + Justering (Hybrid)

**Idé:** Minsta garanterat värde för kunden

```
STRUKTUR:
Kund betalar: MAX(30% × besparing, 50 kr/månad)

Exempel:
- Jan (400 kr sparad): 30% = 120 kr ✅ (över 50 kr min)
- Jul (52 kr sparad): 30% = 16 kr ❌ → Lyfts till 50 kr minimum
- Jun (50 kr sparad): 30% = 15 kr ❌ → Lyfts till 50 kr minimum

RESULTAT: Kund betalar aldrig under 50 kr för synligt värde
```

**Årligt för Effira:**
- Vinterm nader: 30% × höga sparsamhet
- Sommarmånader: garanterad 50 kr × 6 mån = 300 kr
- Totalt: ~1,200-1,300 kr/år (samma som nuvarande)

**Fördelar:**
✅ Enkel för kund att förstå
✅ Garanterad minimum-värde-känsla
✅ En avgift (50 kr) enkel att fakturera
✅ Alignment med VPP-tanke: "Även om sparsamhet är låg, får du värde från nätverket"

**Nackdelar:**
❌ Kan bli jämnt dyrare för Effira sommartid om besparing < 167 kr
❌ Behöver tydlig kommunikation av "varför 50 kr minimum"

---

### ALTERNATIV 3: Bundel-Modell (Subscription + VPP)

**Idé:** Slå samman abonnemang + VPP-värde i ett erbjudande

```
NYT ERBJUDANDE:
"OPTi Smart Flex" - 89 kr/månad all-in

Vad ingår:
- 30% av besparingar (subscription)
- Tillgång till flexibilitetsmarknaden (värde från VPP redan från dag 1)

KOMMUNIKATION:
  "Du betalar 89 kr för kontroll + nätverksvärde
   Sparsamhet är bonus ovanpå."

EFFIRA INTÄKT:
  - 60 kr/månad subscription netto (129 × 46% efter rörlig kostnad)
  - + ~20-40 kr/månad VPP-värde (Year 1-2, not yet active but promised)
  = 80-100 kr/månad total
```

**Fördelar:**
✅ Enkel säljpitch ("ett pris, fullt värde")
✅ Kan lansera redan innan VPP-intäkter aktiveras officiellt
✅ Justerar kundförväntningar: "Du får värde från två håll"
✅ Matchas med år 2-3 reality när VPP aktiveras

**Nackdelar:**
❌ Kund förstår inte "vart går pengarna" utan transparent VPP-data
❌ Kräver tydligt kommunicera att VPP-värde kommer senare
❌ Högre pris (89 kr) än den 60 kr vi faktiskt tjänar på subscription

---

### ALTERNATIV 4: Tiered Model (Per Customer Segment)

**Idé:** Olika modeller för olika kundsegment

```
🏘️ PROFESSIONELL/STORA VILLOR:
  Modell A: 30% riskdelning (låga utgifter, högre sparsamhet)
  Target: >350 kr/mån sparsamhet
  
🏘️ NORMAL VILLA:
  Modell B: 59 kr + 20% (hybrid, lägre risk för Effira)
  Target: 200-350 kr/mån sparsamhet
  
🏘️ MINDRE VILLA/LÅG SPARSAMHET:
  Modell C: 99 kr fast (enkel, täcker Effiras kostnader)
  Target: <200 kr/mån sparsamhet
```

**Fördelar:**
✅ Matcher customer economics bättre
✅ Justerar expectation-setting vid försäljning
✅ Kan identifiera "profitabel segment" per modell

**Nackdelar:**
❌ Portfölj-komplexitet
❌ Säljare förvirrad om vilken att rekommendera
❌ Kundkommunikation blir nästan annorlunda mellan segmenten

---

## REKOMMENDERAD VÄGEN FRAMÅT

### KORT SIKT (Nästa 3 månader)

**Implementera:** ALTERNATIV 2 (Garantipris + Justering)

```
MODELL A+: 
  Prissättning: 30% × sparsamhet, MEN minst 50 kr/månad
  
KOMMUNIKATION:
  "Du betalar 30% av sparsamheten, med ett minimum på 50 kr.
   Sommarmånader får du automatisk rabatt om sparsamheten är låg.
   Så du tjänar alltid pengar."

IMPLEMENTATION:
  ✓ Uppdatera pris-sidan (https://effira-opti-prissattning-2026...)
  ✓ Visa exempel: "I juli sparade denna kund 52 kr → du betalar 50 kr (vår minimum)"
  ✓ Tydliggör i app: "Din besparingsgranth denna månad var X kr, din kostnad Y kr"
```

**Varför denna vägen:**
- Löser kundförlusst-problemet direkt (50 kr är rimligt)
- Affärsmodell oförändrad (samma totalt årligt värde för Effira)
- Enkel att kommunicera
- Tekniskt enkel att implementera

---

### MEDEL SIKT (6-12 månader)

**Parallel-spår: Förbereda ALTERNATIV 3 (Bundel + VPP)**

```
Förbereda:
1. Validera VPP-intäkter med Tibber (juni-juli 2027 redan gjort i july3-plan)
2. Skapa transparent VPP-dashboard för kund (visa: "Du tjänar 15 kr/mån från nätet")
3. Pilotera kombinerat erbjudande: "OPTi Smart Flex" - 89 kr/mån all-in

LAUNCH TIMELINE:
  - Q4 2026: Pilot with 50-100 customers (test messaging)
  - Q2 2027: Validate customer feedback + economics
  - Q3 2027: Full launch when VPP becomes official (fall 2028 target)
```

**Varför denna vägen:**
- Förberedelse för VPP-aktivering (hösten 2028)
- Ger tid att validera kommunikation
- Kan lansera "två pris-modeller samtidigt" (A+ och Smart Flex)

---

### LÅNG SIKT (2027+)

**Med VPP aktivt: Fullständig modell-utvidning**

```
MODELL A+: 30% + 50 kr minimum
  → Continue for risk-sharing lovers
  
MODELL VPP-BUNDEL: 89 kr all-in (sub + VPP explicit)
  → Primary offer (easier to understand)
  
MODELL C: 129 kr flat (for simple preference customers)
  → Keep for those who want predictability

OPTIONAL - Modell D: DYNAMIC (säsongsbaserad)
  → Sommar: 20% × sparsamhet
  → Vinter: 35% × sparsamhet
  → For customers who want "Fair seasonal pricing"
```

---

## FINANSIELL IMPACT ANALYS

### Scenario 1: Alternativ 2 (Garantipris + 50 kr min) — REKOMMENDERAD

**Årlig effekt per enhet:**

| Period | Scenario | Sparsamhet | Effira intäkt (30%) | Med 50 kr min | Skillnad |
|--------|----------|-----------|-------------------|--------------|----------|
| Vinter (6 mån) | Historik | 3,000 kr | 900 kr | 900 kr | 0 kr |
| **Sommar (6 mån)** | **Historik** | **700 kr** | **210 kr** | **300 kr** | **+90 kr** |
| **Totalt årligt** | **Idag** | **3,700 kr** | **1,110 kr** | **1,200 kr** | **+90 kr/år** |

**Effekt på 1,000 active customers:**
- Effira-intäkt ökning: 90,000 kr/år = +7,500 kr/månad
- Marginal ökning men **massiv kundnöjdsförbättring**

**Kundperspektiv:**
- Sommarmånad (jul): Betalar 50 kr för 52 kr sparande = +2 kr profit ✅ (vs -13 kr förut)
- Kundnöjdhet: "Jag tjänar pengar varje månad" = retention boost

---

### Scenario 2: Alternativ 3 (VPP-Bundel 89 kr)

**Årlig effekt per enhet (om VPP aktiveras Year 2):**

| Källa | Monatligt | Årligt |
|-------|----------|--------|
| Subscription netto (129 kr - costs) | 60 kr | 720 kr |
| VPP (Year 2, 83 kr/mån värd) | 83 kr | 996 kr |
| **Total värde delivered** | **143 kr** | **1,716 kr** |
| **Kund betalar** | **89 kr** | **1,068 kr** |
| **Effira intäkt (netto efter costs)** | **69 kr** | **828 kr** |

**Resultat:**
- Kund sparar 54 kr/månad genom bundel (vs att betala separat)
- Effira tjänar 108 kr/år mindre (828 vs 1,200 från A+)
- **Men:** VPP-bundel är "future-proofed" och enklare att sälja

---

## IMPLEMENTATION ROADMAP

### Phase 0: NOW (August 2026)

**Define pricing update:**
```
☐ Decide: Alternativ 2 (Garantipris) eller vänta på VPP-bundel?
☐ Update https://effira-opti-prissattning-2026... website
☐ Create customer FAQ: "Varför 50 kr minimum?"
☐ Prepare sales pitch (Model A+ vs Model C)
```

### Phase 1: Soft Launch (September 2026)

```
☐ Implement Alternativ 2 for NEW customers only
☐ Monitor: Do customers understand 50 kr minimum?
☐ Gather feedback via support/app
☐ Do NOT change existing customers (grandfathering)
```

### Phase 2: Full Migration (Q4 2026)

```
☐ Migrate existing Model A customers to A+ (if profitable)
☐ Keep Model C and Model B as-is
☐ Update all marketing materials
☐ Track: churn, NPS, customer satisfaction
```

### Phase 3: VPP Prep (2027)

```
☐ Parallel testing of "Smart Flex" bundle
☐ Design VPP dashboard for customer visibility
☐ Prepare Q3 2027 pilot launch
```

---

## CUSTOMER COMMUNICATION TEMPLATE

### Modell A+ (Recommended messaging)

**Vad betalar du:**
```
Du betalar 30 % av den besparing OPTi skapar varje månad.
Minimalt 50 kr för att säkerställa att systemet är värt det för dig.

Exempel:
  Januari (400 kr sparad):   Du betalar 30% = 120 kr ✅
  Juli (52 kr sparad):       Du betalar 50 kr (minsta nivå) ✅
  
Du tjänar ALLTID pengar — varje månad är positiv.
```

**Varför 50 kr minimum:**
```
Under sommaren sparar värmepumpen mindre (mindre uppvärmningsbehov).
Vi säger: "Du betalar minst 50 kr, så att du alltid ser värde från OPTi.
Resten av året när sparsamheten är högre, betalar du bara 30% och tjänar mycket mer."
```

---

## SUMMARY & NEXT STEPS

| Aspekt | Beslut | Ansvar |
|--------|--------|--------|
| **Strategi-val** | Alternativ 2 (Garantipris) | Henrik |
| **Website update** | Uppdatera pricepage | Webteam |
| **Kundkommunikation** | FAQ + pitch template | Försäljning |
| **Teknik** | Implementera 50 kr minimum i abonnemang-logic | Backend |
| **Pilotgrupp** | 50 nya kunder i sept | Försäljning |
| **Feedback-loop** | Samla NPS + support-frågor | Support |
| **Timeline** | Go-live Q1 2027 full | Projektledning |

---

**Nästa möte:** Diskutera alternativet, validera med sales & support, sedan proceed.

