# Prissättning OPTi — Pågående resonemang

**Status:** Pågående diskussion, ej beslutad. Fortsätts vid senare tillfälle.
**Senast uppdaterad:** 2026-08-24

**Källdokument:**
- `Diskussionsunderlag_OPTi_Ny prissättning.docx` (tidigare underlag, se sammanfattning nedan)
- `Kostnader-2026-08-20.xlsx` (kostnadsdata, se sammanfattning nedan)
- VPP-material (`VPP/styrelseplan-aug2026-v4.html`, `VPP/v3-antaganden.md`, `vpp-teknisk-berakning.md`)

---

## 1. Utgångsläge och mål

- **Hårdvara ska vara kostnadsneutral.** Effira är inte ett bolag som ska tjäna på hårdvaran.
- **Abonnemang: ~129 kr/månad från kund**, varav Effira ska sitta kvar med **~60 kr netto per enhet och månad**.
- Nuvarande revenue-share-modell (se hemsidan, Modell A: 30 % av besparing) skapar många månader där kunden upplever lågt/obefintligt värde (sommar), vilket vi vill motverka.

---

## 2. Beslut hittills

### 2.1 Ingen kombination av fast + rörlig avgift
Hybridmodellen (Modell B: 49 kr + 30 % av besparing) avvisas. Den skapade "juli-problemet" — kund betalade ~65 kr för ~52 kr besparing, dvs gick back ~13 kr. Att kombinera fast och rörlig avgift på en produkt som OPTi bedöms som fel väg.

### 2.2 Två fasta abonnemangsnivåer istället för rörlig modell
Förslag: **99 kr och 129 kr** (exakta nivåer ej låsta).

- **129 kr (premium)** ska innehålla **spotprisoptimering och effekttariffer** — dvs mer avancerad optimering, vilket motiverar prisskillnaden funktionellt (inte bara kosmetiskt).
- **99 kr (bas)** = grundfunktion, styrning mot baseline.

### 2.3 Ingen revenue-share mot slutkund — argument mot
Beslutat: vi tror inte på rev-share mot kund. Skäl som identifierats i resonemanget:

1. **Oförutsägbar intäkt.** Investerare/styrelse vill se recurring revenue som går att modellera. Rev-share kopplar Effiras intäkt till väder och elpris — variabler ingen på Effira styr. VPP är redan den prestationsbaserade intäktskällan (mot nätet) — att göra samma sak mot kunden är en dubblering av samma mekanism, inte ett komplement.
2. **Kunden kan inte verifiera baseline-beräkningen själv.** När siffran känns fel (även om matematiskt korrekt) blir det supportärenden och misstro.
3. **Skalar dåligt operationellt.** Varje kund blir en unik beräkning istället för en produkt med ett pris.
4. **Sommar/vinter-snedheten är strukturell, inte en bugg att laga.** Fast pris tar bort problemet helt istället för att flytta runt det (vi testade flera faktureringsupplägg för att lösa det — se avsnitt 4 — och kom fram till att faktureringsteknik inte löser ett grundläggande värde-problem).

### 2.4 Revenue-share mot PARTNERS — accepteras, annan logik
Partners äger sin egen kundrelation och ska ha frihet att prissätta som de vill mot sin kund. Rev-share från partner till Effira blir då ett grossistpris-mekanism, inte en kundvänd modell — annan riskprofil. Effira tar inte på sig väderrisken; partnern gör det, om de själva väljer rörlig prissättning mot sin slutkund.

---

## 3. Pumpavstängning i avtalet (förutsättning för balanstjänster/VPP)

Kontraktet med kund måste ge Effira rätt att stänga av/reglera pumpen kortvarigt — detta krävs för att kunna delta i balanstjänster (mFRR m.fl., se VPP-underlaget). Tre varianter diskuterade:

**(a) Rabatt för opt-in**
Kund får lägre pris om de opt:ar in på avstängning.
→ Skeptisk hållning: detta innebär att Effira tar en kostnad (lägre pris) *innan* VPP-intäkten är bevisad eller flödar. Samma risk som rev-share mot kund, fast i omvänd riktning — lovar bort pengar mot en ej säkerställd framtida intäkt.

**(b) Tibber-stil "Grid Rewards"**
Kund får utbetalning/ersättning kopplad till faktisk levererad flexibilitet, när VPP-intäkter är reella (Fas 2/3, när Tibber-avtalet aktiveras, ~höst 2028 enligt V4-planen).
→ Tydlig, mätbar ersättning ("du fick 340 kr förra året för din flexibilitet"). Passar bäst **när intäkten faktiskt finns**, inte innan.

