# Besparingskalkylator v2 — Projektbeskrivning

## Bakgrund

CEO-initiativ: Bygga en AI-driven besparingskalkylator som ersätter nuvarande v1.  
Målsättning: 90% av vad en energirådgivare skulle räkna fram, men med bara 5–7 inputs från kunden.  
Dubbelt syfte: kundnära beslutsverktyg + leadsgenerering.

Ursprungsidén diskuterad i workshop med House:ID (Peter + CEO, 2 möten).  
Beslut: bygger vi själva — vi äger datan, vi äger relationen.

---

## Vad vi vet om befintliga resurser

### Peos Excel — kalkylmodellen
Excelen (`Peos excel som test att ta fram agent.xlsx`) är en **komplett uppslagsmodell** med 192 kombinationer:

- **4 elområden**: SE1, SE2, SE3, SE4
- **3 systemtyper**: BV (bergvärme), LV (luft/vatten), FL (frånluft)
- **4 husprofiler**: hus 1–4
- **4 scenarier per kombination**: nej (bas), sol, elbil, sol+elbil
- **2 prisår**: 2023 och 2024

Sparade värden är i kr/år. Exempelutfall SE3, BV, hus 3, sol = **5 627 kr/år (2023) / 5 553 kr/år (2024)**.

Data är redan extraherat och redo att bäddas in som JSON i koden — ingen extern datakälla behövs.

### Hus 1–4 — arbetsmappning från skärmdump
Skärmdumpen `Skärmavbild 2026-04-14 kl. 10.23.22.png` gav en användbar första mappning av husprofilerna:

| Husprofil | Förklaring | Antal kvm | Ålder | kWh/kvm/år | Förbrukning värme+vv |
|-----------|------------|-----------|-------|------------|----------------------|
| Hus 1 | 1 plans 100 kvm, 6 kW avgiven effekt | 120 | 1990 | 55 | **6 600 kWh/år** |
| Hus 2 | 1-plan villa 150 kvm, 8 kW avgiven effekt | 160 | 2010 | 55 | **8 800 kWh/år** |
| Hus 3 | 1,5 plan villa 200 kvm, 10 kW avgiven effekt | 210 | 1960 | 60 | **12 600 kWh/år** |
| Hus 4 | 2-plan villa 250 kvm+, 14 kW avgiven effekt | 250 | 1970 | 70 | **17 500 kWh/år** |

Notering: skärmdumpen visar VP-typ **MV**, medan Excelens summering använder **BV / LV / FL**. Detta räcker för att fortsätta v1-arbetet, men bör fortfarande bekräftas av Effira som gemensamma standardprofiler för alla systemtyper.

### PDF-specen
`Effira besparingskalkylator_agent_draft (kopia).pdf` är en 8-sidig kravspec som dokumenterar:
- Syfte, affärsmål och designprinciper
- Exakt vilka frågor agenten ska ställa (v1: 5–7 obligatoriska)
- Mappningslogik: kundsvar → Excel-kategorier
- Beräkningslogik: spann, brutto/netto, tidshorisont
- Output-format: 5 delar (huvudbudskap, förklaring, antaganden, alternativ vy, CTA)
- Fallback-regler när kunden inte kan svara
- Rekommendation för v1 och v2

### PPT-underlag — centrala insikter
`Utveckling_Besparingskalkylator 2.0 (kopia).pptx` tillför tre viktiga saker:

1. **Förbättringsspår 2.0**  
   - byt från enbart 2023 års spotpriser till nyare prisdata eller en flerårsserie
   - visa avrundade belopp eller spann i stället för exakta kronor
   - byt fokus från husstorlek till **årsförbrukning**
   - tydliggör att besparingen är **brutto**

2. **Förbättringsspår 2.1 (AI/agent)**  
   - 5-7 frågor
   - screening -> AI-dialog -> personlig kalkyl -> CTA
   - personlig, trygg och enkel upplevelse
   - möjlighet att lämna över till människa vid behov

3. **Strategiskt spår med House:ID**  
   - House:ID kan bidra med husdata och distribution
   - intressant partnerspår, men inte nödvändigt för att bygga v1 själva

---

## Arkitekturbeslut (överenskommet)

| Fråga | Beslut |
|-------|--------|
| Beräkningslogik | **Hard-coded** — Excel-tabellen bäddas in som JSON. Ingen LLM i mattelagret. |
| LLM-användning | **Endast för textoutput** — GPT skriver förklaringstexten på svenska, inte räknar |
| LLM-ägande | **Effira äger API-kostnaden** — eget OpenAI-konto på platform.openai.com |
| Datakälla | **Självständig** — ingen Google Sheet, Airtable eller extern källa |
| Exakthet | **Spann, inte exakta tal** — ±15% på medelhög datakvalitet, rundat till tusental |
| CTA / lead | **HubSpot** — befintlig integration |
| Webbplacering | **På befintlig Effira-sida**: `https://effiraenergy.com/se/rakna-ut-din-besparing/` |
| Webbmiljö | **WordPress** med custom theme |

