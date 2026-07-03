# VPP Kunskapsbas — Effira
**Senast uppdaterad: juli 2026**

Denna fil är Effiras referensdokument för svenska och nordiska flexibilitetsmarknader. Den täcker alla relevanta marknader, tekniska krav, prisutveckling och Effiras tillgänglighet per marknad.

---

## Snabbguide: Marknadslandskapet

| Marknad | Typ | Min volym | Responstid | Tillgänglig för Effira | Tidslinje |
|---|---|---|---|---|---|
| Tibber helhemsoptimering | Ekosystem | — | Timmar | Nu (avtal krävs) | År 1 |
| Lokal flex (Nodes/Effekthandel Väst) | DSO | 50 kW | 30 min | Nu | År 1 |
| Intradag & obalans (via Tibber BRP) | BRP-värde | — | Timmar | Via avtal | År 1–2 |
| mFRR upp | SvK | 1 MW | 15 min | Via BSP-partner | År 1–2 |
| aFRR upp | SvK | 1 MW | 5 min | Via BSP-partner | År 2–3 |
| FCR-D upp | SvK | 0,05 MW | 30 sek | Svårt (tekniska hinder) | År 4+ |
| FCR-N | SvK | 0,05 MW | <1 sek | Nej (real-time Hz-respons) | Aldrig |

**Riktlinje:** Vi kan bara göra **upp-reglering** (stänga av pumpar = minska förbrukning). Ned-reglering (öka förbrukning) är begränsad — på vintern kör pumparna redan på max, det finns ingen headroom.

---

## 1. FCR-N — Frekvensstabilisering normal (UTESLUTEN)

**Vad det är:** Kontinuerlig, proportionell reglering mot nätfrekvensavvikelse inom ±0,1 Hz. Krävs att resursen svarar autonomt inom millisekunder utan extern signal.

**Varför Effira inte kan göra detta:**
- Kräver inbyggd frekvensmätning i varje enhet och omedelbar autonom respons.
- Kompressorer och värmepumpar har fysiska minimitider och kan inte cykla på ms-nivå.
- Kräver fullständig instrumentering och realtidskommunikation till SvK.

**Pris:** €100–600/MW/dag (historiska toppar 2022–2023). Irrelevant för Effira.

**Verdict: Aldrig aktuellt med nuvarande OPTi-arkitektur.**

---

## 2. FCR-D — Frekvensstabilisering vid störning

### FCR-D upp (minska förbrukning vid frekvensfall under 49,9 Hz)

**Tekniska krav:**
- 50% aktivering inom **5 sekunder**, full aktivering inom **30 sekunder** — autonomt, utan extern signal.
- Uthållighet: minst 20 minuter vid 100% aktivering.
- Mätdata skickas realtid till SvK via ICCP-protokoll.
- Prequalificering hos SvK. Typkvalificering möjlig för likadana enheter (samma modell, samma BSP, samma styrningslogik).
- Min-budstorlek: 0,05 MW (50 kW).

**Vad som gör FCR-D svårt för värmepumpar:**
- Pumpen måste vara igång vid aktiveringstillfället — om den inte kör kan vi inte leverera.
- Effektmätningen per pump är osäker (smart meter ger 15-min granularitet, inte sekund-nivå).
- Rebound-effekten (pumpen kör hårdare efteråt) är svår att hantera på 30-sekunders produkter.
- Prequalificering kräver verifierbara portföljer med garanterad tillgänglighet — svårt med heterogen flotta.

### FCR-D ned (öka förbrukning vid frekvenstopp) — UTESLUTEN
Kräver att pumpar ökar förbrukning. Ej möjligt på vintern, marginellt möjligt resten av året. Utesluts.

### Prisutveckling FCR-D

| Period | FCR-D upp (EUR/MW/dag) | Kommentar |
|---|---|---|
| 2022 (topp) | €100–200 | Ukraina-krig, gasprischock, hög volatilitet |
| 2023 | €30–100 | Gradvis prisfall pga BESS-etablering |
| 2024 Q1-Q3 | €6–25 | Dramatiskt prisfall |
| Nov 2024 | ~€2,70 | Ny bottennivå |
| Feb 2025 | <€3 | Rekordlågt — BESS har tagit marknaden |
| Apr 2025 | €8,91 (upp), €11,38 (ned) | Viss återhämtning, fortsatt volatilitet |

**Prisfall orsak:** BESS (batterilager) har flodat marknaden. Bara i Q1 2025 växte BESS-kapaciteten i mFRR-marknaden från 120 MW till ~600 MW. FCR-D har liknande dynamik.

