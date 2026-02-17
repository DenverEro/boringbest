# Boring Best

A 5-pillar optimized static affiliate site for everyday household essentials. Built with Astro 5, Tailwind CSS, and Pagefind.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Build and index for search
npm run build && npx pagefind --site dist
```

## Project Structure

```
/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Breadcrumb.astro
│   │   ├── Footer.astro
│   │   ├── Header.astro
│   │   ├── NewsletterForm.astro
│   │   ├── PickCard.astro
│   │   ├── SortableTable.astro
│   │   └── TrustBar.astro
│   ├── layouts/
│   │   ├── BaseLayout.astro    # Main layout with Header/Footer
│   │   └── Layout.astro        # Base HTML layout
│   ├── pages/
│   │   ├── index.astro         # Homepage
│   │   ├── about.astro         # About page
│   │   ├── methodology.astro   # Testing methodology
│   │   ├── newsletter.astro    # Newsletter signup
│   │   ├── search.astro        # Search page
│   │   ├── categories/         # Category pages
│   │   └── reviews/            # Product reviews
│   └── styles/
│       └── global.css          # Tailwind + custom styles
├── dist/                       # Build output
├── public/                     # Static assets
└── ...
```

## Design System

### Colors
- **Primary:** #2563EB (Trust Blue)
- **Primary Dark:** #1D4ED8
- **Text:** #111827
- **Background:** #FFFFFF
- **Border:** #E5E7EB

### Typography
- **Font:** Inter (Google Fonts)
- **Headings:** Bold, tight line-height
- **Body:** 1.6 line-height for readability

## Content Structure

Each review follows this template:

1. Quick Answer - 30-second read with top pick
2. Trust Bar - Testing credentials
3. Why You Should Trust Us - Methodology transparency
4. Who This Is For - Audience targeting
5. Comparison Table - Sortable product comparison
6. Top Picks - Individual product deep-dives
7. Buying Guide - What to look for
8. The Competition - Runners-up
9. Care & Maintenance - Longevity tips
10. FAQ - 5 questions with direct answers (GEO-optimized)
11. Newsletter - Email capture
12. Affiliate Disclosure - Compliance

## Deployment

### Build and Deploy

```bash
# Build the site
npm run build

# Index for search
npx pagefind --site dist

# Deploy the dist/ folder to your host
```

The `dist/` folder contains a fully static site ready for deployment to any static host (Hostinger, Netlify, Vercel, etc.)

## Affiliate Links

All affiliate links use the format:
```
https://amazon.com/dp/[ASIN]?tag=boringbest-20
```

Update the tag in each review file with your actual Amazon Associates tag.

## License

MIT License - feel free to use this as a template for your own affiliate sites.

---

**Boring Best** - We test the boring stuff so you don't have to.
