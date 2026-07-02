# Tibber — Mötesprep | Juni 2026

> Internt dokument. Effira-teamet: Henrik, Peter, Kenny.

---

## Mål

| Person | Mål |
|--------|-----|
| **Henrik** | Lämna mötet med ett muntligt eller skriftligt samarbetsavtal — definierade faser, milstolpar, nästa steg |
| **Peter** | Teknisk validering — förstå Tibbers VPP-stack, bekräfta integrationsmodellen |
| **Kenny** | Teknisk back-up — svarar detaljfrågor om OPTi, API, mätning |

**Carolina Appelqvist** är Tibbers Country Director SE/NO och en bekant till Henrik. Tonläget kan vara direkt och personligt — men pitchen ska vara skarp. Carolina sitter i ett möte för att det kan bli affär, inte för att göra en tjänst.

---

## Mötesstruktur — 60–75 minuter

| Tid | Block | Vem |
|-----|-------|-----|
| 0–7 min | Henriks pitch | Henrik |
| 7–25 min | Tibbers reaktion — deras VPP-setup, syn på värmepumpar | Dialog |
| 25–45 min | Teknisk genomgång — integrationsmodell, API, mätning | Peter + Kenny |
| 45–65 min | Kommersiellt upplägg + pilotstruktur | Henrik |
| 65–75 min | Nästa steg — vad vi landar på idag | Henrik |

**Taktik:** Tibbers frågor om Effiras teknologi svaras direkt och kort. CTO:s egna frågor om hur Tibber fungerar lyfts i block 2 — inte som ett förhör utan som en naturlig dialog om hur det ska hänga ihop.

---

## Henriks pitch — 5–7 minuter

*Levereras stående eller med ett papper på bordet. Inga slides behövs.*

---

**Öppning**

> "Carolina — kul att vi äntligen sitter ner för det här. Ni har byggt Grid Rewards och ett riktigt VPP. Vi har byggt den sak ni förmodligen saknar: robust, komfortsäker styrning av värmepumpar som faktiskt fungerar i 95% av alla svenska villor. Det är därför vi är här."

---

**Vad Effira har**

OPTi kopplar upp vattenburna värmepumpar och ger Effira förmågan att styra dem — med ett komfortskydd som är inbyggt i systemet, inte ett marknadsföringsbudskap.

- Fungerar med NIBE, Bosch, IVT, Thermia, Mitsubishi — ~95% av den svenska marknaden
- Styr uppvärmning och varmvatten — ~75% av ett hushålls totala elförbrukning
- Stänger av en pump inom **30 sekunder** och håller den av i **60–90 minuter** vid normala förhållanden
- **150 enheter live. 1 750 i lager. 2 000 i december.**

---

**Varför det är relevant för Tibber**

Ni har idag batterier, laddboxar och elbilar i ert VPP. Det är bra. Men värmepumpar är tio gånger vanligare i svenska hem än hemsbatterier — och de passar FCR-D perfekt: av inom 30 sekunder, håll 15 minuter.

> 100 000 pumpar = **130 MW** styrbar kapacitet.
> Det förändrar skalan på er VPP-affär.

---

**Modellen**

Vi säljer inte en färdig balanstjänst. Vi erbjuder tillgång till **flexibilitetslagret i värmepumpen**.

- Tibber avropar: *"minska last med X kW under Y minuter"*
- Effira svarar om kapaciteten finns — och genomför styrningen via OPTi
- Ni äger kundupplevelsen, appen, elavtalet och dispatch-logiken
- Vi äger styrningen, komfortskyddet, installationen och lokal logik

Ingen konkurrens om kundrelationen. Ingen överlappning.

---

**Vad vi vill**

> "Vi vill göra en pilot. 100–200 Tibber-kunder med värmepump. Vi sätter upp integrationen, mäter resultatet, och lägger en kommersiell principmodell på plats. Det är vad vi vill komma överens om idag."

---

## Förberedda svar på Tibbers sannolika frågor

**"Hur många enheter har ni idag?"**
150 live, 1 750 i lager, väg mot 2 000 i december. En pilot på 100–200 enheter kan starta omgående — hårdvaran finns.

**"Vilka värmepumpar fungerar?"**
NIBE, Bosch, IVT, Thermia, Mitsubishi — ~95% av vattenburna pumpar. Bergvärme, luft/vatten, frånluft. Inte luft/luft.

**"Hur snabbt kan ni styra ner lasten?"**
Inom 30 sekunder. FCR-D-kompatibelt.

**"Hur länge kan ni hålla pumpen av?"**
60–90 minuter vid 0°C i normallisolerat hus. 2–4 timmar i vällisolerat. Vi aktiverar aldrig om inte termisk buffert redan finns — det är konstruktionsgarantin, inte ett löfte.

**"Kan ni öka last, eller bara minska?"**
Båda. Vi kan förladda huset (förvärma) för att bygga buffert — sedan stänga av. Det ger längre dispatchfönster och är optimalt för FCR-D.

**"Hur mäter ni faktisk effekt?"**
OPTi läser pumpens faktiska effektuttag via pumpens API — före och efter kommando. Delta = bevisad reducering. Realtidsmätare installeras vid varje enhet.

**"Hur hanterar ni reboundeffekten?"**
Huset är en värmebuffert. Vi aktiverar bara när bufferten är tillräcklig. Vid portföljnivå jämnas individuell rebound ut statistiskt — vi binder oss till 80% av beräknad kapacitet och levererar konsekvent mer.

**"Måste kunderna vara Tibber-kunder?"**
För en första pilot — troligen ja, det ger er kontroll över kundupplevelsen. Långsiktigt kan modellen fungera oberoende av elleverantör. Vi lyssnar gärna på er syn på det.

**"Vem äger kunden, datan, supporten?"**
Effira äger kundrelationen, installationen, supporten och styrlogiken. Tibber äger dispatch-logiken, appen och kundupplevelsen. Ingen dubbelexponering.

**"Vad kostar det?"**
OPTi: 3 000 kr + 129 kr/mån, installation ingår. I ett pilotupplägg diskuterar vi subventionsmodell.

**"Vad vill ni ha från Tibber?"**
Tre saker: ett pilotkundssegment (Tibber-kunder med värmepump), teknisk integration (er dispatch-API-spec), och en kommersiell principmodell att skala från.

---

## Om mötet fastnar

**Om Tibber bromsar på "vi behöver tänka":**
> "Vad behöver stämma för att det ska vara värt att testa? Låt oss backa från det."

**Om de fastnar på teknisk osäkerhet:**
Kenny tar det. Henrik och Peter håller den kommersiella tråden levande — tekniken är inte hindret, viljan är frågan.

**Om de ifrågasätter skalan (150 enheter):**
> "Det är poängen med en pilot — ni ska inte ta vår kapacitet för given. Piloten är beviset. Vi har hårdvaran, vi har tekniken, vi behöver ett gemensamt ramverk."

---

## Stängningsfrågan

Om mötet har gått bra och Tibber är positiva:

> "Kan vi enas om att formulera ett Letter of Intent inom två veckor? Vi skriver ett förslag och skickar till dig, Carolina."

Sätt datum i rummet.
