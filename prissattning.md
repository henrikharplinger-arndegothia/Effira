# Prissättning OPTi — Pågående resonemang

**Status:** Pågående diskussion, ej beslutad. Fortsätts vid senare tillfälle.
**Senast uppdaterad:** 2026-08-25

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

## 8. Tre-kanalsmodell (tillagt 2026-08-25)

Nytt förslag: prissättning och kanalstruktur uppdelad i tre distinkta spår — elbolag, partners och konsument. Ersätter/kompletterar inte punkt 2.2 (två konsumentnivåer) utan lägger till B2B-kanalerna runt den.

### 8.1 Elbolag

| Post | Värde |
|---|---|
| Hårdvarupris till elbolag | 2 000 kr |
| — exkluderar installation | 1 000 kr (elbolaget/kund hanterar separat) |
| Abonnemang | 69 kr/mån inkl. moms |
| VPP | Revenue share mellan Effira och elbolag |

**Kostnadsanalys:** Produktionskostnad hårdvara 2 983 kr (vid 2K-volym, se avsnitt 6). Om installation (1 000 kr) dras bort eftersom elbolaget hanterar den, blir kvarvarande hårdvarukostnad **1 983 kr**. Vid säljpris 2 000 kr ⇒ **+17 kr marginal, i praktiken kostnadsneutralt** — konsekvent med målet i avsnitt 1, löst genom att flytta installationskostnaden dit den faktiskt uppstår.

**Abonnemangsekonomi:** 69 kr inkl. moms ≈ 55 kr exkl. moms. Rörlig kostnad ~18–23 kr/enhet/mån (se avsnitt 6) ⇒ nettobidrag **~32–37 kr/mån**, lägre än konsumentens 60 kr-mål. Antas kompenseras av volym (elbolagets befintliga kundbas, lägre CAC) plus VPP-delning.

### 8.2 Partners (sälj/installation)

| Post | Värde |
|---|---|
| Hårdvarupris till partner | 2 000 kr |
| Installation | Partnern utför och behåller den intäkten |
| Löpande servicebusiness | Partnern äger relationen, sätter eget pris mot sin kund (jfr avsnitt 2.4 — rev-share-logik mot partners) |
| Effiras leverans | Dashboard som verktyg åt partnern |

Samma kostnadslogik som elbolag (2 000 kr mot 1 983 kr kostnad exkl. installation ⇒ kostnadsneutralt).

### 8.3 Konsument (direkt eller via partner)

- Fortsätter **129 kr/mån**
- **Ny bas-nivå införs** (jfr avsnitt 2.2 — 99/129-tankarna, exakt nivå ej låst)
- Värdekommunikation ska vara tydlig för att undvika "kändes-som-förlust"-situationen (kopplar till avsnitt 5 — icke-monetära värden)
- **Årsbetalning-rabatt:** betala 10 månader, få 12 (~17 % rabatt). Enklare lösning än fakturerings-varianterna A–D i avsnitt 4 — löser samma problem (undvik betalning i låg-besparingsmånader) genom att kunden själv väljer betalningstillfälle, istället för ett fast säsongsschema.

**Marginalpåverkan av årsrabatt:** 129 × 10 = 1 290 kr/år mot 129 × 12 = 1 548 kr/år ⇒ **−258 kr/år (~−21,5 kr/mån)** jämfört med målet på 60 kr netto/mån. Ej ännu bedömt om detta är en medveten avvägning mot retention/kassaflöde.

### 8.4 Öppna frågor från kanalmodellen (obesvarade)

1. **Är "Partners för sälj" (2 000 kr, partner äger service) och "konsument via partner" (129 kr till Effira) samma partnertyp i två lägen, eller två separata partnermodeller** — en återförsäljarpartner (äger hela kundrelationen) och en distributionspartner (säljer/installerar, men konsumentens 129 kr går fortsatt till Effira)?
2. **Vad får Effira löpande i partnerkanalen** om partnern äger servicebusinessen — en licensavgift för dashboarden, eller är hela Effiras intäkt där en engångs-hårdvaruförsäljning nära break-even (dvs. partnerkanalen är i första hand en volymkanal för flottans VPP-kapacitet, inte en lönsam kanal i sig)?
3. **Ersätter eller kompletterar elbolagets VPP-delning Tibber-relationen?** Tar elbolaget rollen som BSP/BRP för just dessa pumpar (konkurrerar med Tibber-modellen i V4-planen), eller delar Effira med elbolaget av det man ändå får via Tibber?
4. **Är 69 kr/32–37 kr nettobidrag medvetet lägre än konsumentmålet**, med antagandet att VPP-delning och volym kompenserar, eller ska prissättningen justeras?
5. **Är 10-för-12-rabatten den slutgiltiga nivån**, givet att den äter ~36 % av det avsedda nettobidraget (60 kr → ~38,5 kr/mån för årsbetalande kunder)?

