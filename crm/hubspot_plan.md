# HubSpot-import — VVS Partner Pipeline

## Dataläge (2026-05-07)

| Källa | Totalt | Email% | VD% | org_nr% | Anst% |
|---|---|---|---|---|---|
| Comfort | 96 | 100% | 98% | 1% | 100% |
| Bad & Värme | 38 | 100% | 100% | 0% | 100% |
| Thermia | 14 | 100% | 93% | 93% | 93% |
| Bosch | 22 | 100% | 100% | 100% | 82% |
| NIBE | 404 | 0% | 0% | 0% | 0% |
| IVT | 42 | 7% | 2% | 2% | 2% |
| Daikin | 17 | 94% | 12% | 12% | 12% |
| Mitsubishi | 23 | 100% | 4% | 0% | 4% |
| Enwell | 11 | 100% | 100% | 0% | 0% |
| Sparc | 11 | 0% | 100% | 100% | 100% |

**Primärt gap:** NIBE (404 bolag) saknar all kontaktdata — behöver allabolag-körning.
**Klart för import:** Comfort (96), Bad & Värme (38), Thermia (14), Bosch (22), Mitsubishi (23) = 193 bolag.

---

## Objektstruktur i HubSpot

```
Company (bolag)
  └── Contact (VD/kontaktperson)
        └── Deal (outreach-case)
```

Importera i ordning: Companies → Contacts (associerade) → Deals.

---

## Custom Company Properties att skapa i HubSpot

| Property name | Typ | Värden |
|---|---|---|
| `opti_org_nr` | Single-line text | |
| `opti_elzon` | Dropdown | SE1, SE2, SE3, SE4 |
| `opti_tier` | Dropdown | A, B, C |
| `opti_poang` | Number | |
| `opti_marken` | Single-line text | |
| `opti_partner_niva` | Single-line text | |
| `opti_kalla` | Single-line text | |
| `opti_pitch_vinkel` | Multi-line text | |
| `opti_anteckning` | Multi-line text | |

---

## Deal Pipeline: "VVS Partner Outreach"

Stages:
1. **Ny** — importerad, ej kontaktad
2. **Kontaktad** — e-post/telefon skickat
3. **Svar** — svarat, intresserat
4. **Möte bokat** — webinar eller samtal inbokat
5. **Pilot** — provinstallation överenskommen
6. **Aktiv partner** — avtal klart
7. **Ej intresserad** — avslutad

---

## CSV-format för Company import

HubSpot förväntar sig dessa kolumnnamn (mappas mot native properties):

```
Company name,City,Phone number,Website URL,Number of employees,
Annual revenue,opti_org_nr,opti_elzon,opti_tier,opti_poang,
opti_marken,opti_partner_niva,opti_kalla,opti_pitch_vinkel,opti_anteckning
```

Fil: `crm/hubspot_companies.csv`

## CSV-format för Contact import

```
First name,Last name,Email,Associated company
```

Fil: `crm/hubspot_contacts.csv`

---

## Rekommenderad importordning

### Fas 1 — Omedelbart (193 bolag klara)
1. Skapa custom properties i HubSpot (15 min, Settings → Properties)
2. Skapa Deal pipeline "VVS Partner Outreach" (5 min)
3. Importera `hubspot_companies.csv` → Companies
4. Importera `hubspot_contacts.csv` → Contacts, associera mot Companies
5. Bulk-skapa Deals för Tier A (stage: "Ny")

### Fas 2 — Efter NIBE-berikande (~450 bolag till)
6. Kör allabolag-berikande på NIBE Tier A (65 bolag, SE4 prioritet)
7. Komplettera import med NIBE + IVT

### Fas 3 — Enterprise
8. Skapa manuella Deals för Assemblin VS + Bravida (stage: "Ny", owner: Henrik)

---

## Vad som behöver göras innan import

- [ ] Allabolag-berikande av NIBE Tier A SE4 (65 bolag)
- [ ] Generera `hubspot_companies.csv` med rätt kolumnnamn
- [ ] Generera `hubspot_contacts.csv`
- [ ] HubSpot-access bekräftad (portal 146943805)
