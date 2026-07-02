# Effira × Tibber — Samarbetsförslag
*Utkast för diskussion | Juni 2026*

---

## Vad vi föreslår

Effira erbjuder Tibber tillgång till **flexibilitetslagret i värmepumpen** — en resurs Tibber idag saknar i sin VPP-portfölj.

Modellen är enkel: **Tibber avropar flexibilitet. Effira exekverar via OPTi.**

Tibber behöver inte bli installatör, bygga värmepumpsstyrning eller hantera komfortfrågor. Effira behöver inte bygga VPP-logik, prisoptimering eller kund-app. Varje part gör det de är bra på.

---

## Vad Effira bidrar med

| Vad | Detalj |
|-----|--------|
| **Hårdvara + styrning** | OPTi installerat i kundens hem — styr uppvärmning och varmvatten |
| **Kompatibilitet** | ~95% av vattenburna värmepumpar: NIBE, Bosch, IVT, Thermia, Mitsubishi |
| **Responstid** | Pump av inom 30 sekunder — FCR-D-kompatibelt |
| **Uthållighet** | 60–90 min vid normala förhållanden, 2–4 tim i vällisolerat hus |
| **Komfortskydd** | Strukturell konstruktionsgaranti — systemet agerar aldrig om termisk buffert saknas |
| **Mätning** | Realtidseffektmätning per pump — bevisad delta vid varje dispatch |
| **Installation + support** | Professionell installation ingår, Effira ansvarar för kundkontakt och support |

---

## Dispatch-modellen

```
Tibber          →   "Minska last med X kW under Y minuter"
Effira          →   Kontrollerar tillgänglig kapacitet
Effira          →   Exekverar styrning via OPTi
Effira          →   Rapporterar levererad kapacitet + delta per pump
```

Dispatch kan ske på **enskild kundnivå** eller **portfölj-/klusternivå** (per elområde, kundsegment, teknisk profil).

---

## Fas 1 — Pilot

| Parameter | Förslag |
|-----------|---------|
| **Volym** | 100–200 Tibber-kunder med vattenburen värmepump |
| **Geografi** | SE3 eller SE4 |
| **Tidslinje** | Start Q3 2026, utvärderas Q4 2026 |
| **Tibbers bidrag** | Kundrekrytering, dispatch-API-integration, VPP-logik |
| **Effiras bidrag** | OPTi-installation, flex-API, realtidsmätning |
| **Mätetal** | Kapacitet levererad vs. utlovad, komfortutfall, responstid |
| **Kommersiell modell** | Att diskutera — förslag: delad installationskostnad + intäktsdelning på VPP-inkomst |

---

## Fas 2 — Kommersiell skala

Bindande samarbetsavtal träder i kraft när piloten visar:

- Effira levererar ≥ 80% av utlovad kapacitet
- Komfortreklamationer under överenskommen gräns
- Tibber har framgångsrikt integrerat dispatch i sin VPP-plattform

**Intäktsdelning vid full skala:** 50/50 på VPP-inkomster (FCR-D + aFRR kapacitet + aktivering).

| Enheter | Tibbers VPP-intäkt/år (50%) |
|---------|---------------------------|
| 2 000 | ~1,3 Mkr |
| 10 000 | ~6,7 Mkr |
| 100 000 | ~67 Mkr |

*Baserat på FCR-D 15 EUR/MW/h, 130 MW vid 100 000 enheter, 4 380 h/år. FCR-D-priset varierade 5–37 EUR/MW/h de senaste två åren.*

---

## Nästa steg

| Steg | Ansvar | När |
|------|--------|-----|
| Letter of Intent | Effira skickar utkast | Inom 2 veckor |
| Teknisk workshop | Peter + Kenny / Tibber tech | Inom 4 veckor |
| Pilotdefinition | Gemensamt | Inom 6 veckor |
| Pilotstart | — | Q3 2026 |

---

*Effira Energy AB · effiraenergy.com*
*Kontakt: Henrik Harplinger · peter@effiraenergy.com*