---

## 9. Besparingsgaranti — beslut: avveckla

**Beslut (2026-08-25): Besparingsgarantin (Bilaga B, gäller från 2026-06-01) avvecklas helt.** Ersätts av transparent funktionalitet, tydliga kundförutsättningar och löpande visning av uppnådd optimering — utan ekonomisk garanti. Kopplar direkt till avsnitt 5 (icke-monetära värden).

### 9.1 Underlag

- `Effira - Allmänna villkor - Bilaga B Besparingsgaranti - 2026-06-01.pdf` — gällande juridiska villkor
- `Effira_besparingsgaranti_diskussionsunderlag.docx` — internt diskussionsunderlag/kritik

### 9.2 Vad garantin i dag kräver (Bilaga B)

Fem samtidiga villkor under 12 obrutna månader:
1. Spotprisavtal + minst 0,80 kr/kWh genomsnittlig dygnsvolatilitet (SE1–SE4, Nord Pool Day-Ahead)
2. Över 7 000 kWh/år i uppvärmning
3. ≥98 % effektiv drift (Effiras styrsystem)
4. Besparingsläge hela perioden — komfort-/balanserat läge diskvalificerar
5. Obrutet abonnemang, ingen paus/avbrott

Mål: 3 600 kr besparing/12 mån. Ersättning = Målbesparing − Faktisk besparing (min 0), utbetalas som **krediter** (ej kontant) mot framtida abonnemang — icke återbetalningsbara, icke överlåtbara, förfaller vid uppsägning. Force majeure-undantag vid extrema marknadsförhållanden.

### 9.3 Varför den avvecklas — kärnargument

1. **Samma strukturella problem som customer-facing rev-share (avsnitt 2.3).** Baseline är en modellberäkning kunden inte själv kan verifiera — samma rotorsak till misstro/supportärenden som redan diskvalificerade rev-share mot kund. Garanti och rev-share är två förklädnader av samma sårbarhet.
2. **Garantin motverkar den nya värdestrategin.** Kravet på konstant besparingsläge diskvalificerar komfortläge — dvs. straffar kunden för att använda just de funktioner (komfort, kontroll) som identifierats som kandidater för icke-monetärt värde (avsnitt 5).
3. **Golv uppfattas som tak.** 3 600 kr är ett garanterat *minimum*, men kunder tolkar det som ett *maximum* ("mer än så sparar jag inte") — motsatt effekt av avsikten.
4. **Svag konvertering i säljögonblicket.** Fem villkor är svåra att förklara vid köp; få kunder uppfyller sannolikt alla samtidigt, vilket gör garantin mer friktion än säljargument.
5. **Dold operativ kostnad.** Manuell hantering av avtalsstatus, drift, Wi-Fi, läge, förbrukning, volatilitet och baseline vid varje tvist — skalar dåligt, saknas i kostnadsunderlaget i avsnitt 6.
6. **Krediter känns svagare än ersättning.** Ej kontanta, förfaller vid uppsägning — kunden kan hoppa av innan värdet går att använda, trots att Standard/Flex idag saknar bindningstid.

### 9.4 Öppen fråga efter avveckling

Om garantin tas bort helt, vad ersätter 3 600 kr-siffran som konkret "hook" i säljögonblicket? Kopplar till öppen fråga 6 nedan (positionering/marknadsföring givet att OPTi historiskt sålts som en "spara pengar"-produkt).

---

## 10. Styrelsemöte torsdag 2026-08-27 — agenda, beslutsunderlag och kommentarer till anställda

### 10.1 Bakgrund

