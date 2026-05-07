# IVT Partner Pipeline — Summary Report
Datakällor insamlade 2026-05-05

## Metod och datakällor

### API-undersökning
IVT:s "Hitta oss"-sida är en JavaScript-renderad kartapplikation. Ingen publik API hittades:
- https://www.ivt.se/api/dealers -> 404
- https://www.ivt.se/api/partners -> 404
IVT är del av Bosch-koncernen men delar inte Bosch HomeComfort API på svensk domän.

### Insamlingsmetod
IVT har strukturerade URL:er: ivt.se/hitta-oss/{landskap}/{ort}/{bolagsnamn}/
Data insamlades via Google site-sökning och direkthämtning av partnerprofilsidor.

### Begränsning
E-postadresser sällan publicerade på IVT:s partnersidor. Behöver berikas via bolagens egna webbplatser.

## Resultat

leads_raw.csv: 42 poster
outreach_leads.csv: 42 poster (filtrerade och scorade)

### Exkluderade bolag
- Enwell (Örebro, Vetlanda, Nässjö, Karlstad): Redan i pipeline
- Comfort-butiker: Redan i pipeline
- Bad & Värme: Redan i pipeline
- Rotek AB (Vellinge): Säljer Thermia, inte IVT
- Bravida, Assemblin: Enterprise-prospects

### Certifieringsnivåer
- IVT Center: Återförsäljare med utställningslokal, djupare utbildning (+2p)
- Standard/Auktoriserad: Auktoriserad utan Center-status (+1p)

### Tier-fördelning
- Tier A (>=6p): 2 bolag (SE4 + IVT Center)
- Tier B (4-5p): 29 bolag
- Tier C (<4p): 11 bolag (SE1/SE2 Standard)

### Elområdesfördelning
- SE4: 2 | SE3: 35 | SE2: 3 | SE1: 4

### Top Tier A
1. Energitjänst VK AB (Limhamn/Malmö, SE4) — IVT Center + No1 Service + Mitsubishi-partner
   Tel: 040-15 96 96 | info@energitjanst.nu
2. Skånska Energilösningar AB (Södra Sandby, SE4) — IVT Center i Skåne
   Tel: 046-12 00 24

### Viktigaste IVT Center-nätverk
Värmekällan Väst AB / IVT Center Väst (Sävedalen): Nordens första IVT Center (1990).
Täcker: Göteborg, Kungsbacka, Trollhättan, Varberg, Falkenberg, Halmstad, Helsingborg, Ängelholm, Båstad.
Årets serviceombud IVT 2024. Tel: 010-264 60 60 | info@ivtcenter.se

## Scoring-modell
Elområde: SE4=4p | SE3=3p | SE2=2p | SE1=1p
Certifiering: IVT Center=+2p | Standard=+1p
Tier A: >=6p | Tier B: 4-5p | Tier C: <4p

## Elzon-mappning
SE4: Skåne, Blekinge (exakt matchning — "Alunda" != "Lund")
SE3: Övriga Sverige utom SE1/SE2/SE4
SE2: Gävleborg, Dalarna, Jämtland, Västernorrland
SE1: Norrbotten, Västerbotten

## Rekommenderade nästa steg
1. Berika e-post via bolagens egna webbplatser (prioritera Tier A och B IVT Center)
2. Kontakta Värmekällan Väst AB som strategisk partner — ett avtal täcker halva Sverige väster
3. Energitjänst VK AB i Malmö: IVT Center + No1 + Mitsubishi-partner = trolig hög öppenhet för OPTi