**Projektioner FCR-D:**
- Kort sikt (2025–2026): fortsatt låga priser, €3–15/MW/dag
- Medellång sikt (2027–2028): oklart — beror på hur mycket BESS som byggs. Eventuell återhämtning till €15–40/MW/dag om balanseras av ökad efterfrågan.
- Lång sikt: strukturellt lägre än 2022-topparna.

**Verdict för Effira: Tekniskt möjligt på lång sikt (år 4+) med hårdvarumodifiering. Ekonomiskt ointressant idag. Lägsta prioritet bland SvK-produkter.**

---

## 3. mFRR — Manuell Frekvensåterställning (PRIMÄR SvK-PRODUKT)

**Varför mFRR är den mest realistiska SvK-produkten för värmepumpsaggregering:**
1. 15-minuters responstid — värmepumpar klarar detta komfortabelt.
2. Manuell dispatch via signal (sedan mars 2025 automatiserat via mFRR EAM) — inte autonom frekvensrespons.
3. 1 MW minimum — nåbart med 250–500 OPTi-kunder (4–8 kW/pump).
4. SvK fast-trackar ansökningar ≥40 MW tom juni 2026.
5. Marknaden är nyare och ännu inte lika mättad som FCR.

**Tekniska krav:**
- Full aktivering inom 15 minuter från dispatchsignal.
- Budstorlek: ≥1 MW, i 15-minutersblock.
- Bud lämnas D-1 (dagen innan), gateclose 45 min före leveranskvarteret.
- Realtidsmätning krävs men är mindre strikt än FCR/aFRR.
- BSP (Balansserviceaktör) krävs — Effira behöver inte egen BSP-licens i närtid, kan verka under Tibbers BSP.

**Intäktsstruktur — två delar:**
1. **Kapacitetsbetalning** (mFRR kapacitetsmarknad, D-1 auktion): Betalning bara för att vara tillgänglig. Pay-as-cleared.
2. **Energibetalning** (mFRR EAM, aktiveringsmarknad): Tillägg vid faktisk aktivering. Spotbaserat pris.

### Prisutveckling mFRR

| Period | Kapacitetspris | Aktiveringspris | Kommentar |
|---|---|---|---|
| Okt 2023 | Marknad öppnad | — | Kapacitetsmarknaden lanserad i Sverige |
| Feb 2024 | ~€200/MW (ned, spike) | Variabelt | SvK ökade upphandling Q2 2024 |
| Q2 2024 | Kraftig spike | €500–2 000/MWh vid aktivering | Akut nätbehov, prisspike |
| 2025 | Marknad etableras | Varierande | BESS ökar: 120 → 600 MW Q1 2025 |

**OBS:** mFRR-marknaden är nyare och datan är begränsad. Priser är mer volatila och lägre transparens än FCR.

**Uppskattad intäkt per pump (4 kW) — scenarioanalys:**

| Scenario | Kapacitetspris | Aktivering | SEK/pump/mån |
|---|---|---|---|
| Konservativt | €10/MW/dag | 50h/år × €80/MWh | ~12–18 SEK |
| Bas | €25/MW/dag | 100h/år × €120/MWh | ~30–40 SEK |
| Optimistiskt | €60/MW/dag | 200h/år × €200/MWh | ~65–90 SEK |

*Antaganden: 4 kW pump, 50% säsong, 65% duty, SEK/EUR = 11,5*

**Projektioner mFRR:**
- 2025–2026: Prisinflation pga ökad BESS-konkurrens men fortfarande attraktivare än FCR-D.
- 2027–2028: Oklart. Möjlig stabilisering om SvK ökar upphandlingsvolymerna.
- Bedömning: mFRR är Effiras primära SvK-marknad de närmaste 2–4 åren.

**Verdict: Primär SvK-produkt. Tillgänglig via Tibber BSP år 1–2.**

---

## 4. aFRR — Automatisk Frekvensåterställning

**Vad det är:** aFRR aktiveras automatiskt via en kontinuerlig setpunktsignal från SvK:s kontrollsystem — inte frekvens autonomt, utan ett värde som ändras i realtid och som resursen måste följa.

**Tekniska krav:**
- Full aktivering inom **5 minuter** från setpunktsändring.
- Initial respons inom 30 sekunder.
- **Realtids-SCADA-setpunkt** från SvK — ingen dispens möjlig. Resursen måste ta emot och följa en kontinuerlig styrsignal.
- Min-budstorlek: 1 MW.
- SvK upphandlar upp till 97 MW uppåt och 124 MW nedåt i Sverige (2025).

