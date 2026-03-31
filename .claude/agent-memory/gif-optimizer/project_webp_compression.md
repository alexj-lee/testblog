---
name: webp_compression_results
description: Compression findings for animated WebP protein wiggle hero image - what worked and sweet spots
type: project
---

Compressed the animated WebP hero image (1jrj protein wiggle) from 8.1MB to 1.04MB (87% reduction).

Key findings for this content type (protein space-fill model on transparent background):
- Original: 960x1201, 250 frames, 80ms/frame, lossy ~32KB/frame
- Animated WebP has minimal inter-frame compression - per-frame overhead dominates
- Frame reduction (skip) is the highest-impact optimization (halving frames nearly halves size)
- Quality below q=20 shows diminishing returns (q=20 vs q=10 saves only ~5%)
- Scaling from 960px to 480px (50%) saves ~40% but doesn't halve size due to per-frame overhead
- img2webp method=4 is best speed/quality tradeoff; method=6 saves only ~3% more
- Pillow with minimize_size=True produces identical sizes to img2webp for this content
- The ffmpeg on this system lacks libwebp_anim encoder
- VP9 alpha encoding doesn't work easily with this ffmpeg build (drops to yuv420p)

Best variant chosen: 480x601, q=20, skip3 (84 frames, 240ms/frame), method=6 -> 1.04MB
Sub-1MB alternative: 384x480, q=30, skip3 -> 0.91MB

**Why:** 8.1MB hero image was too large for web; displayed at max-w-sm (384px) in Tailwind.
**How to apply:** For future protein animation compression, start with skip3 + 50% scale + q=20. Frame count reduction is the primary lever.
