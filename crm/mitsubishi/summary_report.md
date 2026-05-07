# Mitsubishi Electric Partner Pipeline — Summary Report
Datakällor insamlade 2026-05-05

## Metod och datakällor

### API-undersökning
Mitsubishis återförsäljarsida är JavaScript-renderad. Autentiseringsendpoint hittades
(/api/auth/login?returnTo=%2Faterforsaljare) men ingen publik data-API.

Mitsubishi Electric har strukturerade URL:er: mitsubishielectric.se/aterforsaljare/{slug}/

### Insamlingsmetod
Google site-sökning + direkthämtning av partnerprofilsidor + kompletterande webbsökning.

### Luft/vatten vs luft/luft-filtrering
OPTi kräver vattenburet system. Exkluderat:
- Ios Luftvärmecenter AB (Karlskoga): 7 000 luft/luft-pumpar, ej vattenburet -> EXKLUDERAD

OPTi-relevanta ME-produkter:
- Ecodan: luft/vatten-serie (primär OPTi-kompatibel)
- Geodan: bergvärme (OPTi-kompatibel)

### Certifieringsnivåer (Mitsubishi Electric)
- Service Partner: Fördjupad kompetens, tätt samarbete med ME (+2p om verifierad)
- Auktoriserad återförsäljare: Standard (+1p)
Ingen av de insamlade profilerna identifierade sig explicit som Service Partner i profilens text.
Behöver verifieras via ME Sverige.

## Resultat

leads_raw.csv: 24 poster
outreach_leads.csv: 23 poster (exkl. luft/luft-only)

### Exkluderade bolag
- Ios Luftvärmecenter AB: Primärt luft/luft, ej vattenburet
- Comfort, Bad & Värme, Enwell: Redan i pipeline
- Bravida, Assemblin: Enterprise-prospects

### Kommentar: Kungälvs Rörläggeri AB
260 anst, 8 kontor (Borås/Gbg/Jkpg/Malmö/Sthlm) — stor aktör men ej Bravida/Assemblin-kategorin.
Inkluderat i leads_raw men ej outreach_leads. Utvärderas separat som strategisk partner.

### Tier-fördelning
- Tier A (>=6p): 0 (Service Partner-status ej verifierad, alla =+1p)
- Tier B (4-5p): 20
- Tier C (<4p): 3

### Elområdesfördelning
SE4: 6 | SE3: 14 | SE2: 2 | SE1: 1

### Top Tier B leads (SE4 = 5p)
1. Siverssons VVS & Värme AB (Åhus) — luft/vatten + berg, Skåne
2. JS Energi / JS Energi Service AB (Helsingborg) — 20+ cert tekniker, luft/vatten + berg
3. Lindsells AB (Löddeköpinge) — kategori 1-behörighet, 50+ år, luft/vatten
4. EkoEnergi AB (Lomma) — luft/vatten + berg, Skåne
5. A4U I Skåne AB (Teckomatorp) — 400+ installationer, lokal familjeverksamhet
6. Energitjänst VK AB (Limhamn) — multi-brand (IVT+ME+Bosch), hög OPTi-relevans

## Scoring-modell
Elområde: SE4=4p | SE3=3p | SE2=2p | SE1=1p
Certifiering: Service Partner=+2p (ej verifierad) | Auktoriserad=+1p
Tier A: >=6p | Tier B: 4-5p | Tier C: <4p

## Rekommenderade nästa steg
1. Verifiera vilka som är "Service Partners" via ME Sverige -> kan lyfta SE4-bolag till Tier A
2. JS Energi (Helsingborg) som volympartner — 20+ tekniker, luft/vatten + berg
3. Berglunds Rör i Vegby AB (Gällstad) — bergvärme-specialist, Borås-täckning
4. Borås Elektrokyl-Energiteknik erbjuder sol-el + styrsystem -> naturlig ingång för OPTi-samtal
