# WebP & Image Work Summary

## Overview

A series of changes across 8 commits (`8518d98`..`2b50606`) to improve the protein animation, favicon, press thumbnails, and image handling across the site.

## 1. Protein Animation (animated WebP)

**Source file:** `static/1jrj-d80_minsize.webp` (1jrj protein structure, rotating)

| Change | Details |
|--------|---------|
| Frame rate | Sped up to 180ms per frame |
| File size | Compressed from 8.5 MB → ~1 MB for the homepage variant |
| Variants created | `_1mb_backup`, `_sub1mb`, `_diffusion`, `_diffusion_checkpoint`, `_diffusion_checkpoint2` |
| Homepage usage | Switched to the 1 MB variant (`1jrj-d80_minsize_1mb_backup.webp`) |
| Frame geometry | Rebuilt with proper frame geometry (fixed in `b903bd7`) |

### Fade-in animation

A CSS fade-in was added so the protein image doesn't pop in abruptly:

```css
@keyframes protein-fade {
  from { opacity: 0; }
  to   { opacity: var(--protein-opacity, 0.9); }
}
.protein-img { animation: protein-fade 4s ease-in forwards; }
```

### Dark mode opacity fix

The animation initially restarted on theme toggle because light/dark used different `@keyframes` names. Fixed by using a **CSS custom property** (`--protein-opacity`) so the same animation name works for both themes:

- Light: `--protein-opacity: 0.9`, `brightness(1.25)`
- Dark: `--protein-opacity: 1`, `brightness(1.1)`

### Accessibility

- Added `width`/`height` attributes to prevent CLS (Cumulative Layout Shift)
- Updated alt text to reflect animated WebP format

## 2. Favicon

| Change | Details |
|--------|---------|
| Source | Generated from a frame of the 1jrj protein structure |
| Files updated | `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-*.png` |
| Safari pinned tab | Removed `safari-pinned-tab.svg` (was a potrace letter, not the protein); Safari now falls back to the standard PNG favicon |

## 3. Press Coverage Thumbnails

Three press/news images added to `static/press/`:

| File | Size | Source |
|------|------|--------|
| `quanta-brain-cartography.webp` | 662 KB | Quanta Magazine |
| `transmitter-ai-neuroscience.png` | 1.7 MB | The Transmitter |
| `microsoft-dayhoff-atlas.png` | 273 KB | Microsoft Research |

These were initially untracked (not committed), which caused the "News coverage" section to render cards without visible thumbnails on the deployed site.

### Rendering

Cards display in a 2-column grid with:
- `object-cover` + `h-40` for consistent thumbnail sizing
- Hover scale effect (`group-hover:scale-105`)
- Alt text includes publication name

## 4. Image Accessibility & CLS Prevention

Applied across all images on the science and homepage:

- Explicit `width`/`height` attributes on `<img>` tags
- `background-color: transparent` on the protein image (overrides the global grey placeholder)
- Descriptive alt text on all press thumbnails

## Commit Trail

| Commit | Summary |
|--------|---------|
| `8518d98` | Favicon from protein, animation speedup, WebP compression, codebase cleanup |
| `b903bd7` | Fade-in animation, rebuilt WebP frame geometry |
| `cb39b29` | Dark mode animation restart fix (first attempt) |
| `f8e081f` | Dark mode opacity fix via CSS custom property (final fix) |
| `798a87a` | CLS prevention, alt text, press coverage section with thumbnails |
| `b2f51d4` | Alt text correction for animated WebP |
| `3a92eac` | Commit the press thumbnail images |
| `2b50606` | Remove Safari pinned tab SVG for favicon fallback |
