# Effira OPTi — Pitch-templates för Comfort-butiker

Tre varianter beroende på lead-profil. Välj baserat på kolumnerna `se_zone` och `has_solar` i outreach-listan.

---

## Variant A — Standard (SE3, vattenburen värmepump)
**Används för:** SE3-butiker med luft/vatten- eller bergvärmepump i sortimentet (majoriteten av Tier A)

**Ämne:** Nytt verktyg för era värmepumpskunder — OPTi från Effira

---

Hej [FÖRNAMN],

Jag heter [AVSÄNDARE] och kontaktar er från Effira Energy.

Ni installerar värmepumpar och jobbar nära kunder som bryr sig om sina energikostnader. Vi tänkte ni borde känna till OPTi — en hårdvaru- och mjukvarulösning som sätts på befintliga vattenburna värmepumpar och automatiskt styr dem efter spotpriset.

**Vad det gör för er kund:**
- Skiftar värme- och varmvattenproduktion till de billigaste timmarna på dygnet
- Fungerar med ~95 % av alla vattenburna värmepumpar (NIBE, Bosch, IVT, Thermia m.fl.)
- Genomsnittlig besparing: 3 000–6 000 kr/år beroende på elpris och hushåll
- Installation ingår — vi skickar en Effira-tekniker

**Varför det är relevant för er:**
OPTi är en naturlig merförsäljning eller uppföljningsservice till kunder ni redan installerat hos. Ni äger kundrelationen — vi tar hand om teknik och support.

Skulle ni ha 20 minuter för ett samtal den här veckan? Jag berättar gärna mer och visar hur andra Comfort-butiker samarbetar med oss.

Med vänliga hälsningar
[AVSÄNDARE]
Effira Energy AB
[TELEFON] | [EMAIL]

---

## Variant B — SE4-premium (SE4, vattenburen värmepump)
**Används för:** Butiker i Skåne, Blekinge, Halland, Kalmar, Gotland (SE4 = högst elpriser = starkast ROI)

**Ämne:** Era värmepumpskunder i [STAD] betalar mest för el — vi kan hjälpa dem spara

---

Hej [FÖRNAMN],

Jag heter [AVSÄNDARE] från Effira Energy.

Ni är baserade i SE4 — elzonen med Sveriges högsta spotpriser. Det gör era värmepumpskunder till exakt rätt målgrupp för OPTi: vår styrenhet som automatiskt skiftar uppvärmning och varmvatten till dygnets billigaste timmar.

**I SE4 räknar vi med:**
- Besparing på 4 000–8 000 kr/år per hushåll (vs. SE3)
- Återbetalningstid under 2 år vid normala spotpriser
- Ännu starkare effekt under vintrar med hög prisvariation

**Hur vi arbetar med Comfort-butiker:**
Vi är öppna för partnermodeller — ni identifierar kandidater bland era kunder, vi hanterar installation och support, ni får en andel av abonnemangsintäkten.

Kan vi ta ett kortare samtal den här veckan?

Med vänliga hälsningar
[AVSÄNDARE]
Effira Energy AB
[TELEFON] | [EMAIL]

---

## Variant C — Sol-vinkel (har solceller i sortimentet)
**Används för:** Butiker som säljer både värmepump och solceller (kolumn `has_solar = 1`)

**Ämne:** Slut kretsen — OPTi styr värmepumpen på solöverskott

---

Hej [FÖRNAMN],

Jag heter [AVSÄNDARE] från Effira Energy.

Ni säljer både solceller och värmepumpar — det är precis den kombination OPTi är byggd för.

**Problemet vi löser:**
Kunder med sol + värmepump tappar ofta värde: överskottsel exporteras till lågt pris medan värmepumpen går på obekväma tider. OPTi koordinerar de två systemen automatiskt — laddar upp värme-batteriet (varmvattentanken + huset) när solen producerar, och styr om mot spotpris-dalar när den inte gör det.

**Konkret kundnytta:**
- 20–40 % mer egenkonsumtion av solelen
- 3 000–7 000 kr/år i minskad elräkning
- Fungerar med befintlig installation — inga nya sensorer krävs

Det här är en stark säljpunkt för nya sol+värmepump-affärer — en anledning för kunden att köpa hela paketet hos er.

Har ni möjlighet för ett snabbt samtal den här veckan?

Med vänliga hälsningar
[AVSÄNDARE]
Effira Energy AB
[TELEFON] | [EMAIL]

---

## Fält att fylla i

| Platshållare | Källa |
|---|---|
| `[FÖRNAMN]` | Kolumn `vd_firstname` i outreach-listan |
| `[STAD]` | Kolumn `city` |
| `[AVSÄNDARE]` | Din egen signatur |
| `[TELEFON]` / `[EMAIL]` | Effiras kontaktuppgifter |

## Hur du väljer variant

```
se_zone == 4 AND has_solar == 1  → Variant B + lägg till sol-stycket från C
se_zone == 4 AND has_solar == 0  → Variant B
se_zone <= 3 AND has_solar == 1  → Variant C
se_zone <= 3 AND has_solar == 0  → Variant A
```