Två dokument har tagits fram av anställda inför mötet:
- `Diskussionsunderlag_OPTi_Ny prissättning.docx` (ursprungsunderlaget, modeller A/B/C)
- `effira_opti_prissattning_2026_presentation_v4.html` (presentation, 24 aug — lägger till Modell D "Bas/Premium" 69/99 kr, rekommenderar D)

Båda dokumenten är **inte uppdaterade** med besluten som fattats i detta arbetsdokument (avsnitt 2, 8, 9). De känner varken till tre-kanalsmodellen, det redan avfärdade rev-share-mot-kund-resonemanget, eller det redan tagna beslutet att avveckla besparingsgarantin med specifika motargument (avsnitt 9).

### 10.2 Föreslagen agenda till styrelsemötet

1. **Bakgrund och problem** — dagens höga köpbarriär (6 995 kr Standard), besparingsgarantins svaghet (avsnitt 9), behov av volym.
2. **Beslut: besparingsgarantin avvecklas** — presentera avsnitt 9.3 (kärnargument) som färdigt beslutsunderlag, inte öppen diskussion.
3. **Beslut: ingen revenue-share mot slutkund** — presentera avsnitt 2.3 som färdigt beslutsunderlag. Vikigt att A/B (från anställdas underlag) inte diskuteras som öppna alternativ — de är redan avfärdade med konkreta skäl.
4. **Prisnivå för konsumentabonnemang** — **öppen fråga att lösa nu**: 99/129 kr (ditt spår) vs 69/99 kr (anställdas D-förslag). Se 10.4 nedan — vi tar denna direkt efter detta avsnitt.
5. **Tre-kanalsmodellen** — presentera avsnitt 8 (elbolag, partner, konsument) som det nya ramverket runt prisnivån — anställdas underlag känner bara till en kanal (konsument).
6. **Hårdvarupris** — kostnadsneutralitet vid 2 000 kr (exkl. installation) vs anställdas 3 500/2 750 kr utgångspunkt — kräver beslut om vilket pris som gäller i respektive kanal.
7. **Öppna frågor kvar att besluta** (avsnitt 7 och 8.4) — lista dem som "till nästa möte", inte som blockerande för lansering.

### 10.3 Kommentarer till anställda (för avstämning innan/efter mötet)

- **Bra jobbat med Modell D** — den landar på samma slutsats vi redan kommit fram till (fast pris, ingen beräkningsberoende debitering) via ett annat resonemang (operationell risk snarare än icke-monetärt värde). Bra oberoende bekräftelse.
- **Prisnivån i D (69/99 kr) matchar inte vårt mål** (99/129 kr, 60 kr netto/mån). Behöver stämmas av — se 10.4.
- **Tre-kanalsmodellen (elbolag/partner/konsument) saknas i underlaget.** Deras analys utgår från en enda kanal (konsument, eget köp av hårdvara 3 500 kr). Behöver bygga in elbolags- och partnerspåren i nästa version.
- **Hårdvarupriset (3 500/2 750 kr) är inte avstämt mot kostnadsneutralitets-analysen** (2 000 kr exkl. installation ≈ break-even). Be dem räkna om marginalerna med rätt kostnadsbas innan nästa version.
- **Besparingsgarantins avveckling bör motiveras med de konkreta argumenten i avsnitt 9.3** (särskilt "golv uppfattas som tak" och konflikten med komfortläge) snarare än bara "svår att förklara" — starkare underlag för styrelsen.
- **Fråga tillbaka till dem:** har de sett den nya kanalmodellen och besparingsgaranti-beslutet innan de gjorde presentationen, eller jobbar vi i två spår som behöver synkas snarast?

### 10.5 Fyra diskussionspunkter för mötet

**1. Hårdvarukostnad**
Nytt pris: **2 000 kr** (ersätter 3 500/2 750 kr i anställdas underlag). Produktionskostnad 2 983 kr vid 2K-volym, men installation (1 000 kr) hanteras separat av kanalen (elbolag/partner). Kvarvarande kostnad 1 983 kr vid 2 000 kr säljpris ⇒ **i praktiken kostnadsneutralt** (+17 kr). Gäller elbolags- och partnerkanalen.