**Vad detta kräver av Effira:**
- Dispatch-infrastruktur som tar emot SvK-signal (via BSP) och vidarebefordrar till hela flotten med <30 sekunders latens.
- Nära-realtidsmätning av faktisk lastrespons för avräkning.
- Potentiellt undermätare på VP-kretsen (separat mätare, tillkommande hårdvarukostnad).

**Intäktsstruktur:** Kapacitetsbetalning + energibetalning vid aktivering. Kapacitetsmarknaden under uppbyggnad (2025).

**Verdict: Mer realistisk än FCR-D, men kräver signifikant infrastrukturuppbyggnad. Medellång sikt (år 2–3).**

---

## 5. Lokal Flex — Nodes / Effekthandel Väst (ENKLASTE INGÅNGSPUNKTEN)

**Vad det är:** DSO-drivna flexibilitetsmarknader där elnätsägare köper flexibilitet lokalt för att hantera flaskhalsar i nätet. Enklare regler än SvK. Ingen BSP-licens krävs.

### Effekthandel Väst (Göteborg, Nodes-plattform)
- **Köpare:** Göteborg Energi Nät och Mölndal Energi Nät.
- **Min-budstorlek:** 50 kW (10 kW granularitet) — ett tiotal pumpar räcker.
- **Produkter:** ShortFlex (timbaserad), LongFlex (längre perioder), MaxUsage (effektbegränsning).
- **Gateclose:** 2 timmar innan leverans.
- **Responstid:** ~30 minuter — värmepumpar klarar detta.
- **Onboarding:** Registrera som FSP (Flexibility Service Provider) på Nodes, signera NODES Membership Agreement, baseline-diskussion med DSO.
- **Vem kan delta:** Privata individer och aggregatorer. Sedan 2024–2025 deltar privatpersoner direkt.

### Priser (Lokal flex, generellt Europa/Sverige)
| Komponent | Typiskt intervall |
|---|---|
| Tillgänglighetsbetalning | 5–50 EUR/MW/vecka |
| Aktiveringsbetalning | 50–400 EUR/MWh |
| Geometrisk täckning | Begränsad till specifika DSO-zoner |

**Begränsning:** Lokal flex är geografiskt begränsad. Effekthandel Väst täcker Göteborg-regionen. Övriga marknader: E.ON (pilot sedan vintern 2025), sthlmflex (pilot, ej permanent ännu).

**Verdict: Lägst barriär för Effira. Starta här. Liten intäkt men kritisk för att bygga baseline-modell och driftsbevis.**

---

## 6. Intradag & Obalans (via Tibber som BRP)

**Vad det är:** Tibber (som BRP — Balansansvarig) hanterar avvikelser mellan sin day-ahead-prognos och faktisk förbrukning. Flexibla laster hjälper Tibber att undvika dyra imbalans-kostnader.

**Hur värdet skapas:**
- Tibbers dag-ahead-prognos missmatchas med verkligheten → imbalans → Tibber köper på intradagmarknaden (dyrt) eller styrs av obalansavräkning (kan bli €990–4 691/MWh vid stress).
- OPTi-flottans flexibilitet hjälper Tibber att ta igen positionen.
- Värdet är en kommersiell uppgörelse, inte ett direktmarknadspris.

**Prissättning:** Förhandlas med Tibber. Inte offentligt transparent. Sannolikt rörlig komponent baserad på undvikta imbalanspriser.

**Teknisk interface:** Dispatch-API (signal från Tibber → OPTi-fleet). Samma infrastruktur som mFRR.

**Verdict: Strategiskt viktigt som kommersiell relation med Tibber. Svårt att modellera men kan bidra 10–30 SEK/pump/mån.**

---

## 7. Tibber Helhemsoptimering (STRATEGISK PRIORITET #1)

**Vad det är:** Inte en VPP-marknad — en ekosystemintegration. Tibber samordnar billaddare, batteri och värmepump i hemmet för att optimera kundens kostnad mot dynamisk tariff.

**Varför detta är Tibbers #1 prioritet:**
- Pulse + VP + billaddare = komplett hemoptimering.
- Effira i Tibbers app och ekosystem = attraktiv lösning för Tibbers kunder.
- Schema-delning och gemensam effektbalansering i hemmet mot nätavgiftstariffer.

**Intäkt för Effira:** Indirekt — kundvärde, reducerad churn, lättare sälj via Tibbers kanal. Inte direkta VPP-pengar.

**Verdict: Strategisk prioritet. Bör drivas parallellt, inte som alternativ till VPP.**

---

## 8. Effiras Tillgänglighet och Produktutveckling

