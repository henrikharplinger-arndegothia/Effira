# Daikin Partner Pipeline — Summary Report
Datakällor insamlade 2026-05-05

## Metod och datakällor

### API-undersökning
Daikins återförsäljarsida (daikin.se) är JavaScript-renderad. Inga fungerande API-endpoints:
- https://www.daikin.se/api/dealers -> 404
- https://sbm-cp.daikin.eu/api/partners?country=SE -> ej tillgänglig

Daikin Stand By Me (sbm-cp.daikin.eu) är ett certifieringsprogram för tekniker (R32/R290 f-gascertifikat), inte en partnerlista.

Daikin.se har strukturerade URL:er: daikin.se/sv_se/privatkund/hitta-aterforsaljare-installator/{slug}/

### Insamlingsmetod
Google site-sökning per region + direkthämtning av partnerprofilsidor.

### Begränsning
Ingen komplett offentlig partnerlista eller API. Täckning god via Google-indexering men troligen inte 100%.
Daikin saknar tydliga certifieringsnivåer i Sverige — alla är "auktoriserade återförsäljare och installatörer".

## Resultat

leads_raw.csv: 17 poster
outreach_leads.csv: 17 poster (filtrerade och scorade)

### Exkluderade bolag
- Comfort-butiker, Bad & Värme, Enwell: Redan i pipeline
- Bravida, Assemblin: Enterprise-prospects

### OPTi-relevanta partners (luft/vatten eller bergvärme)
- Värme Konsulten i Sverige AB (Norberg) — luft/vatten + berg
- Kylkraft Skåne AB (Helsingborg) — luft/vatten + berg
- Centralservice i Osby AB (Osby) — luft/vatten + berg
- Energilagret - Halmstad — luft/vatten + berg
- Värmis AB (Västerås) — luft/vatten + berg
- Energioptimering i Norden AB (Skene) — luft/vatten + berg
- Teknisk Fastighetsservice Umeå — luft/vatten + berg (SE1)
Daikin Altherma = Daikins luft/vatten-serie, primärt OPTi-kompatibel.

### Tier-fördelning
- Tier A (>=6p): 0 (Daikin saknar +2p certifieringsnivå)
- Tier B (4-5p): 16
- Tier C (<4p): 1

### Elområdesfördelning
SE4: 5 | SE3: 11 | SE2: 0 | SE1: 1

## Scoring-modell
Elområde: SE4=4p | SE3=3p | SE2=2p | SE1=1p
Certifiering: Auktoriserad Daikin=+1p (ingen känd premiumtier i Sverige)
Tier A: >=6p | Tier B: 4-5p | Tier C: <4p

## Rekommenderade nästa steg
1. Verifiera om Daikin har Elite/Gold/Silver-partnerprogram i Sverige — kan lyfta SE4-partners till Tier A
2. Prioritera SE4-partners med luft/vatten: Kylkraft Skåne AB och Centralservice i Osby AB
3. Kyl- Värmepumpservice Ängelholm har personlig e-post (rune@) — direktkontakt med ägare
