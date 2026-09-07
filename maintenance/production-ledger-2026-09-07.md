# Boring Best — Production Ledger / Save Point
Captured: 2026-09-07 02:10 EDT. Pick up here next session.

## LIVE STATE (all deployed + verified)
- **7 guides live** (18 pages total): best-shower-curtains, best-shower-curtain-liners, best-toilet-plungers, best-extension-cords, best-dish-racks, best-kitchen-trash-cans, best-power-strips.
- Every guide: real Amazon ratings/prices/review-counts, **self-hosted product photos** (`public/images/<slug>-<ASIN>.jpg`), honest framing ("ranked from real Amazon customer reviews"), **Article + FAQPage schema** (never Review/reviewCount). All `boringbest-20` affiliate tags.
- All buy links verified live (browser-level). No broken images site-wide.

## ANALYTICS
- GA4 property id **524964122** (a384810222 is ACCOUNT id — don't confuse). Key `/root/workspace/documents/adu-analytics-b98b054a1e4e.json`. Venv `/root/workspace/ana-venv`.
- Baseline (90d ending 09-06): 52 clicks / 5,420 impressions / 0.96% CTR / avg pos 17.1. Top query "best shower curtain liner" 5 clk / 1,028 imp / pos 21. Myriad 0-click queries at pos 8-17 (big untapped CTR).

## AUTOMATION (armed, verified)
- **cron b1d875c17257** — monthly refresh, 1st of month 9am, forever, deliver TG. Audits links, rescrapes ratings/prices/photos, flags dead/moved, prompts user for fresh top-10 links. Next 2026-10-01.
- **cron 046723ded04a** — 30d analytics check-in, one-shot 2026-10-06 09:00, GA4/GSC vs baseline. Locked.
- (Optional, not created yet: deploy-status monitor pings if a GH Actions run ever fails.)

## DEPLOY PIPELINE
- Auto-deploy = GitHub Actions `.github/workflows/deploy.yml` on push to main. **VERIFIED HEALTHY** — last pushes green. One isolated failure (0031446) = transient rsync/SSH blip; I added a **rsync retry** so it self-heals. Committed `3c4edea`.
- **Fallback if a deploy ever fails live:** manual rsync (skip the flaky path): `cd boringbest && npm run build && rsync -az --delete -e "ssh -p 65002 -i /root/.ssh/id_ed25519" ./dist/ u429886550@82.25.87.122:~/domains/boringbest.com/public_html/`
- GitHub Secrets used: HOSTINGER_SSH_KEY/HOST/({PORT/USER}). Repo DenverEro/boringbest.

## GOTCHAS LEARNED (do not relitigate)
- Amazon returns HTTP 200 bot-wall on genuinely dead ASINs — use REAL BROWSER (browser_exec #productTitle) for liveness. Handle "Continue shopping" interstitial by clicking it, then re-read.
- TrustBar date: parse `lastUpdated + 'T00:00:00'` (local), else UTC shifts date back a day.
- Header logo is TEXT (styled "Boring Best"), never an image; og-default.jpg + logo.png now exist (were 404ing).
- After adding a review JSON, ALSO wire nav: homepage featuredReviews + category count, categories/<cat>.astro (use ReviewCard incl image), categories/index.astro. Stale stubs caused "images broken / guide missing" complaints.
- JSON schema fields: slug/status/title/description/category/categoryLabel/lastUpdated/quickAnswer/howWeChose/whoThisIsFor/comparison/products[{name,price,rating,type,bestFor,verdict,buyLink,buyText,image}]/picks[{rank,...badge,image}]/guide.blocks/care/faqs/newsletter.
- Images: `public/images/` must match exact reference; `main_image`/photo from browser `#landingImage` src, download to `<slug>-<ASIN>.jpg`.

## WEEKLY CATEGORY PLAN (grounded in GSC authority)
User wants ~1 new category/week. Current: Bathroom(3), Kitchen(2), Home Office(2).
- Week 1 ✅ Best Shower Curtains (DONE, live).
- Week 2 → Bath mats or shower heads (bathroom cluster).
- Week 3 → Kitchen: sink organizers / cutting boards.
- Week 4 → Home Office: desk accessories.
Each: user sends ~10 top-N non-sponsored Amazon links (a.co or amazon), agent resolves ASIN→browser-capture title/price/rating/reviews/photo→build JSON→wire nav→build→verify→commit+push (auto-deploy).

## OPEN / NEXT
- Week 2 links (bath mats or shower heads) not yet sent.
- 0-click rankings on liner page (311 "shower liners mildew resistant"@pos27, 174 "best shower curtain liners"@pos25, etc.) — title/FAQ nudge = cheap CTR win.
- Optional: deploy-failure monitor cron.

## CONTENT/BUDGET BLOCKERS (unchanged, for when money allows)
- Amazon Creators API 403 AssociateNotEligible — needs ~10 qualifying sales/30d. `scripts/source_products.py` ready; creds in .env work. Re-test when user hits threshold.
- Rainforest (~$30/mo) = paid fallback for sourcing; user can't afford yet. Do NOT use third-party Amazon scrapers (associate termination risk).