**(c) Opt-in/civic-ramning**
Samtyckesbaserad klausul utan ekonomisk koppling: "Effira kan pausa/reglera din pump kortvarigt inom komfortgränser för att bidra till elnätets stabilitet."
→ **Rekommenderas som obligatorisk del av grundavtalet från dag 1**, inte som frivilligt tillval. Annars blir flottan för fragmenterad för att nå den tröskel (~250 pumpar / 1 MW) som krävs för mFRR-auktioner (se `vpp-teknisk-berakning.md`).

**Föreslagen ordning:** (c) obligatoriskt i avtalet nu. (b) läggs på som separat, tydligt kommunicerat lager när VPP-intäkten är reell. (a) avvisas — för riskabelt att lova bort intäkt idag.

*Ej slutgiltigt beslutat — fortsätt resonemanget vid nästa tillfälle.*

---

## 4. Faktureringsupplägg — resonemang (delvis övergivet spår, se avsnitt 5)

### Utgångspunkt
Kunden ska betala årligen, men betalningen ska läggas i månader med hög besparing/synligt värde, inte i månader med låg besparing.

**"Ok"-månader (kan debiteras):** oktober, november, december, januari, februari, april
**"Förbjudna"-månader (ingen debitering):** maj, juni, juli, augusti, september
**Mars:** grå zon, ej beslutad

### Alternativ som diskuterades

**A) Engångsfaktura** (hela årsbeloppet en gång, t.ex. nov/dec)
- + Enklast att kommunicera och administrera
- − Stort engångsbelopp kan kännas tungt, ger Effira en enda kassaflödesspik/år

**B) Flat rate spridd över de 6 goda månaderna** (t.ex. 258 kr/mån okt–feb+apr, 0 kr maj–sep)
- + Jämnare kassaflöde än A, betalning aldrig kopplad till låg besparing
- − Dubblerad månadssiffra kan se skrämmande ut även om årssumman är oförändrad

**C) Två delbetalningar** (halvårsvis, t.ex. nov + feb)
- + Balans mellan A och B — mindre chock än engångsbelopp, färre transaktioner än B

**D) Säsongsviktat fast schema** (belopp varierar per månad, förutbestämt, ej kopplat till verifierad besparing men speglar besparingskurvan grovt — t.ex. dec/jan högre än april)
- **Avvisat: "känns krångligt"** — bedömdes vara onödigt komplicerat.
- Ingen känd precedent hittades för exakt denna modell (viktad efter säsong).
- Enklare säsongsbetalning (flat, bara vissa månader) **har** precedent: lantbruksfinansiering (betalning kopplad till skördemånader), snöröjning/gräsklippning (fakturering bara under leveranssäsong).
- Egen precedent finns redan: Modell C:s sommarkampanj (köp i maj → fria sommarmånader → första faktura 1 okt) är i praktiken samma princip, redan validerad för nya kunder.

**Status:** Denna tråd (exakt faktureringsschema) pausades när ett mer grundläggande omtag identifierades, se avsnitt 5.

---

## 5. Centralt omtag (senaste vändpunkten i resonemanget)

**Insikt:** Om produktens enda värde är kr-besparing, kommer det *alltid* finnas månader där priset känns fel — oavsett faktureringsschema. Att flytta betalningstillfället löser inte grundproblemet, det flyttar bara smärtan (juli → april → etc.). Det går inte att fakturerings-teknikera bort ett svagt värdeerbjudande.

**Ny riktning:** Bygg värden i produkten som **inte varierar med väder/elpris**, starka nog att kunden inte utvärderar/säger upp abonnemanget baserat på månadens kr-besparing. Om detta lyckas kan man potentiellt gå tillbaka till en enkel, platt avgift året runt (ingen säsongslogik behövs alls) — priset blir då som att betala för Spotify eller ett larmabonnemang: tillgång/trygghet/kontroll, besparing är bonus.

### Kandidater till icke-monetära värden (under diskussion, ej prioriterade)

- **Trygghet/drifttillsyn** — OPTi upptäcker pumpfel, larmar innan huset blir kallt eller innan dyr reparation blir akut.
- **Kontroll/insyn** — appen visar historik, jämförelse mot liknande hus ("du använder 15 % mindre än snittet").
- **Automatik/enkelhet** — "sätt och glöm", kunden slipper själv tänka på elpriser och styrning.
- **Grönt bidrag** — kopplar direkt till pumpavstängnings-frågan (avsnitt 3): "du är med och gör elnätet stabilare och grönare." Ingen extra kostnad att kommunicera eftersom infrastrukturen för VPP redan byggs.
- **Förutsägbarhet** — jämnare, kända kostnader istället för att gissa vad uppvärmningen kostar månad till månad.

