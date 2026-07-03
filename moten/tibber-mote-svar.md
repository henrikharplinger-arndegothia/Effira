# Svar på Peters email — möte imorgon
**Förberedelse för genomgång av känslighetsmodellen**

---

## Vad Peter frågade (implicit)

1. Hur resonerade vi kring värdena i modellen?
2. Varför valde vi just dessa tjänster?
3. Vilka tekniska lösningar saknas?
4. Hur ser det ut med prequalificering ihop med andra resurser?
5. Krav på hög leveranssäkerhet — hur resonerade vi?

---

## Peters rangordning (som vi nu håller med om)

1. Tibber helhemsoptimering
2. Intradag & obalans
3. Lokal flex (Nodes, E.ON Switch)
4. mFRR upp ← mest realistisk SvK-produkt
5. aFRR upp
6. FCR-D upp

---

## Vad modellen hade rätt om

- **FCR-N borttagen** — vi exkluderade den redan med förklaringen att den kräver millisekunds-respons och realtids-frekvensstyrning. Det var rätt.
- **Grundlogiken** — en stor flotta VP:ar har flexibilitetsvärde. Håller.
- **Vi kan bara göra upp-reglering** — vi modellerade bara "upp" (pumpar stängs av). Rätt.

---

## Vad modellen hade fel

**FCR-D som primärprodukt:**
Vi valde FCR-D som primär marknad för att den hade de högsta historiska priserna. Det var ett misstag av två skäl:

1. **Teknisk:** FCR-D kräver autonom respons inom 30 sekunder utan extern signal. Pumpen måste vara igång vid aktiveringstillfället och effektmätningen måste vara exakt — ingen av dessa saker är garanterad i vår nuvarande setup.
2. **Marknadsmässig:** FCR-D-priserna kollapsade 2024–2025 pga BESS-överskott. April 2025: €8,91/MW/dag. Vår modell använde 7 EUR/MW/h (~168 EUR/MW/dag) — ca 20× för högt.

**aFRR som sekundärprodukt:**
Vi rangordnade aFRR högt. Peter rangordnar det som #5 (under mFRR). Skäl: aFRR kräver kontinuerlig SCADA-setpunktsignal från SvK — ingen dispens möjlig. Det är mer infrastruktur än vi antog.

**mFRR saknades:**
Den mest realistiska SvK-produkten för oss fanns inte alls i modellen. Det borde ha varit primärprodukten.

---

## Vår reviderade förståelse (ta med till mötet)

### Vad vi har idag (OPTi)
- Cloud-connectivity till hela flottan — kan ta emot och skicka kommandon.
- Termiska modeller per hus — rätt förutsättning för baseline-modellering och rebound-hantering.
- VP-styrning — kan stänga av/reglera pump.

### Vad vi behöver bygga (mjukvara, ingen hårdvara)
| Fas | Vad | Tidsuppskattning |
|---|---|---|
| 1 | Dispatch-API (ta emot signal från Tibber → relay till fleet) | 1–2 mån |
| 1 | Baseline-konsumtionsmodell per enhet (för avräkning) | 2–3 mån |
| 1 | Staggerad omstart-algoritm (motverka rebound) | 1 mån |
| 1 | Responsrapportering (faktisk MW levererad per event) | 1–2 mån |
| 2 | D-1 budoptimering för mFRR (automatiserad) | 3–4 mån |
| 3 | Realtids-setpunktsföljning för aFRR | 4–6 mån |

Fas 1 = lokal flex + mFRR via Tibber BSP. Ingen hårdvaruändring krävs.

---

## Frågor att ställa Peter & Kenny imorgon

**Om kommersiell modell:**
- Hur prissätter ni intradag-värdet? Rörlig andel av undvikta imbalanspriser, eller fast?
- Vilket revenueshare är rimligt för mFRR via er BSP — vad tar ni för BSP-risken?
- Hur är er Grid Rewards-modell uppbyggd idag för BESS — kan vi använda samma struktur för VP?

**Om teknisk integration:**
- Vilket API/protokoll skickar ni dispatchsignaler på? REST, MQTT, annat?
- Vad behöver ni från oss för baseline-avräkning — AMI-data (15 min), undermätning, eller kan vi leva med OPTi-intern logg?
- Vilken latens är acceptabel från er signal till fleet-respons?

**Om lokal flex:**
- Har ni relation med Nodes / Effekthandel Väst idag — kan vi komma in under er?
- E.ON Switch-piloten — har ni koll på vad de betalar och vad som krävs tekniskt?

**Om mFRR specifikt:**
- Ni har BSP-licens — hur stor portfölj behöver vi ha för att vara intressanta för er att ta med i mFRR-buden?
- Hur ser verifieringsprocessen ut — vad skickar ni vidare till SvK, och vad behöver ni från oss för det?

---

## Budskapspunkter för mötet

1. **Vi var för optimistiska om FCR-D** — vi förstår nu varför det inte är startpunkten. Marknaden, tekniken och prequalificeringskraven är alla svårare än vi antog.

2. **Vi håller med om rangordningen** — lokal flex → mFRR → aFRR. Det stämmer med vad vi kan leverera tekniskt och i vilken takt.

3. **OPTi har rätt grund** — cloud-connectivity + termiska modeller är exakt vad som behövs för baseline och rebound. Vi behöver inte bygga om från grunden, vi behöver lägga VPP-logiken ovanpå.

4. **Vi behöver er för att nå SvK** — vi har inte BSP och vill inte äga den risken i närtid. Vi vill vara sub-aggregator under er BSP.

5. **Nästa steg vi föreslår:** Definiera en minimal teknisk integration för lokal flex / mFRR via er plattform. Vad behöver ni se från oss, och när?