### Vad Effira redan har
- Cloud-connectivity till OPTi-fleet (kan ta emot och skicka kommandon).
- Termiska modeller per hus (förutsättning för baseline-modellering och rebound-hantering).
- VP-styrning (stänga av/reglera pump).

### Produktutveckling per marknadsfas

| Fas | Marknad | Dev-behov | Hårdvara? | Tidslinje |
|---|---|---|---|---|
| 1 | Lokal flex (Nodes) | Baseline-modell, Nodes-API, dispatchreläer, responsrapportering | Nej | 3–6 mån |
| 1 | mFRR via Tibber BSP | Dispatch-API (signal in → fleet), staggerad omstart, mätaggregering | Nej | 3–6 mån (parallellt) |
| 2 | mFRR direkt (egen BSP) | D-1 budoptimering, mFRR EAM-integration, BSP-registrering | Nej | 6–12 mån mer |
| 3 | aFRR via BSP | Realtids-setpunktsföljning, <30sek flottlatens, undermätning | Möjligen undermätare | 6–12 mån mer |
| 4 | FCR-D | Inbyggd frekvensmätning, autonom respons, OPTi-hårdvaruredesign | Ja — ny hårdvara | År 3–5 |

### Rebound-hantering (kritiskt för alla marknader)
- Stäng av X pumpar i 15–60 min → byggnaden förlorar värme → pumpar kör hårdare 30–90 min efteråt.
- Löses med:
  1. **Staggerad omstart** — pumpar startar i vågor, inte simultant.
  2. **Förkonditionering** — förvärm byggnader 2–6h innan avsedd curtailment (möjligt för mFRR D-1 bud).
  3. **Konservativ budsättning** — bud 70% av nominell flottkapacitet, behåll headroom.
  4. OPTi:s termiska modeller är rätt verktyg för detta.

---

## 9. Intäktsprojektioner per Fas — Effira

| Tidpunkt | Aktiva marknader | VPP SEK/pump/mån | Total SEK/pump/mån |
|---|---|---|---|
| År 1 (lokal flex + mFRR via Tibber) | Nodes + Tibber BRP | 15–35 | 75–95 |
| År 2 (mFRR direkt + intradag) | mFRR + Tibber | 35–60 | 95–120 |
| År 2–3 (+ aFRR) | mFRR + aFRR + Tibber | 60–100 | 120–160 |
| År 3+ (full portfölj) | Alla marknader | 100–140 | 160–200 |

*Abonnemang netto: 60 SEK/pump/mån (konstant)*

### Vägen till 200 SEK/pump/mån
200 SEK kräver ~140 SEK VPP. Det kräver:
- mFRR (25–40 SEK) + aFRR (30–50 SEK) + Tibber intradag/ekosystem (20–50 SEK) + lokal flex (5–15 SEK)
- Genomsnittlig activation rate och mFRR-priser i bas-scenario.
- Nås sannolikt år 2–3 med full marknadsportfölj.

---

## 10. Marknadsaktörer och Referenscase

| Aktör | Marknad | Tillgång | Kommentar |
|---|---|---|---|
| CheckWatt/Emaldo | FCR-D → mFRR | BESS | Startade mFRR via Bixia maj 2025 |
| Tibber | FCR, mFRR, intradag | BESS + EV | Grid Rewards lanserat dec 2024 i Sverige |
| Sonnen | FCR-D Sverige | BESS | SvK-godkänd 2024 |
| Svea Solar | FCR-D | BESS + solceller | Via Sunbeam-plattform |
| sthlmflex (pilot) | Lokal flex | Bl.a. värmepumpar (Stockholm Exergi) | Visade att VP kan delta med 5–30 min respons |

---

## 11. Nyckeltermer

| Term | Förklaring |
|---|---|
| BSP | Balansserviceaktör — licensierad aktör som lämnar bud till SvK. Tibber är BSP. |
| BRP | Balansansvarig aktör — ansvarar för att prognos matchar verklighet mot eSett. |
| EAM | Energy Activation Market — mFRR:s aktiveringsmarknad (live från mars 2025). |
| FSP | Flexibility Service Provider — aktör på lokala DSO-marknader (Nodes). |
| ICCP | Realtidsdataprotokoll till SvK — krävs för FCR och aFRR. |
| Rebound | Förbrukningspik efter curtailment då pumpar kör ikapp förlorad värme. |
| Typkvalificering | SvK-process där man testar ett urval enheter och sedan lägger till fler av samma typ. |
| Upp-reglering | Minska förbrukning (stänga av pumpar) — det vi kan göra. |
| Ned-reglering | Öka förbrukning — svårt för VP på vintern, begränsad kapacitet. |