**Öppen fråga (obesvarad, ta upp nästa gång):**
Vilka av dessa värden är redan starka i produkten idag, och vilka skulle kräva att Effira bygger något nytt (t.ex. felvarningar, jämförelsedata) för att kunna stå för det på riktigt?

**Notering:** Detta är inte längre bara en prisfråga — det blir också en positionerings-/marknadsföringsfråga: vad OPTi säljs som idag ("du sparar pengar") kontra vad det kanske borde säljas som ("kontroll, trygghet och bidrag till elnätet — besparing är bonus").

---

## 6. Bakgrundsdata från källdokumenten (för referens)

### Från `Diskussionsunderlag_OPTi_Ny prissättning.docx`
- Nuvarande besparingsgaranti är svår att förklara (årsvis uppföljning, gäller bara första året, ersättning = fria månader ej pengar) → föreslås tas bort helt.
- Hårdvara idag: 3 500 kr inkl. moms (kampanjpris 2 750 kr).
- Besparingsberäkning: baseline vs. faktisk kostnad, kräver kvartsprisavtal.
- Central årsprofil (modellbedömning, ej kundlöfte): **~3 748 kr/år per aktiv kund** i besparing. Tidigare påståenden om 6 000–12 000 kr/år ska INTE användas utan nytt stöd.
- Tre gamla modeller (A/B/C) — se avsnitt 2 för varför A och B avvisas i nya resonemanget.
- Förutsättningar innan lansering: Kustom/Klarna/kort måste klara månadsvis variabel debitering; tydliga villkor för beräkningsmodell; transparens i app före debitering.

### Från `Kostnader-2026-08-20.xlsx`
**Hårdvara (exkl. moms), vid 2K volym:**
| Komponent | Kostnad |
|---|---|
| SG-A | 1 183 kr |
| SG-T | 450 kr (för dyr, bör ersättas) |
| P1/HAN/Kamstrup | 200 kr |
| Installation | 1 000 kr |
| Frakt | 150 kr |
| **Totalt** | **2 983 kr** |

**Löpande tjänstekostnader (exkl. moms):**
| Post | Fast/mån | Per enhet/mån |
|---|---|---|
| SaveEye | 1 500 kr | 8 kr |
| Onomondo (SIM, min. 2 000 SIM committed) | 16 600 kr | 10 kr |
| Serverdrift | ej beräkningsbart ännu vid låga volymer | — |
| **Totalt** | **18 100 kr** | **18 kr** |

→ Vid 129 kr/mån abonnemang och ~18 kr rörlig kostnad/enhet: bruttomarginal ~111 kr/enhet innan fast kostnad slås ut. (Målet "60 kr netto" i avsnitt 1 tyder på ytterligare kostnadsposter, t.ex. andel av fast kostnad eller supportkostnad, som inte är fullt specificerade i detta underlag.)

### Från VPP-underlaget (kontext för pumpavstängningsfrågan)
- mFRR (Svenska Kraftnäts primära balansmarknad) kräver att flottan kan levereras statistiskt pålitligt — minimibud 1 MW ≈ 250 pumpar.
- VPP-intäkter aktiveras enligt plan **hösten 2028** (Fas 2 i styrelseplanen).
- Tibber agerar BSP (Balance Service Provider) och BRP; kommersiellt avtal inkluderar Grid Rewards-liknande ersättning — värmepumpar är "coming soon" i Tibbers eget program (juni 2025).

---

## 7. Öppna frågor att ta upp nästa gång

1. Vilka icke-monetära värden (trygghet, insyn, automatik, grönt bidrag, förutsägbarhet) är redan starka i produkten idag — vilka kräver nybyggnation?
2. Om icke-monetära värden byggs upp tillräckligt starkt — går vi tillbaka till platt 129 kr/månad året runt, eller behålls ändå säsongsanpassad fakturering som en extra "känns rätt"-faktor?
3. Exakta nivåer för bas/premium (99/129 kr eller andra belopp) — ej låst.
4. Mars — betalmånad eller ej?
5. Pumpavstängningsklausul — går vidare med (c) obligatoriskt + (b) senare, eller finns invändningar?
6. Hur kommuniceras/positioneras det nya värdeerbjudandet i marknadsföring och i onboarding, givet att OPTi historiskt sålts som en "spara pengar"-produkt?