---

## De 6 frågorna (reviderat förslag)

Nuvarande v1 frågar om elbil men OPTi kontrollerar inte elbilladdning — ger missvisande bild.  
Förslag: byt ut elbil mot elavtalstyp, som är den starkaste besparingsdrivaren.

| # | Fråga | Typ | Mappar till |
|---|-------|-----|-------------|
| 1 | Typ av uppvärmning? | Dropdown | BV / LV / FL |
| 2 | Elområde? (SE1–SE4) | Dropdown | Elområde |
| 3 | Årsförbrukning el? | Dropdown (intervall) eller fritext kWh | hus 1–4 |
| 4 | Har du solceller? | Ja/Nej | sol-scenario |
| 5 | Har du elbil? | Ja/Nej | elbil-scenario |
| 6 | Typ av elavtal? | Timpris / Rörligt / Vet ej | datakvalitet → osäkerhetsband |

---

## Output-format (per spec)

```
Rubrik:   "Du kan spara cirka 5 000–7 000 kr per år"
Text:     "Beräkningen bygger på bergvärme i SE3, ca 18 000 kWh/år och solceller."
Antaganden: [lista med 2–3 punkter]
Alternativ vy: per månad | per år | över 5 år
CTA:      "Vill du ha en exaktare kalkyl?" → HubSpot-formulär
```

Arbetsprincip: kalkylatorn ska kännas **närmare ett första rådgivande samtal** än dagens statiska kalkylator, utan att ge sken av att vara ett fullständigt projekteringsverktyg.

---

## Byggtid (1–2 timmar/dag)

| Fas | Innehåll | Dagar |
|-----|---------|-------|
| 1 | JSON-lookup + hus 1–4 labels | 1 |
| 2–3 | Frontend-formulär (HTML/JS, Effira-stil) | 2 |
| 4–5 | Beräkningsmotor + spannlogik | 2 |
| 6 | GPT-textlager (förklaring på svenska) | 1 |
| 7–8 | HubSpot CTA + lead capture | 2 |
| 9 | Testning, edge cases, fallbacks | 1 |
| 10 | Deploy / embed | 1 |

**→ ~2 veckor till live v1 @ 1–2 h/dag**  
**→ Fungerande demo (utan HubSpot/LLM) inom 3–4 dagar**

---

## Öppna frågor / blockers

| # | Fråga | Status | Ansvarig |
|---|-------|--------|---------|
| 1 | **Bekräfta att Hus 1-4 = 6 600 / 8 800 / 12 600 / 17 500 kWh/år** och att profilerna gäller för alla systemtyper | ⏳ Väntar | Peo / Effira |
| 2 | **OpenAI API-nyckel** — Effira skapar konto på platform.openai.com | ⏳ Väntar | Henrik / Effira |
| 3 | **HubSpot formulär-ID** för CTA-integrationen | ⏳ Väntar | Effira marketing |
| 4 | **Hur lösningen ska läggas in i WordPress** — direkt i temat, embed eller separat komponent | ⏳ Väntar | Effira |
| 5 | **Hur elavtal (timpris/rörligt/vet ej) ska påverka kalkylen** — besparing eller osäkerhetsspann | ⏳ Väntar | Effira |
| 6 | **Vilken prislogik v1 ska använda** — 2024, flerårsserie eller annan standard | ⏳ Väntar | Effira |
| 7 | **Vilken CTA som ska prioriteras** — offert, rådgivning, bli uppringd eller expertkontakt | ⏳ Väntar | Effira |

---

## Nästa steg (när hus 1–4 är klart)

1. Extrahera komplett JSON-lookup från Excel (klart — 192 rader parsade)
2. Bygga formulär + beräkningsmotor
3. Demo till CEO

---

## Filer i detta projekt

| Fil | Beskrivning |
|-----|-------------|
| `Peos excel som test att ta fram agent.xlsx` | Kalkylmodellen — 192 besparingskombinationer |
| `Effira besparingskalkylator_agent_draft (kopia).pdf` | Kravspec v1 (8 sidor) |
| `Utveckling_Besparingskalkylator 2.0 (kopia).pptx` | Presentationsunderlag för förbättringsspår 2.0 och 2.1 |
| `PROJECT-BRIEF.md` | Detta dokument — beslut, arkitektur, plan |
