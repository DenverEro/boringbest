#!/usr/bin/env python3
"""
Phase 3: ChatGPT - Amazon Creators API sourcing script.

Turns a product keyword into a draft boringbest JSON guide file.

USAGE
  step 1: create /root/workspace/boringbest/.env with:
          AMAZON_CLIENT_ID=...
          AMAZON_CLIENT_SECRET=...
          AMAZON_PARTNER_TAG=boringbest-20
  step 2: python3 scripts/source_products.py --keyword "best toilet plunger"
          python3 scripts/source_products.py --keywords "toilet plunger" "shower liner"

Output: src/data/reviews/<slug>.json  (status:"coming-soon" = safe draft you can push
        WITHOUT it publishing a full guide; edit it to status:"live" + add verdicts/pros/cons).
"""
import argparse, json, os, re, sys, time, uuid

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "src", "data", "reviews")

TOKEN_URL = "https://api.amazon.com/auth/o2/token"
SEARCH_URL = "https://creatorsapi.amazon/catalog/v1/searchItems"


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-").strip() or "guide"


def load_creds() -> dict:
    env = {}
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return {
        "client_id": env.get("AMAZON_CLIENT_ID", ""),
        "client_secret": env.get("AMAZON_CLIENT_SECRET", ""),
        "partner_tag": env.get("AMAZON_PARTNER_TAG", ""),
    }


def get_token(creds) -> str:
    r = requests.post(TOKEN_URL, json={
        "grant_type": "client_credentials",
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "scope": "creatorsapi::default",
    }, timeout=60)
    if r.status_code != 200:
        sys.exit(f"Token request failed ({r.status_code}): {r.text[:500]}")
    return r.json()["access_token"]


def search_keyword(token, creds, keyword, item_count=10):
    body = {
        "keywords": keyword,
        "partnerTag": creds["partner_tag"],
        "marketplace": "www.amazon.com",
        "itemCount": item_count,
        "resources": [
            "itemInfo.title",
            "images.primary.large",
            "offersV2.listings.price",
            "customerReviews.count",
            "customerReviews.starRating",
        ],
    }
    hdr = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-marketplace": "www.amazon.com",
    }
    r = requests.post(SEARCH_URL, json=body, headers=hdr, timeout=60)
    if r.status_code != 200:
        # Common error: customerReviews resource unsupported on this search index.
        if r.status_code == 400 and "customerReviews" in r.text:
            return _search_retry_drop_reviews(token, creds, keyword, body)
        sys.exit(f"SearchItems failed ({r.status_code}): {r.text[:800]}")
    return parse_items(r.json())


def _search_retry_drop_reviews(token, creds, keyword, body):
    print("  customerReviews not supported on this index; retrying without it")
    body["resources"] = [res for res in body["resources"] if "customerReviews" not in res]
    r = requests.post(SEARCH_URL, json=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "x-marketplace": "www.amazon.com",
    }, timeout=60)
    if r.status_code != 200:
        sys.exit(f"SearchItems retry failed ({r.status_code}): {r.text[:800]}")
    return parse_items(r.json())


def parse_items(resp):
    items = (resp.get("searchResult") or {}).get("items") or []
    out = []
    for it in items:
        title = (((it.get("itemInfo") or {}).get("title") or {}).get("displayValue")) or ""
        if not title:
            continue
        # price
        price = None
        try:
            offers = (it.get("offersV2") or {}).get("listings") or []
            price = offers[0]["price"]["money"]["amount"]
        except Exception:
            pass
        # image (large URL)
        image = None
        try:
            image = (it.get("images") or {}).get("primary", {}).get("large", {}).get("url")
        except Exception:
            pass
        # customer reviews
        cr = it.get("customerReviews") or {}
        star = cr.get("starRating")
        count = cr.get("count")
        out.append({
            "asin": it.get("asin"),
            "title": title,
            "price": round(price, 2) if price else None,
            "rating": float(star) if star else None,
            "ratingCount": int(count) if count else None,
            "image": image,
            "buyLink": f"https://amazon.com/dp/{it.get('asin')}?tag=boringbest-20",
        })
    return out


def main():
    ap = argparse.ArgumentParser(description="Fetch top products for a keyword from Amazon Creators API")
    ap.add_argument("--keyword", help="single keyword to search")
    ap.add_argument("--keywords", nargs="+", help="multiple keywords (one search each)")
    ap.add_argument("--slug", help="override output slug (default from keyword)")
    ap.add_argument("--count", type=int, default=10, help="items per search (1-10)")
    args = ap.parse_args()

    if not args.keyword and not args.keywords:
        ap.error("provide --keyword or --keywords")

    creds = load_creds()
    missing = [k for k, v in creds.items() if not v]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}. Create /root/workspace/boringbest/.env with AMAZON_CLIENT_ID, AMAZON_CLIENT_SECRET, AMAZON_PARTNER_TAG.")

    print(f"Authenticating with partner tag '{creds['partner_tag']}' ...")
    token = get_token(creds)
    print("Token OK.")

    keywords = [args.keyword] if args.keyword else args.keywords
    os.makedirs(DATA_DIR, exist_ok=True)

    for kw in keywords:
        print(f"\nSearching: {kw} ...")
        items = search_keyword(token, creds, kw, args.count)
        print(f"  {len(items)} items returned")
        if not items:
            print("  no results; skipped.")
            continue
        slug = args.slug or slugify(kw)
        draft = {
            "slug": slug,
            "status": "coming-soon",
            "title": f"Best {kw.title()} of 2026: Guide Coming Soon",
            "description": f"We are researching the best-rated {kw.lower()} on Amazon right now. Join the list and we will let you know the moment this guide publishes.",
            "category": "uncategorized",
            "categoryLabel": "Coming Soon",
            "comingSoonMessage": f"We are digging through real Amazon reviews to rank the best-rated {kw.lower()}. Join the list and we will notify you the moment it is published.",
            "_sources": items,
        }
        out_path = os.path.join(DATA_DIR, f"{slug}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(draft, f, indent=2)
        print(f"  wrote draft: {out_path}")
        print("  To publish: clear the _sources[] into live product data, fill verdicts/pros/cons, set status:'live'.")

    print("\nDone.")


if __name__ == "__main__":
    main()