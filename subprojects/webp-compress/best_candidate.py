"""Generate the best compression candidates for final selection."""
import os
from pathlib import Path
from PIL import Image

work_dir = "/Users/alex/projects/website/subprojects/webp-compress/work"
output_dir = "/Users/alex/projects/website/subprojects/webp-compress/final"

# The protein image is displayed as a hero - CSS will likely constrain it.
# 480x601 (s50) is a good balance. skip3 = 240ms per frame (smooth enough for a wiggle).

# Try Pillow with minimize_size for better inter-frame compression
configs = [
    ("best_s50_q20_skip3", "frames_s50", 20, 3, 4),
    ("best_s50_q25_skip3", "frames_s50", 25, 3, 4),
    ("best_s50_q30_skip3", "frames_s50", 30, 3, 4),
    ("best_s40_q25_skip3", "frames_s40", 25, 3, 4),
    ("best_s40_q30_skip3", "frames_s40", 30, 3, 4),
    # Method 6 (slower but better compression)
    ("best_s50_q20_skip3_m6", "frames_s50", 20, 3, 6),
    ("best_s50_q25_skip3_m6", "frames_s50", 25, 3, 6),
]

for name, fdir, quality, skip, method in configs:
    full_fdir = os.path.join(work_dir, fdir)
    ff = sorted(Path(full_fdir).glob("frame_*.png"))[::skip]
    duration = 80 * skip
    out_path = os.path.join(output_dir, f"{name}.webp")

    print(f"{name:<35} ({len(ff)} frames, q={quality}, m={method})...", end=" ", flush=True)
    frames = [Image.open(f).convert("RGBA") for f in ff]
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        quality=quality,
        method=method,
        lossless=False,
        minimize_size=True,
    )
    size = os.path.getsize(out_path) / (1024 * 1024)
    marker = " ***" if size < 1.0 else ""
    print(f"{size:.2f} MB{marker}")
