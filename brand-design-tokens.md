# Effira Energy — Design Tokens

*Hämtat från effiraenergy.com/se/ 2026-04-23*

## Färger

```css
--color-darkGreen:  #013233   /* header, footer, knappar, rubriker */
--color-lightGreen: #d0e7e2   /* bakgrunder, highlights */
--color-orange:     #ff8c2d   /* primär CTA-knapp, accent */
--color-white:      #ffffff
--color-black:      #000000
--color-brandBlack: #062121   /* brödtext, mörka element */
```

## Typsnitt

| Användning | Familj |
|---|---|
| Brödtext & UI | Work Sans (Google Fonts) |
| Display / accent | Permanent Marker (Google Fonts) |
| Fallback | system-ui, sans-serif |

**Vikter:** 400 · 500 · 600 · 700

**Storlekar:**
| Klass | rem | px |
|---|---|---|
| xs | 0.75 | 12 |
| sm | 0.875 | 14 |
| base | 1 | 16 |
| lg | 1.125 | 18 |
| xl | 1.25 | 20 |
| 2xl | 1.5 | 24 |
| 3xl | 1.875 | 30 |
| 4xl | 2.25 | 36 |
| 5xl | 3 | 48 |
| 6xl | 3.75 | 60 |

**Rubrikklasser:** `heading-xxl` · `heading-lg` · `heading-sm`
**Brödtextklasser:** `body-lg` · `body-md`

## Knappar

| Typ | Bakgrund | Text | Radie |
|---|---|---|---|
| Primary | `#ff8c2d` (orange) | `#062121` | 9999px (pill) |
| Secondary | `#013233` (mörkgrön) | `#ffffff` | 9999px (pill) |
| White | `#ffffff` | `#013233` | 9999px (pill) |

Padding: `12px 22px` (standard) · `12px 40px` (bred)
Hover: 80% opacity + underline

## Layout

- **Max-bredd:** 1400px
- **Ramverk:** Tailwind CSS v4.1.14
- **Breakpoints:** sm 640 · md 768 · lg 1024 · xl 1280 · 2xl 1536

## Skuggor

```
Natural:  6px 6px 9px rgba(0,0,0,0.2)
Deep:    12px 12px 50px rgba(0,0,0,0.4)
Sharp:    6px 6px 0px rgba(0,0,0,0.2)
```

## Användningsmönster

- **Header/Footer:** mörkgrön bakgrund, vit text
- **Sektionshighlights:** ljusgrön bakgrund
- **Primär CTA:** alltid orange pill-knapp
- **Rubriker:** mörkgrön
- **Brödtext:** brandBlack (`#062121`) eller mörkt grå
