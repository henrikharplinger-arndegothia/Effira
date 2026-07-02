# Effira website — rebuild plan
*Started 2026-05-07*

## Strategy

Next.js + TypeScript + Tailwind CSS, with WordPress kept as headless CMS.
WooCommerce stays untouched — shop/checkout links go to existing WP URLs.
Deploy to Vercel. DNS cutover is the final step. WordPress site stays live the entire time.

---

## Preparation (do before Phase 0)

| Task | Where | Notes |
|---|---|---|
| Verify WP REST API is public | `effiraenergy.com/se/wp-json/wp/v2/pages` | Should return JSON |
| Install "ACF to REST API" plugin | WP Admin → Plugins | Exposes ACF field content via REST |
| Create Application Password | WP Admin → Users → profile | Name it "Next.js frontend", keep for `.env.local` |
| Create Vercel account | vercel.com | Connect GitHub |
| Create new repo | GitHub | `effira-website` (separate from this CRM repo) |
| Audit savings calculator formula | WP page source / team | Needed for Phase 4 — most critical interactive feature |

---

## Phase 0 — Foundation (3–4 days)
- `npx create-next-app@latest effira-website --typescript --tailwind --app`
- Brand tokens as Tailwind config (see `design/look-and-feel.md`)
- Base components: Button, Section, Container, NavBar, Footer
- WordPress REST API typed client
- Deploy skeleton to Vercel

**Milestone:** `effira-website.vercel.app` loads with correct fonts, colors, nav, footer.

---

## Phase 1 — Core marketing pages (1–2 weeks)
Priority order (traffic + conversion value):

1. Homepage (`/se/`)
2. Hur fungerar OPTi (`/se/optimera-varmepumpen/`)
3. Priser (`/se/opti-priser-2026/`)
4. Beställ OPTi — links to existing WP checkout, not rebuilt (`/se/bestall-opti/`)
5. Kompatibilitet (`/se/kompatibilitet/`)
6. Effira-appen (`/se/effira-appen/`)

All content via WP REST API — no hardcoded copy.

**Milestone:** 6 highest-traffic pages live on Vercel preview.

---

## Phase 2 — Secondary marketing + legal (3–5 days)
- Besparingsgaranti
- Huset som ett batteri
- Om oss
- Press
- Integritetspolicy + Allmänna villkor
- Radera konto / Delete account

**Milestone:** Full site navigable except calculator, blog, webinars.

---

## Phase 3 — Content hub (3–5 days)
- Kunskapsbanken hub
- Articles: listing + 10 individual pages (dynamic routing from WP posts)
- Webinars: listing + 6 individual pages (YouTube embeds)
- Nyhetsbrev + Seminarie

**Milestone:** All published content accessible on Vercel.

---

## Phase 4 — Interactive features (1–2 weeks)
- Savings calculator — rebuilt in React with real formula
- Compatibility checker — data from WP custom post type or JSON
- HubSpot forms — same embed script as today
- Ring upp mig callback form
- Newsletter signup
- Support FAQ (via REST if ACF fields exposed)

**Milestone:** All conversion paths work end-to-end.

---

## Phase 5 — SEO + polish (3–4 days)
- `next/head` metadata per page (from WP Yoast fields via REST)
- Open Graph images
- `sitemap.xml` generated from WP REST
- `robots.txt`
- Google Tag Manager script
- Lighthouse audit

**Milestone:** SEO parity with current site. Ready for cutover.

---

## Phase 6 — Cutover
Do on a low-traffic day (Tuesday morning).

1. WP → maintenance mode
2. Change DNS A record to Vercel IPs
3. Add `effiraenergy.com` as custom domain in Vercel
4. SSL provisions automatically
5. Keep WP at `wp.effiraenergy.com` — WooCommerce must stay live
6. Test every page and every form on live domain
7. Monitor Google Search Console for crawl errors x2 weeks

---

## What stays on WordPress forever
WooCommerce shop, cart, checkout, order management, subscriptions, my account, payments.
These are linked to from the Next.js site — invisible to users, zero migration risk.

---

## Timeline at side-project pace (~5–8h/week)
| Phase | Weeks |
|---|---|
| 0 Foundation | 1–2 |
| 1 Core pages | 3–5 |
| 2 Secondary pages | 6–7 |
| 3 Content hub | 8–9 |
| 4 Interactive | 10–13 |
| 5 SEO + polish | 14–15 |
| Cutover | ~Week 16 |

Approximately 3–4 months of relaxed side-project work.
