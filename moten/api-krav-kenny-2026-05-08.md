# Effira Customer API — Kravspecifikation för produktionslansering

**Datum:** 2026-05-08
**Från:** Henrik Harplinger
**Till:** Kenny Eliasson (Technical Lead)
**Kontext:** HA- och Homey-integrationer är klara från vår sida och väntar på ett stabilt produktions-API.

---

## Bakgrund

Vi har byggt klart följande:

- **Home Assistant-integration** (HACS-paket): OAuth-login, asset discovery, 4 sensorer med riktig API-data, 4 tjänster (boost/stop/normal/clear), blueprint för automationer
- **Homey-app** (skeleton): samma API-logik, pair-flow, flow cards
- **Kod för OAuth-flödet** är helt klar — väntar bara på att redirect-URI:n registreras

Allt detta är blockerat av att API:et fortfarande pekar på testmiljön (`unstable-app.enerflex.cloud`) och saknar de garantier som krävs för att publicera på HACS, Homey App Store och framöver HA official.

---

## Krav

### 1. Akut — måste vara klart innan vi kan lansera

| # | Krav | Detalj |
|---|---|---|
| A1 | **Registrera HA redirect-URI i Cognito** | Lägg till `https://my.home-assistant.io/redirect/oauth` som tillåten redirect URI i app-klienten `4fmn375d1uhammpa9j3rld9kum`. Tar ~30 sekunder i AWS Console. |
| A2 | **Produktions-URL** | Vad ska `unstable-app.enerflex.cloud` heta i produktion? Vi behöver den slutgiltiga domänen för att byta ut i alla integrationer. |
| A3 | **Produktions-Cognito-pool** | Separat Cognito user pool för produktion (inte samma som test). Authorize- och token-URL:er för produktionspoolen. |

---

### 2. För HA official-submission (krävs av Home Assistant core team)

| # | Krav | Detalj |
|---|---|---|
| B1 | **Stabil produktions-URL med eget domännamn** | T.ex. `api.effiraenergy.com`. Kan inte vara `unstable-*` eller en AWS-URL. |
| B2 | **Versionsgaranti på `/api/v1/`** | Formellt löfte om att inte bryta befintliga endpoints utan förvarning. HA core-teamet kräver att leverantören kan garantera API-stabilitet. |
| B3 | **Deprecation policy** | Minimistandard: 90 dagars förvarning innan ett endpoint ändras eller tas bort. |
| B4 | **OpenAPI-spec publicerad** | Swagger/OpenAPI-dokumentation för endpunktarna vi använder. Krävs i HA official review-processen. Peter Tellrams wrapper-app har redan all logik — enkelt att generera från den. |

---

### 3. Bra att ha (stärker produkten, krävs inte för lansering)

| # | Krav | Detalj |
|---|---|---|
| C1 | **Rate limiting** | Skyddar API:et från dåliga klienter. Rekommenderat: 60 req/min per API-nyckel. |
| C2 | **API-nyckelhantering i Effira-appen** | Användare ska kunna se, döpa och radera sina API-nycklar inifrån appen. Idag skapas de via OAuth Debugger + curl. |
| C3 | **Webhook / push för statusändringar** | Gör att integrationer kan reagera direkt istället för att polla var 5:e minut. Lägre latens, lägre API-belastning. |

---

## Vad vi levererar när kraven är uppfyllda

När A1–A3 är klara:
- OAuth-login i HA fungerar direkt — användaren loggar in med Effira-kontot, väljer installation, klart
- Vi byter URL-konstanter och publicerar på HACS

När B1–B4 är klara:
- Vi ansöker om inkludering i HA official (pre-installerat för alla ~1M HA-användare)
- Vi publicerar Homey-appen på Homey App Store

---

## Slutsats

Koden är klar. Det som återstår är infrastruktur- och policy-beslut på Effiras sida. A1 kan göras idag och tar en minut. A2–A3 är beroende av när Effira väljer att lansera produktionsmiljön.

Vi är redo att publicera så fort grön ljus ges.
