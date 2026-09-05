# Boring Best — Phase 2 & 3 Design

**Status:** Design (not built). Phase 1 (honesty fix) is DONE, committed & pushed.
**Reader:** you (non-programmer) — this is the map, not the code.

---

## Where we are after Phase 1 (done)

- Every fake "we tested it / X hrs / X products" claim is gone across all 22 files.
- Fabricated `@type: Review` + `reviewCount` structured data replaced with honest `Article` + `FAQPage` schema.
- Site is Google-safe and Amazon-associates-safe. Affiliate tag `boringbest-20` on all links, intact.
- **Result: 3 real published guides + 3 honest "coming soon" pages.**

The blocker now is *volume*, not trust. Phase 2 + 3 are the scale engine.

---

## The core problem Phase 2 solves

Today each guide is a hand-written 400-line `.astro` file. Every new keyword = rewriting that whole file.

**Target:** adding a guide = adding one block of product data. The page renders itself.

---

## Phase 2 — Data-driven rebuild

### Architecture

```
src/
  data/
    reviews/
      toilet-plungers.json      <- one file per keyword (the ONLY thing you hand-edit)
      extension-cords.json
      shower-curtain-liners.json
  pages/
    reviews/
      [slug].astro              <- ONE generic template renders every guide from the JSON
```

- **`[slug].astro`** is a single template. It contains all the HTML sections (Quick Answer, Trust Bar, comparison table, top picks, buying guide, FAQ, newsletter, disclosure) exactly like today's pages — except the copy/prices/ratings come from the matching JSON by URL slug.
- **`getStaticPaths()`** reads `src/data/reviews/*.json`, figures out every slug, and builds one page per file at build time. Sitemap + robots still work automatically.

### What lives in each JSON file

```json
{
  "slug": "best-toilet-plungers",
  "title": "Best Toilet Plungers of 2026: Ranked by Real Reviews",
  "description": "...",
  "category": "bathroom",
  "lastUpdated": "2026-02-09",
  "quickAnswer": "...",
  "howWeChose": ["...", "..."],
  "shipping": "...",
  "faqs": [ { "q": "...", "a": "..." } ],
  "products": [
    {
      "name": "Korky 99-4A Max Performance Plunger",
      "asin": "B0FG47SHKB",
      "price": 22.37,
      "rating": 4.9,
      "badge": "Best Overall",
      "image": "/images/korky-99-4A.png",
      "pros": ["...", "..."],
      "cons": ["...", "..."],
      "verdict": "..."      <- the human-written 1-2 sentence rationale
    }
  ]
}
```

### Why this pays off

- **One template fix = every guide inherits it** (schema, honest framing, CTA, disclosure).
- **Adding a guide is: drop in a JSON file, hit build.** No 400-line page to write.
- **Keeps the honest framing automatic** — the "ranked from real reviews, not a lab" text lives once in the template, so future guides can't silently backslide into fake claims.
- The `"verdict"` per product stays human-written: that's the value-add only you can give, and it's what keeps the review honest, not just scraped.

### Migration (Phase 2 work, recipe order)

1. Create `src/data/reviews/` with the 3 existing guides as JSON (copy data out of today's files).
2. Build `[slug].astro` template (port today's page structure).
3. Delete the 3 static review `.astro` files (they'd collide with the dynamic route).
4. Build + verify the 3 URLs still resolve identically.
5. Commit.

**Each future direction is now cheap:** a "best X" keyword drop-in is one JSON file.

---

## Phase 3 — Rainforest sourcing pipeline (the automation you asked for)

### What it does in one sentence
Type a keyword → a script calls the Rainforest API → it returns the real **ASIN, title, price, star rating, and review count** for the top-rated products → you approve → a ready-to-drop JSON guide file is produced.

### The exact call

```
GET https://api.rainforestapi.com/request
  ?api_key=YOUR_KEY
  &type=search
  &amazon_domain=amazon.com
  &search_term=best shower curtain liner
```

The response's `products[]` gives you, for each item:
`asin`, `title`, `link`, `price`, `rating`, `ratings_total`, `image`.

### The pipeline (with your human checkpoint)

```
1. Keyword list  (e.g. "best dish rack", "best kitchen trash can")
2. Script calls Rainforest search for each keyword
3. Script filters: rating >= 4.3 AND ratings_total >= 500  (auto-skip junk)
4. Script ranks top 5-6, maps to boringbest JSON schema
5. YOU review the verdicts/pros/cons (the only manual step — real human judgment)
6. Script writes reviews/<slug>.json
7. npm run build  --> new page live
```

### Rainforest details
- **Cost:** ~$0.01–0.03 per request. Seed a guide for pennies; a full keyword sprint is a few dollars.
- **No approval wait** — this is why we picked it over Amazon PA-API (which needs application + qualifying sales history). `product-price-monitor`-style refresh can re-pull prices later.
- All numbers come from the API = **no risk of fabricating a rating** (the thing Phase 1 fixed).

### Guardrails built in (keep it honest)
- Only accept ratings/values the API returned — never let a script write a "verdict."
- A guide is only published after a human reviews it; otherwise it stays "coming soon."
- Keep the one-line-differentiator up top: rankings from real buyer reviews, not a lab.

### First keyword sprint (high-leverage, low-effort picks)
1. Best dish racks (stub already exists → fills a live gap)
2. Best kitchen trash cans (stub)
3. Best power strips (stub)
4. Bath mats, shower caddies (new, high search volume)
Then extend one category at a time toward the $10k/mo volume goal.

---

## Play sequence (proposed order)

1. **Phase 3a:** Build the Rainforest pull script + prove it on 1 keyword. (Small, high-visible win.)
2. **Phase 2:** Stand up the data-driven `[slug]` template, migrate the 3 guides. (Unlocks cheap scaling.)
3. **Phase 3b:** Wire Phase-3 output directly into Phase-2's JSON store. Now a keyword→live-guide is a single command + one human review.
4. Fill the 3 stubs, then push one new keyword per week.

---

## Open questions for you (when we get there)

- **Rainforest API key** — you'll need to create one at rainforestapi.com (paid, ~$30/mo base or pay-as-you-go). Confirm budget is OK.
- **Hosting/deploy** — current manual Hostinger upload. Phase 2/3 makes auto-deploy on `push to main` worth adding (the `hermes-agent`/GitHub skill can wire that).
- **Scope per guide** — keep Top 3 PickCards (as now) or expand to 5? More products = more empty ranking slots to fill, more cost per guide.