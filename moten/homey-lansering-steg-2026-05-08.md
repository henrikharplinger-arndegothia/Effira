# Homey-app: steg för lansering till Homey-ägare

**Datum:** 2026-05-08

---

**1. Testa och rätta fel — Peters Homey**
Peter klonar repot, kör `homey app run`, lägger till enheten och verifierar att kapabiliteter och flow-kort fungerar. Eventuella buggar fixas här innan vi går vidare.

**2. Produktions-URL — Kenny**
Byt ut `unstable-app.enerflex.cloud` mot den riktiga produktions-URL:en i `api.js`. Utan detta anropar appen testmiljön — inte acceptabelt för en publicerad app.

**3. OAuth-login — Kenny + vi**
Kenny registrerar Homeys redirect-URI i Cognito. Vi implementerar OAuth-steget i par-flödet så att användare loggar in med sitt Effira-konto istället för att klistra in API-nycklar. Det är skillnaden mellan en konsumentapp och ett utvecklarverktyg.

**4. Validera och certifiera**
```bash
homey app validate
```
Athom (Homeys tillverkare) kräver att appar klarar deras validator innan inlämning. Rättar eventuella problem med manifestet, bildstorlekar och saknade fält.

**5. Skicka in till Homey App Store**
```bash
homey app publish
```
Athom granskar appen — tar vanligtvis några dagar till ett par veckor. När den godkänts syns den i butiken på `homey.app/a/com.effiraenergy.opti` och alla Homey-ägare kan installera den med ett tryck.

---

**Innan steg 5 behövs också:**
- Flytta repot till en officiell Effira GitHub-organisation
- Uppdatera `author`, `support` och `homepage` i `app.json` till Effiras officiella uppgifter
- Ett Homey-utvecklarkonto registrerat under Effira

---

**Den verkliga blockeringen** är densamma som för HA: steg 2 och 3 beror båda på att Kenny lanserar en produktionsmiljö. Allt annat är klart.

---

**Relaterade dokument:**
- `api-krav-kenny-2026-05-08.md` — formella krav till Kenny för produktions-API
- Repo: `github.com/henrikharplinger-arndegothia/homey-effira`
