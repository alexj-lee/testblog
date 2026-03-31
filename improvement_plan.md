# SEO & Discoverability Improvements

## Context

SvelteKit + Tailwind CSS academic personal site for a PhD student in computational biology. Deployed on Netlify. Goal: improve search engine visibility, especially for name-based queries and research topics.

---

## 1. Server-Side Rendering & Prerendering

- Ensure all public pages use SSR or prerendering (not client-only SPA mode).
- Add `export const prerender = true;` in `+page.js` or `+layout.js` for all static pages (homepage, about, publications, blog index).
- Blog posts can also be prerendered if they're built from markdown at build time.

## 2. Sitemap & Robots

- Create a `sitemap.xml` route at `src/routes/sitemap.xml/+server.js` that dynamically lists all public URLs with `<lastmod>` dates.
- Create a `static/robots.txt` with:
  ```
  User-agent: *
  Allow: /
  Sitemap: https://alexlee.netlify.app/sitemap.xml
  ```

## 3. Per-Page Metadata via `<svelte:head>`

Every route should include a `<svelte:head>` block with:

```svelte
<svelte:head>
  <title>{pageTitle} | Alex Lee</title>
  <meta name="description" content="{pageDescription}" />

  <!-- Open Graph -->
  <meta property="og:title" content="{pageTitle} | Alex Lee" />
  <meta property="og:description" content="{pageDescription}" />
  <meta property="og:type" content="website" /> <!-- or "article" for blog posts -->
  <meta property="og:url" content="https://alexlee.netlify.app{$page.url.pathname}" />
  <meta property="og:image" content="{ogImageUrl}" />

  <!-- Twitter/X Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{pageTitle} | Alex Lee" />
  <meta name="twitter:description" content="{pageDescription}" />
  <meta name="twitter:image" content="{ogImageUrl}" />

  <!-- Canonical URL -->
  <link rel="canonical" href="https://alexlee.netlify.app{$page.url.pathname}" />
</svelte:head>
```

- Consider creating a reusable `<SEO>` component that accepts `title`, `description`, `image`, and `type` props to keep this DRY across routes.

## 4. JSON-LD Structured Data

### Homepage — Person Schema

Add to the homepage `<svelte:head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Alex Lee",
  "jobTitle": "PhD Student in Computational Biology",
  "affiliation": {
    "@type": "Organization",
    "name": "[University Name]"
  },
  "url": "https://alexlee.netlify.app",
  "sameAs": [
    "https://scholar.google.com/citations?user=XXXX",
    "https://github.com/XXXX",
    "https://orcid.org/XXXX",
    "https://twitter.com/XXXX"
  ]
}
</script>
```

### Blog Posts — Article Schema

Add to each blog post `<svelte:head>`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{postTitle}",
  "datePublished": "{isoDate}",
  "dateModified": "{isoModifiedDate}",
  "author": {
    "@type": "Person",
    "name": "Alex Lee",
    "url": "https://alexlee.netlify.app"
  },
  "description": "{postDescription}",
  "mainEntityOfPage": "https://alexlee.netlify.app/blog/{slug}"
}
</script>
```

## 5. Heading & Anchor Text Strategy

- Homepage `<h1>` should contain full name + field: e.g., `Alex Lee — Computational Biology`.
- Blog index `<h1>`: "Computational Biology Blog" or similar (not just "Blog").
- Research/publications page `<h1>`: include specific research areas, e.g., "Protein Structure Prediction Research".
- Use descriptive link text everywhere — avoid bare "here" or "link" anchors.

## 6. Cross-Linking & External Profiles

Ensure the site footer or about section includes links to:
- Google Scholar profile
- ORCID
- GitHub
- Twitter / Bluesky
- Lab group page
- LinkedIn

And that each of those profiles links back to `https://alexlee.netlify.app`.

## 7. Image Accessibility & SEO

- All `<img>` tags must have descriptive `alt` attributes.
- The protein animation on the homepage should have alt text describing what it shows.
- Press coverage thumbnails should have alt text like `"{Publication Name} article thumbnail: {brief description}"`.
- Use WebP format (already in use) with appropriate `width`/`height` attributes to avoid layout shift.

## 8. Performance (Netlify-Specific)

- Enable Netlify's asset optimization (CSS/JS minification, image compression) in `netlify.toml` or dashboard.
- Add cache headers for static assets.
- Confirm Core Web Vitals are green via Google PageSpeed Insights — LCP, CLS, and INP all matter for ranking.

## 9. Blog Content Strategy (Not a Code Task)

For reference — these are content decisions, not implementation tasks:
- Target one post per month minimum.
- Title posts with search-friendly phrasing: "How to [do X]" or "[Tool/Method] for [Problem]".
- Each post should have a unique meta description (120–160 chars) summarizing the content.
- Tag/categorize posts if the blog grows beyond ~10 entries.