**2. Abonnemang och betalning — konsument**
**99/129 kr**, inte anställdas 69/99 kr. Tier-logik: 99 kr (Bas) = komfort, styrning, kontroll, smart integration. 129 kr (Premium) = Bas + spotprisoptimering och effekttariffer. Ingen rev-share mot kund, ingen besparingsgaranti. Årsbetalning ger rabatt (10 månader betalas, 12 levereras).

**3. Betalning mot partner**
Partner köper hårdvara för 2 000 kr, utför och behåller installationsintäkten, äger den löpande kundrelationen och sätter eget pris mot sin slutkund. Effira levererar dashboard som verktyg. Rev-share accepteras här (till skillnad från konsument) eftersom partnern bär väder-/prisrisken själv.

**4. Betalning mot energibolag**
Energibolag köper hårdvara för 2 000 kr (exkl. installation), betalar 69 kr/mån abonnemang, samt delar VPP-intäkt med Effira. Lägre nettobidrag per enhet (~32–37 kr vs 60 kr-målet för konsument) — kompenseras av volym via energibolagets befintliga kundbas och VPP-delningen.

**5. Beräkning — vad innebär beslutet**

| Kanal | Hårdvara (intäkt−kostnad) | Abonnemang/mån | Nettobidrag/mån | Anmärkning |
|---|---|---|---|---|
| Konsument – Bas | 2 000 kr / kostnadsneutralt* | 99 kr | ~lägre än Premium | *vid 3 500 kr hårdvara: högre marginal men högre köpbarriär |
| Konsument – Premium | samma som ovan | 129 kr | ~60 kr (mål) | Referens-nivå för hela modellen |
| Partner | 2 000 kr / ~+17 kr | Partnerns eget pris | Ej Effiras — engångsintäkt hårdvara + ev. rev-share | Effiras vinst främst i flottans VPP-kapacitet |
| Elbolag | 2 000 kr / ~+17 kr | 69 kr | ~32–37 kr | Lägre än mål, kompenseras av volym + VPP-delning |

**Vad det innebär i klartext:** Effira tjänar mest per kund i konsumentkanalen (direkt), mindre per kund i elbolags-/partnerkanalen — men dessa kanaler ger lägre CAC, snabbare volym och flottstorlek för VPP-tröskeln (~250 enheter/1 MW). Modellen bygger medvetet in en avvägning: lägre marginal per enhet i B2B-kanalerna mot högre volym och snabbare väg till VPP-intäkt.

### 10.4 Beslut: prisnivå och tier-innehåll (99/129 kr)

**Beslutat (2026-08-25):** 99/129 kr fastställs, med tydlig innehållslogik per nivå — detta är inte längre en öppen fråga, utan ett beslut att föra fram på styrelsemötet.

- **99 kr — Bas:** komfort, styrning, kontroll, smart integration. Bevisar produktens värde utan att referera till kr-besparing (kopplar till avsnitt 5 — icke-monetära värden).
- **129 kr — Premium:** allt i Bas + spotprisoptimering och effekttariffer, dvs den faktiska besparingskapabiliteten.

Anställdas Modell D (69/99 kr) är fel prissatt och saknar denna tier-logik — de har byggt en fast-pris-struktur som liknar er modell, men utan kännedom om de fastställda nivåerna eller bas/premium-innehållet. Kommentar till anställda: uppdatera till 99/129 kr med tier-innehållet ovan, inte 69/99 kr.

---

## 7. Öppna frågor att ta upp nästa gång

1. Vilka icke-monetära värden (trygghet, insyn, automatik, grönt bidrag, förutsägbarhet) är redan starka i produkten idag — vilka kräver nybyggnation?
2. Om icke-monetära värden byggs upp tillräckligt starkt — går vi tillbaka till platt 129 kr/månad året runt, eller behålls ändå säsongsanpassad fakturering som en extra "känns rätt"-faktor?
3. Exakta nivåer för bas/premium (99/129 kr eller andra belopp) — ej låst.
4. Mars — betalmånad eller ej?
5. Pumpavstängningsklausul — går vidare med (c) obligatoriskt + (b) senare, eller finns invändningar?
6. Hur kommuniceras/positioneras det nya värdeerbjudandet i marknadsföring och i onboarding, givet att OPTi historiskt sålts som en "spara pengar"-produkt?
7. Se avsnitt 8.4 för öppna frågor kopplade till den nya kanalmodellen (elbolag/partner/konsument).
